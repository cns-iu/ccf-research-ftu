import json
# from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Set2_6
import numpy as np
from PIL import Image
import os

# from read_roi import read_roi_zip

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

    folder = r'C:\Users\bunny\Desktop\hackathon_temp\crypts'

    image_index = 'a'
    rescale_index = 1.2

    # VU "gold" standard reading
    gt_file_name = os.path.join(folder, f'{image_index}.json')
    html_name = gt_file_name.replace('json', 'html')
    image_name = gt_file_name.replace('json', 'tiff')
    output_file(html_name)
    path_list = [gt_file_name]

    # student json reading
    name_list = ["Ground Truth", "Tom", "Gleb", "Whats goin on", "Deeplive.exe", "Deepflash2"]
    for i in [1, 2, 3, 4, 5]:
        path_list.append(os.path.join(rf"{folder}\{i}", f"{i}{image_index}.json"))
    json_count = len(path_list)

    color_list = ['yellow', "red", "green", "blue", "fuchsia", "cyan"]

    annotation_list = []
    for i in range(len(path_list)):
        path = path_list[i]
        with open(path) as data_file:
            data = json.load(data_file)

        coor_list = []

        for item in data:
            coor_list.extend(item["geometry"]["coordinates"])
        x_list = [[xy[0] // 2 // rescale_index for xy in coor] for coor in coor_list]
        y_list = [[xy[1] // 2 // rescale_index for xy in coor] for coor in coor_list]
        if i == 0:
            annotation_list.append((x_list, y_list))
        else:
            annotation_list.append((y_list, x_list))

    for i in range(json_count):
        print(name_list[i], color_list[i], '\t', path_list[i])
    background_img = Image.open(image_name).convert('RGBA')
    new_size = (int(background_img.size[0] // rescale_index),
                int(background_img.size[1] // rescale_index))
    background_img = background_img.resize(new_size, Image.ANTIALIAS)
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
    for coord, name, color in zip(annotation_list, name_list, color_list):
        p.patches(coord[0], coord[1],
                  fill_alpha=0,
                  line_alpha=1,
                  # color='pink',
                  color=color,
                  line_width=2.5,
                  hover_line_alpha=0,
                  muted_alpha=0,
                  muted=False if name in name_list[:2] else True,
                  legend_label=name)

    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    show(p)
