#!/usr/bin/env python
#-*-coding:utf8-*-

""" Event registration """

class CallbackBase:
    def __init__(self):
        self.__callbackMap = {}
        for k in (getattr(self, x) for x in dir(self)):
            if hasattr(k, "bind_to_event"):
                self.__callbackMap.setdefault(k.bind_to_event, []).append(k)

    ## staticmethod is only used to create a namespace
    @staticmethod
    def callback(event):
        def f(g, ev = event):
            g.bind_to_event = ev
            return g
        return f

    def dispatch(self, event):
        l = self.__callbackMap[event]
        f = lambda *args, **kargs: \
        map(lambda x: x(*args, **kargs), l)
        return f

