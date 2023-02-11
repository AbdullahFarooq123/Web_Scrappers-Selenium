import math
import threading
import time
import requests


def get_phone_info(start, end):
    for i in range(start, end):
        npa = numbers[i][0:3]
        nxx = numbers[i][3:6]
        response = requests.get(f'http://www.telcodata.us/query/queryexchangevalid.html?npa={npa}&nxx={nxx}')
        data = response.text.split('\n')[:-1]
        dictionary_format = {}
        for entry in data:
            single_temp_entry = entry.split('=')
            dictionary_format[single_temp_entry[0]] = single_temp_entry[1]
        if dictionary_format['response'] == '200' and not (dictionary_format['valid'] == 'NO'):
            try:
                number_ = numbers[i].strip()
                carrier_type = get_type(dictionary_format['companytype'])
                carrier_name = dictionary_format['company']
                if 'UNKNOWN' not in carrier_type:
                    phone_details.append(number_ + '|' + carrier_type + '|' + carrier_name)
            except KeyError:
                print(dictionary_format['valid'])
                print(dictionary_format)
        time.sleep(1)


def get_type(code):
    wireless = ['PCS', 'WIRELESS', 'CLEC', 'IPES']
    landline = ['RBOC', 'ICO']
    if code in wireless:
        return 'WIRELESS'
    elif code in landline:
        return 'LANDLINE'
    else:
        return code


def write_to_file():
    index = 0
    with open('lookup_completed.txt', 'w') as delete:
        delete.write('')
        delete.close()
    while True:
        details_to_save = open('lookup_completed.txt', 'a')
        for index in range(index, len(phone_details)):
            details_to_save.write(phone_details[index] + "\n")
            index += 1
        details_to_save.close()
        running = False
        for thr in threads:
            if thr.is_alive():
                running = True
                break
        if not running:
            break
    print('Bot finished!')


numbers = []
threads = []
phone_details = []
with open('numbers.txt', 'r') as number_file:
    for number in number_file:
        numbers.append(number)
    number_file.close()
no_of_threads = (20 if len(numbers) > 20 else len(numbers))
no_of_inputs = math.floor(len(numbers) / no_of_threads)
for thread_no in range(no_of_threads):
    start = thread_no * no_of_inputs
    end = no_of_inputs * (thread_no + 1)
    if thread_no == no_of_threads - 1:
        end = len(numbers)
    t = threading.Thread(target=get_phone_info, name=str(thread_no), args=(
        start, end))
    threads.append(t)
    t.start()
threading.Thread(target=write_to_file).start()
print('Bot processing!')
print('You can view realtime progress in lookup_completed.txt')
