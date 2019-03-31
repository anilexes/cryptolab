import textwrap

WORD = 32
BLOCK = 512

def wide(bits):
    # Первый этап
    bits += '1'
    l = len(bits)
    additional = 448 - (l % BLOCK)
    bits += ('0' * additional)

    # Второй этап
    additional = '{0:b}'.format(l).rjust(64, '0') # двоичная запись справа налево
    first_add = additional[32:64] # начальные 32 бита
    second_add = additional[:32] # конечные 32 бита
    bits += (first_add + second_add)
    return bits

def F(a, b, c):
    return a & b | ~a & c

def G(a, b, c):
    return a & b | a & c | b & c

def H(a, b, c):
    return a ^ b ^ c

def r1(a, b, c, d, k, s, X):
    str_res = '{0:b}'.format(a + F(b, c, d) + X[k])
    return int(str_res[s:] + str_res[:s], base=2)

def r2(a, b, c, d, k, s, X):
    str_res = '{0:b}'.format(a + G(b, c, d) + X[k] + 0x5A827999)
    return int(str_res[s:] + str_res[:s], base=2)

def r3(a, b, c, d, k, s, X):
    str_res = '{0:b}'.format(a + H(b, c, d) + X[k] + 0x6ED9EBA1)
    return int(str_res[s:] + str_res[:s], base=2)

def md4(bits):
    string = wide(bits)

    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476


    # Разбиваем текст на блоки 512 бит
    chunks = textwrap.fill(string, BLOCK).split()

    for chunk in chunks:
        X = textwrap.fill(chunk, WORD).split()
        X = list(map(lambda x: int(x, base=2), X))

        AA = A
        BB = B
        CC = C
        DD = D

        # 1 раунд
        A = r1( A, B, C, D, 0,  3,  X)
        A = r1( A, B, C, D, 4,  3,  X)
        A = r1( A, B, C, D, 8,  3,  X)
        A = r1( A, B, C, D, 12, 3,  X)
        D = r1( D, A, B, C, 1,  7,  X)
        D = r1( D, A, B, C, 5,  7,  X)
        D = r1( D, A, B, C, 9,  7,  X)
        D = r1( D, A, B, C, 13, 7,  X)
        C = r1( C, D, A, B, 2,  11, X)
        C = r1( C, D, A, B, 6,  11, X)
        C = r1( C, D, A, B, 10, 11, X)
        C = r1( C, D, A, B, 14, 11, X)
        B = r1( B, C, D, A, 3,  19, X)
        B = r1( B, C, D, A, 7,  19, X)
        B = r1( B, C, D, A, 11, 19, X)
        B = r1( B, C, D, A, 15, 19, X)

        # 2 раунд
        A = r2( A, B, C, D, 0,  3,  X)
        A = r2( A, B, C, D, 1,  3,  X)
        A = r2( A, B, C, D, 2,  3,  X)
        A = r2( A, B, C, D, 3,  3,  X)
        D = r2( D, A, B, C, 4,  5,  X)
        D = r2( D, A, B, C, 5,  5,  X)
        D = r2( D, A, B, C, 6,  5,  X)
        D = r2( D, A, B, C, 7,  5,  X)
        C = r2( C, D, A, B, 8,  9,  X)
        C = r2( C, D, A, B, 9,  9,  X)
        C = r2( C, D, A, B, 10, 9,  X)
        C = r2( C, D, A, B, 11, 9,  X)
        B = r2( B, C, D, A, 12, 13, X)
        B = r2( B, C, D, A, 13, 13, X)
        B = r2( B, C, D, A, 14, 13, X)
        B = r2( B, C, D, A, 15, 13, X)

        # 3 раунд
        A = r3( A, B, C, D, 0,  3,  X)
        A = r3( A, B, C, D, 2,  3,  X)
        A = r3( A, B, C, D, 1,  3,  X)
        A = r3( A, B, C, D, 3,  3,  X)
        D = r3( D, A, B, C, 8,  9,  X)
        D = r3( D, A, B, C, 10, 9,  X)
        D = r3( D, A, B, C, 9,  9,  X)
        D = r3( D, A, B, C, 11, 9,  X)
        C = r3( C, D, A, B, 4,  11, X)
        C = r3( C, D, A, B, 6,  11, X)
        C = r3( C, D, A, B, 5,  11, X)
        C = r3( C, D, A, B, 7,  11, X)
        B = r3( B, C, D, A, 12, 15, X)
        B = r3( B, C, D, A, 14, 15, X)
        B = r3( B, C, D, A, 13, 15, X)
        B = r3( B, C, D, A, 15, 15, X)

        A = A + AA
        B = B + BB
        C = C + CC
        D = D + DD

    print('{0:x}{1:x}{2:x}{3:x}'.format(A, B, C, D))

def str_to_bin(string):
    return ''.join(['{0:b}'.format(ord(x)) for x in string])

a = str_to_bin('abc')
b = a
b = '0'+b[1:]
a = '1'+a[1:]
md4(a)
md4(b)
