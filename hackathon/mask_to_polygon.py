import imageio
import json
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import copy

# read mask image
image_path = r'x:\mask_0.png'
img = imageio.imread(image_path)
if len(img.shape) == 2:
    mask = img
else:
    mask = np.array(img[:, :, 0])
mask = np.where(mask > 127, 1, 0)

# get the contour
contours = measure.find_contours(mask, 0.8)

# contour to polygon
polygons = []
for object in contours:
    coords = []
    for point in object:
        coords.append([int(point[0]), int(point[1])])
    polygons.append(coords)
print(polygons)

# save as json
geojson_dict_template = {
    "type": "Feature",
    "id": "PathAnnotationObject",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
        ]
    },
    "properties": {
        "classification": {
            "name": "glomerulus",
            "colorRGB": -3140401
        },
        "isLocked": True,
        "measurements": []
    }
}
geojson_list = []
for polygon in polygons:
    geojson_dict = copy.deepcopy(geojson_dict_template)
    geojson_dict["geometry"]["coordinates"].append(polygon)
    geojson_list.append(geojson_dict)
json_path = image_path.replace('png', 'json')
with open(json_path, 'w') as fp:
    json.dump(geojson_list, fp, indent=2)

# polygon preview
new_img = np.zeros((mask.shape[0], mask.shape[1]))
for polygon in polygons:
    for point in polygon:
        new_img[int(point[0]), int(point[1])] = 1
plt.imshow(new_img)
# plt.imsave(r'x:\mask_88.png', new_img)
plt.show()
