"""имитация сервера"""
import logging
import os
import socket
import sys
import json

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, \
    MAX_CONNECTIONS
from common.errors import ReqFieldMissingError

import logs.server_log_config
LOG_SERVER = logging.getLogger('server.api')


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение
    от клиента, проверяет на валидность, возвращает словарь-ответ для клиента
    :param message:
    :return:
    """

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        LOG_SERVER.info('Ответ {RESPONSE: 200}')
        return {RESPONSE: 200}
    LOG_SERVER.warning('Ответ {RESPONSE: 200}')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def check_cmd_port():
    """
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию
    :return: порт
    """
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
        return listen_port
    except IndexError:
        # print('После параметра -\'p\' необходимо указывать номер порта')
        LOG_SERVER.error('IndexError: После параметра -\'p\' необходимо указывать номер порта')
        sys.exit()
    except ReqFieldMissingError as missing_error:
        LOG_SERVER.error(f'Нет поля {missing_error.missing_data}: Корректный порт в диапазоне 1024-65535')
        # print('Корректный порт в диапазоне 1024-65535')
        sys.exit()


def check_cmd_addr():
    """
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию
    :return: адрес
    """
    try:
        if '-a' in sys.argv:
            listen_addr = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addr = ''
        return listen_addr
    except IndexError:
        # print('После параметра -\'a\' необходимо указывать номер адрес, который слушает сервер')
        LOG_SERVER.error('IndexError: После параметра -\'a\' необходимо указывать номер адрес, который слушает сервер')
        sys.exit(1)


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию
    обработка порта
    server.ru -p 8888 -a 127.0.0.1
    :return:
    """
    #Получае логгер

    LOG_SERVER.debug('Start')

    # загружаем порт
    listen_port = check_cmd_port()
    LOG_SERVER.debug(f'получен порт {listen_port}')
    # Загружаем какой адрес слушать
    listen_addr = check_cmd_addr()
    LOG_SERVER.debug(f'получен адрес {listen_addr}')
    # Готовим сокет к передаче
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    transport.bind((listen_addr, listen_port))

    # Слушаем порт
    LOG_SERVER.debug(f'слушаем адрес {listen_addr}:{listen_port}')
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_addr = transport.accept()
        try:
            message_from_client = get_message(client)
            LOG_SERVER.debug(f'получено сообщение {message_from_client}')
            # print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except json.JSONDecodeError:
            # print('Принято некорректное сообщение')
            LOG_SERVER.error(f'Не удалось декодировать строку JSON')
            client.close()
        except ReqFieldMissingError as missing_error:
            LOG_SERVER.error(f'В ответе сервера нет необходимого поля {missing_error.missing_data}')


if __name__ == '__main__':
    main()
