# Docker Module 4 --- Docker Compose & Task Manager Hands-On

> Complete notes from the Docker Compose learning and Task Manager
> hands-on practice.

------------------------------------------------------------------------

# 1. What is Docker Compose?

Docker Compose is a tool for defining and running **multi-container
applications** using a YAML configuration file.

Instead of manually running several containers:

``` bash
docker run ...
docker run ...
docker run ...
docker run ...
```

we describe the application in:

``` text
compose.yaml
```

and start the complete stack with:

``` bash
docker compose up
```

Mental model:

``` text
Dockerfile
    ↓
How to build/package ONE service

Docker Compose
    ↓
How multiple services run TOGETHER
```

Our Task Manager contains:

``` text
React frontend
      ↓
FastAPI backend
   ↓       ↓
 MySQL   Redis
```

------------------------------------------------------------------------

# 2. Why Docker Compose?

A real application often contains multiple components.

Our project has:

1.  React frontend
2.  FastAPI backend
3.  MySQL database
4.  Redis cache

Without Compose, we would manually manage:

-   images
-   containers
-   networking
-   environment variables
-   ports
-   dependencies
-   database storage

Compose lets us define the desired setup once and start it with:

``` bash
docker compose up
```

------------------------------------------------------------------------

# 3. Dockerfile vs Docker Compose

## Dockerfile

A Dockerfile describes how to create an image for one service.

``` dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Mental model:

``` text
Dockerfile
    ↓
ONE service/image
```

## Docker Compose

Compose describes how multiple services run together:

``` text
compose.yaml
    ↓
frontend
backend
mysql
redis
```

### Core rule

> **Dockerfile = how to package a service.**
>
> **Compose = how to run multiple services together.**

------------------------------------------------------------------------

# 4. When to Introduce Compose

For this project, we first made the application work normally:

``` text
React
FastAPI
SQLite fallback
Redis optional
```

Then:

``` text
Application
    ↓
Dockerfile
    ↓
Test individual containers
    ↓
Docker Compose
    ↓
Connect multiple services
```

Compose therefore solves a real multi-container problem.

------------------------------------------------------------------------

# 5. Compose File

We use:

``` text
compose.yaml
```

Modern Docker Compose uses the Compose Specification, so we do not need
the old `version: "3"` style for this project.

------------------------------------------------------------------------

# 6. Task Manager Architecture

``` text
                         Browser
                            │
                            │ localhost:5173
                            ↓
                    ┌───────────────┐
                    │   Frontend    │
                    │ React + Nginx │
                    └───────┬───────┘
                            │
                            ↓
                    ┌───────────────┐
                    │    Backend    │
                    │    FastAPI    │
                    │     :8000     │
                    └───────┬───────┘
                            │
                   ┌────────┴────────┐
                   ↓                 ↓
             ┌──────────┐      ┌──────────┐
             │  MySQL   │      │  Redis   │
             │  :3306   │      │  :6379   │
             └────┬─────┘      └──────────┘
                  │
                  ↓
             mysql-data
                volume
```

------------------------------------------------------------------------

# 7. Project Structure

``` text
task-manager/
│
├── compose.yaml
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── src/
│   └── ...
│
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    ├── main.py
    └── ...
```

------------------------------------------------------------------------

# 8. `services`

``` yaml
services:
```

A service represents one component of the application.

Our services:

``` text
frontend
backend
mysql
redis
```

Conceptually:

``` text
Compose service
      ↓
Container
```

------------------------------------------------------------------------

# 9. `build`

Example:

``` yaml
frontend:
  build: ./frontend
```

This means Compose builds the image using:

``` text
frontend/Dockerfile
```

Similarly:

``` yaml
backend:
  build: ./backend
```

uses:

``` text
backend/Dockerfile
```

------------------------------------------------------------------------

# 10. `image`

For MySQL:

``` yaml
mysql:
  image: mysql:latest
```

For Redis:

``` yaml
redis:
  image: redis:latest
```

`image` means:

> Use an existing Docker image.

Difference:

``` yaml
build: ./backend
```

means build an image from our Dockerfile.

``` yaml
image: mysql:latest
```

means use an existing image.

------------------------------------------------------------------------

# 11. `ports`

Frontend:

``` yaml
ports:
  - "5173:80"
```

Backend:

``` yaml
ports:
  - "8000:8000"
```

Syntax:

``` text
HOST_PORT:CONTAINER_PORT
```

Therefore:

``` text
5173:80
```

means:

``` text
Host:5173
    ↓
