from functions import *
from lib.InterceptionWrapper import InterceptionMouseState, InterceptionMouseStroke
import cv2
import numpy as np


class Bot:

    def __init__(self, autohot_py):
        self.autohot_py = autohot_py
        self.step = 0
        self.window_info = get_window_info()
        self.useless_steps = 0

    def set_default_camera(self):
        self.autohot_py.PAGE_DOWN.press()
        time.sleep(0.2)
        self.autohot_py.PAGE_DOWN.press()
        time.sleep(0.2)
        self.autohot_py.PAGE_DOWN.press()

    def go_somewhere(self):
        """
        click to go
        """
        self.set_default_camera()
        smooth_move(self.autohot_py, 900, 650)  # @TODO dynamic
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)
        self.set_default_camera()

    def turn(self):
        """
        turn right
        """
        time.sleep(0.02)
        smooth_move(self.autohot_py, 300, 500)  # @TODO dynamic
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        smooth_move(self.autohot_py, 305, 500)  # @TODO dynamic
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_RIGHT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)

    def get_targeted_hp(self):
        """
        return victim's hp
        or -1 if there is no target
        """

        hp_color = [214, 24, 65]
        target_widget_coordinates = {}
        filled_red_pixels = 1

        img = get_screen(
            self.window_info["x"],
            self.window_info["y"],
            self.window_info["x"] + self.window_info["width"],
            self.window_info["y"] + self.window_info["height"] - 300
        )

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        template = cv2.imread('img/target_bar.png', 0)
        # w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        if count_nonzero(loc) == 2:
            for pt in zip(*loc[::-1]):
                target_widget_coordinates = {"x": pt[0], "y": pt[1]}
                # cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 255, 255), 2)

        if not target_widget_coordinates:
            return -1

        pil_image_hp = get_screen(
            self.window_info["x"] + target_widget_coordinates['x'] + 16,
            self.window_info["y"] + target_widget_coordinates['y'] + 31,
            self.window_info["x"] + target_widget_coordinates['x'] + 165,
            self.window_info["y"] + target_widget_coordinates['y'] + 32,
        )

        pixels = pil_image_hp[0].tolist()
        for pixel in pixels:
            if pixel == hp_color:
                filled_red_pixels += 1

        percent = 100 * filled_red_pixels / 150
        return percent

    def set_target(self):
        """
        find target and click
        """
        img = get_screen(
            self.window_info["x"],
            self.window_info["y"] + 50,
            self.window_info["x"] + self.window_info["width"],
            self.window_info["y"] + self.window_info["height"] - 300
        )

        cnts = get_target_centers(img)
        approxes = []
        hulls = []
        for cnt in cnts:
            approxes.append(cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True))
            hulls.append(cv2.convexHull(cnt))
            left = list(cnt[cnt[:, :, 0].argmin()][0])
            right = list(cnt[cnt[:, :, 0].argmax()][0])
            if right[0] - left[0] < 20:
                continue
            center = round((right[0] + left[0]) / 2)
            center = int(center)

            smooth_move(self.autohot_py, center + self.window_info["x"], left[1] + 110 + self.window_info["y"])
            time.sleep(0.1)
            if self.find_from_targeted(left, right):
                self.click_target()
                return True

            # # Slide mouse down to find target
            # iterator = 50
            # while iterator < 220:
            #     time.sleep(0.3)
            #     smooth_move(
            #         self.autohot_py,
            #         center + self.window_info["x"],
            #         left[1] + iterator + self.window_info["y"]
            #     )
            #     if self.find_from_targeted(left, right):
            #         self.click_target()
            #         return True
            #     iterator += 20

        return False

    def find_from_targeted(self, left, right):

        # @TODO ignore red target - it is attacked and dead
        template = cv2.imread('img/template_target.png', 0)

        # print template.shape
        roi = get_screen(
            left[0] - 70 + self.window_info["x"],
            left[1] - 15 + self.window_info["y"] + 50,
            right[0] + 70 + self.window_info["x"],
            right[1] + 12 + self.window_info["y"] + 50
        )

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(roi, 224, 255, cv2.THRESH_TOZERO_INV)
        ret, th2 = cv2.threshold(th1, 135, 255, cv2.THRESH_BINARY)
        ret, tp1 = cv2.threshold(template, 224, 255, cv2.THRESH_TOZERO_INV)
        ret, tp2 = cv2.threshold(tp1, 135, 255, cv2.THRESH_BINARY)
        if not hasattr(th2, 'shape'):
            return False
        wth, hth = th2.shape
        wtp, htp = tp2.shape
        if wth > wtp and hth > htp:
            res = cv2.matchTemplate(th2, tp2, cv2.TM_CCORR_NORMED)
            if res.any():
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > 0.7:
                    return True
                else:
                    return False
        return False

    def click_target(self):
        # time.sleep(0.02)
        stroke = InterceptionMouseStroke()
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_DOWN
        self.autohot_py.sendToDefaultMouse(stroke)
        stroke.state = InterceptionMouseState.INTERCEPTION_MOUSE_LEFT_BUTTON_UP
        self.autohot_py.sendToDefaultMouse(stroke)
