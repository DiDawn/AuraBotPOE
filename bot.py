from capture import WindowCapture
from detection import Detection
import cv2
from time import time
from PIL import Image
import os
import time
import ctypes
from threading import Thread


class Params:
    HEALTH = "health"
    SHIELD = "shield"
    VISUAL_ONLY = "visual_only"
    TEXT_ONLY = "text_only"
    ALL = "all"


class Bot:
    def __init__(self, detection_method, classifier_name, scale_factor: int = 3,
                 window_size: tuple[int, int] = (1920, 1080),
                 grayscale: bool = False, debug_mode: str | None = None, bar_priority: str = 'health',
                 health_threshold: int = 0.85, shield_threshold: int = 0.85):
        """
        :param detection_method: Should be 'template' or 'cascade'. Will define the method used to detect the bar.
        :param scale_factor: integer between 1 and 10. Will scale down the image by this factor.
        :param window_size: size of the window to capture. Should be the same as the game window.
        :param grayscale: If True, will convert the image to grayscale before searching for the health bar.
        :param debug_mode: If provided, should be 'visual_only', 'text_only' or 'all'. Will define what is displayed.
        :param bar_priority: Should be 'health' or 'shield'. Will define which one is searched first.
        :param health_threshold: Threshold of confidence for the health bar (only needed for 'template' method).
        :param shield_threshold: Threshold of confidence for the shield bar (only needed for 'template' method).
        """
        self.detection_method = detection_method
        if detection_method != "template" and detection_method != "cascade":
            raise Exception(f"detection_method should be 'template' or 'cascade'. Not: {detection_method}")
        if detection_method == "cascade" and classifier_name is None:
            raise Exception("classifier_name should be provided when using detection_method 'cascade'")

        self.debug_mode = debug_mode
        if debug_mode is not None:
            if debug_mode != Params.VISUAL_ONLY and debug_mode != Params.TEXT_ONLY and debug_mode != Params.ALL:
                raise Exception(f"Debug mode should be 'visual_only', 'text_only' or 'all'. Not: {debug_mode}")

        self.scale_factor = scale_factor
        if not (1 <= self.scale_factor <= 10):
            raise Exception(f"scale factor needs to be between 1 and 10. Current scale factor : {self.scale_factor}")

        self.gray_scale = grayscale

        self.bar_priority = bar_priority
        if self.bar_priority != "health" and self.bar_priority != "shield":
            raise Exception(f"Bar priority should be 'health' or 'shield' not: {bar_priority}")

        self.window_w, self.window_h = window_size
        if "Path of Exile" in WindowCapture.list_window_names():
            self.window_capture = WindowCapture(1920, 1080, "Path of Exile")
        else:
            raise Exception("Path of Exile is not running")

        match debug_mode:
            case Params.TEXT_ONLY:
                self.window_capture.list_window_names()
            case Params.ALL:
                self.window_capture.list_window_names()

        self.health_bar, self.shield_bar = self.load_needle_images()
        self.health_threshold, self.shield_threshold = health_threshold, shield_threshold

        self.detection = Detection(self.detection_method, classifier_name)

        self.running = False

        self.user32 = ctypes.windll.user32

    def load_needle_images(self):
        images = os.listdir('Images/')
        if f"health_bar_d{self.scale_factor}.png" in images:
            health_bar = cv2.imread(f"Images/health_bar_d{self.scale_factor}.png")
        else:
            health_bar = Image.open(f"Images/health_bar.png")
            health_bar.resize((health_bar.width // self.scale_factor, health_bar.height // self.scale_factor))
            health_bar.save(f"Images/health_bar_d{self.scale_factor}.png")
            health_bar = cv2.imread(f"Images/health_bar_d{self.scale_factor}.png")

        if f"shield_bar_d{self.scale_factor}.png" in images:
            shield_bar = cv2.imread(f"Images/health_bar_d{self.scale_factor}.png")
        else:
            shield_bar = Image.open(f"Images/shield_bar.png")
            shield_bar.resize((shield_bar.width // self.scale_factor, shield_bar.height // self.scale_factor))
            shield_bar.save(f"Images/shield_bar_d{self.scale_factor}.png")
            shield_bar = cv2.imread(f"Images/shield_bar_d{self.scale_factor}.png")

        if self.gray_scale:
            health_bar, shield_bar = Detection.convert2grayscale(health_bar), Detection.convert2grayscale(shield_bar)

        return health_bar, shield_bar

    def start(self):
        self.running = True
        self.main_loop()

    def pause(self):
        if self.running:
            self.running = False
            while not self.is_key_pressed(0x50):
                time.sleep(0.1)
        else:
            self.running = True
            self.main_loop()

    def stop(self):
        self.running = False

    def sort_matches(self, matches):
        """
        Sort the matches to be sure that the bot doesn't click on the ATH
        """
        sorted_matches = []
        d = self.scale_factor
        # print(rectangles)
        for rectangle in matches:
            x, y = rectangle[0], rectangle[1]
            if not ((764 // d <= x <= 1159 // d and 20 // d <= y <= 67 // d) or (
                    90 // d <= x <= 238 // d and 235 // d <= y <= 273 // d)):
                sorted_matches.append(rectangle)

        return sorted_matches

    def move_mouse(self, x, y):
        # move to position
        x = int(65536 * x / ctypes.windll.user32.GetSystemMetrics(0) + 1)
        y = int(65536 * y / ctypes.windll.user32.GetSystemMetrics(1) + 1)
        self.user32.mouse_event(0x0001 + 0x8000, x, y, 0, 0)

    def click(self):
        self.user32.mouse_event(0x0002 + 0x0004, 0, 0, 0, 0)

    def move_click(self, x, y):
        self.move_mouse(x, y)
        self.click()

    def hold_click(self):
        self.user32.mouse_event(0x0002, 0, 0, 0, 0)

    def release_click(self):
        self.user32.mouse_event(0x0004, 0, 0, 0, 0)

    def click_loop(self):
        """
        As the game only allow around 10 clicks per second, we need to hold the mouse button for a short time
        to continue moving the character without performing too many clicks.
        """
        while self.running:
            self.click()
            self.hold_click()
            time.sleep(0.5)
            self.release_click()

    def is_key_pressed(self, key: int):
        """
        :param key: vk code of the key as defined here:
         https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        """
        return self.user32.GetAsyncKeyState(key) & 0x8000

    def main_loop(self):
        n_frames = 1
        total_time0 = time()
        template_methode = self.detection_method == "template"
        # start click loop thread
        click_loop_thread = Thread(target=self.click_loop)
        click_loop_thread.start()
        while self.running:

            if self.scale_factor != 1 and template_methode:
                capture = self.window_capture.scaled_capture(self.scale_factor)
            # as the cascade classifier has been trained on non-scaled images, we must not scale the image
            else:
                capture = self.window_capture.capture()

            capture = Detection.convert2non_alpha(capture)
            if self.gray_scale and template_methode:
                capture = Detection.convert2grayscale(capture)

            detection_time0 = time()
            if self.bar_priority == Params.HEALTH:
                matches = self.detection.find(capture, self.health_bar, self.health_threshold)
                if len(matches) == 0:
                    matches = self.detection.find(capture, self.shield_bar, self.shield_threshold, True)

            else:
                matches = self.detection.find(capture, self.shield_bar, self.shield_threshold, True)
                if len(matches) == 0:
                    matches = self.detection.find(capture, self.health_bar, self.health_threshold)
            detection_time1 = time()

            if len(matches) > 0:
                matches = self.sort_matches(matches)

            if len(matches) > 0:
                x, y = matches[0][0], matches[0][1]
                # print(x, y)
                self.move_click(x * self.scale_factor, y * self.scale_factor)

                if self.debug_mode == Params.VISUAL_ONLY or self.debug_mode == Params.ALL:
                    capture = Detection.draw_cross(capture, x, y)

            if self.debug_mode == Params.VISUAL_ONLY or self.debug_mode == Params.ALL:
                capture = Detection.draw_rectangles(capture, matches)
                cv2.imshow('debug_window', capture)
                cv2.waitKey(1)
            if self.debug_mode == Params.TEXT_ONLY or self.debug_mode == Params.ALL:
                elapsed_time = time() - total_time0
                elapsed_detection_time = detection_time1 - detection_time0
                avg_fps = (n_frames / elapsed_time)
                n_frames += 1

                print(f"Fps:{avg_fps} | Total loop time:{elapsed_time}.2f | Detection time:{elapsed_detection_time}")

            if self.is_key_pressed(0x51):
                self.stop()

            if self.is_key_pressed(0x50):
                self.pause()
