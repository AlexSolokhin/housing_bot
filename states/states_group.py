from aiogram.dispatcher.filters.state import StatesGroup, State

'''*****Главное Меню*****'''


class FSMMain(StatesGroup):
    main = State()


'''*****Регистрация*****'''


class FSMRegistration(FSMMain):
    register_name = State()
    register_phone = State()


'''*****Меню обращений*****'''


class FSMRequestMenu(FSMMain):
    request_menu = State()


class FSMRequest(FSMRequestMenu):
    request_address = State()
    request_media = State()
    request_description = State()
    request_complete = State()


class FSMIdea(FSMRequestMenu):
    request_idea = State()


'''*****Меню обратной связи*****'''


class FSMContactUsMenu(FSMMain):
    contacts_menu = State()


class FSMCallMe(FSMContactUsMenu):
    check_number = State()
    another_number = State()


class FSMTextMe(FSMContactUsMenu):
    connect_admin = State()


'''*****Меню настроек*****'''


class FSMSettingMenu(FSMMain):
    setting_menu = State()


class FSMSetName(FSMSettingMenu):
    set_name = State()


class FSMSetPhone(FSMSettingMenu):
    set_phone = State()


'''*****Панель администратора*****'''


class FSMAdmin(StatesGroup):
    admin_action = State()
    mass_mailing = State()
    user_info = State()
    block_user = State()
    unblock_user = State()
    set_admin = State()
    user_chat = State()
