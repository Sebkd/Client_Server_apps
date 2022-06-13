"""unit-test client"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDR, \
    DEFAULT_PORT
from client import create_presense, process_ans, check_cmd


class TestClassClient(unittest.TestCase):
    """
    Класс с тестами для client
    """

    def setUp(self) -> None:
        sys.argv = ['127.0.0.1', DEFAULT_IP_ADDR, DEFAULT_PORT]

    def tearDown(self) -> None:
        pass

    def test_def_create_presense(self):
        """
        Тест корректного запроса
        :return:
        """
        test = create_presense()
        test[TIME] = 1.1
        model_out = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        self.assertEqual(test, model_out)

    def test_def_process_ans_200(self):
        """
        Тест корректного разбора ответа 200
        :return:
        """
        test_message = {RESPONSE: 200}
        self.assertEqual(process_ans(test_message), '200 : OK')

    def test_def_process_ans_400(self):
        """
        Тест корректного разбора ответа 400
        :return:
        """
        test_message = {RESPONSE: 400, ERROR: 'Bad Request'}
        self.assertEqual(process_ans(test_message), '400 : Bad Request')

    def test_def_process_ans_no_response(self):
        """
        Тест если не пришло поле RESPONSE
        :return:
        """
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})

    def test_check_cmd_value_error(self):
        """
        Тест не корреткный номер порта
        :return:
        """
        sys.argv[1], sys.argv[2] = DEFAULT_IP_ADDR, 1020
        try:
            self.assertRaises(ValueError, check_cmd)
        except SystemExit:
            print()

    def test_check_cmd_index_error(self):
        """
        Тест не корреткный номер порта
        :return:
        """
        sys.argv = []
        model_index_error = (DEFAULT_IP_ADDR, DEFAULT_PORT)
        test_check_cmd = tuple(check_cmd())
        self.assertEqual(test_check_cmd, model_index_error)


if __name__ == '__main__':
    unittest.main()
