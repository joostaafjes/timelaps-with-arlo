import os
import time
import cv2
import numpy as np

from PIL import ImageDraw, ImageFont
# from keras.preprocessing.image import load_img
from pathlib2 import Path

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

ext = '.avi'
width = None
height = None

# topdir = 'timelaps/AchterInTuin/'
topdir = 'timelaps/muis/'
# hour = 9
for hour in range(24):

    img_array = []

    # dir = topdir + '/' + str(hour) + '/'
    dir = "{0}{1:02d}/".format(topdir, hour)
    print(dir)
    print('current dir:', os.curdir)
    for root, dirs, files in os.walk(dir):
        print(root)
        files.sort()
        for filename in files:
            if filename.startswith('.DS_Store'):
                continue

            image = cv2.imread(dir + filename)
            height, width, layers = image.shape
            size = (width, height)

            img_array.append(image)

    if len(img_array) > 0:
        print(width, height)
        out = cv2.VideoWriter(topdir + 'timelaps_{0:02d}'.format(hour) + ext,
                              cv2.VideoWriter_fourcc('M','J','P','G'),
                              10,
                              (width, height))

        for img in img_array:
            out.write(np.array(img))  #write frame to the output video

        out.release()
    else:
        print('no files found')


