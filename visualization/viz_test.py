import json
import pandas as pd
from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from pandas.io.json import json_normalize
import os

if __name__ == '__main__':
    tools_list = "pan," \
                 "box_select," \
                 "lasso_select," \
                 "box_zoom, " \
                 "wheel_zoom," \
                 "reset," \
                 "save," \
                 "help"

    folder = './annotations'
    file_names = os.listdir(folder)
    size_list = [
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 1.02],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
        [2780, 3805, 0.9],
    ]

    for file_name, size in zip(file_names, size_list):
        # file_name = './annotations/VAN0006-LK-2-85-AF_preIMS_registered_glomerulus_detections.json'
        output_name = file_name.split('_')[0]
        output_file(f"result/{output_name}.html")
        with open(os.path.join(folder, file_name)) as data_file:
            data = json.load(data_file)

        coor_list = []

        for item in data:
            coor_list.extend(item["geometry"]["coordinates"])

        # df = json_normalize(data, max_level=1)

        # geo = df['geometry']

        # coor = pd.read_json(geo.values) # geo['coordinates']

        # print(file_name, len(coor_list))

        x_list = [[xy[0] for xy in coor] for coor in coor_list]
        y_list = [[xy[1] for xy in coor] for coor in coor_list]

        p = figure(match_aspect=True,
                   plot_width=int(size[0] * size[2]), plot_height=int(size[1] * size[2]),
                   tools=tools_list,
                   # title='nuclei/vessel distance',
                   )

        p.image_url(url=[r'C:\Users\bunny\Desktop\VAN0006-LK-2-85-AF_preIMS_registered.ome.tiff - default.jpg'],
                    x=0, y=0, anchor="bottom_left")
        p.xgrid.visible = False
        p.ygrid.visible = False
        p.axis.visible = False
        p.background_fill_alpha = 0.0
        p.outline_line_color = None

        p.patches(x_list, y_list, fill_alpha=0, color='white', line_width=2)
        show(p)
