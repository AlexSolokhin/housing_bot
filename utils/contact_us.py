from typing import Optional
from config import ADMIN_GROUP
from create_bot import bot
from states.states_group import FSMCallMe, FSMTextMe
from database.user_db_methods import get_user_details
from keyboards.navigation_keyboards import check_phone_keyboard, stop_dialog
from keyboards.admin_keyboard import response_in_chat_keyboard


async def check_phone_number(tg_id: int) -> None:
    """
    Уточнение номера телефона.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMCallMe.check_number.set()
    user_details = await get_user_details(tg_id)
    phone_num = user_details['phone']

    await bot.send_message(tg_id, f"<b>Это ваш номер телефона</b> {phone_num}? "
                                  f"<i>Если да, нажмите соответствующую кнопку, "
                                  f"<b>если нет,</b> впишите свой актуальный номер телефона здесь</i>",
                           reply_markup=check_phone_keyboard(),
                           parse_mode='HTML')


async def send_call_request_admins(tg_id: int,
                                   actual_phone: Optional[str] = None) -> None:
    """
    Генерация запроса обратного звонка и перенаправление в админский чат

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param actual_phone: актуальный номер телефона
    :type actual_phone: Optional[str]
    :return: None
    """

    user_details = await get_user_details(tg_id)
    username = user_details['username']
    name = user_details['name']
    surname = user_details['surname']
    if actual_phone:
        phone = actual_phone
    else:
        phone = user_details['phone']

    text_line = f'📞<b>Поступила заявка на обратный звонок</b>\n' \
                f'@{username}\n' \
                f'<b><i>Имя и Фамилия:</i></b> {name} {surname}\n' \
                f'<b><i>Номер телефона:</i></b> {phone}\n' \

    await bot.send_message(ADMIN_GROUP, text_line, parse_mode='HTML')


async def connect_to_meat_bag(tg_id: int) -> None:
    """
    Соединение с оператором.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMTextMe.connect_admin.set()
    await bot.send_message(tg_id, '✅📞✅Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ" - готов помочь Вам. '
                                  'Напишите, пожалуйста, интересующий Вас вопрос и ожидайте:',
                           reply_markup=stop_dialog(),
                           parse_mode='HTML')


async def send_message_to_admin(tg_id: int, message_text: str) -> None:
    """
    Отправка сообщения оператору.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param message_text: текст вопроса/сообщения пользователя
    :rtype message_text: str
    :return: None
    """

    user_details = await get_user_details(tg_id)
    username = user_details['username']
    name = user_details['name']
    surname = user_details['surname']
    phone = user_details['phone']

    text_line = f'📞<b>Поступила вопрос в чат</b>\n' \
                f'@{username}\n' \
                f'<b><i>Имя и Фамилия:</i></b> {name} {surname}\n' \
                f'<b><i>Номер телефона:</i></b> {phone}\n' \
                f'<b><i>Вопрос::</i></b> {message_text}'

    await bot.send_message(ADMIN_GROUP,
                           text_line,
                           reply_markup=response_in_chat_keyboard(tg_id),
                           parse_mode='HTML')
