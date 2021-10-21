"""
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.
Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);

b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;

c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml

# key_1 = ['val1', 'val2', 1]
# key_2 = 2
# key_3 = [{}]

data = {
    'key1': ['val1', 'val2', 1],
    'key2': 2,
    'key3': [
        {
            'key1': 'Слово',
            'key2': 'Дело',
            'key3': 'Пример'
        },
        {
            'key1': 'tree',
            'key2': 'door',
            'key3': 'world'
        },
    ]
}

with open('file.yaml', 'w', encoding='utf-8') as wr_file:
    yaml.dump(data, wr_file, default_flow_style=False, allow_unicode=True)

with open('file.yaml', encoding='utf-8') as r_file:
    read_data = yaml.load(r_file, Loader=yaml.FullLoader)

if read_data == data:
    print(True)
else:
    print(False)

print(read_data)
print(data)
