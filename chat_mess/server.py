"""Server programm"""
import select
import socket
import sys
import logging
import time

import logs.server_log_config

from decor import Log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, MESSAGE, \
    MESSAGE_TEXT, SENDER
from common.utils import get_data, send_data, get_port_server, get_ip_server

SERVER_LOGGER = logging.getLogger('server')


@Log()
def check_client_message(message, messages_lst, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :param messages_lst:
    :param client:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        SERVER_LOGGER.debug(f'Пользователь {message[USER][ACCOUNT_NAME]} распознан')
        send_data(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        SERVER_LOGGER.debug(f'Сообщение от пользователя {message[ACCOUNT_NAME]} получено')
        messages_lst.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_data(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        SERVER_LOGGER.debug(f'Не корректное сообщение от пользователя {message[USER][ACCOUNT_NAME]}')
        return


@Log()
def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8888 -a 127.0.0.1
    :return:
    """
    server_port = get_port_server(SERVER_LOGGER)
    server_ip_address = get_ip_server(SERVER_LOGGER)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((server_ip_address, server_port))
    transport.settimeout(0.5)

    transport.listen(MAX_CONNECTIONS)

    clients = []
    messages = []

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.debug(f'Установлено соедение с ПК {client_address}')
            clients.append(client)

        read_data_lst = []
        write_data_lst = []

        try:
            read_data_lst, write_data_lst, errors_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if read_data_lst:
            for client_msg in read_data_lst:
                try:
                    check_client_message(get_data(client_msg), messages, client_msg)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_msg.getpeername()} отключился.')
                    clients.remove(client_msg)

        if messages and write_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in write_data_lst:
                try:
                    send_data(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
