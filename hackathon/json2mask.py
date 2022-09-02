import cv2
import json
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from tifffile import imread, imwrite, TiffFile
import codecs

json_filename = r'X:\temp\Annotations\json\CL_HandE_1234_B004_topleft.json'
image_filename = r'X:\temp\train\CL-HandE-1234-B004-topleft.tiff'

if len(sys.argv) >= 2:
    json_filename = sys.argv[1]
if len(sys.argv) >= 3:
    image_filename = sys.argv[2]

output_filename = json_filename.replace('.json', '.tiff')

read_file = codecs.open(json_filename, "r", 'utf-8-sig')
data = json.load(read_file)

image_data = imread(image_filename)
print("raw size: ", image_data.shape, "\tdata type: ", image_data.dtype)

polys = []

for index in range(data.__len__()):
    geom = np.array(data[index]['geometry']['coordinates'])
    polys.append(geom)

# the shape of the image, h * w
image_shape = []
if len(image_data.shape) == 3:
    image_shape = image_data.shape[:2]
if len(image_data.shape) == 5:
    image_shape = image_data.shape[3:]

mask_1 = np.zeros(image_shape)
for i in range(len(polys)):
    cv2.fillPoly(mask_1, np.int32(polys[i]), 255)

print("mask size: ", mask_1.shape, "\tdata type: ", mask_1.dtype)

imwrite(output_filename, mask_1.astype('uint8'), metadata={'axes': 'YXC',
                                                            # 'PhysicalSizeX': 0.5 * int(shrink_index),
                                                            # 'PhysicalSizeY': 0.5 * int(shrink_index),
                                                            # 'PhysicalSizeXUnit': 'um',
                                                            # 'PhysicalSizeYUnit': 'um',
                                                            },
        # resolution=((tif_tags['XResolution'][0] // unit_index // int(shrink_index), tif_tags['XResolution'][1]),
        #             (tif_tags['YResolution'][0] // unit_index // int(shrink_index), tif_tags['YResolution'][1])),
        imagej=False)
