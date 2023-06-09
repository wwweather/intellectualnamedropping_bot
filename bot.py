import telebot
import config
from telebot import types 

telegram_token = config.telegrambot_token
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['start','go', 'help'])
def start(message):
    bot.send_message(message.chat.id, text=f'Привет, {message.from_user.username}, поиграем?')
    markup_inline = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Правила игры", url='https://github.com/wwweather/intellectualnamedropping_bot/blob/main/README.md')
    btn2 = types.InlineKeyboardButton("Начать играть", callback_data='start_the_game')
    markup_inline.row(btn1, btn2)
    bot.reply_to(message, "Bot is avaliable.", reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda callback: True)
def go_to(callback):
    if callback.data == "start_the_game":
        bot.send_message(callback.from_user.id, text='Первый ход за тобой!')
    # bot.answer_callback_query(callback_query_id=callback.id)

@bot.message_handler(content_types=['text'])  # Ограничение по типу информации на входе
def handle_text(message):
    bot.reply_to(message, 'тривиальная обработка хода')

@bot.message_handler(content_types=['photo', 'video', 'audio'])  # Ограничение по типу информации на входе
def handle_all(message):
    bot.reply_to(message, "Нет, бот не принимает фотографии философов и записи их лекций в формате игры. Распознавать такие входные данные — ваша задача, господин-интеллектуал.")

bot.polling(none_stop=True) # Для нон-стоп работы
