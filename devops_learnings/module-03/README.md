# Docker Module 3 — Dockerfile, Multi-Stage Builds & Port Mapping

> Complete notes from the hands-on Module 3 practice.

---

# 1. Docker Build Command

The main command used to create a Docker image is:

```bash
docker build -f Dockerfile.v1 -t my_app:v1 .
```

Let's break down **every part**.

```text
docker     build     -f Dockerfile.v1     -t my_app:v1     .
  │          │             │                    │           │
  │          │             │                    │           └── Build context
  │          │             │                    └── Image name + tag
  │          │             └── Dockerfile to use
  │          └── Build an image
  └── Docker CLI
```

---

## 1.1 `docker`

The Docker command-line interface.

```bash
docker
```

Used to communicate with the Docker daemon.

---

## 1.2 `build`

```bash
docker build
```

Tells Docker:

> "Build an image using a Dockerfile."

---

## 1.3 `-f`

```bash
-f Dockerfile.v1
```

`-f` means:

> Use this specific Dockerfile.

Example:

```bash
docker build -f Dockerfile.v1 .
```

or:

```bash
docker build -f Dockerfile.v2 .
```

or:

```bash
docker build -f Dockerfile.v3 .
```

Without `-f`, Docker looks for a file named:

```text
Dockerfile
```

by default.

### Example

If your directory contains:

```text
module-03/
│
├── Dockerfile
├── Dockerfile.v1
├── Dockerfile.v2
└── Dockerfile.v3
```

Then:

```bash
docker build .
```

uses:

```text
Dockerfile
```

while:

```bash
docker build -f Dockerfile.v2 .
```

uses:

```text
Dockerfile.v2
```

---

# 2. `-t`

```bash
-t my_app:v1
```

`-t` means:

> Tag/name the Docker image.

The general syntax is:

```text
-t IMAGE_NAME:TAG
```

Example:

```bash
-t my_app:v1
```

means:

```text
Image name = my_app
Tag        = v1
```

So:

```text
my_app:v1
│      │
│      └── Tag
└───────── Image name
```

You can have:

```text
my_app:v1
my_app:v2
my_app:v3
```

These can represent different versions of the same application.

---

## 2.1 What happens if you don't specify a tag?

If you run:

```bash
docker build -t my_app .
```

Docker automatically uses:

```text
latest
```

So this:

```bash
docker build -t my_app .
```

is effectively:

```text
my_app:latest
```

---

# 3. The `.` at the end

This is extremely important.

```bash
docker build -f Dockerfile.v1 -t my_app:v1 .
                                                    ↑
```

The `.` means:

> Use the current directory as the **build context**.

For example, if you're currently in:

```text
C:\devops_N\module-03
```

then:

```bash
docker build -f Dockerfile.v1 -t my_app:v1 .
```

means:

```text
Build context:
C:\devops_N\module-03
```

Docker can access files inside this build context when processing:

```dockerfile
COPY
ADD
```

---

# 4. Build Context

Suppose:

```text
module-03/
│
├── Dockerfile.v3
│
└── app/
    ├── app.py
    └── requirements.txt
```

and you run:

```bash
docker build -f Dockerfile.v3 -t my_app:v3 .
```

The `.` tells Docker:

> Send `module-03` as the build context.

Therefore the Dockerfile can do:

```dockerfile
COPY app/app.py .
```

and:

```dockerfile
COPY app/requirements.txt .
```

---

# 5. Why did `COPY` fail earlier?

Initially, you ran:

```text
C:\devops_N\module-03\app
```

and tried:

```bash
docker build -f Dockerfile.v1 -t mypython_app .
```

But Docker couldn't find:

```text
Dockerfile.v1
```

because it was not in that directory.

Later, you moved to:

```text
C:\devops_N\module-03
```

and ran:

```bash
docker build -f Dockerfile.v1 -t mypython_app .
```

Now Docker could find:

```text
module-03/
└── Dockerfile.v1
```

and because `.` represented `module-03`, Docker could also access:

```text
module-03/app/
```

---

# 6. Dockerfile — V1

Example:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY app/requirements.txt .

