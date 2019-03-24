# Задание 4
# Нужно устанвить numpy:
# > pip install numpy
import numpy as np
from lfsr import make_M_sequence

KEY_FILE = 'key.txt'

# Функция считывания файла в бинарном формате (как массив байтов)
def bytes_from_file(filename, chunksize=8192):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    # Даём обработать этот байт извне
                    yield b
            else:
                break

# Считываем начальную последовательность
with open(KEY_FILE, 'r') as key_file:
    starting = [int(x) for x in list(key_file.read())]

# Даём алгоритму выполниться
sequence, M = make_M_sequence(polinom=[4,1], starting=np.array(starting))

# Задаём действие
done = False
while not done:
	done = True
	action = input("Зашифровать или расшифровать (e/d)?")

	if action == 'e':
		file = 'text.txt'
		result_file = 'encoded.txt'
	elif action == 'd':
		file = 'encoded.txt'
		result_file = 'decoded.txt'
	else:
		print("Нужно ввести e или d")
		done = False

result = []

bn = 0
def get_byte(sequence):
    global bn
    if M < 8:
        sequence = (sequence * 4)[:8]        
    res = sequence[bn:bn+8]
    if len(res) < 8:
        bn = 8 - len(res)
        res = np.append(res,sequence[:bn])
    else:
        bn += 8
    return int(''.join([str(x) for x in res]), base=2)

# Зашифровка и расшифровка происходит ОДИНАКОВО
# Используем один и тот же алгоритм
for b in bytes_from_file(file):
	result.append(
            # Побайтовый xor с сгенерированной последовательностью - и есть шифрование
		np.bitwise_xor(get_byte(sequence), b)
	)
        
# Пишем результат в файл
with open(result_file, 'wb') as write_file:
	write_file.write(bytearray(result))
