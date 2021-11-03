"""Server programm"""

import socket
import sys
import json
import logging
import logs.server_log_config
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_ETHERNET_PORT, RESPONSE_DEFAULT_IP_ADDRESS, DEFAULT_IP
from common.utils import get_data, send_data
from errors import IncorrectDataReceivedError

SERVER_LOGGER = logging.getLogger('server')


def check_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug(f'Сообщение от пользователя {message[USER][ACCOUNT_NAME]} корретно')
        return {RESPONSE: 200}

    SERVER_LOGGER.debug(f'Не корректное сообщение от пользователя {message[USER][ACCOUNT_NAME]}')
    return {
        RESPONSE_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """

    try:
        SERVER_LOGGER.debug('Проверка введенного порта')
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = DEFAULT_ETHERNET_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        SERVER_LOGGER.info(f'Порт сервера {server_port}')

    except IndexError:
        SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        SERVER_LOGGER.debug('Проверка введенного ip адреса')
        if '-a' in sys.argv:
            server_ip_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_ip_address = DEFAULT_IP
        SERVER_LOGGER.info(f'IP адрес {server_ip_address}')

    except IndexError:
        SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((server_ip_address, server_port))

    # Слушаем порт

    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_data(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = check_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_data(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от {client_address}.')
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'Приняты некорретное сообщение от клиента {client_address}.')
            client.close()


if __name__ == '__main__':
    main()
