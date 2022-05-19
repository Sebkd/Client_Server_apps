"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных
 данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список для
 хранения данных отчета — например, main_data — и поместить в него названия
столбцов отчета в виде списка: «Изготовитель системы», «Название ОС»,
 «Код продукта», «Тип системы». Значения для этих столбцов также оформить
 в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
 В этой функции реализовать получение данных через вызов функции get_data(),
 а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re
from pprint import pprint

from lesson_1.task_6 import check_encoding


def get_values(key, row):
    for r in row:
        search = re.findall(r'\w+', r)
        delete_list = []
        for el in search:
            if el in key:
                delete_list.append(el)
        for el in delete_list:
            search.remove(el)
        clear_val = ' '.join(search)
        return clear_val


def check_row(key, row):
    for r in row:
        if key in r:
            return True
        else:
            return False


def get_data(*args):
    original_key = ['Изготовитель системы',
                    'Название ОС',
                    'Код продукта',
                    'Тип системы']
    main_data = []
    main_data.append(original_key)
    print()
    for arg in args:
        encoding = check_encoding(arg)
        with open(arg, encoding=encoding) as file:
            file_reader = csv.reader(file)
            os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []
            for row in file_reader:
                for key in original_key:
                    if check_row(row=row, key=key):
                        found_value = get_values(row=row, key=key)
                        if key == original_key[0]:
                            os_prod_list.append(found_value)
                        elif key == original_key[1]:
                            os_name_list.append(found_value)
                        elif key == original_key[2]:
                            os_code_list.append(found_value)
                        else:
                            os_type_list.append(found_value)
                    else:
                        continue
            main_data.append([*os_prod_list, *os_name_list, *os_code_list, *os_type_list])
    return main_data


def write_to_csv(*args, input_files):
    files = [*input_files]
    DATA = get_data(*files)
    with open(*args, 'w', encoding='utf-8') as file:
        FILE_WRITER = csv.writer(file)
        FILE_WRITER.writerows(DATA)


if __name__ == '__main__':
    INPUT_FILES = ['info_1.txt',
                   'info_2.txt',
                   'info_3.txt', ]
    OUTPUT_FILE = 'output_task1.csv'
    write_to_csv('output_task1.csv', input_files=INPUT_FILES)
