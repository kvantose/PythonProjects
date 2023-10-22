from loader import bot
import schedule
import time
import requests
from config_data import config
from database import add_history

sent_news = set()


def send_news(chat_id, num_messages):
    response = requests.get(config.BASE_URL)
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
                    sent_messages += 1
                    add_history.writing_to_a_file(title)
        if sent_messages == 0:
            bot.send_message(chat_id, 'Нет доступных новостей. Попробуйте позже')


def schedule_news(chat_id):
    desired_time = "14:00"
    current_time = time.strftime("%H:%M")
    if current_time == desired_time:
        num_messages = 3
        send_news(chat_id, num_messages)


schedule.every().day.at("14:00").do(schedule_news)