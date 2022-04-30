import csv
import random
from random import gauss
from random import seed

from inputimeout import inputimeout, TimeoutOccurred


def generate_temp(number_sensor, init_temp, desidered_temp=0, ventil_force=0):
    # seed random number generator
    seed(random.random())
    temp = 0
    with open('data'+number_sensor+'.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["#", "Temp Actual", "Temp Desidered", "Ventil Force"])
        for i in range(1000):
            value = gauss(init_temp, 0.2)
            print(round(value, 2))
            try:
                while temp not in list(range(15, 30)):
                    temp = int(inputimeout(prompt='Set or modify the desidered temperature of the sensor name ' + str(number_sensor) + ' : ', timeout=3))
                    ventil_force = 0
                    desidered_temp = temp
            except TimeoutOccurred:
                temp = 0

            if 10 <= temp <= 30 and ventil_force == 0:
                print('Temperature set at: ', temp)
                while ventil_force not in list(range(1, 6)):
                    ventil_force = int(input('Set the ventilation strength - 1 (strong) 5 (low) - : '))
                temp = 0

            if ventil_force > 0:
                print('desidered_temp ', desidered_temp)
                print('value ', value)
                if i % ventil_force == 0 and round(desidered_temp, 0) > round(value, 0):
                    init_temp += 0.3
                elif i % ventil_force == 0 and round(desidered_temp, 0) < round(value, 0):
                    init_temp -= 0.3
                elif round(desidered_temp, 0) == round(value, 0):
                    ventil_force = 0

            writer.writerow([i, round(value, 2), desidered_temp, ventil_force])


num_sensor = input('Enter sensor name: \n')
init_temp = int(input('Enter initial temperature: \n'))
ventil_force = 0
desidered_temp = 0
try:
    while desidered_temp not in list(range(15, 30)):
        desidered_temp = int(inputimeout(prompt='Enter the desired temperature within 3 seconds: ', timeout=3))
except TimeoutOccurred:
    desidered_temp = 0

if 10 < desidered_temp < 30:
    print('Temperature set at: ', desidered_temp)
    while ventil_force not in list(range(1, 6)):
        ventil_force = int(input('Set the ventilation strength - 1 (strong) 5 (low) - : '))
else:
    desidered_temp = 0
    ventil_force = 0

generate_temp(number_sensor=num_sensor, init_temp=init_temp, desidered_temp=desidered_temp, ventil_force=ventil_force)
