# -*- coding: utf-8 -*-

import numpy as np
import cv2

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
        return LINE_NUM_TO_NAME[line_type]
    elif key == 'shift':
        return str(shift)


def on_create():
    return True


def on_init():
    return True


def on_valid():
    return True


def on_run(source: np.ndarray, lines: np.ndarray):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1

    assert len(lines.shape) == 2
    assert lines.shape[0] >= 1
    assert lines.shape[1] == 4

    result = source.copy()
    for i in range(lines.shape[0]):
        cv2.line(result,
                 (int(lines[i][0]), int(lines[i][1])),
                 (int(lines[i][2]), int(lines[i][2])),
                 color, thickness, line_type, shift)
    return {'result', result}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
