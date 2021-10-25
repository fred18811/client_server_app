"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
a. Создать функцию write_order_to_json(),
в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json


def write_order_to_json(file, item, quantity, price, buyer, date):
    param = 'orders'
    dict_data = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    try:
        with open(file, encoding='utf-8') as r_file:
            json_data = json.load(r_file)

        json_data[param].append(dict_data)
        with open(file, 'w', encoding='utf-8') as wr_file:
            json.dump(json_data, wr_file, indent=4)

    except FileNotFoundError:
        with open(file, 'w', encoding='utf-8') as wr_file:
            json.dump({param: [dict_data]}, wr_file, indent=4)

    except KeyError:
        json_data[param] = [dict_data]
        with open(file, 'w', encoding='utf-8') as wr_file:
            json.dump(json_data, wr_file, indent=4)


JSON_FILE = 'orders.json'

write_order_to_json(JSON_FILE, 'car', 4, 40000, 'Jhon', '24-10-2021')
write_order_to_json(JSON_FILE, 'bus', 2, 70000, 'Bill', '24-10-2020')
