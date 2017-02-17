import spacy
from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives
from nlp import print_tokens

from topic_generation import get_topics

def word_associations(word):
  '''
  
  '''


def identify_handles(topic):
  method = 2
  tokenized = tokenize(topic)

  if method == 1:
    without_stop_words = remove_stop_words(tokenized)
    without_adverbs = remove_adverbs(without_stop_words)
    without_adjectives = remove_adjectives(without_adverbs)
    return without_adjectives

  elif method == 2:
    return list(tokenized.noun_chunks)


if __name__ == '__main__':
  for topic in get_topics():
    print('--------------------------')
    print('topic', topic)
    print(identify_handles(topic))
