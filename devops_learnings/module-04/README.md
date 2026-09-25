# Docker Module 4 — Docker Networking & Volumes

> **Goal:** Understand how Docker containers communicate with each other and with the outside world, how Docker provides networking through different network drivers, and how Docker provides persistent storage through volumes and mounts.

---

# 1. What We Study in Module 4

Module 4 focuses on two major Docker concepts:

```text
                    Docker Container
                           │
              ┌────────────┴────────────┐
              │                         │
          NETWORKING                 STORAGE
              │                         │
       ┌──────┼──────┐            ┌─────┼─────┐
       │      │      │            │     │     │
     Bridge  Host   None        Volume Bind  Tmpfs
       │
   Overlay
   Macvlan
```

The important questions are:

### Networking

* How does a container get an IP address?
* How does one container communicate with another?
* How does a container communicate with the internet?
* How does the host communicate with a container?
* What is a Docker network?
* What is a network driver?
* What is the difference between the default bridge and a user-defined bridge?
* How does Docker DNS work?
* What are bridge, host, none, overlay and macvlan networks?
* What is the difference between container networking and publishing a port?
* Why does `localhost` behave differently inside a container?

### Storage

* Where does data inside a container actually live?
* What happens to data when a container is deleted?
* What is a Docker volume?
* What is a bind mount?
* What is `tmpfs`?
* What is the difference between a named volume and a bind mount?
* When should persistent data use a volume?
* How do multiple containers share data?

---

# 2. The Basic Docker Networking Mental Model

When Docker starts a container, Docker normally gives that container access to a network.

For example:

```bash
docker run -it ubuntu bash
```

The container may receive an address such as:

```text
172.17.0.2
```

A simplified view is:

```text
Host Machine
│
├── Docker Engine
│
│   └── Docker Network
│       │
│       ├── Container A
│       │    IP: 172.17.0.2
│       │
│       └── Container B
│            IP: 172.17.0.3
│
└── Physical Network / Internet
```

Docker creates the networking infrastructure needed to connect containers.

---

# 3. Container Network Interfaces

Inside a container:

```bash
ip a
```

You may see:

```text
1: lo
    inet 127.0.0.1/8

2: eth0
    inet 172.17.0.2/16
```

There are two important interfaces.

## 3.1 `lo` — Loopback

```text
127.0.0.1
```

This means:

> This container itself.

For example:

```bash
curl http://127.0.0.1:3000
```

means:

```text
Container → Container itself
```

It does **not** mean:

```text
Container → Host machine
```

This distinction is extremely important.

---

## 3.2 `eth0`

`eth0` is normally the container's main network interface.

For example:

```text
eth0
└── 172.17.0.2
```

This address allows the container to communicate through its Docker network.

---

# 4. What Is a Docker Network?

A Docker network is a logical network managed by Docker that allows containers to communicate.

You can see existing networks using:

```bash
docker network ls
```

Example:

```text
NETWORK ID     NAME      DRIVER    SCOPE
abc123         bridge    bridge    local
def456         host      host      local
ghi789         none      null      local
```

The important fields are:

| Field      | Meaning                   |
| ---------- | ------------------------- |
| NETWORK ID | Identifier of the network |
| NAME       | Docker network name       |
| DRIVER     | Network driver being used |
| SCOPE      | Where the network exists  |

---

# 5. Docker Network Drivers

Docker supports different network drivers.

The important ones to understand are:

```text
Docker Network Drivers

├── bridge
├── host
├── none
├── overlay
└── macvlan
```

Each one provides a different networking model.

---

# 6. Bridge Network

The **bridge** driver is the most common networking mode for ordinary containers.

Conceptually:

```text
                 Host
                  │
          Docker Bridge
                  │
       ┌──────────┼──────────┐
       │          │          │
   Container A Container B Container C
   172.17.0.2  172.17.0.3  172.17.0.4
```

Containers attached to the same bridge network can communicate with each other.

---

# 7. Default Bridge Network

Docker creates a default network called:

```text
bridge
```

Check it:

```bash
docker network ls
```

You should see something similar to:

```text
NETWORK ID     NAME      DRIVER
xxxxxx         bridge    bridge
xxxxxx         host      host
xxxxxx         none      null
```

Inspect it:

```bash
docker network inspect bridge
```

---

# 8. Running a Container on the Default Bridge

Run two containers:

```bash
docker run -dit --name c3 busybox
docker run -dit --name c4 busybox
```

Check their IP addresses:

```bash
docker inspect c3
docker inspect c4
```

You can also use:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c3
```

and:

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' c4
```

---

# 9. Default Bridge vs User-Defined Bridge

This is one of the most important concepts in Module 4.

