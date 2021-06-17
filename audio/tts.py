#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gtts import gTTS
import os

class Speaker():
    def say(text, speed = 1):
        gTTS(text).save("audio.mp3")
        os.system("play -q audio.mp3 speed " + str(speed))

if __name__ == "__main__":
    pi = Speaker()
    pi.say("I am happy", 1.4)
    pi.say("I am sad", 0.85)