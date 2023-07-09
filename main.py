# https://www.youtube.com/watch?v=pVZN03sNRxc
# https://www.youtube.com/watch?v=RAKpMYOlttA
# https://www.youtube.com/watch?v=OqFI_g8vAoc

import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
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
greetings = ["Hello, sir.", "Greetings, sir.", "How can I assist you today?"]

def speak(text, rate=150):
	print(f'Jarvis: {text}')
	engine.setProperty('rate', rate)
	engine.say(text)
	engine.runAndWait()

def greet():
	return random.choice(greetings)

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

def ask_gpt3(prompt):
	response = openai.Completion.create(
		engine="davinci",
		prompt=prompt,
		temperature=0.7,
		max_tokens=100,
		top_p=1.0,
		frequency_penalty=0.0,
		presence_penalty=0.0,
		stop=None
	)
	return response.choices[0].text.strip()

def runCommand(query):
	command = query.pop(0)

	if command == 'search' and query[0] == 'for':
		query.pop(0)

		query = ' '.join(query)
		speak('According to Wikipedia')
		results = wikipedia.summary(query, sentences=2)
		speak(results)

	elif command == 'open':
		speak(f'Opening {query[0]}...')
		webbrowser.open(f'https://www.{query[0]}.com')

	elif command == 'ask' and query[0] == 'chat' and query[1] == 'gpt':
		speak('What is your question?')
		question = takeCommand()
		speak('Searching...')
		answer = ask_gpt3(question)
		speak(answer)

if __name__ == '__main__':
	greet()
	while True:
		query = takeCommand().lower()

		if any(phrase in query for phrase in activationPhrases):
			query = query.split()

			for phrase in activationPhrases:
				if ' '.join(query).startswith(phrase):
					query = query[len(phrase.split()):]
					break

			runCommand(query)

			while True:

				query = takeCommand().lower()

				for phrase in activationPhrases:
					if ' '.join(query).startswith(phrase):
						query = query[len(phrase.split()):]
						break

				if any(phrase in query for phrase in shutdownPhrases):
					speak('as you wish, sir. I will be here if you need me.')
					break
				else:
					runCommand(query.split())
		elif any(phrase in query for phrase in shutdownPhrases):
			break