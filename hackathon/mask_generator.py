import cv2
import json
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from tifffile import imread, imwrite, TiffFile

json_filename = r'X:/VAN0003-LK-33-2-PAS_FFPE_glom_annotations.json'
image_filename = r'X:/VAN0003-LK-33-2-PAS_FFPE.ome.tiff'

if len(sys.argv) >= 2:
    json_filename = sys.argv[1]
if len(sys.argv) >= 3:
    image_filename = sys.argv[2]

output_filename = json_filename.replace('json', 'tiff')

shift_dict = {
    # "VAN0003-LK-33-2": (1, 0, -6, 0, 1, -3),  # test
    "VAN0009-LK-102-7": (1, 0, -6, 0, 1, -3),
    "VAN0010-LK-155-40": (1, 0, -14, 0, 1, -5),
    "VAN0016-LK-202-89": (1, 0, -3, 0, 1, -3),
}

read_file = open(json_filename, "r")
data = json.load(read_file)

agreement_dict = {}
with open('agreement.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        if row[0] in agreement_dict:
            agreement_dict[row[0]].append(row[1])
        else:
            agreement_dict[row[0]] = []

image_data = imread(image_filename)
print("raw size: ", image_data.shape, "\tdata type: ", image_data.dtype)

polys = []
shift = np.asarray([0, 0])
for key in shift_dict:
    if key in json_filename:
        shift[0] = shift_dict[key][2] * 8
        shift[1] = shift_dict[key][5] * 8
filter_list = []

for key in agreement_dict:
    if key in json_filename:
        filter_list = agreement_dict[key]
        print(filter_list)

skip_count = 0
for index in range(data.__len__()):
    if str(index) in filter_list:
        skip_count += 1
        continue
    geom = np.array(data[index]['geometry']['coordinates'])
    shifted_geom = geom + shift
    polys.append(shifted_geom)

print(f'{skip_count} gloms skipped')

# the shape of the image, h * w
image_shape = []
if len(image_data.shape) == 3:
    image_shape = image_data.shape[:2]
if len(image_data.shape) == 5:
    image_shape = image_data.shape[3:]

mask_1 = np.zeros(image_shape)
for i in range(len(polys)):
    cv2.fillPoly(mask_1, polys[i], i + 1)

print("mask size: ", mask_1.shape, "\tdata type: ", mask_1.dtype)

imwrite(output_filename, mask_1.astype('uint16'), metadata={'axes': 'YXC',
                                                            # 'PhysicalSizeX': 0.5 * int(shrink_index),
                                                            # 'PhysicalSizeY': 0.5 * int(shrink_index),
                                                            # 'PhysicalSizeXUnit': 'um',
                                                            # 'PhysicalSizeYUnit': 'um',
                                                            },
        # resolution=((tif_tags['XResolution'][0] // unit_index // int(shrink_index), tif_tags['XResolution'][1]),
        #             (tif_tags['YResolution'][0] // unit_index // int(shrink_index), tif_tags['YResolution'][1])),
        imagej=True)
