import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)   # speed
engine.setProperty('volume', 0.8) # volume (0.0 to 1.0)

engine.say("Hello, this is offline text to speech.")
engine.runAndWait()
