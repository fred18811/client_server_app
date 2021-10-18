# Выполнить пинг веб-ресурсов yandex.ru, youtube.com
# и преобразовать результаты из байтовового в строковый тип на кириллице.

import subprocess
import chardet  # необходима предварительная инсталляция!

args1 = ['ping', '-c', '5', 'yandex.ru']
args2 = ['ping', '-c', '5', 'youtube.com']

ya_ping = subprocess.Popen(args1, stdout=subprocess.PIPE)
for line in ya_ping.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))

you_ping = subprocess.Popen(args2, stdout=subprocess.PIPE)
for line in you_ping.stdout:
    result = chardet.detect(line)
    line = line.decode(result['encoding']).encode('utf-8')
    print(line.decode('utf-8'))
