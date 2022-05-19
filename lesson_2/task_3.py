"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт,
 автоматизирующий сохранение данных в файле YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу
 соответствует список, второму — целое число, третьему — вложенный словарь,
 где значение каждого ключа — это целое число с юникод-символом, отсутствующим
в кодировке ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
 При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
 а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают
 ли они с исходными.
"""
import yaml

if __name__ == '__main__':
    F_KEY = ['msg_1', 'msg_2', 'msg_3']
    S_KEY = 12
    T_KEY = {
        '€': 23,
        '£': 34,
    }
    DATA_TO_YAML = {
        'message': F_KEY,
        'numbers': S_KEY,
        'currency': T_KEY
    }

    with open('output_task3.yaml', 'w', encoding='utf-8') as f_n:
        yaml.dump(DATA_TO_YAML, f_n, default_flow_style=False, allow_unicode=True)

    with open('output_task3.yaml', encoding='utf-8') as f_n:
        F_N_CONTENT = yaml.load(f_n, Loader=yaml.FullLoader)
        print(F_N_CONTENT)
