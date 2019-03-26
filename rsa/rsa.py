# Программно реализовать процедуру генерации открытого и закрытого
# ключей заданной длины L (128, 256, 512). В качестве открытой
# экспоненты использовать одно из чисел Ферма (17, 257,
# 65537). Сформированные ключи сохранить в файлы: открытый – в файл
# public.txt, а закрытый – в файл private.txt.

import math
import sympy
from random import randint, choice

FERM_NUMBERS = [17, 257, 65537]

# Простое число с bit_len значащими битами в двоичной записи
# exclude - массив чисел, которые исключаются
def get_prime(bit_len, exclude=[]):
    first = int('1' + ('0' * (bit_len - 1)), base=2)
    last = int('1' + ('1' * (bit_len - 1)), base=2)

    while True:
        num = randint(first, last)
        found=True
        if num in exclude:
            continue

        if sympy.isprime(num) and not num in exclude:
            return num

        exclude.append(num)

# Два случайных простых числа с L/2 значащими битами
def get_2_primes(L):
    bit_len = round(L/2)
    a = get_prime(bit_len)
    b = get_prime(bit_len, [a])
    return a, b

# Параметр E
def get_e(n, euler):
    # e < n
    # НОД(euler, e) = 1
    less_than_n = list(filter(lambda x: x < n, FERM_NUMBERS))

    return choice(less_than_n)

# Параметр D
def get_d(e, euler):
    # e*d mod euler = 1
    a = e
    b = euler
    u1 = 1
    v2 = 1
    u2 = 0
    v1 = 0
    while b != 0:
        q = a // b
        r = a % b
        a = b
        b = r
        r = u2
        u2 = u1 - q*u2
        u1 = r
        r = v2
        v2 = v1 - q*v2
        v1 = r
    d = u1
    if d < 0:
        d += euler
    return d

# Алгоритм RSA
def rsa_keys(L):
    p, q = get_2_primes(L)
    n = p*q
    euler = (p-1)*(q-1)
    e = get_e(n, euler)
    # e, n - открытый ключ
    d = get_d(e, euler)
    # d, n - закрытый ключ

    return (e, n), (d, n)



(e, n), (d, n) = rsa_keys(L=128)

# Задание 1
with open('public.txt', 'w') as public_f:
    print(e, n)
    public_f.write("{} {}".format(e,n))

with open('private.txt', 'w') as private_f:
    print(d, n)
    private_f.write("{} {}".format(d,n))

# Задание 2
# Принимаем строку 16 символов
def fast_power(base, power):
    """
    Returns the result of a^b i.e. a**b
    We assume that a >= 1 and b >= 0

    Remember two things!
     - Divide power by 2 and multiply base to itself (if the power is even)
     - Decrement power by 1 to make it even and then follow the first step
    """

    result = 1
    while power > 0:
        # If power is even
        if power % 2 == 0:
            # Divide the power by 2
            power = power / 2
            # Multiply base to itself
            base = base * base
        else:
            # Decrement the power by 1 and make it even
            power = power - 1
            # Take care of the extra value that we took out
            # We will store it directly in result
            result = result * base

            # Now power is even, so we can follow our previous procedure
            power = power / 2
            base = base * base

    return result



string = '0123456789abcdef'

encoded = []
for letter in string:
    ascii_value = ord(letter)
    encoded.append(pow(ascii_value, e, n))

decoded = []
for enc_letter in encoded:
    decoded.append(pow(enc_letter, d, n))

print(encoded)
for l in decoded:
    print(chr(l), end='')

print()
