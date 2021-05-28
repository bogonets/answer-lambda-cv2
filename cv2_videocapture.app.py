# -*- coding: utf-8 -*-
# @see <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html>

import numpy as np
import cv2


API_NAME_TO_NUM = {
    'default': 0,
    'ffmpeg': cv2.CAP_FFMPEG,
    'images': cv2.CAP_IMAGES,
    'dshow': cv2.CAP_DSHOW,
}
API_NUM_TO_NAME = {v: k for k, v in API_NAME_TO_NUM.items()}

filename = ''
api_preference = API_NAME_TO_NUM['default']
reopen = True


class VideoCapture:
    def __init__(self, filename: str, api_preference: int, reopen: bool):
        self.filename = filename
        self.api_preference = api_preference
        self.reopen = reopen
        self.last_frame = None
        self.cap = None

    def open_video(self):
        assert self.cap is None
        try:
            if self.api_preference == 0:
                self.cap = cv2.VideoCapture(self.filename)
            else:
                self.cap = cv2.VideoCapture(self.filename, self.api_preference)
            return True
        except BaseException:
            return False

    def is_opened_video(self):
        return self.cap is not None

    def close_video(self):
        if self.cap is None:
            return

        try:
            self.cap.release()
        except BaseException:
            pass
        finally:
            self.cap = None

    def reopen_video(self):
        self.close_video()
        assert self.cap is None
        return self.open_video()

    def read_next_frame(self):
        result, last_frame = self.cap.read()
        if not result:
            raise StopIteration()
        self.last_frame = last_frame
        return self.last_frame

    def run(self):
        if not self.is_opened_video():
            self.open_video()

        while not self.server_exit.value:
            # Read current frame.
            try:
                self.read_next_frame()
            except BaseException:
                if self.reopen:
                    self.reopen_video()
                else:
                    break

            self.push_data(self.last_frame)


cap: VideoCapture = None


def on_set(key, val):
    if key == 'filename':
        global filename
        filename = str(val)
    elif key == 'api_preference':
        global api_preference
        api_preference = API_NAME_TO_NUM[val]
    elif key == 'reopen':
        global reopen
        reopen = bool(val)


def on_get(key):
    if key == 'filename':
        return filename
    elif key == 'api_preference':
        return API_NUM_TO_NAME[api_preference]
    elif key == 'reopen':
        return str(reopen)


def on_init():
    global cap
    cap = VideoCapture(filename, api_preference, reopen)
    cap.open_video()
    return True


def on_valid():
    global cap
    return cap.is_opened_video()


def on_run():
    global cap

    if not cap.is_opened_video():
        cap.open_video()

    try:
        frame = cap.read_next_frame()
    except BaseException:
        if cap.reopen:
            cap.reopen_video()
        raise

    return {'frame': frame}


def on_destroy():
    cap.close_video()


if __name__ == '__main__':
    pass
