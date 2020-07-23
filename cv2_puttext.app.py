# -*- coding: utf-8 -*-

import cv2

FONT_NAME_TO_NUM = {
    'HERSHEY_PLAIN': cv2.FONT_HERSHEY_PLAIN,
    'HERSHEY_SMALL': cv2.FONT_HERSHEY_COMPLEX_SMALL,
    'HERSHEY_SIMPLEX': cv2.FONT_HERSHEY_SIMPLEX,
    'ITALIC': cv2.FONT_ITALIC,
    'HERSHEY_DUPLEX': cv2.FONT_HERSHEY_DUPLEX,
    'HERSHEY_COMPLEX': cv2.FONT_HERSHEY_COMPLEX,
    'HERSHEY_TRIPLEX': cv2.FONT_HERSHEY_TRIPLEX,
    'HERSHEY_SCRIPT_COMPLEX': cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    'HERSHEY_SCRIPT_SIMPLEX': cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
}
FONT_NUM_TO_NAME = {v: k for k, v in FONT_NAME_TO_NUM.items()}

point_x = 0
point_y = 0
font_type = cv2.FONT_HERSHEY_PLAIN
font_scale = 0
color = (0, 0, 0)
font_thickness = 1


def on_set(key, val):
    if key == 'x':
        global point_x
        point_x = int(val)
    elif key == 'y':
        global point_y
        point_y = int(val)
    elif key == 'font_type':
        global font_type
        font_type = FONT_NAME_TO_NUM[val]
    elif key == 'font_scale':
        global font_scale
        font_scale = int(val)
    elif key == 'color':
        global color
        h = str(val).lstrip('#')
        color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    elif key == 'font_thickness':
        global font_thickness
        font_thickness = int(val)


def on_get(key):
    if key == 'x':
        return str(point_x)
    elif key == 'y':
        return str(point_y)
    elif key == 'font_type':
        return FONT_NUM_TO_NAME[font_type]
    elif key == 'font_scale':
        return str(font_scale)
    elif key == 'color':
        return '#' + rgb_to_hex(color)
    elif key == 'font_thickness':
        return str(font_thickness)


def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:] + hex(g)[2:] + hex(b)[2:]


def on_run(source, text):
    assert len(source.shape) == 3
    assert source.shape[0] >= 1
    assert source.shape[1] >= 1
    assert source.shape[2] >= 1
    result = source.copy()

    text_str = "".join([chr(item) for item in text])

    result = cv2.putText(result,
                         text_str,
                         (point_x, point_y),
                         font_type,
                         font_scale,
                         color,
                         font_thickness)

    return {'result': result}


if __name__ == '__main__':
    pass
