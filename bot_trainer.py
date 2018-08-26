from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('Bot')
bot.set_trainer(ListTrainer)


for file in os.listdir('/home/ashok/Desktop/SaiBot/chatterbot-corpus/chatterbot_corpus/data/english'):
	
	training_data= open('/home/ashok/Desktop/SaiBot/chatterbot-corpus/chatterbot_corpus/data/english/'+ file, 'r').readlines()
	bot.train(training_data)

