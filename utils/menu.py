from create_bot import bot
from states.states_group import FSMMain, FSMRequestMenu, FSMContactUsMenu, FSMSettingMenu
from keyboards.menu_keyboards import main_menu_keyboard, request_menu_keyboard, contacts_menu_keyboard, \
    settings_menu_keyboard


async def main_menu(tg_id: int) -> None:
    """
    Вызов главного меню бота.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMMain.main.set()
    await bot.send_message(tg_id, "✈<b>Добро пожаловать</b> <i>в главное меню бота Управляющей компании \"УЭР-ЮГ\".</i>"
                                  "Здесь вы можете оставить заявку для управляющей компании или направить своё "
                                  "предложение по управлению домом. Просто воспользуйтесь кнопками <b><i>меню</i></b>, "
                                  "чтобы взаимодействовать с функциями бота.",
                           reply_markup=main_menu_keyboard(),
                           parse_mode="HTML")


async def request_menu(tg_id: int) -> None:
    """
    Вызов меню заявок и предложений.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMRequestMenu.request_menu.set()
    await bot.send_message(tg_id, "📛👇📛<i>Выберите категорию, по которой вы хотите оставить заявку в УК:</i>",
                           reply_markup=request_menu_keyboard(),
                           parse_mode="HTML")


async def contact_us_menu(tg_id: int) -> None:
    """
    Вызов меню обратной связи.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMContactUsMenu.contacts_menu.set()
    await bot.send_message(tg_id, "👇<i>Выберите способ связи из нижеперечисленного списка:</i>",
                           reply_markup=contacts_menu_keyboard(),
                           parse_mode="HTML")


async def settings_menu(tg_id: int) -> None:
    """
    Вызов меню настроек.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMSettingMenu.setting_menu.set()
    await bot.send_message(tg_id, "⚙Тут Вы сможете поменять <b>Имя</b> и <b>Фамилию</b> в Базе данных нашего бота или "
                                  "же можете поменять ваш <b>номер телефона,</b> если вы изначально вводили что-то "
                                  "неверно. Выберете, что хотите поменять или вернитесь назад в "
                                  "<b><i>главное меню:</i></b>",
                           reply_markup=settings_menu_keyboard(),
                           parse_mode="HTML")
