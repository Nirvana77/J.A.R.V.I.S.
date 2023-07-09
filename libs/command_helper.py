

from dotenv import load_dotenv
import libs.voice as voice
import libs.openai_helper as openai

import os
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import random
import openpyxl as xl

language = "en"

greetings = []
activationPhrases = []
shutdownPhrases = []

commands = {}

Responses_table = None
User_table = None
Commands_table = None

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

		if any(phrase in query for phrase in commands['activationPhrases'][0]):
			query = query.split()

			for phrase in commands['activationPhrases'][0]:
				if ' '.join(query).startswith(phrase):
					query = query[len(phrase.split()):]
					break

			runCommand(query)

			while True:

				query = takeCommand().lower()

				for phrase in commands['activationPhrases'][0]:
					if ' '.join(query).startswith(phrase):
						query = query[len(phrase.split()):]
						break

				if any(phrase in query for phrase in commands['shutdownPhrases'][0]):
					voice.speak('as you wish, sir. I will be here if you need me.')
					break
				else:
					runCommand(query.split())
		elif any(phrase in query for phrase in commands['shutdownPhrases'][0]):
			break

def init():
	load_dotenv()
	language = os.getenv('language')

	voice.init()

	wb = xl.load_workbook('commands.xlsx')
	User_table = wb['User']
	Responses_table = wb['Responses']
	Commands_table = wb['Commands']

	user = list(User_table.iter_rows(values_only=True))
	responses = list(Responses_table.iter_rows(values_only=True))

	# Extract the commands and responses
	for i, row in enumerate(Commands_table.iter_rows(values_only=True)):
		command_name = row[0]
		user_commands = [value for value in user[i] if value is not None]
		ai_responses = [value for value in responses[i] if value is not None]
		commands[command_name] = (user_commands, ai_responses)

	# Print the extracted commands and responses
	for command, (user_commands, ai_responses) in commands.items():
		print(f"Command: {command}")
		print(f"User Commands: {user_commands}")
		print(f"AI Responses: {ai_responses}")
		print()

	voice.speak(greet())