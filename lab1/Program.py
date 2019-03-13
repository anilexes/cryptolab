import random
import json
import codecs
import pprint
import copy
import string
import operator

alphabet = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 
    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 
    'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я',
    ' ' 
]

pp = pprint.PrettyPrinter(indent=2)

CLOSE_CH = 0.02
# chastota = {
#     ' ': 0.175, 'о': 0.089, 'е': 0.072, 'а': 0.062,
#     'и': 0.062, 'т': 0.053, 'н': 0.053, 'с': 0.045,
#     'р': 0.040, 'в': 0.038, 'л': 0.035, 'к': 0.028,
#     'м': 0.026, 'д': 0.025, 'п': 0.023, 'у': 0.021,
#     'я': 0.018, 'ы': 0.016, 'з': 0.016, 'ь': 0.014,
#     'ъ': 0.014, 'б': 0.014, 'г': 0.013, 'ч': 0.012,
#     'й': 0.010, 'х': 0.009, 'ж': 0.007, 'ю': 0.006,
#     'ш': 0.006, 'ц': 0.004, 'щ': 0.003, 'э': 0.003,
#     'ф': 0.002, 'ё': 0.072
# }
chastota = {
  ' ': 0.175, 'о': 0.10983, 'е': 0.08483, 'ё': 0.08483,
  'а': 0.07998, 'и': 0.07367, 'т': 0.067,
  'н': 0.06318, 'с': 0.05473, 'р': 0.04746,
  'в': 0.04533, 'л': 0.04343, 'к': 0.03486,
  'м': 0.03203, 'д': 0.02977, 'п': 0.02804,
  'у': 0.02615, 'я': 0.02001, 'ы': 0.01898,
  'г': 0.01687, 'з': 0.01641, 'б': 0.01592,
  'ч': 0.0145, 'й': 0.01208, 'х': 0.00966,
  'ъ': 0.00037, 'ж': 0.0094, 'ш': 0.00718,
  'ь': 0.01735, 'ю': 0.00639, 'ц': 0.00486,
  'щ': 0.00361, 'э': 0.00331, 'ф': 0.00267,
  }
def pprint(v):
    pp.pprint(v)

def keys_sorted_by_value(d):
    return sorted(d, key=d.get, reverse=True)


def check_decryption(text, dic):
    words = text.split()
    found = 0
    for word in words:
        if word in dic:
            found += 1

    return found / len(words)

