

from dotenv import load_dotenv
import libs.voice as voice
import libs.openai_helper as openai
import libs.brain as brain
from libs.training import traing_model
import json
import threading
import time

import os
import speech_recognition as sr
import wikipedia
import webbrowser
import random
import openpyxl as xl

language = "en"

intents = json.loads(open('intents.json').read())

standby = True

def takeCommand(pause_threshold=1):
	r = sr.Recognizer()
	r.pause_threshold = pause_threshold
	with sr.Microphone() as source:
		audio = r.listen(source)

	try:
		statement = r.recognize_google(audio, language=language)
		print(f'user said: {statement}\n')

	except Exception as e:
		print(e)
		return 'None'
	
	return statement

def runCommand(res, userIntent=None):
	tag = res.get('tag')
	response = res.get('response')
	action = res.get('action')
	global standby
	
	if action == 'start':
		if standby == True:
			voice.speak(response)
		else:
			voice.speak('I am already awake.')
		standby = False
		return
	elif action == 'exit':
		if standby == True:
			shutdown()
		else:
			standby = True
			voice.speak('I will enter standby mode´.')
		return
	elif action == 'shutdown':
		shutdown()
		return
	
	if standby == True:
		return
	
	if action == 'none':
		if response != "":
			voice.speak(response)
		return
	elif action == 'train':
		voice.speak('Training with the new data')
		threading.Thread(target=traing.traing_model).start()
		return
	elif response != "":
		voice.speak(response)
	
	
	if action == 'ask_chat_gpt':
		ask_chat_gpt()
	else:
		voice.speak('Sorry, I don\'t know how to do that yet.')

def ask_chat_gpt():
	voice.speak('What is your question?')
	question = takeCommand()
	voice.speak('Searching...')
	answer = openai.ask_gpt3(question)
	voice.speak(answer)

def shutdown():
	voice.speak('Goodbye!')
	my_thread.join()
	exit()

def my_thread_function():
	while True:
		# do something here ...
		print('thread')
		time.sleep(1)

my_thread = threading.Thread(target=my_thread_function)

def run():
	# start an other thread
	my_thread.start()

	while True:
		query = takeCommand().lower()

		if 'none' == query:
			continue
		else:
			ints = brain.predict_class(query)
			res = brain.get_response(ints, intents)
			runCommand(res)


def init():
	load_dotenv()
	language = os.getenv('language')

	voice.init()
	
	#traing_model()