Docker has a default bridge network:

```text
bridge
```

But you can create your own bridge network:

```bash
docker network create mynet
```

Now:

```bash
docker network ls
```

may show:

```text
bridge
host
none
mynet
```

`mynet` is a **user-defined bridge network**.

---

# 10. User-Defined Bridge Network

Create two containers:

```bash
docker run -dit --name c1 --network mynet busybox
docker run -dit --name c2 --network mynet busybox
```

Now test:

```bash
docker exec -it c1 ping -c 3 c2
```

This works because Docker provides DNS-based name resolution on user-defined networks.

The important idea is:

```text
c1
 │
 │ asks Docker DNS:
 │ "Where is c2?"
 ↓
Docker Embedded DNS
 │
 ↓
c2
```

The container does not need to know the IP address manually.

---

# 11. Docker Embedded DNS

Docker provides an embedded DNS server for user-defined networks.

Inside a container, you may see:

```text
127.0.0.11
```

in DNS configuration.

For example:

```bash
cat /etc/resolv.conf
```

may contain:

```text
nameserver 127.0.0.11
```

This means Docker is providing DNS resolution for the container.

Therefore:

```bash
ping c2
```

can resolve:

```text
c2 → 172.x.x.x
```

without manually specifying the IP.

---

# 12. Why Container Names Matter

Suppose:

```text
mynet
│
├── c1
└── c2
```

From `c1`:

```bash
ping c2
```

Docker resolves:

```text
c2 → c2's container IP
```

This is extremely useful for applications.

For example:

```text
frontend
    │
    │ HTTP
    ↓
backend
    │
    │ PostgreSQL
    ↓
database
```

Instead of hardcoding:

```text
172.18.0.4
```

the application can use:

```text
http://backend:5000
```

and:

```text
postgres://database:5432
```

The container name becomes the hostname.

---

# 13. Practical Network Exercise

Create a network:

```bash
docker network create mynet
```

Create two containers:

```bash
docker run -dit --name c1 --network mynet busybox
docker run -dit --name c2 --network mynet busybox
```

Test:

```bash
docker exec -it c1 ping -c 3 c2
```

Expected concept:

```text
c1
 │
 │ resolve "c2"
 ↓
Docker DNS
 │
 ↓
c2
```

---

# 14. Inspect the Network

Run:

```bash
docker network inspect mynet
```

Look for:

```text
Containers
```

You should find:

```text
c1
c2
```

This allows you to see which containers are connected to the network.

---

# 15. Connect an Existing Container to a Network

A container can be connected to another network after creation.

Create:

```bash
docker network create mynet
```

Create a container:

```bash
docker run -dit --name app busybox
```

Connect it:

```bash
docker network connect mynet app
```

Inspect:

```bash
docker inspect app
```

The container can now have network connectivity through the additional network.

---

# 16. Disconnect a Container

To disconnect:

```bash
docker network disconnect mynet app
```

The container is removed from that Docker network.

---

# 17. Multiple Networks

A container can be attached to multiple networks.

Example:

```text
             frontend-net
                  │
                  │
               frontend
                  │
             ┌────┴────┐
             │ backend │
             └────┬────┘
                  │
              backend-net
                  │
               database
```

This can be used to control which containers can communicate with each other.

For example:

```text
frontend
   │
   ↓
backend

backend
   │
   ↓
database
```

The frontend does not necessarily need direct access to the database.

---

# 18. Network Isolation

Docker networks can be used to separate application components.

Example:

```text
frontend-net
│
├── frontend
└── backend

database-net
│
├── backend
└── database
```

The backend belongs to both networks.

The database only belongs to:

```text
database-net
```

This creates a basic network boundary.

---

# 19. Port Publishing Is Different from Networking

This distinction is extremely important.

Suppose a container runs:

```text
Container
Port 3000
```

Running:

```bash
docker run -p 8080:3000 myapp
```

means:

```text
Host port 8080
        │
        ↓
Container port 3000
```

Diagram:

```text
Browser
   │
   │ localhost:8080
   ↓
Host
   │
   │ port mapping
   ↓
Container
   │
   └── port 3000
```

Port publishing is primarily about making a container service reachable through the host.

---

# 20. Container-to-Container Communication Does Not Require `-p`

Suppose:

```bash
docker run -dit --name backend --network mynet mybackend
docker run -dit --name frontend --network mynet myfrontend
```

The frontend can communicate with:

```text
backend:5000
```

without:

```bash
-p 5000:5000
```

Why?

Because both containers are already on the same Docker network.

```text
frontend
   │
   │ backend:5000
   ↓
backend
```

No host port is required.

---

# 21. Host Network

The `host` network driver removes much of Docker's network isolation.

