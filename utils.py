from Side import Side


def toString(list_t: []) -> str:
    """
    :param: list_t: The list of objects to convert to string.
    :return: The string representation of the list.
    """
    result = ''
    for element in list_t:
        result += element.__str__() + " "
    result += '\n'
    return result


def askUserForNumber(message: str) -> int:
    """
    :param: message: The message to display to the user.
    :return: The number entered by the user.
    """
    value = ''
    while not value.isdigit():
        value = askUserForString(message)

    return int(value)


def askUserForSide(message: str) -> Side:
    """
    :param: message: The message to display to the user.
    :return: The side entered by the user.
    """
    value = ''
    while type(value) != Side:
        value = askUserForString(message)
        for name, side in Side.__members__.items():
            if side.value == value:
                return Side(value)


def askUserForBool(message: str) -> bool:
    """
    :param: message: The message to display to the user.
    :return: The boolean entered by the user.
    """
    value = ''
    while not (value == 'y' or value == 'n'):
        value = askUserForString(message)

    return value == 'y'


def askUserForString(message: str) -> str:
    """
    :param: message: The message to display to the user.
    :return: The string entered by the user.
    """
    value = input(message)
    return value
