from skimage import data
from skimage import transform
from skimage import io
from skimage.exposure import rescale_intensity
from skimage.feature import (match_descriptors, corner_harris,
                             corner_peaks, ORB, plot_matches)
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

src_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\pas\8_thumbnail\VAN0005-RK-4-172-PAS_registered_8.jpg'
dst_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\af\8_thumbnail\VAN0005-RK-4-172-AF_preIMS_registered_8.jpg'

img1 = io.imread(src_path)[1500:2000, 1500:2000]
img2 = io.imread(dst_path)[1500:2000, 1500:2000]

img_orig = rescale_intensity(img1)
img1_gray = rgb2gray(img_orig)

img_warped = rescale_intensity(img2)
img2_gray = rgb2gray(img_warped)

descriptor_extractor = ORB(n_keypoints=50)

descriptor_extractor.detect_and_extract(img1_gray)
keypoints1 = descriptor_extractor.keypoints
descriptors1 = descriptor_extractor.descriptors

descriptor_extractor.detect_and_extract(img2_gray)
keypoints2 = descriptor_extractor.keypoints
descriptors2 = descriptor_extractor.descriptors

matches12 = match_descriptors(descriptors1, descriptors2, cross_check=True)

fig, ax = plt.subplots(nrows=2, ncols=1)

plt.gray()

plot_matches(ax[1], img1, img2, keypoints1, keypoints2, matches12)
ax[1].axis('off')
ax[1].set_title("Original Image vs. Transformed Image")

plot_matches(ax[0], img1, img2, keypoints1, keypoints2, matches12)
ax[0].axis('off')
ax[0].set_title("Original Image vs. Transformed Image")

plt.show()
