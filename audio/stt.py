#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ctypes import *
from contextlib import contextmanager
import struct
import pyaudio
import speech_recognition as sr

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

class Listener():
    def __init__(self) -> None:
        recognizer = sr.Recognizer()
        with noalsaerr():
            microphone = sr.Microphone(device_index=0)

    def listen(self):
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
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
            
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
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        if response["transcription"]:
            return response["transcription"]
        elif not response["success"]:
            return response["error"]
        elif response["error"]:
            return response["error"]
        else:
            return "I didn't catch that. Say again?"

if __name__ == "__main__":
    #PROMPT_LIMIT = 10
    
    pi = Listener()
    print(pi.listen())

    # for i in range(PROMPT_LIMIT):
    #     response = listen(recognizer, microphone)
    #     if response["transcription"]:
    #         break
    #     if not response["success"]:
    #         break
    #     print("I didn't catch that. Say again?")
    
    # if response["error"]:
    #     print("ERROR: {}".format(response["error"]))
    # else:
    #     print(response["transcription"])
