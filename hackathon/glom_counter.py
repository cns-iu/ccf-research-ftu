import cv2
import json
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from tifffile import imread, imwrite, TiffFile

json_filepath = r'X:\hackathon_new\1\annotations\VAN0005-RK-4-172-PAS_registered.ome.json'

if len(sys.argv) >= 2:
    json_filepath = sys.argv[1]

read_file = open(json_filepath, "r")
data = json.load(read_file)

file_name = json_filepath.split('\\')[-1]
print(f'{file_name}\t{len(data)}')
