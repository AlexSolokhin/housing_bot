from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from states.states_group import FSMCallMe, FSMTextMe
from utils.contact_us import send_call_request_admins, send_message_to_admin


async def check_phone_inline_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Инлайн хэндлер проверки актуального номера телефона".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :param state: текущий стэйт
    :type: FSMCallMe
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'yes':
        await send_call_request_admins(tg_id)
        await bot.send_message(tg_id, '✅<b>Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время!',
                               parse_mode='HTML')
        await state.finish()

    elif next_step == 'another_phone':
        await bot.send_message(tg_id, "📞Напишите номер телефона, на который мы вам перезвоним?")
        await FSMCallMe.another_number.set()

    await callback.answer()


async def send_actual_phone_message_handler(message: types.Message, state: FSMContext) -> None:
    """
    Хэндлер отправки актуального номера телефона".

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMCallMe
    :return: None
    """

    tg_id = message.from_user.id
    actual_phone = message.text

    await send_call_request_admins(tg_id, actual_phone=actual_phone)
    await bot.send_message(tg_id, '✅<b>Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время!', parse_mode='HTML')
    await state.finish()


async def chat_with_admin_message_handler(message: types.Message) -> None:
    """
    Хэндлер отправки сообщения в чат администратору".

    :param message: объект сообщения
    :type message: types.Message
    """

    tg_id = message.from_user.id
    await send_message_to_admin(tg_id, message.text)


async def stop_chat_inline_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Инлайн хэндлер остановки чата с администратором".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :param state: текущий стэйт
    :type: FSMTextMe
    :return: None
    """

    tg_id = callback.from_user.id
    await bot.send_message(tg_id, '❌📞<b>Диалог с администратором завершен...</b>', parse_mode='HTML')
    await state.finish()
    await callback.answer()


def register_contact_us_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(check_phone_inline_handler,
                                               state=FSMCallMe.check_number)
    dispatcher.register_message_handler(send_actual_phone_message_handler,
                                        content_types=['text'],
                                        state=FSMCallMe.another_number)
    dispatcher.register_message_handler(chat_with_admin_message_handler,
                                        content_types=['text'],
                                        state=FSMTextMe.connect_admin)
    dispatcher.register_callback_query_handler(stop_chat_inline_handler,
                                               state=FSMTextMe.connect_admin)
