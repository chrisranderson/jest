from topic_generation import get_topics
from punch_lines import identify_handles
from censor import is_english_word

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


################################################################################


indent = '  '

print('Getting topics...')
topics = get_topics()
topics = [u'A restaurant in Pennsylvania is making news for selling a hamburger with deep-fried twinkies instead of a bun.']
for topic in topics:
  handles = identify_handles(topic)
  print('\n' + 'topic: ' + topic)

  if len(handles) > 1:

    for handle in handles:
      print(indent + 'handle: ' + str(handle))

      for association in get_associations(handle):
        print(indent*2 + association)
