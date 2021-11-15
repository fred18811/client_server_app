"""Constants"""
import logging

# Порт поумолчанию для сетевого ваимодействия
DEFAULT_ETHERNET_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMATTER = '%(asctime)s %(levelname)-10s %(filename) -25s %(message)s'
LOGGING_FOLDER = 'data'
LOGGING_CLIENT_NAME = 'client.log'
LOGGING_SERVER_NAME = 'server.log'

# JIM protocol main keys:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
PORT = 'port'
SENDER = 'sender'
DESTINATION = 'to'
ALL = 'all'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONSE_DEFAULT_IP_ADDRESS = 'response_default_ip_address'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
DEFAULT_MODE_CLIENT = 'listen'
EXIT = 'exit'
