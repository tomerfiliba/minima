from flask import Flask, request, make_response
app = Flask(__name__)
from minima import hypertext as H
from minima.page import SimplePage
import json


def webapi(func):
    url = "/api/%s" % (func.__name__,)
    @app.route(url)
    def wrapper(self):
        arg = json.loads(request.data)
        try:
            res = (True, func(self, arg))
        except Exception as ex:
            res = (False, str(ex))
        resp = make_response(json.dumps(res))
        resp.headers['Content-Type'] = 'application/json'
        return resp
    wrapper.url = url
    return wrapper

class JExp(object):
    def __init__(self, text):
        self._text = text
    def __str__(self):
        return self._text
    def __getattr__(self, name):
        return JExp("%s.%s" % (self, name))
    def __call__(self, *args):
        return JExp("%s(%s)" % (self, ", ".join(json.dumps(a) for a in args)))

def JQ(selector):
    return JExp('$(%s)' % (json.dumps(selector),))
def function(*stmts):
    return JExp("function(){%s;}" % (";\n".join(stmts)))
def ajaxCall(url, obj):
    return 'ajaxCall("%s", %s)' % (url, obj)

#print JQ("#foo").click(function("ajaxCall('/api/foo')"))
#exit()

class PasswordForm(object):
    def __init__(self, page):
        self.page = page
    def _id_for(self, type):
        return "%s-%s" % (type, id(self))
    
    def render(self):
        with H.p:
            H.TEXT("Enter your password")
            H.input(type = "text", id = self._id_for("text"))
            with H.button(id = self._id_for("send")):
                H.TEXT("send")
    
    def bind(self):
        #with JS:
        #    sendid = 
        #    with function():
        j = JQ("#" + self._id_for("send")).click(
            function('ajaxCall("%s").success' % (self.check_password.url,))
        )
        self.page.add_js(j)
    
    @webapi
    def check_password(self, value):
        if value == "moshe":
            return "Correct"
        else:
            return "Wrong"


@app.route("/")
def hello():
    pg = SimplePage(title = "Angry Birds")
    #pg.add_js("/static/js/jquery-2.0.0.min.js")
    #pg.add_js("/static/js/bootstrap.min.js")
    #pg.add_js("/static/js/underscore-min.js")
    pg.add_css("/static/css/bootstrap.min.css")
    
    with pg.header:
        H.h1("Das Heading")
    
    with pg.content:
        with H.p:
            H.TEXT("This is the first paragraph")
        with H.p:
            H.TEXT("This is the second paragraph")
        with H.p:
            H.TEXT("This is the third paragraph")

    with pg.footer:
        H.TEXT("(C) 2013, Tomer Filiba")
    
    return str(pg)


if __name__ == "__main__":
    #app.run(debug = True)
    print dir(hello)
    #print hello()


