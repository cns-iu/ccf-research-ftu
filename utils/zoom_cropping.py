import json
import csv
import shutil
import os
import sys
from skimage import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from bokeh.io import output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.palettes import Set2_5
from bokeh.plotting import save, show


# from read_roi import read_roi_zip
# from collections import OrderedDict

def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)


def crop_patch(x_list, y_list, id_list, title):
    x_start = top_left[0]
    x_end = bottom_right[0]
    y_start = top_left[1]
    y_end = bottom_right[1]

    cropped_patch = raw_image[x_start:x_end, y_start:y_end]
    # rgb_channels = []
    # for i in range(cropped_patch.shape[-1]):
    #     std = np.std(cropped_patch[:, :, i])
    #     mean = np.mean(cropped_patch[:, :, i])
    #     print(np.max(cropped_patch[:, :, i]), np.min(cropped_patch[:, :, i]), mean, std)
    #     # cropped_patch[:, :, i].max()
    #     rgb_channels.append((cropped_patch[:, :, i] - cropped_patch[:, :, i].min()) * (
    #             (255 - 0) / (8 * std)))
    # # # cropped_patch = (cropped_patch - cropped_patch.min()) * ((255 - 0) / (cropped_patch.max() - cropped_patch.min()))
    # # # cropped_patch = np.dstack((np.zeros(rgb_channels[0].shape) ,rgb_channels[1], np.zeros(rgb_channels[0].shape)))
    #
    # cropped_patch = np.dstack(rgb_channels).astype('uint8')
    cropped_patch = np.transpose(cropped_patch, (1, 0, 2))
    img = Image.fromarray(cropped_patch, 'RGB')
    # text = f'{file_prefix}_{title}_{id_list[_id]}'
    text = 'test'
    font_path = r"c:\windows\fonts\bahnschrift.ttf"
    font = ImageFont.truetype(font_path, 24)
    # ImageDraw.Draw(img).text((20, 20), f'{text}', font=font)
    ImageDraw.Draw(img).text((20, 60), f'Type: Glomerulus', font=font)
    ImageDraw.Draw(img).text((20, 100), f'Anno-', font=font)
    ImageDraw.Draw(img).text((20, 125), f'tation', font=font)
    ImageDraw.Draw(img).text((100, 100), f'Raw', font=font)
    ImageDraw.Draw(img).rectangle(((15, 95), (95, 150)), outline="white", width=2)
    ImageDraw.Draw(img).rectangle(((95, 95), (175, 150)), outline="white", width=2)

    for _i in range(len(x_list)):
        xs = x_list[_i]
        ys = y_list[_i]

        polygon = [(xs[j] - x_start, ys[j] - y_start) for j in range(len(xs))]
        ImageDraw.Draw(img).polygon(polygon, fill="#4666FF", width=5)

    left = np.array(img)
    margin = np.zeros((cropped_patch.shape[0], 10, 3))
    margin = 255 - margin
    merge = np.concatenate((left, margin, cropped_patch), axis=1)

    output_path = os.path.join(output_dir, f'{text}.jpg')
    io.imsave(output_path, merge.astype("uint8"))
    print(f"Image saved to {output_path}")

