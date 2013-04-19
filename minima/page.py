from minima import hypertext


class ExtensionPoint(object):
    def __init__(self, name):
        self.name = name
        self.roots = []
    def __repr__(self):
        return "ExtensionPoint(%r)" % (self.name,)
    def __enter__(self):
        if hasattr(self, "_rec"):
            raise TypeError("%r cannot be recursively embedded" % (self,))
        self._rec = hypertext.recording()
        self._roots = self._rec.__enter__()
        return self
    def __exit__(self, t, v, tb):
        self._rec.__exit__(t, v, tb)
        self.roots.extend(self._roots)
        del self._rec, self._roots
    def __call__(self):
        for r in self.roots:
            hypertext.EMBED(r)
    def clear(self):
        del self.roots[:]

class SimplePage(object):
    EXTENSIONS = ["extra_head", "extra_body", "content", "header", "footer"]
    
    def __init__(self, title = "Untitled"):
        self.title = title
        self.stylesheets = []
        self.head_scripts = []
        self.body_scripts = []
        for ext in self.EXTENSIONS:
            setattr(self, ext, ExtensionPoint(ext))

    def add_css(self, href):
        if href not in self.stylesheets:
            self.stylesheets.append(href)
    def add_js(self, href):
        if href not in self.head_scripts:
            self.head_scripts.append(href)

    def __str__(self):
        return str(self.render())

    def render(self):
        with hypertext.html as doc:
            with hypertext.head:
                hypertext.meta(http_equiv = "Content-Type", content = "text/html; charset=utf-8")
                hypertext.meta(name = "viewport", content="width=device-width, initial-scale=1.0")
                hypertext.title(self.title)
                for href in self.stylesheets:
                    hypertext.link(rel="stylesheet", href = href, type = "text/css")
                for href in self.head_scripts:
                    hypertext.script(type = "text/javascript", src = href)
                self.extra_head()
            with hypertext.body:
                with hypertext.div.page_wrapper:
                    with hypertext.div.header:
                        self.header()
                    with hypertext.div.content:
                        self.content()
                    with hypertext.div.footer:
                        self.footer()
                    self.extra_body()
                for href in self.body_scripts:
                    hypertext.script(type = "text/javascript", src = href)
        return doc









