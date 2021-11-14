"""Программа-клиент"""

import sys
import json
import socket
import time
import logging
import logs.client_log_config
import threading

from decor import Log
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, EXIT
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
def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name
    }


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
        elif message[RESPONSE] == 409:
            CLIENT_LOGGER.debug(f'Статус сообщения "409 : Bad name client"')
            return '409 : Bad name client'
        elif message[RESPONSE] == 400:
            CLIENT_LOGGER.debug(f'Статус сообщения 400 : {message[ERROR]}')
            raise ServerError(f'400: {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@Log()
def message_from_server(sock, username):
    while True:
        pass
    # print(sock)
    # if ACTION in sock and sock[ACTION] == MESSAGE and \
    #         SENDER in sock and MESSAGE_TEXT in sock:
    #     print(f'Получено сообщение от пользователя '
    #           f'{sock[SENDER]}:\n{sock[MESSAGE_TEXT]}')
    #     CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
    #                        f'{sock[SENDER]}:\n{sock[MESSAGE_TEXT]}')
    # else:
    #     CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {sock}')


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
def initializing_client_interface(sock, username):
    # print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'send':
            create_message(sock, username)
        elif command == 'help':
            pass
            # print_help()
        elif command == 'exit':
            send_data(sock, create_exit_message(username))
            print('Завершение соединения.')
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            # Задержка неоходима, чтобы успело уйти сообщение о выходе
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


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

        while True:
            client_name = input('Введите имя клиента: ')
            send_data(transport, create_client_info(client_name))
            answer_from_server = check_answer(get_data(transport))
            if answer_from_server == '200 : OK':
                break
            else:
                print('Данное имя занято')
            CLIENT_LOGGER.debug(f'Ответ сервера {answer_from_server}')

        CLIENT_LOGGER.info(f'Имя клиента {client_name}')
        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(f'Сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{error.missing_field}')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_ip_address}:{server_eth_port}, '
                               f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        client_interface = threading.Thread(target=initializing_client_interface, args=(transport, client_name))
        client_interface.daemon = True
        client_interface.start()
        CLIENT_LOGGER.debug('Запущены процессы')

        while True:
            time.sleep(1)
            if receiver.is_alive() and client_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
