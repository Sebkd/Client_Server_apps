"""имитация сервера"""
import argparse
import logging
import os
import select
import socket
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.utils import get_message, send_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_PORT, \
    MAX_CONNECTIONS, SENDER, MESSAGE, MESSAGE_TEXT, RESPONSE_200, RESPONSE_400, DESTINATION
from decos import log

import logs.server_log_config

LOG_SERVER = logging.getLogger('server.api')


@log
def process_client_message(message, messages_list, client, clients, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, отправляет словарь-ответ в случае необходимости.
    :param message:
    :param messages_list:
    :param client:
    :param clients:
    :param names:
    :return:
    """
    LOG_SERVER.debug(f'Разбор сообщения от клиента: {message}')
    # если это сообщение о том что есть клиент, принимаем и отвечаем, если валидно
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        # Если такой пользователь ещё не зарегистрирован, то регистрируем
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
            LOG_SERVER.info('Ответ о присутствии клиента {RESPONSE: 200}')
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    # если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message and \
            SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        LOG_SERVER.info(f'Добавлена очередь сообщений {message[SENDER]} '
                        f'к {message[DESTINATION]} : {message[MESSAGE_TEXT]}')
        return
    # Иначе Bad Requests
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен'
        send_message(client, response)
        return

@log
def process_msg(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        LOG_SERVER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        LOG_SERVER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')

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

    # Словарь, содержащий именя пользователей и соотвествующие им сокеты
    # {client_name: client_socket}
    names = dict()

    # Слушаем порт
    LOG_SERVER.debug(f'слушаем адрес {listen_addr}:{listen_port}')
    transport.listen(MAX_CONNECTIONS)

    # Основной цикл программы
    while True:
        # Ждем подключения, если таймаут вышел, то ловим исключение

        try:
            client, client_addr = transport.accept()
        except OSError as err:

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
                                           msgs, client_with_msg, clients, names)
                except Exception:
                    LOG_SERVER.info(f'Клиент {client_with_msg.getpeername()} '
                                    f'отключился от сервера.')
                    clients.remove(client_with_msg)

        # Если есть сообщения для отправки и ожидающие клиенты,
        # отправляем им сообщение.

        for i in msgs:
            try:
                process_msg(i, names, send_data_lst)
            except Exception:
                LOG_SERVER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        msgs.clear()


if __name__ == '__main__':
    main()
