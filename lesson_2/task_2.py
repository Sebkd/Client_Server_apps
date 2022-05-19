"""
2. Задание на закрепление знаний по модулю json. Есть файл orders
в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий
 его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров
 — товар (item), количество (quantity), цена (price), покупатель (buyer),
 дата (date). Функция должна предусматривать запись данных в виде словаря
 в файл orders.json. При записи данных указать величину отступа в 4
 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(*args, item, quantity, price, buyer, date):
    DICT_TO_JSON = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('ouput_task2.json', 'w', encoding='utf-8') as f_n:
        json.dump(DICT_TO_JSON, f_n, indent=4)


if __name__ == '__main__':
    ITEM = 'товар'
    QUANTITY = 120
    PRICE = 360
    BUYER = 'покупатель'
    DATA = '12.12.2022'
    write_order_to_json(item=ITEM, quantity=QUANTITY, price=PRICE, buyer=BUYER, date=DATA)
