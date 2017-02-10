
#will add these later from Daniel Ricks' github account
#import scholar.scholar as sch
#import penseur.penseur as penseur


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
	pass

    #GENERATION FUNCTIONS

    def getTopic(self):
	pass

    def buildBasicJoke(self):
	pass

    def optimizeJoke(self, joke):
        #executes one or more optimisers on
        #the joke, then returns the new version
        pass

    def createJoke(self, topic):
	topic = self.getTopic()
	joke = self.buildBasicJoke(topic)
	joke - self.optimizeJoke(joke)

	#pass the joke to espeak

	

	pass




