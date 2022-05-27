"""имитация сервера"""

import socket
import sys
import json

from lesson_3.utils import get_message, send_message
from lesson_3.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение
    от клиента, проверяет на валидность, возвращает словарь-ответ для клиента
    :param message:
    :return:
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию
    обработка порта
    server.ru -p 8888 -a 127.0.0.1
    :return:
    """

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметров -\'p\' необходимо указывать номер порта')
        sys.exit()
    except ValueError:
        print('Корректный порт в диапазоне 1024-65535')
        sys.exit()

        # Загружаем какой адрес слушать
