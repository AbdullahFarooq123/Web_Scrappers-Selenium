import math
import random
import string

characters = list(string.digits)
codes = open('codes.txt', 'r')
service_code = input("Enter Country Code : ")
length = int(input('Enter remaining length of numbers : '))
no = int(input('Enter amount of numbers : '))
phones = open('phone.txt', 'w')
random.shuffle(characters)
area_codes = []
for code in codes:
    area_codes.append(code.strip())
codes.close()
for code in area_codes:
    for number in range(math.floor(no / len(area_codes))):
        phone = []
        for i in range(length):
            r = random.choice(characters)
            phone.append(r)
        random.shuffle(phone)
        phones.write(service_code + code.strip() + ''.join(phone) + '\n')
phones.close()
