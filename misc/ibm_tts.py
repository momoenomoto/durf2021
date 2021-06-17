from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
#import vlc
import time

def speak_file(tts, text):
	try:
		with open('./speech.mp3','wb') as audio_file:
			audio_file.write(
				tts.synthesize(
					text, 
					accept='audio/mp3', 
					voice='en-US_AllisonV3Voice'
				).get_result().content)
		end = time.time()
		os.system("mpg123 -q speech.mp3")
		return end
	except Exception as e:
		print("TTS Error: {}".format(e)) 

def speak(player, instance, tts, text):
	media = instance.media_new(tts.synthesize(text,voice='en-US_AllisonV3Voice',accept='audio/wav').get_result().content)
	player.set_media(media)
	player.play()
	
if __name__ == '__main__':
	#define VLC instance
	#instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
	#Define VLC player
	#player=instance.media_player_new()
	#authenticator = IAMAuthenticator()
	#tts = TextToSpeechV1(authenticator=authenticator)
	tts = TextToSpeechV1()
	#tts.set_service_url()
	start = time.time()
	end = speak_file(tts, "<prosody pitch='high' rate='fast'>I am doing great! How are you today?</prosody>")
	#speak(player, instance, tts, 'I am doing great! How are you today?')
	print("Time elapsed: ",end-start)
	start = time.time()
	end = speak_file(tts, "<prosody pitch='x-low' rate='slow'>I'm not doing too well... Thanks for asking.</prosody>")
	print("Time elapsed: ",end-start)
