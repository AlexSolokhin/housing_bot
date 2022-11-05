from config import db
from database.models import UserModel
from typing import Optional

# TODO: прописать exceptions
# TODO: прописать логирования


async def check_user_exist(tg_id: int) -> bool:
    """
    Проверка на существование юзера

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: существует ли юзер в БД
    :rtype: bool
    """

    with db:
        if UserModel.get_or_none(UserModel.tg_id == tg_id):
            return True
    return False


async def check_user_blocked(tg_id: int) -> bool:
    """
    Проверка на блокировку пользователя

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: заблокирован ли пользователь
    :rtype: bool
    """

    with db:
        user = UserModel.get(tg_id=tg_id)
        return user.is_blocked


async def check_user_admin(tg_id: int) -> bool:
    """
    Проверка на статус админа

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: заблокирован ли пользователь
    :rtype: bool
    """

    with db:
        user = UserModel.get(tg_id=tg_id)
        return user.is_admin


async def create_user(tg_id: int, tg_username: str, name: str, surname: str, phone: str) -> None:
    """
    Создание нового пользователя

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param tg_username: имя пользователя в Telegram
    :param name: имя юзера
    :type name: str
    :param surname: фамилия юзера
    :type surname: str
    :param phone: телефон юзера
    :type phone: str
    :return: None
    """

    with db:
        UserModel.create(tg_id=tg_id, tg_username=tg_username, name=name, surname=surname, phone=phone)


async def get_user_details(tg_id: int) -> dict:
    """
    Получение информации о пользователе

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: словарь с информацией о пользователе
    :rtype: dict
    """

    with db:
        user = UserModel.get(tg_id=tg_id)

    user_info = {'username': user.tg_username,
                 'name': user.name,
                 'surname': user.surname,
                 'phone': user.phone,
                 'is_blocked': user.is_blocked,
                 'is_admin': user.is_admin}
    return user_info


async def get_all_users() -> list:
    """
    Получение списка всех незаблокированных пользователей

    :return: список незаблокированных пользователей
    :rtype: list
    """

    with db:
        users = UserModel.select().where(UserModel.is_blocked == 0)
        users_list = [user.tg_id for user in users]

    return users_list


async def get_id_by_username(username: str) -> Optional[int]:
    """
    Получаем id пользователя по его username
    :param username: имя пользователя в Tg
    :type username: str
    :return: id пользователя в Tg или None
    :rtype: Optional[int]
    """
    if username.startswith('@'):
        username = username[1:]

    with db:
        user = UserModel.get_or_none(tg_username=username)
        if user:
            return user.tg_id


async def change_name(tg_id: int, new_name: str, new_surname: str) -> None:
    """
    Изменение имени пользователя

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param new_name: новое имя пользователя
    :type new_name: str
    :param new_surname: новая фамилия пользователя
    :type new_surname: str
    :return: None
    """

    with db:
        update_query = UserModel.update(name=new_name, surname=new_surname).where(tg_id == tg_id)
        update_query.execute()


async def change_phone(tg_id: int, new_phone: str) -> None:
    """
    Изменение телефона пользователя

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :param new_phone: новой номер телефона пользователя
    :type new_phone: str
    :return: None
    """

    with db:
        update_query = UserModel.update(phone=new_phone).where(tg_id == tg_id)
        update_query.execute()


async def block_user(tg_id: int) -> None:
    """
    Блокировка пользователя. Лишает права использовать бота.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    with db:
        update_query = UserModel.update(is_blocked=True).where(tg_id == tg_id)
        update_query.execute()


async def unblock_user(tg_id: int) -> None:
    """
    разблокировка пользователя.

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    with db:
        update_query = UserModel.update(is_blocked=False).where(tg_id == tg_id)
        update_query.execute()


async def set_admin(tg_id: int) -> None:
    """
    Даёт пользователю админские права

    :param tg_id: id юзера в Telegram
    :type tg_id: int
    :return: None
    """

    with db:
        update_query = UserModel.update(is_admin=True).where(tg_id == tg_id)
        update_query.execute()
