# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 22:48:44 2020

@author: ophel
"""


"""Getting Started Example for Python 2.7+/3.3+"""

import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
import speech_recognition as sr
from subprocess import STDOUT, check_output
import mutagen
from mutagen.mp3 import MP3
import time

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
#session = Session(profile_name="adminuser")
#polly = session.client("polly")

polly = boto3.client('polly')

question = "<speak> Hello <break time='300ms'/> <prosody rate='85%'>  Your heart rate has increased a lot. If you are fine, could you please say : I'm fine  </prosody>  </speak>"
firstanswer= "<speak> <prosody rate='85%'> I'm happy to hear it. <break time='300ms'/> If you feel unwell, do not hesitate to contact your relatives and emergencies. </prosody> </speak>"
secondanswer = "<speak> <prosody rate='85%'> Do not worry. I call your relatives and emergencies. </prosody> </speak>"
problem = "<speak> <prosody rate='85%'> I do not understand. If you are fine, could you please say : I'm fine . </prosody> </speak>"


def createtext(text,file_name):
		
	try:
		# Request speech synthesis
		response = polly.synthesize_speech(Text=text, OutputFormat="mp3",VoiceId="Amy", TextType="ssml")
	except (BotoCoreError, ClientError) as error:
		# The service returned an error, exit gracefully
		print(error)
		sys.exit(-1)


	# Access the audio stream from the response
	if "AudioStream" in response:
    # Note: Closing the stream is important because the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be called automatically
    # at the end of the with statement's scope.
	
		try:
			body = response ['AudioStream'].read()
			    
			with open(file_name,'wb') as file:
				file.write(body)
				file.close()
							
                   
		except IOError as error:
            # Could not write to file, exit gracefully
			print(error)
			sys.exit(-1)

	else:
    		# The response didn't contain audio data, exit gracefully
		print("Could not stream audio")
		sys.exit(-1)

def createall() :
	createtext(question,"question.mp3")
	createtext(firstanswer,"firstanswer.mp3")
	createtext(secondanswer,"secondanswer.mp3")
	createtext(problem,"problem.mp3")

def playtext(file_name,player):
	
	if player :
		subprocess.call(["cvlc", "--play-and-exit", file_name])
		length_in_secs=0
	else :
		length_in_secs=2.5
		audio = MP3(file_name)
		audio_info = audio.info    
		length_in_secs = length_in_secs+int(audio_info.length)
				
		# Play the audio using the platform's default player
		if sys.platform == "win32":
			os.startfile(file_name)
	    
		else:
	    	# The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
			opener = "open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, file_name])
		
	return length_in_secs


def createandplaytext(text,file_name):
	createtext(text,file_name)
	playtext(file_name)

# dialog with the API and the person who fell
def play() :
	
	pb=0
	duration=playtext("question.mp3",1) #ask the question whether everything is OK
	time.sleep(duration) # waiting the end of the question
	r  = sr.Recognizer() # the speech recognition
	
	while pb<2 : # if the person says something not understandable 2 times, we call emergencies and relatives
		with sr.Microphone() as source:	#using the microphone
			r.adjust_for_ambient_noise(source)	
			audio = r.listen(source)
	
		try:
			text = r.recognize_google(audio, language='en-GB') #en-US, en-GB, fr-FR
			pb=5
			print("You said : " + text)
			if text.find("I'm fine")!=-1 or text.find('I am fine')!=-1 :
				playtext("firstanswer.mp3",1)#confirm the person is fine
				time.sleep(duration) #wait the end of the sentence
			else :
				playtext("secondanswer.mp3",1) #saying we call relatives and emergencies
				time.sleep(duration) #wait the end of the sentence

		except sr.UnknownValueError: 
			pb=pb+1 			
			print("Audio was not understood")
			if pb<2 : 
				duration=playtext("problem.mp3",1)#ask the person to repeat what he or she said
				time.sleep(duration) #wait the end of the question
			else :
				duration=playtext("secondanswer.mp3",1) #saying we call relatives and emergencies
				time.sleep(duration) #wait the end of the sentence

		except sr.RequestError as e:
			print("Google Speech API doesn't work" + format(e))
			pb=5

	


#createall()
#play()
