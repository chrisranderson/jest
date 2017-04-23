#import scholar.scholar as sch
import penseur.penseur as pens
import topic_generation
import random
import time
import nltk.data
import pickle
from handles import identify_handles
import numpy as np
import skipthought_decode_helper
import censor
from associations import n_maximally_distant_points 
from associations import concept_associations
from evaluate import rate_joke
import scipy.spatial.distance as scipy_distance
import sys

#import sys
#sys.setrecursionlimit(10000)


def nearest_skipthought_match(sentence, input_file, penseur):
     print "Attempting to open input file"
     sys.stdout.flush()
     f = open(input_file, 'r')
     try:
         v1 = penseur.encode(sentence)
     except:
	print "ERROR ENCODING SENTENCE:"
        sys.stdout.flush()
	print sentence
        print type(sentence)
        sys.stdout.flush()
	
     cosine_similarity = 0
     nearest_match = ''
     print "HERE"
     sys.stdout.flush()
     for line in f:
	try:
	    v2 = penseur.encode(line)
	except:
	    print "ERROR ENCODING SENTENCE FROM TEXT CORPUS:"
            sys.stdout.flush()
	    print line
	    print type(line)
            sys.stdout.flush()
	new_similarity = 1 - scipy_distance.cosine(v1,v2)
	print "HERE2"
        sys.stdout.flush()
	if new_similarity > cosine_similarity:
	    cosine_similarity = new_similarity
            nearest_match = line
	print "HERE3"
        sys.stdout.flush()

     return cosine_similarity, nearest_match


class Comedian:
#not sure whether joke should be just a 
#string of text or a class with its oen
#properties and functions.

    def __init__(self):
        #print "Initializing scholar..."
        #self.scholar = sch.Scholar()

        print "loading penseur data structure (this will take about 90 seconds...)"
        #with open('Wikipedia_first_10000_lines.pkl', 'rb') as handle:
        #    self.penseur = pickle.load(handle)
        self.penseur = pens.Penseur()
        #self.decode_helper = skipthought_decode_helper.decode_helper('MONOLOGUE_PLUS_REDDIT_JUMBLED', self.penseur)
        #self.decode_helper = skipthought_decode_helper.decode_helper('larry_king_processed', self.penseur)
        #self.decode_helper = skipthought_decode_helper.decode_helper('reddit', self.penseur)
        
	#self.decode_helper = skipthought_decode_helper.decode_helper('larry_king_processed_LONG', self.penseur)
        self.decode_helper = skipthought_decode_helper.decode_helper('REDDIT_LONG2b', self.penseur)
 
    #GENERATION FUNCTIONS


    def score_match(self, match):
        #score word pairs based on interest level...
        score = 0
        word1 = match[0] + '_' +  self.scholar.get_most_common_tag(match[0])
        word2 = match[1] + '_' + self.scholar.get_most_common_tag(match[1])

        #low score for synonyms - we want words with different connotations
        print self.scholar.get_cosine_similarity(word1, word2)
        dist = self.scholar.get_cosine_similarity(word1,word2)
        print "COSINE SIMILARITY: %f" % (dist)
        score += (1-dist)

        #high score if one of the words is a proper noun?

        #high score if one or both words has an emotional connotation

        #high score if it's a verb/noun or adj/noun pair?

        #high score if both words are common
        #(Common words tend to appear near the mean of the vector space)
