import spacy
from spacy.parts_of_speech import ADV, ADJ, VERB

nlp = spacy.load('en')

def tokenize(text):
  return nlp(text)

def remove_stop_words(tokens):
  return [token for token in tokens if not token.is_stop]

def remove_part_of_speech(tokens, part):
  return [token for token in tokens if not token.pos == part]

def remove_adverbs(tokens):
  return remove_part_of_speech(tokens, ADV)

def remove_adjectives(tokens):
  return remove_part_of_speech(tokens, ADJ)

def print_tokens(tokens):
  for token in tokens:
    print('', )
    print('token', token)
    # print('token.pos', token.pos)
    print('token.dep_', token.dep_)
    # print('token.tag', token.tag)
    print('token.head', token.head)
    for child in token.children:
      print('  child', child)
    print('token.subtree', token.subtree)
    # print('token.norm', token.norm)
    # print('token.sentiment', token.sentiment)

def lemmatize(text):
  try:
    token = nlp(text)
  except TypeError as e:
    token = text
  try:
    return token[0].lemma_
  except AttributeError as e:
    print('e', e)
    return text
