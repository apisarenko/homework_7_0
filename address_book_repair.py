from pprint import pprint
import csv
import re
import itertools


with open("phonebook_raw.csv", encoding='utf8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


record_number = 0
while record_number < len(contacts_list):
    mystring = ','.join(contacts_list[record_number])
    lastname = r"^[\w]+"
    firstname = r"^([\w]+\D)([\w]+)"
    surname = r"^([\w]+)?(\W)?([\w]+)?(\W)?([\w]+)?((\,)+)"
    res_lastname = re.findall(lastname, mystring)
    res_firstname = re.findall(firstname, mystring)
    res_surname = re.findall(surname, mystring)
    contacts_list[record_number][0] = res_lastname[0]
    contacts_list[record_number][1] = res_firstname[0][1]
    contacts_list[record_number][2] = res_surname[0][4]
    record_number += 1


for item in contacts_list:
    pattern = re.compile('(\+7|8)?[\s]?\(?(\d{3})\)?[\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})((\,|\s)\(*(доб.)?)+(\d{4})*\)*')
    result = re.sub(pattern, r'+7(\2)\3-\4-\5 \8\9', item[5] + '  ')
    item[5] = result.strip()


lastname_list = []
empty_list = [[]]
for item in contacts_list:
    lastname_list.append(item[0])
    empty_list.append([])

out_dict = {}
out_dict = dict(zip(lastname_list, empty_list))

record_number = 0
for number_of_field in contacts_list:
    for key in out_dict.keys():
        if number_of_field[record_number] == key:
            out_dict[key].append(number_of_field)

for key in out_dict.keys():
        out_dict[key] = list(itertools.chain.from_iterable(out_dict[key]))

address_book_new = []
for value in out_dict.values():
    address_book_new.append(value)

for field in address_book_new:
    for i in range(6):
        if (field[i] == '') and (len(field) > 7):
            field[i] = field[i + 7]

for field in address_book_new:
    while len(field) != 7:
        field.pop()

pprint(address_book_new)


with open('phonebook.csv', 'w', encoding='utf8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(address_book_new)
