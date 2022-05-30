# import imp
import os
import glob
from pathlib import Path
import subprocess
import tqdm
db = Path("Real_Life_Violence_Dataset/NonViolence/")

non_violence = glob.glob("Real_Life_Violence_Dataset/NonViolence/*")

violence = glob.glob("Real_Life_Violence_Dataset/Violence/*")
hz = 30
out_path = Path("extract_videos")
cmd = f"rm -rf {out_path.as_posix()}/*"
print(cmd)
os.system(cmd)

full_videos = violence + non_violence
print(len(full_videos))
for video in tqdm.tqdm(full_videos):
    # print(1)
    filename = video.split("/")[-1]
    filename = filename.split(".")[0]
    os.mkdir(out_path/filename)
    
    out_name=f"{out_path/filename}/%05d.jpg"
    # print(out_name)
    # break
    cmd = f"ffmpeg -i {video} -r {hz} -q:v 1 {out_name}"
    print(cmd)
    os.system(cmd)
    # break
