"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import logs.client_log_config

from decor import Log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_data, send_data, get_ip_server, get_port_server, get_client_mode
from errors import ReqFieldMissingError, ServerError

CLIENT_LOGGER = logging.getLogger('client')


@Log()
def create_client_info(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name:
    :return:
    """
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение {PRESENCE} для пользователя {account_name}')
    return out


@Log()
def check_answer(message):
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
        elif message[RESPONSE] == 400:
            CLIENT_LOGGER.debug(f'Статус сообщения 400 : {message[ERROR]}')
            raise ServerError(f'400: {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@Log()
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@Log()
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение или \'###\' для завершения работы: ')
    if message == '###':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Выход из системы')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@Log()
def main():
    """Загружаем параметы коммандной строки"""
    server_ip_address = get_ip_server(CLIENT_LOGGER)
    server_eth_port = get_port_server(CLIENT_LOGGER)
    client_mode = get_client_mode(CLIENT_LOGGER)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: {server_ip_address} , порт: {server_eth_port}/'
                       f', режим {client_mode}')

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_ip_address, server_eth_port))
        send_data(transport, create_client_info())
        answer_from_server = check_answer(get_data(transport))
        CLIENT_LOGGER.debug(f'Ответ сервера {answer_from_server}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError:
        CLIENT_LOGGER.error(f'Сервер вернул ошибку: {ServerError.text}')
        sys.exit(1)
    except ReqFieldMissingError:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{ReqFieldMissingError.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_ip_address}:{server_eth_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)

    if client_mode == 'send':
        print('Отправка сообщений.')
    else:
        print('Приём сообщений.')

    while True:
        if client_mode == 'send':
            try:
                send_data(transport, create_message(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером {server_ip_address} было потеряно.')
                sys.exit(1)

        if client_mode == 'listen':
            try:
                message_from_server(get_data(transport))
            except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                CLIENT_LOGGER.error(f'Соединение с сервером {server_ip_address} было потеряно.')
                sys.exit(1)


if __name__ == '__main__':
    main()
