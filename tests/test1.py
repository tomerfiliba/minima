from flask import Flask, request, make_response
app = Flask(__name__)
from minima import hypertext as H
from minima.page import SimplePage


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
    app.run(debug = True)
    #print hello()


