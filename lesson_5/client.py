"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import logs.client_log_config
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP, DEFAULT_ETHERNET_PORT, PORT
from common.utils import get_data, send_data
from errors import ReqFieldMissingError

CLIENT_LOGGER = logging.getLogger('client')


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
    CLIENT_LOGGER.debug(f'Сформировано сообщение {PRESENCE} для пользователя {account_name}')
    return out


def check_ans(message):
    """
    Функция разбирает ответ сервера
    :param message:
    :return:
    """
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOGGER.debug(f'Статус сообщения "200 : OK"')
            return '200 : OK'
        CLIENT_LOGGER.debug(f'Статус сообщения 400 : {message[ERROR]}')
        return f'400 : {message[ERROR]}'
    raise ValueError


def main():
    """Загружаем параметы коммандной строки"""
    try:
        CLIENT_LOGGER.debug('Проверка введенного ip адреса')
        server_ip_address = sys.argv[2]
    except IndexError:
        server_ip_address = DEFAULT_IP
        CLIENT_LOGGER.debug(f'IP адрес сервера не был указан, адрес по умолчанию {DEFAULT_IP}')

    try:
        CLIENT_LOGGER.debug('Проверка введенного порта')
        server_eth_port = int(sys.argv[1])
        if server_eth_port < 1024 or server_eth_port > 65535:
            raise ValueError
    except IndexError:
        server_eth_port = DEFAULT_ETHERNET_PORT
        CLIENT_LOGGER.debug(f'Порт сервера не был указан, адрес по умолчанию {DEFAULT_ETHERNET_PORT}')
    except ValueError:
        CLIENT_LOGGER.error('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_ip_address} , порт: {server_eth_port}')
    # Инициализация сокета и обмен
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_ip_address, server_eth_port))
        message_to_server = create_message(port=server_eth_port)
        send_data(transport, message_to_server)
        answer = check_ans(get_data(transport))
        CLIENT_LOGGER.debug(f'Ответ сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{ReqFieldMissingError.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_ip_address}:{server_eth_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
