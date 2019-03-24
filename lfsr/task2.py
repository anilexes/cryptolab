import numpy as np
from lfsr import make_M_sequence
from math import ceil

res, M = make_M_sequence(polinom=[7,1], starting=[])
combinations = []
k = 4
freedom = pow(2,k)
for i in reversed(range(freedom)):
	comb = "{0:b}".format(i)
	k = max(k, len(comb))
	comb = comb.zfill(k)
	combinations.append(comb)

N = int(ceil( M / k))
seq = (res * N)[:M]

print(k)
seria = []
seria_d = {}
for i in range(N):
	seria.append(seq[i*k:(i+1)*k])
	if not seria[i] in seria_d:
		seria_d[seria[i]] = 0
	else:
		seria_d[seria[i]] +=1
	print(seria[i])

Ne = {}
for s in combinations:
	if s not in seria_d:
		Ne[s] = 0
	else:
		Ne[s] = float(seria_d[s]) / pow(2, k)
	print("Ne["+s+"]: "+str(Ne[s]))

NT = N / pow(2,k)
print("NT: "+str(NT))

xi2 = 0
for i in combinations:
	xi2 += pow(abs(Ne[i] - NT),2) / NT

print("xi2: "+str(xi2))


