# https://www.youtube.com/watch?v=pVZN03sNRxc
# https://www.youtube.com/watch?v=RAKpMYOlttA
# https://www.youtube.com/watch?v=OqFI_g8vAoc

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import ecapture as ec
import wolframalpha
import json
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

language = "en"

openai.api_key = os.environ.get('api_key')

print('Loading your JARVIS...')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationPhrases = ['jarvis', 'hey jarvis', 'ok jarvis', 'hello jarvis', 'hi jarvis']
shutdownPhrases = ['goodbye', 'ok bye', 'stop', 'shut down', 'shutdown', 'exit', 'quit', 'bye']

def speak(text, rate=150):
	print(f'Jarvis: {text}')
	engine.setProperty('rate', rate)
	engine.say(text)
	engine.runAndWait()

def wishMe():
	hour = datetime.datetime.now().hour
	if hour >= 0 and hour < 12:
		speak('Good Morning Sir!')
	elif hour >= 12 and hour < 18:
		speak('Good Afternoon Sir!')
	else:
		speak('Good Evening Sir!')

	speak('I am JARVIS. How may I help you today?')

def takeCommand(pause_threshold = 2):
	r = sr.Recognizer()
	r.pause_threshold = pause_threshold
	with sr.Microphone() as source:
		print('Listening...')
		audio = r.listen(source)

	try:
		statement = r.recognize_google(audio, language=language)

		print(f'user said: {statement}\n')

	except Exception as e:
		print(e)
		return 'None'
	return statement

def ask_gpt3(question):
    # Step 1: send the conversation and available functions to GPT
    response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[
			{
			"role": "user",
			"content": question
			}
		],
		temperature=1,
		max_tokens=256,
		top_p=1,
		frequency_penalty=0,
		presence_penalty=0
	)
    return response.choices[0].message.content

def runCommand(query):
	command = query[0]

	if command == 'wikipedia':
		speak('Searching Wikipedia...')
		query = query.replace('wikipedia', '')
		results = wikipedia.summary(query, sentences=2)
		speak('According to Wikipedia')
		speak(results)
	
	elif command == 'open':
		speak(f'Opening {query[1]}...')
		webbrowser.open(f'https://www.{query[1]}.com')
	
	elif command == 'ask' and query[1] == 'chat' and query[2] == 'GTP':
		speak('What is your question?')
		question = takeCommand()
		speak('Searching...')
		answer = ask_gpt3(question)
		speak(answer)

if __name__ == '__main__':
	#wishMe()
	while True:
		query = takeCommand(pause_threshold = 1).lower()
		# Check if query contains any activation word
		if any(phrase in query.lower() for phrase in activationPhrases):
			query = query.split()

        # Remove the activation phrase from the query
			for phrase in activationPhrases:
				if ' '.join(query).lower().startswith(phrase):
					query = query[len(phrase.split()):]
					break

			runCommand(query)

			while True:

				query = takeCommand().lower()

				if any(phrase in query.lower() for phrase in shutdownPhrases):
					break
				else:
					runCommand(query.split())
		
			