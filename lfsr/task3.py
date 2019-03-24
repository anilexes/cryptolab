# 3
from lfsr import make_M_sequence 
from math import sqrt
N = 15
polinom = [13,1]
ks = [1,2,8,9]

sequence, M, starting = make_M_sequence(polinom=polinom, N=N)

Sx = sequence.count("1")


Sums = {}
for k in ks:
    Sums[k] = 0

    for i in range(N-1):
        b = i + k
        if b >= N:
            b = (i + k) % N
        Sums[k] += int(sequence[i]) * int(sequence[b])

for k in ks:
    R = float(N*Sums[k] - Sx*Sx) /  sqrt((N*Sx - Sx**2) * 2)
    E = 1.0/(N-1) + 2.0/(N-2)*sqrt(N*(N-3)/(N+1))
    print("k = "+str(k))
    print("|R| <= E"+ " " + str(abs(R) <= E))

    print(str(abs(R))+" <= "+str(E))

