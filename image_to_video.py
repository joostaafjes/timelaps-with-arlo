import os
import time
import cv2
import numpy as np
import copy

from PIL import ImageDraw, ImageFont
# from keras.preprocessing.image import load_img
from pathlib2 import Path
import datetime
import glob
import itertools

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

ext = '.avi'
img_width = None
img_height = None

topdir = 'timelaps/AchterInTuin/'
# topdir = 'timelaps/muis/'
# hour = 9

if False:
    min_date = datetime.datetime(2018, 11, 2)
    max_date = datetime.datetime.now()
    # min_date = datetime.datetime(2019, 3, 27)
    # max_date = datetime.datetime(2019, 5, 31)
    img_height = 1072
    img_width = 1920
    layers = 3
else:
    #
    # determine min and max date
    #
    min_date = "99999999"
    max_date = "00000000"
    for hour in range(24):

        # dir = topdir + '/' + str(hour) + '/'
        dir = "{0}{1:02d}/".format(topdir, hour)
        for root, dirs, files in os.walk(dir):
            for filename in files:
                if filename.startswith('.DS_Store'):
                    continue

                date_part = filename[0:8]
                if date_part > max_date:
                    max_date = date_part
                if date_part < min_date:
                    min_date = date_part

                image = cv2.imread(dir + filename)
                new_img_height, new_img_width, new_layers = image.shape
                if img_height and img_width and (img_height != new_img_height or img_width != new_img_width or layers != new_layers):
                    raise Exception('Wrong images size ({}x{}x{}) for file {}'.format(new_img_width, new_img_height, new_layers, filename))
                img_height = new_img_height
                img_width = new_img_width
                layers = new_layers
                size = (img_width, img_height)

    # convert to datetime
    min_date = datetime.datetime(int(min_date[0:4]), int(min_date[4:6]), int(min_date[6:8]))
    max_date = datetime.datetime(int(max_date[0:4]), int(max_date[4:6]), int(max_date[6:8]))

print(img_height, img_width, layers)
print("min date {} - max date {} - diff days {}".format(min_date, max_date, max_date - min_date))

# margin
m_x = 10
m_y = 10
matrix_height = 4
matrix_width = 6

crop_factor = 1
fps = 10
reduced_img_width = int(crop_factor * img_width)
reduced_img_height =  int(crop_factor * img_height)
print('video size after crop: {}x{} (wxh)'.format(reduced_img_width, reduced_img_height))
out = cv2.VideoWriter(topdir + 'timelaps_{}fps'.format(fps) + ext,
                      cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      # cv2.VideoWriter_fourcc(*'DIVX'),
                      fps,
                      (reduced_img_width, reduced_img_height))


count = 0
imgmatrix = np.zeros((img_height * matrix_height + m_y * (matrix_height - 1),
                      img_width * matrix_width + m_x * (matrix_width - 1),
                      layers),
                     np.uint8)
imgmatrix.fill(255)

# loop through all dates
for day, date in [(x, min_date + datetime.timedelta(days=x)) for x in range((max_date - min_date).days + 1)]:
    print('day {} - date {}'.format(day, date))

    # images = []
    # loop through all hour
    # for hour in range(24):
    for hour in range(14, 15):
        filename = "{0}{1:02d}/{2}{3:02d}{4:02d}*".format(topdir, hour, date.year, date.month, date.day)
        # print(filename)
        expanded_filename = glob.glob(filename)
        if len(expanded_filename) == 0:
            # print('not found...skip')
            pass
        elif len(expanded_filename) > 1:
            print('too many...skip')
        else:
            image = cv2.imread(expanded_filename[0])

            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 150)
            fontScale = 2
            fontColor = (255, 255, 255)
            lineType = 2

            image_copy = cv2.resize(image, (reduced_img_width, reduced_img_height))
            cv2.putText(image_copy, date.strftime("%Y-%m-%d") + " - day {}".format(day),
                        bottomLeftCornerOfText,
                        font,
                        fontScale,
                        fontColor,
                        lineType)

            ret = out.write(np.array(image_copy))  #write frame to the output video
            # print('output write {}'.format(ret))
        # count += 20
        # if (count > 2):
        #    break


out.release()
