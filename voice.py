from random import shuffle

import pyttsx

engine = pyttsx.init()

voices = [x for x in engine.getProperty('voices') if x.id in ['default',
                                                              'english',
                                                              'en-scottish',
                                                              'english-north',
                                                              'english_rp',
                                                              'english_wmids',
                                                              'english-us',
                                                              'en-westindies']]

def say(something):
  
  gender = ''
  engine = pyttsx.init()
    engine.setProperty('voice', voice.id)
    print('voice.id', voice.id)
    engine.say(something)
  engine.say(something)
  engine.runAndWait()
