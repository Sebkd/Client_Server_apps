"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе. Важно: решение должно быть универсальным,
т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""


def create_bytes(*args):
    for word in args:
        try:
            byte_word = eval(f"b'{word}'")
            print(f'слово "{word}" возможно записать в байтовом типе')
            print(type(byte_word)), print(byte_word), print(len(byte_word), '\n')
        except SyntaxError:
            print(f'слово "{word}" невозможно записать в байтовом типе\n')


if __name__ == '__main__':
    create_bytes('attribute', 'класс', 'функция', 'type', )
