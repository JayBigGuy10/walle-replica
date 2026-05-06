import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} ({voice.id})")

engine.setProperty('voice', voices[26].id)

engine.say("Short speech")
engine.runAndWait()
