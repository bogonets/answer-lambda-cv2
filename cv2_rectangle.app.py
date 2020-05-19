# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys

LINE_4_NAME = '4'
LINE_8_NAME = '8'
LINE_AA_NAME = 'AA'
LINE_NAME_TO_NUM = {
    LINE_4_NAME: cv2.LINE_4,
    LINE_8_NAME: cv2.LINE_8,
    LINE_AA_NAME: cv2.LINE_AA
}
LINE_NUM_TO_NAME = {v: k for k, v in LINE_NAME_TO_NUM.items()}

color = (0, 0, 0)
thickness = 0
line_type = cv2.LINE_8
shift = 0


def on_set(key, val):
    if key == 'color':
        global color
        color = str(val).split(',')
    elif key == 'thickness':
        global thickness
        thickness = int(val)
    elif key == 'line_type':
        global line_type
        line_type = LINE_NAME_TO_NUM[val]
    elif key == 'shift':
        global shift
        shift = int(val)


def on_get(key):
    if key == 'color':
        return ','.join(list(str(x) for x in color))
    elif key == 'thickness':
        return str(thickness)
    elif key == 'line_type':
        return LINE_NUMthickness

def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(source: np.ndarray, rectangles: np.ndarray):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1

    assert len(rectangles.shape) == 2
    assert rectangles.shape[0] >= 1
    assert rectangles.shape[1] == 4

    result = source.copy()

    # sys.stdout.write(f"color : {color}")
    # sys.stdout.write(f"thickness : {thickness}")
    # sys.stdout.write(f"line_type : {line_type}")
    # sys.stdout.flush()

    for i in range(rectangles.shape[0]):
        cv2.rectangle(result,
                      (int(rectangles[i][0]), int(rectangles[i][1])),
                      (int(rectangles[i][2]), int(rectangles[i][3])),
                      (255, 255, 255),
                      thickness,
                      line_type)
    return {'result': result}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
