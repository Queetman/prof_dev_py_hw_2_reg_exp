# -*- coding: utf-8 -*-
"""RegEx.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pue7gpB9LksSO5weRIMsKl74B92MoauW
"""

from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

init_first_name = [row[0] for row in contacts_list] # получение данных в графах ФИО
init_second_name = [row[1] for row in contacts_list]
init_third_name = [row[2] for row in contacts_list]

first_name = []
second_name = []
third_name = []

# получение единой строки с ФИО и раскидывание по массивам с Ф, И и О.
for i in range(len(init_first_name)):
    full_name = init_first_name[i] +  ' ' + init_second_name[i]+ ' ' + init_third_name[i]

    full_name_arr =  full_name.split(' ')
    first_name.append(full_name_arr[0])
    second_name.append(full_name_arr[1])
    third_name.append(full_name_arr[2])

for i in range(len(first_name)):
    contacts_list[i][0] = first_name[i]
    contacts_list[i][1] = second_name[i]
    contacts_list[i][2] = third_name[i]

pprint (contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list)

contacts_list

phones = [row[5] for row in contacts_list]
phones

import re

new_phones =[]
add_num =[]
#замена шаблона
for i in range(len(phones)):
    # преобразование номеров
    data_num =re.sub(r'(\+7|8)?[-\s]*(\()?(\d{3})(\))?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})',
            r'+7(\3)\5-\6-\7',
            phones[i])
    # преобразование доп. номеров.
    data_num =re.sub(r'[(]*доб\. (\d{4})[)]*', r'доб.\1',data_num)
    new_phones.append(data_num)

print( new_phones)

for i in range(len(new_phones)):
    contacts_list[i][5] = new_phones[i]
pprint(contacts_list)

"""Объединить все дублирующиеся записи о человеке в одну. Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ)."""

# сначала будут описаны методы, затем решение на основании этих методов.

# добавление еще столбца содержащего строку с фамилией и именем
f_s_name = [] #  листа для получения фамилий и именд дубликатов

for i in range(len(contacts_list)):
  contacts_list[i].append(contacts_list[i][0]+ ' '+ contacts_list[i][1])
  f_s_name.append(contacts_list[i][0]+ ' '+ contacts_list[i][1])
pprint(f_s_name)

# метод возвращает list с  фамилией и именем одинаковых людей.
def get_duplicates_name(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)

# метод получает ряды из contacts_list с одинаковыми фамилиями и именами
def get_dupl_rows(lst,key):

  out =[]
  for i in range(len(lst)):
    if key == lst[i][len(lst[0])-1]:
      out.append(lst[i])
  return out

# метод соединяет строки с одинаковыми именами и фамилиями
def merge_data(lst):
  mer_dat = []
  for i in range(len(lst[0])):
    if lst[0][i] == lst[1][i]:
      mer_dat.append(lst[0][i])
    else:
      mer_dat.append(lst[0][i] + lst[1][i])
  return mer_dat

# метод удаляет дубликаты по ключу - фамилии и имени
def delete_row(key, lst):
  new_lst =[]
  for i in range(len(lst)):
    if key!= lst[i][len(lst[0])-1]:
      new_lst.append(lst[i])

  return new_lst

# метод удаляет последний толбец
def delete_last_column(lst):
  out =[]
  for i in range(len(lst)):
    for j in range(len(lst[0])-1):
      out.append(lst[i][j])
  return out

dupl_f_s_name = get_duplicates(f_s_name)
dupl_f_s_name

for dupl_name in dupl_f_s_name:
  dupl_rows = get_dupl_rows(contacts_list, dupl_name) # получение данных дублированных данных
  single_row = merge_data(dupl_rows) # смержживание
  contacts_list = delete_row(dupl_name, contacts_list) # удаление дубликатов
  contacts_list.append(single_row) # добавление смерженных данных

contacts_list = delete_last_column(contacts_list)

pprint(contacts_list)