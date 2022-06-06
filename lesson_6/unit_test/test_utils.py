"""unit-test utils"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import MAX_PACKAGE_LENGTH, ENCODING, ACTION, PRESENCE, TIME, USER, \
    ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT

from common.utils import send_message, get_message


class TestClassSocket:
    """
    Тестовый класс для формирования словаря, который будет прогоняться через тестовую
    функцию для тестирования отправки и получения сообщения
    """

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_msg = None
        self.recieved_msg = None

    def send(self, message_to_send):
        """
        Функция формирующая на отправку корректно кодируемое сообщение, а также
        сохарняющая сообщение, что должно отправится
        :param message_to_send:
        :return:
        """
        json_test_msg = json.dumps(self.test_dict)
        self.encoded_msg = json_test_msg.encode(ENCODING)
        self.recieved_msg = message_to_send

    def recv(self):
        """
        Получение данных из сокета
        :return:
        """
        json_test_msg = json.dumps(self.test_dict)
        return json_test_msg.encode(ENCODING)


class TestClassUtils(unittest.TestCase):
    """
    Класс с тестами для utils
    """

    def setUp(self) -> None:
        MAX_PACKAGE_LENGTH = None
        self.test_dict_send = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'test',
            }
        }

        self.test_dict_recv_ok = {RESPONSE: 200}
        self.test_dict_recv_err = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def tearDown(self) -> None:
        pass

    def test_def_send_message_true(self):
        """
        Тестируем корректность работы функции отправки
        создаем тестовый сокет и проверяем корреткность отправки словаря
        :return:
        """
        test_socket = TestClassSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты которой будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)

        # Проверка корректности кодирования словаря
        # Сравнение результата кодирования и результата тестируемой функции
        self.assertEqual(test_socket.encoded_msg, test_socket.recieved_msg)

    def test_def_send_message_with_error(self):
        """
        Тестируем корректность работы функции отправки
        создаем тест-сокет и проверим корректность отправки словаря
        :return:
        """
        test_socket = TestClassSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты которой будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)

        # проверка исключения при не словаре на входе

        self.assertRaises(TypeError, send_message, test_socket, 'wrong')

    def test_def_get_message_ok(self):
        """
        Тест функции приема сообщения
        :return:
        """
        test_socket_ok = TestClassSocket(self.test_dict_recv_ok)
        # тест распаковки словаря

        self.assertEqual(get_message(test_socket_ok), self.test_dict_recv_ok)

    def test_def_get_message_err(self):
        """
        Тест функции приема сообщения
        :return:
        """
        test_socket_err = TestClassSocket(self.test_dict_recv_err)
        # тест распаковки словаря

        self.assertEqual(get_message(test_socket_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
