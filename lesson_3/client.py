"""Программа-клиент"""

import sys
import json
import socket
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP, DEFAULT_ETHERNET_PORT, PORT
from common.utils import get_data, send_data


def create_message(account_name='Guest', port=DEFAULT_ETHERNET_PORT):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :param port:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        PORT: port,
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def check_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    """Загружаем параметы коммандной строки"""
    try:
        server_ip_address = sys.argv[2]
        server_eth_port = int(sys.argv[1])
        if server_eth_port < 1024 or server_eth_port > 65535:
            raise ValueError
    except IndexError:
        server_ip_address = DEFAULT_IP
        server_eth_port = DEFAULT_ETHERNET_PORT
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_ip_address, server_eth_port))
    message_to_server = create_message(port=server_eth_port)
    send_data(transport, message_to_server)
    try:
        answer = check_ans(get_data(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
