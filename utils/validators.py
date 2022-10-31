from re import fullmatch


async def name_validator(input_name: str) -> bool:
    """
    Проверка имени и фамилии на соответствие нужному формату

    :param input_name: имя и фамилия, указанные пользователем
    :type input_name: str
    :return: статус прохождения проверки
    :rtype: bool
    """

    input_array = input_name.split(' ')
    if len(input_array) != 2:
        return False

    for word in input_array:
        if not fullmatch(r'[а-я]+', word[1:]) or not fullmatch(r'[А-Я]', word[0]):
            return False

    return True


async def phone_validator(input_phone: str) -> bool:
    """
    Проверка телефона на соответствие нужному формату

    :param input_phone: номер телефона, указанный пользователем
    :type input_phone: str
    :return: статус прохождения проверки
    :rtype: bool
    """

    if len(input_phone) != 12 or not input_phone.startswith('+7') or not input_phone[1:].isdigit():
        return False

    return True
