from chatterbot import ChatBot
from gtts import gTTS
import speech_recognition as sr
import wikipedia as wiki
import os
import re
import datetime
import webbrowser
import smtplib
import urllib.request
from urllib.parse import urlencode

bot = ChatBot('Bot')
flag=True

def audio_process(audio):
	tts = gTTS(text=audio, lang='en')
	tts.save("audio.mp3")

	os.system("mpg321 audio.mp3")

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
	if 'google' in command:
		audio_process('What should I search')
		query = chat_listen()
		url = "https://www.google.co.in/search?q=" +(str(query))+ "&oq="+(str(query))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
		webbrowser.open_new(url)
		
	elif 'website' in command:
		audio_process('tell me the name')
		web_name = chat_listen()
		reg_ex = re.search('(.+)', web_name)
		if reg_ex:
			domain = reg_ex.group(1)
			url = 'https://www.' + domain
			print("opening "+ url)
			webbrowser.open(url)

	elif 'youtube' in command:
		audio_process('tell me the video name')
		video_name = chat_listen()
		query_string = urlencode({"query" : video_name})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		result = "http://www.youtube.com/watch?v=" + search_results[0]
		print("opening "+ result)
		webbrowser.open_new(result)

	elif 'mail' in command or 'email' in command:
		audio_process('please write is the recipient?')
		recipient = input("Recipient: ")
		audio_process('What should I say?')
		content = chat_listen()
		mail = smtplib.SMTP('smtp.gmail.com', 587)
		mail.ehlo()
		mail.starttls()
		mail.login('username', 'password')
		mail.sendmail('username', recipient, content)
		mail.close()

		audio_process('The mail has been sent.')

	elif 'wiki' in command or 'wikipedia' in command:
		audio_process('tell me you query')
		query = chat_listen()
		try:
			audio_process("Processing...will take some time")
			audio_process(wiki.summary(query))
			
		except Exception as e:
			print(e)
			audio_process("I dont know about " + query)
			audio_process("Please come again")
	
	elif 'tell me the date' in command:
		now = datetime.datetime.now()
		today = now.strftime('%d %B')
		day = now.strftime('%a')
		audio_process("today is "+day+", "+today)

	elif command in ['bye', 'exit', 'quit', 'terminate', 'stop']:
		print("Sai: Bye...See you")
		audio_process('Bye, see you')
		exit()

	else:
		reply = bot.get_response(command)
		print("Sai:", reply)
		audio_process(str(reply))
		

audio_process("Hey there, How may I help you")
chat_bot(chat_listen())
while flag==True:
	audio_process("You want more help?, Please say")
	ans = chat_listen()
	if 'no' in ans or 'thank' in ans or 'bye' in ans:
		audio_process("Bye, see you")
		flag=False
	else:
		audio_process("how may I assist you")
		chat_bot(chat_listen())
		