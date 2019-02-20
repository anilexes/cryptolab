import random
import json
import codecs

alphabet = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 
    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 
    'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
    ' ' 
]

def zashifr(): # определяем функцию encode
    # Читаем данные из файла
    handle = codecs.open("Текст.txt", "r", "cp1251")
    data = handle.read() # считываем текст  в переменную data
    handle.close()

    data = data.lower() 

    shuffled = alphabet.copy() # создаем копию алфавита и ее перемешиваем
    random.shuffle(shuffled)

    translations = {} # создаем словарь

    # Создаём таблицу с трансляциями
    for i, letter in enumerate(alphabet):
        translations[letter] = shuffled[i]

    # Создаём файл для трансляций
    translations_json = json.dumps(translations, indent=4, ensure_ascii=False)
    trans_handle = codecs.open("translation.txt", "w", "cp1251")
    trans_handle.write(translations_json)
    trans_handle.close()

    # Зашифровываем файл
    new_data = "" # новая пустая зашифрованная строка
    for letter in data: # data - текст, который нужно зашифровать. 
        if letter in translations:
            new_data += translations[letter]

    new_handle = codecs.open("Зашифрованный.txt", "w", "cp1251")
    new_handle.write(new_data)
    new_handle.close()

def rushifr(): # расшифровка
    handle = codecs.open("Зашифрованный.txt", "r", "cp1251")
    data = handle.read()
    handle.close()

    trans_handle = codecs.open("translation.txt", "r", "cp1251")
    translations = json.loads(trans_handle.read()) # переводим json в объект питона (питоновский словарь)
    trans_handle.close()

    back_translations = dict((v,k) for k,v in translations.items()) # 

    old_data = ""
    for letter in data:
        if letter in back_translations:
            old_data += back_translations[letter]

    old_handle = codecs.open("Расшифрованный.txt", "w", "cp1251")
    old_handle.write(old_data)
    old_handle.close()

action = input("Зашифровать (z) или расшифровать (r)? ")

if action == "r":
    zashifr()
else:
    rushifr()
