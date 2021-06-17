#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stt, tts

class Chatbot:
    def __init__(self) -> None:
        listener = stt.Listener()
        speaker = stt.Speaker()

if __name__ == "__main__":
    pi = Chatbot()
    while True:
        pi.speak(pi.listen())

