"""Ошибки"""


class IncorrectDataReciviedError(Exception):
    """
    От сокета получены некорреткные данные
    """

    def __str__(self):
        return 'Принято некорректное сообщение от удаленого компьютера'


class NonDictInputError(Exception):
    """
    Аргумент функции  - не словарь
    """

    def __str__(self):
        return 'Аргумент функции должен быть словарь'


class ReqFieldMissingError(Exception):
    """
    Отсутсивует обязательное поле в принятом словаре
    """

    def __init__(self, missing_data):
        self.missing_data = missing_data

    def __str__(self):
        return f'В принятом словаре нет обязательного поля {self.missing_data}'
