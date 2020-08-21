# -*- coding: utf-8 -*-

import numpy as np
import cv2

COLOR_BGR2RGB_NAME = "BGR2RGB"
COLOR_RGB2BGR_NAME = "RGB2BGR"
COLOR_BGR2GRAY_NAME = "BGR2GRAY"
COLOR_GRAY2BGR_NAME = "GRAY2BGR"
COLOR_RGB2GRAY_NAME = "RGB2GRAY"
COLOR_GRAY2RGB_NAME = "GRAY2RGB"
COLOR_BGR2HSV_NAME = "BGR2HSV"
COLOR_HSV2BGR_NAME = "HSV2BGR"
COLOR_RGB2HSV_NAME = "RGB2HSV"
COLOR_HSV2RGB_NAME = "HSV2RGB"
COLOR_NAME_TO_FLAG = {
    COLOR_BGR2RGB_NAME: cv2.COLOR_BGR2RGB,
    COLOR_RGB2BGR_NAME: cv2.COLOR_RGB2BGR,
    COLOR_BGR2GRAY_NAME: cv2.COLOR_BGR2GRAY,
    COLOR_GRAY2BGR_NAME: cv2.COLOR_GRAY2BGR,
    COLOR_RGB2GRAY_NAME: cv2.COLOR_RGB2GRAY,
    COLOR_GRAY2RGB_NAME: cv2.COLOR_GRAY2RGB,
    COLOR_BGR2HSV_NAME: cv2.COLOR_BGR2HSV,
    COLOR_HSV2BGR_NAME: cv2.COLOR_HSV2BGR,
    COLOR_RGB2HSV_NAME: cv2.COLOR_RGB2HSV,
    COLOR_HSV2RGB_NAME: cv2.COLOR_HSV2RGB,
}
COLOR_FLAG_TO_NAME = {v: k for k, v in COLOR_NAME_TO_FLAG.items()}

flag = cv2.COLOR_BGR2RGB


def on_set(key, val):
    if key == 'flag':
        global flag
        flag = COLOR_NAME_TO_FLAG[val]


def on_get(key):
    if key == 'flag':
        return COLOR_FLAG_TO_NAME[flag]


def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(array):
    return {'result': cv2.cvtColor(array, flag)}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
