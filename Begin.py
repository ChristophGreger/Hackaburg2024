import sounddevice as sd
import numpy as np
import RPi.GPIO as GPIO
import time
from scipy.io import wavfile
import speech_recognition as sr

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set the button pin
recording_button = 10
GPIO.setup(recording_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set the sample rate for the recording
sample_rate = 44100

while True:

    # Create a buffer for the recording
    buffer = np.array([])

    while True:  # Run forever
        if GPIO.input(recording_button) == GPIO.HIGH:  # If the button is pressed
            print("Button pressed! Recording...")
            # Record for 1 second
            myrecording = sd.rec(int(1 * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()  # Wait for the recording to finish
            # Append the recording to the buffer
            buffer = np.append(buffer, myrecording)
        else:  # If the button is not pressed
            if len(buffer) > 0:  # If there is a recording in the buffer
                print("Button released! Saving recording...")
                # Save the recording from the buffer
                wavfile.write('my_recording.wav', sample_rate, buffer)
                # Clear the buffer
                buffer = np.array([])
                break

    print("Datei Aufgenommen.")
    print("Jetzt kommt der Text, der drin ist:")

    import soundfile

    data, samplerate = soundfile.read('my_recording.wav')
    soundfile.write('my_recording.wav', data, samplerate, subtype='PCM_16')

    r = sr.Recognizer()

    harvard = sr.AudioFile('my_recording.wav')
    with harvard as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language='de-DE')
    print("end")

    from openai import OpenAI

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=300,
        temperature=0,
        messages=[
            {"role": "system",
             "content": "Frag immer nach, wenn du nicht sicher bist, welche Daten in eine Funktion einzufügen sind. Mache nie Annahmen. Stelle sicher, dass Tage vom Nutzer sicher festgelegt werden."},
            {"role": "user", "content": text}
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "bekunde_interesse",
                    "description": "Erlaubt es dem Nutzer, sich in eine Liste einzutragen, um eine Freizeitbeschäftigung zu machen.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "beschaftigung": {
                                "type": "string",
                                "description": "Die Beschäftigung, die der Nutzer machen möchte.",
                            },
                            "anfangsdatum": {
                                "type": "string",
                                "description": "Das Datum, ab dem der Nutzer die Beschäftigung gerne machen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Wenn nötig berechne das Datum anhand des aktuellen Datums. Heute ist der 21.April 2024"
                            },
                            "enddatum": {
                                "type": "string",
                                "description": "Das Datum, bis zu dem der Nutzer die Beschäftigung spätestens machen wollen würde. Beispiel: '10/11/2022' (DD/MM/YYYY). Berechne dabei das Datum anhand des aktuellen Datums, wenn nötig."
                            }
                        },
                        "required": ["beschäftigung", "enddatum", "anfangsdatum"],
                    },
                },
            }
        ]
    )

    print(completion.choices[0].message)


    break