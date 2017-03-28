from nlp import tokenize, remove_stop_words, remove_adverbs, remove_adjectives

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

if __name__ == '__main__':
  print('identify_handles("I went to the store and bought a puppy."', identify_handles(u"I went to the store and bought a puppy."))
