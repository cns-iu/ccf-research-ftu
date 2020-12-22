import cv2
import json
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from tifffile import imread, imwrite, TiffFile

json_filename = r'X:\hackathon_new\1\annotations\VAN0005-RK-4-172-PAS_registered.ome.json'

if len(sys.argv) >= 2:
    json_filename = sys.argv[1]

output_filename = json_filename

read_file = open(json_filename, "r")
data = json.load(read_file)

remove_dict = {}
with open('remove.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        if row[0] in remove_dict:
            remove_dict[row[0]].append(row[1])
        else:
            remove_dict[row[0]] = [row[1]]

filter_list = []
for key in remove_dict:
    if key in json_filename:
        filter_list = remove_dict[key]
        print(filter_list)
        print(f'{len(filter_list)} items to remove')

filtered_data = [data[i] for i in range(len(data)) if str(i) not in filter_list]

read_file.close()
a_file = open(output_filename, "w")
json.dump(filtered_data, a_file, indent=4)
a_file.close()
