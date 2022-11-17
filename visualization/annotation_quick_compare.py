import json
# from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Category10_10
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

    # VU "gold" standard reading
    file_name = r'X:\00a67c839.json'
    output_name = file_name.split('\\')[-1].split('.')[0]
    image_name = fr'X:\00a67c839.jpg'
    html_name = fr"{output_name}_{image_type}_compare"
    output_file(f"result/{html_name}.html")
    path_list = [os.path.join(folder, file_name)]
    rescale_index_list = [8, 8, 8, 8, 8]

    # student json reading
    image_index_name = output_name = file_name.split('-')[0]
    name_list = ["ground_truth", "predicted", ]
    path_list.append(r'X:\pred_00a67c839.json')
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

    background_img = Image.open(image_name).convert('RGBA')
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
    for coord, name, color in zip(annotation_list[:json_count], name_list[:json_count],
                                  Category10_10[2:2 + json_count]):
        p.patches(coord[0], coord[1],
                  fill_alpha=0,
                  line_alpha=0.8,
                  # color='pink',
                  color=color,
                  line_width=3,
                  hover_line_alpha=0.05,
                  muted_alpha=0,
                  muted=False,
                  legend_label=name)

    for coord, name, color in zip(annotation_list[json_count:], name_list[json_count:],
                                  Category10_10[json_count:len(name_list)]):
        p.ellipse(x=coord[0], y=coord[1], width=coord[2], height=coord[3],
                  fill_alpha=0,
                  line_alpha=0.8,
                  # color='pink',
                  color=color,
                  line_width=3,
                  hover_line_alpha=0.05,
                  muted_alpha=0,
                  muted=False,
                  legend_label=name)

    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    show(p)