Container:80
```

and:

``` text
8000:8000
```

means:

``` text
Host:8000
    ↓
Container:8000
```

------------------------------------------------------------------------

# 12. Application Port vs Container Port vs Host Port

Think:

``` text
Application
    ↓
listens on a port

Container
    ↓
application listens on container port

Host
    ↓
Docker publishes it using a host port
```

Frontend:

``` text
Browser
localhost:5173
      ↓
container:80
      ↓
Nginx
      ↓
React
```

Backend:

``` text
Browser/client
localhost:8000
      ↓
container:8000
      ↓
Uvicorn
      ↓
FastAPI
```

------------------------------------------------------------------------

# 13. `EXPOSE` vs `ports`

Dockerfile:

``` dockerfile
EXPOSE 8000
```

does **not** publish port 8000 to the host.

It documents the expected container port.

Compose:

``` yaml
ports:
  - "8000:8000"
```

creates the actual host-to-container forwarding.

Mental model:

``` text
EXPOSE
   ↓
Container port documentation / metadata

ports:
   ↓
Actual host → container forwarding
```

------------------------------------------------------------------------

# 14. Why `0.0.0.0`?

Inside a container:

``` text
127.0.0.1
```

means the current network environment/container.

For a containerized FastAPI server we use:

``` bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

`0.0.0.0` means:

> Listen on all available network interfaces inside the container.

Important:

``` text
127.0.0.1
    ↓
localhost/current network environment

0.0.0.0
    ↓
bind/listen on all interfaces
```

`0.0.0.0` is a bind address, not normally the browser URL.

------------------------------------------------------------------------

# 15. Why `--reload` Was Not Used

We initially considered:

``` dockerfile
CMD ["uvicorn", "main:app", "--reload"]
```

For our production-style container this was not appropriate because:

1.  It did not explicitly use `0.0.0.0`.
2.  `--reload` is mainly a development feature that watches files and
    restarts the server.

We use:

``` dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

------------------------------------------------------------------------

# 16. Backend Dockerfile

Final backend Dockerfile:

``` dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Flow:

``` text
FROM
  ↓
WORKDIR
  ↓
COPY requirements
  ↓
RUN pip install
  ↓
COPY application
  ↓
EXPOSE
  ↓
CMD
```

------------------------------------------------------------------------

# 17. React Multi-Stage Dockerfile

Final frontend Dockerfile:

``` dockerfile
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build


FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
```

Flow:

``` text
React source
    ↓
Node build stage
    ↓
npm run build
    ↓
dist/
    ↓
Nginx runtime stage
    ↓
port 80
```

------------------------------------------------------------------------

# 18. React Dockerfile Mistakes We Fixed

## Mistake 1 --- No `npm run build`

A build stage must actually create the production output:

``` dockerfile
RUN npm run build
```

This creates:

``` text
dist/
```

which is copied into Nginx.

## Mistake 2 --- Running npm in the Nginx image

Initially we had:

``` dockerfile
FROM nginx:alpine
CMD ["npm", "run", "dev"]
```

This is wrong because the final image is an Nginx image, not a Node
image.

The final runtime should be:

``` text
Nginx
  ↓
serve /usr/share/nginx/html
```

## Mistake 3 --- Development server vs production server

During local development:

``` bash
npm run dev
```

Vite commonly serves on:

``` text
localhost:5173
```

In our production Docker image:

``` text
npm run build
      ↓
dist/
      ↓
Nginx
      ↓
container port 80
```

Compose maps:

``` yaml
ports:
  - "5173:80"
```

------------------------------------------------------------------------

# 19. `environment`

Backend:

``` yaml
environment:
  DATABASE_URL: mysql+pymysql://appuser:apppassword@mysql:3306/tasks
  REDIS_URL: redis://redis:6379/0
```

These provide configuration to the backend container.

Important:

``` text
@mysql
```

and:

``` text
redis://redis
```

use Compose service names.

------------------------------------------------------------------------

# 20. Why Not `localhost` for MySQL/Redis?

Inside the backend container:

``` text
localhost
```

means:

``` text
backend container itself
```

It does not mean the MySQL or Redis container.

Compose networking provides service-name discovery.

Therefore:

``` text
mysql
```

resolves to the MySQL service.

And:

``` text
redis
```

resolves to the Redis service.

So:

``` text
Backend
   │
   ├── mysql:3306
   │
   └── redis:6379
```

This directly applies the Docker networking and DNS concepts.

------------------------------------------------------------------------

# 21. MySQL Configuration

