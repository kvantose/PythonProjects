import bot_sent
from loader import bot
from utils.set_bot_commands import set_default_commands
from utils.currency import sent_currency


@bot.message_handler(func=lambda message: message.text == '3 новости')
def send_three_news(message):
    """Функция отправки трех новостей"""
    bot_sent.send_news(message.chat.id, 3)


@bot.message_handler(func=lambda message: message.text == '5 новостей')
def send_five_news(message):
    """Функция отправки пяти новостей"""
    bot_sent.send_news(message.chat.id, 5)


@bot.message_handler(func=lambda message: message.text == 'Введите кол-во новостей')
def ask_custom_num(message):
    """Функция запроса пользовательского количества новостей"""
    bot_sent.send_news(message.chat.id, 'Введите количество новостей, которые вы хотели бы увидеть')


@bot.message_handler(func=lambda message: message.text.isdigit())
def send_custom_news(message):
    """Функция отправки пользовательского количества новостей"""
    num_messages = int(message.text)
    bot_sent.send_news(message.chat.id, num_messages)


@bot.message_handler(func=lambda message: message.text == 'Курс валют')
def currency(message):
    """Функция отправки курса валют"""
    sent_currency(message.chat.id)


if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
