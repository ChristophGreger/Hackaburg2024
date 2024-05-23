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

    r = sr.Recognizer()

    harvard = sr.AudioFile('my_recording.wav')
    with harvard as source:
        audio = r.record(source)

    try:
        print(r.recognize_bing(audio, language='de-DE'))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    print("end")
    break