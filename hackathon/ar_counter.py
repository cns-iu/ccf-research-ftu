import json
import sys
import os
import csv

root_path = r'G:\HuBMAP\hackathon_new\5\ar_annotations'
if len(sys.argv) >= 2:
    root_path = sys.argv[1]
file_list = [os.path.join(root_path, f) for f in os.listdir(root_path) if os.path.isfile(os.path.join(root_path, f))]

all_region = ['inner medulla', 'outer medulla', 'medulla', 'outer stripe', 'cortex']

print('file_name', '\t', '\t'.join(all_region))

for file_path in file_list:
    region_dict = {}
    for reg_name in all_region:
        region_dict[reg_name] = 0
    read_file = open(file_path, "r")
    data = json.load(read_file)

    for region in data:
        # all_region.append(region['properties']['classification']['name'])
        if len(region['geometry']['coordinates'][0]) > 5:
            region_dict[region['properties']['classification']['name'].lower()] += 1
    # print(region['properties']['classification']['name'])
    # print(len(region['geometry']['coordinates'][0]))

    file_name = file_path.split('\\')[-1]
    # print(f'{file_name}\t{len(data)}')
    values = [str(v) for v in region_dict.values()]
    print(file_name, '\t', '\t'.join(values))

# print(set(all_region))
