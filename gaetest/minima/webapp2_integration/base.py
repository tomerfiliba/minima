import webapp2
import urllib
import os

IS_DEBUG_SERVER = os.environ['SERVER_SOFTWARE'].startswith('Dev')

class URLStr(str):
    def build(self, **params):
        url = ""
        if "_host" in params:
            url = "http://%s" % (params.pop("_host"),)
        path = self.rstrip("/")
        url += path if path.startswith("/") else "/" + path
        if params:
            url += "?" + urllib.urlencode(params, True)
        return url

class Application(webapp2.WSGIApplication):
    def __init__(self, config = None):
        webapp2.WSGIApplication.__init__(self, [], debug = IS_DEBUG_SERVER, config = config)
        self._registered_urls = set()
    
    #===============================================================================================
    # flask-like decorators
    #===============================================================================================
    def route(self, url):
        def deco(cls):
            if url in self._registered_urls:
                raise ValueError("URL %r already appears in routes" % (url,))
            self.router.add((url, cls))
            self._registered_urls.add(url)
            cls.URL = URLStr(url)
            return cls
        return deco
    
    def error_handler(self, code):
        def deco(func):
            self.error_handlers[code] = func
            return func
        return deco


class Handler(webapp2.RequestHandler):
    URL = None




