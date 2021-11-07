# pip install opencv-contrib-python==4.4.0.46
# http://wayou.github.io/t-rex-runner/

from pynput.keyboard import Key, Controller

keyboard = Controller()

import cv2
import numpy as np
import time
from mss import mss
from PIL import Image

mon = {'left': 660, 'top': 240, 'width': 660, 'height': 200}

is_release = True
id = 0
time.sleep(5)

with mss() as sct:
    while True:
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )
        id += 1
        image = np.array(img)
        small_image = cv2.imread('./sprites/dino-run.png')
        result = cv2.matchTemplate(small_image, image, cv2.TM_SQDIFF_NORMED)
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        MPx, MPy = mnLoc
        trows, tcols = small_image.shape[:2]
        dino_start = (MPx, MPy)
        dino_end = (MPx + tcols, MPy + trows)
        cv2.rectangle(image, dino_start, dino_end, (0, 0, 255), -1)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph_img = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, kernel)
        (thresh, blackAndWhiteImage) = cv2.threshold(morph_img, 240, 255, cv2.THRESH_BINARY)
        whiteBlack = cv2.bitwise_not(blackAndWhiteImage)
        contours, hierarchy = cv2.findContours(whiteBlack, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]

        dino_threshold = 50
        dino_end = (dino_end[0] + 5, dino_end[1] + 5)

        last_press = 1.0
        time_threshold = 100
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            roi = image[y:y + h, x:x + w]
            if abs(x - dino_end[0]) < dino_threshold and time.time() - last_press > time_threshold and dino_start[1] < y:
                last_press = time.time()
                print(dino_end)
                print(x, y)
                keyboard.press(' ')
            elif y < dino_start[1] and \
                    y < dino_end[1] and \
                    y + h > dino_start[1] and \
                    x > dino_end[0] and \
                    abs(x - dino_end[0]) < w:

                    keyboard.press(Key.down)
                    time.sleep(0.5)
                    keyboard.release(Key.down)
