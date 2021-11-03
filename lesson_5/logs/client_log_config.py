import os
import logging
import sys

from common.variables import LOGGING_LEVEL, LOGGING_FORMATTER, LOGGING_FOLDER, LOGGING_CLIENT_NAME

CLIENT_FORMATTER = logging.Formatter(LOGGING_FORMATTER)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, LOGGING_FOLDER)
PATH = os.path.join(PATH, LOGGING_CLIENT_NAME)

CONSOLE_HANDLER = logging.StreamHandler(sys.stderr)
CONSOLE_HANDLER.setFormatter(CLIENT_FORMATTER)
CONSOLE_HANDLER.setLevel(logging.ERROR)

FILE_HANDLER = logging.FileHandler(PATH, encoding='utf8')
FILE_HANDLER.setFormatter(CLIENT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(CONSOLE_HANDLER)
LOGGER.addHandler(FILE_HANDLER)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Critical err')
    LOGGER.error('error')
    LOGGER.debug('debug message')
    LOGGER.info('info message')
