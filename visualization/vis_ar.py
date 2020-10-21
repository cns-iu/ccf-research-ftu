import json
# from collections import OrderedDict
from bokeh.io import show, save, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.palettes import Set1_6
import numpy as np
from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None

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

    folder = './ar_annotations'
    file_names = os.listdir(folder)
    rescale_index = 8
    size_index = 1.0

    types = ['PAS', 'AF_preIMS']
    image_type = types[0]

    shift_dict = {
        "VAN0009-LK-102-7-PAS": (1, 0, -13, 0, 1, - 4),
        "VAN0010-LK-155-40-PAS": (1, 0, -13, 0, 1, - 4),
        "VAN0014-LK-203-108-PAS": (1.015, -0.010, 0, 0, 1, -2),
    }

    ALL_TYPE_LIST = ['Medulla', 'Inner medulla', 'Cortex', 'Outer Medulla', 'Outer Stripe']

    for file_name in file_names[:]:
        # file_name = './annotations/VAN0006-LK-2-85-AF_preIMS_registered_glomerulus_detections.json'
        output_name = file_name.split('PAS')[0]
        image_name = f'result/images/{image_type}/{output_name}{image_type}_registered_8.jpg'
        if not os.path.isfile(image_name):
            image_name = f'result/images/{image_type}/{output_name}{image_type}_FFPE.ome.jpg'
        if not os.path.isfile(image_name):
            print('image file does not exist')
            continue
        html_name = f"{output_name}{image_type}"
        output_file(f"result/{html_name}.html")
        with open(os.path.join(folder, file_name)) as data_file:
            data = json.load(data_file)

        coor_list = []
        type_list = []
        color_list = []
        color_list_2 = []

        for item in data:
            coor_list.extend(item["geometry"]["coordinates"])
            type_list.append(item["properties"]["classification"]["name"])
            color_list.append(
                f'{"#{:06x}".format(abs(int(item["properties"]["classification"]["colorRGB"])))}')
            color_list_2.append(Set1_6[ALL_TYPE_LIST.index(type_list[-1])])
        ALL_TYPE_LIST.extend(type_list)

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
        # VIS_source = ColumnDataSource(data={
        #     'x_list': x_list,
        #     'y_list': y_list,
        #     'color': color_list,
        #     'title': type_list
        # })
        for xs, ys, color, legend_title in zip(x_list, y_list, color_list_2, type_list):
            p.patch(xs, ys,
                    fill_alpha=0.5, line_alpha=0.6, color=color, line_width=3,
                    hover_line_alpha=0.05,
                    hover_fill_alpha=0.05,
                    muted_alpha=0,
                    muted=False,
                    legend_label=legend_title, )
            # source=VIS_source)

        p.legend.location = "top_left"
        p.legend.click_policy = "mute"

        show_image = False

        if show_image:
            show(p)
        else:
            save(p)
    # print(set(ALL_TYPE_LIST))
