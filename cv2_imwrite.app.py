# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2
import sys


filename = str()


def on_set(key, val):
    if key == 'filename':
        global filename
        filename = val


def on_get(key):
    if key == 'filename':
        return filename


def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(array):
    shape = array.shape

    # sys.stdout.write(f"{shape}")
    # sys.stdout.flush()
    assert len(shape) == 3
    assert shape[0] > 0
    assert shape[1] > 0
    assert shape[2] == 1 or shape[2] == 3
    cv2.imwrite(filename, array)


def on_destroy():
    return True


if __name__ == '__main__':
    pass
