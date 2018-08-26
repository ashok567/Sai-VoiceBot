from chatterbot import ChatBot
from gtts import gTTS
import speech_recognition as sr
import os

bot = ChatBot('Bot')

def audio_process(audio):
	tts = gTTS(text=audio, lang='en')
	tts.save("chat.mp3")

	os.system("mpg321 chat.mp3")

def chat_listen():
	r =sr.Recognizer()
	
	with sr.Microphone() as source:
		print("Please say something")
		r.adjust_for_ambient_noise(source,duration=1)
		audio = r.listen(source)

	try:
		print("processing...")
		command = r.recognize_google(audio).lower()
		print("You said: " +command+ "\n")
	except sr.UnknownValueError:
		audio_process("Didn't hear you. Please come again")
		command = chat_listen()
	return command

	
def chat_bot(command):
	if command in ['bye', 'exit', 'quit', 'terminate', 'stop']:
		print("Sai: Bye...See you")
		audio_process('Bye, see you')
		exit()
	else:
		reply = bot.get_response(command)
		print("Sai:", reply)
		audio_process(str(reply))
		


audio_process("Hey there, How may I help you")
while True:
	chat_bot(chat_listen())
