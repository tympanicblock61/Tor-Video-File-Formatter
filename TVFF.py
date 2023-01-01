import random
import string
import cv2
import os
import datetime
import numpy as np


def torVideoFormat(video_file: string, website:string, nameType:string):
    file_metadata = os.stat(video_file)
    creation_time = datetime.datetime.fromtimestamp(file_metadata.st_ctime)
    video = cv2.VideoCapture(video_file)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = total_frames // 6
    frame_image = None
    rows_image = None

    for i in range(1, 7):
        video.set(cv2.CAP_PROP_POS_FRAMES, (i - 1) * frame_interval)
        success, frame = video.read()
        frame_rate = video.get(cv2.CAP_PROP_FPS)

        if frame_rate == 0:
            frame_rate = 30

        timestamp = creation_time + datetime.timedelta(seconds=i * frame_interval / frame_rate)
        elapsed_time = timestamp - creation_time
        elapsed_hours, remainder = divmod(elapsed_time.seconds, 3600)
        elapsed_minutes, elapsed_seconds = divmod(remainder, 60)
        elapsed_time_str = f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}"
        cv2.putText(frame, elapsed_time_str, (frame.shape[1] - 320, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        
        if frame_image is None:
            frame_image = frame
        else:
            frame_image = cv2.hconcat([frame_image, frame])

        if i % 3 == 0:
            row_image = frame_image
            frame_image = None
            
            if rows_image is None:
                rows_image = row_image
            else:
                rows_image = cv2.vconcat([rows_image, row_image])

    video.release()
    video_size = file_metadata.st_size
    video_length = (total_frames / frame_rate) * 1000
    image = np.zeros((200, rows_image.shape[1], rows_image.shape[2]), dtype=rows_image.dtype)
    cv2.putText(image, f"Video name: {video_file}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(image, f"Video size: {video_size} bytes", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(image, f"Video length: {video_length:.2f} Ms", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    creation_time_str = creation_time.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(image, f"Creation time: {creation_time_str}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(image, f"From: {website}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
    result_image = cv2.vconcat([image, rows_image])

    if nameType.lower() == "false":
        filename, extension = os.path.splitext(video_file)
    else:
        filename = random.sample(string.ascii_letters + string.digits, random.randint(5, 15))

    cv2.imwrite(f"{filename}.png", result_image)
    return f"{filename}.png"

print("welcome to the Tor Video File Formatter or TVFF")
while True:
    video_file = input("video file: ")
    website = input("website url: ")
    nameType = input("random name (true/false): ")
    torVideoFormat(video_file, website, nameType)
