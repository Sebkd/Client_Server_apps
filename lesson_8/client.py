"""Имитация клиента"""
import argparse
import os
import sys
import json
import socket
import time
import threading

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_7'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, EXIT, DESTINATION
from common.errors import ReqFieldMissingError, ServerError, IncorrectDataReciviedError
from decos import log

import logging
import logs.client_log_config

LOG_CLIENT = logging.getLogger('client.api')


@log
def create_exit_message(account_name):
    """Функция создает словарб с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


@log
def msg_from_server(sock, my_username):
    """Функция обработчик сообщений других пользователей, которые приходят с сервера"""
    while True:
        try:
            msg = get_message(sock)
            if ACTION in msg and msg[ACTION] == MESSAGE and \
                    SENDER in msg and DESTINATION in msg \
                    and MESSAGE_TEXT in msg and msg[DESTINATION] == my_username:
                print(50 * "*")
                print(f'Получено сообщение от пользователя '
                      f'{msg[SENDER]}:\n{msg[MESSAGE_TEXT]}')
                LOG_CLIENT.info(f'Получено сообщение от пользователя '
                                f'{msg[SENDER]}:\n{msg[MESSAGE_TEXT]}')
                print(50 * "*")
                print_help()
            else:
                LOG_CLIENT.error(f'Получено сообщение с ошибкой с сервера {msg}')
        except IncorrectDataReciviedError:
            LOG_CLIENT.error(f'Не удалось декодировать полученное сообщение.')
        except (OSError, ConnectionError, ConnectionAbortedError,
                ConnectionResetError, json.JSONDecodeError):
            LOG_CLIENT.critical(f'Потеряно соединение с сервером.')
            break


@log
def create_msg(sock, account_name='Guest'):
    """Функция создания сообщения: кому отправить и само сообщение"""
    to_user = input('Введите получателя сообщения: ')
    msg = input('Введите сообщение для отправки: ')
    msg_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: msg
    }
    LOG_CLIENT.debug(f'Сформированно сообщение {msg_dict}')
    try:
        send_message(sock, msg_dict)
        LOG_CLIENT.info(f'Отправлено сообщение для пользователя {to_user}')
        print(50*"*")
    except Exception as e:
        print(e)
        LOG_CLIENT.critical('Потеряно соединение с сервером.')
        sys.exit(1)


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


@log
def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_msg(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            LOG_CLIENT.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def create_presense(account_name):
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
    parser.add_argument('-n', '--name', default='', nargs='?')
    namespaces = parser.parse_args(sys.argv[1:])
    server_addr = namespaces.addr
    server_port = namespaces.port
    client_name = namespaces.name

    # проверяем порт
    if server_port < 1024 or server_port > 65535:
        LOG_CLIENT.critical(f'Корректный порт должен быть в диапазоне 1024-65535, '
                            f'здесь порт {server_port}. Клиент завершается')
        sys.exit(1)

    return server_addr, server_port, client_name


@log
def main():
    """Загрузка параметров командной строки"""
    LOG_CLIENT.debug('Start')

    server_addr, server_port, client_name = check_cmd()
    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')


    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя: ')

    print(f'Получен адрес {server_addr} : {server_port}, '
                    f'Имя пользователя: {client_name}')

    LOG_CLIENT.info(f'Получен адрес {server_addr} : {server_port}, '
                    f'Имя пользователя: {client_name}')

    # инициализация сокета
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_addr, server_port))
        message_to_server = create_presense(client_name)
        send_message(transport, message_to_server)

        answer = process_ans(get_message(transport))
        LOG_CLIENT.info(f'Принят ответ {server_addr} : {server_port}. Ответ сервера "{answer}"')
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
    except (ConnectionRefusedError, ConnectionError):
        LOG_CLIENT.critical(f'Не удалось подключиться по адресу {server_addr} : {server_port}, запрос на '
                            f'на подключение отвергнут')
        sys.exit(1)
    else:
        # соединение установлено, ошибок нет, начинается обмен согласно режиму
        # запускаем клиентский процесс приёма сообщений
        receiver = threading.Thread(target=msg_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # затем запускаем отправку сообщений и взаимодействие с пользователем.
        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        LOG_CLIENT.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
