import cv2 as cv2
import numpy as np

__author__ = 'konst'


class Screen(object):
    # HSV Thresholds
    # Hmin, Smin, Vmin, Vmax
    hsvRedMin = np.array([15, 70, 50])
    hsvRedMax = np.array([227, 255, 255])

    hsvGreenMin = np.array([31, 132, 84])
    hsvGreenMax = np.array([48, 255, 255])

    hsvYellowMin = np.array([25, 97, 100])
    hsvYellowMax = np.array([47, 255, 255])

    hsvBlueMin = np.array([137, 110, 138])
    hsvBlueMax = np.array([227, 255, 255])

    def shapeFilter(self, inputImageInHSV):
        shapeFilterDown = np.array([15,70,50])
        shapeFilterUp = np.array([227,255,255])
        return cv2.inRange(inputImageInHSV, shapeFilterDown, shapeFilterUp)

    def redFilter(self, inputImageInHSV):
        redFilterDown = np.array([0,70,50])
        redFilterUp = np.array([50,255,255])
        return cv2.inRange(inputImageInHSV,redFilterDown,redFilterUp)

    def blueFilter(self, inputImageInHSV):
        blueFilterDown = np.array([50,50,50])
        blueFilterUp = np.array([120,255,255])
        return cv2.inRange(inputImageInHSV, blueFilterDown, blueFilterUp)

    def yellowFilter(self, inputImageInHSV):
        yellowFilterDown = np.array([25,50,50])
        yellowFilterUp = np.array([35,255,255])
        return cv2.inRange(inputImageInHSV, yellowFilterDown, yellowFilterUp)

    def __init__(self, fname, screen_name, out_dir="out", out_format="png"):
        self.fname = fname
        self.screen_name = screen_name
        self.out_format = out_format
        self.out_dir = out_dir
        outfile = self.out_dir + '/' + self.screen_name + "." + self.out_format
        hsvfile = self.out_dir + '/' + self.screen_name + ".hsv." + self.out_format
        edgefile = self.out_dir + '/' + self.screen_name + ".edg." + self.out_format

        img = cv2.imread(fname)

        # converting to HSV color-space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # thresholding blue signs
        hsv = self.redFilter(hsv)
        # debug write
        cv2.imwrite(hsvfile, hsv)

        # contour detection
        edgeImg = cv2.Canny(hsv, 0, 200)
        cv2.imwrite(edgefile, edgeImg)

        contours, _ = cv2.findContours(hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        drawing = np.zeros(img.shape)
        for i in xrange(len(contours)):
            if cv2.contourArea(contours[i]) < 5000:  # just a condition
                cv2.drawContours(drawing, contours, i, (255, 0, 255), 1, 8)

        cv2.imwrite(outfile, drawing)
