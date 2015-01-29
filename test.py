# -*- coding: utf-8 -*-

import time

from promise import promise, utils


def hoge(x):
    print 'in promise'
    return x + 10


def p(v):
    print v


@promise.promisize
def add_prom(x, y):
    return x + y


def generator():

    a = yield add_prom('aiueo', 'kakikukeko')
    b = yield add_prom('naninuneno', 'hahifuheho')

    time.sleep(1)

    yield add_prom(a, b)


def end_async(v):

    print 'async finished:', v


def main():

    promise.promise(hoge, 20).then(p)
    add_prom('あいうえお', 'なにぬねの').then(p)

    utils.async(generator).then(end_async)


if __name__ == '__main__':
    main()
