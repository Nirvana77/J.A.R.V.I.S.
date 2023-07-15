

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

def runCommand(res, userIntent=None):
	tag = res.get('tag')
	response = res.get('response')
	action = res.get('action')
	
	if action == 'none':
		voice.speak(response)
		return
	elif action == 'open':
		openApp()
	elif action == 'search':
		search()
	elif action == 'play':
		play()
	elif action == 'write':
		write()
	elif action == 'ask_chat_gpt':
		ask_chat_gpt()
	elif action == 'exit':
		exit()
	else:
		voice.speak('Sorry, I don\'t know how to do that yet.')

def openApp(query):
	voice.speak(f'Opening {query}...')
	webbrowser.open(f'https://www.{query}.com')

def search(query):
	voice.speak(f'Searching for {query} on Wikipedia...')
	results = wikipedia.summary(query, sentences=2)
	voice.speak('According to Wikipedia...')
	voice.speak(results)

def ask_chat_gpt():
	voice.speak('What is your question?')
	question = takeCommand()
	voice.speak('Searching...')
	answer = openai.ask_gpt3(question)
	voice.speak(answer)

def play(query):
	voice.speak(f'Playing {query} on YouTube...')
	webbrowser.open(f'https://www.youtube.com/results?search_query={query}')

def write():
	voice.speak('What do you want me to write?')
	text = takeCommand()
	voice.speak('Writing...')
	voice.write(text)

def run():
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

	ints = brain.predict_class("hey")
	res = brain.get_response(ints, intents)

	runCommand(res)