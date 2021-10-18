# Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.


WORD_1 = b'attribute'
WORD_4 = b'type'
WORD_2 = b'класс'
WORD_3 = b'функция'

# Строки с киррилицей не возможно записать в байтовом типе
# иначе выскакиват ошибка SyntaxError: bytes can only contain ASCII literal characters.
