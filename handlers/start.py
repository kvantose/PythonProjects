from telebot import types
from loader import bot


@bot.message_handler(commands=['start'], func=lambda message: True)
def welcome(message):
    """Функция приветствия"""
    bot.send_message(message.chat.id,
                     'Привет. Я новостной бот BBC. Я могу отправлять вам самые последние новости мира.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    three_news = types.KeyboardButton('3 новости')
    five_news = types.KeyboardButton('5 новостей')
    custom = types.KeyboardButton('Введите кол-во новостей')
    currency = types.KeyboardButton('Курс валют')
    markup.add(three_news, five_news, custom, currency)

    bot.send_message(message.chat.id, 'Выберите количество новостей, которые вы хотели бы увидеть.'
                                      , reply_markup=markup)
