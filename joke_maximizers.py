from associations import c
from nlp import lemmatize

def get_specific(sentence):
  words = sentence.lower().split(' ')

  for i, word in enumerate(words):
    word_info = c.look_up_word(lemmatize(word))

    print('word_info', word_info)

    for fact in word_info:
      first, relation, second = fact.split(' ')

      if relation == 'InstanceOf' and second == word:
        print('fact', fact)
        words[i] = first

  return ' '.join(words)


def wildly_exaggerate(joke):
    pass


def alliterize(joke):
    pass


if __name__ == '__main__':
  # print('lemmatize("cats")', lemmatize(u"cats"))
  print("get_specific(u'dog cat car')", get_specific(u'dog cat car'))
