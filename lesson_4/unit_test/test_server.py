"""unit-test server"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT
from server import check_cmd_port, check_cmd_addr, process_client_message


class TestClassServer(unittest.TestCase):
    """
    Класс с тестами для client
    """

    def setUp(self) -> None:
        self.err_dict = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        self.ok_dict = {RESPONSE: 200}

    def tearDown(self) -> None:
        pass

    def test_def_check_cmd_port(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 8888, '-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-p', 8888, '-a', '127.0.0.1']
        test_check_cmd_port = 8888
        self.assertEqual(check_cmd_port(), test_check_cmd_port)

    def test_def_check_cmd_port_wot_p(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-a', '127.0.0.1']
        test_check_cmd_port = DEFAULT_PORT
        self.assertEqual(check_cmd_port(), test_check_cmd_port)

    def test_def_check_cmd_port_value_error_min(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 1020, '-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-p', 1020, '-a', '127.0.0.1']
        try:
            self.assertRaises(ValueError, check_cmd_port)
        except SystemExit:
            print()

    def test_def_check_cmd_port_value_error_max(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 65600, '-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-p', 65600, '-a', '127.0.0.1']
        try:
            self.assertRaises(ValueError, check_cmd_port)
        except SystemExit:
            print()

    def test_def_check_cmd_port_index_error(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', '-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-p', '-a', '127.0.0.1']
        try:
            self.assertRaises(IndexError, check_cmd_port)
        except SystemExit:
            print()

    def test_def_check_cmd_addr(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 7777, '-a', '127.0.0.1']
        :return:
        """
        sys.argv = ['-p', 8888, '-a', '127.0.0.2']
        test_check_cmd_addr = '127.0.0.2'
        self.assertEqual(check_cmd_addr(), test_check_cmd_addr)

    def test_def_check_cmd_addr_wot_a(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 8888]
        :return:
        """
        sys.argv = ['-p', 8888]
        test_check_cmd_addr = ''
        self.assertEqual(check_cmd_addr(), test_check_cmd_addr)

    def test_def_check_cmd_addr_index_error(self):
        """
        Тест проверки выходного значения, когда sys.argv = ['-p', 8888, '-a']
        :return:
        """
        sys.argv = ['-p', 8888, '-a']
        try:
            self.assertRaises(IndexError, check_cmd_addr)
        except SystemExit:
            print()

    def test_process_client_message_ok(self):
        """
        Корректный запрос
        :return:
        """
        test_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        self.assertEqual(process_client_message(test_msg), self.ok_dict)

    def test_process_client_message_no_action(self):
        """
        Ощибка если нет действия
        :return:
        """
        test_msg = {
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        self.assertEqual(process_client_message(test_msg), self.err_dict)

    def test_process_client_message_wrong_action(self):
        """
        Ощибка если неизвестное действие
        :return:
        """
        test_msg = {
            ACTION: 'Wrong',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        self.assertEqual(process_client_message(test_msg), self.err_dict)

    def test_process_client_message_no_time(self):
        """
        Ощибка если нет времени
        :return:
        """
        test_msg = {
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        self.assertEqual(process_client_message(test_msg), self.err_dict)


    def test_process_client_message_no_user(self):
        """
        Ощибка если нет юзера
        :return:
        """
        test_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
        }

        self.assertEqual(process_client_message(test_msg), self.err_dict)

    def test_process_client_message_unknown_user(self):
        """
        Ощибка если нет юзера
        :return:
        """
        test_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'God',
            }
        }

        self.assertEqual(process_client_message(test_msg), self.err_dict)


if __name__ == '__main__':
    unittest.main()
