---
title: 10 Simple Steps to Harden Your Docker Containers
author: Siddarth Senthilkumar
comments: true
date: 2019-06-20 07:50:49
tags:
- Docker
- Hardening
- Secure
- Containers
---

Docker is a well tested containerization platform that is used by hundreds of companies to securely and scalably deploy applications. Today, I'll explain some of the basic steps you can take to secure your containers so that if an application gets popped, you can minimize the impact on other containers on the same host and the host itself. Many of the practices listed here are just my notes from [this snyk blog post](https://snyk.io/blog/10-docker-image-security-best-practices/) and [this secjuice article](https://www.secjuice.com/how-to-harden-docker-containers/), so please give their pages a look for more details!

## 1. Create a Less Privileged User
By default, your app runs as root inside the container. You can create a special group and user and then change to that user before launching your app. That way, your attacker doesn't get root access by default!

```Dockerfile
RUN addgroup -S app_group && adduser -S --shell /sbin/nologin -g app_group app_user
RUN chown -R app_user:app_group /app
USER app_user
```

## 2. Use an Alpine Base Image
If an attacker compromises your app, they may wish to pivot around the system and escalate their privileges. This is facilitated by the other programs residing in the container that may have vulnerabilities themselves. One of the first things an attacker will do is check what processes are running on the system, which processes are running as root, and what suid binaries are installed on the system. For example, the Morris Worm exploited a buffer overflow in the [`finger` daemon](http://seclab.cs.ucdavis.edu/projects/vulnerabilities/doves/1.html) to get a root shell on the victim, since the daemon often ran as superuser.

The potential for escalation can be significantly reduced by just stripping out all the unnecessary programs in your base image as this decreases the available attack surface. Fortunately, there are already pre-built Docker images that take care of this for you: the Alpine images. Alpine images are based on BusyBox and only contain the essential files needed for your app. If you need a container for nginx, for example, you can specify a container like the following:

```Dockerfile
FROM nginx:alpine
```

Want to run a Python application? Easy:

```Dockerfile
FROM python:3.7-alpine
```

The image will be stripped down but will still have the bare minimum needed to run a Python application. You won't find programs that should never get run (like vim or netcat) inside an Alpine image. Finally, one last benefit of the Alpine image is that your resulting image will be a lot smaller! The whole image might only take up a few megabytes of space, compared to over a gigabyte if you use a Debian or Ubuntu image.

## 3. Namespace Isolation on the Docker Host

By default, the root namespace in your Docker container maps 1:1 with the host. What this means is that if an attacker gets root in a container and then breaks out of the container, they'll also have root access on the Docker host. This can easily be mitigated by re-mapping the Docker `root` to a less privileged user on the host. The [Docker docs](https://docs.docker.com/engine/security/userns-remap/) have a great explanation with more details; here I just list what I think are the easiest ways to apply this.

First, set Docker to use a configuration file (if not already). Edit `/etc/default/docker` and add:
```
DOCKER_OPTS="--config-file=/etc/docker/daemon.json"
```
Then, create or edit `/etc/docker/daemon.json` and add the `userns-remap` option to the config:
```json
{
    "userns-remap": "default"
}
```

With the "default" remap option set, Docker will look for the `dockremap` subuid and subgid to perform any remappings. Now, we'll add "dockremap" user and group entries for subuid/subgid.

```
$ echo "dockremap:345000:65536" | sudo tee -a /etc/subuid
$ echo "dockremap:345000:65536" | sudo tee -a /etc/subgid
```

I chose the UID/GID ranges you see above (345000-65536) but you're free to choose anything that doesn't conflict with another existing mapping. Finally, restart your Docker daemon to apply the changes.
```
$ systemctl restart docker
```

## 4. Use .dockerignore

Sometimes, I'll find myself issuing a command like `COPY . .` in a Dockerfile. You want to be careful whenever you copy a full folder's contents into your image. Make sure you don't copy local build files like `__pycache__` and `venv`, or secret files like `.env` or `creds.json`. You can use a `.dockerignore` file to explicitly blacklist or whitelist certain file types. I would recommend using whitelisting so that you're always aware of exactly what files are going into your container. Better yet would be to avoid blind full directory copies like `COPY . .` altogether, but since that can be difficult for larger projects, a `.dockerignore` file might be more practical.

## 5. Use Dockerfile Security Linters & Scanners

A linter is an automatic way to provide immediate feedback on  best practices and could catch simple security issues in your Dockerfile. One that I've used in the past is [hadolint](https://github.com/hadolint/hadolint), which integrates into my text editor (VSCode) nicely. There are lots of tools that automatically scan your images for known CVEs. If you have any good suggestions that you've used in the past, please let me know in the comments!

## 6. Explicitly supply IP Addresses for Exposed Ports

In a docker-compose file, you can use the `ports` command to map container ports to ports on the host like the following:

```yaml
ports:
  - 80:80
```

By default, this makes port 80 on the host's public IP address available for use. If you're just developing locally, you should explicitly define the IP that gets mapped so that others can't access your dev environment.

```yaml
ports:
  - 127.0.0.1:80:80
```

## 7. Use Control Groups (cgroups)

The Linux kernel allows you to limit access to physical hardware resources (eg the CPU, RAM, network, etc). This can be important if you don't want one container to monopolize the resources on the host, such as in a DOS attack. There are many things you could restrict, but here are some of the basic things.

```bash Restrict app to Certain CPU Cores
# Restrict app to only use cores 0-1
docker run --cpuset-cpus 0-1 my_image
# Restrict app to only use cores 0 and 2
docker run --cpuset-cpus 0,2 my_image
```

```bash Specify Time Allocation per Container
docker run --cpu-shares 512
```

The `--cpu-shares` flag takes a value from 0-1024 and uses a relative weighting scheme. For example:
    - Container 1 has 1024 shares, Containers 2 and 3 have 512 shares each.
    - Then Container 1 has 50% of the CPU time, the other 2 have 25% each.

Shares are only enforced when CPU time is running, not I/O wait time. This is because other containers can use the CPU during that time anyway.

```bash Prevent Fork Bombs
docker run --pids-limit 200 my_image
```
This limits the number of processes a container can fork at runtime, which prevents fork bombs from consuming a Docker Hosts' entire process table.

## 8. Make Container Read-Only

Ideally, your app's container should be stateless so writes aren't really necessary. Any "writes" should happen in a separate database container. Practically, though, many programs rely on the ability to write files to `/tmp` or other files during their runtime, and they may throw errors if you try to make the whole container read-only. One way around this is to use the `--tmpfs` flag to create writeable directories for whatever you need. See [here](https://nickjanetakis.com/blog/docker-tip-55-creating-read-only-containers) for more details and the [compose file](#Sample-docker-compose) at the bottom of the page for an example.

## 9. Network Isolation

If you use `docker-compose`, you can specify networking namespaces to isolate the different containers that comprise your application. For example: Let's say you have 1 container for your app logic and 2 containers for different databases.

You want the different databases to talk to the application, but you don't want the databases to talk to each other. If one of the DB containers gets compromised, it at least shouldn't be able to mess with the other DB container. You can use network namespaces to implement this in your docker compose file. Here's a simple example where the databases can't talk to each other, but they can talk to the app.

```yaml
services:
    app:
        networks:
            - dbA
            - dbB
    databaseA:
        networks:
            - dbA
    databaseB:
        networks:
            - dbB

networks:
  dbA:
  dbB:
```

## 10. Set up AppArmor, Seccomp Rules, and Capabilities

Linux provides extremely fine-grained controls to OS resources. AppArmor, Seccomp, and Capabilities are ways to  minimize the resources available to an attacker of your app both during and after the exploitation process. This may be overkill depending on your app's functionality and your threat model - they're probably more relevant to those who wish to build a sandbox to run untrusted code, but I list these here for completeness. [Here](https://security.stackexchange.com/questions/196881/docker-when-to-use-apparmor-vs-seccomp-vs-cap-drop) is an excellent set of explanations from the security stack exchange on the differences between the three.

1. AppArmor is a kernel security module that allows you to restrict or remove fine-grained access to specific operations. For example, you can explicitly deny your app from ever reading files from `/etc/`. Even if an attacker can execute arbitrary code via your app, they'll never be able to perform a read on anything in `/etc/` if you configure your AppArmor rules as such. You can also restrict things like network and socket access to only talk to pre-specified hosts.

2. Seccomp is short for "secure computing mode" and is another Linux security feature. You can use seccomp to remove the ability of a program to use certain syscalls that aren't needed. A common exploitation technique is to use syscalls with attacker-specified arguments to perform reads and writes in memory. With the right seccomp rules in place, an attacker will have an extremely difficult time manipulating the program's memory to build a reliable exploit.

3. Capabilities are individual privileges of the root user that are provided by the Linux kernel. A root process can drop capabilities so that it's never able to do something it shouldn't, such as creating raw connections to the network.

## Sample docker-compose

I've implemented some of the above protections in the below docker-compose file. I've specified a web app that uses nginx to field requests, a Flask web server that processes the requests, and a separate image for a job called "dirsearch". The "dirsearch" job only talks to nginx via the `frontend` network. The nginx container talks to the flask webapp via the `backend` network. Finally, the flask container is `read_only`, except for the `/tmp` directory.

```yaml
version: '3'

services:

  flask: # Creates a virtual hostname "flask" available to nginx container too!
    image: webapp-flask
    build:
      context: flask_server
      dockerfile: app_container/Dockerfile
    networks:
      - backend
    read_only: true
    tmpfs:
      - /tmp

  nginx:
    image: webapp-nginx
    build:
      context: flask_server
      dockerfile: nginx_container/Dockerfile
    depends_on:
      - flask
    networks:
      - frontend
      - backend
    ports:
      - 127.0.0.1:80:80 # Map port 80 on host to port 80 on nginx container (so http://localhost works on host)

  dirsearch:
    image: dirsearch
    build:
      context: dirsearch_job
      dockerfile: Dockerfile
    depends_on:
      - nginx
    networks:
      - frontend
    ports:
      - 127.0.0.1:5000:5000

networks:
  frontend:
  backend:
```
