import json
import csv
from skimage import io
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import sys


# from collections import OrderedDict
# from bokeh.io import show, output_file
# from bokeh.plotting import figure
# from bokeh.models import HoverTool
# from bokeh.palettes import Set2_5
# from read_roi import read_roi_zip


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def crop_patch(x_list, y_list, id_list, title):
    _i = 0
    for xs, ys in zip(x_list, y_list):
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
        cropped_patch = raw_image[x_start:x_end, y_start:y_end]
        # cropped_patch = raw_image[mid_x - int(w * 1.5):mid_x + int(w * 1.5),
        #                 mid_y - int(h * 1.5):mid_y + int(h * 1.5)]
        cropped_patch = np.transpose(cropped_patch, (1, 0, 2))

        # left - image processing
        img = Image.fromarray(cropped_patch, 'RGB')
        text = f'{file_prefix}_{title}_{id_list[_i]}'
        font_path = r"c:\windows\fonts\bahnschrift.ttf"
        font = ImageFont.truetype(font_path, 24)
        ImageDraw.Draw(img).text((20, 20), f'{text}', font=font)
        ImageDraw.Draw(img).text((20, 60), f'Type: Glomerulus', font=font)
        ImageDraw.Draw(img).text((20, 100), f'Anno-', font=font)
        ImageDraw.Draw(img).text((20, 125), f'tation', font=font)
        ImageDraw.Draw(img).text((100, 100), f'Raw', font=font)
        ImageDraw.Draw(img).rectangle(((15, 95), (95, 150)), outline="white", width=2)
        ImageDraw.Draw(img).rectangle(((95, 95), (175, 150)), outline="white", width=2)
        polygon = [(xs[j] - (mid_x - int(edge // 2)), ys[j] - (mid_y - int(edge // 2))) for j in range(len(xs))]
        # polygon.append((xs[0], ys[0]))
        ImageDraw.Draw(img).line(polygon, fill="#4666FF", width=5)
        left = np.array(img)

        margin = np.zeros((cropped_patch.shape[0], 10, 3))
        margin = 255 - margin
        merge = np.concatenate((left, margin, cropped_patch), axis=1)
        output_path = os.path.join(output_dir, f'{text}.jpg')
        io.imsave(output_path, merge.astype("uint8"))
        print(f"Image saved to {output_path}")
        _i += 1


if __name__ == '__main__':
    file_A_path = r'../visualization/annotations/VAN0008-RK-403-100-AF_preIMS_registered_glomerulus_detections.json'
    file_B_path = r'../visualization/student_annotations/VAN0008ML.csv'
    raw_image_path = r'X:\VAN0008-RK-403-100-PAS_registered.ome.tiff'

    file_A_index = 1
    file_B_index = 1

    edge = 1000
    shift_dict = {
        "VAN0009-LK-102-7-PAS": (1, 0, -4 * 8, 0, 1, - 13 * 8),
        "VAN0010-LK-155-40-PAS": (1, 0, -4 * 8, 0, 1, - 13 * 8),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 0, 0, 1, -2),
    }

    if len(sys.argv) >= 4:
        file_A_path = sys.argv[1]
        file_B_path = sys.argv[2]
        raw_image_path = sys.argv[3]
    if len(sys.argv) >= 6:
        file_A_index = int(sys.argv[4])
        file_B_index = int(sys.argv[5])

    raw_image = io.imread(raw_image_path)
    raw_image = np.transpose(raw_image.reshape(raw_image.shape[2:]), (1, 0, 2))

    file_prefix = raw_image_path.split('\\')[-1].split('_registered')[0]
    output_dir = os.path.join(os.path.dirname(raw_image_path), file_prefix)
    make_dir(output_dir)

    if file_prefix in shift_dict:
        img_trans = Image.fromarray(raw_image, 'RGB')
        img_trans = img_trans.transform(img_trans.size, Image.AFFINE, shift_dict[file_prefix])
        raw_image = np.array(img_trans)

    # A - VU json
    with open(file_A_path) as data_file:
        data = json.load(data_file)

    coor_list = []

    for item in data:
        coor_list.extend(item["geometry"]["coordinates"])
    A_x_list = [[xy[0] // file_A_index for xy in coor] for coor in coor_list]
    A_y_list = [[xy[1] // file_A_index for xy in coor] for coor in coor_list]

    # B - ML
    B_x_list, B_y_list, widths, heights = [], [], [], []
    tl_xy, br_xy = [], []
    with open(file_B_path, newline='') as inputfile:
        for row in csv.reader(inputfile):
            tlx = int(row[0]) // file_B_index
            tly = int(row[1]) // file_B_index
            brx = int(row[2]) // file_B_index
            bry = int(row[3]) // file_B_index
            widths.append(brx - tlx)
            heights.append(bry - tly)
            B_x_list.append(tlx + widths[-1] // 2)
            B_y_list.append(tly + heights[-1] // 2)
            tl_xy.append((tlx, tly))
            br_xy.append((brx, bry))

    # find difference
    center_list_VU = []
    for i in range(len(A_x_list)):
        mean_x = sum(A_x_list[i]) / len(A_x_list[i])
        mean_y = sum(A_y_list[i]) / len(A_y_list[i])
        center_list_VU.append((mean_x, mean_y))

    center_list_ML = [(B_x_list[i], B_y_list[i]) for i in range(len(B_x_list))]

    VU_false_positive_list = []
    ML_false_positive_list = []

    threshold = 150 // file_A_index
    for x, y in center_list_VU:
        _flag = False
        for _x, _y in center_list_ML:
            if (x - _x) ** 2 + (y - _y) ** 2 <= threshold ** 2:
                _flag = True
                break
        if not _flag:
            VU_false_positive_list.append(center_list_VU.index((x, y)))

    for x, y in center_list_ML:
        _flag = False
        for _x, _y in center_list_VU:
            if (x - _x) ** 2 + (y - _y) ** 2 <= threshold ** 2:
                _flag = True
                break
        if not _flag:
            ML_false_positive_list.append(center_list_ML.index((x, y)))

    # export VU images
    selected_A_x_list = [A_x_list[i] for i in range(len(A_x_list)) if i in VU_false_positive_list]
    selected_A_y_list = [A_y_list[i] for i in range(len(A_y_list)) if i in VU_false_positive_list]
    crop_patch(selected_A_x_list, selected_A_y_list, VU_false_positive_list, "VU")

    # export ML images
    selected_B_x_list = [[tl_xy[i][0], tl_xy[i][0], br_xy[i][0], br_xy[i][0], tl_xy[i][0]]
                         for i in range(len(B_x_list)) if i in ML_false_positive_list]
    selected_B_y_list = [[tl_xy[i][1], br_xy[i][1], br_xy[i][1], tl_xy[i][1], tl_xy[i][1]]
                         for i in range(len(B_y_list)) if i in ML_false_positive_list]
    crop_patch(selected_B_x_list, selected_B_y_list, ML_false_positive_list, "ML")