RUN pip install -r requirements.txt

COPY app/app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

---

# 7. `FROM`

```dockerfile
FROM python:3.11
```

Defines the base image.

Docker starts building your image from:

```text
python:3.11
```

Think:

```text
Python application
       +
Python environment
       +
OS libraries
       ↓
Docker image
```

---

# 8. `WORKDIR`

```dockerfile
WORKDIR /app
```

Sets the working directory inside the image/container.

After this:

```dockerfile
COPY app.py .
```

means:

```text
/app/app.py
```

instead of:

```text
/app.py
```

You can think of it like:

```bash
cd /app
```

inside the container.

---

# 9. `COPY`

Example:

```dockerfile
COPY app/requirements.txt .
```

General syntax:

```text
COPY SOURCE DESTINATION
```

Here:

```text
SOURCE      = app/requirements.txt
DESTINATION = .
```

Because:

```dockerfile
WORKDIR /app
```

is already set, the file becomes:

```text
/app/requirements.txt
```

---

# 10. `RUN`

Example:

```dockerfile
RUN pip install -r requirements.txt
```

`RUN` executes a command **while building the image**.

It is different from `CMD`.

```text
RUN
 ↓
Image build time
```

while:

```text
CMD
 ↓
Container runtime
```

---

# 11. `EXPOSE`

Example:

```dockerfile
EXPOSE 5000
```

`EXPOSE` documents the port that the application inside the container is expected to use.

It does **NOT**:

* start a port
* publish a port
* create host-to-container forwarding
* change the application's port

For example:

```dockerfile
EXPOSE 5000
```

does not automatically make:

```text
localhost:5000
```

work.

Actual port publishing is done with:

```bash
docker run -p ...
```

---

# 12. `CMD`

Example:

```dockerfile
CMD ["python", "app.py"]
```

Specifies the default command executed when the container starts.

So:

```text
docker run image
        ↓
CMD executes
        ↓
python app.py
```

---

# 13. `RUN` vs `CMD`

This distinction is important.

### `RUN`

```dockerfile
RUN pip install flask
```

Runs during:

```text
IMAGE BUILD
```

### `CMD`

```dockerfile
CMD ["python", "app.py"]
```

Runs during:

```text
CONTAINER START
```

Mental model:

```text
Docker build
     │
     ├── FROM
     ├── WORKDIR
     ├── COPY
     ├── RUN
     │
     ↓
  IMAGE
     │
     │ docker run
     ↓
 CONTAINER
     │
     └── CMD
```

---

# 14. Multi-Stage Build

A multi-stage Dockerfile uses multiple `FROM` instructions.

Example:

```dockerfile
FROM python:3.11 AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local

COPY app/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

There are two stages:

```text
Stage 1
Builder
   ↓
Install dependencies
   ↓
Stage 2
Runtime
   ↓
Run application
```

---

# 15. `AS builder`

```dockerfile
FROM python:3.11 AS builder
```

The:

```text
AS builder
```

gives this build stage a name:

```text
builder
```

Later we can refer to it using:

```dockerfile
COPY --from=builder ...
```

---

# 16. Why Multi-Stage Builds?

The idea is:

```text
BUILD ENVIRONMENT
       ↓
Install/build everything
       ↓
Take only what is required
       ↓
RUNTIME ENVIRONMENT
```

This prevents unnecessary build dependencies from being included in the final image.

Conceptually:

```text
Builder image
├── Python
├── pip
├── build tools
├── dependencies
└── temporary files

             ↓
       COPY only needed
          artifacts

             ↓

Runtime image
├── Python
├── required dependencies
└── application
```

---

# 17. `--prefix`

This command was particularly important in our Python multi-stage build:

```dockerfile
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

The important part is:

```text
--prefix=/install
```

It tells `pip`:

> Install the Python packages under `/install`.

So instead of installing them in the normal location, we intentionally create:

```text
/install
```

inside the builder stage.

Conceptually:

```text
Builder
│
└── /install
     │
     └── Python dependencies
```

Then we can copy `/install` into the runtime image.

---

# 18. Why did we need `--prefix=/install`?