Run:

```bash
docker run --network host nginx
```

Conceptually:

```text
Normal bridge:

Host
 │
Docker network
 │
Container
```

Host mode:

```text
Host Network
     │
     └── Container
```

The container shares the host's network namespace.

Therefore the container does not receive a separate normal Docker bridge IP in the same way.

---

# 22. Why Host Networking Is Different

With bridge networking:

```text
Container IP
172.x.x.x
```

With host networking:

```text
Container
    │
    └── Host's network stack
```

This can reduce networking isolation and changes how ports work.

For example, a service listening on:

```text
0.0.0.0:8080
```

inside the container is using the host network namespace.

---

# 23. None Network

The `none` network provides essentially no normal external networking.

Run:

```bash
docker run -it --network none busybox sh
```

Then:

```bash
ip a
```

You will primarily see the loopback interface.

Conceptually:

```text
Container
   │
   └── lo
       127.0.0.1
```

No normal Docker network connection is provided.

This can be useful when a container should not have network connectivity.

---

# 24. Comparing Bridge, Host and None

| Network  | Separate network namespace | Container gets normal Docker IP | External networking |
| -------- | -------------------------: | ------------------------------: | ------------------: |
| `bridge` |                        Yes |                             Yes |                 Yes |
| `host`   |      No / shared with host |  Not in the normal bridge sense |                 Yes |
| `none`   |                        Yes |        No normal Docker network |                  No |

The key idea:

```text
bridge → isolated Docker networking
host   → use host networking
none   → no normal networking
```

---

# 25. Overlay Network

The `overlay` driver is designed for networking across multiple Docker hosts.

Conceptually:

```text
Docker Host A                    Docker Host B
      │                                │
   Container A                     Container B
      │                                │
      └──────── Overlay Network ───────┘
```

Instead of only connecting containers on one machine, an overlay network can connect containers across Docker hosts.

It is mainly associated with Docker Swarm and multi-host container networking.

---

# 26. Why Overlay Networks Exist

Without an overlay network:

```text
Host A
└── Network A

Host B
└── Network B
```

Containers on separate hosts are not automatically on the same local Docker bridge.

Overlay networking creates a logical network spanning hosts:

```text
             Overlay Network
          ┌──────────────────┐
          │                  │
       Host A             Host B
          │                  │
      Container A       Container B
```

The application can communicate across the logical Docker network.

---

# 27. Macvlan Network

The `macvlan` driver gives containers their own MAC addresses and allows them to appear more directly on the physical network.

Conceptually:

```text
Physical Network
       │
   ┌───┼────┐
   │   │    │
 Host C1   C2
     │     │
   MAC1   MAC2
```

Each container can appear more like a physical network device.

This is useful in specialized networking scenarios where containers need to integrate directly with an existing Layer 2 network.

---

# 28. Network Driver Comparison

| Driver    | Main purpose                                   |
| --------- | ---------------------------------------------- |
| `bridge`  | Normal container networking on one Docker host |
| `host`    | Container uses host network                    |
| `none`    | Disable normal networking                      |
| `overlay` | Multi-host Docker networking                   |
| `macvlan` | Containers appear directly on physical network |

For normal application development, the most important ones are:

```text
bridge
host
none
```

Understand:

```text
overlay → multi-host
macvlan → direct physical-network integration
```

---

# 29. Docker DNS vs External DNS

There are two different DNS concepts to understand.

### Container-to-container DNS

Example:

```bash
ping backend
```

Docker can resolve:

```text
backend → container IP
```

using its embedded DNS.

### Internet DNS

Example:

```bash
ping google.com
```

or:

```bash
dig google.com
```

This requires DNS resolution for an external domain.

Conceptually:

```text
Container
   │
   ├── backend
   │      ↓
   │   Docker DNS
   │
   └── google.com
          ↓
      External DNS
```

---

# 30. Testing DNS

Inside a container with DNS tools installed:

```bash
dig google.com
```

or:

```bash
nslookup google.com
```

For a user-defined network, test:

```bash
ping c2
```

The two tests answer different questions:

```text
dig google.com
    ↓
Can I resolve an external domain?

ping c2
    ↓
Can Docker resolve another container?
```

---

# 31. Container Outbound Networking

A container on a normal bridge network can usually access the internet.

For example:

```bash
curl -I https://docker.com
```

Conceptually:

```text
Container
    │
    ↓
Docker Network
    │
    ↓
Host
    │
    ↓
Internet
```

Docker performs the networking/NAT necessary for normal outbound connectivity.

---

# 32. `localhost` Inside a Container

This is one of the most common Docker networking mistakes.

Inside a container:

```text
localhost
127.0.0.1
```

