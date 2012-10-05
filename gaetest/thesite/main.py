from thesite.base import app
from minima.webapp2_integration import Handler, json_api
from google.appengine.api import users


@app.route("/api/is-logged-in")
class IsLoggedIn(Handler):
    @json_api
    def get(self):
        user = users.get_current_user()
        return repr(user)


@app.route("/")
class MainHandler(Handler):
    def get(self):
        self.response.out.write("hello world")

