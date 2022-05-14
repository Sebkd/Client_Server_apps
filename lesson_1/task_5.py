"""
5. Написать код, который выполняет пинг веб-ресурсов yandex.ru,
youtube.com и преобразовывает результат из байтовового типа данных
в строковый без ошибок для любой кодировки операционной системы.
"""
import platform
import subprocess

import chardet as chardet


def print_ping(*args):
    for process in args:
        for line in process.stdout:
            result = chardet.detect(line)
            print('result = ', result)
            line = line.decode(result['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


def ping_to_nodes(*args):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for node in args:
        arguments = ['ping', param, '3', node]
        procces = subprocess.Popen(args=arguments, stdout=subprocess.PIPE)
        print_ping(procces)


if __name__ == '__main__':
    ping_to_nodes('yandex.ru', 'youtube.com')
