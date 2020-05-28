# -*- coding: utf-8 -*-

import numpy as np
import cv2

LINE_NAME_TO_NUM = {
    '4': cv2.LINE_4,
    '8': cv2.LINE_8,
    'AA': cv2.LINE_AA
}
LINE_NUM_TO_NAME = {v: k for k, v in LINE_NAME_TO_NUM.items()}

color = (0, 0, 0)
thickness = 0
line_type = cv2.LINE_8
shift = 0


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


def on_get(key):
    if key == 'color':
        return ','.join(list(map(lambda x: str(x), color)))
    elif key == 'thickness':
        return str(thickness)
    elif key == 'line_type':
        return LINE_NUM_TO_NAME[line_type]
    elif key == 'shift':
        return str(shift)


def convert_drawable_line(line, w, h, is_absolute_coordinates=False):
    if is_absolute_coordinates:
        return int(line[0]), int(line[1])
    else:
        return int(line[0]*w), int(line[1]*h)


def convert_drawable_lines(lines: np.ndarray, width, height):
    is_absolute_coordinates = lines.dtype not in [np.float32, np.float64]
    lines_rank = len(lines.shape)
    result = list()
    if lines_rank == 1:
        assert lines.shape[0] >= 4
        result.append(convert_drawable_line(lines[0:2], width, height, is_absolute_coordinates))
    else:
        assert lines_rank == 2
        assert lines.shape[0] >= 1
        assert lines.shape[1] >= 4
        for i in range(lines.shape[0]):
            result.append(convert_drawable_line(lines[i][0:2], width, height, is_absolute_coordinates))
    return result


def on_run(source: np.ndarray, rectangles: np.ndarray):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1
    result = source.copy()
    for line in convert_drawable_lines(rectangles, source.shape[1], source.shape[0]):
        cv2.line(result,
                 (line[0], line[1]),
                 (line[2], line[3]),
                 color,
                 thickness,
                 line_type,
                 shift)
    return {'result': result}


if __name__ == '__main__':
    pass
