import numpy as np

def make_M_sequence(polinom, starting, N=None):
    if not len(starting) and not 1 in starting:
        starting = np.random.randint(0,2,np.max(polinom))
    else:
        starting = np.array(starting)

    sequence = starting[-1]
    polinom.sort(reverse=True)
    st = polinom[0]
    M = pow(2, st) - 1
    if N == None:
        N = M

    for i in range(M):
        b = starting[polinom[0]-1]
        for i in range(1, len(polinom)):
            b = np.logical_xor(starting[polinom[i]-1],b)
        
        starting = np.roll(starting, 1)
        starting[0] = b
        sequence = np.append(sequence, starting[-1])

    return ''.join([str(int(x)) for x in sequence]), M