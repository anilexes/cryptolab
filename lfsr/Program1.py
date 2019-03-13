# Задание 1
# ======================================
# необходимо установить пакет numpy
# > pip install numpy
# numpy позволяет производить работу с массивами данных быстрее, чем со списками python

import numpy as np
from math import ceil
from LFSR import LFSR

KEY_FILE = 'key.txt'

# Начальную последовательность можно считать
load = input("Считать изначальную последовательность (y/n)? ")

# Если ответим "нет", то будет генерироваться рандомно
initstate = []

if load == 'y':
	with open(KEY_FILE, 'r') as key_file:
		initstate = [int(x) for x in list(key_file.read())]

print(initstate)

# Создаём объект класса LFSR для полиндрома x^4 + x + 1
alg = LFSR(polinom=[4,1], initstate=np.array(initstate))

# Запускаем работу алгоритма (генериуем битовую последовательность)
alg.process()

# Получаем эту последовательность
sequence = alg.getMSequence()

# Выводим столько битов, сколько нужно пользователю
how_many = int(input("Сколько элементов вывести: "))
seqs = int(ceil( how_many / alg.expectedPeriod))
print((sequence * seqs)[:how_many])

# Начальную последовательность можно сохранить
save = input("Сохранить изначальную последовательность (y/n)? ")

# Сохраням в файл
if save == 'y':
	text = ''.join([str(x) for x in alg.initstate])
	with open(KEY_FILE, 'w') as key_file:
		key_file.write(text)
