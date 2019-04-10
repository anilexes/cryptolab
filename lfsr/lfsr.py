import numpy as np
from math import ceil

def make_M_sequence(polinom, starting=None, N=None): #starting - нач.посл-ть. N-размер посл-ти
    # Максимальный индекс
    st = int(np.max(polinom)) #степень
    # Проверка на начальную последовательность 
    if starting == None or not len(starting) or len(starting) < st:
        starting = np.random.randint(0,2,np.max(polinom))
    else:
        starting = np.array(starting) # приводим к типу np.array. для эффективности алгоритма
    print("starting: "+str(starting))   
    sequence = starting[-1] # списываем послед символ в новуб посл-ть
    M = pow(2, st) - 1 # M это кол-во неповторяющихся битов в посл-ти
   
    if not N:
        N = M
    print(M)
    for i in range(N): # range создает массив упорядоченных символов
        # [10, 5, 1]
        # bit = 1
        bit = starting[polinom[0]-1]# получаем индекс первого элемента для сложения по модулю 2
        for j in range(1, len(polinom)): # для оставшихся элементов складываем по модулю 2
            # j = 1, bit = xor(starting[4], 1)
            # j = 2, bit = xor(starting[0], bit)
            bit = np.logical_xor(starting[polinom[j]-1],bit)
        
        starting = np.roll(starting, 1) # смещение  1 вправо
        starting[0] = bit
        sequence = np.append(sequence, starting[-1])

    res = ''.join([str(x) for x in sequence]) # из массива в строку

    

    # Выводим столько, сколько задано в N
    nums = int(ceil( N / M))
    res = (res * nums)[:N] # ceil - округляет 

    return res, M, starting