``` yaml
mysql:
  image: mysql:latest
  environment:
    MYSQL_DATABASE: tasks
    MYSQL_USER: appuser
    MYSQL_PASSWORD: apppassword
    MYSQL_ROOT_PASSWORD: rootpassword
```

This creates/configures:

``` text
Database:
tasks

Application user:
appuser

Application password:
apppassword

Root password:
rootpassword
```

Backend connection:

``` text
mysql+pymysql://appuser:apppassword@mysql:3306/tasks
```

Breakdown:

``` text
mysql+pymysql
    ↓
SQLAlchemy database driver

appuser
    ↓
database user

apppassword
    ↓
password

mysql
    ↓
Compose service name

3306
    ↓
MySQL container port

tasks
    ↓
database
```

------------------------------------------------------------------------

# 22. Redis Configuration

``` yaml
redis:
  image: redis:latest
```

Backend:

``` yaml
REDIS_URL: redis://redis:6379/0
```

Breakdown:

``` text
redis
  ↓
protocol

redis
  ↓
Compose service name

6379
  ↓
Redis port

/0
  ↓
Redis database number
```

------------------------------------------------------------------------

# 23. `depends_on`

Frontend:

``` yaml
depends_on:
  - backend
```

Backend:

``` yaml
depends_on:
  mysql:
    condition: service_healthy
  redis:
    condition: service_started
```

`depends_on` controls dependency startup behavior.

------------------------------------------------------------------------

# 24. `service_started` vs `service_healthy`

## `service_started`

``` yaml
condition: service_started
```

Means:

> Wait until the dependency container has started.

It does not prove that the application is ready.

## `service_healthy`

``` yaml
condition: service_healthy
```

Means:

> Wait until the dependency passes its health check.

We use this for MySQL because the backend needs the database to actually
be ready.

------------------------------------------------------------------------

# 25. Why a MySQL Health Check?

A container can be running while its application is still initializing.

Without readiness checking:

``` text
MySQL container starts
        ↓
MySQL initializes
        ↓
Backend starts
        ↓
Backend tries MySQL
        ↓
MySQL not ready
        ↓
connection failure
```

Health checks help Compose wait for actual readiness.

------------------------------------------------------------------------

# 26. MySQL Health Check

Our configuration:

``` yaml
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
  interval: 5s
  timeout: 5s
  retries: 10
```

### `test`

Runs:

``` bash
mysqladmin ping -h localhost
```

inside the MySQL container.

### `interval`

``` text
5 seconds
```

between checks.

### `timeout`

``` text
5 seconds
```

maximum time for one check.

### `retries`

``` text
10
```

maximum failed attempts before unhealthy status.

------------------------------------------------------------------------

# 27. Volumes

Our MySQL configuration:

``` yaml
volumes:
  - mysql-data:/var/lib/mysql
```

and:

``` yaml
volumes:
  mysql-data:
```

Mental model:

``` text
MySQL container
      ↓
/var/lib/mysql
      ↓
mysql-data volume
```

The volume survives container recreation.

Therefore:

``` text
Remove/recreate MySQL container
            ↓
mysql-data remains
            ↓
database data remains
```

------------------------------------------------------------------------

# 28. Why MySQL Needs a Volume

Containers are replaceable.

Database data should not depend on the lifecycle of a specific MySQL
container.

Therefore:

``` text
Container lifecycle
        ≠
Database data lifecycle
```

The named volume provides persistence.

------------------------------------------------------------------------

# 29. Why MySQL and Redis Are Not Published

We did not write:

``` yaml
mysql:
  ports:
    - "3306:3306"
```

or:

``` yaml
redis:
  ports:
    - "6379:6379"
```

The backend communicates with them through the Compose network.

Only frontend and backend need host/browser access in this setup.

------------------------------------------------------------------------

# 30. Final `compose.yaml`

``` yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "5173:80"
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"

    environment:
      DATABASE_URL: mysql+pymysql://appuser:apppassword@mysql:3306/tasks
      REDIS_URL: redis://redis:6379/0

    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_started

  mysql:
    image: mysql:latest
    environment:
      MYSQL_DATABASE: tasks
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
      MYSQL_ROOT_PASSWORD: rootpassword

    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 5s
      retries: 10

    volumes:
      - mysql-data:/var/lib/mysql

  redis:
    image: redis:latest

volumes:
  mysql-data:
```

------------------------------------------------------------------------

# 31. Main Docker Compose Commands

## Start

``` bash
docker compose up
```

