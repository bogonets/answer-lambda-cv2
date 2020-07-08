# -*- coding: utf-8 -*-

import sys
import multiprocessing as mp
from multiprocessing.sharedctypes import Value
from queue import Full, Empty
import numpy as np
import time
import cv2


EMPTY_ARRAY = np.zeros((300, 300, 3), dtype=np.uint8)
RECONNECT_SLEEP = 1.0
ENABLE_VERBOSE = False
LOGGING_PREFIX = '[cv2.videocapture.server] '


def print_out(message):
    sys.stdout.write(LOGGING_PREFIX + message)
    sys.stdout.flush()


def print_error(message):
    sys.stderr.write(LOGGING_PREFIX + message)
    sys.stderr.flush()


class VideoCaptureServer:
    """
    """

    def __init__(self,
                 server_queue: mp.Queue,
                 server_exit: Value,
                 filename: str,
                 api_preference: int,
                 sleep: int,
                 reopen: bool):
        self.server_queue = server_queue
        self.server_exit = server_exit

        self.filename = filename
        self.api_preference = api_preference
        self.sleep_seconds = float(sleep) / 1000.0
        self.reopen = reopen

        self.cap: cv2.VideoCapture = None
        self.last_frame = EMPTY_ARRAY

        print_out(f'VideoCaptureServer(filename={filename},sleep={self.sleep_seconds}s,reopen={reopen})')

    def open_video(self):
        print_out('VideoCaptureServer.open_video()')
        assert self.cap is None
        try:
            if self.api_preference == 0:
                self.cap = cv2.VideoCapture(self.filename)
            else:
                self.cap = cv2.VideoCapture(self.filename, self.api_preference)
            return True
        except Exception as e:
            print_error(e)
            return False

    def is_opened_video(self):
        return self.cap is not None

    def close_video(self):
        print_out('VideoCaptureServer.close_video()')
        if self.cap is None:
            return

        try:
            self.cap.release()
        except Exception as e:
            print_error(e)
        finally:
            self.cap = None

    def reopen_video(self):
        print_out('VideoCaptureServer.reopen_video()')
        self.close_video()
        assert self.cap is None
        return self.open_video()

    def read_next_frame(self):
        result, self.last_frame = self.cap.read()
        if not result:
            raise StopIteration()

    def _push_nowait(self, data):
        try:
            self.server_queue.put_nowait(data)
            return True
        except Full:
            return False

    def _pop_nowait(self):
        try:
            self.server_queue.get_nowait()
        except Empty:
            pass

    def push_data(self, data):
        if not self._push_nowait(data):
            self._pop_nowait()
            if not self._push_nowait(data):
                print_error('VideoCaptureServer.push_array() Queue is Full.')

    def run(self):
        print_out('VideoCaptureServer.run() BEGIN.')

        if not self.is_opened_video():
            self.open_video()

        while not self.server_exit.value:
            # Read current frame.
            try:
                self.read_next_frame()
            except Exception as e:
                print_error(e)

                if self.reopen:
                    if not self.reopen_video():
                        time.sleep(RECONNECT_SLEEP)
                else:
                    break

            if ENABLE_VERBOSE:
                print_out(f'VideoCaptureServer.run() Push(frame={self.last_frame.shape})')

            self.push_data(self.last_frame)

            if self.sleep_seconds > 0.0:
                time.sleep(self.sleep_seconds)

        self.close_video()
        print_out('VideoCaptureServer.run() END.')


def on_runner(server_queue, server_exit, filename, api_preference, sleep, reopen):
    print_out('on_runner() BEGIN.')
    VideoCaptureServer(server_queue, server_exit, filename, api_preference, sleep, reopen).run()
    print_out('on_runner() END.')


if __name__ == '__main__':
    pass