means:

> This container.

It does not automatically mean:

> My Windows/Linux host.

Example:

```text
Host
└── localhost:8080

Container
└── localhost:8080
```

These are different network contexts.

---

# 33. `0.0.0.0` vs `127.0.0.1`

Suppose an application inside a container listens on:

```text
127.0.0.1:5000
```

It is listening only on the container's loopback interface.

An application intended to receive connections through the container network generally needs to listen on:

```text
0.0.0.0:5000
```

Meaning:

```text
Listen on all available interfaces.
```

This is why Dockerized web applications commonly use:

```text
0.0.0.0
```

rather than:

```text
127.0.0.1
```

for their server bind address.

---

# 34. Inspecting Container Ports

Use:

```bash
docker port <container>
```

Example:

```bash
docker port myapp
```

You can also inspect:

```bash
docker inspect myapp
```

Look at:

```text
NetworkSettings
```

and:

```text
Ports
```

---

# 35. Network Commands — Quick Reference

```bash
docker network ls
```

List networks.

```bash
docker network inspect mynet
```

Inspect a network.

```bash
docker network create mynet
```

Create a network.

```bash
docker network rm mynet
```

Remove a network.

```bash
docker network connect mynet container
```

Connect a container.

```bash
docker network disconnect mynet container
```

Disconnect a container.

```bash
docker run --network mynet ...
```

Start a container on a specific network.

---

# 36. Cleaning Up the Network Exercise

Remove containers:

```bash
docker rm -f c1 c2 c3 c4
```

Remove the network:

```bash
docker network rm mynet
```

---

# 37. Docker Storage

Networking controls:

```text
How containers communicate
```

Storage controls:

```text
Where container data lives
```

A normal container has a writable layer.

Conceptually:

```text
Docker Image
     │
     │ read-only
     ↓
Container Writable Layer
     │
     └── changes made by application
```

The problem is:

> What happens to that data when the container is deleted?

The writable layer is associated with the container.

Therefore, important application data should not normally depend on the container's writable layer.

---

# 38. Why Persistent Storage Is Needed

Consider a database container:

```text
PostgreSQL Container
        │
        └── database files
```

If the container is deleted:

```bash
docker rm postgres
```

you do not want your database data to disappear with the container.

Instead:

```text
PostgreSQL Container
        │
        ↓
Persistent Storage
```

This is where Docker volumes and mounts become important.

---

# 39. Docker Storage Options

The three important storage mechanisms are:

```text
Docker Storage
│
├── Volumes
├── Bind mounts
└── tmpfs mounts
```

---

# 40. Volumes

A Docker volume is storage managed by Docker.

Create one:

```bash
docker volume create mydata
```

List volumes:

```bash
docker volume ls
```

Inspect:

```bash
docker volume inspect mydata
```

---

# 41. Named Volume

A named volume has a name:

```text
mydata
```

Example:

```bash
docker run -d \
  --name db \
  -v mydata:/data \
  alpine
```

Conceptually:

```text
Docker
│
├── Container
│     └── /data
│
└── Volume
      mydata
```

The container sees:

```text
/data
```

but the actual storage is managed by Docker.

---

# 42. Volume Persistence

Start a container:

```bash
docker run -dit \
  --name data1 \
  -v mydata:/data \
  alpine sh
```

Create a file:

```bash
docker exec data1 sh -c 'echo "hello" > /data/test.txt'
```

Check:

```bash
docker exec data1 cat /data/test.txt
```

Now remove the container:

```bash
docker rm -f data1
```

Create another container using the same volume:

```bash
docker run -dit \
  --name data2 \
  -v mydata:/data \
  alpine sh
```

Check:

```bash
docker exec data2 cat /data/test.txt
```

The data still exists.

This demonstrates:

```text
Container 1
     │
     ↓
  mydata
     ↑
     │
Container 2
```

The data belongs to the volume, not the individual container.

---

# 43. Volume Lifecycle

This is an important mental model:

```text
Container lifecycle:

create → start → stop → delete

Volume lifecycle:

create → use → continue existing
```

Deleting a container does not automatically mean:

```text
delete its named volume
```

The volume can continue to exist independently.

---

# 44. Named Volume vs Container Writable Layer

### Container writable layer

```text
Container
└── Writable Layer
```

Data is tied to the container.

### Named volume

```text
Container
    │
    ↓
Named Volume
```

Data exists independently of the container.

Therefore:

```text
Temporary container data
→ writable layer

Persistent application data
→ volume
```

---

# 45. Bind Mounts

A bind mount maps an actual directory from the host into the container.

Example:

```bash
docker run -it \
  -v /host/path:/container/path \
  alpine
```

Conceptually:

