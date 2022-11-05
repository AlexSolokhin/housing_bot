import os
from dotenv import load_dotenv, find_dotenv
from peewee import SqliteDatabase
import logging.config
from logging_config import dict_config

if not find_dotenv():
    exit('Переменные окружения не загружены: проверьте файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

db = SqliteDatabase('uer_south')

logging.config.dictConfig(dict_config)
db_logger = logging.getLogger('db_logger')
admin_logger = logging.getLogger('admin_logger')

REQUESTS_GROUP = '-816791300'
IDEA_GROUP = '-816791300'
ADMIN_GROUP = '-816791300'
