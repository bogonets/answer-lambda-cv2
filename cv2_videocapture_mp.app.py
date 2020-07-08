# -*- coding: utf-8 -*-
# @see <https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html>

import sys
import multiprocessing as mp
from multiprocessing.sharedctypes import Value
from ctypes import c_bool
from queue import Empty
import numpy as np
import cv2

import cv2_videocapture_server


API_NAME_TO_NUM = {
    'default': 0,
    'ffmpeg': cv2.CAP_FFMPEG,
    'images': cv2.CAP_IMAGES,
    'dshow': cv2.CAP_DSHOW,
}
API_NUM_TO_NAME = {v: k for k, v in API_NAME_TO_NUM.items()}

DEFAULT_MAX_QUEUE_SIZE = 4
DEFAULT_EXIT_TIMEOUT_SECONDS = 4.0

filename = ''
api_preference = API_NAME_TO_NUM['default']
sleep = 0
reopen = True
max_queue_size = DEFAULT_MAX_QUEUE_SIZE
exit_timeout_seconds = DEFAULT_EXIT_TIMEOUT_SECONDS


def print_out(message):
    sys.stdout.write(message)
    sys.stdout.flush()


def print_error(message):
    sys.stderr.write(message)
    sys.stderr.flush()


def on_set(key, val):
    if key == 'filename':
        global filename
        filename = str(val)
    elif key == 'api_preference':
        global api_preference
        api_preference = API_NAME_TO_NUM[val]
    if key == 'sleep':
        global sleep
        sleep = int(val)
    if key == 'reopen':
        global reopen
        reopen = bool(val)
    if key == 'max_queue_size':
        global max_queue_size
        max_queue_size = int(val)
    if key == 'exit_timeout_seconds':
        global exit_timeout_seconds
        exit_timeout_seconds = float(val)


def on_get(key):
    if key == 'filename':
        return filename
    elif key == 'api_preference':
        return API_NUM_TO_NAME[api_preference]
    if key == 'sleep':
        return str(sleep)
    if key == 'reopen':
        return str(reopen)
    if key == 'max_queue_size':
        return str(max_queue_size)
    if key == 'exit_timeout_seconds':
        return str(exit_timeout_seconds)


EMPTY_ARRAY = np.zeros((300, 300, 3), dtype=np.uint8)
server_process: mp.Process
server_queue: mp.Queue
server_exit: Value
server_last_data = EMPTY_ARRAY


def run_process():
    global max_queue_size
    queue_size = max_queue_size if max_queue_size > 0 else DEFAULT_MAX_QUEUE_SIZE

    global server_process, server_queue, server_exit
    global filename, api_preference, sleep, reopen

    server_queue = mp.Queue(queue_size)
    server_exit = Value(c_bool, False)
    server_process = mp.Process(target=cv2_videocapture_server.on_runner,
                                args=(server_queue, server_exit, filename, api_preference, sleep, reopen,))
    server_process.start()

    print_out(f'cv2.videocapture_mp process PID is {server_process.pid}.')
    return server_process.is_alive()


def close_process():
    global server_exit
    server_exit = True

    global exit_timeout_seconds
    timeout = exit_timeout_seconds if exit_timeout_seconds > 0.0 else DEFAULT_EXIT_TIMEOUT_SECONDS

    global server_process
    print_out(f'cv2.videocapture_mp(pid={server_process.pid}) Join(timeout={timeout}s) ...')
    server_process.join(timeout=timeout)

    global server_queue
    server_queue.close()
    server_queue.cancel_join_thread()
    server_queue = None

    if server_process.is_alive():
        print_error(f'cv2.videocapture_mp(pid={server_process.pid}) Kill ...')
        server_process.kill()

    # A negative value -N indicates that the child was terminated by signal N.
    print_out(f'cv2.videocapture_mp(pid={server_process.pid}) Exit Code: {server_process.exitcode}')

    server_process.close()
    server_process = None


def pop_array():
    global server_queue, server_last_data
    try:
        data = server_queue.get_nowait()
    except Empty:
        data = None

    if data is not None:
        server_last_data = data

    return server_last_data


def on_init():
    return run_process()


def on_valid():
    global server_process
    return server_process.is_alive()


def on_run():
    return {'frame': pop_array()}


def on_destroy():
    close_process()


if __name__ == '__main__':
    pass
