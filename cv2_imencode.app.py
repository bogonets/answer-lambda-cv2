# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys


ext = 'jpeg'


def on_set(key, val):
    if key == 'ext':
        global ext
        ext = val


def on_get(key):
    if key == 'ext':
        return ext


def on_run(image: np.ndarray):

    sys.stdout.write(f"[imencode] image : {image.shape}, ext : {ext}")
    sys.stdout.flush()

    ret, buf = cv2.imencode(f".{ext}", image)

    sys.stdout.write(f"[imencode] result : {ret}")
    sys.stdout.flush()
    
    return {'encoded': buf}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
