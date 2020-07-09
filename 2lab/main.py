import os
import matplotlib.pyplot as plt
import numpy as np

FILENAME = 'nfcapd.202002251200'
IP = '87.245.198.147'

getdata = os.popen('nfdump -o "fmt:%te|%sa|%da|%byt" -r '+FILENAME).readlines()
timeArr = []
bytesArr = []
resultBytes = 0
a = ''
price = 0
k2 = 2


def lineplot(x_data, y_data, x_label="", y_label="", title=""):
    _, ax = plt.subplots()

    ax.plot(x_data, y_data, lw = 1, color = '#539caf', alpha = 1)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.savefig('chart')

currentTime = '0'
currentBytes = 0

for line in getdata:
	if (IP in line):
		s = line[(line.rfind('|')+1):]
		b = 0
		if ('M' in s):
			b = int(float(s[:-3])*1000000)
		else:
			b = int(s)
		if (currentTime != line[:(line.find('|'))]):
			timeArr.append(line[:(line.find('|'))])
			bytesArr.append(currentBytes)
			currentBytes = 0
			currentTime = line[:(line.find('|'))]
		else:
			currentBytes += b
		resultBytes += b
			
if (resultBytes/1000000 < 500):
	resultBytes /= 1000
	a = 'KB'
else:
	resultBytes	/= 1000000
	a = 'MB'
price = k2*resultBytes


output = open('output.txt', 'w')
output.write('Пользователь: ' + IP + '\nВсего использовано: ' + str(resultBytes) + ' ' + a + '\nИтого: ' + str(price) + ' руб')
output.close()
lineplot(timeArr, bytesArr, "Time", "Bytes")