```text
Host
└── /host/path
        │
        │ bind mount
        ↓
Container
└── /container/path
```

The directory belongs to the host.

Docker simply exposes it inside the container.

---

# 46. Example Bind Mount

Suppose the host has:

```text
project/
├── index.html
└── app.js
```

Run:

```bash
docker run -it \
  -v "$PWD/project:/app" \
  alpine sh
```

Inside the container:

```bash
ls /app
```

You see:

```text
index.html
app.js
```

The files are actually stored on the host.

---

# 47. Why Bind Mounts Are Useful

Bind mounts are useful when you want the container to work directly with host files.

Common development example:

```text
Host source code
       │
       ↓
Bind mount
       │
       ↓
Container application
```

If you modify:

```text
host/app.js
```

the container sees the change because it is using the same mounted directory.

---

# 48. Volume vs Bind Mount

This distinction is extremely important.

| Feature                             | Named Volume   | Bind Mount         |
| ----------------------------------- | -------------- | ------------------ |
| Managed by Docker                   | Yes            | No                 |
| Source location                     | Docker-managed | Explicit host path |
| Easy persistent application storage | Yes            | Yes                |
| Direct host filesystem access       | Less direct    | Yes                |
| Common development use              | Sometimes      | Very common        |
| Common database storage             | Very common    | Possible           |

Mental model:

```text
Volume:
Docker manages the storage.

Bind mount:
You choose the host directory.
```

---

# 49. Short `-v` Syntax

You can write:

```bash
-v source:destination
```

Examples:

Named volume:

```bash
-v mydata:/data
```

Bind mount:

```bash
-v /home/user/project:/app
```

Docker determines the type based on the source.

---

# 50. `--mount` Syntax

Docker also provides a more explicit syntax:

```bash
--mount type=volume,source=mydata,target=/data
```

For a bind mount:

```bash
--mount type=bind,source=/host/project,target=/app
```

This makes the mount type explicit.

---

# 51. Why `--mount` Can Be Easier to Understand

Compare:

```bash
-v mydata:/data
```

with:

```bash
--mount type=volume,source=mydata,target=/data
```

The second form explicitly tells you:

```text
type   = volume
source = mydata
target = /data
```

For bind mount:

```bash
--mount type=bind,source=/host/project,target=/app
```

means:

```text
type   = bind
source = /host/project
target = /app
```

---

# 52. `tmpfs` Mount

A `tmpfs` mount stores data in memory rather than persistent disk storage.

Example:

```bash
docker run -it \
  --tmpfs /app/tmp \
  alpine sh
```

Conceptually:

```text
Container
    │
    └── /app/tmp
            │
            ↓
           RAM
```

---

# 53. Characteristics of `tmpfs`

`tmpfs` data:

* is temporary
* is stored in memory
* is not intended for persistent storage
* disappears when the container stops/is removed depending on lifecycle
* can be useful for temporary data

Mental model:

```text
Volume
→ persistent

Bind mount
→ host filesystem

tmpfs
→ memory
```

---

# 54. Storage Comparison

| Storage        | Location               |          Persistent | Managed by     |
| -------------- | ---------------------- | ------------------: | -------------- |
| Writable layer | Container storage      | No, container-bound | Docker         |
| Volume         | Docker-managed storage |                 Yes | Docker         |
| Bind mount     | Host filesystem        |                 Yes | User/host      |
| tmpfs          | Memory                 |                  No | Docker/runtime |

---

# 55. Inspecting Volumes

List:

```bash
docker volume ls
```

Inspect:

```bash
docker volume inspect mydata
```

The inspection output contains information such as:

```text
Name
Driver
Mountpoint
Scope
```

The exact mountpoint depends on the Docker environment.

---

# 56. Removing a Volume

Remove:

```bash
docker volume rm mydata
```

Docker will normally refuse to remove a volume that is still in use by a container.

This protects against accidentally removing active storage.

---

# 57. Pruning Unused Volumes

Docker can remove unused volumes with:

```bash
docker volume prune
```

This should be used carefully.

Unused does not necessarily mean:

```text
unimportant
```

Always inspect what will be removed before destructive cleanup in an environment containing important data.

---

# 58. Sharing a Volume Between Containers

Multiple containers can mount the same volume.

Example:

```bash
docker volume create shared-data
```

Container 1:

```bash
docker run -dit \
  --name writer \
  -v shared-data:/data \
  alpine sh
```

Container 2:

```bash
docker run -dit \
  --name reader \
  -v shared-data:/data \
  alpine sh
```

Now:

```text
writer
  │
  ↓
shared-data
  ↑
  │
reader
```

Both containers see the same mounted data.

---

