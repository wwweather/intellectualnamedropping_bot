from flask import Flask, request
import telegram
import config
#import requests
from random import choice
from pathlib import Path
import re

bot_token = config.bot_token
bot = telegram.Bot(bot_token)

# working with data file consist of names (add some better analysis features of user inputs)

def getNextAvailableIndex(availableIndices, indicesSoFar):
    availableIndices.remove(indicesSoFar[-1])
    if len(availableIndices) > 0:
        return sorted(availableIndices)[0]
    else:
        return -1
def loadNamesFromFile():
    try:
        with open("names.txt") as file:
            names = [line.strip() for line in file]
    except FileNotFoundError:
        raise ValueError("Nameslist file not found.")
    if len(set(names)) != len(names):
        raise ValueError("Duplicate entries in nameslist file.")
        return names
    except FileNotFoundError:
        raise ValueError("Nameslist file not found.")

# interactions, interface

@bot.message_handler(commands=['start', 'go', 'help'])
def help(message):
    with open('https://github.com/wwweather/intellectualnamedropping_bot/blob/main/README.md', 'r') as rm:
    rules = rm.read()
    bot.send_message(callback.from_user.id, text=rules)
def start(message):
    bot.send_message(message.chat.id, text=f'Привет, {message.from_user.username}, поиграем?')
    markup_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Правила игры", callback_data='help')
    btn2 = types.InlineKeyboardButton("Начать играть", callback_data='start_the_game')
    markup_inline.row(btn1, btn2)
    bot.reply_to(message, "Bot is avaliable.", reply_markup=markup_inline)
def go(message):
    start()

# interface buttons callback

@bot.callback_query_handler(func=lambda callback: True)
def go_to(callback):
    if callback.data == "start_the_game":
        bot.send_message(callback.from_user.id, text='Первый ход за тобой!')
    elif callback.data == "help":
        help()
        
# content treatment

@bot.message_handler(content_types=['text']) 
def handle_move(message):
    loadNamesFromFile()
    global lastSelectedIndex
    if message in names:
        if lastSelectedIndex >= 0:
            nextIndex = getNextAvailableIndex([lastSelectedIndex], [i for i in range(len(names)) if i != lastSelectedIndex])
            if nextIndex < 0:
                raise ValueError("Все имена уже назывались! Пора сказать что-то новое, господин-философ!")
            this_move = names[nextIndex] + "\n"
            bot.send_message(callback.from_user.id, text=this_move)
        else:
            firstSelection = choice(names)
            this_move = firstSelection + "\n"
            bot.send_message(callback.from_user.id, text=this_move)
        lastSelectedIndex = len(names)-1
    else:
        bot.send_message(message.chat.id, "О ком вы вообще говорите?")

@bot.message_handler(content_types=['photo', 'video', 'audio']) 
def handle_all(message):
    bot.reply_to(message, "Нет, бот не принимает фотографии философов и записи их лекций в формате игры. Распознавать такие входные данные — ваша задача, господин-интеллектуал.")
      
if __name__ == '__main__':
    bot.polling(none_stop=True) # Для нон-стоп работы
    #loadNamesFromFile()
