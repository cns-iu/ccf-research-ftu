import json
# from collections import OrderedDict
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool
import numpy as np
from PIL import Image
import os
from bokeh.palettes import Set1_6

Image.MAX_IMAGE_PIXELS = None


def polygonArea(X, Y, n):
    # Initialze area
    area = 0.0

    # Calculate value of shoelace formula
    j = n - 1
    for i in range(0, n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i  # j is previous vertex to i

    # Return absolute value
    return int(abs(area / 2.0))


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

    folder_index = 1

    annotation_folder = rf'X:\hackathon_new\{folder_index}\annotations'
    ar_annotation_folder = annotation_folder.replace('annotations', 'ar_annotations')
    image_folder = annotation_folder.replace('annotations', 'images_8')
    output_folder = annotation_folder.replace('annotations', 'visualization')
    file_names = os.listdir(annotation_folder)
    rescale_index = 8
    size_index = 1.0

    types = ['PAS', 'AF_preIMS']
    image_type = types[0]

    shift_dict = {
        "_VAN0009-LK-102-7-PAS": (1, 0, -13, 0, 1, - 4),
        "_VAN0010-LK-155-40-PAS": (1, 0, -13, 0, 1, - 4),
        # "VAN0014-LK-203-108-PAS": (1.015, -0.010, 0, 0, 1, -2),
    }

    for annotation_file_name in file_names[:]:
        # file_name = './annotations/VAN0006-LK-2-85-AF_preIMS_registered_glomerulus_detections.json'
        image_file_name = annotation_file_name.replace('.json', '.jpg')
        image_path = os.path.join(image_folder, image_file_name)
        html_name = annotation_file_name.replace('.json', '.html')
        html_path = os.path.join(output_folder, html_name)
        output_file(html_path)
        with open(os.path.join(annotation_folder, annotation_file_name)) as data_file:
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

        for i in range(len(x_list)):
            if polygonArea(x_list[i], y_list[i], len(x_list[i])) < 100:
                print(polygonArea(x_list[i], y_list[i], len(x_list[i])), x_list[i][0], y_list[i][0],
                      annotation_file_name)

        background_img = Image.open(image_path).convert('RGBA')
        # background_img = background_img.resize(
        #     (round(background_img.size[0] // rescale_index),
        #      round(background_img.size[1] // rescale_index)))

        # from tifffile import imread, imwrite, TiffFile
        # from skimage.transform import rescale
        #
        # # read metadata
        # tif_tags = {}
        # with TiffFile(image_path) as tif:
        #     for tag in tif.pages[0].tags.values():
        #         name, value = tag.name, tag.value
        #         tif_tags[name] = value
        #
        # data = imread(image_path)
        # print("raw size: ", data.shape, "\tdata type: ", data.dtype)
        #
        # if len(data.shape) == 3:
        #     print("3-D data converting to 5-D data, TZCYX")
        #     data = np.transpose(data, (2, 0, 1))
        #     data = np.reshape(data, (1, 1, data.shape[0], data.shape[1], data.shape[2],)).astype(data.dtype)
        #
        # if len(data.shape) not in [3, 5]:
        #     print("data dimension not matched with TZCYX")
        #     exit()
        #
        # layers = []
        # i = 1
        # for layer in data[0][0]:
        #     print(f"\tlayer {i}")
        #     resized_layer = rescale(layer, 1 / float(rescale_index), anti_aliasing=False, preserve_range=True)
        #     layers.append(resized_layer)
        #     i += 1
        # print("\tstacking layers")
        # resized_data = np.stack(layers, axis=0)
        # resized_data = np.reshape(resized_data,
        #                           (
        #                               resized_data.shape[0],
        #                               resized_data.shape[1],
        #                               resized_data.shape[2])).astype(data.dtype)
        # resized_data = np.transpose(resized_data, (1, 2, 0))
        #
        # background_img = resized_data

        if html_name in shift_dict:
            background_img = background_img.transform(background_img.size, Image.AFFINE, shift_dict[html_name])
        # background_img = np.roll(background_img,(10,0,0))
        # xdim, ydim = background_img.shape[0], background_img.shape[1]
        xdim, ydim = background_img.size
        print(xdim, ydim)
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

        p.patches(x_list, y_list, fill_alpha=0, line_alpha=0.5, color='black', line_width=3, hover_line_alpha=0.05)

        ar_viz = True
        if ar_viz:
            ALL_TYPE_LIST = ['Medulla', 'Inner Medulla', 'Cortex', 'Outer Medulla', 'Outer Stripe']
            with open(os.path.join(ar_annotation_folder, annotation_file_name)) as data_file:
                data = json.load(data_file)

            coor_list = []
            type_list = []
            color_list = []
            color_list_2 = []

            for item in data:
                if item["geometry"]["type"] != "MultiPolygon":
                    coor_list.extend(item["geometry"]["coordinates"])
                    type_list.append(item["properties"]["classification"]["name"])
                    color_list.append(
                        f'{"#{:06x}".format(abs(int(item["properties"]["classification"]["colorRGB"])))}')
                    color_list_2.append(Set1_6[ALL_TYPE_LIST.index(type_list[-1].title())])
                else:
                    for polygon in item["geometry"]["coordinates"]:
                        coor_list.extend(polygon)
                        type_list.append(item["properties"]["classification"]["name"])
                        color_list.append(
                            f'{"#{:06x}".format(abs(int(item["properties"]["classification"]["colorRGB"])))}')
                        color_list_2.append(Set1_6[ALL_TYPE_LIST.index(type_list[-1].title())])
            ALL_TYPE_LIST.extend(type_list)
            x_list = [[xy[0] // rescale_index for xy in coor] for coor in coor_list]
            y_list = [[xy[1] // rescale_index for xy in coor] for coor in coor_list]
            for xs, ys, color, legend_title in zip(x_list, y_list, color_list_2, type_list):
                p.patch(xs, ys,
                        fill_alpha=0.5, line_alpha=0.6, color=color, line_width=3,
                        hover_line_alpha=0.05,
                        hover_fill_alpha=0.05,
                        muted_alpha=0,
                        muted=False,
                        legend_label=legend_title, )
            p.legend.location = "top_left"
            p.legend.click_policy = "mute"

        show(p)
        print(f"output html: {html_name}")