Starts services in the foreground.

## Start in background

``` bash
docker compose up -d
```

## Build and start

``` bash
docker compose up --build
```

## Build and start in background

``` bash
docker compose up -d --build
```

## List Compose services

``` bash
docker compose ps
```

## View all logs

``` bash
docker compose logs
```

## Follow logs

``` bash
docker compose logs -f
```

## Follow backend logs

``` bash
docker compose logs -f backend
```

## Execute command in a service

``` bash
docker compose exec backend sh
```

## Stop services

``` bash
docker compose stop
```

## Stop and remove containers/network

``` bash
docker compose down
```

## Stop, remove containers/network/volumes

``` bash
docker compose down -v
```

> Be careful with `down -v`: it removes the named volumes, including our
> `mysql-data` volume and therefore its database data.

------------------------------------------------------------------------

# 32. Docker Commands Learned Before Compose

``` bash
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

# Give a container a name
docker run --name my_app_v3 my_app:v3

# Name + detached + port mapping
docker run -d --name my_app_v3 -p 8082:5000 my_app:v3

# Running containers
docker ps

# All containers
docker ps -a

# Logs
docker logs my_app_v3

# Follow logs
docker logs -f my_app_v3

# Execute command inside container
docker exec -it my_app_v3 bash

# Use sh if bash is unavailable
docker exec -it my_app_v3 sh

# Inspect container
docker inspect my_app_v3

# Show processes
docker top my_app_v3

# Resource usage
docker stats

# Image history
docker history my_app:v3

# Stop
docker stop my_app_v3

# Remove
docker rm my_app_v3

# Force stop + remove
docker rm -f my_app_v3
```

------------------------------------------------------------------------

# 33. Important Docker Flags

  -----------------------------------------------------------------------
  Flag                                Meaning
  ----------------------------------- -----------------------------------
  `-f`                                Select Dockerfile in
                                      `docker build`; follow logs in
                                      `docker logs`

  `-t`                                Tag/name image in `docker build`

  `-p`                                Publish/map host port to container
                                      port

  `-d`                                Detached/background mode

  `-i`                                Keep STDIN open

  `-t` in `docker run`                Allocate pseudo-terminal

  `-it`                               Interactive terminal

  `-dit`                              Detached + interactive + terminal

  `--name`                            Give container a custom name

  `--prefix`                          Specify installation prefix for
                                      commands such as pip

  `--from`                            Copy from another Docker build
                                      stage

  `--no-cache-dir`                    Disable pip download cache
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 34. Dockerfile Instructions Learned

## `FROM`

``` dockerfile
FROM python:3.11
```

Defines the base image.

## `WORKDIR`

``` dockerfile
WORKDIR /app
```

Sets the working directory inside the image/container.

Mental model:

``` bash
cd /app
```

## `COPY`

``` dockerfile
COPY requirements.txt .
```

Copies files from the build context into the image.

## `RUN`

``` dockerfile
RUN pip install -r requirements.txt
```

Runs during image build time.

## `CMD`

``` dockerfile
CMD ["python", "app.py"]
```

Defines the default command executed when the container starts.

## `EXPOSE`

``` dockerfile
EXPOSE 8000
```

Documents the expected container port. It does not publish it.

------------------------------------------------------------------------

# 35. `RUN` vs `CMD`

This distinction is important.

``` text
RUN
 ↓
IMAGE BUILD TIME
```

Example:

``` dockerfile
RUN pip install -r requirements.txt
```

while:

``` text
CMD
 ↓
CONTAINER START TIME
```

Example:

``` dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Mental model:

``` text
Dockerfile
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

------------------------------------------------------------------------

# 36. Multi-Stage Builds

A multi-stage Dockerfile uses multiple `FROM` instructions.

Example:

``` dockerfile
FROM node:22-alpine AS build

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
```

Mental model:

``` text
BUILD ENVIRONMENT
        ↓
Build application
        ↓
Copy required artifacts
        ↓
RUNTIME ENVIRONMENT
```

This avoids carrying the complete build environment into the final
runtime image.

------------------------------------------------------------------------

# 37. `AS build` / `AS builder`

Example:

``` dockerfile
FROM node:22-alpine AS build
```

The build stage gets the name:

``` text
build
```

Later:

``` dockerfile
COPY --from=build ...
```

copies files from that stage.

------------------------------------------------------------------------

# 38. `COPY --from`

Normal:

``` dockerfile
COPY source destination
```

copies from the build context.

Multi-stage:

