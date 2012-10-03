minima: noSQL + noHTML + noJS
=============================

Traditional web frameworks comprise of an ORM layer over a DB, a templating engine and some 
HTTP dispatcher and session management. In my view, the first two are relics of the past and
we can (and should) do without them, and the third should be greatly improved. Luckily, modern
minimalist frameworks like ``flask`` get us closer to that, but there's still way to go.

The Vision: Snakes all the Way Down!
------------------------------------

* Websites should be service-oriented, exposing APIs instead of generating HTML pages 
  on the fly. JSON API calls everywhere, by default.
* Templating is a stupid thing: it's basically very limited, cumbersome, and impossible-to-debug
  form of function application. A template takes parameters and generates HTML: it's a function!
* An HTTP server is ultimately a degenerate form of Remote Procedure Call (RPC) - it dispatches
  function names (URLs) to concrete functions, extracts parameters, and generally alleviates
  your code from the mess that is HTTP. It's time to realize it and think about it the way it 
  realy is.
* HTML is too low-level for us to mess with; we ought to be talking at a much more semantic
  level, that renders itself as HTML plus the required JavaScript.
* JavaScript is a horrible language and we should strive to avoid any contact with it. We do this 
  by putting as much of it as possible into the framework. Semantic elements may generate their
  appropriate JavaScript when they render themselves to HTML, but the product should be pure.
* ORM and SQL suck. A document-oriented database (e.g., *mongo*) would normally prove the better
  choice (unless you need really complex queries): if you choose to work in a dynamic language,
  why would you work with a static DB schema? 

Web programming involves too many unrelated technologies that were stacked one on top of the other 
over the years (HTTP, HTML, JavaScript/CoffeeScript, CSS/Sass, JSON, AJAX, SQL, templating, CGI, 
...). The purpose of minima is to reduce that mess to pure Python, as far down as we can go, 
given that these technologies are here to stay.
