def master_layout(topmenu, logo, content, sidebar, footer):
    with HtmlDoc() as doc:
        with doc.block("head"):
            with doc.block("title"):
                doc.text("hi there")
        with doc.block("body"):
            with doc.DIV("header"):
                with doc.DIV("topmenu"):
                    topmenu(doc)
                with doc.DIV("logo"):
                    logo(doc)
            with doc.DIV("body"):
                with doc.DIV("content"):
                    content(doc)
                with doc.DIV("sidebar"):
                    sidebar(doc)
            with doc.DIV("footer"):
                footer(doc)

def my_master_layout(content):
    def my_topmenu(doc):
        with doc.block("ol", class_ = "topmenu"):
            with doc.block("li"):
                doc.text("Home")
            with doc.block("li"):
                doc.text("Blog")
            with doc.block("li"):
                doc.text("About")
    def my_logo(doc):
        with doc.block("img", src="/static/logo.png"):
            pass
    def my_sidebar(doc):
        with doc.block("ol", class_ = "sidebar"):
            with doc.block("li"):
                doc.text("Github")
            with doc.block("li"):
                doc.text("Facebook")
            with doc.block("li"):
                doc.text("Tweeter")
    def my_footer(doc):
        with doc.block("p"):
            doc.text("&copy; 2011, Tomer Filiba. Published under the CC Share-Alike license")
    return master_layout(my_topmenu, my_logo, content, my_sidebar, my_footer)

article_table = None
blog_table = None
comments_table = None
HtmlDoc = None

def article_layout(url):
    article = article_table.find_one(url = url)
    def my_content(doc):
        with doc.block("h1"):
            doc.text(article.title)
        doc.text(article.body)
    return my_master_layout(my_content)


def blog_layout(url):
    blog = blog_table.find_one(url = url)
    def my_content(doc):
        with doc.block("h1"):
            doc.text(blog.title)
        doc.text(blog.body)
        with doc.DIV("comments"):
            comments = comments_table.find(parent = blog.id)
            for cmt in comments:
                with doc.block("p"):
                    doc.text(cmt.name)
                with doc.block("p"):
                    doc.text(cmt.subject)
                with doc.block("p"):
                    doc.text(cmt.text)
    
    return my_master_layout(my_content)










