from minima.hypertext import UNESCAPED, EMBED, a, head, html, div, body, link, title, meta, small, img, h1

# Mocks {{
from collections import namedtuple
from contextlib import contextmanager
import unittest
class request:
    user = None
class db:
    Art = namedtuple("Art", "title,body")
    articles = [Art("foo", "bar bar bar"), Art("spam", "bacon bacon bacon")]
# }}

def gen_meta_stuff(page_title):
    meta(http_equiv="Content-Type", content="text/html; charset=utf-8")
    if page_title:
        title("Foobar - %s" % (page_title,))
    else:
        title("Foobar")
    link(rel="stylesheet", href="/css/my.css", type="text/css", media="screen")

def gen_header():
    with a(href="/"):
        img(src="/img/logo.png")
    if request.user:
        small("Hello %s" % (request.user,))
    else:
        small(a("Click to log in", href="/login"))

@contextmanager
def base_layout(page_title = ""):
    with html as doc:
        with head:
            gen_meta_stuff(page_title)
        
        with body(id = "body"):
            with div.header:
                gen_header()
            
            with div.content(data_role = "page"):
                # it's a context-manager!
                yield doc
            
            with div.footer:
                UNESCAPED("&copy; 2012 Foobar corp.")

def main_page():
    with base_layout(page_title = "Main") as doc:
        for article in db.articles:
            with div.article:
                h1(article.title)
                EMBED(article.body)
    
    return str(doc)



class TestHypertext(unittest.TestCase):
    def test(self):
        out = main_page()
        self.maxDiff = None
        self.assertEqual(out, 
'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <title>Foobar - Main</title>
    <link media="screen" href="/css/my.css" type="text/css" rel="stylesheet"/>
  </head>
  <body id="body">
    <div class="header">
      <a href="/"><img src="/img/logo.png"/></a>
      <small><a href="/login">Click to log in</a></small>
    </div>
    <div data-role="page" class="content">
      <div class="article">
        <h1>foo</h1>
        bar bar bar
      </div>
      <div class="article">
        <h1>spam</h1>
        bacon bacon bacon
      </div>
    </div>
    <div class="footer">&copy; 2012 Foobar corp.</div>
  </body>
</html>''')


if __name__ == "__main__":
    unittest.main()


