import unittest

from client import create_message, check_ans
from common.variables import DEFAULT_ETHERNET_PORT, ERROR


class TestClass(unittest.TestCase):
    message = create_message()

    def test_default_port_message(self):
        self.assertEqual(DEFAULT_ETHERNET_PORT, self.message['port'])

    def test_custom_port_message(self):
        self.assertEqual(8888, create_message(port=8888)['port'])

    def test_default_user_message(self):
        self.assertEqual('Guest', self.message['user']['account_name'])

    def test_custom_user_message(self):
        self.assertEqual('Test', create_message(account_name='Test')['user']['account_name'])

    def test_no_response(self):
        self.assertRaises(ValueError, check_ans, {ERROR: 'Bad Request'})

    def test_message_not_none(self):
        self.assertIsNotNone(create_message())


if __name__ == '__main__':
    unittest.main()
