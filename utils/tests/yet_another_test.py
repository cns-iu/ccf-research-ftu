import numpy as np
from bioformats import omexml as ome
import tifffile as tf
import sys


def writeplanes(pixel, SizeT=1, SizeZ=1, SizeC=1, order='TZCYX'
                , verbose=False):
    if order == 'TZCYX':

        p.DimensionOrder = ome.DO_XYCZT
        counter = 0
        for t in range(SizeT):
            for z in range(SizeZ):
                for c in range(SizeC):

                    if verbose:
                        print('Write PlaneTable: ', t, z, c),
                        sys.stdout.flush()

                    pixel.Plane(counter).TheT = t
                    pixel.Plane(counter).TheZ = z
                    pixel.Plane(counter).TheC = c
                    counter = counter + 1

    return pixel


# Dimension TZCXY
SizeT = 1
SizeZ = 1
SizeC = 3
SizeX = 300
SizeY = 300
Series = 0

scalex = 0.125
scaley = scalex
scalez = 1
pixeltype = 'uint16'
dimorder = 'TZCYX'
output_file = r'temp/stack.ome.tiff'  # this does nothing in this example

# create numpy array with correct order

# Getting metadata info
omexml = ome.OMEXML()
omexml.image(Series).Name = output_file
p = omexml.image(Series).Pixels
# p.ID = 0
p.SizeX = SizeX
p.SizeY = SizeY
p.SizeC = SizeC
p.SizeT = SizeT
p.SizeZ = SizeZ
p.PhysicalSizeX = np.float(scalex)
p.PhysicalSizeY = np.float(scaley)
p.PhysicalSizeZ = np.float(scalez)
p.PixelType = pixeltype
p.channel_count = SizeC
p.plane_count = SizeZ * SizeT * SizeC
p = writeplanes(p, SizeT=SizeT, SizeZ=SizeZ, SizeC=SizeC, order=dimorder)

for c in range(SizeC):
    if pixeltype == 'unit8':
        p.Channel(c).SamplesPerPixel = 1
    if pixeltype == 'unit16':
        p.Channel(c).SamplesPerPixel = 2

omexml.structured_annotations.add_original_metadata(
    ome.OM_SAMPLES_PER_PIXEL, str(SizeC))

# Converting to omexml
xml = omexml.to_xml()

img5d = np.random.randn(
    SizeT, SizeZ, SizeC, SizeY, SizeX).astype(np.uint16)

# ~ write file and save OME-XML as description
tf.imwrite(r'temp/test1.ome.tiff', img5d  # ,
           , description=xml)

with tf.TiffWriter('temp/test2.ome.tiff'
                   # , bigtiff=True
                   # , imagej=True
                   ) as tif:
    for t in range(SizeT):
        for z in range(SizeZ):
            for c in range(SizeC):
                # ~ print(img5d[t,z,c,:,:].shape)   # -> (2044, 2044)
                tif.save(img5d[t, z, c, :, :]
                         #                     ,shape=res.shape

                         # ,resolution= (.1083,0.1083,3)
                         , description=xml
                         , photometric='minisblack'
                         # , datetime= True
                         , metadata={'axes': 'TZCYX'
                        , 'DimensionOrder': 'TZCYX'
                        , 'Resolution': 0.10833}
                         )

with tf.TiffWriter('temp/test3.ome.tiff'
                   # , bigtiff=True
                   # , imagej=True
                   ) as tif:
    for t in range(SizeT):
        # ~ print(img5d[t,z,c,:,:].shape)   # -> (2044, 2044)
        tif.save(img5d[t, :, :, :, :]
                 #                     ,shape=res.shape

                 # ,resolution= (.1083,0.1083,3)
                 , description=xml
                 , photometric='minisblack'
                 # , datetime= True
                 , metadata={'axes': 'TZCYX'
                , 'DimensionOrder': 'TZCYX'
                , 'Resolution': 0.10833}
                 )

with tf.TiffWriter('temp/test4.ome.tiff'
                   # , bigtiff=True
        , imagej=True
                   ) as tif:
    for t in range(SizeT):
        # ~ print(img5d[t,z,c,:,:].shape)   # -> (2044, 2044)
        tif.save(img5d[t, :, :, :, :]
                 #                     ,shape=res.shape

                 # ,resolution= (.1083,0.1083,3)
                 , description=xml
                 , photometric='minisblack'
                 # , datetime= True
                 , metadata={'axes': 'TZCYX'
                , 'DimensionOrder': 'TZCYX'
                , 'Resolution': 0.10833}
                 )
