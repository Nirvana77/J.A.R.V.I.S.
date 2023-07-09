import pyttsx3

engine = None

def speak(text, rate=150):
	print(f'Jarvis: {text}')
	engine.setProperty('rate', rate)
	engine.say(text)
	engine.runAndWait()
		
def init():
	global engine  # Declare engine as global variable
	
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0].id)
	