from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot('Bot')
trainer = ListTrainer(bot)
# bot.set_trainer(ListTrainer)


for file in os.listdir('data/english'):
	
	training_data= open('data/english/'+ file, 'r').readlines()
	trainer.train(training_data)

