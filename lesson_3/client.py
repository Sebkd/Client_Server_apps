"""Имитация клиента"""

import sys
import json
import socket
import time

from lesson_3.utils import get_message, send_message
from lesson_3.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT


def create_presense(account_name='Guest'):
    """Генерируем запрос о присутствии клиента"""

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    return out


def process_ans(message):
    """Разборка ответа клиента"""

    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    """Загрузка параметров командной строки"""
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_addr = DEFAULT_IP_ADDR
        server_port = DEFAULT_PORT
    except ValueError:
        print('Корректный порт в диапазоне 1024-65535')
        sys.exit()

    # инициализация сокета

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_addr, server_port))
    message_to_server = create_presense()
    send_message(transport, message_to_server)
    try:
        answer = process_ans(get_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Ошибка декодирования')


if __name__ == '__main__':
    main()
