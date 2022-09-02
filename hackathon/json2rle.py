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
    # pixels = np.concatenate([[0], pixels, [0]])
    runs = np.where(pixels[1:] != pixels[:-1])[0] # + 1
    runs[1::2] -= runs[::2]
    return ' '.join(str(x) for x in runs)


folder_index = 6

annotation_folder = rf'X:\private\{folder_index}\annotations'
ar_annotation_folder = annotation_folder.replace('annotations', 'ar_annotations')
image_folder = annotation_folder.replace('annotations', 'images')
file_names = os.listdir(annotation_folder)

encodings = {}
import codecs
for annotation_file_name in file_names[:]:
    # file_name = './annotations/VAN0006-LK-2-85-AF_preIMS_registered_glomerulus_detections.json'
    image_file_name = annotation_file_name.replace('.json', '.tif')
    image_path = os.path.join(image_folder, image_file_name)
    with codecs.open(os.path.join(annotation_folder, annotation_file_name), 'r', 'utf-8-sig') as data_file:
        data = json.load(data_file)

    polys = []
    for index in range(data.__len__()):
        geom = np.array(data[index]['geometry']['coordinates'])
        polys.append(geom)

    img = imageio.imread(image_path)
    if len(img.shape) == 2:
        img = imageio.volread(image_path)

        if len(img.shape) == 5:
            img = np.reshape(img, (img.shape[2], img.shape[3], img.shape[4],)).astype(img.dtype)
            print("converted size: ", img.shape, "\tdata type: ", img.dtype)
        # the shape of the image, h * w
        shape = (img.shape[-2], img.shape[-1])
    else:
        shape = (img.shape[-3], img.shape[-2])
    print(annotation_file_name, img.shape)

    Image.MAX_IMAGE_PIXELS = None
    img = Image.new('L', (shape[1], shape[0]), 0)  # (w, h)
    for i in range(len(polys)):
        poly = polys[i]
        if len(poly)>1:
            ImageDraw.Draw(img).polygon(poly[0], outline=1, fill=1)

    img.save(rf'{image_folder}\test.png')
    mask_2 = np.array(img)

    encoding_2 = mask2rle(mask_2)
    # encoding_2 = run_length_encoding(mask_2)
    encodings[annotation_file_name] = encoding_2

file = open(fr'{image_folder}\test.csv', 'w', newline='')

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
