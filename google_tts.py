from gtts import gTTS
import os

def text_to_audio(txt):
    filename = "audio.mp3"
    tts = gTTS(txt, 'en')
    tts.save(filename)
    os.system("mpg123 -q " + filename)