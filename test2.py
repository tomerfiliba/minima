class Dispatcher(object):
    def default(self, *args, **kwargs):
        pass

class BasicLayout(object):
    pass

class BlogPostLayout(BasicLayout):
    def layout_content(self, doc, text, comments):
        with doc.block("div", class_="blogtext"):
            doc.text(text)
        with doc.block("div", class_="comments"):
            for cmt in comments:
                with doc.block("div", class_="comment"):
                    doc.text(cmt)
            with doc.block("div", class_="comment-form"):
                with doc.block("form"):
                    with doc.block("input", type="text", id="name"):
                        pass
                    with doc.block("input", type="text", id="email"):
                        pass
                    with doc.block("input", type="textarea", id="text"):
                        pass
                    with doc.block("input", type="submit"):
                        pass


class BlogLayout(BasicLayout):
    def layout_content(self, doc, ):

