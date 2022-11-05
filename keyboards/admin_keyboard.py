from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_admin_keyboard() -> InlineKeyboardMarkup:
    """
    Основная клавиатура админской группы.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    mass_mailing = InlineKeyboardButton(text="Сделать рассылку всем пользователям", callback_data='mailing')
    user_info = InlineKeyboardButton(text="Узнать о пользователе", callback_data='user_info')
    block_user = InlineKeyboardButton(text="Заблокировать пользователя", callback_data='block')
    unblock_user = InlineKeyboardButton(text="Разблокировать пользователя", callback_data='unblock')
    make_an_admin = InlineKeyboardButton(text="Сделать админом", callback_data='make_admin')

    keyboard.add(mass_mailing)
    keyboard.add(user_info)
    keyboard.add(block_user, unblock_user)
    keyboard.add(make_an_admin)

    return keyboard


def mass_mailing_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для работы с массовыми рассылками.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    confirm_mailing = InlineKeyboardButton(text="Отправить рассылку", callback_data='confirm_mailing')
    edit_text = InlineKeyboardButton(text="Изменить текст", callback_data='edit_text')
    cancel_mailing = InlineKeyboardButton(text="Отменить рассылку", callback_data='cancel_mailing')

    keyboard.add(confirm_mailing)
    keyboard.add(edit_text)
    keyboard.add(cancel_mailing)

    return keyboard


def response_in_chat_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура для ответа на вопрос пользователя в формате чата.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    response = InlineKeyboardButton(text="🔘Ответить", callback_data=f'response|{tg_id}')

    keyboard.add(response)

    return keyboard
