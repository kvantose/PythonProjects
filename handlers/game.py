from telebot import types
from loader import bot
from database import add_history
import random


@bot.message_handler(commands=['game'], func=lambda message: True)
def game(message):
    bot.send_message(message.chat.id, 'Вы запустили игру "Камень, ножницы, бумага"')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    stone = types.KeyboardButton('Камень')
    scissors = types.KeyboardButton('Ножницы')
    paper = types.KeyboardButton('Бумага')
    markup.add(stone, scissors, paper)
    bot.send_message(message.chat.id, 'Для того чтобы начать игру, вам надо выбрать один из предложенных вариантов',
                     reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def handle_game_choice(message):
        user_choice = message.text.lower()
        bot_choice = random.choice(['камень', 'ножницы', 'бумага'])

        if user_choice == 'камень' or user_choice == 'ножницы' or user_choice == 'бумага':
            result = determine_winner(user_choice, bot_choice)
            bot.send_message(message.chat.id, f'Вы выбрали: {user_choice}\nБот выбрал: {bot_choice}\n{result}')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, выберите один из предложенных вариантов.')

    def determine_winner(user_choice, bot_choice):
        if user_choice == bot_choice:
            res = 'Ничья!'
        elif (user_choice == 'камень' and bot_choice == 'ножницы') or \
                (user_choice == 'ножницы' and bot_choice == 'бумага') or \
                (user_choice == 'бумага' and bot_choice == 'камень'):
            res = 'Вы победили!'
        else:
            res = 'Вы проиграли!'
        add_history.writing_to_a_file(res)
        return res
