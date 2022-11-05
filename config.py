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
REQUESTS_GROUP = os.getenv('REQUESTS_GROUP')
IDEA_GROUP = os.getenv('IDEA_GROUP')
ADMIN_GROUP = os.getenv('ADMIN_GROUP')

db = SqliteDatabase('uer_south')

logging.config.dictConfig(dict_config)
db_logger = logging.getLogger('db_logger')
admin_logger = logging.getLogger('admin_logger')
