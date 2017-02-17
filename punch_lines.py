import spacy
from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives
from nlp import print_tokens

def word_associations(word):
  '''
  
  '''


def identify_handles(topic):

  tokenized = tokenize(topic)
  without_stop_words = remove_stop_words(tokenized)
  without_adverbs = remove_adverbs(without_stop_words)
  without_adjectives = remove_adjectives(without_adverbs)

  print('', )

  print('without_stop_words', without_stop_words)
  print('without_adverbs', without_adverbs)
  print('without_adjectives', ' '.join(str(without_adjectives)))



  '''
  How do you identify the most important words or phrases in a sentence?
  '''


if __name__ == '__main__':
  test_topic = u"There's a crisp that looks just like Harambe and it's selling for a staggering sum"
  test_topic = u'Blundering homeowner hunting for keys accidentally traps his own arm in a toilet in bizarre video'

  identify_handles(test_topic)
