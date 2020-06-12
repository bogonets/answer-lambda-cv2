# -*- coding: utf-8 -*-
# https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html?highlight=resize#resize

import numpy as np
import cv2

# INTER_NEAREST - a nearest-neighbor interpolation
# INTER_LINEAR - a bilinear interpolation (used by default)
# INTER_AREA - resampling using pixel area relation.
#              It may be a preferred method for image decimation,
#              as it gives moire’-free results. But when the image is zoomed,
#              it is similar to the INTER_NEAREST method.
# INTER_CUBIC - a bicubic interpolation over 4x4 pixel neighborhood
# INTER_LANCZOS4 - a Lanczos interpolation over 8x8 pixel neighborhood

INTERPOLATION_NAME_TO_ENUM = {
    'nearest': cv2.INTER_NEAREST,
    'linear': cv2.INTER_LINEAR,
    'area': cv2.INTER_AREA,
    'cubic': cv2.INTER_CUBIC,
    'lanczos4': cv2.INTER_LANCZOS4
}
INTERPOLATION_ENUM_TO_NAME = {v: k for k, v in INTERPOLATION_NAME_TO_ENUM.items()}

width = 0
height = 0
fx = 0.0
fy = 0.0
interpolation = cv2.INTER_LINEAR


def on_set(key, val):
    if key == 'width':
        global width
        width = int(val)
    elif key == 'height':
        global height
        height = int(val)
    elif key == 'fx':
        global fx
        fx = float(val)
    elif key == 'fy':
        global fy
        fy = float(val)
    elif key == 'interpolation':
        global interpolation
        interpolation = INTERPOLATION_NAME_TO_ENUM[val]


def on_get(key):
    if key == 'width':
        return str(width)
    elif key == 'height':
        return str(height)
    elif key == 'fx':
        return str(fx)
    elif key == 'fy':
        return str(fy)
    elif key == 'interpolation':
        return INTERPOLATION_ENUM_TO_NAME[interpolation]


def on_run(source: np.ndarray):
    result = cv2.resize(source, dsize=(width, height), fx=fx, fy=fy, interpolation=interpolation)
    return {'result': result}


if __name__ == '__main__':
    pass
