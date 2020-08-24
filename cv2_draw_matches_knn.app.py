# -*- coding: utf-8 -*-

import numpy as np
import cv2
from typing import List

FLAG_NAME_TO_TYPE = {
    'DEFAULT': cv2.DRAW_MATCHES_FLAGS_DEFAULT,
    'DRAW_OVER_OUTIMG': cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG,
    'NOT_DRAW_SINGLE_POINTS': cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS,
    'DRAW_RICH_KEYPOINTS': cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
}
FLAG_TYPE_TO_NAME = {v: k for k, v in FLAG_NAME_TO_TYPE.items()}

flag = cv2.DRAW_MATCHES_FLAGS_DEFAULT


def on_set(key, val):
    if key == 'flag':
        global flag
        flag = FLAG_NAME_TO_TYPE[val]


def on_get(key):
    if key == 'flag':
        return FLAG_TYPE_TO_NAME[flag]


def array_to_keypoints(array: np.ndarray) -> List[cv2.KeyPoint]:
    result = []
    for x in array:
        result.append(cv2.KeyPoint(_angle=x[0],
                                   _class_id=int(x[1]),
                                   _octave=int(x[2]),
                                   x=x[3],
                                   y=x[4],
                                   _response=x[5],
                                   _size=x[6]))
    return result


def array_to_matches(array: np.ndarray) -> List[List[cv2.DMatch]]:
    result = []
    for x in array:
        result.append([cv2.DMatch(_distance=x[0],
                                  _imgIdx=int(x[1]),
                                  _queryIdx=int(x[2]),
                                  _trainIdx=int(x[3]))])
    return result


def on_run(img1, keypoints1, img2, keypoints2, matches1to2):
    result = cv2.drawMatchesKnn(img1=img1,
                                keypoints1=array_to_keypoints(keypoints1),
                                img2=img2,
                                keypoints2=array_to_keypoints(keypoints2),
                                matches1to2=array_to_matches(matches1to2),
                                outImg=None,
                                matchColor=None,
                                singlePointColor=None,
                                matchesMask=None,
                                flags=2)
    return {'result': result}


if __name__ == '__main__':
    pass
