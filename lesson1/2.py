# Каждое из слов «class», «function», «method» записать в байтовом типе
# без преобразования в последовательность кодов (не используя методы encode и decode)
# и определить тип, содержимое и длину соответствующих переменных.


WORD_1 = b'class'
WORD_2 = b'function'
WORD_3 = b'method'

print(f'WORD_1 {type(WORD_1)}, len = {len(WORD_1)}')
print(f'WORD_2 {type(WORD_2)}, len = {len(WORD_2)}')
print(f'WORD_3 {type(WORD_3)}, len = {len(WORD_3)}')
