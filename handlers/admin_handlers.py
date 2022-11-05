from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext, filters
from config import ADMIN_GROUP, admin_logger
from create_bot import bot
from states.states_group import FSMAdmin
from database.user_db_methods import check_user_exist, check_user_blocked, check_user_admin, block_user, unblock_user, \
    set_admin
from keyboards.admin_keyboard import main_admin_keyboard, mass_mailing_confirm_keyboard
from keyboards.navigation_keyboards import stop_dialog
from utils.admin import send_mass_mailing, process_user_id, get_user_full_info


async def admin_command(message: types.Message) -> None:
    """
    Команда /admin. Запускает меню администратора

    :param message: объект сообщения
    :type message: types.Message
    :return: None
    """

    tg_id = message.from_user.id
    chat_id = message.chat.id

    if not await check_user_exist(tg_id):
        await bot.send_message(chat_id, "Вы не зарегистрированы. Для прохождения регистрации напишите команду "
                                        "<b>/start</b> в личные сообщения боту, затем запросите права администратора/",
                               parse_mode="HTML")

    elif await check_user_blocked(tg_id):
        await bot.send_message(chat_id, "К сожалению, вы заблокированы и не можете воспользоваться услугами бота. "
                                        "Для уточнения деталей, обратитесь к администрации.")

    elif not await check_user_admin(tg_id):
        await bot.send_message(chat_id, "К сожалению, вы не являетесь администратором. Запросите права у действующего "
                                        "администратора и повторите попытку.")
    else:
        await FSMAdmin.admin_action.set()
        await bot.send_message(chat_id, "Выберете действие:", reply_markup=main_admin_keyboard())


async def admin_menu_inline_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Инлайн хэндлер обработки команд из меню админа".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = callback.message.chat.id

    if callback.data == 'mailing':
        await FSMAdmin.mass_mailing.set()
        await bot.send_message(chat_id, 'Введите текст рассылки.\n'
                                        'Если вы хотите применить форматирование, используйте HTML-тэги.')
    elif callback.data == 'user_info':
        await FSMAdmin.user_info.set()
        await bot.send_message(chat_id, 'Введите Username или ID интересующего Вас пользователя.')

    elif callback.data == 'block':
        await FSMAdmin.block_user.set()
        await bot.send_message(chat_id, 'Введите Username или ID нужного пользователя.')

    elif callback.data == 'unblock':
        await FSMAdmin.unblock_user.set()
        await bot.send_message(chat_id, 'Введите Username или ID нужного пользователя.')

    elif callback.data == 'make_admin':
        await FSMAdmin.set_admin.set()
        await bot.send_message(chat_id, 'Введите Username или ID нужного пользователя.')

    else:
        admin_logger.debug(f'Что-то пошло не так в админском меню. Callback.date: {callback.data}')
        await bot.send_message(chat_id, 'Кажется, что-то пошло не так. Попробуйте повторно вызвать команду '
                                        '<b>/admin</b>',
                               parse_mode='HTML')
        await state.finish()

    await callback.answer()

'''*****Массовая рассылка*****'''


async def confirm_mailing_handler(message: types.Message, state: FSMContext) -> None:
    """
    Подтверждение массовой рассылки.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    mailing_text = message.text
    chat_id = message.chat.id

    async with state.proxy() as data:
        data['mailing_text'] = mailing_text

    await bot.send_message(chat_id, f'Текст рассылки будет выглядеть следующим образом:\n\n{mailing_text}\n\n'
                                    f'Вы уверены, что хотите отправить рассылку всем пользователям бота?\n'
                                    f'Это действие нельзя отменить.',
                           reply_markup=mass_mailing_confirm_keyboard(),
                           parse_mode='HTML')


async def mailing_menu_inline_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Инлайн хэндлер обработки меню массовой рассылки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = callback.message.chat.id

    if callback.data == 'confirm_mailing':
        async with state.proxy() as data:
            mailing_text = data['mailing_text']

        await bot.send_message(chat_id, 'Начинаю рассылку')
        try:
            await send_mass_mailing(mailing_text)
        except Exception as exc:
            await bot.send_message(chat_id, 'Упс! Что-то пошло не так.\n'
                                            'Попробуйте снова или обратитесь в техническую поддержку.')
            admin_logger.debug(f'Что-то пошло не так при попытке массовой рассылки. Exception: {exc}')
        finally:
            await callback.answer()
            await state.finish()
        admin_logger.info(f'Admin {callback.from_user.id} started mass mailing.')
        await bot.send_message(chat_id, 'Рассылка успешно завершена.')

    elif callback.data == 'edit_text':
        await bot.send_message(chat_id, 'Введите новый текст рассылки. '
                                        'Напоминаю, что для форматирования нужно использовать HTML-теги.')

    elif callback.data == 'cancel_mailing':
        await bot.send_message(chat_id, 'Рассылка отменена.')
        await state.finish()

    await callback.answer()


'''*****Действия с юзером*****'''


async def user_info_handler(message: types.Message, state: FSMContext) -> None:
    """
    Вывод информации о пользователе.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = message.chat.id

    tg_id = await process_user_id(message.text)
    if tg_id:
        await get_user_full_info(tg_id, chat_id)
    else:
        await bot.send_message(chat_id, 'Такой пользователь не найден. Попробуйте снова.')

    await state.finish()


