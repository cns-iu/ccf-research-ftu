import json

file_path = r'X:\hackathon_new\1\annotations\VAN0012-RK-103-75-PAS_registered.ome.json'

a_file = open(file_path, "r")
json_object = json.load(a_file)
a_file.close()

offset = [-6, -6] # + right down  - left up

for row in json_object:
    old_list = row["geometry"]["coordinates"]
    new_list = [[[coor[0] + offset[0], coor[1] + offset[1]] for coor in old_list[0]]]
    row["geometry"]["coordinates"] = new_list

a_file = open(file_path, "w")
json.dump(json_object, a_file)
a_file.close()
