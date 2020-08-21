# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys
from typing import List, Any

LOGGING_PREFIX = '[cv2.bf.knnMatch] '
LOGGING_SUFFIX = '\n'

NORM_NAME_TO_TYPE = {
    "L1": cv2.NORM_L2,
    "L2": cv2.NORM_L1,
    "HAMMING": cv2.NORM_HAMMING,
    "HAMMING2": cv2.NORM_HAMMING2,
}
NORM_TYPE_TO_NAME = {v: k for k, v in NORM_NAME_TO_TYPE.items()}

normType = cv2.NORM_L2
crossCheck = False

# Brute-force matcher.
bf: cv2.BFMatcher = None

k = 2
mask = None
compactResult = None
verbose = False


def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stdout.flush()


def print_error(message):
    sys.stderr.write(LOGGING_PREFIX + message + LOGGING_SUFFIX)
    sys.stderr.flush()


def on_set(key, val):
    if key == 'normType':
        global normType
        normType = NORM_NAME_TO_TYPE[val]
    elif key == 'crossCheck':
        global crossCheck
        crossCheck = str(val).lower() in ['yes', 'y', 'true']
    elif key == 'k':
        global k
        k = int(val)


def on_get(key):
    if key == 'normType':
        return NORM_TYPE_TO_NAME[normType]
    elif key == 'crossCheck':
        return crossCheck
    elif key == 'k':
        return k


def on_init():
    global bf
    bf = cv2.BFMatcher(normType=normType, crossCheck=crossCheck)
    return bf is not None


def on_valid():
    return bf is not None


def normalize_matches(matches: List[List[cv2.DMatch]], i: int) -> List[cv2.DMatch]:
    result = []
    for x in matches:
        if i < len(x):
            result.append(x[i])
        else:
            result.append(cv2.DMatch(distance=0.0, imgIdx=0, queryIdx=0, trainIdx=0))
    return result


def matches_to_list(matches: List[List[cv2.DMatch]], i: int) -> List[List[Any]]:
    return [[x.distance, x.imgIdx, x.queryIdx, x.trainIdx] for x in normalize_matches(matches, i)]


def on_run(query, train):
    matches = bf.knnMatch(query, train, k=k, mask=mask, compactResult=compactResult)

    if len(list(filter(lambda x: len(x) != k, matches))) == 0:
        print_error(f'Found an element that is not of length k({k}).')

    match1 = np.array(matches_to_list(matches, 0), dtype=np.float)
    match2 = np.array(matches_to_list(matches, 1), dtype=np.float)

    if verbose:
        print_out(f'match1: {match1}')
        print_out(f'match2: {match2}')

    return {'match1': match1, 'match2': match2}


if __name__ == '__main__':
    pass
