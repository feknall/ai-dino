# pip install opencv-contrib-python==4.4.0.46
# http://wayou.github.io/t-rex-runner/
from pynput.keyboard import Key, Controller

keyboard = Controller()

import random

import cv2
import numpy as np
import time
from mss import mss
from PIL import Image

mon = {'left': 660, 'top': 200, 'width': 660, 'height': 200}

is_release = True
# with mss() as sct:
# while True:
#     time.sleep(1)
# print(pyautogui.position())
# screenShot = sct.grab(mon)
# img = Image.frombytes(
#     'RGB',
#     (screenShot.width, screenShot.height),
#     screenShot.rgb,
# )
# from matplotlib import pyplot as plt


# if cv2.waitKey(33) & 0xFF in (
#     ord('q'),
#     27,
# ):
#     break

id = 0
time.sleep(5)

with mss() as sct:
    while True:
        # print(pyautogui.position())
        screenShot = sct.grab(mon)
        img = Image.frombytes(
            'RGB',
            (screenShot.width, screenShot.height),
            screenShot.rgb,
        )

        id += 1

        # image = cv2.imread('./sprites/dino-game-start.png')
        image = np.array(img)
        cv2.imwrite(f"./pic/{id}-image1.png", image)
        small_image = cv2.imread('./sprites/dino-run.png')
        result = cv2.matchTemplate(small_image, image, cv2.TM_SQDIFF_NORMED)
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)
        MPx, MPy = mnLoc
        trows, tcols = small_image.shape[:2]
        dino_start = (MPx, MPy)
        dino_end = (MPx + tcols, MPy + trows)
        cv2.rectangle(image, dino_start, dino_end, (0, 0, 255), -1)
        cv2.imwrite(f"./pic/{id}-image2.png", image)
        # cv2.imshow('output', image)
        # cv2.waitKey(0)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        cv2.imwrite(f"./pic/{id}-image3.png", image_gray)
        # cv2.imshow('image_gray', image_gray)
        # cv2.waitKey(0)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        morph_img = cv2.morphologyEx(image_gray, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite(f"./pic/{id}-image4.png", morph_img)
        # cv2.imshow('morph_img', morph_img)
        # cv2.waitKey(0)

        (thresh, blackAndWhiteImage) = cv2.threshold(morph_img, 240, 255, cv2.THRESH_BINARY)
        cv2.imwrite(f"./pic/{id}-image5.png", blackAndWhiteImage)
        # cv2.imshow('blackAndWhiteImage', blackAndWhiteImage)
        # cv2.waitKey(0)

        whiteBlack = cv2.bitwise_not(blackAndWhiteImage)
        cv2.imwrite(f"./pic/{id}-image6.png", whiteBlack)
        # cv2.imshow('whiteBlack', whiteBlack)
        # cv2.waitKey(0)

        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # dilate = cv2.dilate(whiteBlack, kernel, iterations=1)
        # # morph_img2 = cv2.morphologyEx(whiteBlack, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow('morph_img2', dilate)
        # cv2.waitKey(0)
        #
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # morph_img3 = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        # cv2.imshow('morph_img3', morph_img3)
        # cv2.waitKey(0)

        # ret, thresh_img = cv2.threshold(whiteBlack, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        # cv2.imshow('thresh_img', thresh_img)
        # cv2.waitKey(0)


        contours, hierarchy = cv2.findContours(whiteBlack, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        # cv2.drawContours(morph_img3, contours, 2, (0, 255, 0), 3)
        # cv2.imshow('drawContours', morph_img3)
        # cv2.waitKey(0)

        idx = 0
        dino_threshold = 50
        dino_end = (dino_end[0] + 5, dino_end[1] + 5)

        last_press = 1.0
        time_threshold = 100
        for cnt in contours:
            idx += 1
            x, y, w, h = cv2.boundingRect(cnt)
            # if x - dino_start[0] + y - dino_start[1] + w - dino_end[0] + h - dino_end[1] < dino_threshold:
                # continue

            roi = image[y:y + h, x:x + w]
            # cv2.imwrite(str(idx)  + '.jpg', roi)
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
            cv2.rectangle(image, (x, y), (x + w, y + h), (200, 0, 0), -1)
        cv2.rectangle(image, dino_start, dino_end, (0, 0, 255), -1)
        cv2.imwrite(f"./pic/{id}-image7.png", image)
        # cv2.imwrite('./pic/img' + str(id) + ".png", image)
        print(id)
        # cv2.waitKey(0)

        # original = image.copy()
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # # thresh = np.array([10])
        # print(type(thresh))
        # ROI_number = 0
        # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # for c in cnts:
        #     x, y, w, h = cv2.boundingRect(c)
        #     cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
        #     ROI = original[y:y+h, x:x+w]
        #     cv2.imwrite('ROI_{}.png'.format(ROI_number), ROI)
        #     ROI_number += 1
        #
        # cv2.imshow('image', image)
        # cv2.waitKey()


        # image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        # (thresh, blackAndWhiteImage) = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)

        # plt.imshow(RGB_img, interpolation='nearest')
        # plt.show()
        # print(type(RGB_img))

        #
        # cv2.imshow('test', blackAndWhiteImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.waitKey(1)
        # plt.imshow(np.array(img), interpolation='nearest')
        # plt.show()