# 59. Practical Shared Volume Exercise

Create:

```bash
docker volume create shared-data
```

Start writer:

```bash
docker run -dit \
  --name writer \
  -v shared-data:/data \
  alpine sh
```

Write:

```bash
docker exec writer sh -c 'echo "Docker storage" > /data/message.txt'
```

Start reader:

```bash
docker run -dit \
  --name reader \
  -v shared-data:/data \
  alpine sh
```

Read:

```bash
docker exec reader cat /data/message.txt
```

Expected:

```text
Docker storage
```

The important lesson:

```text
The containers are separate.

The storage is shared.
```

---

# 60. Read-Only Mounts

A mount can be made read-only.

Using `-v`:

```bash
-v mydata:/data:ro
```

Using `--mount`:

```bash
--mount type=volume,source=mydata,target=/data,readonly
```

The container can read:

```text
/data
```

but should not be able to modify it through that mount.

---

# 61. Why Read-Only Mounts Matter

Suppose:

```text
Application container
        │
        ↓
Configuration files
```

If the application only needs to read the files, mounting them read-only reduces the ability of the application to modify them.

Conceptually:

```text
Container
   │
   │ READ
   ↓
Storage
```

rather than:

```text
Container
   │
   │ READ + WRITE
   ↓
Storage
```

---

# 62. Volumes and Databases

Databases are a common example of persistent storage.

Without persistent storage:

```text
Database Container
       │
       ↓
Container Writable Layer
```

Deleting the container can lose the database files.

With a volume:

```text
Database Container
       │
       ↓
Postgres Volume
       │
       └── database files
```

Now the container can be replaced while the storage remains.

---

# 63. Application + Database Mental Model

A typical containerized application may look like:

```text
                    Docker Network
                         │
          ┌──────────────┴──────────────┐
          │                             │
      Backend                       Database
          │                             │
          │                         /data
          │                             │
          │                         DB Volume
          │
      API Port
```

Networking handles:

```text
Backend → Database
```

Storage handles:

```text
Database → Persistent Data
```

These are two separate Docker concepts.

---

# 64. Network + Volume Together

Consider:

```text
                 Docker
        ┌──────────┴──────────┐
        │                     │
     Network               Storage
        │                     │
   ┌────┴────┐             Volume
   │         │                │
Backend    DB                 │
   │         │                │
   └─────────┘                │
                             DB data
```

Networking answers:

> How do the containers communicate?

Storage answers:

> Where does the data survive?

---

# 65. Linux Network Inspection Inside a Container

These commands help understand what Docker created.

### Interfaces

```bash
ip a
```

Shows network interfaces and IP addresses.

### Routes

```bash
ip route
```

Shows the container's routing table.

### DNS configuration

```bash
cat /etc/resolv.conf
```

Shows DNS configuration.

### Listening ports

```bash
ss -tulnp
```

Shows listening TCP/UDP sockets.

---

# 66. Understanding `ip route`

Run:

```bash
ip route
```

You may see something conceptually similar to:

```text
default via 172.17.0.1 dev eth0
172.17.0.0/16 dev eth0
```

This tells you that:

```text
Container
   │
   │ eth0
   ↓
Docker network
   │
   ↓
Gateway
```

The exact addresses depend on the Docker network configuration.

---

# 67. Understanding `ss -tulnp`

Run:

```bash
ss -tulnp
```

Breakdown:

```text
-s   socket statistics
-t   TCP
-u   UDP
-l   listening
-n   numeric addresses/ports
-p   process information
```

Example:

```text
LISTEN 0 128 0.0.0.0:5000
```

This tells you that a process is listening on port `5000`.

---

# 68. Network Troubleshooting Flow

When one container cannot communicate with another, check systematically.

```text
1. Are both containers running?
          ↓
2. Are they on the same network?
          ↓
3. Does Docker DNS resolve the container name?
          ↓
4. Is the target application actually listening?
          ↓
5. Is the application listening on the correct interface?
          ↓
6. Is the correct port being used?
```

Useful commands:

```bash
docker ps
```

```bash
docker network inspect mynet
```

```bash
docker exec -it container ping other-container
```

```bash
docker exec -it container getent hosts other-container
```

```bash
docker exec -it container ss -tulnp
```

---

# 69. Storage Troubleshooting Flow

When application data appears to disappear:

```text
1. Where was the data stored?
          ↓
2. Container writable layer?
          ↓
3. Named volume?
          ↓
4. Bind mount?
          ↓
5. Was the volume removed?
          ↓
6. Is the new container using the same mount?
```

Useful commands:

```bash
docker volume ls
```

```bash
docker volume inspect <volume>
```

```bash
docker inspect <container>
```

---

