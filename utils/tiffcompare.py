from tifffile import imread, imwrite, TiffFile
from skimage import io
import imageio
import numpy as np
import sys

file_name = "FFPE_S164_kaggle.ome.tiff"

# override filepath via args
# Sample: python tifffile_test.py IMAGE_PATH 2 4 8 16
if len(sys.argv) == 2:
    file_name = sys.argv[1]

image_path_B = rf'X:\private\5\images\temp/{file_name}'
image_path_A = rf'G:\HuBMAP\hackathon_new\3\images\{file_name}'

if len(sys.argv) >= 3:
    image_path_A = sys.argv[1]
    image_path_B = sys.argv[2]

data_list = []

for image_path in (image_path_A, image_path_B):
    # read metadata
    tif_tags = {}
    with TiffFile(image_path) as tif:
        for tag in tif.pages[0].tags.values():
            name, value = tag.name, tag.value
            tif_tags[name] = value

    # data = imread(image_path)
    data = imageio.imread(image_path)
    if len(data.shape) == 2:
        data = imageio.volread(image_path)
    print("raw size: ", data.shape, "\tdata type: ", data.dtype)

    if len(data.shape) == 5:
        data = np.reshape(data, (data.shape[2], data.shape[3], data.shape[4],)).astype(data.dtype)
        print("converted size: ", data.shape, "\tdata type: ", data.dtype)

    if len(data.shape) not in [3, 5]:
        print("data dimension not matched with TZCYX")
        exit()

    data_list.append(data)

data_A = data_list[0]
data_B = data_list[1]

diff = data_A - data_B
print(np.array_equal(data_A, data_B), not np.any(diff), np.sum(diff))