We had:

```dockerfile
COPY --from=builder /install /usr/local
```

This means:

> Take `/install` from the builder stage and copy it into `/usr/local` in the runtime stage.

Therefore the builder must actually contain:

```text
/install
```

If we only use:

```dockerfile
RUN pip install -r requirements.txt
```

then `/install` is not necessarily created.

Then:

```dockerfile
COPY --from=builder /install /usr/local
```

fails with:

```text
"/install": not found
```

Therefore:

```dockerfile
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

creates the directory that we later copy.

---

# 19. `--no-cache-dir`

In:

```dockerfile
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

this:

```text
--no-cache-dir
```

tells pip:

> Don't keep its package download cache.

This can help reduce unnecessary files in the Docker image.

So:

```text
--prefix=/install
        ↓
Where dependencies are installed

--no-cache-dir
        ↓
Don't keep pip's download cache
```

These options solve **different problems**.

---

# 20. `COPY --from=builder`

Example:

```dockerfile
COPY --from=builder /install /usr/local
```

Normally:

```dockerfile
COPY
```

copies from the build context.

But:

```dockerfile
COPY --from=builder
```

copies from another build stage.

Here:

```text
--from=builder
```

means:

> Copy files from the stage named `builder`.

So:

```text
Builder stage

/install
   │
   │ COPY --from=builder
   ↓
Runtime stage

/usr/local
```

---

# 21. Why doesn't the builder stage become the final image?

Consider:

```dockerfile
FROM python:3.11 AS builder

...

FROM python:3.11-slim

...
```

The second `FROM` starts a new stage.

The final image is based on:

```text
python:3.11-slim
```

not the complete builder image.

We explicitly copy only what we need:

```dockerfile
COPY --from=builder /install /usr/local
```

---

# 22. Docker Run

Basic syntax:

```bash
docker run IMAGE
```

Example:

```bash
docker run my_app
```

This:

1. Creates a container from the image.
2. Starts the container.
3. Executes the image's default `CMD`.

---

# 23. `-p`

This is one of the most important Docker options.

Syntax:

```bash
-p HOST_PORT:CONTAINER_PORT
```

Example:

```bash
docker run -p 8082:5000 my_app
```

means:

```text
HOST PORT       CONTAINER PORT
    │                 │
    ↓                 ↓
   8082      :       5000
```

Docker creates:

```text
Windows
localhost:8082
      │
      ↓
Docker
      │
      ↓
Container:5000
      │
      ↓
Flask
```

---

# 24. Why is the application accessed through `8082`?

Suppose Flask contains:

```python
app.run(host='0.0.0.0', port=5000)
```

Flask is listening on:

```text
5000
```

Then we run:

```bash
docker run -p 8082:5000 my_app
```

The application itself is still running on:

```text
container:5000
```

Docker exposes it to your computer through:

```text
host:8082
```

Therefore the browser uses:

```text
http://localhost:8082
```

The application is NOT running on port 8082.

Docker is forwarding:

```text
8082 → 5000
```

---

# 25. Port Mental Model

Always remember:

```text
HOST PORT : CONTAINER PORT
```

For:

```bash
docker run -p 8082:5000 my_app
```

think:

```text
8082 : 5000
 │       │
 │       └── Application/container
 └────────── Your computer
```

---

# 26. Why did `localhost:5000` fail?

If you run:

```bash
docker run -p 8082:5000 my_app
```

you created:

```text
localhost:8082
       ↓
container:5000
```

You did NOT create:

```text
localhost:5000
       ↓
container:5000
```

Therefore:

```text
http://localhost:8082
```

is the correct URL.

---

# 27. Could we use `5000:5000`?

Yes.

```bash
docker run -p 5000:5000 my_app
```

means:

```text
localhost:5000
       ↓
container:5000
       ↓
Flask
```

Then you can open:

```text
http://localhost:5000
```

---

# 28. Why use different ports?

Suppose you run two containers.

Both applications listen on container port `5000`.

You cannot do:

```bash
docker run -p 5000:5000 app1
docker run -p 5000:5000 app2
```

