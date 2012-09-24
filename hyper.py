import threading


MAPPINGS = {
    "&" : "&amp;",
    "'" : "&apos;",
    '"' : "&quot;",
    "<" : "&lt;",
    ">" : "&gt;",
}

def xml_escape(text):
    return "".join(MAPPINGS.get(ch, ch) for ch in text)

_perthread = threading.local()

class Element(object):
    class __metaclass__(type):
        __slots__ = ()
        def __getattr__(cls, name):
            return cls(class_ = name)
        def __enter__(cls):
            return cls().__enter__()
        def __exit__(cls, t, v, tb):
            _perthread._stack.pop(-1)

    __slots__ = ["_attrs", "_elems"]
    TAG = None
    DEFAULT_ATTRS = {}
    
    def __init__(self, *elems, **attrs):
        self._attrs = self.DEFAULT_ATTRS.copy()
        self._elems = []
        self(*elems, **attrs)
        if getattr(_perthread, "_stack", None):
            _perthread._stack[-1]._elems.append(self)
    
    def __enter__(self):
        if not hasattr(_perthread, "_stack"):
            _perthread._stack = []
        _perthread._stack.append(self)
        return self
    def __exit__(self, t, v, tb):
        _perthread._stack.pop(-1)
    
    def __str__(self):
        _perthread.indent = getattr(_perthread, "indent", 0) + 1
        indent = "  " * _perthread.indent
        tag = self.TAG if self.TAG else self.__class__.__name__.lower()
        try:
            attrs = " ".join('%s="%s"' % (k, xml_escape(str(v))) for k, v in self._attrs.items())
            elements = ("\n" + indent).join(xml_escape(e) if isinstance(e, str) else str(e) 
                for e in self._elems)
            if self._elems:
                return "<%s %s>\n%s%s\n%s</%s>" % (tag, attrs, indent, elements,
                    "  " * (_perthread.indent - 1), tag)
            else:
                return "<%s %s/>" % (tag, attrs)
        finally:
            _perthread.indent -= 1
    
    def __iadd__(self, elem):
        self._elems.append(elem)
    def __getitem__(self, name):
        return self._attrs[name]
    def __delitem__(self, name):
        del self._attrs[name]
    def __setitem__(self, name, value):
        self._attrs[name] = value
    
    def __call__(self, *elems, **attrs):
        self._elems.extend(elems)
        for k, v in attrs.items():
            if k.endswith("_"):
                k = k[:-1]
            self._attrs[k] = v
        return self
    def __getattr__(self, name):
        if "class" in self._attrs:
            self._attrs["class"] += " " + name
        else:
            self._attrs["class"] = name
        return self

def TEXT(text):
    _perthread._stack[-1]._elems.append(text)

class html(Element): pass
class head(Element): pass
class link(Element): pass
class meta(Element): pass
class title(Element): pass
class script(Element): DEFAULT_ATTRS = {"type" : "text/javascript"}
class body(Element): pass
class p(Element): pass
class div(Element): pass
class span(Element): pass
class a(Element): pass
class br(Element): pass


if __name__ == "__main__":
    with html as doc:
        with div.foo(id = "floop"):
            for i in range(10):
                TEXT("hello")
                br()
                TEXT("world")
    
    print doc



