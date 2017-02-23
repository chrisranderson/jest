import spacy
from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives
from nlp import print_tokens

from topic_generation import get_topics

def word_associations(word):
  '''
  
  '''


def identify_handles(topic):
  method = 3
  tokenized = tokenize(topic)

  if method == 1:
    without_stop_words = remove_stop_words(tokenized)
    without_adverbs = remove_adverbs(without_stop_words)
    without_adjectives = remove_adjectives(without_adverbs)
    return without_adjectives

  elif method == 2:
    return list(tokenized.noun_chunks)

  elif method == 3:
    return list(tokenized.ents)

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
