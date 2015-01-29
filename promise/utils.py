# -*- coding: utf-8 -*-

from . import promise


def onerror(e):

    print e


def __next(val, it):

    def _f(v):
        try:
            prom = it.send(v)
            __next(prom, it)
        except StopIteration:
            print 'owari'

    val.then(_f)
    val.onerror(onerror)


def __async(gen, *argl, **argd):
    it = gen(*argl, **argd)
    val = it.next()

    __next(val, it)



def async(gen, *argl, **argd):

    return promise.promise(__async, gen, *argl, **argd)