async def block_user_handler(message: types.Message, state: FSMContext) -> None:
    """
    Блокировка пользователя.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = message.chat.id

    tg_id = await process_user_id(message.text)
    if tg_id:
        await block_user(tg_id)
        await bot.send_message(chat_id, 'Пользователь заблокирован.')
    else:
        await bot.send_message(chat_id, 'Такой пользователь не найден. Попробуйте снова.')

    await state.finish()


async def unblock_user_handler(message: types.Message, state: FSMContext) -> None:
    """
    Разблокировка пользователя.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = message.chat.id

    tg_id = await process_user_id(message.text)
    if tg_id:
        await unblock_user(tg_id)
        await bot.send_message(chat_id, 'Пользователь разблокирован.')
    else:
        await bot.send_message(chat_id, 'Такой пользователь не найден. Попробуйте снова.')

    await state.finish()


async def set_admin_handler(message: types.Message, state: FSMContext) -> None:
    """
    Назначение пользователя админом.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = message.chat.id

    tg_id = await process_user_id(message.text)
    if tg_id:
        await set_admin(tg_id)
        await bot.send_message(chat_id, 'Пользователь назначен админом.')
    else:
        await bot.send_message(chat_id, 'Такой пользователь не найден. Попробуйте снова.')

    await state.finish()


'''*****Чат с юзером*****'''


async def user_chat_inline_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """
    Инлайн хэндлер обработки меню массовой рассылки".

    :param callback: объект CallbackQuery
    :type callback: types.CallbackQuery
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = callback.message.chat.id
    user_id = int(callback.data.split('|')[1])

    await FSMAdmin.user_chat.set()
    async with state.proxy() as data:
        data['user_id'] = user_id

    await bot.send_message(chat_id, 'Введите ответ на сообщение. Оно будет автоматически перенаправлено пользователю.')

    await callback.answer()


async def send_to_user_chat(message: types.Message, state: FSMContext) -> None:
    """
    Отправить сообщение в чат пользователю.

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    chat_id = message.chat.id

    async with state.proxy() as data:
        user_id = data['user_id']

    await bot.send_message(user_id, message.text, reply_markup=stop_dialog(), parse_mode='HTML')
    await bot.send_message(chat_id, 'Сообщение отправлено пользователю.')

    await state.finish()


'''*****Регистратор*****'''


def register_admin_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(admin_command,
                                        filters.IDFilter(chat_id=ADMIN_GROUP),
                                        commands=['admin'],
                                        content_types=['text'],
                                        state=None)
    dispatcher.register_callback_query_handler(admin_menu_inline_handler,
                                               state=FSMAdmin.admin_action)
    dispatcher.register_message_handler(confirm_mailing_handler,
                                        content_types=['text'],
                                        state=FSMAdmin.mass_mailing)
    dispatcher.register_callback_query_handler(mailing_menu_inline_handler,
                                               state=FSMAdmin.mass_mailing)
    dispatcher.register_message_handler(user_info_handler,
                                        content_types=['text'],
                                        state=FSMAdmin.user_info)
    dispatcher.register_message_handler(block_user_handler,
                                        content_types=['text'],
                                        state=FSMAdmin.block_user)
    dispatcher.register_message_handler(unblock_user_handler,
                                        content_types=['text'],
                                        state=FSMAdmin.unblock_user)
    dispatcher.register_message_handler(set_admin_handler,
                                        content_types=['text'],
                                        state=FSMAdmin.set_admin)
    dispatcher.register_callback_query_handler(user_chat_inline_handler,
                                               lambda callback: callback.data.startswith('response'),
                                               state=None)
    dispatcher.register_message_handler(send_to_user_chat,
                                        content_types=['text'],
                                        state=FSMAdmin.user_chat)