def crop_patch_mxif(x_list, y_list, id_list, title, sub_x_list=None, sub_y_list=None, remarks=None):
    _id = 0
    for _i in range(len(x_list)):
        xs = x_list[_i]
        ys = y_list[_i]
        max_x = max(xs)
        min_x = min(xs)
        max_y = max(ys)
        min_y = min(ys)
        mid_x = (max_x + min_x) // 2
        mid_y = (max_y + min_y) // 2

        x_start = mid_x - int(edge // 2)
        x_end = mid_x + int(edge // 2)
        y_start = mid_y - int(edge // 2)
        y_end = mid_y + int(edge // 2)

        if x_start < 0:
            x_end -= x_start
            x_start = 0
        if x_end > raw_image.shape[0]:
            x_start -= (x_end - raw_image.shape[0])
            x_end = raw_image.shape[0]
        if y_start < 0:
            y_end -= y_start
            y_start = 0
        if y_end > raw_image.shape[1]:
            y_start -= (y_end - raw_image.shape[1])
            y_end = raw_image.shape[1]
        mid_x = (x_start + x_end) // 2
        mid_y = (y_start + y_end) // 2

        cropped_patch = raw_mxif_image[x_start:x_end, y_start:y_end]
        cropped_patch = np.transpose(cropped_patch, (1, 0, 2))

        # left - image processing
        img = Image.fromarray(cropped_patch, 'RGB')
        # text = f'{file_prefix}_{title}_{id_list[_id]}'
        text = f'test_{_id}'
        font_path = r"c:\windows\fonts\bahnschrift.ttf"
        font = ImageFont.truetype(font_path, 24)
        # ImageDraw.Draw(img).text((20, 20), f'{text}', font=font)
        #ImageDraw.Draw(img).text((20, 60), f'Type: Glomerulus', font=font)
        #ImageDraw.Draw(img).text((20, 100), f'Anno-', font=font)
        #ImageDraw.Draw(img).text((20, 125), f'tation', font=font)
        #ImageDraw.Draw(img).text((100, 100), f'Raw', font=font)
        #ImageDraw.Draw(img).rectangle(((15, 95), (95, 150)), outline="white", width=2)
        #ImageDraw.Draw(img).rectangle(((95, 95), (175, 150)), outline="white", width=2)
        if remarks is not None:
            ImageDraw.Draw(img).text((20, 160), f'{remarks[_i]}', font=font)
        polygon = [(xs[j] - (mid_x - int(edge // 2)), ys[j] - (mid_y - int(edge // 2))) for j in range(len(xs))]
        ImageDraw.Draw(img).polygon(polygon, fill="#4666FF", width=5)

        if sub_x_list is not None and sub_y_list is not None:
            sub_xs = sub_x_list[_i]
            sub_ys = sub_y_list[_i]
            polygon = [(sub_xs[j] - (mid_x - int(edge // 2)), sub_ys[j] - (mid_y - int(edge // 2))) for j in
                       range(len(sub_xs))]
            ImageDraw.Draw(img).polygon(polygon, fill="#FF8C00", width=5)

        left = np.array(img)
        margin = np.zeros((cropped_patch.shape[0], 10, 3))
        margin = 255 - margin
        merge = np.concatenate((left, margin, cropped_patch), axis=1)

        output_path = os.path.join(output_dir, f'{text}.jpg')
        io.imsave(output_path, merge.astype("uint8"))
        print(f"Image saved to {output_path}")
        _id += 1


if __name__ == '__main__':
    top_left = (580 * 8, 1745 * 8)
    bottom_right = (740 * 8, 1895 * 8)

    VU_annotation_path = r'../visualization/annotations/VAN0008-RK-403-100-AF_preIMS_registered_glomerulus_detections.json'
    file_B_path = r'../visualization/student_annotations/VAN0008ML.csv'
    raw_image_path = r'X:\VAN0008-RK-403-100-AF_preIMS_registered_rendered.tif'
    mxif_image_path = r'X:\VAN0008-RK-403-101-MxIF_cyc3_registered.ome.tiff - default.ome.tif'
    nuclei_mask_image_path = r'X:\layer_3.tiff'

    file_A_index = 1
    file_B_index = 1

    edge = 500
    shift_dict = {
        "VAN0009-LK-102-7-PAS": (1, 0, -6, 0, 1, -3),
        "VAN0010-LK-155-40-PAS": (1, 0, -14, 0, 1, -5),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 14, 0, 1, -5),
        "VAN0016-LK-202-89-PAS": (1, 0, -3, 0, 1, -3),
    }

    if len(sys.argv) >= 4:
        VU_annotation_path = sys.argv[1]
        file_B_path = sys.argv[2]
        raw_image_path = sys.argv[3]
    if len(sys.argv) >= 6:
        file_A_index = int(sys.argv[4])
        file_B_index = int(sys.argv[5])

    raw_image = io.imread(raw_image_path)
    if len(raw_image.shape) == 5:
        raw_image = np.transpose(raw_image.reshape(raw_image.shape[2:]), (1, 0, 2))
    elif len(raw_image.shape) == 3:
        raw_image = np.transpose(raw_image.reshape(raw_image.shape), (1, 0, 2))
    else:
        print('raw image shape is not 3 or 5: exit')
        sys.exit()

    raw_mxif_image = io.imread(mxif_image_path)
    if len(raw_mxif_image.shape) == 5:
        raw_mxif_image = np.transpose(raw_mxif_image.reshape(raw_mxif_image.shape[2:]), (1, 0, 2))
    elif len(raw_mxif_image.shape) == 3:
        raw_mxif_image = np.transpose(raw_mxif_image.reshape(raw_mxif_image.shape), (1, 0, 2))
    else:
        print('raw_mxif_image shape is not 3 or 5: exit')
        sys.exit()

    nuclei_mask_image = io.imread(nuclei_mask_image_path)

    file_prefix = raw_image_path.split('\\')[-1].split('_registered')[0]
    output_dir = os.path.join(os.path.dirname(raw_image_path), file_prefix)
    make_dir(output_dir)

    # if file_prefix in shift_dict:
    #     img_trans = Image.fromarray(raw_image, 'RGB')
    #     img_trans = img_trans.transform(img_trans.size, Image.AFFINE, shift_dict[file_prefix])
    #     raw_image = np.array(img_trans)

    # A - VU json
    with open(VU_annotation_path) as data_file:
        data = json.load(data_file)

    coor_list = []

    for item in data:
        coor_list.extend(item["geometry"]["coordinates"])
    if file_prefix in shift_dict:
        A_x_list = [[(xy[0] + shift_dict[file_prefix][2] * 8) // file_A_index for xy in coor] for coor in coor_list]
        A_y_list = [[(xy[1] + shift_dict[file_prefix][5] * 8) // file_A_index for xy in coor] for coor in coor_list]
    else:
        A_x_list = [[xy[0] // file_A_index for xy in coor] for coor in coor_list]
        A_y_list = [[xy[1] // file_A_index for xy in coor] for coor in coor_list]

    display_list = []

    for i in range(len(A_x_list)):
        x_list = A_x_list[i]
        y_list = A_y_list[i]
        _flag = True
        for j in range(len(x_list)):
            x = x_list[j]
            y = y_list[j]
            if x < top_left[0] or x > bottom_right[0] or y < top_left[1] or y > bottom_right[1]:
                _flag = False
                break
        if _flag:
            display_list.append(i)

    # export AF images
    selected_A_x_list = [A_x_list[i] for i in range(len(A_x_list)) if i in display_list]
    selected_A_y_list = [A_y_list[i] for i in range(len(A_y_list)) if i in display_list]
    crop_patch(selected_A_x_list, selected_A_y_list, display_list, "VU")

    crop_patch_mxif(selected_A_x_list, selected_A_y_list, display_list, "VU")
