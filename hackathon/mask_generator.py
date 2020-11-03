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

read_file = open(json_filename, "r")
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
    image_shape = image_data.shape[2:4]

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
