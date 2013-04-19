from flask import Flask, request, make_response
app = Flask(__name__)
from minima import hypertext as H
from minima.page import SimplePage


@app.route("/")
def hello():
    pg = SimplePage(title = "Angry Birds")
    pg.add_css("http://cdn.google.com/style.css")
    
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
    
    resp = make_response(str(pg))
    return resp


if __name__ == "__main__":
    app.run(debug = True)


