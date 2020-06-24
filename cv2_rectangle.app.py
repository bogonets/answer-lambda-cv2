# -*- coding: utf-8 -*-

import sys
from enum import Enum
import numpy as np
import cv2

LINE_NAME_TO_NUM = {
    '4': cv2.LINE_4,
    '8': cv2.LINE_8,
    'AA': cv2.LINE_AA
}
LINE_NUM_TO_NAME = {v: k for k, v in LINE_NAME_TO_NUM.items()}


class Coordinates(Enum):
    RATIO=1
    ABSOLUTE=2


COORDINATES_NAME_TO_ENUM = {
    'ratio': Coordinates.RATIO,
    'absolute': Coordinates.ABSOLUTE
}
COORDINATES_ENUM_TO_NAME = {v: k for k, v in COORDINATES_NAME_TO_ENUM.items()}

color = (0, 0, 0)
thickness = 0
line_type = cv2.LINE_8
shift = 0
coordinates = Coordinates.RATIO


def on_set(key, val):
    if key == 'color':
        global color
        h = str(val).lstrip('#')
        color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    elif key == 'thickness':
        global thickness
        thickness = int(val)
    elif key == 'line_type':
        global line_type
        line_type = LINE_NAME_TO_NUM[val]
    elif key == 'shift':
        global shift
        shift = int(val)
    elif key == 'coordinates':
        global coordinates
        coordinates = COORDINATES_NAME_TO_ENUM[val]


def on_get(key):
    if key == 'color':
        return ','.join(list(map(lambda x: str(x), color)))
    elif key == 'thickness':
        return str(thickness)
    elif key == 'line_type':
        return LINE_NUM_TO_NAME[line_type]
    elif key == 'shift':
        return str(shift)
    elif key == 'coordinates':
        return COORDINATES_ENUM_TO_NAME[coordinates]


def convert_drawable_rect(r, w, h, is_absolute_coordinates=False):
    if is_absolute_coordinates:
        return int(r[0]), int(r[1]), int(r[2]), int(r[3])
    else:
        return int(r[0]*w), int(r[1]*h), int(r[2]*w), int(r[3]*h)


def convert_drawable_rects(rectangles: np.ndarray, width, height, is_absolute_coordinates=False):
    result = list()
    rectangles_rank = len(rectangles.shape)
    if rectangles_rank == 1:
        assert rectangles.shape[0] >= 4
        result.append(convert_drawable_rect(rectangles[0:4], width, height, is_absolute_coordinates))
    else:
        assert rectangles_rank == 2
        assert rectangles.shape[0] >= 1
        assert rectangles.shape[1] >= 4
        for i in range(rectangles.shape[0]):
            result.append(convert_drawable_rect(rectangles[i][0:4], width, height, is_absolute_coordinates))
    return result


def on_run(source: np.ndarray, rectangles: np.ndarray):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1

    # sys.stdout.write(f"[cv2_rectangle.on_run] rectangles {rectangles} {type(rectangles)}\n")
    # sys.stdout.write(f"[cv2_rectangle.on_run] rectangles.size {rectangles.size}\n")
    # sys.stdout.flush()
    if rectangles.size < 4:
        return {'result': source}

    result = source.copy()
    for rect in convert_drawable_rects(rectangles, source.shape[1], source.shape[0], coordinates is Coordinates.ABSOLUTE):
        cv2.rectangle(result,
                      (rect[0], rect[1]),
                      (rect[2], rect[3]),
                      color,
                      thickness,
                      line_type,
                      shift)
    return {'result': result}


if __name__ == '__main__':
    pass
