import imageio
import json
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


def mask2rle(img):
    '''
    img: numpy array, 1 - mask, 0 - background
    Returns run length as string formated
    '''
    pixels = img.T.flatten()
    pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 1
    runs[1::2] -= runs[::2][:len(runs[1::2])]
    return ' '.join(str(x) for x in runs)


folder_index = 6

image_folder = rf'X:\temp\mask_tiff'
file_names = os.listdir(image_folder)

encodings = {}

for image_file_name in file_names[:]:
    image_path = os.path.join(image_folder, image_file_name)

    img = imageio.imread(image_path)

    mask = np.array(img[:, :, 0])

    mask_2 = np.where(mask > 127, 1, 0)

    encoding_2 = mask2rle(mask_2)
    # encoding_2 = run_length_encoding(mask_2)
    encodings[image_file_name] = encoding_2

file = open(fr'{image_folder}\all.csv', 'w', newline='')

with file:
    # identifying header
    header = ['id', 'predicted']
    writer = csv.DictWriter(file, fieldnames=header)

    # writing data row-wise into the csv file
    writer.writeheader()
    for i in range(len(encodings)):
        writer.writerow({'id': file_names[i].split('.')[0],
                         'predicted': encodings[file_names[i]],
                         })
