import json
# from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
import numpy as np
from PIL import Image
import os

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
    rescale_index = 8
    size_index = 1.0

    types = ['PAS', 'AF_preIMS']
    image_type = types[0]

    shift_dict = {
        "VAN0010-LK-155-40-PAS": (1, 0, -13, 0, 1, - 4),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 0, 0, 1, -2),
    }

    for file_name in file_names[:]:
        # file_name = './annotations/VAN0006-LK-2-85-AF_preIMS_registered_glomerulus_detections.json'
        output_name = file_name.split('AF')[0]
        image_name = f'result/images/{image_type}/{output_name}{image_type}_registered_8.jpg'
        html_name = f"{output_name}{image_type}"
        output_file(f"result/{html_name}.html")
        with open(os.path.join(folder, file_name)) as data_file:
            data = json.load(data_file)

        coor_list = []

        for item in data:
            coor_list.extend(item["geometry"]["coordinates"])

        # df = json_normalize(data, max_level=1)

        # geo = df['geometry']

        # coor = pd.read_json(geo.values) # geo['coordinates']

        # print(file_name, len(coor_list))

        x_list = [[xy[0] // rescale_index for xy in coor] for coor in coor_list]
        y_list = [[xy[1] // rescale_index for xy in coor] for coor in coor_list]

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

        p.patches(x_list, y_list, fill_alpha=0, line_alpha=0.5, color='pink', line_width=3, hover_line_alpha=0.05)
        show(p)
