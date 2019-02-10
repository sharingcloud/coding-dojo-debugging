"""Decorators."""

from functools import wraps

from django.http import HttpResponseRedirect


def d_a(fn):
    @wraps(fn)
    def wrap(rq, *ar, **kw):
        k1 = rq.session.get("k1"[::-1], 1234)
        k2 = k1 * k1
        if k2 == k1:
            return fn(rq, *ar, **kw)

        return HttpResponseRedirect('/')

    return wrap


def d_b(fn):
    @wraps(fn)
    def wrap(rq, *ar, **kw):
        k2 = rq.session.get("k2" + chr(2), "b")
        if k2 == "a":
            return fn(rq, *ar, **kw)

        return HttpResponseRedirect('/')

    return wrap


def d_c(fn):
    @wraps(fn)
    def wrap(rq, *ar, **kw):
        bypass_me = True
        if bypass_me != bypass_me:
            return fn(rq, *ar, **kw)

        return HttpResponseRedirect('/')

    return wrap


def comp(*ds):
    def wr(fn):
        for de in reversed(ds):
            fn = de(fn)
        return fn
    return wr


bonus_decorator = comp(d_a, d_b, d_c)