# 70. Network Isolation vs Storage Persistence

These concepts should not be mixed.

### Networking

Controls:

```text
communication
```

Example:

```text
frontend → backend
backend → database
```

### Storage

Controls:

```text
data persistence
```

Example:

```text
database → volume
```

So:

```text
Network = communication

Volume = persistence
```

---

# 71. Complete Networking Example

Create a network:

```bash
docker network create app-net
```

Run backend:

```bash
docker run -dit \
  --name backend \
  --network app-net \
  alpine sh
```

Run another container:

```bash
docker run -dit \
  --name client \
  --network app-net \
  alpine sh
```

Test DNS:

```bash
docker exec client ping -c 3 backend
```

Inspect:

```bash
docker network inspect app-net
```

The important relationship is:

```text
app-net
│
├── backend
│
└── client
```

---

# 72. Complete Volume Example

Create:

```bash
docker volume create app-data
```

Run:

```bash
docker run -dit \
  --name app1 \
  -v app-data:/data \
  alpine sh
```

Write:

```bash
docker exec app1 sh -c 'echo "persistent data" > /data/file.txt'
```

Remove container:

```bash
docker rm -f app1
```

Run a new container:

```bash
docker run -dit \
  --name app2 \
  -v app-data:/data \
  alpine sh
```

Read:

```bash
docker exec app2 cat /data/file.txt
```

Expected:

```text
persistent data
```

The important observation:

```text
app1
 │
 └── app-data
       │
       └── file.txt
       ↑
       │
app2
```

---

# 73. Complete Network + Volume Example

A simple architecture:

```text
                    app-net
                       │
             ┌─────────┴─────────┐
             │                   │
          backend              db
                                 │
                                 │ /var/lib/data
                                 ↓
                              db-data
                              (volume)
```

Here:

### Network

```text
app-net
```

allows:

```text
backend ↔ db
```

### Volume

```text
db-data
```

provides:

```text
persistent database storage
```

This is the fundamental pattern behind many containerized applications.

---

# 74. Cleanup Commands

Remove containers:

```bash
docker rm -f backend client
```

Remove network:

```bash
docker network rm app-net
```

Remove volume:

```bash
docker volume rm app-data
```

Remember:

```text
Removing a container
≠
Removing a named volume
```

The volume has its own lifecycle.

---

# 75. Important Docker Networking Vocabulary

| Term              | Meaning                                     |
| ----------------- | ------------------------------------------- |
| Network           | Logical Docker network                      |
| Network driver    | Technology/model used by the network        |
| Bridge            | Standard isolated Docker network            |
| Host              | Uses host networking                        |
| None              | No normal network connectivity              |
| Overlay           | Multi-host Docker networking                |
| Macvlan           | Direct Layer-2-style network integration    |
| IP address        | Address assigned to a network interface     |
| DNS               | Converts names into addresses               |
| Embedded DNS      | Docker's container-name resolution          |
| Port publishing   | Exposes container service through host port |
| Network isolation | Separates communication between containers  |

---

# 76. Important Docker Storage Vocabulary

| Term           | Meaning                                       |
| -------------- | --------------------------------------------- |
| Writable layer | Container-specific writable filesystem layer  |
| Volume         | Docker-managed persistent storage             |
| Named volume   | Volume identified by a user-defined name      |
| Bind mount     | Host directory/file mounted into container    |
| tmpfs          | Temporary memory-backed mount                 |
| Mount          | Makes storage available at a container path   |
| Persistence    | Data surviving container replacement/deletion |

---

# 77. Commands to Memorize

## Networking

```bash
docker network ls
docker network create mynet
docker network inspect mynet
docker network connect mynet <container>
docker network disconnect mynet <container>
docker network rm mynet
```

Run on network:

```bash
docker run --network mynet ...
```

Inspect container networking:

```bash
docker inspect <container>
```

Inside container:

```bash
ip a
ip route
ss -tulnp
cat /etc/resolv.conf
```

---

## Volumes

```bash
docker volume ls
docker volume create mydata
docker volume inspect mydata
docker volume rm mydata
docker volume prune
```

Use volume:

```bash
docker run -v mydata:/data ...
```

Explicit syntax:

```bash
docker run \
  --mount type=volume,source=mydata,target=/data \
  ...
```

Bind mount:

```bash
docker run \
  --mount type=bind,source=/host/path,target=/container/path \
  ...
```

tmpfs:

```bash
docker run \
  --tmpfs /tmp \
  ...
```

---

# 78. The Most Important Mental Models

## Network

```text
Container
    │
    ↓
Docker Network
    │
    ├── Container A
    ├── Container B
    └── Container C
```

Containers on the same suitable Docker network can communicate.

