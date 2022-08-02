import os

base_folder_path = r"C:\Users\bunny\Desktop\train"
target_folder_path = r"C:\Users\bunny\Desktop\train_raw"

base_file_list = os.listdir(base_folder_path)
target_file_list = os.listdir(target_folder_path)

for file in target_file_list:
    if file not in base_file_list:
        print(os.path.join(target_folder_path, file))
        os.remove(os.path.join(target_folder_path, file))