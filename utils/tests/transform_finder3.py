# import cv2
# import numpy as np
# import matplotlib.pyplot  as plt
#
# src_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\pas\8_thumbnail\VAN0005-RK-4-172-PAS_registered_8.jpg'
# dst_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\af\8_thumbnail\VAN0005-RK-4-172-AF_preIMS_registered_8.jpg'
#
# # img1 = io.imread(src_path)[1500:2000, 1500:2000]
# img = cv2.imread(src_path)[400:1400, 1000:2000]
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# sift = cv2.xfeatures2d.SIFT_create()  # .SIFT()
# # kp = sift.detect(gray, None)
# kp, des = sift.detectAndCompute(gray, None)
#
# # img = cv2.drawKeypoints(gray, kp)
# cv2.drawKeypoints(gray, kp, img, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#
# cv2.imwrite('sift_keypoints.jpg', img)
#
# fig, ax = plt.subplots()
# im = ax.imshow(img)
#
# fig.show()

##################################################

import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

src_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\pas\8_thumbnail\VAN0005-RK-4-172-PAS_registered_8.jpg'
dst_path = r'G:\HuBMAP\Vanderbilt TMC\rescaled\af\8_thumbnail\VAN0005-RK-4-172-AF_preIMS_registered_8.jpg'

img1 = cv2.imread(src_path, 0)  [:2000, :2000]  # queryImage
img2 = cv2.imread(dst_path, 0)  [:2000, :2000]  # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()  # .SIFT()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

else:
    print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                   singlePointColor=None,
                   matchesMask=matchesMask,  # draw only inliers
                   flags=2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

plt.imshow(img3, 'gray'), plt.show()
