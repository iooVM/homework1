# для генерации телефонного справочника
from faker import Faker
# для работы с json
import json
# для проверки существует ли файл
import os
# для рисования красивой таблички
import pandas as pd
# Для глубокого копирования словаря
import copy


# ----------------------------------------------------------------------------------------

# Глобальные переменные

# ширина окна
WINDOW_WIDTH = 180

# тестовая запись
testdata = [
    {
        'name': 'Кирилл Панфилов',
        'phone_number': '89094512021',
        'company': 'Препод с ирокезом из OTUS',
    }
]

# Файл телефонного справочника json
callbook_file_json = 'callbook.json'


# ----------------------------------------------------------------------------------------
# 1. раздел функций получения данных


# Чтение из json файла
def read_file_json(filename: str) -> list:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return []


# запись в json файла, добавление нет, только перезаписать файл
def write_file_json(filename: str, write_text: list):
    with open(filename, 'w', encoding='UTF-8') as json_file:
        # Сортируем список словарей по имени
        write_text = sorted(write_text, key=lambda x: x["name"])
        json.dump(write_text, json_file, ensure_ascii=False, indent=4)


# очистить содержимое файла
def clear_file_json(filename: str):
    with open(filename, 'w', encoding='UTF-8') as json_file:
        json.dump([], json_file, ensure_ascii=False, indent=4)


# конец раздел функций получения данных
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# 2. функции обработки данных


# Случайная Генерация контакта
def generate_fake_user() -> dict:
    fake = Faker('ru_RU')

    return {
        'name': fake.name(),
        'phone_number': fake.phone_number(),
        'company': fake.company(),
    }


def callbook_clear(filename: str):
    clear_file_json(filename)


# найти контакт

def callbook_find(filename: str, search_area: str) -> list:
    data = read_file_json(filename)
    if search_area.lower() == 'p':
        callbook_show_all(callbook_file_json)

    elif search_area.lower() == 'n':
        find_name = input("Кого искать ? :  ")
        record = [person for person in data if find_name in person["name"]]
        return record

    elif search_area.lower() == 'pn':
        find_name = input("Какой номер искать ? :  ")
        record = [person for person in data if find_name in person["phone_number"]]
        return record

    elif search_area.lower() == 'c':
        find_name = input("Какую компанию искать ? :  ")
        record = [person for person in data if find_name in person["company"]]
        return record


# удалить контакт
def callbook_del(filename: str, del_record: dict):
    data = read_file_json(filename)
    data.remove(del_record)
    write_file_json(filename, data)


# конец функции обработки данных
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# 3. интерфейсы общения с пользователем ( console, GUI, WEB и т.п.)

# прочитать справочник
def callbook_show_all(filename: str):
    data = read_file_json(filename)
    df = pd.DataFrame(data)
    print('-' * WINDOW_WIDTH)
    print(df.to_string(index=False, header=True, justify='center', col_space=40))
    print('-' * WINDOW_WIDTH)


# меню поиска контакта

def callbook_find_menu(filename: str) -> list:
    # data = read_file_json(filename)
    print("'n'   - (name) Искать по имени ")
    print("'pn'  - (phone number) Искать по номеру телефона  ")
    print("'c'   - (company) Искать по копании  ")
    choice = input("Что делаем ? :  ")
    return callbook_find(filename, choice)


# добавить в справочник

