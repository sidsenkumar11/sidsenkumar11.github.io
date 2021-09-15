---
title: Serving a Flask Application
author: Siddarth Senthilkumar
comments: true
date: 2019-06-20 07:56:20
tags:
- Flask
- Python
- gunicorn
- Werkzeug
- WSGI
- uWSGI
- nginx
---

Sometime during my undergrad, I wrote a simple Flask app that had tons of intentional security vulnerabilities. I served the app from my laptop at a security club meeting as a challenge to see who could find all the vulns first. Students connected to my laptop, interacted with login forms, and played around with my website. About 10 minutes in, everyone started reporting that the server was taking too long to respond. I visited the homepage of the app and confirmed that it was taking around ~3 minutes to load. At the time, I thought maybe my laptop couldn't handle the 20-40 people in the room connecting simultaneously, and that I should have gotten a dedicated server. Thinking back, though, that couldn't have been the case. My laptop had an above average 8-core Intel i7 CPU, 16GB of RAM, and an SSD. It also wasn't running much software other than the web server. So what was the issue?

There are plenty of [tutorials](https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/) on how to build basic web apps using Flask. However, most of them stop short at letting you use Flask's debug web server to serve your application. In a production environment, like my security club room, you'd never want to serve an app this way. Today, I'll introduce some of the software used to serve a Flask application and how they fit together. Using this information, you can create an app that serves thousands of clients from just your laptop!

## Flask Application

Very briefly, I'll introduce the basics of a Flask application. First, we start by creating an application object.

```python
app = Flask(__name__)
```

Then, we register different URIs and define the corresponding functions to call when they get hit.

```python
@app.route('/')
def root():
    return "Hello World!"

@app.route('/secret')
def secret():
    return "You found me!"
```

And that's really all there is to a web application!

Think of the app as an API. The app object doesn't "do" anything; it just defines requests and how to respond to these requests.

## Application Server

The Flask application object defines the different URIs and appropriate responses. However, it's not capable of actually "serving" the application - it's just a definition. We need a separate piece of software to serve the app, and we call it an application server. A server handles details about:
- Network connections (sockets, hosts, ports, etc)
- Receiving requests over the network
- Sending responses over the network
- Multiplexing users

How does it do this? It starts by listening for incoming connections on a host and port. When it receives a request, it parses the request and current environment for information like:
- HTTP headers
- Input form data
- Environment Variables

Then, it sends the request information to the application (the `app` object we defined previously). The app object constructs the HTML content and returns it to the server, which then puts the content together with headers and other information. Finally, the server sends the response to the requester over the network.

The server might use threads and buffers to deal with multiple simultaneous connections, where each thread sends request information to its own `app` object and responds to its request with the returned content. There are several different application servers out there, each with its own advantages and disadvantages.

## Werkzeug - Flask's Debug Server

So how do we find a server program to serve our Flask application? Well, it turns out that Flask comes with one!

Flask comes with a built-in library called "Werkzeug", and that library contains a server to serve your app. The Werkzeug server is instantiated and run if you call `app.run()`, where `app` is the object you got from `app = Flask(__name__)`. Now, you can serve real requests to and from your app! The `run()` function takes some arguments like what IP address you want to serve from, what port to serve from, and whether debug messages should be printed on error.

    Q: Can I just write a web application with Flask and NOT start the built-in server?
YES! You're not forced to run Werkzeug's server.
The `app` object represents just the application and doesn't start a server until `app.run()`.
The `app` object won't actively handle real requests; it just defines the API for requests.
You could use another server other than Werkzeug's server to mediate requests to the `app` object.

    Q: Why would I even want to use another server if Flask already gives us one?

Werkzeug's server isn't designed to be efficient, stable, or secure. It doesn't scale well when multiple users access the website (which is why my website was so slow!). Werkzeug's server is purely something for quick testing during development of your application, without having to search for and install another server program. There are much better server programs that can efficiently support hundreds or even thousands of connections at the same time!

## WSGI - Web Server Gateway Interface

The servers that exist today are complex software that handle multiple parts of the server stack. To understand why, it's important to first understand what the WSGI protocol is and why it came to be.

### Problem

There are many competing web servers to choose from (Werkzeug, Apache, nginx, Lighttpd, etc).
There are also many Python webapp frameworks (Flask, Django, Tornado, Pyramid, etc).

In the past, each server expected response content from the webapp in different formats. Similarly, each webapp framework expected request content from the server in different formats. If you got tired of using Flask and wanted to switch to Django, you might've had to find a different server that supported the request/response format that Django used. It would be great if each framework could work with any of the server programs and vice-versa. That way, you could keep your existing server configurations even if you wanted to switch webapp frameworks.

### Solution

