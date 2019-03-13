# Задание 4
# Нужно устанвить numpy:
# > pip install numpy
import numpy as np
from LFSR import LFSR

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
    initstate = [int(x) for x in list(key_file.read())]

# Используем дефолтный полином x^4 + x + 1
alg = LFSR(polinom=[4,1], initstate=np.array(initstate))

# Даём алгоритму выполниться
alg.process()
sequence = alg.getMSequence()

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

# Зашифровка и расшифровка происходит ОДИНАКОВО
# Используем один и тот же алгоритм
for b in bytes_from_file(file):
	result.append(
            # Побайтовый xor с сгенерированной последовательностью - и есть шифрование
		np.bitwise_xor(int(''.join([str(x) for x in alg.getByte()]), base=2), b)
	)
        
# Пишем результат в файл
with open(result_file, 'wb') as write_file:
	write_file.write(bytearray(result))
