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
        lower = cv2.inRange(inputImageInHSV, np.array([0, 60, 60]), np.array([20, 255, 255]))
        upper = cv2.inRange(inputImageInHSV, np.array([160, 60, 60]), np.array([179, 255, 255]))
        return cv2.addWeighted(lower, 1.0, upper, 1.0, 0.0)


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
        hsv = cv2.medianBlur(img, 5)
        # converting to HSV color-space
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
        # thresholding blue signs
        hsv = self.redFilter(hsv)
        hsv = cv2.medianBlur(hsv, 5)
        # debug write
        cv2.imwrite(hsvfile, hsv)

        circles = cv2.HoughCircles(hsv, cv2.cv.CV_HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.rectangle(img, (x - 5 - r, y - 5 - r), (x + 5 + r, y + 5 + r), (0, 128, 255), 3)

        cv2.imwrite(outfile, img)
