# -*- coding: utf-8 -*-
import numpy as np
import cv2


ksize = 3
sigmaX = 0


def on_set(key, val):
    if key == 'ksize':
        global ksize
        ksize = int(val)
        if ksize < 3:
            ksize = 3
        elif ksize % 2 == 0:
            ksize += 1
    elif key == 'sigmaX':
        global sigmaX
        csigmaX = int(val)


def on_get(key):
    if key == 'ksize':
        return str(ksize)
    elif key == 'sigmaX':
        return str(sigmaX)


def on_run(source: np.ndarray):
    if not source.shape:
        return {'result': None}
    result = cv2.GaussianBlur(source, (ksize, ksize), sigmaX)
    return {'result': result}


if __name__ == '__main__':
    pass
