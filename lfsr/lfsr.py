import numpy as np
from math import ceil

def make_M_sequence(polinom, starting=None, N=None):
    # Максимальный индекс
    st = np.max(polinom)
    # Проверка на начальную последовательность 
    if starting == None or not len(starting) or len(starting) < st:
        starting = np.random.randint(0,2,np.max(polinom))
    else:
        starting = np.array(starting)
    print(starting)
    sequence = starting[-1]
    polinom.sort(reverse=True)
    M = pow(2, st) - 1 # M это кол-во неповторяющихся последоате-ей(размер посл-ти, которая без повторов)
   
    if not N:
        N = M

    for i in range(M):
        b = starting[polinom[0]-1]# получаем индекс первого элемента для сложения по модулю 2
        for j in range(1, len(polinom)): # для оставшихся элементов складываем по модулю 2
            b = np.logical_xor(starting[polinom[j]-1],b)
        
        starting = np.roll(starting, 1) 
        starting[0] = b
        sequence = np.append(sequence, starting[-1])

    res = ''.join([str(int(x)) for x in sequence])

    # Выводим столько, сколько задано в N
    nums = int(ceil( N / M))
    res = (res * nums)[:N]

    return res, M, starting