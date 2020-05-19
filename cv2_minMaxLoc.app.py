# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys


def on_init():
    return True


def on_valid():
    return True


def on_run(array: np.ndarray):
    sys.stdout.write(f"[minMaxLoc] array : {array}\n")
    sys.stdout.write(f"[minMaxLoc] array.shape : {array.shape}\n")
    sys.stdout.flush()
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(array)

    sys.stdout.write(f"[minMaxLoc] minVal: {minVal}, maxVal: {maxVal}, minLoc: {minLoc}, maxLoc: {maxLoc}\n")
    sys.stdout.flush()

    return {
        'min_val': np.array([minVal], np.float32),
        'max_val': np.array([maxVal], np.float32),
        'min_loc': np.array(list(minLoc), np.int32),
        'max_loc': np.array(list(maxLoc), np.int32),
    }


def on_destroy():
    return True


if __name__ == '__main__':
    pass