# Функция шифрования\расшифрования
def translate(text, translation):
    result = ""
    for letter in text:
        if letter in translation:
            result += translation[letter]
        else:
            result += letter

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
    ru_words = read_file("ru.dic").split() # Список русских слов
    
    # read encrypted text
    encrypted_text = read_file("Вариант 3.txt").lower()

    # count chastots in the text
    encrypted_ch = {}
    for letter in encrypted_text:
        if letter in alphabet:
            if letter in encrypted_ch:
                encrypted_ch[letter] += 1
            else:
                encrypted_ch[letter] = 0

    all = 0
    for v in encrypted_ch.values():
        all += v

    encrypted_ch = dict(
        map(lambda k: (k, round(encrypted_ch[k] / all, 4)), 
            encrypted_ch.keys())
    )

    # for each letter reassign using chastota
    sorted_chastota = keys_sorted_by_value(chastota)
    sorted_encrypt_ch = keys_sorted_by_value(encrypted_ch)
    result_str = ""
    found_translations = {}
    for letter in encrypted_text:
        if letter in sorted_encrypt_ch:
            indx = sorted_encrypt_ch.index(letter)
            new_letter = sorted_chastota[indx]
            found_translations[letter] = new_letter
            result_str += new_letter
        else:
            result_str += letter
    
    tr = {}
    for i, v in chastota.items():
        text_v = 0
        if i in encrypted_ch:
            text_v = encrypted_ch[i]

        tr[i] = {'real': v, 'text': text_v}

    close_chastota = {}
    for letter, ch in chastota.items():
        if list(chastota.values()).count(ch) > 1:
            if ch in close_chastota:
                close_chastota[ch].append(letter)
            else:
                close_chastota[ch] = [letter]

    break_cnt = 0
    print(encrypted_text)
    print(result_str)
    print(sorted(encrypted_ch.items(), key=operator.itemgetter(1)))
    print(sorted(chastota.items(), key=operator.itemgetter(1)))
    # basic replacement is done
    
    

    words = []
    translator = str.maketrans('','',string.punctuation)
    encrypted_text = translate(encrypted_text, {' ': '_'})
    print(encrypted_text)
    while True:
        print(found_translations)
        letter1 = input('first letter: ')
        letter2 = input('second letter: ')
        ft = copy.deepcopy(found_translations)
        ft[letter1] = letter2
        txt = translate(encrypted_text, {letter1: letter2.upper()})
        print(txt)
        fine = input("Fine?: ")
        if fine == 'y':
            found_translations[letter1] = letter2
            encrypted_text = txt

    for word in result_str.split():
        print("Уже удалось расшифровать:")
        pprint(found_translations)
        word = word.translate(translator)
        word = translate(word, found_translations)
        print(word)

        if check_decryption(word, ru_words) == 1:
            ans = input("Is word "+ word +" fine? (y/n) ")
            if ans != "n":
                words.append(word)
                continue
        replacements_possible = {}
        for letter in word:
            if letter in found_translations:
                continue

            letter_index = sorted_chastota.index(letter)

            before = []
            if letter_index != 0:
                before_index = letter_index - 1
                while before_index >= 0 and \
                abs(chastota[sorted_chastota[letter_index]] - chastota[sorted_chastota[before_index]]) < CLOSE_CH:
                    before.append(sorted_chastota[before_index])
                    before_index -= 1

            after = []
            if letter_index != len(sorted_chastota)-1:
                after_index = letter_index + 1
                while after_index < len(sorted_chastota) and \
                abs(chastota[sorted_chastota[letter_index]] - chastota[sorted_chastota[after_index]]) < CLOSE_CH:
                    after.append(sorted_chastota[after_index])
                    after_index += 1

            if before:
                if letter not in replacements_possible:
                    replacements_possible[letter] = []

                replacements_possible[letter] += before
            if after:
                if letter not in replacements_possible:
                    replacements_possible[letter] = []
                
                replacements_possible[letter] += after

            if letter in replacements_possible:
                replacements_possible[letter] = list(set(replacements_possible[letter]))
                replacements_possible[letter] = list(filter(lambda v: not v in found_translations.values(), 
                    replacements_possible[letter]))

        # {'a': ['b', 'g'], 't': ['o']} => [{'a':'b'}, {'a':'b', 't':'o'}, {'a': 'g', 't': 'o'}, {'t':'o'}]
        variants = []
        succeed_variants = []
        made = []
        for k in replacements_possible:
            for ks in replacements_possible[k]:
                local_variants = copy.deepcopy(variants)
                for variant in local_variants:
                    variant[k] = ks
                variants += local_variants
                variants = list(map(lambda a: dict(a),
                        list(set(list(
                            map(lambda a: tuple(sorted(a.items())), variants)
                        )))
                ))
                variants.append({k:ks})

        # Возможные замены
        pprint(replacements_possible)

        for variant in variants:
            maybe_good = translate(word, variant)
            if check_decryption(maybe_good, ru_words):
                succeed_variants.append([maybe_good, variant])

        if len(succeed_variants) != 1:
            if len(succeed_variants) == 0:
                print("Без вариантов, увеличьте CLOSE_CH="+str(CLOSE_CH)+" ...")
                words.append(word)
                continue
            for idx, succeed in enumerate(succeed_variants):
                print(str(idx)+": "+ succeed[0])
            v = input("Выберете ("+str(0)+"-"+str(len(succeed_variants))+"/else)? ")
            if v[0] == "e":
                your_result = input("Ваш вариант: ")
                if len(your_result) != len(word):
                    print("Длина строки должна быть та же.")
                for idx, letter in enumerate(word):
                    found_translations[letter] = your_result[idx]
                words.append(your_result)
                continue
        else:
            print(succeed_variants[0][0])
            your_result = input("Ваш вариант: ")
            if len(your_result) != len(word):
                print("Длина строки должна быть та же.")
            for idx, letter in enumerate(word):
                found_translations[letter] = your_result[idx]
            words.append(your_result)
            continue
        found_translations.update(succeed_variants[int(v)][1])
        words.append(word)

    print(result_str)
    print(words)
    # pprint(tr)
    # if words are not fully fount in dict, change some letters and go on
    # if % is less, reassign back, try another change
    # if % is more, remember and check if it's ok


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
