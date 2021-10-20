# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).


WORD_1 = 'разработка'
WORD_2 = 'администрирование'
WORD_3 = 'protocol'

ENC_WORD_1 = WORD_1.encode('UTF-8')
print(type(ENC_WORD_1))
print(ENC_WORD_1)
DEC_WORD_1 = ENC_WORD_1.decode('UTF-8')
print(type(DEC_WORD_1))
print(DEC_WORD_1)
print('*' * 100)
print('\n')

ENC_WORD_2 = str.encode(WORD_2, encoding='utf-8')
print(type(ENC_WORD_2))
print(ENC_WORD_2)
DEC_WORD_2 = bytes.decode(ENC_WORD_2, encoding='UTF-8')
print(type(DEC_WORD_2))
print(DEC_WORD_2)
print('*' * 100)
print('\n')

ENC_WORD_3 = bytes(WORD_3, encoding='utf-8')
print(type(ENC_WORD_3))
print(ENC_WORD_3)
DEC_WORD_3 = str(ENC_WORD_3, encoding='UTF-8')
print(type(DEC_WORD_3))
print(DEC_WORD_3)
print('*' * 100)
print('\n')

ENC_WORD_4 = b'standard'
print(type(ENC_WORD_4))
print(ENC_WORD_4)
DEC_WORD_4 = str(ENC_WORD_4, encoding='UTF-8')
print(type(DEC_WORD_4))
print(DEC_WORD_4)
print('*' * 100)