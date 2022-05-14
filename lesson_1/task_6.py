"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и
исходить из того, что перед нами файл в неизвестной кодировке.
Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того,
 в какой кодировке он был создан.
"""
import chardet


def write_to_file(*args, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for word in args:
            f.write(word + '\n')
    f.close()
    return True


def check_encoding(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    print(f'encoding = {chardet.detect(content)["encoding"]}')
    return chardet.detect(content)['encoding']


def read_from_file(filename, encoding='utf-8'):
    try:
        with open(filename, encoding=encoding) as f:
            for el in f:
                print(el, end='')
        return True
    except UnicodeDecodeError:
        return False, print(f'кодировка по умолчанию UTF-8 не подходит')


if __name__ == '__main__':
    filename = 'test_file.txt'
    write_to_file('сетевое программирование', 'сокет', 'декоратор', filename=filename)
    encoding = check_encoding(filename=filename)
    read_from_file(filename=filename, encoding=encoding)
    print('*' * 100)
    filename = 'output_test_file.txt'
    encoding = check_encoding(filename=filename)
    read_from_file(filename=filename)
    print('*' * 100)
    read_from_file(filename=filename, encoding=encoding)
    print('*' * 100)
