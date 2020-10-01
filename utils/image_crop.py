import os
import math
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


file_root_dir = r'X:\test'
app_crop_size = 500

file_names = [file for file in os.listdir(file_root_dir) if file.endswith('.tif')]
for file_name in file_names:
    output_dir = os.path.join(file_root_dir, f'{file_name[:-4]}_output')
    make_dir(output_dir)
    file_path = os.path.join(file_root_dir, file_name)
    image = io.imread(file_path)

    h, w, c = image.shape [2:]
    h_seg = w // app_crop_size
    v_seg = h // app_crop_size
    print(h_seg, v_seg)
    image = image.reshape(h, w, c)
    image = image[: v_seg * app_crop_size, : h_seg * app_crop_size, :]

    rows = np.split(image, v_seg, axis=0)
    for i in range(len(rows)):
        row = rows[i]
        blocks = np.split(row, h_seg, axis=1)
        for j in range(len(blocks)):
            block = blocks[j]
            # block = transform.resize(block, (256, 256), anti_aliasing=True)
            # block = np.concatenate((block, 1 - np.zeros(block.shape)), axis=1)
            output_file_name = ('_'.join([str(i), str(j)])) + '.png'
            output_sub_dir = os.path.join(output_dir, '_'.join([str(i), str(j)]))
            make_dir(output_sub_dir)
            io.imsave(os.path.join(output_sub_dir, output_file_name), block)
            print(block.shape, os.path.join(output_dir, output_file_name))
