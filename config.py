import os
from dotenv import load_dotenv, find_dotenv
from peewee import SqliteDatabase

if not find_dotenv():
    exit('Переменные окружения не загружены: проверьте файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

db = SqliteDatabase('uer_south')

REQUESTS_GROUP = '-816791300'
IDEA_GROUP = '-816791300'
ADMIN_GROUP = '-816791300'
