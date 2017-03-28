from random import shuffle

import conceptnetter.conceptNetter as cn
c = cn.ConceptNetter()
import numpy as np

from censor import is_english_word, is_common_word, string_is_clean, filter_strings
from nlp import lemmatize

print('Importing scholar...')
import scholar.scholar as sch

print('Initializing Scholar...')
scholar = sch.Scholar()

def get_associations(handle):
    associations = set()

    for h in handle:
      word = h.lower_
      tags = ['_JJ', '_JJR', '_JJS', '_NN', '_VB', '_NNP', '_NNPS', 'NNS', 'UH']

      for tag in tags:

        if scholar.exists_in_model(word + tag):
          indexes, metrics = scholar.model.cosine(word + tag)
          response = scholar.model.generate_response(indexes, metrics, 5)

          for r in response:
            associations.add(r[0][:r[0].index('_')])

    return [word for word in list(associations) if is_english_word(word)][:10]

def concept_associations(handle):
  '''
  This needs to be cultural knowledge.
  Urban dictionary?
  '''
  important_relations = ['CapableOf', 'Desires', 'RelatedTo', 'DefinedAs']


  associations = set()

  for word in str(lemmatize(handle)).lower().split(' '):
    if 'trump' in word:
      word = 'president'

    if is_common_word(word):
      continue

    try:
      word_information = c.look_up_word(word)
    except KeyError as e:
      continue

    for relation in important_relations:
      associations = associations.union([fact.lower().split(' ')[-1].replace('_', ' ')
                                        for fact 
                                        in word_information 
                                        if relation in fact and
                                           string_is_clean(fact)])

  return sorted(filter_strings(list(associations)))

def n_maximally_distant_points(points_to_consider, n=10):
  '''
  points: list of np arrays

  returns: a list of indices of the most distant points
  '''
  if len(points_to_consider) <= n:
    return range(n)
  
  import kmc2
  seeding = kmc2.kmc2(np.array(points_to_consider), n)
  reverse_index = {str(value): index for index, value in enumerate(points_to_consider)}
  indexes = [reverse_index[str(x)] for x in seeding]
  return indexes

  # old implementation that gives things around the border
  # if len(points_to_consider) <= n:
  #   return range(n)

  # selected_indices = {0}

  # while len(selected_indices) < n:

  #   biggest_distance = float(0)
  #   new_point_index = -1

  #   for i, point_to_consider in enumerate(points_to_consider): 
  #     if i in selected_indices:
  #       continue

  #     point_distance_to_selected = 0

  #     for selected_index in selected_indices:
  #       distance = np.sqrt(np.sum((points_to_consider[selected_index] - point_to_consider)**2))
  #       point_distance_to_selected += distance

  #     if point_distance_to_selected > biggest_distance:
  #       biggest_distance = point_distance_to_selected
  #       new_point_index = i

  #   selected_indices.add(new_point_index)

  # return list(selected_indices)


if __name__ == '__main__':
  from finch.viz import scatter_plot

  data = np.random.standard_normal((2, 5000)).T.tolist()
  selected_indices = n_maximally_distant_points([np.array(x) for x in data], n=50)
  selected_points = np.array(data)[selected_indices]

  scatter_plot(np.array(data)[:, 0], np.array(data)[:, 1], title='original')
  scatter_plot(selected_points[:, 0], selected_points[:, 1], title='selected')
