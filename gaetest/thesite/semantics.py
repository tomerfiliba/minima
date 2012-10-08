import threading
import itertools
from minima.hypertext import html, head, body, clean_stack, meta, title, script, link, div


_per_thread = threading.local()

class SemanticElement(object):
    REQUIRED_LIBS = []
    REQUIRED_CSS = []
    
    _counter = itertools.count()
    def __init__(self):
        self.id = "id%s_%d" % (self.__class__.name, self._counter.next())
        self.children = []
        if getattr(_per_thread, "stack", None):
            _per_thread.stack[-1].children.append(self)
    def __str__(self):
        return "%s[%s]" % (self.__class__.__name__, ", ".join(str(c) for c in self.children))
    def __enter__(self):
        if not hasattr(_per_thread, "stack"):
            _per_thread.stack = []
        _per_thread.stack.append(self)
        return self
    def __exit__(self, t, v, tb):
        _per_thread.stack.pop(-1)
    
    def prepare(self, doc):
        self._prepare(doc)
        for url in self.REQUIRED_LIBS:
            self.require_script(url)
        for css in self.REQUIRED_CSS:
            if isinstance(css, str):
                self.require_css(css)
            else:
                self.require_css(*css)
        for child in self.children:
            child.prepare(doc)
    def _prepare(self, doc):
        pass
    def to_html(self, doc):
        pass


JQUERY = "http://code.jquery.com/jquery-1.8.2.js"
JQUERY_UI = "http://code.jquery.com/ui/1.9.0/jquery-ui.js"
JQUERY_UI_CSS = "http://code.jquery.com/ui/1.9.0/themes/base/jquery-ui.css"


class Document(SemanticElement):
    def __init__(self, title = None):
        self.title = title
        self.stylesheets = []
        self.libraries = []
        self.scripts = []
    
    def require_script(self, url):
        if url not in self.libraries:
            self.libraries.append(url)
    
    def require_css(self, url, media = "all"):
        if (url, media) not in self.libraries:
            self.stylesheets.append((url, media))
    
    def to_html(self):
        for child in self.children:
            child.prepare(self)

        with clean_stack():
            with html(lang="en"):
                with head:
                    meta(charset="utf-8")
                    meta(http_equiv="content-type", content="text/html; charset=utf-8")
                    title(self.title)
                    for url, media in self.stylesheets:
                        link(rel="stylesheet", href=url, type='text/css', media=media)
                    for url in self.libraries:
                        script("", src=url, type="text/javascript")
                    for code in self.scripts:
                        script(code, src=url, type="text/javascript")
                with body:
                    for child in self.children:
                        child.render()

class Accordion(SemanticElement):
    REQUIRED_CSS = []
    REQUIRED_LIBS = []
    
    def prepare(self, doc):
        doc.scripts.append("""$(function() { $( "#%s" ).accordion(); });""" % (self.id,))
    
    def to_html(self, doc):
        for child in self.children:
            child.prepare(self, doc)

        with div(id=self.id):
            for child in self.children:
                child.to_html(doc)

class AccordionSection(SemanticElement):
    def __init__(self, title):
        self.title = title
    
    def prepare(self, doc):
        for child in self.children:
            child.prepare(doc)
    def to_html(self, doc):
        h3(self.title)
        with div:
            
        

class AutocompleteTextbox(SemanticElement):
    def __init__(self, placeholder, ajaxurl):
        self.placeholder = placeholder
        self.ajaxurl = ajaxurl


'''
<head>
    <meta charset="utf-8" />
    <title>jQuery UI Accordion - Default functionality</title>
    <link rel="stylesheet" href="http://code.jquery.com/ui/1.9.0/themes/base/jquery-ui.css" />
    <script src="http://code.jquery.com/jquery-1.8.2.js"></script>
    <script src="http://code.jquery.com/ui/1.9.0/jquery-ui.js"></script>
    <link rel="stylesheet" href="/resources/demos/style.css" />
    <script>
    $(function() {
        $( "#accordion" ).accordion();
    });
    </script>
</head>
<body>
 
<div id="accordion">
    <h3>Section 1</h3>
    <div>
        <p>
        Mauris mauris ante, blandit et, ultrices a, suscipit eget, quam. Integer
        ut neque. Vivamus nisi metus, molestie vel, gravida in, condimentum sit
        amet, nunc. Nam a nibh. Donec suscipit eros. Nam mi. Proin viverra leo ut
        odio. Curabitur malesuada. Vestibulum a velit eu ante scelerisque vulputate.
        </p>
    </div>
    <h3>Section 2</h3>
    <div>
        <p>
        Sed non urna. Donec et ante. Phasellus eu ligula. Vestibulum sit amet
        purus. Vivamus hendrerit, dolor at aliquet laoreet, mauris turpis porttitor
        velit, faucibus interdum tellus libero ac justo. Vivamus non quam. In
        suscipit faucibus urna.
        </p>
    </div>
    <h3>Section 3</h3>
    <div>
        <p>
        Nam enim risus, molestie et, porta ac, aliquam ac, risus. Quisque lobortis.
        Phasellus pellentesque purus in massa. Aenean in pede. Phasellus ac libero
        ac tellus pellentesque semper. Sed ac felis. Sed commodo, magna quis
        lacinia ornare, quam ante aliquam nisi, eu iaculis leo purus venenatis dui.
        </p>
        <ul>
            <li>List item one</li>
            <li>List item two</li>
            <li>List item three</li>
        </ul>
    </div>
    <h3>Section 4</h3>
    <div>
        <p>
        Cras dictum. Pellentesque habitant morbi tristique senectus et netus
        et malesuada fames ac turpis egestas. Vestibulum ante ipsum primis in
        faucibus orci luctus et ultrices posuere cubilia Curae; Aenean lacinia
        mauris vel est.
        </p>
        <p>
        Suspendisse eu nisl. Nullam ut libero. Integer dignissim consequat lectus.
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos.
        </p>
    </div>
</div>
 
 
</body>
</html>
'''
        
with Document() as doc:
    with Accordion():
        with Section("title 1"):
            pass

        with Section("title 2"):
            pass

        with Section("title 3"):
            pass




















