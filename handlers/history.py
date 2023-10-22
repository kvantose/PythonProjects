from loader import bot
import sqlite3


@bot.message_handler(commands=['history'], func=lambda message: True)
def check_history(message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message FROM title')
    rows = cursor.fetchall()
    for row in rows:
        bot.send_message(message.chat.id, f'===| {row[0]} |===')
    cursor.close()
    conn.close()