because your host's port `5000` can already be occupied.

Instead:

```bash
docker run -p 5000:5000 app1
docker run -p 5001:5000 app2
```

Now:

```text
localhost:5000
      ↓
Container 1 :5000


localhost:5001
      ↓
Container 2 :5000
```

The container port can be the same.

The host ports must be different.

---

# 29. Port Already Allocated

If Docker says:

```text
Bind for 0.0.0.0:8081 failed:
port is already allocated
```

it means:

> Something is already using host port `8081`.

For example:

```text
Container A
localhost:8081
      ↓
container:80
```

Then you cannot start:

```bash
docker run -p 8081:5000 my_app
```

because Docker would have:

```text
8081
 │
 ├── Container A
 │
 └── Container B   ❌
```

Instead use another host port:

```bash
docker run -p 8082:5000 my_app
```

or stop/remove the container using `8081`.

---

# 30. Check Which Ports Are Being Used

Run:

```bash
docker ps
```

Look at the:

```text
PORTS
```

column.

Example:

```text
0.0.0.0:8081->80/tcp
```

means:

```text
Host 8081
     ↓
Container 80
```

Another example:

```text
0.0.0.0:8082->5000/tcp
```

means:

```text
Host 8082
     ↓
Container 5000
```

---

# 31. `-d`

```bash
docker run -d my_app
```

`-d` means:

> Detached mode.

The container runs in the background.

Without `-d`:

```bash
docker run my_app
```

your terminal remains attached to the container.

With:

```bash
docker run -d my_app
```

you immediately get your terminal back.

---

# 32. `-it`

You may see:

```bash
docker run -it ubuntu
```

`-i` means:

```text
interactive
```

It keeps standard input open.

`-t` means:

```text
allocate a pseudo-terminal
```

Together:

```text
-it
```

are commonly used when you want an interactive shell.

Example:

```bash
docker run -it ubuntu bash
```

Now you can interact with the Ubuntu shell.

---

# 33. `-dit`

You may also see:

```bash
docker run -dit ubuntu
```

This combines:

```text
-d
-i
-t
```

So:

```text
-dit
```

means approximately:

```text
-d → detached
-i → interactive
-t → terminal
```

Useful when you want a container running in the background while keeping an interactive terminal attached to its main process.

---

# 34. `-d` vs `-it`

### Run interactively

```bash
docker run -it ubuntu bash
```

You get:

```text
root@container:/#
```

and can type commands.

### Run in background

```bash
docker run -d nginx
```

The container runs in the background.

### Run detached + interactive terminal

```bash
docker run -dit ubuntu bash
```

The container runs in the background while maintaining the interactive terminal configuration.

---

# 35. `--name`

Example:

```bash
docker run --name my_app_v3 -p 8082:5000 my_app:v3
```

`--name` gives the container a custom name.

Without it, Docker generates names such as:

```text
fervent_grothendieck
jolly_bardeen
kind_chatelet
```

With:

```bash
--name my_app_v3
```

you get:

```text
my_app_v3
```

This makes commands easier:

```bash
docker logs my_app_v3
docker stop my_app_v3
docker rm my_app_v3
```

---

# 36. `docker ps`

```bash
docker ps
```

Shows currently running containers.

Example:

```text
CONTAINER ID
IMAGE
COMMAND
STATUS
PORTS
NAMES
```

---

# 37. `docker ps -a`

```bash
docker ps -a
```

Shows:

```text
running containers
+
stopped containers
```

Useful when you think:

> "Where did my container go?"

---

# 38. `docker logs`

```bash
docker logs my_app_v3
```

Shows the container's stdout/stderr output.

For Flask, you might see:

```text
* Serving Flask app 'app'
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

Follow logs continuously:

```bash
docker logs -f my_app_v3
```

Here:

```text
-f
```

means:

```text
follow
```

---

# 39. `docker exec`

```bash
docker exec -it my_app_v3 bash
```

Runs a command inside an already-running container.

Breakdown:

```text
docker
  ↓
exec
  ↓
-it
  ↓
container name
  ↓
