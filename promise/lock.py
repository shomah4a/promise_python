# -*- coding: utf-8 -*-

import threading
import functools


def init_synchronize(f):

    @functools.wraps(f)
    def func(self, *argl, **argd):

        self.__lock = threading.RLock()
        f(self, *argl, **argd)

    return func


def synchronizemethod(f):

    @functools.wraps(f)
    def with_sync(self, *argl, **argd):

        with self.__lock:
            return f(self, *argl, **argd)

    return with_sync



def synchronize(f):

    lock = threading.RLock()

    @functools.wraps(f)
    def synchronized(*argl, **argd):
        with lock:
            return f(*argl, **argd)

    return synchronized
