import json
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), 'lesson_3'))
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decos import log


@log
def get_message(client):
    """прием и декодирование сообщения
    принимает байты, возвращает словарь.
    если принято, что то другое возвращает ValueError"""

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    # encoded_response = client.recv()
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    """кодирование и отправка сообщения
    принимает словарь, делает словарь, кодирует в байты
     и отправляет"""

    if not isinstance(message, dict):
        raise TypeError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
