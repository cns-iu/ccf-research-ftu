import json
import sys

file_path = r'X:\VAN0013-LK-202-96-PAS_registered.ome.json'

if len(sys.argv) >= 2:
    file_path = sys.argv[1]

a_file = open(file_path, "r")
json_object = json.load(a_file)
a_file.close()

offset = [0, 0]  # + right down  - left up
index = 2

if len(sys.argv) >= 3:
    index = int(sys.argv[2])

for row in json_object:
    old_list = row["geometry"]["coordinates"]
    new_list = [[[(coor[0] + offset[0]) * index, (coor[1] + offset[1]) * index] for coor in old_list[0]]]
    row["geometry"]["coordinates"] = new_list

a_file = open(file_path, "w")
json.dump(json_object, a_file, indent=4)
a_file.close()
