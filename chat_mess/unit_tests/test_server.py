import unittest
from server import check_client_message
from common.variables import TIME, USER, ACCOUNT_NAME, ACTION, PRESENCE, \
    RESPONSE_DEFAULT_IP_ADDRESS, ERROR


class TestClass(unittest.TestCase):
    response_ok = {'response': 200}
    response_bad = {
        RESPONSE_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }

    def test_ok(self):
        self.assertEqual(check_client_message({ACTION: PRESENCE, TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.response_ok)

    def test_bad_action_message(self):
        self.assertEqual(check_client_message({ACTION: 'test', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}),
                         self.response_bad)

    def test_bad_user_message(self):
        self.assertEqual(check_client_message({ACTION: PRESENCE, TIME: '1.1', USER: {ACCOUNT_NAME: 'Test'}}),
                         self.response_bad)


if __name__ == '__main__':
    unittest.main()
