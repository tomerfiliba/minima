import json
import threading
from contextlib import contextmanager

_per_thread = threading.local()


class JS(object):
    def __init__(self):
        self._stmts = []
        if getattr(_per_thread, "stack", None):
            self._parent = _per_thread.stack[-1]
            self._parent._stmts.append(self)
        else:
            self._parent = None
    def __enter__(self):
        print ">>>"
        if not hasattr(_per_thread, "stack"):
            _per_thread.stack = []
        _per_thread.stack.append(self)
        return self
    def __exit__(self, t, v, tb):
        print "<<<"
        #_per_thread.stack.pop(-1)
    def __str__(self):
        return "\n".join(self._render(0))
    def _render(self, level):
        for stmt in self._stmts:
            if isinstance(stmt, JS):
                for line in stmt._render(level + 1):
                    yield line
            else:
                yield ("    " * level) + str(stmt)
    
def stmt(text, *args):
    if args:
        text %= args
    _per_thread.stack[-1]._stmts.append("%s;" % (text,))

@contextmanager
def suite(header, *args, **kwargs):
    begin = kwargs.pop("opener", " {")
    end = kwargs.pop("terminator", "}")
    if args:
        header %= args
    _per_thread.stack[-1]._stmts.append("%s%s" % (header, begin))
    with JS() as body:
        yield body
    if end:
        _per_thread.stack[-1]._stmts.append(end)

def function(name, *args):
    return suite("function %s(%s)", name, ", ".join(args))

def if_(cond):
    return suite("if (%s)", cond)
def elif_(cond):
    return suite("elif (%s)", cond)
def else_():
    return suite("else")
def for_(init, next, cond):
    return suite("for (%s; %s; %s)", init, next, cond)
#def foreach(var, coll):
#    return suite("for (%s; %s)", init, next, cond)

class JExpr(object):
    def __init__(self, text):
        self._text = text
        _per_thread.stack[-1]._stmts.append(self)
    def __str__(self):
        return self._text
    def __getattr__(self, name):
        self._text += "." + name
        return self
    def __getitem__(self, index):
        self._text += "[%s]" % (index,)
        return self
    def __setitem__(self, name, val):
        self._text += ".%s = %s" % (name, json.dumps(val))
    def __call__(self, *args):
        self._text += "(%s)" % (", ".join(json.dumps(a) for a in args))
        return self
    def __enter__(self):
        self._ctx = suite("(function()", end = "})").__enter__()
        #return self._ctx
    def __exit__(self, t, v, tb):
        return self._ctx.__exit__(t, v, tb)


def JQ(selector):
    return JExpr('$(%s)' % (json.dumps(selector),))

#_ = JExpr("_")

with JS() as x:
    stmt("var x = 5")
    stmt("var y = 7")
    with function("x", "a", "b"):
        stmt("var z = 5")
        with JQ("#foo").click:
            stmt("var q = 9")
        stmt("return a+b+z")

print x




#class JExpr(object):
#    __slots__ = ["_text"]
#    def __init__(self, text):
#        self._text = text
#    def __str__(self):
#        return self._text
#    def __getattr__(self, name):
#        return JExpr("%s.%s" % (self, name))
#    def __call__(self, *args):
#        return JExpr("%s(%s)" % (self, ", ".join(json.dumps(a) for a in args)))
#    def __enter__(self):
#        JS.__enter__()
#    def __exit__(self, t, v, tb):
#        pass
#
#
#
#print JQ("#foo").click("function(){alert('hi');}")
#
#with JQ("#foo").click():
#    pass




























