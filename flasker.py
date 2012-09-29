from flask import Flask, request, url_for
app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<path:name>')
def hello(name=None):
    return 'Foobar %s' % (name,)

@app.route('/')
def index(): 
    pass

@app.route('/login')
def login(): 
    pass

@app.route('/user/<username>')
def profile(username): pass

with app.test_request_context():
    print url_for('index')
    print url_for('login')
    print url_for('login', next='/')
    print url_for('profile', username='doe', lar="moshe")

if __name__ == "__main__":
    app.run(debug=True)

