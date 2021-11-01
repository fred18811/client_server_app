"""Utils"""

import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING


def get_data(client):
    """
    Утилита приёма и декодирования сообщения
    принимает байты выдаёт словарь, если приняточто-то другое отдаёт ошибку значения
    :param client:
    :return:
    """

    encoded_answer = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_answer, bytes):
        json_answer = encoded_answer.decode(ENCODING)
        answer = json.loads(json_answer)
        if isinstance(answer, dict):
            return answer
        raise ValueError
    raise ValueError


def send_data(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    :param sock:
    :param message:
    :return:
    """

    js_data = json.dumps(message)
    encoded_data = js_data.encode(ENCODING)
    sock.send(encoded_data)
