#!/usr/bin/python
# -*- encoding:UTF-8 -*-
import operator

from PIL import Image, ImageChops


class VaildataWay:
    def __init__(self, model):
        self.model = model
        self.op = {'<': operator.lt, '<=': operator.le, '==': operator.eq, '!=': operator.ne, '>': operator.gt,
                   '>=': operator.ge, 'contain': operator.contains}

    def vail_way(self, **kwargs):
        res = False
        for k, val in kwargs['ydata'].items():
            if kwargs['rdata'].__contains__(k):
                if self.op[self.model](val, kwargs['rdata'][k]):
                    res = True
                else:
                    res = False
            else:
                res = False
        return res



    def __call__(self, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            res = self.vail_way(**kwargs)
            return res

        return wrapper


@VaildataWay('<')
def small(ydata, rdata):
    pass


@VaildataWay('>')
def large(ydata, rdata):
    pass


@VaildataWay('<=')
def le(ydata, rdata):
    pass


@VaildataWay('>=')
def ge(ydata, rdata):
    pass


@VaildataWay('==')
def equal(ydata, rdata):
    pass


@VaildataWay('!=')
def ne(ydata, rdata):
    pass


@VaildataWay('contain')
def include(ydata, rdata):
    pass
