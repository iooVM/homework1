
print('-' * WINDOW_WIDTH)
choice3 = input(
    "изменить: n - (name) Имя, pn - (phone number) Номер телефона, с - (company) компанию, любая другая клавиша - оставить в покое :")
if choice3 == 'n':
    new_name = input("Введите ново имя ")
    # TODO:  Убрать этот страх в отдельные функции добавление, изменения
    rename_record = find_record[0]
    rename_record["name"] = new_name
    callbook_del(callbook_file_json, find_record[0])
    data = read_file_json(callbook_file_json)
    data.append(rename_record)
    write_file_json(callbook_file_json, data)
