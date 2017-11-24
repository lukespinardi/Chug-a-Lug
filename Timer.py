#!/usr/bin/env python2.7

import time

class FollowTimer:
    def __init__(self, _start=None):
        self.elapsed = 0.0
        self._start = _start

    def startTime(self):
        self._start = time.time()

    def setTime(self, load):
        self._start = load

    def getTime(self):
        return self._start

    def getElapsed(self):
        if self._start is None:
            return 0
        now = time.time()
        self.elapsed = now - self._start
        return self.elapsed

    def running(self):
        return self._start is not None

    def getRemaining(self):
        return 86400 - self.getElapsed()