#        mean_vector = np.mean(self.scholar.model.vectors)
#        diff = abs(self.scholar.model[word1].dot(mean_vector)) + abs(self.scholar.model[word2].dot( mean_vector))
#        print "NOVELTY SCORE: %f" % (diff)
#        score += diff

        #high score if the words have a high difference in length
        length_diff = abs(len(match[0]) - len(match[1])) / max(len(match[0]), len(match[1]))
        print "LENGTH DISTANCE: %i" % (length_diff)
        score += length_diff


        #print "match %i" % score
        return score

    def find_a_random_match(self, association_lists):
        #randomly match items from different lists
    
        if len(association_lists) == 0:
            return None

        #only one list, so we match it with itself
        word1 = 'empty'
        word2 = 'empty'
        counter = 0
        MAX_ITERATIONS = 100

        while ((word1 == word2) or word1 == 'empty' or word2 == 'empty') and counter < MAX_ITERATIONS:
            assoc_list1 = random.choice(association_lists)
            assoc_list2 = random.choice(association_lists)
            if len(assoc_list1) != 0:
                word1 = random.choice(assoc_list1)
            if len(assoc_list2) != 0:
                word2 = random.choice(assoc_list2)
            counter += 1

	if word1 == 'empty':
	    return None
        if word2 == 'empty':
	    return None

        return (word1, word2)

    def filterAssociations(self, associations):
        #prune any associations that aren't in the word2vec listings
	#also prune options that are too short

	filtered_associations = []
        for word in associations:
            tagged_word = word + '_' +  self.scholar.get_most_common_tag(word)
            if self.scholar.exists_in_model(tagged_word) and len(word) >= 3:

		if censor.is_english_word(word):
                    filtered_associations.append(word)
	return filtered_associations

    def find_a_match(self, assoc_list):
        #for now, randomly match items from different lists
        #BUT WE WILL MAKE THIS SMARTER LATER!
        return self.find_a_random_match(assoc_list)

    def getAssociations(self,handle):
        associations = []
        for h in handle:
            if type(h) == unicode:
                word = h
            else:
                word = h.lower_
            tags = ['_JJ', '_JJR', '_JJS', '_NN', '_VB', '_NNP', '_NNPS', 'NNS', 'UH']
            for tag in tags:
                if self.scholar.exists_in_model(word+tag):
                    indexes, metrics = self.scholar.model.cosine(word + tag)
                    response = self.scholar.model.generate_response(indexes, metrics, 5)
                    for r in response:
                        #strip tags and append to list
                        associations.append(r[0][:r[0].index('_')])
        return associations


    def getTopic(self):
        topics = topic_generation.get_topics()
        return random.choice(topics)

    def getAssociationMatch(self, topic):
        handles = identify_handles(topic)
        if len(handles) < 1:
            #print "\nNot enough handles found. switching to get_words_by_rarity"
            handles = self.scholar.get_words_by_rarity(topic)
        print "\nHANDLES:"
        print handles

        #associations = {}
        #association_lists = []
        #for h in handles:
        #    associations = self.getAssociations(h)
        #    association_lists.append(self.filterAssociations(associations))
        #    print association_lists[-1]

	association_lists = []
        for h in handles:
            associations = concept_associations(h)
	    #print "ASSOCIATIONS"
	    #print associations
            #association_lists.append(self.filterAssociations(associations))

	    #get vectors for each of the associations,
            #then pass it to Chris's function to find
            #maximally distinct options
	    NUM_ASSOCIATIONS = 10
	    if len(associations) > NUM_ASSOCIATIONS:
	        assoc_vectors = []
                for a in associations:
	            a = ''.join(word.strip(':;()[]-.?!,') for word in a)
                    v = self.penseur.get_vector(a)
                    assoc_vectors.append(v[0])

		#print assoc_vectors
		#raw_input("pause")
		#print assoc_vectors.shape
	        indices = n_maximally_distant_points(assoc_vectors, NUM_ASSOCIATIONS)
	        final_associations = np.array(associations)[indices]
                association_lists.append(final_associations.tolist())
	        #print "ASSOCIATION LISTS [-1]"
                #print association_lists[-1]


        #print "\n MATCHED ASSOCIATIONS:"
        matched = self.find_a_match(association_lists)
        #matched = self.find_a_match(association_lists)
	return matched

    def buildBasicJoke(self, topic, matched, desired_output=5):

	#print "Building basic joke."
	#print "Matched = "
	#print matched

	if matched == None:
		return 0

	if len(matched) < 2:
	    print "len(matched) < 2"
	    return 'empty'
        #word1 = matched[0] + '_' +  self.scholar.get_most_common_tag(matched[0])
        #word2 = matched[1] + '_' + self.scholar.get_most_common_tag(matched[1])
        #print self.scholar.get_cosine_similarity(word1, word2)
        #print self.score_match(matched)

        #primitive_joke_structure = Topic + matched[0] + matched[1]

        #find the embedded location of primitive_joke
        #decode that location to form a grammatically complete sentence (?)

	#print "creating output list"
	output = ['','','','','','','','','','','','','','']

	if desired_output == 1:
	    input1 = matched[0] + ' ' + matched[1]
            target_vector = self.penseur.get_vector(input1)
	    output[1] = self.decode_helper.decode(target_vector)
            #print "\nINPUT1: " + input1
            #print "OUTPUT: " + output[1]
	
	if desired_output == 2:
	    input2 = matched[1] + ' ' + matched[0]
            target_vector = self.penseur.get_vector(input2)
	    output[2] = self.decode_helper.decode(target_vector)
            #print "\nINPUT2: " + input2
            #print "OUTPUT: " + output[2]
	
	if desired_output == 3:
	    input3 = matched[0] + ' ' + matched[1] + ' ' +  matched[0] + ' ' + matched[1] + ' ' + matched[0] + ' ' + matched[1] + '.'
            target_vector = self.penseur.get_vector(input3)
	    output[3] = self.decode_helper.decode(target_vector)
            #print "\nINPUT3: " + input3
            #print "OUTPUT: " + output[3]
	
	if desired_output == 4:
            input4 = topic
            target_vector = self.penseur.get_vector(input4)
	    output[4] = self.decode_helper.decode(target_vector)
            #print "\nINPUT4: " + input4
            #print "OUTPUT: " + output[4]
        
        if desired_output == 5:
	    input5 = matched[0] + ' ' + matched[1] + ' ' + topic
            target_vector = self.penseur.get_vector(input5)
	    output[5] = self.decode_helper.decode(target_vector)
            #print "\nINPUT5: " + input5
            #print "OUTPUT: " + output[5]
        
        if desired_output == 6:
	    input6 = topic + ' ' + matched[0] + ' ' + matched[1]
            target_vector = self.penseur.get_vector(input6)
	    output[6] = self.decode_helper.decode(target_vector)
            #print "\nINPUT6: " + input6
            #print "OUTPUT: " + output[6]
        
	if desired_output == 7:
	    #use linear algebra to find the phrase we're looking for
            target_vector = self.penseur.get_vector(topic) + 0.3 * self.penseur.get_vector(matched[0])
	    output[7] = self.decode_helper.decode(target_vector)
            #print "\nINPUT6: " + input6
            #print "OUTPUT: " + output[6]
	
	if desired_output == 8:
	    #use linear algebra to find the phrase we're looking for
            target_vector = self.penseur.get_vector(topic) + 0.3 * self.penseur.get_vector(matched[1])
	    output[8] = self.decode_helper.decode(target_vector)
            #print "\nINPUT6: " + input6
            #print "OUTPUT: " + output[6]
	
	if desired_output == 9:
	    #use linear algebra to find the phrase we're looking for
            target_vector = 0.1 * self.penseur.get_vector(topic) + self.penseur.get_vector(matched[1])
	    output[9] = self.decode_helper.decode(target_vector)
            #print "\nINPUT6: " + input6
            #print "OUTPUT: " + output[6]
	
	if desired_output == 10:
	    #use linear algebra to find the phrase we're looking for
            target_vector = 0.1 + self.penseur.get_vector(topic) + self.penseur.get_vector(matched[0]) + self.penseur.get_vector(matched[1])
	    output[10] = self.decode_helper.decode(target_vector)
            #print "\nINPUT6: " + input6
            #print "OUTPUT: " + output[6]

        #print "\n"
	
	my_joke = topic + ' ' + output[desired_output]
	#print "about to return " + my_joke.encode('UTF-8')
		
	return my_joke.encode('UTF-8')

    def optimizeJoke(self, joke):
        #executes one or more optimisers on
        #the joke, then returns the new version
        return joke

    def createJoke(self, topic):
        joke = self.buildBasicJoke(topic)
        joke = self.optimizeJoke(joke)

        return joke


    def begin(self):
        print "\nI'm going to tell you a joke:"
        time.sleep(1)

        response = 'y'
        while response == 'y':
           topic = self.getTopic()
           print "\nTopic is '" + topic + "'"

           #joke = self.createJoke(topic)

           topic = self.getTopic()
	   matched = self.getAssociationMatch(topic)
	   joke = self.buildBasicJoke(topic,matched, 9)
	   joke = self.buildBasicJoke(topic,matched, 10)

           print joke
           #(pass the joke to espeak?)
           time.sleep(1)

           response = raw_input("Want to hear another one?(y/n): ")
           
        "Okay, bye!"


    def create_lotsa_jokes(self):
	jokes = []
	scores = []
	for i in range(100):
	
	    if i%1 == 0:
		print "\n\n***********************"
		print "Iteration " + str(i)
		print "***********************"

	    try:
                topic = self.getTopic()
	        print "\n\nTOPIC: "
	        sys.stdout.flush()
	        print topic
	        sys.stdout.flush()
	        matched = self.getAssociationMatch(topic)
	        print "ASSOCIATIONS: "
	        print matched
	        sys.stdout.flush()

	        joke = self.buildBasicJoke(topic,matched, 1)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 2)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 4)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 5)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 6)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)

	        """joke = self.buildBasicJoke(topic,matched, 7)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 8)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	    
                joke = self.buildBasicJoke(topic,matched, 9)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)
	        joke = self.buildBasicJoke(topic,matched, 10)
                score = rate_joke(joke, self.penseur)
	        print '\n' + str(score) + " " + joke
	        sys.stdout.flush()
	        jokes.append(joke)
                scores.append(score)"""

	    except FloatingPointError:
		print "Empty associations. Proceeding to next topic..."
	    except:
		print "Error- 'ascii' codec can't encode characters in topic. Moving on."

	    #print "\nSORTED JOKES:"
	    #joke_list = [joke for (score,joke) in sorted(zip(scores,jokes))]	
	    #score_list = [score for (score,joke) in sorted(zip(scores,jokes))]	
	    #for j in range(len(joke_list)):
	    #    print str(score_list[j]) + ": " + joke_list[j]

	return jokes, scores


