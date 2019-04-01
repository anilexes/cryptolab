# 1
from lfsr import make_M_sequence

START_FILE = 'start.txt'
POLINOM=[17,1]

r = input("Считать стартовую последовательность (да/нет)? ")

# Если ответим "нет", то будет генерироваться рандомно
starting = []

if r == 'да':
	with open(START_FILE, 'r') as start_file:
		data = start_file.read() # data - строка , которую считываем
		starting = [int(x) for x in data] # делаем из строки массив

num = int(input("Количество бит на вывод: "))
sequence, M, starting = make_M_sequence(POLINOM, starting=starting, N=num)
# Вывод M
print("M="+str(M))
print(sequence)

# Начальную последовательность можно сохранить
save = input("Сохранить стартовую последовательность (да/нет)? ")

# Сохраням в файл
if save == 'да':
	text = ''.join([str(x) for x in starting])
	with open(START_FILE, 'w') as start_file:
		start_file.write(text)