bash
```

For a shell:

```bash
docker exec -it my_app_v3 bash
```

If bash isn't available:

```bash
docker exec -it my_app_v3 sh
```

---

# 40. `docker inspect`

```bash
docker inspect my_app_v3
```

Shows detailed JSON information about the container.

It can show:

* container configuration
* network configuration
* IP address
* mounts
* environment
* image
* ports
* runtime configuration

---

# 41. `docker stats`

```bash
docker stats
```

Shows live resource usage.

Examples:

```text
CPU
Memory
Network I/O
Block I/O
PIDs
```

Useful for understanding resource consumption.

---

# 42. `docker top`

```bash
docker top my_app_v3
```

Shows processes running inside the container.

---

# 43. `docker history`

```bash
docker history my_app:v3
```

Shows the image's layers/history.

Useful for understanding how Dockerfile instructions contribute to the image.

---

# 44. `docker images`

```bash
docker images
```

Shows available Docker images.

You can also filter:

```bash
docker images my_app
```

Example:

```text
REPOSITORY   TAG       IMAGE ID       SIZE
my_app       v1        ...            ...
my_app       v2        ...            ...
my_app       v3        ...            ...
```

This is useful for comparing your Dockerfile versions.

---

# 45. `docker run` — Complete Example

```bash
docker run -d --name my_app_v3 -p 8082:5000 my_app:v3
```

Breakdown:

```text
docker
    ↓
Docker CLI

run
    ↓
Create + start container

-d
    ↓
Run in background

--name my_app_v3
    ↓
Give container a name

-p 8082:5000
    ↓
Host 8082 → Container 5000

my_app:v3
    ↓
Image to use
```

---

# 46. Complete Port Flow

Suppose:

### Flask

```python
app.run(host='0.0.0.0', port=5000)
```

### Dockerfile

```dockerfile
EXPOSE 5000
```

### Run

```bash
docker run -d --name my_app_v3 -p 8082:5000 my_app:v3
```

Then:

```text
                    YOUR COMPUTER
                         │
                         │
                  localhost:8082
                         │
                         │
                         ↓
                ┌────────────────┐
                │     DOCKER     │
                │                │
                │ 8082 → 5000    │
                └───────┬────────┘
                        │
                        ↓
                ┌────────────────┐
                │   CONTAINER    │
                │                │
                │     :5000      │
                │       ↓        │
                │     Flask      │
                └────────────────┘
```

Browser:

```text
http://localhost:8082
```

---

# 47. Why `host='0.0.0.0'`?

For a containerized application:

```python
app.run(host='0.0.0.0', port=5000)
```

means:

> Listen on all network interfaces inside the container.

This allows Docker networking to reach the application.

Do not confuse:

```text
0.0.0.0
```

with:

```text
localhost
```

`0.0.0.0` means:

```text
Listen on all available interfaces.
```

It is generally a bind address, not the URL you type into your browser.

---

# 48. `127.0.0.1`

```text
127.0.0.1
```

means:

```text
localhost
```

It refers to the current network environment.

Inside a container:

```text
127.0.0.1
```

means:

> This container itself.

It does not automatically mean your Windows machine.

---

# 49. Container IP

You may see something like:

```text
172.17.0.4
```

This is a container IP on a Docker network.

For example:

```text
Docker bridge network

172.17.0.2 → Container A
172.17.0.3 → Container B
172.17.0.4 → Container C
```

For normal host-to-container access, prefer:

```text
localhost:HOST_PORT
```

when you've published the port using `-p`.

Container IPs become much more important when learning Docker networking and container-to-container communication.

---

# 50. `EXPOSE` vs `-p`

This is one of the most important concepts from Module 3.

```dockerfile
EXPOSE 5000
```

means:

> The application is expected to use container port 5000.

While:

```bash
docker run -p 8082:5000 my_app
```

means:

> Forward host port 8082 to container port 5000.

Therefore:

```text
EXPOSE
   ↓
Documentation / metadata

-p
   ↓
