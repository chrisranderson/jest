import spacy
from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives
from nlp import print_tokens

from topic_generation import get_topics

def word_associations(word):
  '''
  
  '''


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
