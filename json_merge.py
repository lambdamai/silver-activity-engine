import json
from os import listdir

data = []

in_num = 562900

for f in listdir(f'out/{in_num}/'):
    data += json.loads(open(f'out/{in_num}/' + str(f), 'r', encoding='utf-8').read())
    
with open(f'out/{in_num}.json', 'w', encoding="utf-8") as out_file:
            out_file.write(json.dumps(data, indent=3, ensure_ascii=False))