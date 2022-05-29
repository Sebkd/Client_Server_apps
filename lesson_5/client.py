"""Имитация клиента"""
import os
import sys
import json
import socket
import time



sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT
from common.errors import ReqFieldMissingError

import logging
import logs.client_log_config
LOG_CLIENT = logging.getLogger('client.api')


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
            LOG_CLIENT.info('Ответ {RESPONSE: 200}')
            return '200 : OK'
        LOG_CLIENT.warning('Ответ {RESPONSE: 200}')
        return f'400 : {message[ERROR]}'
    raise ValueError


def check_cmd():
    """Загрузка параметров командной строки"""
    try:
        server_addr = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            LOG_CLIENT.critical(f'Корректный порт должен быть в диапазоне 1024-65535, '
                                f'здесь порт {server_port}')
            raise ValueError
        return server_addr, server_port
    except IndexError:
        server_addr = DEFAULT_IP_ADDR
        server_port = DEFAULT_PORT
        return server_addr, server_port
    except ValueError:
        LOG_CLIENT.error(f'некорректный порт')
        # print('Корректный порт в диапазоне 1024-65535')
        sys.exit()


def main():
    """Загрузка параметров командной строки"""
    LOG_CLIENT.debug('Start')

    server_addr, server_port = check_cmd()
    LOG_CLIENT.info(f'Получен адрес {server_addr} : {server_port}')

    # инициализация сокета
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_addr, server_port))
        message_to_server = create_presense()
        send_message(transport, message_to_server)

        answer = process_ans(get_message(transport))
        LOG_CLIENT.info(f'Принят ответ {server_addr} : {server_port} от сервера "{answer}"')
        print(f'{server_addr} : {server_port} ---> {answer}')
    except json.JSONDecodeError:
        LOG_CLIENT.error('Ошибка декодирования')
        # print('Ошибка декодирования')
    except ConnectionRefusedError:
        LOG_CLIENT.critical(f'Не удалось подключиться по адресу {server_addr} : {server_port}, запрос на '
                            f'на подключение отвергнут')
    except ReqFieldMissingError as missing_error:
        LOG_CLIENT.error(f'В ответе сервера нет необходимого поля {missing_error.missing_data}')


if __name__ == '__main__':
    main()
