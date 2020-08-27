# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys


LOGGING_PREFIX = '[cv2.orb.detectAndCompute] '
LOGGING_SUFFIX = '\n'

SCORE_NAME_TO_TYPE = {
    "HARRIS": cv2.ORB_HARRIS_SCORE,
    "FAST": cv2.ORB_FAST_SCORE,
}
SCORE_TYPE_TO_NAME = {v: k for k, v in SCORE_NAME_TO_TYPE.items()}

nfeatures = 500
scaleFactor = 1.2
nlevels = 8
edgeThreshold = 31
firstLevel = 0
WTA_K = 2
scoreType = cv2.ORB_HARRIS_SCORE
patchSize = 31
fastThreshold = 20

orb: cv2.Feature2D = None

mask = None
descriptors = None
use_provided_keypoints = False

verbose = False


def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stdout.flush()


def print_error(message):
    sys.stderr.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stderr.flush()


def on_set(key, val):
    if key == 'nfeatures':
        global nfeatures
        nfeatures = int(val)
    elif key == 'scaleFactor':
        global scaleFactor
        scaleFactor = float(val)
    elif key == 'nlevels':
        global nlevels
        nlevels = int(val)
    elif key == 'edgeThreshold':
        global edgeThreshold
        edgeThreshold = int(val)
    elif key == 'firstLevel':
        global firstLevel
        firstLevel = int(val)
    elif key == 'WTA_K':
        global WTA_K
        WTA_K = int(val)
    elif key == 'scoreType':
        global scoreType
        scoreType = SCORE_NAME_TO_TYPE[val]
    elif key == 'patchSize':
        global patchSize
        patchSize = int(val)
    elif key == 'fastThreshold':
        global fastThreshold
        fastThreshold = int(val)


def on_get(key):
    if key == 'nfeatures':
        return nfeatures
    elif key == 'scaleFactor':
        return scaleFactor
    elif key == 'nlevels':
        return nlevels
    elif key == 'edgeThreshold':
        return edgeThreshold
    elif key == 'firstLevel':
        return firstLevel
    elif key == 'WTA_K':
        return WTA_K
    elif key == 'scoreType':
        return SCORE_TYPE_TO_NAME[scoreType]
    elif key == 'patchSize':
        return patchSize
    elif key == 'fastThreshold':
        return fastThreshold


def on_init():
    global orb
    orb = cv2.ORB_create(nfeatures=nfeatures,
                         scaleFactor=scaleFactor,
                         nlevels=nlevels,
                         edgeThreshold=edgeThreshold,
                         firstLevel=firstLevel,
                         WTA_K=WTA_K,
                         scoreType=scoreType,
                         patchSize=patchSize,
                         fastThreshold=fastThreshold)
    return orb is not None


def on_valid():
    return orb is not None


def on_run(image):
    kp, desc = orb.detectAndCompute(image=image,
                                    mask=mask,
                                    descriptors=descriptors,
                                    useProvidedKeypoints=use_provided_keypoints)
    kp_list = [[x.angle, x.class_id, x.octave, x.pt[0], x.pt[1], x.response, x.size] for x in kp]

    if verbose:
        print_out(f'keypoints: {kp_list}')
        print_out(f'descriptors: {desc}')

    return {
        'keypoints': np.array(kp_list, dtype=np.float),
        'descriptors': desc
    }


if __name__ == '__main__':
    pass
