import os

vipshome = r'C:\Users\bunny\Desktop\vips-dev-8.10\bin'
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']

import pyvips

image_path = rf'X:\segmentation_mask_stitched.ome.tiff'
# image_path = rf'G:\HuBMAP\Vanderbilt TMC\2020 Release Data\DR_reformat\VAN0005-RK-4-172\VAN0005-RK-4-172-AF\processedMicroscopy\VAN0005-RK-4-172-AF_preIMS_images\VAN0005-RK-4-172-AF_preIMS_registered.ome.tiff'

whole_image = pyvips.Image.new_from_file(image_path, access='sequential')
print(whole_image.get_fields())
print([whole_image.get(field) for field in whole_image.get_fields()[:13]])
page_count = whole_image.get('n-pages')

images = []
for i in range(page_count):
    image = pyvips.Image.new_from_file(rf'{image_path}[page={i}]', access='sequential', )
    # image = image.shrink(8, 8)
    # image = image.copy(xres=image.xres / 8, yres=image.yres / 8)
    print(f"writing tif layer {i}...")
    # image.set_type(pyvips.GValue.gint_type, "page-height", 3)
    image.write_to_file(rf'temp/layer_{i}.tiff')
    # images.append(image)
for i in range(page_count):
    image = pyvips.Image.new_from_file(rf'temp/layer_{i}.tiff', access='sequential', )
    image = image.shrink(8, 8)
    # image = image.copy(xres=image.xres / 8, yres=image.yres / 8)
    # images.append(image)
    image.write_to_file(rf'temp/layer_{i}_8.tiff')
# for i in range(1, 4):
#     temp = images[:]
#     out = pyvips.Image.arrayjoin(temp, across=i)
#     out.set_type(pyvips.GValue.gint_type, "page-height", 3)
#     print("writing tif ...")
#     out.write_to_file(rf'C:\Users\bunny\Desktop\test_{i}.tiff')


# out = pyvips.Image.arrayjoin(images, across=1)
# out.set_type(pyvips.GValue.gint_type, "page-height", 3)
# print(out.get_fields())
# print([out.get(field) for field in out.get_fields()[:13]])
# print("writing tif ...")
# out.write_to_file(rf'C:\Users\bunny\Desktop\test.ome.tiff')