``` dockerfile
COPY --from=build /app/dist /usr/share/nginx/html
```

copies from another Docker build stage.

------------------------------------------------------------------------

# 39. Python Multi-Stage Concepts Learned

Earlier Docker practice also covered:

``` dockerfile
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
```

### `--prefix=/install`

Installs dependencies under:

``` text
/install
```

which can later be copied into a runtime stage.

### `--no-cache-dir`

Prevents pip from keeping its package download cache.

They solve different problems:

``` text
--prefix=/install
    ↓
Where dependencies are installed

--no-cache-dir
    ↓
Don't keep pip download cache
```

------------------------------------------------------------------------

# 40. Build Context

Example:

``` bash
docker build -f Dockerfile.v1 -t my_app:v1 .
```

The final:

``` text
.
```

means:

> Use the current directory as the build context.

Docker can use files inside that context with:

``` dockerfile
COPY
```

A Dockerfile cannot arbitrarily copy files from outside the build
context.

------------------------------------------------------------------------

# 41. `docker build`

Example:

``` bash
docker build -f Dockerfile.v1 -t my_app:v1 .
```

Breakdown:

``` text
docker
  ↓
Docker CLI

build
  ↓
Build image

-f Dockerfile.v1
  ↓
Choose Dockerfile

-t my_app:v1
  ↓
Image name + tag

.
  ↓
Build context
```

------------------------------------------------------------------------

# 42. Image vs Container

## Image

An image is a template/package.

Example:

``` text
my_app:v3
```

It contains application files, dependencies, filesystem layers, and
configuration.

## Container

A container is a created/running instance of an image.

``` text
my_app:v3
      ↓
Container
      ↓
my_app_v3
```

Multiple containers can come from the same image.

------------------------------------------------------------------------

# 43. Port Mental Model

Always remember:

``` text
HOST PORT : CONTAINER PORT
```

Example:

``` bash
docker run -p 8082:5000 my_app:v3
```

means:

``` text
Your computer
localhost:8082
      ↓
Docker
      ↓
Container:5000
      ↓
Application
```

The application continues listening on:

``` text
5000
```

------------------------------------------------------------------------

# 44. Why `localhost:5000` Can Fail

With:

``` bash
docker run -p 8082:5000 my_app:v3
```

we created:

``` text
localhost:8082
      ↓
container:5000
```

not:

``` text
localhost:5000
      ↓
container:5000
```

Therefore:

``` text
http://localhost:8082
```

is the correct host URL.

------------------------------------------------------------------------

# 45. Port Already Allocated

If Docker reports:

``` text
port is already allocated
```

the host port is already being used.

Check:

``` bash
docker ps
```

Look at:

``` text
PORTS
```

Example:

``` text
0.0.0.0:8081->80/tcp
```

means:

``` text
Host 8081
   ↓
Container 80
```

Use another host port or stop the process/container using that port.

------------------------------------------------------------------------

# 46. `-d`, `-it`, `-dit`

## Detached

``` bash
docker run -d my_app
```

Runs in the background.

## Interactive terminal

``` bash
docker run -it ubuntu bash
```

`-i` = interactive.

`-t` = pseudo-terminal.

## Detached + interactive + terminal

``` bash
docker run -dit ubuntu bash
```

Combines:

``` text
-d
-i
-t
```

------------------------------------------------------------------------

# 47. `--name`

``` bash
docker run --name my_app_v3 my_app:v3
```

Gives the container a predictable name.

Then:

``` bash
docker logs my_app_v3
docker stop my_app_v3
docker rm my_app_v3
```

become easier.

------------------------------------------------------------------------

# 48. Container Inspection Commands

Useful commands:

``` bash
docker ps
docker ps -a
docker logs <container>
docker logs -f <container>
docker exec -it <container> sh
docker inspect <container>
docker stats
docker top <container>
docker history <image>
docker images
```

These answer questions such as:

``` text
Is it running?
What went wrong?
What processes are running?
What ports are mapped?
What is its configuration?
How much CPU/memory is being used?
How was the image built?
```

------------------------------------------------------------------------

# 49. Hands-On --- Task Manager

## Stack

``` text
Frontend:
React + Vite

Backend:
Python + FastAPI

Database:
MySQL

Cache:
Redis

Production frontend server:
Nginx
```

Application features:

``` text
Create task
View tasks
Update task
Delete task
Mark task completed
```

------------------------------------------------------------------------

# 50. Hands-On --- Local Application Before Docker

Backend:

