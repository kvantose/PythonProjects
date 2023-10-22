from telebot import types
from loader import bot


@bot.message_handler(commands=['help'], func=lambda message: True)
def helper(message):
    bot.send_message(message.chat.id, '/start - запуск бота'
                                      '\n/history - показывает историю последних 10-ти запросов'
                                      '\n/clear - очищает историю'
                                      '\n/game - запуск игры "Камень, ножницы, бумага"')
