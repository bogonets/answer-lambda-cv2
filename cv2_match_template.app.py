# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys

METHOD_TM_CCOEFF_NAME = 'TM_CCOEFF'
METHOD_TM_CCOEFF_NORMED_NAME = 'TM_CCOEFF_NORMED'
METHOD_TM_CCORR_NAME = 'TM_CCORR'
METHOD_TM_CCORR_NORMED_NAME = 'TM_CCORR_NORMED'
METHOD_TM_SQDIFF_NAME = 'TM_SQDIFF'
METHOD_TM_SQDIFF_NORMED_NAME = 'TM_SQDIFF_NORMED'
METHOD_NAME_TO_NUM = {
    METHOD_TM_CCOEFF_NAME : cv2.TM_CCOEFF,
    METHOD_TM_CCOEFF_NORMED_NAME : cv2.TM_CCOEFF_NORMED,
    METHOD_TM_CCORR_NAME : cv2.TM_CCORR,
    METHOD_TM_CCORR_NORMED_NAME : cv2.TM_CCORR_NORMED,
    METHOD_TM_SQDIFF_NAME : cv2.TM_SQDIFF,
    METHOD_TM_SQDIFF_NORMED_NAME : cv2.TM_SQDIFF_NORMED
}
METHOD_NUM_TO_NAME = {v: k for k, v in METHOD_NAME_TO_NUM.items()}

method = METHOD_NAME_TO_NUM[METHOD_TM_CCOEFF_NORMED_NAME]

def on_set(key, val):
    if key == 'method':
        global method
        method = METHOD_NAME_TO_NUM[val]


def on_get(key):
    if key == 'method':
        return METHOD_NUM_TO_NAME[method]


def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(image: np.ndarray, template: np.ndarray):
    assert len(image.shape) == 3
    assert image.shape[0] >= 1
    assert image.shape[1] >= 1
    assert image.shape[2] >= 1

    assert len(template.shape) == 3
    assert template.shape[0] >= 1
    assert template.shape[1] >= 1
    assert template.shape[2] >= 1

    result = cv2.matchTemplate(image, template, method)

    sys.stdout.write(f"[matchTemplate] result : {result}")
    
    return {'result': result}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
