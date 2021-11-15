"""Utils"""

import json
import sys

from common.variables import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_ETHERNET_PORT, DEFAULT_IP, DEFAULT_MODE_CLIENT
from decor import Log
from errors import IncorrectClientMode


@Log()
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


@Log()
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


@Log()
def get_port_server(logger):
    try:
        logger.debug('Проверка введенного порта')
        if '-p' in sys.argv:
            server_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            server_port = DEFAULT_ETHERNET_PORT
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        logger.info(f'Порт сервера {server_port}')
        return server_port
    except IndexError:
        logger.critical('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        logger.critical('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)


@Log()
def get_ip_server(logger):
    try:
        logger.debug('Проверка введенного ip адреса')
        if '-a' in sys.argv:
            server_ip_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            server_ip_address = DEFAULT_IP
        logger.info(f'IP адрес {server_ip_address}')
        return server_ip_address
    except IndexError:
        logger.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)


@Log()
def get_client_name(logger):
    try:
        logger.debug('Проверка введенного имени клиента')
        if '-n' in sys.argv:
            client_name = sys.argv[sys.argv.index('-n') + 1]
            logger.info(f'Имя клиента {client_name}')
            return client_name
    except IndexError:
        logger.critical('После параметра \'n\'- необходимо указать имя.')
        sys.exit(1)
