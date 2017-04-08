from __future__ import division, print_function

from multiprocessing import Pool

from finch.data_prep import batch_generator
import numpy as np
import penseur.penseur as penseur
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

pen = penseur.Penseur()
classifier = joblib.load('cache/random-forest-classifer.pkl')

def rate_joke(joke):
  print('joke', joke)
  vector = pen.get_vector(joke)

  rating = classifier.predict_proba(vector)

  return rating[0][1]


joke = u"Quarterback  Colin has done a complete 180. He now says he WILL stand for the national anthem. He's now sitting for the games, but he's standing for the anthem."

not_joke = u'The only advantage to this method is that the "order" argument is a list of the fields to order the search by. For example, you can sort by the second column, then the third column, then the first column by supplying order.'

print('rate_joke(joke)', rate_joke(joke))
print('rate_joke(not_joke)', rate_joke(not_joke))

def train_classifier():
  monologue_vectors = np.array([np.hstack((x[0], 1)) for x in joblib.load('data/monologue-joke-vectors.pkl')])

  reddit_vectors = []

  for i in range(60):
    reddit_vectors += joblib.load('data/reddit-batches/batch-{}.pkl'.format(str(i).zfill(3)))

  reddit_vectors = np.array([np.hstack((x[0], 0)) for x in reddit_vectors if x is not None])

  all_data = np.concatenate((monologue_vectors, reddit_vectors))

  np.random.shuffle(all_data)

  train = all_data[:, :-1]
  train_labels = all_data[:, -1]

  test = all_data[:, :-1]
  test_labels = all_data[:, -1]

  classifier = RandomForestClassifier(max_depth = 401).fit(train, train_labels)

  probabilities = classifier.predict_proba(test)
  print('classifier.score', classifier.score(test, test_labels))

  joblib.dump(classifier, 'cache/random-forest-classifer.pkl')

# def process_text(filename)
#   batch_size = 500
#   starting_batch = 15

#   with open(filename) as file:
#     sentences = [(i, sentence) 
#                  for i, sentence 
#                  in enumerate(file.readlines()) 
#                  if sentence.strip() != '' and 'http' not in sentence][batch_size*starting_batch:30000]

#   pen = penseur.Penseur()

#   def encode_sentence(x):
#     i, sentence = x
#     print('sentence', sentence)
#     try:
#       return pen.get_vector(sentence)
#     except:
#       return None

#   total_processed = 0

#   for batch_number, batch in enumerate(batch_generator(sentences, sentences, batch_size=batch_size)):
#     print('batch_number', batch_number + starting_batch)

#     pool = Pool(4)
#     vectors = pool.map(encode_sentence, batch[0])
#     pool.close()

#     total_processed += batch_size

#     print('total_processed', total_processed)
#     print('vectors', vectors)

#     joblib.dump(vectors, 'data/reddit-batches/batch-{}.pkl'.format(str(batch_number + starting_batch).zfill(3)))
