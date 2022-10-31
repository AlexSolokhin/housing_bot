from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