Eventually, some smart people decided to make a standardized protocol for requests and responses between servers and apps. The Python community introduced WSGI (pronounced "whiz-gee") as this protocol. WSGI standardizes the way servers talk to Python webapps and vice-versa. Today, all servers and Python webapps implement WSGI.

{% asset_img WSGI.png %}
<center>Image from [https://ruslanspivak.com/lsbaws-part2/](https://ruslanspivak.com/lsbaws-part2/)</center>

In our examples from before, Flask was the webapp and Werkzeug was the web server. Both of these are WSGI compliant!

For a webapp framework to be WSGI compliant, it just needs to define a function with 2 parameters.
```python
def app(environment, start_fn):
    # environment : a dict with all the incoming request information (filled in by the server)
    # start_fn         : a callback function defined by the server
    ...
    return "<html>Here's your response page!</html>"
```

We call this function the "callable". What should the callable do?

1. Understand the request. What are the incoming HTTP headers? Cookies? What is the URI being requested? All of this information comes from the `environment` dictionary.

2. Based on the URI being requested, construct an appropriate response. We already saw how Flask lets you define functions to implement this. The callable simply needs to call the right function for this URI.

3. Call `start_fn()`, which was provided by the server. There are 2 parameters to `start_fn()`; an HTTP response code and a list of response headers expressed as 2-tuples.

    Ex: `start_fn('200 OK', [('Content-Type', 'text/plain')])`

4. Return the actual bytes of the response as an iterable.

    Ex: `["Hello World!\n"]`
    Ex:

```python
def app(env, start_fun):
    # ...
    def double(L):
        for x in L:
            yield str(x**2)
    return double([1, 2, 3]) # returns a generator, which is iterable
```

That's it! That's all it takes to build a WSGI compliant webapp. You could even create your own WSGI Python webapp without Flask or Django  using just this knowledge.

### Flask's Callable
To be WSGI compliant, the webapp has to define a callable function (shown above as `app`) with two parameters. But the "function" can actually be an object too! As long as the object implements `__call__`, it's callable like a function is. In Flask, the object returned by the `Flask()` constructor is the WSGI callable. So when you write `app = Flask(__name__)`, you're creating a callable called `app`. Looking at the [source](https://github.com/pallets/flask/blob/master/src/flask/app.py#L2448) for the Flask class, you can see it implements `__call__`. As expected, it takes 2 arguments:

- environ        - A WSGI environment (A dict with the request information)
- start_response - A function that accepts a status code and list of headers for the response

Any server that is WSGI compliant will require a reference to the `app` callable. The server communicates with your callable using the WSGI process we defined above, passing along request information and receiving response information. For more information about building a WSGI application, check out [this page](https://www.sitepoint.com/python-web-applications-the-basics-of-wsgi/) where I learned most of this information from.

## Werkzeug

Since every web application needs to provide callable functions and handle specific params it receives in WSGI form, it would be great if a library handled this "callable" interface. Well, it turns out that Werkzeug is this library! It provides utilities for developing WSGI-compliant webapps, like:
- Parsing headers
- Sending and receiving cookies
- Providing access to form data
- Generating redirects
- Generating error pages when there's an exception
- Providing an interactive debugger that works in the browser

As we discussed before, it even includes a simple web server. Running a whole server like nginx is probably overkill for just testing on your own box. You can use the Werkzeug server to do your testing instead in a matter of seconds by just entering `app.run()`.

Flask uses the Werkzeug library, so Flask comes with the Werkzeug server. You pass the Flask `app` as the WSGI callable. As we mentioned before, the problem with this server is that isn't meant to be efficient, scalable, or secure. So what are our other options?

## uWSGI

uWSGI is a full-fledged HTTP server. It takes in an HTTP request and converts it to a "WSGI request". Then, it passes that along to the callable and waits for the response.

## Gunicorn ("Green Unicorn")

{% asset_img gunicorn_logo.png %}

gunicorn is a web server modeled after Ruby's "Unicorn" web server. It's similar to uWSGI in that it takes in HTTP requests and translates them into WSGI requests for the callable. The main allure of gunicorn is that it's very easy to setup. It also:
- Easily scales Flask apps to dynamically serve hundreds of users
- Supports HTTP "Keep-Alive" through synchronous/asynchronous workers
- Supports SSL
- Allows specifying number of worker processes
- Incorporates asynchronous I/O

gunicorn uses a "pre-fork worker model", which essentially means that a master process forks many other worker processes. Each worker process is ready to handle an incoming request and contains a reference to its own callable. Upon receiving a request, a worker will translate it to WSGI, send it to its callable, and wait for the response. Scaling a gunicorn server is easy since you just need to configure gunicorn to spawn more workers!

Pre-forking systems are great for low latency communication. They have no cost in spinning up a process to handle each request since the processes are already spun up and just sit around waiting. However, they're not so great at handling slow clients and traffic surges since each worker thread is occupied with its request until it finishes. In those cases, you may be better off using nginx.

## nginx

{% asset_img nginx_logo.png %}

nginx is a reverse proxy that can also be used as a web server. nginx especially excels at:
- Handling large numbers of connections with little CPU/memory cost (tens of thousands of connections at once!)
- Serving static content (it can even redirect to a CDN or a separate bucket)
- Handling gzip compression
- Adding SSL/TLS
- Caching common requests

nginx is more reslient in the face of slow clients as well since it only sends requests to the backend webapp as fast as the backend can handle. When the webapp returns a result, nginx buffers the response to feed it to slow clients at their own pace. The backend can move on to handling another request even as the slow client is still receiving the result.

Another use case for nginx is as a reverse proxy. Let's say you're serving multiple web apps from the same box, but perhaps on different IP addresses or ports. You can use nginx to route requests for any of the apps to the appropriate backend webapps. You could also use nginx similarly for load balancing.

Most commonly, you'll see nginx used in conjunction with another web server like uWSGI or gunicorn sitting behind it, like the following:

{% asset_img architecture.gif %}
<center>Image from [https://blog.paradisetechsoft.com/django-deployment-on-nginx-and-gunicorn/](https://blog.paradisetechsoft.com/django-deployment-on-nginx-and-gunicorn/)</center>

You'd use nginx to:
- Route requests to multiple different web apps. If website A and website B both get routed to the machine that nginx is running on, nginx can reverse proxy the requests to the appropriate uWSGI/gunicorn servers for each website.

- Serve static content. The webapp itself is slow (Python interpreters are a bottleneck!). Serving off easy static content without invoking the interpreter significantly reduces the load on the backend webapp. Ideally, you'd only use the webapp to respond to dynamic content.

- Handle thousands of connections at once with little memory/CPU cost (it's even better than gunicorn and uWSGI at this).

- If one of your apps didn't use WSGI and instead used something like CGI, you could use another nginx behind the muxing nginx to act as the HTTP request handler that translates and passes on the request to the web app using CGI.

You'd use uWSGI/gunicorn to:

- Translate the incoming HTTP request to WSGI.
- Pass on the WSGI request info to the Flask callable.
- Handle multiple requests sent from nginx to the web app.


    Q: Why doesn't nginx translate HTTP requests to WSGI?
       Why do you need uWSGI/gunicorn to do it?

This is about to get tricky, but bear with me. The TLDR is that nginx just doesn't support that feature.

nginx can't translate to WSGI, but it does have a module that can translate HTTP requests to something called `uwsgi`. Just enter `uwsgi_pass <your_uWSGI_server>` in your nginx configuration to enable this.

But, confusingly, uwsgi != WSGI != uWSGI.
- WSGI is a protocol for Python web servers that specifies the callable interface.
- uWSGI is a server program that can receive requests and translate them into WSGI for the callable.
- uwsgi is a binary protocol that nginx can send the request as and uWSGI can receive. It's faster than having nginx send an HTTP request to uWSGI.

Note: gunicorn doesn't support receiving a request in the binary uwsgi protocol, so when nginx is used with gunicorn, you have to just send the HTTP request directly over to gunicorn (use `proxy_pass` instead of `uwsgi_pass`). This is probably the biggest real difference between gunicorn and uWSGI since uWSGI supports both HTTP and uwsgi.

So, nginx can't directly send information to the Python callable because it doesn't support the WSGI callable interface; it only supports directly forwarding the HTTP request or translating it to the uwsgi binary interface. WSGI callables will expect information to be passed to them via WSGI format, so nginx can't call the callable directly. Why doesn't nginx support the callable interface? I'm not sure. Maybe the devs are lazy? There would be marginal gain since there are already tons of projects like uWSGI and gunicorn that already implement this, so maybe there's no reason to include it in nginx.

In conclusion, most commonly we would have nginx receiving the request. It would respond to static content requests immediately. For dynamic requests, it would forward the request over uwsgi or over HTTP to the uWSGI/gunicorn server. Then, the uWSGI/gunicorn server translates the request to WSGI protocol to make use of the Python app's callable. The callable generates the response, which gets sent back up the chain to nginx to serve out to the requester.

## Conclusion
Flask seems like a simple webapp framework and yet the details of efficiently serving it can get very complicated. I've tried to distill my admittedly cursory knowledge of the subject into this post but I'm sure there are still gaps to be filled. If you spot any inaccuracies or have different ways of serving your apps, I'd love to hear from you in the comments!
