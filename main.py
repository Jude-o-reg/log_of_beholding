import speech_recognition as sr
import json

with open("rules.json","r") as f:
    rule_dictionary = json.load(f)

r = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")

            r.adjust_for_ambient_noise(source, duration=.5)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()
            print("You said:", text)

            if text.strip("\n") in rule_dictionary:
                print(rule_dictionary[text])

            if "exit" in text:
                print("Exiting program...")
                break

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("Could not understand audio")

    except KeyboardInterrupt:
        print("Program terminated by user")
        break
