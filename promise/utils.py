# -*- coding: utf-8 -*-

from . import promise


def __retval(v, err=None):

    if err is not None:
        raise err

    return v


def __next(result, val, it):

    def _f(v):
        try:
            prom = it.send(v)
            __next(result, prom, it)
        except KeyboardInterrupt:
            pass
        except StopIteration:
            result.run(v)
        except Exception, e:
            result.run(None, e)

    def _e(err):
        result.run(None, err)

    val.then(_f, _e)


def __async(gen, result, *argl, **argd):

    try:
        it = gen(*argl, **argd)
        val = it.next()
        __next(result, val, it)
    except KeyboardInterrupt:
        pass
    except StopIteration:
        pass
    except Exception, e:
        result.run(None, e)



def async(gen, *argl, **argd):

    result = promise.Promise(__retval)

    promise.promise(__async, gen, result, *argl, **argd)

    return result
