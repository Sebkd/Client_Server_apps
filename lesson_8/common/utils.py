import json
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decos import log
from common.errors import IncorrectDataReciviedError, NonDictInputError


@log
def get_message(client):
    """прием и декодирование сообщения
    принимает байты, возвращает словарь.
    если принято, что то другое возвращает ValueError"""

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataReciviedError
    else:
        raise IncorrectDataReciviedError



@log
def send_message(sock, message):
    """кодирование и отправка сообщения
    принимает словарь, делает словарь, кодирует в байты
     и отправляет"""

    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
