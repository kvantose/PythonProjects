from loader import bot
import sqlite3


@bot.message_handler(commands=['clear'], func=lambda message: True)
def clear_history(message):
    """Отчистка истории запросов"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM title')

    conn.commit()
    cursor.close()
    conn.close()

    bot.send_message(message.chat.id, 'История успешно очищена')
