import pyttsx3

engine = pyttsx3.init()

# List all voices
voices = engine.getProperty('voices')
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name} - {voice.id}")

# Pick the first female voice
female_voice = None
for voice in voices:
    if "f" in voice.id.lower():  # usually 'english+f1', 'english+f2'
        female_voice = voice.id
        break

if female_voice:
    engine.setProperty('voice', female_voice)
else:
    print("No female voice found, using default.")

engine.say("Hello! This is a female voice.")
engine.runAndWait()
