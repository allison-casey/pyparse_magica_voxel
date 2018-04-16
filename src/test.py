import json

with open('example.json') as data:
    d = json.load(data)
    __import__('pprint').pprint(d, indent=4)
