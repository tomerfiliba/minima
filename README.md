``minima: noSQL + noHTML + noJS``

Sketch
======
Traditional web frameworks are comprised of an ORM layer over a DB, a templating engine (or 
several ones), and some sort of an HTTP dispatcher. Take ``sqlalchemy`` with ``cherrypy`` and
``cheeta`` templates and you're done -- so how come web frameworks are still so big and 
complicated? 

``Minima`` aims to eliminate the dozens of existing technologies that traditional web frameworks
stack onto each other: HTTP servers, HTML, templating languages, CSS, javascript, JSON, SQL 
servers and what-not. ``Minima`` allows you to build fully functional, efficient, and good-looking
sites, without ever having to see anything other than server-side python code. On the other hand,
in order to provide this feat, you should be aware that ``minima`` restricts what you can do.

The idea is simple:

* Get rid of SQL: move to a key-value store such as ``mongo``. There's no reason for your
  data store to be statically typed while your code is dynamically typed! The data-model changes
  too frequently to be static, and most sites are not google or ebay -- they amount of traffic 
  shouldn't be a problem.
* Get rid of HTML: your code builds "documents", which define the structure of your data.
  These documents are then rendered as HTML
* get rid of templating engines: since you generate your documents in code, there's no reason
  to use templates. You don't see HTML. Ever. Templating is just a restricted form of function 
  composition, while general function composition gives you much more power.
* Get rid of client-side scripting, in favor of server-side scripting and eliminate ``GETs`` 
  and ``POSTs`` in favor of AJAX - apart from the initial ``GET`` of the page, 
  all server interaction will be AJAXish (using ``jQuery.getJSON``). The server will generate 
  JSON resources and the necessary javascript code to render them in-page. This code will be
  part of the framework, not your site. "There should be one -- and preferably only one -- 
  obvious way to do it."
* Since you're building documents and not HTML "text", there's no different between a JSON 
  resource and a web page -- they only use different renderers.
* In the meantime, until a better solution is found, we'll stick with CSS: after all, you'll 
  have to specify the background color and font size, so there's no reason to reinvent the wheel
  here, at least at this moment.
* Use a unified sessions/cookies library, as part of the framework. Your code won't need to handle
  the context by itself.
* Use a simple HTTP dispatcher built on top of ``WSGI``: let Apache take care of everything 
  HTTP-related, and other than that, there's really no need for cherrypy or other python web 
  servers.

