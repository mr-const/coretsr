import cv2 as cv2
import numpy as np

__author__ = 'konst'


class Screen(object):
    def __init__(self, fname, screen_name, out_dir="out", out_format="png"):
        self.fname = fname
        self.screen_name = screen_name
        self.out_format = out_format
        self.out_dir = out_dir
        outfile = self.out_dir + '/' + self.screen_name + "." + self.out_format

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(outfile, gray)

        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        drawing = np.zeros(img.shape)
        for i in xrange(len(contours)):
            if cv2.contourArea(contours[i]) > 15000:  # just a condition
                cv2.drawContours(drawing, contours, i, (255, 0, 255), 1, 8)

