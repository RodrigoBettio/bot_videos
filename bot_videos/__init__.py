import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv(dotenv_path='../../.env')  

bot = telebot.TeleBot(os.getenv('CHAVE_API'))  

# Criar Teclado
markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
itembtn1 = KeyboardButton('Resumo Detalhado')
itembtn2 = KeyboardButton('Resumo Rápido')
markup.add(itembtn1, itembtn2)

# Mensagem de Start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Olá! Sou seu bot de resumo de vídeos. Escolha uma opção:", reply_markup=markup)

# Resumo Detalhado
@bot.message_handler(func=lambda message: message.text == 'Resumo Detalhado')
def resumo_detalhado(message):
    bot.send_message(message.chat.id, "Envie o vídeo que deseja resumir detalhadamente.")

# Resumo Rápido
@bot.message_handler(func=lambda message: message.text == 'Resumo Rápido')
def resumo_rapido(message):
    bot.send_message(message.chat.id, "Envie o vídeo que deseja resumir rapidamente.")

bot.polling()
