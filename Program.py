import random
import json
import codecs

alphabet = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 
    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 
    'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
    ' ' 
]

# Функция шифрования\расшифрования
def translate(text, translation):
    result = ""
    for letter in text:
        if letter in translation:
            result += translation[letter]

    return result

# Считывание в кодировке windows1251
def read_file(filename):
    handle = codecs.open(filename, "r", "cp1251")
    data = handle.read() # считываем текст  в переменную data
    handle.close()
    return data

# Запись в кодировке windows1251
def write_file(filename, data):
    handle = codecs.open(filename, "w", "cp1251")
    handle.write(data)
    handle.close()

def zashifr(): # определяем функцию шифрования
    # Читаем данные из файла
    data = read_file("Текст.txt")

    data = data.lower() 
    shuffled = alphabet.copy() # создаем копию алфавита и ее перемешиваем
    while True:
        random.shuffle(shuffled)
        # Проверяем, что случайно не создали аналогичную последовательность
        if alphabet != shuffled:
            break

    translations = {} # создаем словарь

    # Создаём таблицу с трансляциями
    for i, letter in enumerate(alphabet):
        translations[letter] = shuffled[i]

    # Создаём файл для трансляций
    translations_json = json.dumps(translations, indent=4, ensure_ascii=False)
    write_file("translation.txt", translations_json)
    # Зашифровываем файл

    new_data = translate(data, translations)

    print(new_data)
    write_file("Зашифрованный.txt", new_data)
    
def rushifr(): # расшифровка
    data = read_file("Зашифрованный.txt")

    json_raw = read_file("translation.txt")
    translations = json.loads(json_raw)

    back_translations = dict((v,k) for k,v in translations.items()) # 
    old_data = translate(data, back_translations)

    print(old_data)
    
    write_file("Расшифрованный.txt", old_data)

# Взлом шифра текста "Вариант 3.txt"
def vzlom():
    pass

done = False
while not done:
    action = input("Зашифровать (z), расшифровать (r), взломать (v)? ")
    done = True
    if action == "r":
        rushifr()
    elif action == "z":
        zashifr()
    elif action == "v":
        vzlom()
    else:
        print("Не заданное действие, повторите ввод")
        done = False
