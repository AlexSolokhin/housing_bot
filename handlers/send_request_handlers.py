from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from states.states_group import FSMRequest
from utils.menu import request_menu
from utils.requests import request_address, request_media, request_issue, send_request_to_admins
from keyboards.navigation_keyboards import skip_back_keyboard


async def ask_address_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер обработки сообщения первого шага подачи заявки

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMRequest
    :return: None
    """

    tg_id = message.from_user.id
    address = message.text

    async with state.proxy() as data:
        data['address'] = address

    await request_media(tg_id)


async def ask_address_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер обработки кнопки первого шага подачи заявки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'skip':
        await request_media(tg_id)
    elif next_step == 'back':
        await request_menu(tg_id)
    await callback.answer()


async def ask_media_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер обработки сообщения второго шага подачи заявки

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMRequest
    :return: None
    """

    tg_id = message.from_user.id
    photo = None
    video = None

    if message.text:
        await bot.send_message(tg_id,
                               "⛔📛В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> "
                               "в виде медиа-сообщения. <b><i>Попробуйте ещё раз:</i></b>",
                               reply_markup=skip_back_keyboard(),
                               parse_mode='HTML')
    else:
        if message.photo:
            photo = message.photo[0].file_id
        elif message.video:
            video = message.video.file_id

        async with state.proxy() as data:
            data['photo'] = photo
            data['video'] = video

        await request_issue(tg_id)


async def ask_media_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер обработки кнопки второго шага подачи заявки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id
    next_step = callback.data

    if next_step == 'skip':
        await request_issue(tg_id)
    elif next_step == 'back':
        await request_address(tg_id)
    await callback.answer()


async def ask_issue_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер обработки сообщения первого шага подачи заявки

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMRequest
    :return: None
    """

    tg_id = message.from_user.id
    issue = message.text

    async with state.proxy() as data:
        address = data.get('address', None)
        photo = data.get('photo', None)
        video = data.get('video', None)

    await send_request_to_admins(tg_id, address, photo, video, issue)
    await bot.send_message(tg_id, '✅<b>Жалоба отправлена администрации.</b>'
                                  '<i>Спасибо за Ваше обращения!</i>', parse_mode='HTML')
    await state.finish()


async def ask_issue_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер обработки кнопки третьего шага подачи заявки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id

    await request_media(tg_id)
    await callback.answer()


def register_requests_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(ask_address_message_handler,
                                        content_types=['text'],
                                        state=FSMRequest.request_address)
    dispatcher.register_callback_query_handler(ask_address_inline_handler,
                                               state=FSMRequest.request_address)
    dispatcher.register_message_handler(ask_media_message_handler,
                                        content_types=['text', 'photo', 'video'],
                                        state=FSMRequest.request_media)
    dispatcher.register_callback_query_handler(ask_media_inline_handler,
                                               state=FSMRequest.request_media)
    dispatcher.register_message_handler(ask_issue_message_handler,
                                        content_types=['text'],
                                        state=FSMRequest.request_description)
    dispatcher.register_callback_query_handler(ask_issue_inline_handler,
                                               state=FSMRequest.request_description)
