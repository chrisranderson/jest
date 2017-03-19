import conceptnetter.conceptNetter as cn
c = cn.ConceptNetter()

from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives
from nlp import print_tokens, lemmatize
import spacy

from censor import is_common_word, string_is_clean, filter_strings
from topic_generation import get_topics

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
  

def identify_handles(topic):
  tokenized = tokenize(topic)

  handles = list(tokenized.ents)
  handles += list(tokenized.noun_chunks)

  if len(handles) < 2:
    without_stop_words = remove_stop_words(tokenized)
    without_adverbs = remove_adverbs(without_stop_words)
    without_adjectives = remove_adjectives(without_adverbs)

    handles += without_adjectives

  return handles


def generate_punchline(topic):
  '''
  Possible approaches (examples needed):

  1 - handle associations
    - links between handle associations
    - angle to glue together.

  2 - handle associations and pop culture assocations
    - link between associations
    - angle to glue together

  3 - ask a question about the topic
    - answer using handle associations

  4 - handles and associations
    - play on words between associations
    - angle to glue together

  5 - visualize the topic

  6 - ask an obvious question
    - punch line based on obvious answer
    - connecting angle
  '''




if __name__ == '__main__':
  for topic in get_topics():
    print('--------------------------')
    print('topic', topic)
    print(identify_handles(topic))
