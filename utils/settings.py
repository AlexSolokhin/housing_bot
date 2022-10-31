from typing import Optional
from config import IDEA_GROUP
from create_bot import bot
from states.states_group import FSMSetName, FSMSetPhone
from database.user_db_methods import get_user_details
from keyboards.navigation_keyboards import back_keyboard


async def change_name_message(tg_id: int) -> None:
    """
    Запрос нового имени и фамилии.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMSetName.set_name.set()
    await bot.send_message(tg_id, "🛠️<i>Отправьте своё Имя и Фамилию, чтобы поменять настройки:</i>",
                           parse_mode='HTML')


async def change_phone_message(tg_id: int) -> None:
    """
    Запрос нового телефона.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMSetPhone.set_phone.set()
    await bot.send_message(tg_id, "🛠️<i>Отправьте свой номер телефона, чтобы поменять настройки:</i>",
                           parse_mode='HTML')
