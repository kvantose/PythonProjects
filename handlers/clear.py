from loader import bot


@bot.message_handler(commands=['clear'], func=lambda message: True)
def clear_history(message):
    with open('title.log', 'w', encoding='utf-8'): pass
    bot.send_message(message.chat.id, 'История очищена')
