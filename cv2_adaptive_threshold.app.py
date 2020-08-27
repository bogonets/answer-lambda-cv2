# -*- coding: utf-8 -*-
import numpy as np
import cv2


ADAPTIVE_THRESH_NAME_TO_ENUM = {
    'gaussian_c': cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    'mean_c': cv2.ADAPTIVE_THRESH_MEAN_C
}
ADAPTIVE_THRESH_ENUM_TO_NAME = {v: k for k, v in ADAPTIVE_THRESH_NAME_TO_ENUM.items()}


THRESH_NAME_TO_ENUM = {
    'binary': cv2.THRESH_BINARY,
    'binary_inv': cv2.THRESH_BINARY_INV,
    'mask': cv2.THRESH_MASK,
    'otsu': cv2.THRESH_OTSU,
    'tozero': cv2.THRESH_TOZERO,
    'tozero_inv': cv2.THRESH_TOZERO_INV,
    'triangle': cv2.THRESH_TRIANGLE,
    'trunc': cv2.THRESH_TRUNC
}
THRESH_ENUM_TO_NAME = {v: k for k, v in THRESH_NAME_TO_ENUM.items()}

max_value = 255
block_size = 3
c = 5
adaptive_thresh = ADAPTIVE_THRESH_NAME_TO_ENUM['gaussian_c']
thresh = THRESH_NAME_TO_ENUM['binary']


def on_set(key, val):
    if key == 'max_value':
        global max_value
        max_value = int(val)
    elif key == 'block_size':
        global block_size
        block_size = int(val)
        if block_size < 3:
            block_size = 3
        elif block_size % 2 == 0:
            block_size += 1
    elif key == 'c':
        global c
        c = int(val)
    elif key == 'adaptive_thresh':
        global adaptive_thresh
        adaptive_thresh = ADAPTIVE_THRESH_NAME_TO_ENUM[val]
    elif key == 'thresh':
        global thresh
        thresh = THRESH_NAME_TO_ENUM[val]


def on_get(key):
    if key == 'max_value':
        return str(max_value)
    elif key == 'block_size':
        return str(block_size)
    elif key == 'c':
        return str(c)
    elif key == 'adaptive_thresh':
        return ADAPTIVE_THRESH_ENUM_TO_NAME[adaptive_thresh]
    elif key == 'thresh':
        return THRESH_ENUM_TO_NAME[thresh]


def on_run(source: np.ndarray):
    result = cv2.adaptiveThreshold(source, max_value, adaptive_thresh, thres, block_size, c)
    return {'result': result}


if __name__ == '__main__':
    pass
