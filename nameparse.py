import re

testlist = [
    '\nAlekseev AP',
    '\nАлексеев А.П.'
    '\nАлексеев АП'
    '\nАлекеев АП.'
    '\nАле-ев А.П.'
    '\nАлексеев А.П'
    '\nАлексеевА.П.'
    '\nАрхитектура ИС'
    ]

def find_name(str_list):
    result = re.findall(r'\n[A-ZА-Я].+\s?[A-ZА-Я]\.?[A-ZА-Я]\.?',
                        ','.join(str_list))
    print(result)

find_name(testlist)
