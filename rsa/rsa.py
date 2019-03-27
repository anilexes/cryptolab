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
print('Задание 1')
print('-'*20)

print()
print('Запись public.txt')

with open('public.txt', 'w') as public_f:
    print(e, n)
    public_f.write("{} {}".format(e,n))

print()
print('Запись private.txt')

with open('private.txt', 'w') as private_f:
    print(d, n)
    private_f.write("{} {}".format(d,n))

print()
print('Файлы public.txt и private.txt записаны')

# Задание 2
# Принимаем строку 16 символов
print()
print('Задание 2')
print('-'*20)
print()

string = 'this is a text 1'

print('Изначальный текст текст')
print(string)

encoded = []
for letter in string:
    ascii_value = ord(letter)
    encoded.append(pow(ascii_value, e, n))

print()
print('Зашифрованные данные')
print(encoded)

decoded = []
for enc_letter in encoded:
    decoded.append(pow(enc_letter, d, n))

print()
print('Расшифрованный текст')

for l in decoded:
    print(chr(l), end='')

print()
