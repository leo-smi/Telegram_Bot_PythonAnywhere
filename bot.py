from flask import Flask, request
import telebot
from telebot import types
from random import random
import requests

token = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url='https://YOUR_USER.pythonanywhere.com/')

app = Flask(__name__)
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
    
    
@bot.message_handler(commands=['start', 'help'])
def startCommand(message):
    bot.send_message(message.chat.id, 'Hi *' + message.chat.first_name + '*!' , parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    
    
@bot.message_handler(commands=['random'])
def rand(msg):
    bot.send_message(msg.chat.id, 'The random number is {:.4f}'.format(random()))
    
# this call is to test the whitelist    
@bot.message_handler(commands=['usd_eur'])
def usd_eur(msg):
    # Where USD is the base currency you want to use
    url = 'https://api.exchangerate-api.com/v4/latest/USD' #api.exchangerate-api.com is in the whitelist
    # Making our request
    response = requests.get(url)
    data = response.json()
    # Your JSON object
    bot.send_message(msg.chat.id, 'USD to EUR: {}'.format(data["rates"]["EUR"]))




    