``` bash
cd backend
python -m venv venv
venv\Scriptsctivate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend:

``` text
http://localhost:8000
```

Frontend:

``` bash
cd frontend
npm install
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

The application could fall back to local SQLite when external database
configuration was not provided, and Redis could be bypassed when
unavailable.

------------------------------------------------------------------------

# 51. Hands-On --- Final Compose Startup

From the folder containing `compose.yaml`:

``` bash
docker compose up --build
```

Or:

``` bash
docker compose up -d --build
```

Expected host access:

``` text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000
```

------------------------------------------------------------------------

# 52. Hands-On --- Final Ports

  Component       Container Port       Host Port Purpose
  ------------- ---------------- --------------- -------------------
  React/Nginx                 80            5173 Browser access
  FastAPI                   8000            8000 API access
  MySQL                     3306   Not published Internal database
  Redis                     6379   Not published Internal cache

------------------------------------------------------------------------

# 53. Hands-On --- Final Communication

``` text
Browser
   ↓
localhost:5173
   ↓
Frontend/Nginx
   ↓
Backend
   ↓
MySQL / Redis
```

Backend container:

``` text
mysql:3306
redis:6379
```

not:

``` text
localhost:3306
localhost:6379
```

------------------------------------------------------------------------

# 54. Repository

Task Manager repository:

``` text
https://github.com/Nandani2024-tech/task_manager_docker_compose
```

Recommended repository structure:

``` text
task-manager/
├── compose.yaml
├── frontend/
│   ├── Dockerfile
│   └── ...
├── backend/
│   ├── Dockerfile
│   └── ...
└── README.md
```

------------------------------------------------------------------------

# 55. Docker Compose Checklist

-   [ ] What Docker Compose is
-   [ ] Why Compose is useful
-   [ ] Dockerfile vs Compose
-   [ ] What `compose.yaml` is
-   [ ] What a service is
-   [ ] `services`
-   [ ] `build`
-   [ ] `image`
-   [ ] `ports`
-   [ ] `environment`
-   [ ] `depends_on`
-   [ ] `service_started`
-   [ ] `service_healthy`
-   [ ] `healthcheck`
-   [ ] `volumes`
-   [ ] Compose networking
-   [ ] Service-name DNS
-   [ ] Why containers should not use `localhost` to reach another
    service
-   [ ] Why MySQL needs persistent storage
-   [ ] Why MySQL/Redis don't need host ports in this project
-   [ ] `docker compose up`
-   [ ] `docker compose up -d`
-   [ ] `docker compose up --build`
-   [ ] `docker compose ps`
-   [ ] `docker compose logs`
-   [ ] `docker compose logs -f`
-   [ ] `docker compose exec`
-   [ ] `docker compose stop`
-   [ ] `docker compose down`
-   [ ] `docker compose down -v`
-   [ ] Why health checks are needed
-   [ ] How the Task Manager services communicate

------------------------------------------------------------------------

# 56. Complete Docker Learning Pipeline

``` text
Application
     ↓
Dockerfile
     ↓
Docker Image
     ↓
Docker Container
     ↓
Port Mapping
     ↓
Docker Networking
     ↓
Volumes
     ↓
Multiple Containers
     ↓
Docker Compose
     ↓
Services
     ↓
depends_on
     ↓
healthcheck
     ↓
Persistent Multi-Container Application
```

------------------------------------------------------------------------

# 57. One Final Mental Model

``` text
                         HOST MACHINE
                              │
                  ┌───────────┴───────────┐
                  │                       │
             :5173 │                  :8000
                  ↓                       ↓
             ┌─────────┐            ┌─────────┐
             │ Nginx   │            │ FastAPI │
             │ React   │──────────→│ Backend │
             │ :80     │            │ :8000   │
             └─────────┘            └────┬────┘
                                         │
                                  ┌──────┴──────┐
                                  ↓             ↓
                             ┌─────────┐   ┌─────────┐
                             │ MySQL   │   │ Redis   │
                             │ :3306   │   │ :6379   │
                             └────┬────┘   └─────────┘
                                  │
                                  ↓
                             mysql-data
                               volume
```

Core rules:

``` text
Dockerfile
    ↓
Build one service

Compose
    ↓
Run multiple services together

EXPOSE
    ↓
Documents container port

ports:
    ↓
Host → container forwarding

depends_on
    ↓
Controls dependency startup

healthcheck
    ↓
Checks service health/readiness

volume
    ↓
Persists data

service name
    ↓
Container-to-container DNS/discovery

localhost
    ↓
Current container/network namespace
```
