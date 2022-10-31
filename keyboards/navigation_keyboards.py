from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def skip_back_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для пропуска шага или возвращения назад.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    skip = InlineKeyboardButton(text="▶Пропустить", callback_data='skip')
    back = InlineKeyboardButton(text="🔙Назад", callback_data='back')

    keyboard.add(skip)
    keyboard.add(back)

    return keyboard


def back_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для возвращения назад.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    back = InlineKeyboardButton(text="🔙Назад", callback_data='back')

    keyboard.add(back)

    return keyboard


def check_phone_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для проверки номера телефона.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    yes = InlineKeyboardButton(text="✅Да", callback_data='yes')
    another_phone = InlineKeyboardButton(text="🔙Оставить номер телефона", callback_data='another_phone')

    keyboard.add(yes, another_phone)

    return keyboard


def stop_dialog() -> InlineKeyboardMarkup:
    """
    Клавиатура для остановки диалога с диспетчером.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    stop_chat = InlineKeyboardButton(text="❌📞Завершить диалог", callback_data='stop_chat')

    keyboard.add(stop_chat)

    return keyboard
