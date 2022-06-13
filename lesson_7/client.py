"""Имитация клиента"""
import argparse
import os
import sys
import json
import socket
import time

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_7'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.errors import ReqFieldMissingError, ServerError
from decos import log

import logging
import logs.client_log_config

LOG_CLIENT = logging.getLogger('client.api')


@log
def msg_from_server(msg):
    """Функция обработчик сообщений других пользователей, которые приходят с сервера"""
    if ACTION in msg and msg[ACTION] == MESSAGE and \
            SENDER in msg and MESSAGE_TEXT in msg:
        print(f'Получено сообщение от пользователя '
              f'{msg[SENDER]}:\n{msg[MESSAGE_TEXT]}')
        LOG_CLIENT.info(f'Получено сообщение от пользователя '
                        f'{msg[SENDER]}:\n{msg[MESSAGE_TEXT]}')
    else:
        LOG_CLIENT.error(f'Получено сообщение с ошибкой с сервера {msg}')


@log
def create_msg(sock, account_name='Guest'):
    """Функция создания сообщения с возможностью выхода по !!!"""
    msg = input('Введите сообщение для отправки или введите "!!!" для завершения работы: ')
    if msg == '!!!':
        sock.close()
        LOG_CLIENT.info('Завершение работы по команде !!!')
        print('Завершение работы по команде !!!')
        sys.exit(0)
    msg_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: msg
    }
    LOG_CLIENT.debug(f'Сформированно сообщение {msg_dict}')
    return msg_dict


@log
def create_presense(account_name='Guest'):
    """Генерируем запрос о присутствии клиента"""

    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name,
        }
    }
    LOG_CLIENT.debug(f'Сформировал {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_ans(message):
    """Разборка ответа клиента"""
    LOG_CLIENT.debug(f'Разбор приветственного сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            LOG_CLIENT.info('Ответ {RESPONSE: 200}')
            return '200 : OK'
        elif message[RESPONSE] == 400:
            LOG_CLIENT.warning('Ответ {RESPONSE: 400}')
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def check_cmd():
    """Загрузка параметров командной строки,
    выводим 3 параметра: адрес сервера, порт сервера, режим работы клиента"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDR, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespaces = parser.parse_args(sys.argv[1:])
    server_addr = namespaces.addr
    server_port = namespaces.port
    client_mode = namespaces.mode

    # проверяем порт
    if server_port < 1024 or server_port > 65535:
        LOG_CLIENT.critical(f'Корректный порт должен быть в диапазоне 1024-65535, '
                            f'здесь порт {server_port}. Клиент завершается')
        sys.exit(1)

    # проверка режима работы
    if client_mode not in ('listen', 'send'):
        LOG_CLIENT.critical(f'Указан недопустимый режим работы, '
                            f'здесь режим работы {client_mode}. '
                            f'Допустимые режимы: listen, send. '
                            f'Клиент завершается')
        sys.exit(1)
    return server_addr, server_port, client_mode

@log
def main():
    """Загрузка параметров командной строки"""
    LOG_CLIENT.debug('Start')

    server_addr, server_port, client_mode = check_cmd()
    LOG_CLIENT.info(f'Получен адрес {server_addr} : {server_port}, режим работы: {client_mode}')

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
        sys.exit(1)
    except ServerError as err:
        LOG_CLIENT.error(f'При установке соединения сервер вернул ошибку: {err.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        LOG_CLIENT.error(f'В ответе сервера нет необходимого поля {missing_error.missing_data}')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG_CLIENT.critical(f'Не удалось подключиться по адресу {server_addr} : {server_port}, запрос на '
                            f'на подключение отвергнут')
        sys.exit(1)
    else:
        # соединение установлено, ошибок нет, начинается обмен согласно режиму
        # основной цикл программы

        if client_mode == 'send':
            print('Режим работы - отправка сообщений')
        else:
            print('Режим работы - прием сообщений')
        while True:
            # режим работы send
            if client_mode == 'send':
                try:
                    send_message(transport, create_msg(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG_CLIENT.error(f'Соединение с сервером {server_addr} было потеряно.')
                    sys.exit(1)
            # режим работы listen
            if client_mode == 'listen':
                try:
                    msg_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    LOG_CLIENT.error(f'Соединение с сервером {server_addr} было потеряно.')
                    sys.exit(1)



if __name__ == '__main__':
    main()
