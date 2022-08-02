import numpy as np
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt

def rle2mask(rle, height, width):
    rle = [int(xx) for xx in rle.split(' ')]
    offsets, runs = rle[0::2], rle[1::2]

    tmp = np.zeros(height * width, dtype=np.uint8)
    for offset, run in zip(offsets, runs):
        tmp[offset:offset + run] = 1

    return tmp.reshape(width, height).T


train_df = pd.read_csv(fr"C:\Users\bunny\Desktop\train_ship_segmentations_v2.csv")
print(train_df.head())

img_width = 768
del_list = []

for ind in train_df.index:
    if isinstance(train_df.iloc[ind, 1], str):
        mask = rle2mask(train_df.iloc[2, 1], img_width, img_width)

        plt.figure(figsize=(10,10))
        plt.imshow(mask, cmap='jet', alpha=0.5)
        plt.show()
        io.imsave(fr"C:\Users\bunny\Desktop\test\{train_df.iloc[ind, 0]}", mask.astype(float))
    else:
        del_list.append(f"del {train_df.iloc[ind, 0]}")
        # print(mask.shape)

with open(rf'C:\Users\bunny\Desktop\del.bat', 'w') as fp:
    for item in del_list:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
