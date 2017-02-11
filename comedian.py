import scholar.scholar as sch
import penseur.penseur as pens
import topic_generation
import random
import time
import nltk.data

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
	#self.scholar = sch.Scholar() (not using this just yet)

	print "Initializing penseur..."

	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	fp = open("penseur/Wikipedia_first_10000_lines.txt")
	data = fp.read()
	sentences = "".join(tokenizer.tokenize(data))
	self.penseur = pens.Penseur()
	print "Encoding sentences"
	self.penseur.encode(sentences)
	#self.penseur.load('Wikipedia_first_10000_lines')

    #GENERATION FUNCTIONS

    def getTopic(self):
	topics = topic_generation.get_topics()
	return random.choice(topics)

    def buildBasicJoke(self, topic):
	#for now, our joke just consists of finding a sentence
	#in skip-thought space that is similar to the topic
	#
	#(Obviously, we will need to improve on this method)

	joke = self.penseur.get_closest_sentences(topic)[0]
	return joke

    def optimizeJoke(self, joke):
        #executes one or more optimisers on
        #the joke, then returns the new version
        pass

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

	   print self.scholar.get_words_by_rarity(topic)

	   joke = self.createJoke(topic)

	   print joke
	   #(pass the joke to espeak?)
	   time.sleep(1)

	   response = raw_input("Want to hear another one?(y/n): ")
	   

c = Comedian()
c.begin()

