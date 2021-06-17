#!/usr/bin/env python3

from ctypes import *
from contextlib import contextmanager
import struct
import pyaudio
import os
import time

import speech_recognition as sr
from gtts import gTTS
from io import BytesIO


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)
    
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()
    
def listen(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def get_next_audio_frame(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    return audio

if __name__ == "__main__":
    PROMPT_LIMIT = 5
    hotword = 'Hi'
    #pa = pyaudio.PyAudio()
    #handle = pvporcupine.create(keywords=['porcupine', 'blueberry'])
    
    #with noalsaerr():
    #    audio_stream = pa.open(
    #                rate=handle.sample_rate,
    #                channels=2,
    #                format=pyaudio.paInt16,
    #                input=True,
    #                frames_per_buffer=handle.frame_length)
    
    #engine = pyttsx3.init()
    #engine.setProperty('rate', 178)
    #engine.setProperty('voice', 'english_rp+f3')

    
    recognizer = sr.Recognizer()
    with noalsaerr():
        microphone = sr.Microphone(device_index=0)
    #while True:
        #keyword_index = handle.process(get_next_audio_frame(recognizer, microphone))
    #    pcm = audio_stream.read(handle.frame_length)
    #    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    #    keyword_index = handle.process(pcm)
    #    if keyword_index >= 0:
    #        print("Keyword detected")
    #       break
    start = time.time()
    gTTS('hello').save("hello.mp3")
    print(time.time() - start)
    os.system("play -q hello.mp3 pitch 100 speed 1.2")
    
    #speak(engine, "Hello!")
    for i in range(PROMPT_LIMIT):
        guess = listen(recognizer, microphone)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        print("I didn't catch that. Say again?")
    
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
    else:
        print(guess["transcription"])
    gTTS(guess["transcription"]).save("voice.mp3")
    os.system("play -q voice.mp3 pitch 100 speed 1.2")


    #gTTS(guess["transcription"]).save('voice.mp3')
    #os.system("aplay voice.mp3")
        #speak(engine, "I heard you say " + guess["transcription"])
    #handle.delete()

#os.system("aplay test.wav")
#pygame.mixer.init()
#pygame.mixer.music.load("test.wav")
#print("Playing wav file...")
#pygame.mixer.music.play()
#while pygame.mixer.music.get_busy() == True:
#    continue
