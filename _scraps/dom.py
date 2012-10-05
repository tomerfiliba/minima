import threading
import itertools


_per_thread = threading.local()

class Layout(object):
    _counter = itertools.count()
    def __init__(self, id = None):
        self.id = id if id else "auto_%s_%r" % (self.__class__.__name__, self._counter.next())
        self.children = []
        if getattr(_per_thread, "_stack", None):
            _per_thread._stack[-1].children.append(self)
    def __enter__(self):
        if not hasattr(_per_thread, "_stack"):
            _per_thread._stack = []
        _per_thread._stack.append(self)
        return self
    def __exit__(self, t, v, tb):
        _per_thread._stack.pop(-1)

def THIS():
    return _per_thread._stack[-1]
def PARENT(count = 1):
    return _per_thread._stack[-1 - count]


class Page(Layout):
    def __init__(self):
        Layout.__init__(self)
        self.scripts = []

class Section(Layout):
    def __init__(self, title):
        self.title = title









