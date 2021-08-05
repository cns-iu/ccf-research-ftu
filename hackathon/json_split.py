import json
import sys

file_path = r'X:\temp\Annotations\json\CL_HandE_1234_B004_annotations.json'

if len(sys.argv) >= 2:
    file_path = sys.argv[1]

a_file = open(file_path, "r")
json_object = json.load(a_file)
a_file.close()

list_TL, list_TR, list_BL, list_BR = [], [], [], []
center_X, center_Y = 4704, 4536

for row in json_object:
    old_list = row["geometry"]["coordinates"]
    if old_list[0][0][0] < center_X and old_list[0][0][1] < center_Y:
        new_list = [[[coor[0], coor[1]] for coor in old_list[0]]]
        row["geometry"]["coordinates"] = new_list
        list_TL.append(row)
    if old_list[0][0][0] >= center_X and old_list[0][0][1] < center_Y:
        new_list = [[[coor[0] - center_X, coor[1]] for coor in old_list[0]]]
        row["geometry"]["coordinates"] = new_list
        list_TR.append(row)
    if old_list[0][0][0] < center_X and old_list[0][0][1] >= center_Y:
        new_list = [[[coor[0], coor[1] - center_Y] for coor in old_list[0]]]
        row["geometry"]["coordinates"] = new_list
        list_BL.append(row)
    if old_list[0][0][0] >= center_X and old_list[0][0][1] >= center_Y:
        new_list = [[[coor[0] - center_X, coor[1] - center_Y] for coor in old_list[0]]]
        row["geometry"]["coordinates"] = new_list
        list_BR.append(row)

assert (len(json_object) == len(list_TL) + len(list_TR) + len(list_BL) + len(list_BR))

for path, json_list in zip(["topleft", "topright", "bottomleft", "bottomright"], [list_TL, list_TR, list_BL, list_BR]):
    path_part = file_path.replace("annotations", path)
    a_file = open(path_part, "w")
    json.dump(json_list, a_file, indent=4)
    a_file.close()
