import warnings
import cv2
import os
from TVFF import torVideoFormat

warnings.filterwarnings("ignore")


def isVidFile(file):
    try:
        video = cv2.VideoCapture(file)
        if video.isOpened():
            video.release()
            return True
        else:
            video.release()
            return False
    except:
        return False

    
for file in os.listdir():
    if os.path.isfile(file):
        if isVidFile(file):
            got = torVideoFormat(file, "None", "true", output_dir="pngs")
            if got['code'] == -1:
                print(f"{file}:-:{got['path']}")
                exit()
            else:
                print(f"couldnt make png for {file}")
