import cherrypy


class Dispatcher(object):
    @cherrypy.expose
    def default(self):
        pass

class Root(object):
    #@cherrypy.expose
    #def index(self, *args):
    #    return "index" + repr(args)

    @cherrypy.expose
    def blog(self, *args):
        return "blog" + repr(args)


if __name__ == "__main__":
    cherrypy.quickstart(Root())


