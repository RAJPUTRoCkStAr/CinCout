import pyttsx3

def tts(text):
    engine =  pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 175)   # getting details of current speaking rate                
    engine.say(text)
    engine.runAndWait()