import json
# from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Set2_5
import numpy as np
from PIL import Image
import os
from read_roi import read_roi_zip

if __name__ == '__main__':
    tools_list = "pan," \
                 "box_select," \
                 "lasso_select," \
                 "box_zoom, " \
                 "wheel_zoom," \
                 "reset," \
                 "save," \
                 "help," \
        # "hover"

    folder = './annotations'
    file_names = os.listdir(folder)
    size_index = 1.0

    types = ['PAS', 'AF_preIMS']
    image_type = types[0]

    shift_dict = {
        "VAN0010-LK-155-40-PAS": (1, 0, -13, 0, 1, - 4),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 0, 0, 1, -2),
    }

    # VU "gold" standard reading
    file_name = 'VAN0008-RK-403-100-AF_preIMS_registered_glomerulus_detections.json'
    output_name = file_name.split('AF')[0]
    image_name = f'result/images/{image_type}/{output_name}{image_type}_registered_8.jpg'
    html_name = f"{output_name}{image_type}_compare"
    output_file(f"result/{html_name}.html")
    path_list = [os.path.join(folder, file_name)]
    rescale_index_list = [8, 4, 4, 4, 4]

    # student json reading
    image_index_name = output_name = file_name.split('-')[0]
    name_list = ["VU", "Jash", "Leah", "Yash", "Sumeet"]
    path_list.append(os.path.join('./student_annotations', 'VAN0008Jash.json'))
    path_list.append(os.path.join('./student_annotations', 'VAN0008Leah.json'))
    json_count = len(path_list)

    annotation_list = []
    for i in range(len(path_list)):
        path = path_list[i]
        rescale_index = rescale_index_list[i]
        with open(path) as data_file:
            data = json.load(data_file)

        coor_list = []

        for item in data:
            coor_list.extend(item["geometry"]["coordinates"])
        x_list = [[xy[0] // rescale_index for xy in coor] for coor in coor_list]
        y_list = [[xy[1] // rescale_index for xy in coor] for coor in coor_list]
        annotation_list.append((x_list, y_list))

    # student roi reading
    path_list.append(os.path.join('./student_annotations', "VAN0008Yash.zip"))
    path_list.append(os.path.join('./student_annotations', "VAN0008Sumeet.zip"))
    for i in range(json_count, len(path_list)):
        path = path_list[i]
        rescale_index = rescale_index_list[i]
        rois = read_roi_zip(path)
        center_x_list = []
        center_y_list = []
        width_r_list = []
        height_r_list = []
        for key in rois.keys():
            left = rois[key]['left']
            top = rois[key]['top']
            width = rois[key]['width']
            height = rois[key]['height']

            center_x = int(left + (width / 2))
            center_y = int(top + (height / 2))
            width_r = int(width / 1)
            height_r = int(height / 1)

            center_x_list.append(center_x // rescale_index)
            center_y_list.append(center_y // rescale_index)
            width_r_list.append(width_r // rescale_index)
            height_r_list.append(height_r // rescale_index)
        annotation_list.append((center_x_list, center_y_list, width_r_list, height_r_list))

    background_img = Image.open(image_name).convert('RGBA')
    if html_name in shift_dict:
        background_img = background_img.transform(background_img.size, Image.AFFINE, shift_dict[html_name])
    # background_img = np.roll(background_img,(10,0,0))
    xdim, ydim = background_img.size
    a_layer = np.empty((ydim, xdim), dtype=np.uint32)
    view = a_layer.view(dtype=np.uint8).reshape((ydim, xdim, 4))
    # view[:, :, :] = np.flipud(np.asarray(lena_img))
    view[:, :, :] = np.asarray(background_img)

    p = figure(match_aspect=True,
               plot_width=int(xdim * size_index), plot_height=int(ydim * size_index),
               tools=tools_list,
               # title='nuclei/vessel distance',
               )

    # p.image_url(url=[image_name], x=0, y=0, anchor="bottom_left")

    p.image_rgba(image=[a_layer], x=0, y=0, dw=xdim, dh=ydim)
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.visible = False
    p.background_fill_alpha = 0.0
    p.outline_line_color = None
    p.add_tools(HoverTool(show_arrow=False,
                          line_policy='nearest',
                          tooltips=None))
    for coord, name, color in zip(annotation_list[:json_count], name_list[:json_count], Set2_5[:json_count]):
        p.patches(coord[0], coord[1],
                  fill_alpha=0,
                  line_alpha=0.5,
                  # color='pink',
                  color=color,
                  line_width=3,
                  hover_line_alpha=0.05,
                  legend_label=name)

    for coord, name, color in zip(annotation_list[json_count:], name_list[json_count:],
                                  Set2_5[json_count:len(name_list)]):
        p.ellipse(x=coord[0], y=coord[1], width=coord[2], height=coord[3],
                  fill_alpha=0,
                  line_alpha=0.5,
                  # color='pink',
                  color=color,
                  line_width=3,
                  hover_line_alpha=0.05,
                  legend_label=name)

    # ML csv reading
    import csv

    rx, ry, widths, heights = [], [], [], []
    with open(os.path.join('./student_annotations', 'VAN0008ML.csv'), newline='') as inputfile:
        for row in csv.reader(inputfile):
            tlx = int(row[0]) // rescale_index_list[0]
            tly = int(row[1]) // rescale_index_list[0]
            brx = int(row[2]) // rescale_index_list[0]
            bry = int(row[3]) // rescale_index_list[0]
            widths.append(brx - tlx)
            heights.append(bry - tly)
            rx.append(tlx + widths[-1] // 2)
            ry.append(tly + heights[-1] // 2)
    p.rect(x=rx, y=ry, width=widths, height=heights,
           fill_alpha=0,
           line_alpha=0.5,
           # color='pink',
           color='red',
           line_width=3,
           hover_line_alpha=0.05,
           legend_label='ML')

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    show(p)
