import webapp2


class APIHandler(webapp2.RequestHandler):
    pass

app = webapp2.WSGIApplication([
    ('/api', APIHandler)
], debug=True)


