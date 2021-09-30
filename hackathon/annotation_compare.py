import json
from re import split
import shutil
import os
import sys
from shapely.geometry import Polygon


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)


def dice(a, b):
    # print(a.intersection(b).area)
    return a.intersection(b).area / a.union(b).area


if __name__ == '__main__':
    file_A_path = r'C:\Users\yiju\Desktop\Copy\Scripts\masks\1-tom-mask\pred_2ec3f1bb9.json'
    file_B_path = r'C:\Users\yiju\Desktop\Copy\Scripts\masks\1-tom-mask\gt_2ec3f1bb9.json'

    if len(sys.argv) >= 3:
        file_A_path = sys.argv[1]
        file_B_path = sys.argv[2]

    A_name = file_A_path.split('\\')[-1].split('.')[0]
    B_name = file_B_path.split('\\')[-1].split('.')[0]

    # A - new json
    with open(file_A_path) as data_file:
        data = json.load(data_file)

    coor_list_a = []

    for item in data:
        coor_list_a.extend(item["geometry"]["coordinates"])
    A_x_list = [[xy[0] for xy in coor] for coor in coor_list_a]
    A_y_list = [[xy[1] for xy in coor] for coor in coor_list_a]
    A_id_list = [i for i in range(len(coor_list_a))]

    # B - old json
    with open(file_B_path) as data_file:
        data = json.load(data_file)

    coor_list_b = []

    for item in data:
        coor_list_b.extend(item["geometry"]["coordinates"])
    B_x_list = [[xy[0] for xy in coor] for coor in coor_list_b]
    B_y_list = [[xy[1] for xy in coor] for coor in coor_list_b]

    # find difference
    center_list_new = []
    for i in range(len(A_x_list)):
        mean_x = (sum(A_x_list[i]) - A_x_list[i][-1]) / (len(A_x_list[i]) - 1)
        mean_y = (sum(A_y_list[i]) - A_y_list[i][-1]) / (len(A_y_list[i]) - 1)
        center_list_new.append((mean_x, mean_y))

    center_list_old = []
    for i in range(len(B_x_list)):
        mean_x = (sum(B_x_list[i]) - B_x_list[i][-1]) / (len(B_x_list[i]) - 1)
        mean_y = (sum(B_y_list[i]) - B_y_list[i][-1]) / (len(B_y_list[i]) - 1)
        center_list_old.append((mean_x, mean_y))

    new_added_list = []
    new_same_list = []
    new_revised_list = []
    op_list = []

    positon_threshold = 500
    dice_threshold = 0.8

    average_area = sum([Polygon(coor_list_a[i]).area for i in A_id_list]) / len(coor_list_a)
    print("average area size: ", average_area)

    ignore_count = 0
    for i in A_id_list:
        x, y = center_list_new[i]
        new_p = Polygon(coor_list_a[i])
        if new_p.area < average_area / 50:
            print("ignore", new_p.area)
            ignore_count += 1
            continue
        min_f1 = 0
        min_j = -1
        for j in range(len(center_list_old)):
            _x, _y = center_list_old[j]
            old_p = Polygon(coor_list_b[j])
            if (x - _x) ** 2 + (y - _y) ** 2 <= positon_threshold ** 2:
                f1 = dice(new_p, old_p)
                if f1 > min_f1:
                    min_f1 = f1
                    min_j = j
        if min_f1 > 0.999:
            _flag = f"Same\t{min_f1}"
            new_same_list.append(i)
        elif min_f1 > dice_threshold:
            _flag = f"Revised\t{min_f1}"
            new_revised_list.append(i)
        else:
            _flag = f"Added\t{min_f1}"
            new_added_list.append(i)
            # print(min_f1)
        if _flag.startswith("Same") or _flag.startswith("Revised"):
            if min_j != -1:
                coor_list_b.pop(min_j)
                center_list_old.pop(min_j)
        # print(i, _flag)

    removed_count = len(center_list_old)
    print(f"{A_name}\t{B_name}\tsame\trevised\tadded\tdeleted")
    print(f"{len(A_x_list)- ignore_count}\t{len(B_x_list)}\t{len(new_same_list)}\t{len(new_revised_list)}"
          f"\t{len(new_added_list)}\t{removed_count}")
    print(f"[{len(new_added_list)}/{len(A_x_list) - ignore_count}]")
    # print(f"{len(new_same_list)} same")
    # print(f"{len(new_revised_list)} revised")
    # print(f"{len(new_added_list)} added")
    # print(f"{removed_count} deleted")
