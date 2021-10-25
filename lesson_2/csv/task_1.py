"""
1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt, info_3.txt
и формирующий новый «отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
 их открытие и считывание данных. В этой функции из считанных данных необходимо
 с помощью регулярных выражений извлечь значения параметров «Изготовитель системы»,
 «Название ОС», «Код продукта», «Тип системы».
 Значения каждого параметра поместить в соответствующий список.
 Должно получиться четыре списка — например, os_prod_list,
 os_name_list, os_code_list, os_type_list.
 В этой же функции создать главный список для хранения данных отчета — например,
 main_data — и поместить в него названия столбцов отчета в виде списка: «Изготовитель системы»,
 «Название ОС», «Код продукта», «Тип системы».
 Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

c. Проверить работу программы через вызов функции write_to_csv().
"""
from chardet.universaldetector import UniversalDetector
import pathlib
import csv


def encoding_file(file_path_name):
    ud = UniversalDetector()
    for row in open(file_path_name, 'rb'):
        ud.feed(row)
        if ud.done:
            break
    ud.close()
    return ud.result['encoding']


def get_data(files_list):
    params = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [params, os_prod_list, os_name_list, os_code_list, os_type_list]

    for file in files_list:
        with open(file, 'r', encoding=encoding_file(file)) as obj:
            for line in obj:
                for i in range(len(params)):
                    if not line.find(params[i]):
                        main_data[i + 1].append(line.split(':')[1].strip())
    return main_data


def write_to_csv(file_csv, data):
    with open(file_csv, 'w', encoding='utf-8') as file:
        fl_writer = csv.writer(file)
        for row in data:
            fl_writer.writerow(row)


LIST_FILES = [str(_) for _ in pathlib.Path('.').glob('info_*.txt')]  # Get list files
DATA_FILES = get_data(LIST_FILES)  # Get data from files
FILE_CSV = './file.csv'

write_to_csv(FILE_CSV, DATA_FILES)
