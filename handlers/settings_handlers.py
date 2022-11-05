from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from states.states_group import FSMSetName, FSMSetPhone
from database.user_db_methods import change_name, change_phone
from utils.validators import name_validator, phone_validator


async def change_name_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер для изменения имени и фамилии пользователя в БД

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    tg_id = message.from_user.id
    user_input = message.text

    if await name_validator(user_input):
        new_name = user_input.split(' ')[0]
        new_surname = user_input.split(' ')[1]

        await change_name(tg_id, new_name, new_surname)

        await bot.send_message(tg_id, "🛠️✅🛠️Настройки <b>имени</b> успешно применены!", parse_mode='HTML')
        await state.finish()

    else:
        await bot.send_message(message.from_user.id, "⛔📛<b>Имя</b> и <b>Фамилия</b> должны быть написаны через один "
                                                     "<i>пробел,</i> и должны быть написаны через <i>Кириллицу</i>. "
                                                     "Также должны быть <i>заглавные буквы.</i> <b>Учтите формат и"
                                                     "попробуйте снова:</b>",
                               parse_mode="HTML")


async def change_phone_message_handler(message: types.Message, state: FSMContext):
    """
    Хэндлер для изменения номера телефона пользователя в БД

    :param message: объект сообщения
    :type message: types.Message
    :param state: стэйт
    :type: FSMContext
    :return: None
    """

    tg_id = message.from_user.id
    user_input = message.text

    if await phone_validator(user_input):
        await change_phone(tg_id, user_input)

        await bot.send_message(tg_id, "🛠️✅🛠️Настройки <b>номера</b> успешно применены!", parse_mode='HTML')
        await state.finish()

    else:
        await bot.send_message(message.from_user.id, "⛔📛⛔<b>Номер телефона</b> должен содержать 11 цифр и должен "
                                                     "обязательно содержать в начале <b>+7. Учтите формат и попробуйте "
                                                     "снова:</b>",
                               parse_mode="HTML")


def register_settings_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(change_name_message_handler,
                                        content_types=['text'],
                                        state=FSMSetName.set_name)
    dispatcher.register_message_handler(change_phone_message_handler,
                                        content_types=['text'],
                                        state=FSMSetPhone.set_phone)
