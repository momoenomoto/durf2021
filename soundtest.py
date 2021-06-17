import os
import RPi.GPIO as GPIO
import time

CTR = 7
A = 8
B = 9
C = 10
D = 11
BUZ = 4

def beep_on():
	GPIO.output(BUZ, GPIO.HIGH)
def beep_off():
	GPIO.output(BUZ, GPIO.LOW)
	
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CTR,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(A,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(B,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(C,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(D,GPIO.IN,GPIO.PUD_UP)
GPIO.setup(BUZ,GPIO.OUT)

try:
	while True:
		if GPIO.input(CTR) == 0:
			while GPIO.input(CTR) == 0:
				time.sleep(0.01)
				os.system("arecord --device=hw:1,0 --format S16_LE --rate 44100 -c2 test.wav")
			os.system("\^C")
			os.system("aplay test.wav")
		else:
			pass
except KeyboardInterrupt:
	GPIO.cleanup()
	
#os.system("arecord --duration 5 --device=hw:1,0 --format S16_LE --rate 44100 -c2 test.wav")
#os.system("aplay test.wav")
