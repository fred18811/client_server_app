"""Server programm"""
import select
import socket
import logging

import logs.server_log_config

from decor import Log
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, MESSAGE, \
    MESSAGE_TEXT, SENDER, EXIT, DESTINATION, ALL
from common.utils import get_data, send_data, get_port_server, get_ip_server

SERVER_LOGGER = logging.getLogger('server')


@Log()
def check_client_message(message, messages_lst, client, clients, names):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :param messages_lst:
    :param client:
    :param clients:
    :param names:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            SERVER_LOGGER.debug(f'Пользователь {message[USER][ACCOUNT_NAME]} распознан')
            send_data(client, {RESPONSE: 200})
        else:
            send_data(client, {
                RESPONSE: 409,
                ERROR: 'Имя пользователя уже занято.'
            })
        return
    elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and \
            TIME in message and SENDER in message and MESSAGE_TEXT in message:
        SERVER_LOGGER.debug(f'Сообщение от пользователя {message[SENDER]} получено')
        messages_lst.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        send_data(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        SERVER_LOGGER.debug(f'Не корректное сообщение от пользователя {message[USER][ACCOUNT_NAME]}')
        return


@Log()
def sending_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_data(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] == ALL:
        for name in names:
            message[DESTINATION] = name
            send_data(names[name], message)
        SERVER_LOGGER.info(f'Отправлено сообщение всем '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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
    names = dict()

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
            if clients:
                read_data_lst, write_data_lst, errors_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if read_data_lst:
            for client_msg in read_data_lst:
                try:
                    check_client_message(get_data(client_msg), messages, client_msg, clients, names)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_msg.getpeername()} отключился.')
                    clients.remove(client_msg)

        for i in messages:
            try:
                SERVER_LOGGER.debug(f'Sending messages')
                sending_message(i, names, write_data_lst)
            except:
                if not i[DESTINATION] == ALL:
                    SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                    clients.remove(names[i[DESTINATION]])
                    del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
