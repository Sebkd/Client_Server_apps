"""
Простое логгирование серверной части
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

# Создаём объект-логгер с именем server
LOG = logging.getLogger('server.api')

# Создаём объект форматирования:
FORMATTER = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s ")

# Создаём файловый обработчик логгирования (можно задать кодировку):
FILE_HANDLER = logging.handlers.TimedRotatingFileHandler("server.api.log", encoding='utf-8')
FILE_HANDLER.setLevel(logging.DEBUG)

FILE_HANDLER.setFormatter(FORMATTER)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
LOG.addHandler(FILE_HANDLER)
LOG.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
    STREAM_HANDLER = logging.StreamHandler()
    STREAM_HANDLER.setLevel(logging.DEBUG)
    STREAM_HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(STREAM_HANDLER)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    LOG.debug('Отладочное сообщение server.api')
