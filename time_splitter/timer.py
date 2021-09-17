
import threading
import datetime
import time
import atexit

import PySimpleGUI as sg


class Timer:

    def __init__(self):
        self.overall_elapsed: float = 0.0
        self.current_elapsed: time.perf_counter = 0.0
        self.splits: list = []
        self._current_start_time: time.perf_counter = None
        self._start_time: time.perf_counter = None
        self._running: bool = False
        self._thread: threading.Thread = None

    def start(self):
        if not self._running:
            self.splits = []
            threading.Thread(target=self._start_thread, daemon=True).start()
            atexit.register(self.stop)

    def stop(self):
        self._running = False

    def split(self, desc):
        split = Split(self.current_elapsed, description=desc)
        self.splits.append(split)
        self._current_start_time = time.perf_counter()
        return split

    def _start_thread(self):
        self._running = True
        pc = time.perf_counter()
        self._start_time = pc
        self._current_start_time = pc
        while self._running:
            pc = time.perf_counter()
            st, cst = self._start_time, self._current_start_time
            self.overall_elapsed = round(pc - st, 2)
            self.current_elapsed = round(pc - cst, 2)
            time.sleep(0.01)

class Split:

    def __init__(self, elapsed: float, description: str = None):
        self.split_time: datetime.datetime = datetime.datetime.now()
        self.elapsed = elapsed
        self.description = description


if __name__ == '__main__':
    from random import randint
    timer = Timer()
    timer.start()
    while True:
        try:
            time.sleep(1)
            if randint(0, 10) > 5:
                print('Splitting')
                timer.split()
        except KeyboardInterrupt:
            timer.stop()
            break
    print('Elapsed', timer.overall_elapsed)
    for split in timer.splits:
        print(split.split_time, split.elapsed, split.description)
