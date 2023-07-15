

from dotenv import load_dotenv
import libs.voice as voice
import libs.openai_helper as openai
import libs.brain as brain
from libs.training import traing_model
import json

import os
import speech_recognition as sr
import wikipedia
import webbrowser
import random
import openpyxl as xl

language = "en"

intents = json.loads(open('intents.json').read())

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

def runCommand(query):
	command = query.pop(0)

	if command == 'search' and query[0] == 'for':
		query.pop(0)

		query = ' '.join(query)

		voice.speak(f'Searching for {query} on Wikipedia...')
		results = wikipedia.summary(query, sentences=2)
		voice.speak('According to Wikipedia')
		voice.speak(results)

	elif command == 'open':
		voice.speak(f'Opening {query[0]}...')
		webbrowser.open(f'https://www.{query[0]}.com')

	elif command == 'ask' and query[0] == 'chat' and query[1] == 'gpt':
		voice.speak('What is your question?')
		question = takeCommand()
		voice.speak('Searching...')
		answer = openai.ask_gpt3(question)
		voice.speak(answer)

def greet():
	return random.choice(commands['greetings'][1])

def run():
	while True:
		query = takeCommand().lower()

		if 'none' == query:
			continue
		else:
			ints = brain.predict_class(query)
			res = brain.get_response(ints, intents)
			voice.speak(res)


def init():
	load_dotenv()
	language = os.getenv('language')

	voice.init()
	
	#traing_model()

	ints = brain.predict_class("hey")
	res = brain.get_response(ints, intents)

	voice.speak(res)