def callbook_add(filename: str):
    data = read_file_json(filename)
    choice = ''
    while choice != 'e':
        # Ввод данных от пользователя
        print('-' * WINDOW_WIDTH)
        print("'g'  - (generate) Сгенерировать случайно")
        print("'a'  - (add) Ввести в ручную  ")
        print("'w'  - (write) Сохранить")
        print("'we' - (write and exit) Сохранить и выйти ")
        print("'e'  - (exit) Выход без сохранения ")
        print("'p'  - (print) Показать все контакты ")

        choice = input("Что делаем ? :  ")
        if choice.lower() == 'we':
            write_file_json(filename, data)
            break
        elif choice.lower() == 'w':
            write_file_json(filename, data)

        elif choice.lower() == 'g':
            record = generate_fake_user()
            data.append(record)
            print(f"Запись сгенерирована : {list(map(lambda x: x, record.values()))}")
            # print(record)

        elif choice.lower() == 'p':
            callbook_show_all(callbook_file_json)

        elif choice.lower() == 'a':
            name = input("Введите имя  : ")
            phone_number = input("Введите номер телефона : ")
            company = input("Введите компанию: ")

            # Создание новой записи
            record = {
                'name': name,
                'phone_number': phone_number,
                'company': company,
            }

            # Добавление записи в список
            data.append(record)
            print(f"Новая запись: {list(map(lambda x: x, record.values()))}")


# Основное меню

def menu():
    choice = ''
    while choice != 'e':
        # Ввод данных от пользователя
        print('-' * WINDOW_WIDTH)
        print('e - (exit) Выход')
        print('p - (print) Показать все контакты')
        print('a - (add) Добавить новую запись')
        print('c - (clear) Очистить справочника')
        print('f - (find) Поиск по справочнику, удалить или изменить запись ')

        choice = input("Что делаем ? : ")
        print('-' * WINDOW_WIDTH)

        if choice == 'p':
            callbook_show_all(callbook_file_json)

        elif choice == 'a':
            callbook_add(callbook_file_json)

        elif choice == 'c':
            callbook_clear(callbook_file_json)
        elif choice == 'f':
            find_record = callbook_find_menu(callbook_file_json)
            print('-' * WINDOW_WIDTH)
            print(f'найдено {find_record}')
            choice2 = input("d - (del) удалить, m - (modify), любая другая клавиша - оставить в покое : ")
            if choice2 == 'd':
                callbook_del(callbook_file_json, find_record[0])
                print('Запись удалена ')
            elif choice2 == 'm':
                print('-' * WINDOW_WIDTH)
                print(' Что изменить ? :')
                print(" 'n' - (name) Имя")
                print(" 'pn' - (phone number) Номер телефона")
                print(" 'с' - (company) компанию")
                print(" любая другая клавиша - оставить в покое")
                choice3 = input(' :')
                if choice3 == 'n':
                    new_name = input("Введите новое имя ")
                    rename_record = copy.deepcopy(find_record[0])
                    rename_record['name'] = new_name
                    print(f'Выглядит так {rename_record}. перезаписать (y - yes) ')
                    choice4 = input(' :')
                    if choice4 == 'y':
                        callbook_del(callbook_file_json, find_record[0])
                        data = read_file_json(callbook_file_json)
                        data.append(rename_record)
                        write_file_json(callbook_file_json, data)

                elif choice3 == 'pn':
                    new_name = input("введите новый номер телефона ")
                    rename_record = copy.deepcopy(find_record[0])
                    rename_record['phone_number'] = new_name
                    print(f'Выглядит так {rename_record}. перезаписать (y - yes) ')
                    choice4 = input(' :')
                    if choice4 == 'y':
                        callbook_del(callbook_file_json, find_record[0])
                        data = read_file_json(callbook_file_json)
                        data.append(rename_record)
                        write_file_json(callbook_file_json, data)

                elif choice3 == 'c':
                    new_name = input("Введите новую компанию ")
                    rename_record = copy.deepcopy(find_record[0])
                    rename_record['company'] = new_name
                    print(f'Выглядит так {rename_record}. перезаписать (y - yes) ')
                    choice4 = input(' :')
                    if choice4 == 'y':
                        callbook_del(callbook_file_json, find_record[0])
                        data = read_file_json(callbook_file_json)
                        data.append(rename_record)
                        write_file_json(callbook_file_json, data)


# ____________________________________________________________________________________________________
# Вызов
if __name__ == '__main__':
    print('Добро пожаловать!!!')
    menu()
