"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе.
Сделать это необходимо в автоматическом, а не ручном режиме,
с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes)
и определить тип, содержимое и длину соответствующих переменных.
"""


def create_bytes(*args):
    for word in args:
        byte_word = eval(f"b'{word}'")
        print(type(byte_word)), print(byte_word), print(len(byte_word), '\n')


if __name__ == '__main__':
    create_bytes('class', 'function', 'method')
