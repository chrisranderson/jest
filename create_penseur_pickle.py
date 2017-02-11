import nltk.data
import penseur.penseur
import pickle

import sys
sys.setrecursionlimit(10000)

#loads and encodes sentences for penseur, then saves the
#penseur object as a pickle for faster loading.

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("Wikipedia_first_10000_lines.txt")
data = fp.read()
sentences = tokenizer.tokenize(data)
print sentences

p = penseur.penseur.Penseur()
print "preparing to encode"
p.encode(sentences)

print "preparing to pickle"
with open('Wikipedia_first_10000_lines.pkl', 'wb') as handle:
    pickle.dump(p, handle, protocol=pickle.HIGHEST_PROTOCOL)

