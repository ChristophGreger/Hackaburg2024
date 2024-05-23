import sounddevice as sd
import numpy as np
import RPi.GPIO as GPIO
import time
from scipy.io import wavfile
import speech_recognition as sr
import soundfile

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)

# Set the button pin
recording_button = 10
GPIO.setup(recording_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set the sample rate for the recording
sample_rate = 44100

def record() -> str:
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

    data, samplerate = soundfile.read('my_recording.wav')
    soundfile.write('my_recording.wav', data, samplerate, subtype='PCM_16')

    r = sr.Recognizer()

    harvard = sr.AudioFile('my_recording.wav')
    with harvard as source:
        audio = r.record(source)

    text = r.recognize_google(audio, language='de-DE')
    print("end")
    return text