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


def crop_patch(x_list, y_list, id_list, title, sub_x_list=None, sub_y_list=None, remarks=None):
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

        cropped_patch = raw_image[x_start:x_end, y_start:y_end]
        cropped_patch = np.transpose(cropped_patch, (1, 0, 2))

        # left - image processing
        img = Image.fromarray(cropped_patch, 'RGB')
        text = f'{file_prefix}_{title}_{id_list[_id]}'
        font_path = r"c:\windows\fonts\bahnschrift.ttf"
        font = ImageFont.truetype(font_path, 24)
        ImageDraw.Draw(img).text((20, 20), f'{text}', font=font)
        ImageDraw.Draw(img).text((20, 60), f'Type: Glomerulus', font=font)
        ImageDraw.Draw(img).text((20, 100), f'Anno-', font=font)
        ImageDraw.Draw(img).text((20, 125), f'tation', font=font)
        ImageDraw.Draw(img).text((100, 100), f'Raw', font=font)
        ImageDraw.Draw(img).rectangle(((15, 95), (95, 150)), outline="white", width=2)
        ImageDraw.Draw(img).rectangle(((95, 95), (175, 150)), outline="white", width=2)
        if remarks is not None:
            ImageDraw.Draw(img).text((20, 160), f'{remarks[_i]}', font=font)
        polygon = [(xs[j] - (mid_x - int(edge // 2)), ys[j] - (mid_y - int(edge // 2))) for j in range(len(xs))]
        ImageDraw.Draw(img).line(polygon, fill="#4666FF", width=5)

        if sub_x_list is not None and sub_y_list is not None:
            sub_xs = sub_x_list[_i]
            sub_ys = sub_y_list[_i]
            polygon = [(sub_xs[j] - (mid_x - int(edge // 2)), sub_ys[j] - (mid_y - int(edge // 2))) for j in
                       range(len(sub_xs))]
            ImageDraw.Draw(img).line(polygon, fill="#FF8C00", width=5)

        left = np.array(img)
        margin = np.zeros((cropped_patch.shape[0], 10, 3))
        margin = 255 - margin
        merge = np.concatenate((left, margin, cropped_patch), axis=1)

        output_path = os.path.join(output_dir, f'{text}.jpg')
        io.imsave(output_path, merge.astype("uint8"))
        print(f"Image saved to {output_path}")
        _id += 1


if __name__ == '__main__':
    file_A_path = r'../visualization/annotations/VAN0008-RK-403-100-AF_preIMS_registered_glomerulus_detections.json'
    file_B_path = r'../visualization/student_annotations/VAN0008ML.csv'
    raw_image_path = r'X:\VAN0008-RK-403-100-PAS_registered.ome.tiff'

    file_A_index = 1
    file_B_index = 1

    edge = 1000
    shift_dict = {
        "VAN0009-LK-102-7-PAS": (1, 0, -6, 0, 1, -3),
        "VAN0010-LK-155-40-PAS": (1, 0, -14, 0, 1, -5),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 14, 0, 1, -5),
        "VAN0016-LK-202-89-PAS": (1, 0, -3, 0, 1, -3),
    }

    if len(sys.argv) >= 4:
        file_A_path = sys.argv[1]
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

    file_prefix = raw_image_path.split('\\')[-1].split('_registered')[0]
    output_dir = os.path.join(os.path.dirname(raw_image_path), file_prefix)
    make_dir(output_dir)

    # if file_prefix in shift_dict:
    #     img_trans = Image.fromarray(raw_image, 'RGB')
    #     img_trans = img_trans.transform(img_trans.size, Image.AFFINE, shift_dict[file_prefix])
    #     raw_image = np.array(img_trans)

    # A - VU json
    with open(file_A_path) as data_file:
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

    # B - ML
    B_x_list, B_y_list, widths, heights = [], [], [], []
    tl_x, tl_y, br_x, br_y = [], [], [], []
    confidences = []
    with open(file_B_path, newline='') as inputfile:
        for row in csv.reader(inputfile):
            tlx = int(row[-5]) // file_B_index
            tly = int(row[-4]) // file_B_index
            brx = int(row[-3]) // file_B_index
            bry = int(row[-2]) // file_B_index
            widths.append(brx - tlx)
            heights.append(bry - tly)
            B_x_list.append(tlx + widths[-1] // 2)
            B_y_list.append(tly + heights[-1] // 2)
            tl_x.append(tlx)
            tl_y.append(tly)
            br_x.append(brx)
            br_y.append(bry)
            confidences.append(float(row[-1]))

    # find difference
    center_list_VU = []
    for i in range(len(A_x_list)):
        mean_x = sum(A_x_list[i]) / len(A_x_list[i])
        mean_y = sum(A_y_list[i]) / len(A_y_list[i])
        center_list_VU.append((mean_x, mean_y))

    center_list_ML = [(B_x_list[i], B_y_list[i]) for i in range(len(B_x_list))]

    VU_false_positive_list = []
    ML_false_positive_list = []
    VU_same_list = []
    ML_same_list = []

    threshold = 200 // file_A_index
    for x, y in center_list_VU:
        _flag = False
        for _x, _y in center_list_ML:
            if (x - _x) ** 2 + (y - _y) ** 2 <= threshold ** 2:
                _flag = True
                VU_same_list.append(center_list_VU.index((x, y)))
                ML_same_list.append(center_list_ML.index((_x, _y)))
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
    selected_B_x_list = [[tl_x[i], tl_x[i], br_x[i], br_x[i], tl_x[i]]
                         for i in range(len(B_x_list)) if i in ML_false_positive_list]
    selected_B_y_list = [[tl_y[i], br_y[i], br_y[i], tl_y[i], tl_y[i]]
                         for i in range(len(B_y_list)) if i in ML_false_positive_list]
    selected_conf_remarks = [f'Confidence = {confidences[i]}' for i in range(len(B_y_list)) if
                             i in ML_false_positive_list]
    crop_patch(selected_B_x_list, selected_B_y_list, ML_false_positive_list, "ML", remarks=selected_conf_remarks)

    # export same images
    VU_same_x_list = [A_x_list[i] for i in VU_same_list]
    VU_same_y_list = [A_y_list[i] for i in VU_same_list]
    ML_same_x_list = [[tl_x[i], tl_x[i], br_x[i], br_x[i], tl_x[i]] for i in ML_same_list]
    ML_same_y_list = [[tl_y[i], br_y[i], br_y[i], tl_y[i], tl_y[i]] for i in ML_same_list]
    conf_remarks = [f'Confidence = {confidences[i]}' for i in ML_same_list]
    crop_patch(ML_same_x_list, ML_same_y_list, ML_same_list, "ML",
               sub_x_list=VU_same_x_list, sub_y_list=VU_same_y_list, remarks=conf_remarks)

    # for confidence filter
    # thre = 0.99
    # VU_same_x_list = [A_x_list[i] for i in VU_same_list if confidences[ML_same_list[VU_same_list.index(i)]] < thre]
    # VU_same_y_list = [A_y_list[i] for i in VU_same_list if confidences[ML_same_list[VU_same_list.index(i)]] < thre]
    # ML_same_x_list = [[tl_x[i], tl_x[i], br_x[i], br_x[i], tl_x[i]] for i in ML_same_list if confidences[i] < thre]
    # ML_same_y_list = [[tl_y[i], br_y[i], br_y[i], tl_y[i], tl_y[i]] for i in ML_same_list if confidences[i] < thre]
    # conf_remarks = [f'Confidence = {confidences[i]}' for i in ML_same_list if confidences[i] < thre]
    # crop_patch(ML_same_x_list, ML_same_y_list, ML_same_list, "ML",
    #            sub_x_list=VU_same_x_list, sub_y_list=VU_same_y_list, remarks=conf_remarks)

    # visualization
    tools_list = "pan," \
                 "box_select," \
                 "lasso_select," \
                 "box_zoom, " \
                 "wheel_zoom," \
                 "reset," \
                 "save," \
                 "help," \
        # "hover"
    custom_tooltip = [
        ("id", "$id"),
        # ("(x,y)", "($x, $y)"),
        # ("label", "@label"),
    ]
    types = ['PAS', 'AF_preIMS']
    image_type = types[0]

    image_name = f'../visualization/result/images/{image_type}/{file_prefix}_registered_8.jpg'
    html_name = f"{file_prefix}"
    output_file(os.path.join(output_dir, f'{html_name}.html'))
    background_img = Image.open(image_name).convert('RGBA')
    # if html_name in shift_dict:
    #     background_img = background_img.transform(background_img.size, Image.AFFINE, shift_dict[html_name])
    # background_img = np.roll(background_img,(10,0,0))
    xdim, ydim = background_img.size
    a_layer = np.empty((ydim, xdim), dtype=np.uint32)
    view = a_layer.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    # view[:, :, :] = np.flipud(np.asarray(lena_img))
    view[:, :, :] = np.asarray(background_img)

    p = figure(match_aspect=True,
               plot_width=int(xdim), plot_height=int(ydim),
               tools=tools_list,
               # title='nuclei/vessel distance',
               )

    p.image_rgba(image=[a_layer], x=0, y=0, dw=xdim, dh=ydim)
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False
    p.background_fill_alpha = 0.0
    p.outline_line_color = None
    p.add_tools(HoverTool(show_arrow=False,
                          line_policy='nearest',
                          tooltips=None))

    selected_A_x_list = [[item // 8 for item in A_x_list[i]] for i in range(len(A_x_list)) if
                         i in VU_false_positive_list]
    selected_A_y_list = [[item // 8 for item in A_y_list[i]] for i in range(len(A_y_list)) if
                         i in VU_false_positive_list]
    selected_B_x_list = [[tl_x[i] // 8, tl_x[i] // 8, br_x[i] // 8, br_x[i] // 8, tl_x[i] // 8]
                         for i in range(len(B_x_list)) if i in ML_false_positive_list]
    selected_B_y_list = [[tl_y[i] // 8, br_y[i] // 8, br_y[i] // 8, tl_y[i] // 8, tl_y[i] // 8]
                         for i in range(len(B_y_list)) if i in ML_false_positive_list]

    VU_source = ColumnDataSource(data={
        'x_list': selected_A_x_list,
        'y_list': selected_A_y_list,
        'id': VU_false_positive_list,
    })
    ML_source = ColumnDataSource(data={
        'x_list': selected_B_x_list,
        'y_list': selected_B_y_list,
        'id': ML_false_positive_list,
    })

    for data_source, color, name in zip(
            (VU_source, ML_source),
            (Set2_5[0], 'red'),
            ('VU_false_positive', 'ML_false_positive')):
        p.patches(xs='x_list',
                  ys='y_list',
                  source=data_source,
                  fill_alpha=0,
                  line_alpha=0.5,
                  color=color,
                  line_width=3,
                  hover_line_alpha=0.05,
                  muted_alpha=0,
                  muted=False,
                  legend_label=name)

    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    show_image = False

    if show_image:
        show(p)
    else:
        save(p)
