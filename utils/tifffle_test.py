from tifffile import imread, imwrite, TiffFile
from skimage.transform import rescale
import numpy as np
import sys

image_path = rf'X:\VAN0005-RK-4-172-AF_preIMS_registered.ome.tiff'

shrink_list = [2, 4, 8, 16]

# override filepath via args
# Sample: python tifffile_test.py IMAGE_PATH 2 4 8 16
if len(sys.argv) >= 2:
    image_path = sys.argv[1]
if len(sys.argv) >= 3:
    shrink_list = []
    for i in range(2, len(sys.argv)):
        shrink_list.append(sys.argv[i])

# read metadata
tif_tags = {}
with TiffFile(image_path) as tif:
    for tag in tif.pages[0].tags.values():
        name, value = tag.name, tag.value
        tif_tags[name] = value

data = imread(image_path)
print("raw size: ", data.shape, "\tdata type: ", data.dtype)

if len(data.shape) == 3:
    print("3-D data converting to 5-D data, TZCYX")
    data = np.reshape(data, (1, 1, data.shape[0], data.shape[1], data.shape[2])).astype(data.dtype)

if len(data.shape) not in [3, 5]:
    print("data dimension not matched with TZCYX")
    exit()

for shrink_index in shrink_list:
    print(f"resizing: scale = {shrink_index}")
    layers = []
    i = 1
    for layer in data[0][0]:
        print(f"\tlayer {i}")
        resized_layer = rescale(layer, 1 / float(shrink_index), anti_aliasing=False, preserve_range=True)
        layers.append(resized_layer)
        i += 1
    print("\tstacking layers")
    resized_data = np.stack(layers, axis=0)
    resized_data = np.reshape(resized_data,
                              (1,
                               1,
                               resized_data.shape[0],
                               resized_data.shape[1],
                               resized_data.shape[2])).astype(data.dtype)

    print("\tafter resizing: ", resized_data.shape, "\tdata type: ", resized_data.dtype)
    output_path = ""

    postfix_list = ['.ome.tiff', '.tiff']

    for postfix in postfix_list:
        if image_path.endswith(postfix):
            output_path = image_path[:-len(postfix)] + f"_{shrink_index}" + postfix
            break

    if len(output_path) == 0:
        print("failed to generate output path")
        exit()

    print(f"\twriting file at {output_path}")
    unit_index = 10000
    imwrite(output_path, resized_data, metadata={'axes': 'TZCYX',
                                                 # 'PhysicalSizeX': 0.5 * int(shrink_index),
                                                 # 'PhysicalSizeY': 0.5 * int(shrink_index),
                                                 # 'PhysicalSizeXUnit': 'um',
                                                 # 'PhysicalSizeYUnit': 'um',
                                                 },
            # resolution=((tif_tags['XResolution'][0] // unit_index // int(shrink_index), tif_tags['XResolution'][1]),
            #             (tif_tags['YResolution'][0] // unit_index // int(shrink_index), tif_tags['YResolution'][1])),
            resolution=((tif_tags['XResolution'][0] * int(shrink_index), tif_tags['XResolution'][1]),
                        (tif_tags['YResolution'][0] * int(shrink_index), tif_tags['YResolution'][1])),
            imagej=True)
