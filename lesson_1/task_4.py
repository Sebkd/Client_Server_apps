"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить обратное
преобразование (используя методы encode и decode).
"""


def transformation(*args):
    for word in args:
        print(f'начальное слово \033[33m"{word}"\033[0m')
        byte_word = word.encode('utf-8')
        print(f'преобразованное в байтовое \033[35m{byte_word}\033[0m')
        word_from_byte = byte_word.decode('utf-8')
        print(f'обратное преобразование \033[36m{word_from_byte}\033[0m', '\n')


if __name__ == '__main__':
    transformation('разработка', 'администрирование', 'protocol', 'standard',)
