#!/usr/bin/env python3

import pvporcupine
import struct
import pyaudio

from ctypes import *
from contextlib import contextmanager
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

porcupine = None
pa = None
audio_stream = None

def get_next_audio_frame():
	pass
	
try:
	handle = pvporcupine.create(keywords=['blueberry','porcupine'])
	with noalsaerr():
		pa = pyaudio.PyAudio()
	
	audio_stream = pa.open(
                    rate=handle.sample_rate,
                    channels=2,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=handle.frame_length)
	
	while True:
		pcm = audio_stream.read(handle.frame_length)
		pcm = struct.unpack_from("h" * handle.frame_length, pcm)
		keyword_index = handle.process(pcm)
		if keyword_index >= 0:
			print("detected")
			
finally:
	if porcupine is not None:
		porcupine.delete()

	if audio_stream is not None:
		audio_stream.close()

	if pa is not None:
		pa.terminate() 
