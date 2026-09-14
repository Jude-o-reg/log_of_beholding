import speech_recognition as sr
import json
import PySimpleGUI as sg
import threading
import webbrowser

with open("rules.json", "r") as f:
    rule_dictionary = json.load(f)

layout = [
    [sg.Text("Speech Recognition Status:", font=("Helvetica", 11, "bold"))],
    [sg.Text("Initializing...", key="-STATUS-", size=(40, 1), text_color="yellow")],
    [sg.Text("Recognized Text:", font=("Helvetica", 11, "bold"))],
    [sg.Text("None", key="-HEARD-", size=(40, 2))],
    [sg.Text("Rule Match:", font=("Helvetica", 11, "bold"))],
    # Clickable text displaying the rule name (key)
    [sg.Text("No match yet.", key="-MATCH-", size=(40, 2), enable_events=True, tooltip="Click to open link")],
    [sg.Button("Exit", size=(10, 1))]
]

window = sg.Window("Log of Beholding", layout, finalize=True)

# Store the matched URL separately
active_url = ""


def speech_recognition_loop(window):
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                window.write_event_value("-UPDATE_STATUS-", "Listening...")

                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                text = text.lower()

                window.write_event_value("-UPDATE_HEARD-", text)

                matched_key = text.strip("\n")
                if matched_key in rule_dictionary:
                    # Pass both key (rule name) and value (url) to the GUI
                    window.write_event_value(
                        "-UPDATE_MATCH-",
                        {"rule": matched_key, "url": rule_dictionary[matched_key]}
                    )

        except sr.RequestError as e:
            window.write_event_value("-UPDATE_STATUS-", f"Request Error: {e}")

        except sr.UnknownValueError:
            window.write_event_value("-UPDATE_STATUS-", "Could not understand audio")

        except KeyboardInterrupt:
            break


# Start the speech recognition thread
threading.Thread(target=speech_recognition_loop,
                 args=(window,),
                 daemon=True).start()

# Main GUI event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    if event == "-UPDATE_STATUS-":
        window["-STATUS-"].update(values[event])

    elif event == "-UPDATE_HEARD-":
        window["-HEARD-"].update(values[event])
        window["-STATUS-"].update("Processing complete. Listening again...")

    elif event == "-UPDATE_MATCH-":
        match_data = values[event]
        rule_name = match_data["rule"]
        active_url = match_data["url"]

        # Display the rule name and format as a clickable hyperlink
        window["-MATCH-"].update(
            value=rule_name,
            text_color="blue",
            font=("Helvetica", 10, "underline")
        )

    # Click handler for the rule text block
    elif event == "-MATCH-":
        if active_url and active_url.startswith(("http://", "https://")):
            webbrowser.open(active_url)

window.close()