from skimage import io
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

image_path = r"x:\bin_VAN008_combined.jpg"

image = io.imread(image_path)

offset = 15  # 10 is enough, 15 is for 100% cover

types = 4 + 1  # include background

# find the unique points
values, counts = np.unique(image, return_counts=True)
ind = np.argpartition(-counts, kth=5)[:5]
# print(values[ind])
centers = list(values[ind])
centers.sort()
print(centers)

color_table = [[255, 255, 255],  # 'white',
               [0, 0, 255],  # 'blue',
               [255, 0, 0],  # 'red',
               [255, 255, 0],  # 'yellow',
               [0, 255, 0], ]  # 'green'

new_image = np.zeros((image.shape[0], image.shape[1], 3))

for i in range(len(image)):
    for j in range(len(image[i])):
        for k in range(len(centers)):
            center = centers[k]
            if center - offset <= image[i][j] <= center + offset:
                new_image[i][j] = color_table[k]
                break
    if i % 10 == 0:
        print(i)

io.imsave(image_path.replace("jpg", "png"), new_image)
