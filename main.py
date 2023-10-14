import requests
import json
import telebot
from telebot import types
import time
import schedule
from datetime import datetime
import random
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
sent_news = set()


@bot.message_handler(commands=['help'], func=lambda message: True)
def helper(message):
    bot.send_message(message.chat.id, '/start - запуск бота'
                                      '\n/history - показывает историю последних 10-ти запросов'
                                      '\n/clear - очищает историю'
                                      '\n/game - запуск игры "Камень, ножницы, бумага"')


@bot.message_handler(commands=['history'], func=lambda message: True)
def check_history(message):
    with open('urlbase.log', 'r', encoding='utf-8') as file:
        for line in file:
            bot.send_message(message.chat.id, line.strip())


@bot.message_handler(commands=['clear'], func=lambda message: True)
def clear_history(message):
    with open('urlbase.log', 'w', encoding='utf-8'): pass
    bot.send_message(message.chat.id, 'История очищена')


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
        writing_to_a_file(res)
        return res


@bot.message_handler(commands=['start'], func=lambda message: True)
def welcome(message):
    """Функция приветствия"""
    bot.send_message(message.chat.id,
                     'Привет. Я новостной бот BBC. Я могу отправлять вам самые последние новости мира.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    three_news = types.KeyboardButton('3')
    five_news = types.KeyboardButton('5')
    custom = types.KeyboardButton('Введите кол-во новостей')
    sub = types.KeyboardButton('Подписаться на рассылку новостей')
    markup.add(three_news, five_news, custom, sub)

    bot.send_message(message.chat.id, 'Выберите количество новостей, которые вы хотели бы увидеть.'
                                      'Так же вы можете подписаться на ежедневную рассылку новостей нажав на кнопку'
                                      '"Подписаться на рассылку"', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '3')
def send_three_news(message):
    """Функция отправки трех новостей"""
    send_news(message.chat.id, 3)


@bot.message_handler(func=lambda message: message.text == '5')
def send_five_news(message):
    """Функция отправки пяти новостей"""
    send_news(message.chat.id, 5)


@bot.message_handler(func=lambda message: message.text == 'Введите кол-во новостей')
def ask_custom_num(message):
    """Функция запроса пользовательского количества новостей"""
    bot.send_message(message.chat.id, 'Введите количество новостей, которые вы хотели бы увидеть')


@bot.message_handler(func=lambda message: message.text.isdigit())
def send_custom_news(message):
    """Функция отправки пользовательского количества новостей"""
    num_messages = int(message.text)
    send_news(message.chat.id, num_messages)


@bot.message_handler(func=lambda message: message.text == 'Подписаться на рассылку новостей')
def subscribe(message):
    """Функция подписки"""
    bot.send_message(message.chat.id, 'Хорошо! Теперь я буду отправлять вам по 3 новости каждый день в 14:00')
    schedule_news()


def send_news(chat_id, num_messages):
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        json_data = response.json()
        articles = json_data['articles']
        sent_messages = 0
        for article in articles:
            if sent_messages >= num_messages:
                break
            if 'title' in article and 'url' in article:
                title = article['title']
                url = article['url']
                if title not in sent_news:
                    bot.send_message(chat_id, f'{title}\n{url}')
                    sent_news.add(title)
                    sent_messages += 1a
                    writing_to_a_file(title)
        if sent_messages == 0:
            bot.send_message(chat_id, 'Нет доступных новостей. Попробуйте позже')


def writing_to_a_file(mesg):
    with open('urlbase.log', 'a', encoding='utf-8') as file:
        file.write(f'--- {mesg}\n')
    with open('urlbase.log', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) > 10:
            with open('urlbase.log', 'w', encoding='utf-8') as f:
                f.writelines(lines[:-1])


def schedule_news():
    desired_time = "14:00"
    current_time = time.strftime("%H:%M")
    if current_time == desired_time:
        num_messages = 3
        send_news(num_messages)


schedule.every().day.at("14:00").do(schedule_news)
bot.infinity_polling()
