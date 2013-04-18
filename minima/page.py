import srcgen.hypertext as h


class ExtensionPoint(object):
    def __init__(self, name):
        self.name = name
        self.roots = []
    def __repr__(self):
        return "ExtensionPoint(%r)" % (self.name,)
    def __enter__(self):
        if hasattr(self, "_rec"):
            raise TypeError("%r cannot be recursively embedded" % (self,))
        self._rec = h.recording()
        self._roots = self._rec.__enter__()
        return self
    def __exit__(self, t, v, tb):
        self._rec.__exit__(t, v, tb)
        self.roots.extend(self._roots)
        del self._rec, self._roots
    def __call__(self):
        for r in self.roots:
            h.EMBED(r)
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

    def __str__(self):
        return str(self.render())

    def render(self):
        with h.html as doc:
            with h.head:
                h.meta(http_equiv = "Content-Type", content = "text/html; charset=utf-8")
                h.title(self.title)
                for href in self.stylesheets:
                    h.link(rel="stylesheet", href = href, type = "text/css")
                for href in self.head_scripts:
                    h.script(type = "text/javascript", src = href)
                self.extra_head()
            with h.body:
                with h.div.page_wrapper:
                    with h.div.header:
                        self.header()
                    with h.div.content:
                        self.content()
                    with h.div.footer:
                        self.footer()
                    self.extra_body()
                for href in self.body_scripts:
                    h.script(type = "text/javascript", src = href)
        return doc

class Component(object):
    pass

jquery_cdn = "//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"
class EditableList(Component):
    required_js = [jquery_cdn]




if __name__ == "__main__":
    pg = SimplePage(title = "Angry Birds")
    pg.add_css("http://cdn.google.com/style.css")
    
    with pg.header:
        h.h1("Das Heading")
    
    with pg.content:
        with h.p:
            h.TEXT("This is the first paragraph")
        with h.p:
            h.TEXT("This is the second paragraph")
        with h.p:
            h.TEXT("This is the third paragraph")
    
    with pg.footer:
        h.TEXT("(C) 2013, Tomer Filiba")

    print pg











