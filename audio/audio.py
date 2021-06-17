#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import stt, tts

class Chatbot:
    def __init__(self) -> None:
        self.listener = stt.Listener()
        self.speaker = tts.Speaker()

    def say(self, text, speed = 1):
        self.speaker.speak(text, speed = 1)
        
    def listen(self):
        return self.listener.listens()


if __name__ == "__main__":
    pi = Chatbot()
    pi.say("hello")
    while True:
        text = pi.listen()
        if text == "bye":
            pi.say("goodbye")
            exit()
        print(text)
        pi.say(text)
        

