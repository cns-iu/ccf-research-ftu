import os
import numpy as np
from skimage import transform, io


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


file_root_dir = r'C:\Users\bunny\Desktop\test_image'

folder_names = [file for file in os.listdir(file_root_dir)]

h_crop_seg = max([int(file_name.split('_')[1]) for file_name in folder_names]) + 1
v_crop_seg = max([int(file_name.split('_')[0]) for file_name in folder_names]) + 1

result = None
for i in range(v_crop_seg):
    row_blocks = list()
    for j in range(h_crop_seg):
        #file_name = ()) + '-outputs.png'
        folder_name = '_'.join([str(i), str(j)])
        folder_path = os.path.join(file_root_dir, folder_name)
        file_path = os.path.join(folder_path, 'label.png')
        file_size = os.path.getsize(file_path)
        if file_size < 200000:
            file_path = os.path.join(folder_path, f'{folder_name}.png')
        row_blocks.append(io.imread(file_path))
    row_merged = np.concatenate([row_blocks[index] for index in range(h_crop_seg)], axis=1)
    if result is None:
        result = row_merged
    else:
        result = np.concatenate((result, row_merged), axis=0)
    print(result.shape)
output_dir = os.path.join(file_root_dir, 'output')
make_dir(output_dir)
io.imsave(os.path.join(output_dir, 'result.tiff'), result)


