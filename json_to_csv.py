import json
import csv

file_name = 563000

data =  json.loads(open(f'out/{file_name}.json', encoding='utf-8').read())
data2 = open(f'out/{file_name}.csv', 'w', encoding='utf-8')

csvwriter = csv.writer(data2)

count = 0

for item in data:
      if count == 0:
             header = item.keys()
             csvwriter.writerow(header)
             count += 1
      csvwriter.writerow(item.values())
data2.close()
