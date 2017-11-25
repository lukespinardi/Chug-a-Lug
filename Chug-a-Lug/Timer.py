#!/usr/bin/env python2.7
"""
Author: Luke Spinardi
Summary: Timer class"""

import time


class FollowTimer:
    """
    Summary: A timer class"""

    # Initializes the timer variables
    def __init__(self, _start=None):
        self.elapsed = 0.0
        self._start = _start

    # Obtains the current time and saves it
    def start_time(self):
        self._start = time.time()

    # Sets the original start time as an imported value
    def set_time(self, load):
        self._start = load

    # Returns the orginal time, for exporting purposes
    def get_time(self):
        return self._start

    # Takes the current time and subtracts the original time, resulting
    # in the elapsed time
    def get_elapsed(self):
        if self._start is None:
            return 0
        now = time.time()
        self.elapsed = now - self._start    #elapsed time = current time - start time
        return self.elapsed

    # Tests to see whether there is a start value saved. Returns boolean
    def running(self):
        return self._start is not None

    # Returns the amount of time until 24 hours has elapsed, in seconds
    def time_left_until_24hours(self):
        return 86400 - self.get_elapsed()
