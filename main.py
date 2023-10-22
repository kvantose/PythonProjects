import bot_sent
from loader import bot
from bot_sent import sent_news, schedule_news
import handlers
from utils.set_bot_commands import set_default_commands


@bot.message_handler(func=lambda message: message.text == '3')
def send_three_news(message):
    """Функция отправки трех новостей"""
    bot_sent.send_news(message.chat.id, 3)


@bot.message_handler(func=lambda message: message.text == '5')
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


@bot.message_handler(func=lambda message: message.text == 'Подписаться на рассылку новостей')
def subscribe(message):
    """Функция подписки"""
    bot.send_message(message.chat.id, 'Хорошо! Теперь я буду отправлять вам по 3 новости каждый день в 14:00')
    schedule_news(message.chat.id)


if __name__ == '__main__':
    set_default_commands(bot)
    bot.infinity_polling()
