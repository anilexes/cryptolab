# Задание 1
# ======================================
# необходимо установить пакет numpy
# > pip install numpy
# numpy позволяет производить работу с массивами данных быстрее, чем со списками python

from lfsr import make_M_sequence

START_FILE = 'start.txt'

# Начальную последовательность можно считать
r = input("Считать стартовую последовательность (y/n)? ")

# Если ответим "нет", то будет генерироваться рандомно
starting = []

if r == 'y':
	with open(START_FILE, 'r') as start_file:
		starting = [int(x) for x in list(start_file.read())]

num = int(input("Количество битов на вывод: "))
sequence, M, starting = make_M_sequence(polinom=[7,1], starting=starting, N=num)
# Вывод M
print("M="+str(M))
print(sequence)

# Начальную последовательность можно сохранить
save = input("Сохранить стартовую последовательность (y/n)? ")

# Сохраням в файл
if save == 'y':
	text = ''.join([str(x) for x in starting])
	with open(START_FILE, 'w') as start_file:
		start_file.write(text)
