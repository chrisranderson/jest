import scholar.scholar as sch
import penseur.penseur as pens
import topic_generation
import random
import time
import nltk.data
import pickle
from punch_lines import *

#import sys
#sys.setrecursionlimit(10000)

#EVALUATION FUNCTIONS

def wildly_exaggerate(joke):
    pass

def alliterize(joke):
    pass


#JOKE MAXIMIZERS



class Comedian:
#not sure whether joke should be just a 
#string of text or a class with its oen
#properties and functions.

    def __init__(self):
        #print "Initializing scholar..."
        self.scholar = sch.Scholar()

        print "loading penseur data structure (this will take about 90 seconds...)"
        #with open('Wikipedia_first_10000_lines.pkl', 'rb') as handle:
        #    self.penseur = pickle.load(handle)
        self.penseur = pens.Penseur()
#
    #GENERATION FUNCTIONS

    def find_a_random_match(self, assoc_list):
        #for now, randomly match items from different lists
        #BUT WE WILL MAKE THIS SMARTER LATER!

        if len(assoc_list) == 0:
            return None

        #if len(assoc_list) == 1:
        if True:
            #match the list with itself
            word1 = 'a'
            word2 = 'a'
            while word1 == word2:
                word1 = random.choice(assoc_list[0])
                word2 = random.choice(assoc_list[0])
            return (word1, word2)

        else:
            #match items from two different sublists
            pass



    def find_a_match(self, assoc_list):
        #for now, randomly match items from different lists
        #BUT WE WILL MAKE THIS SMARTER LATER!
        return self.find_a_random_match(assoc_list)

    def getAssociations(self,handle):
        associations = []
        for h in handle:
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

    def buildBasicJoke(self, topic):
        handles = identify_handles(topic)
        print "\nHANDLES:"
        print handles

        associations = {}
        assoc_list = []
        for h in handles:
            associations = self.getAssociations(h)
            assoc_list.append(associations)
            print associations

        matched = self.find_a_match(assoc_list)
        print matched

        joke = ''
        #joke = self.penseur.get_closest_sentences(topic)[0]
        return joke

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

           #print self.scholar.get_words_by_rarity(topic)

           joke = self.createJoke(topic)

           print joke
           #(pass the joke to espeak?)
           time.sleep(1)

           response = raw_input("Want to hear another one?(y/n): ")
           
        "Okay, bye!"

c = Comedian()
c.begin()
