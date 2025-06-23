import pyttsx3

text = input("Enter your text: ")
speaker = pyttsx3.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[0].id) # 0 for male, 1 = female
speaker.setProperty('rate',160)
speaker.say(text)
speaker.runAndWait()