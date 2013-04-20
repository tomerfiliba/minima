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
        if not hasattr(_per_thread, "stack"):
            _per_thread.stack = []
        _per_thread.stack.append(self)
        return self
    def __exit__(self, t, v, tb):
        _per_thread.stack.pop(-1)
    def __str__(self):
        return "".join(self._render(0))
    def _render(self, level, compact = True):
        for stmt in self._stmts:
            if isinstance(stmt, JS):
                for line in stmt._render(level + 1):
                    yield line
            else:
                line = str(stmt)
                if compact:
                    #if line == "\n":
                    #    continue
                    yield line
                else:
                    yield ("    " * level) + line

def stmt(text, *args, **kwargs):
    end = kwargs.pop("end", ";")
    if args:
        text %= args
    if text.strip() and text.strip()[-1] not in ";:{([":
        text += end
    stmts = _per_thread.stack[-1]._stmts
    stmts.append(text)
    stmts.append("\n")

@contextmanager
def suite(header, *args, **kwargs):
    begin = kwargs.pop("begin", " {")
    end = kwargs.pop("end", "}")
    embed = kwargs.pop("embed", False)
    if args:
        header %= args
    stmts = _per_thread.stack[-1]._stmts
    if embed and stmts and stmts[-1] == "\n":
        stmts.pop(-1)
    stmts.append("%s%s" % (header, begin))
    stmts.append("\n")
    
    with JS() as body:
        yield body
    if end:
        stmts.append(end)
    stmts.append("\n")

def function(name, *args):
    return suite("function %s(%s)", name, ", ".join(args))

def var(name, val = NotImplemented):
    if val is not NotImplemented:
        return stmt("var %s = %s", name, json.dumps(val))
    else:
        return stmt("var %s", name)


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
    @contextmanager
    def func(self, *args):
        with suite("(function(%s)" % (", ".join(args),), end = "});", embed = True):
            yield self


def JQ(selector):
    return JExpr('$(%s)' % (json.dumps(selector),))

#_ = JExpr("_")

with JS() as x:
    var("x", 5)
    var("y", "hello")
    with function("x", "a", "b"):
        var("z", [])
        with JQ("#foo").click.func("obj"):
            var("q", {"a":1,"b":2})
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




























