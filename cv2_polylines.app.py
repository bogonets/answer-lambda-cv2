# -*- coding: utf-8 -*-

# import sys
import numpy as np
import cv2

LINE_NAME_TO_NUM = {
    '4': cv2.LINE_4,
    '8': cv2.LINE_8,
    'AA': cv2.LINE_AA
}
LINE_NUM_TO_NAME = {v: k for k, v in LINE_NAME_TO_NUM.items()}

POLYLINE_TYPE_TO_SELECT = {
    'True': True,
    'False': False
}
POLYLINE_SELECT_TO_TYPE = {v: k for k, v in POLYLINE_TYPE_TO_SELECT.items()}

isClosed = 'True'
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
    elif key == 'isClosed':
        global isClosed
        isClosed = POLYLINE_TYPE_TO_SELECT[val]


def on_get(key):
    if key == 'color':
        return ','.join(list(map(lambda x: str(x), color)))
    elif key == 'thickness':
        return str(thickness)
    elif key == 'line_type':
        return LINE_NUM_TO_NAME[line_type]
    elif key == 'shift':
        return str(shift)
    elif key == 'isClosed':
        return POLYLINE_SELECT_TO_TYPE[isClosed]


def on_run(source: np.ndarray, points: np.ndarray):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1

    # sys.stdout.write(f"[cv2_polylines.on_run] polylines:points {points} {type(points)}\n")
    # sys.stdout.write(f"[cv2_polylines.on_run] polylines:points {points.size} \n")
    # sys.stdout.flush()

    if points.size < 3:
        return {'result': source}

    result = source.copy()

    pts = []
    for pt in points:
        pts.append(np.array(pt, np.int32).reshape(-1, 2))
    if not pts:
        return {'result': source}

    result = cv2.polylines(result,
                           pts,
                           isClosed,
                           color,
                           thickness,
                           line_type,
                           shift)
    return {'result': result}


if __name__ == '__main__':
    pass
