from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для главного меню бота.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    make_request = InlineKeyboardButton(text="📛Оставить заявку", callback_data='make_request')
    contact_us = InlineKeyboardButton(text="📞Связаться", callback_data='contact_us')
    settings = InlineKeyboardButton(text="⚙Настройки", callback_data='settings')
    more_contacts = InlineKeyboardButton(text='☎Полезные контакты', callback_data='more_contacts')

    keyboard.add(make_request, contact_us)
    keyboard.add(settings)
    keyboard.add(more_contacts)

    return keyboard


def request_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для меню заявок бота.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    send_request = InlineKeyboardButton(text="📛Оставить заявку", callback_data='send_request')
    send_idea = InlineKeyboardButton(text="💡Поделиться предложением", callback_data='send_idea')
    back = InlineKeyboardButton(text="🔙Назад", callback_data='back')

    keyboard.add(send_request, send_idea)
    keyboard.add(back)

    return keyboard


def contacts_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для меню обратной связи бота.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    call_me = InlineKeyboardButton(text="📞Перезвоните мне", callback_data='call_me')
    text_me = InlineKeyboardButton(text="📞Свяжитесь со мной в чат-боте", callback_data='text_me')
    back = InlineKeyboardButton(text="🔙Назад", callback_data='back')

    keyboard.add(call_me)
    keyboard.add(text_me)
    keyboard.add(back)

    return keyboard


def settings_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура для меню настроек бота.

    :return: объект клавиатуры
    :rtype: InlineKeyboardMarkup
    """

    keyboard = InlineKeyboardMarkup()

    change_name = InlineKeyboardButton(text="🛠️Поменять имя", callback_data='change_name')
    change_phone = InlineKeyboardButton(text="🛠️Сменить номер", callback_data='change_phone')
    back = InlineKeyboardButton(text="🔙Назад", callback_data='back')

    keyboard.add(change_name, change_phone)
    keyboard.add(back)

    return keyboard
