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


# Parsing the bbox file and get the text crop from the videos

def get_bb(filename):
    x = 0
    y = 0
    hei = 0
    wid = 0
    # print(filename.replace('.jpg','.txt'))


    if not os.path.exists(filename): return x, y, hei, wid
    count = len(open(filename).readlines())
    fp = open(filename, "r")
    for i in range(count):
        line = fp.readline()
    ss = parse("'{}'  [{},{},{},{}]", line)
    # ss = parse("'{}' [{} {} {} {}]", line)

    if ss == None: return 0, 0, 0, 0
    y = int(float(ss[1]))  # size_img[0] - int(float(ss[2]))
    x = int(float(ss[2]))
    wid = int(float(ss[3])) - int(float(ss[1]))
    hei = int(float(ss[4])) - int(float(ss[2]))
    # x = x- hei
    return x, y, hei, wid

# retrieving and storing text crops

def extract_bg_crop(folderPath):
    images = [i for i in os.listdir(folderPath + "/frame")]

    for image in images:
        print(image)
        txt_file = folderPath+'/' + image.replace('.jpg', '.txt')
        x, y, hei, wid = get_bb(txt_file)
        img_name = folderPath + '/frame/' + image
        I = cv2.imread(img_name, cv2.COLOR_BGR2RGB)
        crop = I[x:x + hei, y:y + wid]

        ## store the crop for further analysis