"""Location for all available function."""

# Todo(C.Feng, 202020515): Use Path from `pathlib.py`(Py36)

import os

LOC = os.getcwd()
if LOC.split("/")[-1] != "MVIMP":
    raise ValueError("Please change directory to the root of MVIMP.")

ANIMEGAN_PREFIX = os.path.join(LOC, "third_party/AnimeGAN")
DAIN_PREFIX = os.path.join(LOC, "third_party/DAIN")
Photo_3D = os.path.join(LOC, "third_party/Photo3D")
DeOldify = os.path.join(LOC, "third_party/DeOldify")
waifu2x_vulkan = os.path.join(LOC, "third_party/waifu2x-ncnn-vulkan")

input_data_dir = os.path.join(LOC, "Data/Input")
output_data_dir = os.path.join(LOC, "Data/Output")
tmp_data_dir = os.path.join(LOC, "Data/Temp")
all_dir_link = [input_data_dir, output_data_dir, tmp_data_dir]
for dir_link in all_dir_link:
    if not os.path.exists(dir_link):
        os.makedirs(dir_link)
