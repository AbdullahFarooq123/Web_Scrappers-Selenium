import json

with open('data.json', 'r') as file:
    data = json.load(file)
    print(len(data))
    # for d in data:
    #     if d['First Name'] is not None and d['Last Name'] is not None :
    #         print(d['First Name'])