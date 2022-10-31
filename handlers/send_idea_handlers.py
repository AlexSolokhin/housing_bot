from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from states.states_group import FSMIdea
from utils.ideas import request_idea, send_idea_to_admins


async def request_idea_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер обработки входящей идеи

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMIdea
    :return: None
    """

    tg_id = message.from_user.id
    photo = None
    video = None

    # Подозреваю, в ТЗ всё-таки ошибка и прикреплять медиа к этому сообщению можно.
    if message.photo:
        photo = message.photo[0].file_id
        idea = message.caption
    elif message.video:
        video = message.video.file_id
        idea = message.caption
    else:
        idea = message.text

    await send_idea_to_admins(tg_id, photo, video, idea)
    await bot.send_message(tg_id, '💡<b>Идея принята и передана администрации.</b>'
                                  '<i>Спасибо за Ваше обращения!</i>', parse_mode='HTML')
    await state.finish()


async def request_idea_inline_handler(callback: types.CallbackQuery) -> None:
    """
    Инлайн хэндлер обработки входящей идеи".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :return: None
    """

    tg_id = callback.from_user.id

    await request_idea(tg_id)
    await callback.answer()


def register_idea_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(request_idea_message_handler,
                                        content_types=['text', 'photo', 'video'],
                                        state=FSMIdea.request_idea)
    dispatcher.register_callback_query_handler(request_idea_inline_handler,
                                               state=FSMIdea.request_idea)
