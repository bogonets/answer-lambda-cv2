# -*- coding: utf-8 -*-

import os
import numpy as np
import cv2

FLAG_COLOR_NAME = 'color'
FLAG_GRAYSCALE_NAME = 'grayscale'
FLAG_UNCHANGED_NAME = 'unchanged'
FLAG_NAME_TO_TYPE = {
    FLAG_COLOR_NAME: cv2.IMREAD_COLOR,
    FLAG_GRAYSCALE_NAME: cv2.IMREAD_GRAYSCALE,
    FLAG_UNCHANGED_NAME: cv2.IMREAD_UNCHANGED,
}
FLAG_TYPE_TO_NAME = {v: k for k, v in FLAG_NAME_TO_TYPE.items()}
LOWER_IMAGE_EXTENSIONS = ('.jpeg', '.jpg', '.png')

filename = str()
flag = cv2.IMREAD_COLOR
cache = True
cached_image = None


def get_filename():
    global APP
    WORKING_DIRECTORY = APP['current_working_directory']
    global filename
    if os.path.isabs(filename):
        return filename
    else:
        return os.path.join(WORKING_DIRECTORY, filename)


def is_image_name(name: str):
    lower_name = name.lower()
    for ext in LOWER_IMAGE_EXTENSIONS:
        if lower_name.endswith(ext):
            return True
    return False


def get_files(search_dir: str):
    return [f for f in os.listdir(search_dir) if os.path.isfile(os.path.join(search_dir, f))]


def get_image_files(search_dir: str):
    return [f for f in get_files(search_dir) if is_image_name(f)]


def get_recursive_image_files(search_dir: str):
    result = []
    for root, dirs, files in os.walk(search_dir):
        for item in files:
            if is_image_name(item):
                result.append(item)
    return result


def on_set(key, val):
    if key == 'filename':
        global filename
        filename = val
    elif key == 'flag':
        global flag
        flag = FLAG_NAME_TO_TYPE[val]
    elif key == 'cache':
        global cache
        cache = bool(val)


def on_get(key):
    global APP
    WORKING_DIRECTORY = APP['current_working_directory']
    if key == 'filename':
        return filename
    elif key == 'filename_list':
        return ','.join(get_recursive_image_files(WORKING_DIRECTORY))
    elif key == 'flag':
        return FLAG_TYPE_TO_NAME[flag]
    elif key == 'cache':
        return str(cache)


def on_create():
    return True


def on_init():
    global cached_image
    cached_image = cv2.imread(get_filename(), flag)
    return True


def on_valid():
    return cached_image is not None


def on_run():
    global cached_image
    if cached_image is not None or not cache:
        cached_image = cv2.imread(get_filename(), flag)
    return {'result': cached_image}


def on_destroy():
    return True


if __name__ == '__main__':
    # print(f"Working directory: {WORKING_DIRECTORY}")
    pass

