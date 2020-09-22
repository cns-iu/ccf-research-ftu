from PIL import Image
from PIL import ImageSequence
from PIL import TiffImagePlugin

Image.MAX_IMAGE_PIXELS = None
INFILE  = rf'C:\Users\bunny\Desktop\VAN0005-RK-1-1-AF_preIMS_registered.ome1.ome.tiff'
OUTFILE = rf'C:\Users\bunny\Desktop\test.ome.tiff'

print ('Resizing TIF pages')
pages = []
imagehandler = Image.open(INFILE)
for page in ImageSequence.Iterator(imagehandler):
    # page = page.rotate(90, expand=True)
    new_size = (page.size_index[0] // 8, page.size_index[1] // 8)
    page = page.resize(new_size)
    pages.append(page)

print ('Writing multipage TIF')
with TiffImagePlugin.AppendingTiffWriter(OUTFILE) as tf:
    for page in pages:
        page.save(tf)
        # tf.newFrame()