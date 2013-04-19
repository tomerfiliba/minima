import threading
from minima import hypertext


class Component(object):
    REQUIRED_JS = []
    REQUIRED_CSS = []
    def __init__(self, eid = None):
        if not eid:
            eid = "auto-%d" % (id(self),)
        self.eid = eid
    
    def get_required_js(self):
        return self.REQUIRED_JS
    def get_required_css(self):
        return self.REQUIRED_CSS

_per_thread = threading.local()

class ContainerComponent(Component):
    def __init__(self):
        self._subcomponents = []
        if getattr(_per_thread, "stack", None):
            self._parent = _per_thread.stack[-1]
            self._parent._subcomponents.append(self)
        else:
            self._parent = None
    def __enter__(self):
        if not hasattr(_per_thread, "stack"):
            _per_thread.stack = []
        _per_thread.stack.append(self)
        self._rec = hypertext.recording()
        self._roots = self._rec.__enter__()
        return self
    def __exit__(self, t, v, tb):
        self._rec.__exit__(t, v, tb)
        self.roots.extend(self._roots)
        del self._rec, self._roots
        _per_thread.stack.pop(-1)
    def render(self):
        print "!!", self._subcomponents
        for comp in self._subcomponents:
            comp.render()

jquery_cdn = "//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"
class Textbox(Component):
    REQUIRED_JS = [jquery_cdn]
    REQUIRED_CSS = ["../static/css/bootstrap.min.css"]
    
    def __init__(self, eid = None, placeholder = None):
        Component.__init__(self, eid = eid)
        self.placeholder = placeholder
    
    def render(self):
        hypertext.input(type = "text", placeholder = self.placeholder, id = self.eid)


class Form(ContainerComponent):
    def render(self):
        with hypertext.form:
            ContainerComponent.render(self)
