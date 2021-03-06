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
        lower = cv2.inRange(inputImageInHSV, np.array([0, 110, 110]), np.array([15, 255, 255]))
        upper = cv2.inRange(inputImageInHSV, np.array([165, 110, 110]), np.array([179, 255, 255]))
        return cv2.addWeighted(lower, 1.0, upper, 1.0, 0.0)


    def blueFilter(self, inputImageInHSV):
        blueFilterDown = np.array([50,50,50])
        blueFilterUp = np.array([120,255,255])
        return cv2.inRange(inputImageInHSV, blueFilterDown, blueFilterUp)

    def yellowFilter(self, inputImageInHSV):
        yellowFilterDown = np.array([25,50,50])
        yellowFilterUp = np.array([35,255,255])
        return cv2.inRange(inputImageInHSV, yellowFilterDown, yellowFilterUp)

    def gamma_correction(self, img, correction):
        img = img/255.0
        img = cv2.pow(img, correction)
        return np.uint8(img*255)

    def _do_hsv(self, img):
        # converting to HSV color-space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # thresholding red sign
        hsv = self.redFilter(hsv)
        hsv = cv2.medianBlur(hsv, 5)
        hsv = cv2.Canny(hsv, 5, 70)
        # debug write
        cv2.imwrite(self.hsvfile, hsv)

        circles = cv2.HoughCircles(hsv, cv2.cv.CV_HOUGH_GRADIENT, 1, 35, minRadius=10, maxRadius=150, param1=100, param2=30)

        rect_offset = 3
        rect_width = 2
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.rectangle(img, (x - rect_offset - r, y - rect_offset - r), (x + rect_offset + r, y + rect_offset + r), (0, 128, 255), rect_width)

        cv2.imwrite(self.outfile, img)

    def _do_bgr(self, img):
        r_thresh = 50

    def _shape_detection(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kern)
        gray = cv2.Canny(gray, 50, 200)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cont_img = np.zeros(gray.shape, np.uint8)
        for cnt in contours:
            # debug output
            # cv2.drawContours(cont_img, contours, i, (255, 0, 255), 1, 8)
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if approx.size == 3:
                cv2.polylines(cont_img, approx, True, (255, 0, 255), 1)
        # debug write
        cv2.imwrite(self.edgefile, cont_img)


        # filtering lines
        # lines = cv2.HoughLinesP(cont_img, 2, 3*np.pi / 180, 5, minLineLength=30, maxLineGap=10)
        # if not lines is None:
        #     # const: uncomment for debug
        #     for x1, y1, x2, y2 in lines[0]:
        #         cv2.line(img, (x1, y1), (x2, y2), (255, 255, 0, 0), 1)
        #     cv2.imwrite(self.gamfile, img)

    def __init__(self, fname, screen_name, out_dir="out", out_format="png"):
        self.fname = fname
        self.screen_name = screen_name
        self.out_format = out_format
        self.out_dir = out_dir
        self.outfile = self.out_dir + '/' + self.screen_name + "." + self.out_format
        self.edgefile = self.out_dir + '/' + self.screen_name + ".edg." + self.out_format
        self.gamfile = self.out_dir + '/' + self.screen_name + ".gam." + self.out_format
        self.hsvfile = self.out_dir + '/' + self.screen_name + ".hsv." + self.out_format

        img = cv2.imread(fname)
        img = self.gamma_correction(img, 0.7)
        # debug write
        cv2.imwrite(self.gamfile, img)

        img = cv2.medianBlur(img, 5)
        #self._do_hsv(img)
        self._shape_detection(img)
