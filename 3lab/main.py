#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from docx2pdf import convert
from docxtpl import DocxTemplate
import decimal

units = (
    u'ноль',

    (u'один', u'одна'),
    (u'два', u'две'),

    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

minus = u'минус'


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num2text(num, main_units=((u'', u'', u''), 'm')):
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip() # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def decimal2text(value, places=2,
                 int_units=((u'рубль', u'рубля', u'рублей'), 'm'),
                 exp_units=((u'копейка', u'копейки', u'копеек'), 'f')):
    value = decimal.Decimal(value)
    q = decimal.Decimal(10) ** -places

    integral, exp = str(value.quantize(q)).split('.')
    return u'{} {}'.format(
        num2text(int(integral), int_units),
        num2text(int(exp), exp_units))

f = open('data.txt', 'r')
data = f.readlines()
f.close()

doc = DocxTemplate("draft.docx")



context = {
	'bank': 'АО "Мелореан банк" Г. Санкт-Петербрг',
	'BIK': '043323410',
	'N1': '30101810200000000700',
	'N2': '40702810900000002453',
	'INN': '000513522',
	'KPP': '442203343',
	'dest': 'ООО"Гавриловка"',
	'Number': '76',
	'Day': '22',
	'Month': 'мая',
	'Year': '20',
	'Supplier': 'ООО"Гавриловка", ИНН 000513522, КПП 442203343, 104525, Санкт-Петербрг, пер. Авиаторов, дом №31, корпус 1, тел.:',
	'Customer': 'ООО Далее, ИНН 7734327378, КПП 772330001, 239361, Москва г, Петровская .ул, дом № 4',
	'Base': '№ 1112019 от 22.05.2020',
	'tbl_contents': [
		{
			'n': '1',
			'name': "Входящие и исходящие звони до 00:30",
			'tariff': '', 
			'amount': '{:,}'.format(float(data[0][(data[0].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' мин',
			'price': "4 руб/мин",
			'sum': '{:,}'.format(float(data[1][(data[1].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' руб.'
		},
		{
			'n': '2',
			'name': "Входящие и исходящие звони после 00:30",
			'tariff': '',
			'amount': '{:,}'.format(float(data[2][(data[2].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' мин',
			'price': "2 руб/мин",
			'sum': '{:,}'.format(float(data[3][(data[3].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' руб.'
		},
		{
			'n': '3',
			'name': "СМС",
			'tariff': '',
			'amount': '{:,}'.format(float(data[4][(data[4].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' СМС',
			'price': "1.5 руб/мин",
			'sum': '{:,}'.format(float(data[5][(data[5].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' руб.'
		},
		{
			'n': '4',
			'name': "Интернет",
			'tariff': '',
			'amount': '{:,}'.format(float(data[7][(data[7].rfind(':')+2):-4])).replace(',', ' ').replace('.', ',') + data[7][-4:],
			'price': "2руб/MB",
			'sum': '{:,}'.format(float(data[8][(data[8].rfind(':')+1):])).replace(',', ' ').replace('.', ',') + ' руб.'
		}
	],
	'Overall': str('{:,}'.format(float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):])).replace(',', ' ').replace('.', ',')) + ' руб.',
	'Bill': str('{:,}'.format(float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):])).replace(',', ' ').replace('.', ',')) + ' руб.',
	'NDS': str('{:,}'.format(float(toFixed(((float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):]))*0.2), 2))).replace(',', ' ').replace('.', ',')) + ' руб.',
	'Amount': "4",
	'Summ': str('{:,}'.format(float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):])).replace(',', ' ').replace('.', ',')),
	'BillWords': decimal2text(float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):]))[0].upper() + decimal2text(float(data[8][(data[8].rfind(':')+1):]) + float(data[5][(data[5].rfind(':')+1):]) + float(data[3][(data[3].rfind(':')+1):]) + float(data[1][(data[1].rfind(':')+1):]))[1:],
	'Director': 'Зайцев Р.П.',
	'Accounter': 'Зайцев Р.П.',
	
}
doc.render(context)
doc.save("generated_doc.docx")


convert('generated_doc.docx', 'generated_doc.pdf'),1243
