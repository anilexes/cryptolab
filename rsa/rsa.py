# Программно реализовать процедуру генерации открытого и закрытого
# ключей заданной длины L (128, 256, 512). В качестве открытой
# экспоненты использовать одно из чисел Ферма (17, 257,
# 65537). Сформированные ключи сохранить в файлы: открытый – в файл
# public.txt, а закрытый – в файл private.txt.
import math
from random import randint

FERM_NUMBERS = [17, 257, 65537]

def get_prime(bit_len, exclude=[]):
    first = int('1' + ('0' * (bit_len - 1)), base=2)
    last = int('1' + ('1' * (bit_len - 1)), base=2)

    while True:
        num = randint(first, last)
        found=True
        if num in exclude:
            continue

        for x in range(2, int(math.sqrt(num) + 1)):
            if num % x == 0 and not num in exclude:
                found=False
                break

        if found:
            return num

        exclude.append(num)

def get_2_primes(L):
    bit_len = round(L/2)
    a = get_prime(bit_len)
    b = get_prime(bit_len, [a])
    return 13, 73

def get_e(n, euler):
    # e < n
    # НОД(euler, e) = 1
    e = list(filter(lambda x: x < n, FERM_NUMBERS))[0]
    return e

def get_d(e, euler):
    # e*d mod euler = 1
    d = 173
    return d

def rsa(L):
    p, q = get_2_primes(L)
    n = p*q
    euler = (p-1)*(q-1)
    e = get_e(n, euler)
    # e, n - открытый ключ
    d = get_d(e, euler)
    # d, n - закрытый ключ

    block_size = round(L / 4)
