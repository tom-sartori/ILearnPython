from Side import Side


def toString(list_t: []) -> str:
    result = ''
    for element in list_t:
        result += element.__str__() + " "
    result += '\n'
    return result


def askUserForNumber(message: str) -> int:
    value = ''
    while not value.isdigit():
        value = askUserForString(message)

    return int(value)


def askUserForSide(message: str) -> Side:
    value = ''
    while type(value) != Side:
        value = askUserForString(message)
        for name, side in Side.__members__.items():
            if side.value == value:
                return Side(value)


def askUserForBool(message: str) -> bool:
    value = ''
    while not (value == 'y' or value == 'n'):
        value = askUserForString(message)

    return value == 'y'


def askUserForString(message: str) -> str:
    value = input(message)
    return value
