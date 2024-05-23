# Import the required module for text
# to speech conversion
from gtts import gTTS
from pydub import AudioSegment

# This module is imported so that we can
# play the converted audio
import pygame



def texttospeech(s: str):
    # Language in which you want to convert
    language = 'de'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    myobj = gTTS(text=s, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    # welcome
    myobj.save("abspielen.mp3")

    sound = AudioSegment.from_mp3("abspielen.mp3")
    sound.export("abspielen.wav", format="wav")

    pygame.mixer.init()
    pygame.mixer.music.load("abspielen.wav")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