Actual port publishing
```

---

# 51. Common Port Mistake

Suppose:

```python
app.run(port=5000)
```

but Dockerfile says:

```dockerfile
EXPOSE 8000
```

and you run:

```bash
docker run -p 8082:80 my_app
```

You have:

```text
Flask       → 5000
EXPOSE      → 8000
Port mapping → 8082:80
```

These don't match.

The container may still start, because `EXPOSE` doesn't control Flask.

But:

```text
8082 → 80
```

will not reach Flask because Flask is listening on:

```text
5000
```

Correct mapping would be:

```bash
docker run -p 8082:5000 my_app
```

---

# 52. Best Practice for Port Management

Use this three-step process.

## Step 1 — Find the application port

Example:

```python
app.run(port=5000)
```

Therefore:

```text
Application port = 5000
```

---

## Step 2 — Make `EXPOSE` match

```dockerfile
EXPOSE 5000
```

---

## Step 3 — Choose a free host port

Example:

```bash
docker run -p 8082:5000 my_app
```

Now:

```text
Application → 5000
Container   → 5000
Host        → 8082
```

Browser:

```text
http://localhost:8082
```

---

# 53. Port Naming Convention

Think about ports as:

```text
Application Port
       ↓
Container Port
       ↓
Host Port
```

Usually:

```text
Application Port = Container Port
```

For example:

```text
Flask application → 5000
Container          → 5000
Host               → 8082
```

So:

```text
localhost:8082
       ↓
container:5000
       ↓
Flask:5000
```

---

# 54. Common Examples

### Flask

```text
Flask = 5000
```

```bash
docker run -p 8080:5000 flask_app
```

Access:

```text
localhost:8080
```

---

### Node.js

```text
Node = 3000
```

```bash
docker run -p 8080:3000 node_app
```

Access:

```text
localhost:8080
```

---

### Nginx

Nginx normally listens on:

```text
80
```

```bash
docker run -p 8080:80 nginx
```

Access:

```text
localhost:8080
```

---

### PostgreSQL

PostgreSQL normally listens on:

```text
5432
```

```bash
docker run -p 5433:5432 postgres
```

Your host uses:

```text
5433
```

while PostgreSQL inside the container continues using:

```text
5432
```

---

# 55. Useful Docker Commands — Quick Reference

```bash
# Build an image
docker build -t my_app:v1 .

# Build using a specific Dockerfile
docker build -f Dockerfile.v3 -t my_app:v3 .

# List images
docker images

# Run a container
docker run my_app:v3

# Run in background
docker run -d my_app:v3

# Run with port mapping
docker run -p 8082:5000 my_app:v3

# Run in background with port mapping
docker run -d -p 8082:5000 my_app:v3

# Give container a name
docker run --name my_app_v3 my_app:v3

# Name + detached + port mapping
docker run -d --name my_app_v3 -p 8082:5000 my_app:v3

# List running containers
docker ps

# List all containers
docker ps -a

# View logs
docker logs my_app_v3

# Follow logs
docker logs -f my_app_v3

# Execute command inside container
docker exec -it my_app_v3 bash

# Inspect container
docker inspect my_app_v3

# Show container processes
docker top my_app_v3

# Show resource usage
docker stats

# Show image history
docker history my_app:v3

# Stop container
docker stop my_app_v3

# Remove container
docker rm my_app_v3

# Force stop and remove
docker rm -f my_app_v3
```

---

# 56. Important Docker Flags

| Flag                    | Meaning                                                |
| ----------------------- | ------------------------------------------------------ |
| `-f`                    | Select Dockerfile                                      |
| `-t`                    | Tag/name an image                                      |
| `-p`                    | Publish/map host port to container port                |
| `-d`                    | Detached/background mode                               |
| `-i`                    | Keep STDIN open                                        |
| `-t`                    | Allocate pseudo-terminal                               |
| `-it`                   | Interactive terminal                                   |
| `-dit`                  | Detached + interactive + terminal                      |
| `--name`                | Give container a custom name                           |
| `--prefix`              | Specify installation prefix for commands such as `pip` |
| `--from`                | Copy from another Docker build stage                   |
| `--no-cache-dir`        | Disable pip's package download cache                   |
| `-f` with `docker logs` | Follow logs                                            |

> Note: `-t` has different meanings depending on the Docker command.
> In `docker build -t`, it means **tag**.
> In `docker run -it`, `-t` means **allocate a pseudo-terminal**.

---

# 57. Image vs Container

This distinction is fundamental.

## Image

An image is a template/package.

```text
my_app:v3
```

It contains:

```text
Application
Dependencies
Filesystem
Configuration
```

---

## Container

A container is a running/created instance of an image.

```text
my_app:v3
     ↓
