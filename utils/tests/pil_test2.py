from __future__ import print_function  # Python 2/3 compatibility
import glob
from PIL import Image
import tifffile
import numpy

Image.MAX_IMAGE_PIXELS = None


def PIL2array(img):
    """ Convert a PIL/Pillow image to a numpy array """
    return numpy.array(img.getdata(),
                       numpy.uint16).reshape(1, img.size_index[1], img.size_index[0], 1)


FRAMES = []  # Empty list of frames
FIRST_SIZE = None  # I am going to say that the first file is the right size
OUT_NAME = "test.tiff"  # Name to save to
filelist = glob.glob(
    "temp/*.tiff")  # For this test I am just using the images in the current directory in the order they are
# Get the images into an array
for fn in filelist:  # For each name in the list
    img = Image.open(fn)  # Read the image
    if FIRST_SIZE is None:  # Don't have a size
        FIRST_SIZE = img.size_index  # So use this one
    if img.size_index == FIRST_SIZE:  # Check the current image size if it is OK we can use it
        print("Adding:", fn)  # Show some progress
        FRAMES.append(img)  # Add it to our frames list
    else:
        print("Discard:", fn, img.size_index, "<>", FIRST_SIZE)  # You could resize and append here!

print("Writing", len(FRAMES), "frames to", OUT_NAME)
with tifffile.TiffWriter(OUT_NAME) as tiff:
    for img in FRAMES:
        tiff.save(PIL2array(img))
print("Done")
