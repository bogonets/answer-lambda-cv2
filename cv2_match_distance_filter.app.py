# -*- coding: utf-8 -*-

import numpy as np

ratio = 0.7
verbose = False


def on_set(key, val):
    if key == 'ratio':
        global ratio
        ratio = float(val)


def on_get(key):
    if key == 'ratio':
        return ratio


def on_run(query, train):
    good = query[::, 0] < train[::, 0]*ratio
    good_query = query[good]
    return {'good': good_query}


if __name__ == '__main__':
    pass
