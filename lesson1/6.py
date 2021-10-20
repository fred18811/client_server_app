# Создать текстовый файл test_file.txt,
# заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
# Проверить кодировку файла по умолчанию.
# Принудительно открыть файл в формате Unicode и вывести его содержимое.
from chardet import UniversalDetector

# Проверяем кодировку файла по умолчанию
detector = UniversalDetector()
with open('test_file.txt', 'rb') as file:
    for line in file:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
print(detector.result['encoding'])

# Принудительное открытие файла в utf-16
try:
    with open('test_file.txt', encoding='utf-16') as file:
        for line in file:
            print(line, end='')
except UnicodeError as error:
    print(error)
