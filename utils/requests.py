from typing import Optional
from config import REQUESTS_GROUP
from create_bot import bot
from states.states_group import FSMRequest
from database.user_db_methods import get_user_details
from keyboards.navigation_keyboards import skip_back_keyboard, back_keyboard


async def request_address(tg_id: int) -> None:
    """
    Вызов первого шага для направления заявки.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMRequest.request_address.set()
    await bot.send_message(tg_id, "<b><i>Шаг 1/3.</i></b> 📝Напишите адрес или ориентир проблемы (улицу, номер дома,"
                                  "подъезд, этаж, и квартиру) или пропустите этот пункт:",
                           reply_markup=skip_back_keyboard(),
                           parse_mode='HTML')


async def request_media(tg_id: int) -> None:
    """
    Вызов второго шага для направления заявки.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMRequest.request_media.set()
    await bot.send_message(tg_id, "<b><i>Шаг 2/3.</i></b> 🖻Прикрепите видео или фотографию к своей заявке"
                                  "или пропустите этот пункт:",
                           reply_markup=skip_back_keyboard(),
                           parse_mode='HTML')


async def request_issue(tg_id: int) -> None:
    """
    Вызов третьего шага для направления заявки.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMRequest.request_description.set()
    await bot.send_message(tg_id, "<b><i>Шаг 3/3.</i></b> 📛Напишите причину обращения в подробностях:",
                           reply_markup=back_keyboard(),
                           parse_mode='HTML')


async def send_request_to_admins(tg_id: int,
                                 address: Optional[str],
                                 photo: Optional[str],
                                 video: Optional[str],
                                 issue: str) -> None:
    """
    Генерация заявки и перенаправление в админский чат

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param address: адрес (если был указан)
    :type address: Optional[str]
    :param photo: фото заявки (если было приложено)
    :type photo: Optional[str]
    :param video: видео заявки (если было приложено)
    :type video: Optional[str]
    :param issue: описание проблемы
    :type issue: str
    :return: None
    """

    user_details = get_user_details(tg_id)
    username = user_details['username']
    name = user_details['name']
    surname = user_details['surname']
    phone = user_details['phone']

    if address:
        address_line = f'<b><i>Адрес:</i></b> {address}\n'
    else:
        address_line = ''

    text_line = f'⛔<b>Поступила новая жалоба</b>\n' \
                f'@{username}\n' \
                f'<b><i>Имя и Фамилия:</i></b> {name} {surname}\n' \
                f'<b><i>Номер телефона:</i></b> {phone}\n' \
                f'{address_line}' \
                f'<b><i>Содержание:</i></b> {issue}\n'

    if photo:
        await bot.send_photo(REQUESTS_GROUP, photo, caption=text_line, parse_mode='HTML')
    elif video:
        await bot.send_video(REQUESTS_GROUP, video, caption=text_line, parse_mode='HTML')
    else:
        await bot.send_message(REQUESTS_GROUP, text_line, parse_mode='HTML')
