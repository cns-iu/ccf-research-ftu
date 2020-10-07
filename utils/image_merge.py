import os
import numpy as np
from skimage import transform, io
from skimage.color import rgb2gray


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def center_filter(mat):
    w, h = mat.shape
    for i in range(h):
        for j in range(w):
            center = mat[i, j]
            if center != 0:
                top, left, right, bottom, tl, tr, bl, br = 0, 0, 0, 0, 0, 0, 0, 0
                if i > 0:
                    top = mat[i - 1, j]
                if j > 0:
                    left = mat[i, j - 1]
                if i > 0 and j > 0:
                    tl = mat[i - 1, j - 1]
                if i + 1 < h:
                    bottom = mat[i + 1, j]
                if j + 1 < w:
                    right = mat[i, j + 1]
                if i + 1 < h and j + 1 < w:
                    br = mat[i + 1, j + 1]
                if i > 0 and j + 1 < w:
                    tr = mat[i - 1, j + 1]
                if i + 1 < h and j > 0:
                    bl = mat[i + 1, j - 1]
                if top > 0 and left > 0 and tl > 0:
                    continue
                if top > 0 and right > 0 and tr > 0:
                    continue
                if bottom > 0 and left > 0 and bl > 0:
                    continue
                if bottom > 0 and right > 0 and br > 0:
                    continue
                mat[i, j] = 0


file_root_dir = r'X:\test_image'

folder_names = [file for file in os.listdir(file_root_dir)]
folder_names.remove("output")
merge_type = 'mask'

h_crop_seg = max([int(file_name.split('_')[1]) for file_name in folder_names]) + 1
v_crop_seg = max([int(file_name.split('_')[0]) for file_name in folder_names]) + 1

result = None
for i in range(v_crop_seg):
    row_blocks = list()
    for j in range(h_crop_seg):
        # file_name = ()) + '-outputs.png'
        folder_name = '_'.join([str(i), str(j)])
        folder_path = os.path.join(file_root_dir, folder_name)
        # file_path = os.path.join(folder_path, 'label.png')
        file_path = os.path.join(folder_path, f'{merge_type}.png')
        file_size = os.path.getsize(file_path)
        if merge_type == 'label' and file_size < 200000:
            file_path = os.path.join(folder_path, f'{folder_name}.png')
        block = io.imread(file_path).astype('uint8')
        if len(block.shape) == 3:
            block = rgb2gray(block).astype('uint8')
        center_filter(block)
        row_blocks.append(block)
    row_merged = np.concatenate([row_blocks[index] for index in range(h_crop_seg)], axis=1)
    if result is None:
        result = row_merged
    else:
        result = np.concatenate((result, row_merged), axis=0)
    print(result.shape)
output_dir = os.path.join(file_root_dir, 'output')
make_dir(output_dir)
io.imsave(os.path.join(output_dir, f'{merge_type}.tiff'), result)
