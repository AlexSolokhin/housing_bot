from config import db
from peewee import Model
from peewee import CharField, IntegerField, BooleanField


class UserModel(Model):
    tg_id = IntegerField(unique=True)
    tg_username = CharField(unique=True)
    name = CharField()
    surname = CharField()
    phone = CharField()
    is_blocked = BooleanField(default=False)
    is_admin = BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'bot_users'


UserModel.create_table()