c = Comedian()
#c.begin()
jokes, scores = c.create_lotsa_jokes()
joke_list = [joke for (score,joke) in sorted(zip(scores,jokes))]	
score_list = [score for (score,joke) in sorted(zip(scores,jokes))]	

print "Writing joke output file..."
print len(joke_list)
print len(score_list)
f1 = open('comedian_REDDIT_LONG2b_100_jokes.txt', 'w')
for j in range(len(joke_list)):
    f1.write(str(score_list[j]) + ": " + joke_list[j] + '\n')
f1.close()

#check how close they are to the dataset
print "Writing dataset correlation file..."
sys.stdout.flush()
f2 = open('comedian_REDDIT_LONG2b_100_jokes_nearest_match.txt', 'w')
print "File opened..."
sys.stdout.flush()
for j in joke_list:
   #cosine_distance, matching_sentence = nearest_skipthought_match(j, 'data/reddit-comments-filtered-processed-truncated-LONG.txt', c.penseur)
   print "here1"
   sys.stdout.flush()
   cosine_distance, matching_sentence = nearest_skipthought_match(j, 'data/reddit-comments-filtered-processed-truncated.txt', c.penseur)
   print "here2"
   sys.stdout.flush()
   f2.write(str(cosine_distance) + j + ":::" + matching_sentence + '\n')
f2.close()
