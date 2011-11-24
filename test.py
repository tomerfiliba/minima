class View(object):
    def __init__(self, db):
        self.db = db
    def handle(self, request):
        raise NotImplementedError()


class BasicView(object):
    def layout(self, doc):
        def DIV(cls, **kwargs):
            return doc.block(class_ = cls, **kwargs)
        with doc.block("body"):
            with DIV("document", style="width:70em; margin: 0 auto;"):
                with DIV("header"):
                    with DIV("menubar"):
                        self.layout_menubar(doc)
                    with DIV("logo"):
                        self.layout_logo(doc)
                with DIV("body"):
                    with DIV("content"):
                        self.layout_content(doc)
                    with DIV("sidebar"):
                        self.layout_sidebar(doc)
                with DIV("footer"):
                    self.layout_footer(doc)


class BlogView(BasicView):
    def handle(self, request):
        pass

    def layout_content(self, doc):
        pass























