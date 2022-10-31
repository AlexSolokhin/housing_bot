from typing import Optional
from config import IDEA_GROUP
from create_bot import bot
from states.states_group import FSMIdea
from database.user_db_methods import get_user_details
from keyboards.navigation_keyboards import back_keyboard


async def request_idea(tg_id: int) -> None:
    """
    Запрос описания идеи/предложения.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    await FSMIdea.request_idea.set()
    await bot.send_message(tg_id, "💡<b><i>Распишите ваше предложение в подробностях: "
                                  "(Добавьте фотографию, если есть)</i></b>",
                           reply_markup=back_keyboard(),
                           parse_mode='HTML')


async def send_idea_to_admins(tg_id: int,
                              photo: Optional[str],
                              video: Optional[str],
                              idea: str) -> None:
    """
    Генерация предложения и перенаправление в админский чат

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param photo: фото заявки (если было приложено)
    :type photo: Optional[str]
    :param video: видео заявки (если было приложено)
    :type video: Optional[str]
    :param idea: описание идеи/предложения
    :type idea: str
    :return: None
    """

    user_details = get_user_details(tg_id)
    username = user_details['username']
    name = user_details['name']
    surname = user_details['surname']
    phone = user_details['phone']

    text_line = f'💡<b>Поступило новое предложение</b>\n' \
                f'@{username}\n' \
                f'<b><i>Имя и Фамилия:</i></b> {name} {surname}\n' \
                f'<b><i>Номер телефона:</i></b> {phone}\n' \
                f'<b><i>Содержание:</i></b> {idea}\n'

    if photo:
        await bot.send_photo(IDEA_GROUP, photo, caption=text_line, parse_mode='HTML')
    elif video:
        await bot.send_video(IDEA_GROUP, video, caption=text_line, parse_mode='HTML')
    else:
        await bot.send_message(IDEA_GROUP, text_line, parse_mode='HTML')
