"""
Константы для проекта
"""

DEFAULT_PORT = 7777
DEFAULT_IP_ADDR = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 1024
ENCODING = 'utf-8'

# Ключи для протокола JIM
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'

# Прочие ключи
PRESENCE = 'presense'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'msg_txt'
EXIT = 'exit'

# Словари-ответы
# 200
RESPONSE_200 = {RESPONSE: 200}
# 400
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None
}
