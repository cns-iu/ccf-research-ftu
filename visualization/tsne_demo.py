import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE
from skimage import io
import os

# data reading
root_path = r'X:\temp\vessel/'
test_path = r"VESSEL_TEST\IMAGES"
train_path = r"VESSEL_TRAIN\IMAGES"

test_file_name_list = [file_name for file_name in os.listdir(os.path.join(root_path, test_path))]
train_file_name_list = [file_name for file_name in os.listdir(os.path.join(root_path, train_path))]

test_image_features = [io.imread(os.path.join(root_path, test_path, img_name)) for img_name in test_file_name_list]
train_image_features = [io.imread(os.path.join(root_path, train_path, img_name)) for img_name in train_file_name_list]

# tsne
tsne = TSNE(n_components=2, init='random', random_state=42)
X_ori = np.asarray(test_image_features + train_image_features)
X_ori = X_ori.reshape(X_ori.shape[0], -1)
X_tsne = tsne.fit_transform(X_ori)

print(X_tsne.shape)
print("After {} iter: Org data dimension is {}. Embedded data dimension is {}".format(tsne.n_iter, X_ori.shape[-1],
                                                                                      X_tsne.shape[-1]))

test_tsne = X_tsne[:len(test_file_name_list)]
train_tsne = X_tsne[len(test_file_name_list):]

# visualization
fig, ax = plt.subplots()
ax.scatter([point[0] for point in test_tsne], [point[1] for point in test_tsne], c="blue", label="Test", alpha=0.5,
           edgecolors='none')
ax.scatter([point[0] for point in train_tsne], [point[1] for point in train_tsne], c="red", label="Train", alpha=0.5,
           edgecolors='none')
ax.legend()
ax.grid(False)
plt.show()
