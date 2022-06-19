"""имитация сервера"""
import argparse
import logging
import os
import select
import socket
import sys
import json
import time

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, \
    MAX_CONNECTIONS, SENDER, MESSAGE, MESSAGE_TEXT
from common.errors import ReqFieldMissingError
from decos import log

import logs.server_log_config

LOG_SERVER = logging.getLogger('server.api')


@log
def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение
    от клиента, проверяет на валидность, возвращает словарь-ответ для клиента
    :param message:
    :return:
    """
    LOG_SERVER.debug(f'Разбор сообщения от клиента: {message}')
    # если это сообщение о том что есть клиент, принимаем и отвечаем, если валидно
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        LOG_SERVER.info('Ответ о присутствии клиента {RESPONSE: 200}')
        return
    # если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        LOG_SERVER.info(f'Добавленна очередь сообщений {message[ACCOUNT_NAME]} : {message[MESSAGE_TEXT]}')
        return
    # Иначе Bad Requests
    else:
        send_message(client,
                     {
                         RESPONSE: 400,
                         ERROR: 'Bad Request'
                     })
        return


@log
def check_cmd():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        LOG_SERVER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаем значения по умолчанию
    обработка порта
    server.ru -p 8888 -a 127.0.0.1
    :return:
    """
    # Получаем логгер

    LOG_SERVER.debug('Start')

    listen_addr, listen_port = check_cmd()

    LOG_SERVER.info(
        f'Запущен сервер, порт для подключений: {listen_port}, '
        f'адрес с которого принимаются подключения: {listen_addr}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет к передаче
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    transport.bind((listen_addr, listen_port))
    transport.settimeout(0.5)

    # список клиентов, очередь сообщений
    clients = []
    msgs = []

    # Слушаем порт
    LOG_SERVER.debug(f'слушаем адрес {listen_addr}:{listen_port}')
    transport.listen(MAX_CONNECTIONS)

    # Основной цикл программы
    while True:
        # Ждем подключения, если таймаут вышел, то ловим исключение

        try:
            client, client_addr = transport.accept()
        except OSError as err:
            print(err.errno)  # The error number returns None because it's just a timeout
            pass
        else:
            LOG_SERVER.info(f'Установлено соедение с ПК {client_addr}')
            clients.append(client)

        # списки для SELECT
        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        # проверяем наличие ждущих клиентов
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.

        if recv_data_lst:
            for client_with_msg in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_msg),
                                           msgs, client_with_msg)
                except:
                    LOG_SERVER.info(f'Клиент {client_with_msg.getpeername()} '
                                    f'отключился от сервера.')
                    clients.remove(client_with_msg)

        # Если есть сообщения для отправки и ожидающие клиенты,
        # отправляем им сообщение.

        if send_data_lst and msgs:
            msg = {
                ACTION: MESSAGE,
                SENDER: msgs[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: msgs[0][1]
            }
            del msgs[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message=msg)
                except:
                    LOG_SERVER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
