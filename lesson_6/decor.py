import logs.client_log_config
import logs.server_log_config
import sys
import logging
import inspect

from functools import wraps


class Log:
    def __init__(self):
        if sys.argv[0].find('server.py') != -1:
            self.LOGGER = logging.getLogger('server')
        else:
            self.LOGGER = logging.getLogger('client')

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            # print(inspect.stack(context=1)[1][3])
            self.LOGGER.debug(
                f'Вызвана функция {func.__name__} с параметрами {args}, '
                f'{kwargs}.Функция вызвана в функции\молуле {inspect.stack(context=1)[1][3]}.'
            )
            res = func(*args, **kwargs)
            return res

        return decorated
