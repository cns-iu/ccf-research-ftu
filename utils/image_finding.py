import os
import csv
import shutil

file_root_dir = r'C:\Users\bunny\Desktop\false_positive_sample'

img_list = []
img_full_path_list = []
for (dirpath, dirnames, filenames) in os.walk(os.path.join(file_root_dir, file_root_dir)):
    img_full_path_list += [os.path.join(dirpath, file) for file in filenames if (file.endswith('.jpg'))]
    img_list += [file for file in filenames if (file.endswith('.jpg'))]

# print(img_list)

manual_filter_list_file = 'tests/temp/image_disagreement_list.csv'

filter_list = []

with open(manual_filter_list_file, newline='') as inputfile:
    for row in csv.reader(inputfile):
        filter_list.append(row[-1])

# print(filter_list)

to_delete_list = []

for i in range(len(img_list)):
    if img_list[i].split('.')[0] not in filter_list:
        to_delete_list.append(img_full_path_list[i])

# print(to_delete_list)

for full_path in to_delete_list:
    os.remove(full_path)