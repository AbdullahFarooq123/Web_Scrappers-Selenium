import random

import pyautogui as auto
import time
import csv


time.sleep(10)
txt = open('animals.txt', 'r')
csv_spam = open('spam.csv', 'r')
#
# persons = ['Mian', 'Aqib', 'Chota Main']

for i in range(0, 4):
    for animal in txt:
        r = random.randint(0, 2)
        auto.write(f'You are {animal}')
        auto.press('Enter')
        time.sleep(1)
# auto.write(f'Regards "Anonymous"')
# auto.press('Enter')

with open('spam.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        auto.write(row[1])
        auto.press('Enter')
        time.sleep(1)
    print(csv_reader.line_num)
auto.write(f'Regards "Anonymous"')
auto.press('Enter')
