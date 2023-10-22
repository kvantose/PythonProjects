import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv('BASE_URL')
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("history", "История 10-ти запросов"),
    ("clear", "Отчитстка истории"),
    ("game", "Игра: 'камень, ножницы, бумага'")
)
