# -*- coding: utf-8 -*-
import numpy as np
import cv2


kernel = 3


def on_set(key, val):
    if key == 'kernel':
        global kernel
        kernel = int(val)
        if ksize < 3:
            ksize = 3
        elif ksize % 2 == 0:
            ksize += 1


def on_get(key):
    if key == 'kernel':
        return str(kernel)


def on_run(source: np.ndarray):
    result = cv2.erode(source, (kernel, kernel))
    return {'result': result}


if __name__ == '__main__':
    pass
