import cv2
import os
import matplotlib.pyplot as plt
from parse import *

# extracting frames from videos

def extract_frame(folderPath, videoName, subfolder):
    if not os.path.exists(os.path.join(folderPath, subfolder)):
        os.mkdir(os.path.join(folderPath, subfolder))

    vidcap = cv2.VideoCapture(folderPath + '/' + videoName)
    success, image = vidcap.read()
    count = 0

    while success:
        cv2.imwrite(folderPath + "/" + subfolder + "/IMG_%s_%04d.jpg" % (subfolder, count),
                    image)  # save frame as JPEG file
        success, image = vidcap.read()
        # print(count, ': Read a new frame: ', success)

        count += 1

    return "Frames extracted successfully"

# Get bbox for synthetic videos
def get_bb_synthetic(filename):
    x = 0
    y = 0
    hei = 0
    wid = 0
    print('file name : ', filename)

    if not os.path.exists(filename): return x, y, hei, wid
    count = len(open(filename).readlines())
    fp = open(filename, "r")

    for i in range(count):
        line = fp.readline()

    print(line)
    ss = parse("'{}' [{} {} {} {}]", line)
    print(ss)
    y = int(float(ss[1]))  # size_img[0] - int(float(ss[2]))
    x = int(float(ss[2]))
    wid = int(float(ss[3])) - int(float(ss[1]))
    hei = int(float(ss[4])) - int(float(ss[2]))
    # x = x- hei
    return x, y, hei, wid



# get crop from video
def get_crop_from_videos(folderPath):

    images = [i for i in os.listdir(folderPath + "/frame")]

    text_files = [f for f in os.listdir('verify2/SchoolCorridor-video13/')]
    for image in images:
        print(image)
        # image = 'IMG_frame1_0174.jpg'
        txt_file = folderPath+'/' + image.replace('.jpg', '.txt')
        print(txt_file)
        x, y, hei, wid = get_bb_synthetic(txt_file.replace('frame_', 'frame_'))

        I = cv2.imread(folderPath + '/frame/' + image)

        top = abs(y)
        left = abs(x)
        H = left + (hei)
        right = left + H
        W = top + (wid)
        bottom = top + W
        padding = 0

        print(x, y, hei, wid)

        img_rotate = cv2.rotate(I, cv2.ROTATE_90_CLOCKWISE)
        crop = img_rotate[top:bottom, left:right]
        # store crop for further analysis
