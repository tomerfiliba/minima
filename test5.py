class MasterLayout(object):
    def __init__(self, provider):
        self.provider = provider
    
    def render(self, doc):
        with doc.block("head"):
            with doc.block("title"):
                doc.text(self.get_title())
        with doc.block("body"):
            with doc.DIV("page"):
                with doc.DIV("header"):
                    with doc.DIV("topmenu"):
                        self.render_topmenu(doc)
                    with doc.DIV("logo"):
                        self.render_logo(doc)
                with doc.DIV("body"):
                    with doc.DIV("content"):
                        self.render_content(doc)
                    with doc.DIV("sidebar"):
                        self.render_sidebar(doc)
                with doc.DIV("footer"):
                    self.render_footer(doc)
    
    def render_footer(self, doc):
        with doc.block("p"):
            doc.text("(C) 2011, Tomer Filiba. Published under the CC 3.0 Share-Alike license")
    
    def render_logo(self, doc):
        doc.elem("img", src="/static/logo.png", title="My logo")
    
    def render_topmenu(self, doc):
        with doc.block("ol"):
            with doc.block("li"):
                doc.link("/", "Home")
            with doc.block("li"):
                doc.link("/blog", "Blog")
            with doc.block("li"):
                doc.link("/about", "About")
            
import cherrypy

class Dispatcher(object):
    exposed = True


class BlogDispatcher(Dispatcher):
    @cherrypy.expose
    def default(self, *path, **kwargs):
        return "BlogDispatcher: %r, %r\n\n%r" % (path, kwargs, cherrypy.request.headers)


class RootDispatcher(Dispatcher):
    @cherrypy.expose
    def index(self):
        return "index"

    blog = BlogDispatcher()


if __name__ == "__main__":
    cherrypy.quickstart(RootDispatcher())







