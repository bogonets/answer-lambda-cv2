# -*- coding: utf-8 -*-
import numpy as np
import cv2


def on_run(source: np.ndarray):
    result = cv2.bitwise_not(source)
    return {'result': result}


if __name__ == '__main__':
    pass
