import cv2
import numpy as np


class Detection:
    def __init__(self, detection_method, classifier_name: str = None):
        self.detection_method = detection_method
        if self.detection_method == "cascade":
            self.classifier = cv2.CascadeClassifier(classifier_name)

    def find(self, haystack_img, needle_img, threshold: float, force_template: bool = False):
        if not 0 < threshold <= 1:
            raise Exception(f'threshold:{threshold} should be between 0 and 1')

        if self.detection_method == "template":
            return self.find_template(haystack_img, needle_img, threshold)

        elif self.detection_method == "cascade" and not force_template:
            return self.find_cascade(haystack_img)

        else:
            return self.find_template(haystack_img, needle_img, threshold)

    @staticmethod
    def find_template(haystack_img, needle_img, threshold: float):
        match_template_result = cv2.matchTemplate(haystack_img, needle_img, cv2.TM_CCOEFF_NORMED)

        locations = np.where(match_template_result >= threshold)

        locations = list(zip(*locations[::-1]))

        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            shape = np.shape(needle_img)
            rect = [int(loc[0]), int(loc[1]), shape[0], shape[1]]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)

        return rectangles

    def find_cascade(self, haystack_img):
        rectangles = self.classifier.detectMultiScale(haystack_img, scaleFactor=1.1, minNeighbors=3)
        if len(rectangles) == 0:
            return np.array([], dtype=np.int32).reshape(0, 4)
        return rectangles

    @staticmethod
    def draw_rectangles(haystack_img, rectangles, rectangle_color=(0, 255, 0)):

        line_type = cv2.LINE_4
        haystack_image_copy = haystack_img.copy()

        for (x, y, h, w) in rectangles:
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
