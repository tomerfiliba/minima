from contextlib import contextmanager

MAPPINGS = {
    "&" : "&amp;",
    "'" : "&apos;",
    '"' : "&quot;",
    "<" : "&lt;",
    ">" : "&gt;",
}

def xml_escape(text):
    return "".join(MAPPINGS.get(ch, ch) for ch in text)

class XmlText(object):
    def __init__(self, text, *args, **kwargs):
        text = str(text)
        if args:
            text = text.format(*args)
        self.text = text
        self.escape = kwargs.pop("escape", True)
        if kwargs:
            raise TypeError("invalid keyword argument(s): %r" % (kwargs.keys(),))
    def render(self, lean = False):
        if self.escape:
            return [xml_escape(self.text)]
        else:
            return [self.text]

class XmlComment(object):
    def __init__(self, text, *args):
        text = str(text)
        if args:
            text = text.format(*args)
        self.text = text
    def render(self, lean = False):
        return ["<!-- %s -->" % (xml_escape(self.text),)]

class XmlBlock(object):
    def __init__(self, _tag, **attrs):
        self.tag = _tag.lower()
        self.attrs = {}
        self.children = []
        self.stack = []
        self.attr(**attrs)
    
    def _get_head(self):
        return self.stack[-1] if self.stack else self

    def attr(self, **kwargs):
        head = self._get_head()
        for k, v in kwargs.items():
            if k.endswith("_"): # to allow for kwargs named 'class_' or 'if_'
                k = k[:-1]
            head.attrs[k.lower()] = str(v)
    def text(self, *args, **kwargs):
        self._get_head().children.append(XmlText(*args, **kwargs))
    def comment(self, *args, **kwargs):
        self._get_head().children.append(XmlComment(*args, **kwargs))
    def elem(self, *args, **attrs):
        with self.block(*args, **attrs):
            pass

    @contextmanager
    def block(self, *args, **kwargs):
        blk = XmlBlock(*args, **kwargs)
        self._get_head().children.append(blk)
        self.stack.append(blk)
        yield blk
        self.stack.pop(-1)
    
    def render(self, lean = False):
        attrs = " ".join('%s="%s"' % (k, xml_escape(v)) 
            for k, v in sorted(self.attrs.items()))
        if attrs:
            attrs = " " + attrs
        if self.children:
            lines = ["<%s%s>" % (self.tag, attrs)]
            ind = "" if lean else "\t"
            for child in self.children:
                lines.extend((ind + l) for l in child.render(lean))
            lines.append("</%s>" % (self.tag,))
        else:
            lines = ["<%s%s />" % (self.tag, attrs)]
        return lines


class XmlDoc(XmlBlock):
    ENCODING = '<?xml version="1.0" encoding="UTF-8"?>'

    def __enter__(self):
        return self
    def __exit__(self, t, v, tb):
        pass
    def render(self, lean = False):
        sep = "" if lean else "\n"
        text = self.ENCODING + "\n" + sep.join(XmlBlock.render(self, lean))
        return text.encode("utf-8") 


class HtmlDoc(XmlBlock):
    DOCTYPE = ('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
        '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')

    def __init__(self):
        XmlBlock.__init__(self, "html", xmlns = "http://www.w3.org/1999/xhtml")
    def __enter__(self):
        return self
    def __exit__(self, t, v, tb):
        pass
    def render(self):
        return self.DOCTYPE + "\n" + "\n".join(XmlBlock.render(self))








