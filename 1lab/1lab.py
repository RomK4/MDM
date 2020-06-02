import csv
import re
in_file = "data.csv"
out_file = "output.txt"
sms = 0
t_in = 0
t_out = 0
k1 = 2 
k2 = 4
sms_price = 1.5
number = "933156729"
# Читаем файл и получаем данные
with open(in_file, 'r') as read_file:
	#Переводим в словарь
	csv_reader = csv.DictReader(read_file)
	for line in csv_reader:
		#Ищем номер
		if (line['msisdn_origin']) == number:
			t_in += float(line['call_duration'])
			sms += int(line['sms_number'])
			#Находим время в строке и переводим в числовой тип
			time = re.search(r':(.*):', line['timestamp'])
			time = int(time.group(1))
			if time >30:
				t_in *= k2
			else:
				t_in *= k1

		if (line['msisdn_dest']) == number:
			t_out += float(line['call_duration'])
			time = re.search(r':(.*):', line['timestamp'])
			time = int(time.group(1))
			if time >30:
				t_out *= k2
			else:
				t_out *= k1

sms_price *= sms 
t_final = t_out + t_in
#Сохраняем в файл
with open(out_file, 'a') as save_file:
        save_file.write('Общая стоимость типа услуг "Телефония": '+ str(t_final) + '\nОбщая стоимость типа услуг "СМС": ' + str(sms_price))