Container
     ↓
my_app_v3
```

You can create multiple containers from the same image.

```text
             my_app:v3
            /    |    \
           ↓     ↓     ↓
      Container Container Container
```

---

# 58. Final Mental Model

When working with Docker, think in this order:

```text
1. Application
       ↓
   Which port does it listen on?

2. Dockerfile
       ↓
   EXPOSE that container port

3. docker run
       ↓
   Choose a host port

4. -p HOST:CONTAINER
       ↓
   Create port forwarding

5. Browser
       ↓
   localhost:HOST_PORT
```

For your current Flask application:

```text
Flask
  ↓
5000

Dockerfile
  ↓
EXPOSE 5000

docker run
  ↓
-p 8082:5000

Browser
  ↓
http://localhost:8082
```

---

# 59. Module 3 — What I Should Be Able to Explain

Before considering Module 3 complete, I should be able to explain:

* [ ] What a Dockerfile is
* [ ] What `FROM` does
* [ ] What `WORKDIR` does
* [ ] What `COPY` does
* [ ] What `RUN` does
* [ ] Difference between `RUN` and `CMD`
* [ ] What `EXPOSE` does
* [ ] What `docker build` does
* [ ] What `-f` does
* [ ] What `-t` does
* [ ] What `.` means in `docker build`
* [ ] What build context means
* [ ] What an image is
* [ ] What a container is
* [ ] What multi-stage builds are
* [ ] What `AS builder` does
* [ ] What `COPY --from=builder` does
* [ ] What `--prefix=/install` does
* [ ] What `--no-cache-dir` does
* [ ] What `docker run` does
* [ ] What `-d` does
* [ ] What `-i` does
* [ ] What `-t` does in `docker run`
* [ ] What `-it` means
* [ ] What `-dit` means
* [ ] What `--name` does
* [ ] What `-p` does
* [ ] Difference between host port and container port
* [ ] Why `localhost:8082` can reach a container listening on `5000`
* [ ] Why `localhost:5000` may not work
* [ ] Why a port can be "already allocated"
* [ ] Difference between `EXPOSE` and `-p`
* [ ] Why Flask uses `0.0.0.0` inside a container
* [ ] Difference between `127.0.0.1`, `0.0.0.0`, and a container IP
* [ ] How to inspect running containers
* [ ] How to inspect logs
* [ ] How to enter a container
* [ ] How to inspect image layers/history

---

# 60. The One Diagram to Remember

```text
                     DOCKER

┌──────────────────────────────────────────────────────┐
│                    HOST MACHINE                      │
│                                                      │
│              Browser / curl                          │
│                    │                                 │
│                    │ localhost:8082                  │
│                    ↓                                 │
│          ┌─────────────────────┐                     │
│          │    Docker Engine    │                     │
│          │                     │                     │
│          │   -p 8082:5000      │                     │
│          │        │            │                     │
│          └────────┼────────────┘                     │
│                   ↓                                  │
│          ┌─────────────────────┐                     │
│          │      CONTAINER      │                     │
│          │                     │                     │
│          │       :5000         │                     │
│          │         │           │                     │
│          │         ↓           │                     │
│          │       Flask         │                     │
│          │                     │                     │
│          └─────────────────────┘                     │
│                                                      │
└──────────────────────────────────────────────────────┘


Application:
    port = 5000

Dockerfile:
    EXPOSE 5000

Docker:
    -p 8082:5000

Browser:
    localhost:8082
```

> **Core rule:**
> `EXPOSE` tells you/document the **container port**.
> `-p HOST:CONTAINER` creates the actual **host → container forwarding**.
> The application itself decides which port it actually listens on.
