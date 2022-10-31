from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from create_bot import bot
from states.states_group import FSMRegistration
from database.user_db_methods import check_user_exist, check_user_blocked, create_user
from utils.validators import name_validator, phone_validator
from utils.menu import main_menu


async def start_command(message: types.Message) -> None:
    """
    Команда старт. Регистрирует пользователя, направляет в главное меню или запрещает доступ

    :param message: объект сообщения
    :type message: types.Message
    :return: None
    """

    tg_id = message.from_user.id

    if not check_user_exist(tg_id):
        await FSMRegistration.register_name.set()
        await bot.send_message(tg_id, "☀<b>Доброго времени суток,</b> бот создан, "
                                      "чтобы обрабатывать заявки и обращения пользователей. "
                                      "Чтобы воспользоваться этим пришлите для начала ваше "
                                      "<b>Имя</b> и <b>Фамилию</b>",
                               parse_mode="HTML")

    elif check_user_blocked(tg_id):
        await bot.send_message(tg_id, "К сожалению, вы заблокированы и не можете воспользоваться услугами бота. "
                                      "Для уточнения деталей, обратитесь к администрации.",
                               parse_mode="HTML")

    else:
        await main_menu(tg_id)


async def set_name(message: types.Message, state: FSMContext) -> None:
    """
    Запрос и сохранение имени и фамилии

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMRegistration
    :return: None
    """

    if await name_validator(message.text):
        name = message.text.split(' ')[0]
        surname = message.text.split(' ')[1]

        async with state.proxy() as data:
            data['name'] = name
            data['surname'] = surname

        await FSMRegistration.next()
        await bot.send_message(message.from_user.id, "📞Теперь отправьте Ваш <b>номер телефона</b> через <b>+7</b> "
                                                     "следующим сообщением:",
                               parse_mode="HTML")

    else:
        await bot.send_message(message.from_user.id, "⛔📛<b>Имя</b> и <b>Фамилия</b> должны быть написаны через один "
                                                     "<i>пробел,</i> и должны быть написаны через <i>Кириллицу</i>. "
                                                     "Также должны быть <i>заглавные буквы.</i> <b>Учтите формат и"
                                                     "попробуйте снова:</b>",
                               parse_mode="HTML")


async def set_phone(message: types.Message, state: FSMContext) -> None:
    """
    Запрос и сохранение имени и фамилии

    :param message: объект сообщения
    :type message: types.Message
    :param state: текущий стэйт
    :type: FSMRegistration
    :return: None
    """

    if await phone_validator(message.text):
        async with state.proxy() as data:
            tg_id = message.from_user.id
            tg_username = message.from_user.username
            name = data['name']
            surname = data['surname']
            phone = message.text
            create_user(tg_id, tg_username, name, surname, phone)

        await state.finish()
        await main_menu(tg_id)

    else:
        await bot.send_message(message.from_user.id, "⛔📛⛔<b>Номер телефона</b> должен содержать 11 цифр и должен "
                                                     "обязательно содержать в начале <b>+7. Учтите формат и попробуйте "
                                                     "снова:</b>",
                               parse_mode="HTML")


def register_registration_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_command, content_types=['text'], commands=['start'], state=None)
    dispatcher.register_message_handler(set_name, content_types=['text'], state=FSMRegistration.register_name)
    dispatcher.register_message_handler(set_phone, content_types=['text'], state=FSMRegistration.register_phone)
