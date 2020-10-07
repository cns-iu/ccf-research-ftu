import os
import math
import numpy as np
from skimage import transform, io
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

root_path = r'X:\test_image\output'
image_name = 'mask.tiff'
output_name = 'new_heatmap.tiff'
img_path = os.path.join(root_path, image_name)
output_path = os.path.join(root_path, output_name)

image = io.imread(img_path)[::2, ::2].astype('uint8')

heat_map = np.zeros(image.shape).astype('uint16')

h, w = image.shape

r = 20
index = 255 // (r + 1)
offset = 10
# for i in range(h):
#     for j in range(w):
#         if image[i, j] != 0:
#             for m in range(-r, r):
#                 for n in range(-r, r):
#                     if 0 <= j + n < w and 0 <= i + m < h:
#                         distant = int((n ** 2 + m ** 2) ** 0.5)
#                         if distant <= r:
#                             distant = distant * index + offset
#                             if distant != 0:
#                                 heat_map[i + m, j + n] += image[i, j] // distant
#                             else:
#                                 heat_map[i, j] += image[i, j]
step = 50
for i in range(0, h, step):
    for j in range(0, w, step):
        heat_map[i:i + step, j:j + step] = image[i:i + step, j:j + step].sum()

    if i % 1000 == 0:
        print(i)
norm1 = heat_map / np.linalg.norm(heat_map).astype('uint8')
g_layer = np.zeros(image.shape).astype('uint8')
b_layer = np.zeros(image.shape).astype('uint8')
result = np.stack([norm1, g_layer, b_layer], axis=0).astype('uint8')
io.imsave(output_path, result)
print(result.shape)
