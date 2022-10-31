from aiogram import types, Dispatcher
from states.states_group import FSMMain, FSMRequestMenu, FSMSettingMenu, FSMContactUsMenu
from utils.menu import main_menu, request_menu, contact_us_menu, settings_menu
from utils.requests import request_address
from utils.useful_contacts import useful_contacts
from utils.ideas import request_idea
from utils.settings import change_name_message, change_phone_message
from utils.contact_us import check_phone_number, connect_to_meat_bag


async def main_menu_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер главного меню".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'make_request':
        await request_menu(tg_id)
    elif next_step == 'contact_us':
        await contact_us_menu(tg_id)
    elif next_step == 'settings':
        await settings_menu(tg_id)
    elif next_step == 'more_contacts':
        await useful_contacts(tg_id)
    await callback.answer()


async def request_menu_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер меню заявки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'send_request':
        await request_address(tg_id)
    elif next_step == 'send_idea':
        await request_idea(tg_id)
    elif next_step == 'back':
        await main_menu(tg_id)
    await callback.answer()


async def settings_menu_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер меню настроек.

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'change_name':
        await change_name_message(tg_id)
    elif next_step == 'change_phone':
        await change_phone_message(tg_id)
    await callback.answer()


async def contact_us_menu_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер меню обратной связи.

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'call_me':
        await check_phone_number(tg_id)
    elif next_step == 'text_me':
        await connect_to_meat_bag(tg_id)
    await callback.answer()


def register_menu_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(main_menu_inline_handler,
                                               state=FSMMain.main)
    dispatcher.register_callback_query_handler(request_menu_inline_handler,
                                               state=FSMRequestMenu.request_menu)
    dispatcher.register_callback_query_handler(settings_menu_inline_handler,
                                               state=FSMSettingMenu.setting_menu)
    dispatcher.register_callback_query_handler(contact_us_menu_inline_handler,
                                               state=FSMContactUsMenu.contacts_menu)
