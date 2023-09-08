import cv2
import numpy as np


class Detection:
    def __init__(self):
        pass

    @staticmethod
    def find(haystack_img, needle_img, threshold: float):
        if not 0 < threshold <= 1:
            raise Exception(f'threshold:{threshold} should be between 0 and 1')

        # run the OpenCV algorithm
        match_template_result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_CCOEFF_NORMED)

        # threshold of confidence
        locations = np.where(match_template_result >= threshold)

        # we can zip those into positions tuples to get the result like : [(x0,y0),(x1,y1), ..., (xn,yn)]
        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # first we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            shape = np.shape(needle_img)
            rect = [int(loc[0]), int(loc[1]), shape[0], shape[1]]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)

        return rectangles

    @staticmethod
    def draw_rectangles(haystack_img, rectangles, rectangle_color=(0, 255, 0)):

        line_type = cv2.LINE_4
        haystack_image_copy = haystack_img.copy()

        for (x, y, h, w) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(haystack_image_copy, top_left, bottom_right, rectangle_color, line_type)

        return haystack_image_copy

    @staticmethod
    def draw_cross(haystack_img, x, y, cross_color=(255, 0, 0)):
        line_type = cv2.LINE_4
        haystack_image_copy = haystack_img.copy()
        cv2.line(haystack_image_copy, (x - 25, y - 25), (x + 25, y + 25), cross_color, line_type)
        cv2.line(haystack_image_copy, (x + 25, y - 25), (x - 25, y + 25), cross_color, line_type)

        return haystack_image_copy

    @staticmethod
    def convert2non_alpha(img):
        return img[..., :3]

    @staticmethod
    def convert2grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
