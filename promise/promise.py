# -*- coding: utf-8 -*-

import threading
import functools
import traceback

from . import lock


EMPTY = []


class Promise(object):


    @lock.init_synchronize
    def __init__(self, f):

        self.func = f
        self.__next = None
        self.__onerror = None
        self.__thread = None
        self.__value = EMPTY
        self.__error = EMPTY


    @lock.synchronizemethod
    def __set_value(self, value):

        if self.__value is EMPTY:
            self.__value = value

        self.__run_next()


    @lock.synchronizemethod
    def __set_error(self, err):

        if self.__error is EMPTY:
            self.__error = err

        self.__run_onerror()


    @lock.synchronizemethod
    def __run_next(self):
        if self.__value is not EMPTY and self.__next is not None:
            self.__next.run(self.__value)


    @lock.synchronizemethod
    def __run_onerror(self):
        if self.__error is not EMPTY:
            if self.__onerror is not None:
                self.__onerror.run(self.__error)
            else:
                traceback.print_exc()


    def __run(self, *argl, **argd):

        try:
            ret = self.func(*argl, **argd)
            self.__set_value(ret)
        except KeyboardInterrupt:
            pass
        except StopIteration:
            pass
        except Exception, e:
            self.__set_error(e)


    @lock.synchronizemethod
    def run(self, *argl, **argd):

        if self.__thread is None:
            self.__thread = threading.Thread(target=self.__run, args=argl, kwargs=argd)
            self.__thread.start()


    @lock.synchronizemethod
    def then(self, handle, error=None):

        if self.__next is None:
            self.__next = Promise(handle)

        if self.__onerror is None and error is not None:
            self.__onerror = Promise(error)

        self.__run_next()
        self.__run_onerror()

        return self.__next


def promise(func, *argl, **argd):

    p = Promise(func)
    p.run(*argl, **argd)
    return p


def promisize(f):

    @functools.wraps(f)
    def promisized(*args, **argd):
        return promise(f, *args, **argd)

    return promisized
