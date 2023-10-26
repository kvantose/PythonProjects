from loader import bot
import requests
from config_data import config


def sent_currency(message):
    response_first = requests.get(config.DOLLAR_URL)
    response_second = requests.get(config.EURO_URL)
    if response_first.status_code == 200 and response_second.status_code == 200:
        data_f = response_first.json()
        data_s = response_second.json()

        data_first = data_f['data']['RUB']['value']
        data_second = data_s['data']['RUB']['value']

        result = (f'Курс валют на данный момент:'
                  f'\nUSD($): {round(data_first, 2)} RUB'
                  f'\nEUR(€): {round(data_second, 2)} RUB')
        bot.send_message(message, result)

    else:
        bot.send_message(message, 'Неудалось получить данные')

