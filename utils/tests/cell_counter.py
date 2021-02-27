import os
import sys
from skimage import io

vipshome = r'C:\Users\bunny\Desktop\vips-dev-8.10\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

import pyvips

root = rf'X:\test\VAN0003-LK'

if len(sys.argv) >= 2:
    root = sys.argv[1]

page_count = 1

print(root)

for i in range(page_count):
    # image = pyvips.Image.new_from_file(rf'{root}\layer_{i}_8.tiff', access='sequential', )
    # print(image.max())
    img = io.imread(rf'{root}\layer_{i}.tiff')
    img_dict = {}
    for row in img[::2]:
        for cell in row[::2]:
            value = cell[0]
            if value == 0:
                continue
            if value not in img_dict:
                img_dict[value] = 1
    # print(img_dict.keys())
    keys = img_dict.keys()
    print(max(keys), len(keys))
