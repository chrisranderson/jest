from topic_generation import get_topics
from handles import identify_handles
from associations import concept_associations
from censor import is_english_word
from associations import get_associations

indent = '  '

print('Getting topics...')
topics = get_topics()
# topics = [u'adorable puppies']
for topic in topics:
  handles = identify_handles(topic)
  print('\n' + 'topic: ' + topic)

  if len(handles) > 1:

    for handle in handles:
      print(indent + 'handle: ' + str(handle))

      for association in concept_associations(handle):
      # for association in get_associations(handle) + concept_associations(handle):
        print(indent*2 + association)
