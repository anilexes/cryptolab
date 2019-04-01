# 4
import numpy as np
from lfsr import make_M_sequence

START_FILE = 'start.txt'
POLINOM = [7,1]
# Считываем начальную последовательность
with open(START_FILE, 'r') as start_file:
    data = start_file.read()
    starting = [int(x) for x in data]

# Даём алгоритму выполниться
sequence, M, starting = make_M_sequence(POLINOM, starting=starting)

# Задаём действие
action = input("Зашифровать или расшифровать (e/d)?")

if action == 'e':
	file = 'text.txt'
	result_file = 'encoded.txt'
else:
	file = 'encoded.txt'
	result_file = 'decoded.txt'

result = [] # массив байт

bn = 0 # индекс бита в послед-ти
def get_byte_from_sequence(sequence):
    global bn # наследуемый индекс бита    
    res = sequence[bn:bn+8]
    if len(res) < 8:
        bn = 8 - len(res)
        res = np.append(res,sequence[:bn])
    else:
        bn += 8
    return int(''.join([str(x) for x in res]), base=2) # приводим 10ти ричную записать байтов в двоичную

# Функция считывания файла в бинарном формате (как массив байтов)
# считываем байти из файла
def get_byte_from_file(filename):
    bufsize = 1024
    with open(filename, "rb") as f:
        while True:
            buffer = f.read(bufsize) # считываем в буфер 1024 байта
            if buffer:
                for byte in buffer:
                    yield byte  # отдаём в цикл
            else:
                break

# Зашифровка и расшифровка происходит ОДИНАКОВО
# Используем один и тот же алгоритм
for byte in get_byte_from_file(file):
	result.append(
         # Побайтовый xor с сгенерированной последовательностью - и есть шифрование
		np.bitwise_xor(
            get_byte_from_sequence(sequence), 
            byte
        )
	)
        
# Пишем результат в файл
with open(result_file, 'wb') as write_file:
	write_file.write(bytearray(result))