---

## DNS

```text
container name
      │
      ↓
Docker DNS
      │
      ↓
container IP
```

Therefore:

```text
backend:5000
```

is usually preferable to hardcoding:

```text
172.x.x.x:5000
```

inside a user-defined network.

---

## Port Publishing

```text
Host :8080
     │
     ↓
Container :3000
```

```bash
-p 8080:3000
```

means:

```text
HOST_PORT:CONTAINER_PORT
```

---

## Volume

```text
Container
    │
    ↓
Named Volume
    │
    ↓
Persistent Data
```

Container can be replaced:

```text
Container A
    ↓
deleted

Container B
    ↓
same volume
    ↓
same data
```

---

## Bind Mount

```text
Host Directory
      │
      ↓
Bind Mount
      │
      ↓
Container Directory
```

---

## tmpfs

```text
Container
    │
    ↓
tmpfs
    │
    ↓
RAM
```

---

# 79. Final Comparison

## Network Types

```text
bridge
│
└── Normal isolated container networking

host
│
└── Container uses host network

none
│
└── No normal networking

overlay
│
└── Multi-host Docker networking

macvlan
│
└── Direct physical-network style integration
```

## Storage Types

```text
Writable Layer
│
└── Container-specific temporary data

Volume
│
└── Docker-managed persistent data

Bind Mount
│
└── Host-controlled filesystem data

tmpfs
│
└── Temporary memory-backed data
```

---

# 80. Module 4 Learning Checklist

I should be able to explain:

### Docker Networking

* [ ] What a Docker network is
* [ ] What a network driver is
* [ ] What the default bridge network is
* [ ] What a user-defined bridge network is
* [ ] Why user-defined bridge networks are useful
* [ ] How containers communicate with each other
* [ ] How Docker DNS resolves container names
* [ ] What `127.0.0.11` represents
* [ ] Difference between container IP and host IP
* [ ] Difference between container networking and port publishing
* [ ] Why `-p` is not required for containers on the same network
* [ ] What `localhost` means inside a container
* [ ] Why applications commonly bind to `0.0.0.0` in containers
* [ ] What the `host` network does
* [ ] What the `none` network does
* [ ] What the `overlay` network is used for
* [ ] What the `macvlan` network is used for
* [ ] How to inspect a Docker network
* [ ] How to connect/disconnect containers from networks
* [ ] How to troubleshoot container networking

### Docker Storage

* [ ] What the container writable layer is
* [ ] Why important data should not live only in the writable layer
* [ ] What a Docker volume is
* [ ] What a named volume is
* [ ] How to create and inspect a volume
* [ ] How volume data survives container deletion
* [ ] How multiple containers can share a volume
* [ ] What a bind mount is
* [ ] Difference between a volume and a bind mount
* [ ] What `tmpfs` is
* [ ] When to use persistent storage
* [ ] How to mount storage using `-v`
* [ ] How to mount storage using `--mount`
* [ ] How to make a mount read-only
* [ ] How to inspect and remove volumes

---

# 81. Core Rules to Remember

### Rule 1

```text
Same Docker network
→ containers can communicate directly
```

### Rule 2

```text
User-defined bridge
→ Docker DNS can resolve container names
```

### Rule 3

```text
-p
→ publishes a container port through the host
```

### Rule 4

```text
Container-to-container communication
→ does not inherently require -p
```

### Rule 5

```text
127.0.0.1
→ this container
```

### Rule 6

```text
0.0.0.0
→ listen on all container interfaces
```

### Rule 7

```text
Volume
→ persistent Docker-managed storage
```

### Rule 8

```text
Bind mount
→ explicit host path mounted into container
```

### Rule 9

```text
tmpfs
→ temporary memory-backed storage
```

### Rule 10

```text
Container deletion
≠
Named volume deletion
```

---

# 82. One Final Mental Picture

Everything studied in this module can be reduced to:

```text
                         DOCKER
                            │
             ┌──────────────┴──────────────┐
             │                             │
         NETWORKING                     STORAGE
             │                             │
      ┌──────┼──────┐              ┌──────┼──────┐
      │      │      │              │      │      │
   bridge  host   none          volume  bind   tmpfs
      │
      ├── overlay
      │
      └── macvlan
      │
      ↓
 Container Communication
      │
      ├── Container IP
      ├── Docker DNS
      ├── Network isolation
      └── Port publishing


 Storage
    │
    ├── Persistent data
    ├── Shared data
    ├── Host files
    └── Temporary memory
```

The central idea of Module 4 is:

```text
NETWORKING
"How do containers communicate?"

STORAGE
"Where does container data live,
and does it survive the container?"
```

That is the core of Docker networking and storage.
