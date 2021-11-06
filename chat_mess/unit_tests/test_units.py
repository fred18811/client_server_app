import json
import unittest

from common.utils import get_data, send_data
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, ENCODING, RESPONSE


class TestSocket:

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message):
        json_msg = json.dumps(self.test_dict)
        self.encoded_message = json_msg.encode(ENCODING)
        self.received_message = message

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_message = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'test'
        }
    }

    def test_send_data_ok(self):
        test_socket = TestSocket(self.test_message)
        send_data(test_socket, self.test_message)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)

    def test_get_data_ok(self):
        test_socket = TestSocket(self.test_message)
        self.assertEqual(get_data(test_socket), self.test_message)

    def test_get_data_raise(self):
        test_socket = TestSocket([])
        self.assertRaises(ValueError, get_data, test_socket)


if __name__ == '__main__':
    unittest.main()
