# 3
from lfsr import make_M_sequence 
from math import sqrt

N = 10000
polinom = [161,18]
ks = [1,2,8,9]

sequence, M, starting = make_M_sequence(polinom=polinom, N=N)

Sx = sequence.count("1") # считаем кол-во единиц и получаем сумму Sx

Sums = {} # вычисялем сумму произведении элементов исходной и смещен посл-ти для каждого k 
for k in ks:
    Sums[k] = 0 # начальное значение для суммы 0

    for i in range(N-k): # от 0 -15 (при условии, что N=16)
        Sums[k] += int(sequence[i]) * int(sequence[i+k]) # x(i)*y(i)

for k in ks:
    Sy = sequence[k:-k].count("1")
    R = float(N*Sums[k] - Sx*Sy) /  sqrt((N*Sx - Sx**2)*(N*Sy - Sy**2))
    E = 1.0/(N-1) + 2.0/(N-2)*sqrt(float(N*(N-3))/(N+1))
    print("k = "+str(k))
    print("|R| <= E"+ " " + str(abs(R) <= E))

    print(str(abs(R))+" <= "+str(E))

