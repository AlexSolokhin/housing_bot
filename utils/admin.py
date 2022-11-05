from create_bot import bot
from database.user_db_methods import get_all_users, check_user_exist, get_id_by_username, get_user_details
from typing import Optional


async def send_mass_mailing(mailing_text: str) -> None:
    """
    Отправка рассылки всем незаблокированным пользователям

    :param mailing_text: текст рассылки
    :type mailing_text: str
    :return: None
    """

    users_list = await get_all_users()

    for user in users_list:
        await bot.send_message(user, mailing_text, parse_mode='HTML')


async def process_user_id(admin_input: str) -> Optional[int]:
    """
    Обработка инпута от админа. Если пользователь существует, возвращает id пользователя в Tg

    :param admin_input: пользовательский ввод
    :type admin_input: str
    :return: id пользователя в Tg или None
    :rtype: Optional[int]
    """

    if admin_input.isdigit():
        tg_id = int(admin_input)
        if not await check_user_exist(tg_id):
            return None
    else:
        tg_id = await get_id_by_username(admin_input)
    return tg_id


async def get_user_full_info(tg_id: int, chat_id: int) -> None:
    """
    Отправка сообщения оператору.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param chat_id: id админского чата
    :type chat_id: int
    :return: None
    """

    user_details = await get_user_details(tg_id)
    username = user_details['username']
    name = user_details['name']
    surname = user_details['surname']
    phone = user_details['phone']
    if user_details['is_blocked']:
        blocked = 'Да'
    else:
        blocked = 'Нет'
    if user_details['is_admin']:
        admin = 'Да'
    else:
        admin = 'Нет'

    text_line = f'<b>Детальная информация о пользователе</b>\n' \
                f'@{username}\n' \
                f'<b><i>Имя и Фамилия:</i></b> {name} {surname}\n' \
                f'<b><i>Номер телефона:</i></b> {phone}\n' \
                f'<b><i>Админ:</i></b> {admin}\n' \
                f'<b><i>Заблокирован:</i></b> {blocked}'

    await bot.send_message(chat_id, text_line, parse_mode='HTML')
