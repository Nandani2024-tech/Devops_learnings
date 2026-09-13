# Docker Networking — Revision Notes

> **Source:** Docker Engine Networking Overview  
> https://docs.docker.com/engine/network/  
> **Purpose:** Quick revision + practical command reference

---

## 1. What is Docker Networking?

Docker networking allows containers to:

- communicate with other containers
- communicate with the Docker host
- communicate with services outside Docker
- access the Internet when networking is configured appropriately

A container sees a normal network environment containing things such as:

- network interface
- IP address
- gateway
- routing table
- DNS configuration

**Core idea:**

> A Docker container is isolated, but Docker gives it networking capabilities through Docker networks.

Containers have networking enabled by default.

---

# 2. Default `bridge` Network

On Linux, Docker Engine has a built-in network called:

```text
bridge
```

If you run:

```bash
docker run <image>
```

without specifying `--network`, the container is attached to the default `bridge` network.

Example:

```bash
docker run --rm -ti busybox ping -c1 docker.com
```

### Internet access

Containers on the default bridge can access services outside the Docker host.

Docker uses **masquerading** so that if the host has Internet access, the container can normally access the Internet without extra configuration.

---

# 3. Default Bridge vs User-Defined Network

This is one of the most important concepts.

## Default bridge

Containers connected to the default bridge can communicate using their **container IP addresses**.

However:

```text
container-name -> NOT automatically usable as DNS name
```

So the default bridge is less convenient for service-to-service communication.

## User-defined network

You can create your own network:

```bash
docker network create -d bridge my-net
```

Then run a container on it:

```bash
docker run --network=my-net -it busybox
```

Containers on the same user-defined network can communicate using:

- container IP addresses
- container names

### Easy mental model

```text
Default bridge
    ↓
IP-based communication

User-defined bridge
    ↓
IP + container-name communication
```

**Practical rule:** For applications with multiple containers, prefer a user-defined network.

---

# 4. Network Drivers

Docker provides different network drivers.

| Driver | Main purpose |
|---|---|
| `bridge` | Default networking for containers on a single Docker host |
| `host` | Removes network isolation between container and Docker host |
| `none` | Completely isolates the container from networking |
| `overlay` | Connects multiple Docker daemons / Swarm networks |
| `ipvlan` | Connects containers to external VLANs |
| `macvlan` | Makes containers appear like devices on the physical network |

## 4.1 Bridge

Most common for normal multi-container applications.

```bash
docker network create -d bridge my-net
```

## 4.2 Host

The container shares the host's network stack.

Conceptually:

```text
Container
   |
   +---- Host network
```

There is much less network isolation.

## 4.3 None

No normal network connectivity.

Useful when a container should be completely isolated.

## 4.4 Overlay

Used when networking needs to span multiple Docker daemons, especially Docker Swarm.

## 4.5 IPvlan

Connects containers to an external VLAN/network.

## 4.6 Macvlan

Makes containers appear as network devices on the external network.

---

# 5. Containers Can Join Multiple Networks

A container does not have to belong to only one Docker network.

Example architecture:

```text
                Internet
                   |
             [Frontend]
              /       \
       public bridge   internal network
                        |
                    [Backend]
                        |
                    [Database]
```

For example, a frontend container can connect to:

- a network with external access
- an internal network used for backend communication

A container can also use different network types simultaneously.

### Connect an existing container

```bash
docker network connect anet2 myctr
```

---

# 6. Default Gateway

When a container is attached to multiple networks, Docker chooses a default gateway.

The network with the highest `gw-priority` becomes the default gateway.

Default:

```text
gw-priority = 0
```

Example:

```bash
docker run \
  --network name=gwnet,gw-priority=1 \
  --network anet1 \
  --name myctr \
  myimage
```

Here `gwnet` gets priority `1`, so it becomes the preferred default gateway.

### Remember

```text
Higher gw-priority
        ↓
Preferred default gateway
```

---

# 7. Published Ports

A container port is not automatically exposed to the outside world.

For example:

```bash
docker run nginx
```

The application may listen on port `80` inside the container.

But external clients cannot automatically access:

```text
host-ip:80
```

To publish the port:

```bash
docker run -p 8080:80 nginx
```

Meaning:

```text
Host port 8080
      ↓
Container port 80
```

So:

```text
localhost:8080
       |
       v
container:80
```

### Important distinction

`EXPOSE` and `-p` are not the same thing.

- `EXPOSE` documents / declares the intended container port.
- `-p` / `--publish` creates a port mapping that makes the port available outside the host and, depending on networking, to other networks.

### Source concept

For bridge networks, container ports are accessible from the Docker host and other containers on the same network. Publishing is used to make them available outside the host or to containers on other bridge networks.

---

# 8. IP Addresses

Docker normally gives a container an IP address for every Docker network it joins.

Example:

```text
Network: app-net
Subnet: 172.x.x.0/24

Container:
IP = 172.x.x.2
Gateway = 172.x.x.1
```

The container receives its IP from the network's subnet.

Docker performs dynamic IP allocation.

---

# 9. IPv4 and IPv6

IPv4 is enabled by default when creating a network.

You can disable IPv4:

```bash
docker network create --ipv4=false mynet
```

You can enable IPv6:

```bash
docker network create --ipv6 mynet
```

Example:

```bash
docker network create \
  --ipv6 \
  --ipv4=false \
  v6net
```

This creates an IPv6-only network.

---

# 10. Connecting a Running Container

You can connect an already-running container to another network:

```bash
docker network connect my-network my-container
```

A container can therefore have multiple network interfaces/IP addresses.

You can also specify an IP:

```bash
docker network connect --ip 172.20.0.10 my-network my-container
```

For IPv6:

```bash
docker network connect --ip6 <IPv6-address> my-network my-container
```

You can also assign a network alias:

```bash
docker network connect --alias backend my-network my-container
```

---

# 11. Hostname

By default, a container's hostname is its container ID.

You can change it:

```bash
docker run --hostname myhost <image>
```

Conceptually:

```text
Container ID
     ↓
Default hostname

--hostname myhost
     ↓
Custom hostname
```

---

# 12. Subnets

A Docker network has a subnet.

Example:

```text
Subnet:
172.19.0.0/24

Gateway:
172.19.0.1
```

You can explicitly choose the subnet:

```bash
docker network create \
  --subnet 192.0.2.0/24 \
  mynet
```

For IPv6:

```bash
docker network create \
  --ipv6 \
  --subnet 2001:db8::/64 \
  mynet
```

---

# 13. Automatic Subnet Allocation

If you do not specify `--subnet`, Docker automatically selects a subnet from its configured default address pools.

Concept:

```text
Docker address pool
       |
       +---- Network 1
       |
       +---- Network 2
       |
       +---- Network 3
```

Docker attempts to avoid prefixes already in use on the host.

### Why should you care?

Subnet conflicts can cause routing problems.

For example:

```text
Docker network:
192.168.1.0/24

Physical LAN:
192.168.1.0/24
```

This can create routing conflicts.

---

# 14. Default Address Pools

Docker's built-in default pools include ranges such as:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/14
172.24.0.0/14
172.28.0.0/14
192.168.0.0/16
```

These are used when Docker automatically allocates network subnets.

The address pools can be customized in:

```text
/etc/docker/daemon.json
```

Example:

```json
{
  "default-address-pools": [
    {
      "base": "172.17.0.0/16",
      "size": 24
    }
  ]
}
```

This allows Docker to divide:

```text
172.17.0.0/16
```

into smaller `/24` networks.

That means:

```text
172.17.0.0/24
172.17.1.0/24
172.17.2.0/24
...
172.17.255.0/24
```

So one `/16` base can provide **256 `/24` networks**.

---

# 15. DNS in Docker

DNS is extremely important for multi-container applications.

Containers use DNS to resolve names such as:

```text
backend
database
redis
```

On a custom Docker network, Docker provides an embedded DNS server.

Its IPv4 address is:

```text
127.0.0.11
```

The embedded DNS server forwards external DNS queries to the DNS servers configured on the host.

### Key difference

Default bridge:

```text
Container
   ↓
inherits /etc/resolv.conf configuration
```

Custom network:

```text
Container
   ↓
Docker embedded DNS
   ↓
127.0.0.11
   ↓
Host DNS / upstream DNS
```

### Very important revision point

On a user-defined network, containers can resolve each other by container/service name.

Example:

```text
backend container
database container

backend → database
```

The application can use:

```text
database:5432
```

instead of trying to hard-code the database IP.

---

# 16. DNS Configuration Options

You can configure DNS when starting a container.

## `--dns`

Specify a DNS server:

```bash
docker run --dns 8.8.8.8 <image>
```

Multiple DNS servers can be provided using multiple `--dns` flags.

## `--dns-search`

Specifies DNS search domains.

## `--dns-opt`

Specifies DNS resolver options.

Example structure:

```bash
docker run \
  --dns <dns-server> \
  --dns-search <search-domain> \
  --dns-opt <option> \
  <image>
```

---

# 17. `/etc/hosts`

A container has its own `/etc/hosts`.

It contains entries for things such as:

```text
localhost
container hostname
```

Host-machine `/etc/hosts` entries are **not automatically inherited** by containers.

If additional host entries are required, configure them explicitly when starting the container.

---

# 18. Container Network Mode

A container can directly use another container's networking stack.

Syntax:

```bash
--network container:<name-or-id>
```

Example:

```bash
docker run -d \
  --name redis \
  redis \
  --bind 127.0.0.1
```

Then another container can share Redis's network stack:

```bash
docker run --rm -it \
  --network container:redis \
  redis \
  redis-cli -h 127.0.0.1
```

The important idea is:

```text
Container A
   |
   | shared network namespace
   |
Container B
```

Both containers see the same network stack.

Therefore `127.0.0.1` can refer to the same network namespace.

---

# 19. Restrictions of `container:` Network Mode

When using:

```bash
--network container:<name|id>
```

these options are not supported for the second container:

```text
--add-host
--hostname
--dns
--dns-search
--dns-option
--mac-address
--publish
--publish-all
--expose
```

Why?

Because the container is sharing another container's network stack instead of creating its own independent network configuration.

---

# 20. Important Docker Networking Commands

## List networks

```bash
docker network ls
```

## Create a network

```bash
docker network create my-network
```

## Create a bridge network

```bash
docker network create -d bridge my-network
```

## Inspect a network

```bash
docker network inspect my-network
```

## Connect container to network

```bash
docker network connect my-network my-container
```

## Disconnect container

```bash
docker network disconnect my-network my-container
```

## Remove network

```bash
docker network rm my-network
```

---

# 21. Typical Multi-Container Application

A common architecture looks like:

```text
                  Internet
                     |
                 Host :8080
                     |
                [Frontend]
                     |
                app-network
                     |
                 [Backend]
                     |
                app-network
                     |
                 [Database]
```

For example:

```bash
docker network create app-network
```

Run backend:

```bash
docker run -d \
  --name backend \
  --network app-network \
  backend-image
```

Run database:

```bash
docker run -d \
  --name database \
  --network app-network \
  postgres
```

The backend can communicate with the database using:

```text
database:<port>
```

rather than using a hard-coded IP.

This is one of the biggest practical benefits of user-defined Docker networks.

---

# 22. Common Confusions

## Confusion 1: Container port vs host port

```bash
-p 8080:80
```

means:

```text
HOST:8080 → CONTAINER:80
```

Not the other way around.

---

## Confusion 2: `EXPOSE` vs `-p`

```dockerfile
EXPOSE 80
```

does not mean:

```text
Host port 80 is automatically open
```

Publishing is done with:

```bash
-p 8080:80
```

---

## Confusion 3: Default bridge vs custom bridge

Default bridge:

```text
IP communication
```

User-defined bridge:

```text
IP + DNS/name-based communication
```

---

## Confusion 4: Container IPs are not stable service identities

Avoid designing applications around hard-coded container IPs.

Prefer:

```text
database
backend
redis
```

as names on a user-defined network.

---

## Confusion 5: `127.0.0.1` inside a container

Inside a normal container:

```text
127.0.0.1
```

means:

```text
this container itself
```

It does **not** normally mean the host or another container.

Exception:

With:

```bash
--network container:<other-container>
```

the containers share the same network namespace, so `127.0.0.1` can reach services in that shared namespace.

---

# 23. Quick Revision Table

| Concept | Remember |
|---|---|
| Default network | `bridge` |
| Default network flag | No `--network` specified |
| Custom network | `docker network create` |
| Recommended multi-container communication | User-defined network |
| Name-based communication | Available on user-defined networks |
| Common driver | `bridge` |
| Multi-host/Swarm | `overlay` |
| No networking | `none` |
| Host network isolation removed | `host` |
| Publish port | `-p HOST:CONTAINER` |
| Container IP | Allocated from network subnet |
| Custom subnet | `--subnet` |
| Enable IPv6 | `--ipv6` |
| Disable IPv4 | `--ipv4=false` |
| Docker embedded DNS | `127.0.0.11` |
| Connect running container | `docker network connect` |
| Inspect network | `docker network inspect` |
| Shared network stack | `--network container:<name/id>` |
| Custom hostname | `--hostname` |

---

# 24. Must-Know Commands

### Create network

```bash
docker network create mynet
```

### Create bridge network

```bash
docker network create -d bridge mynet
```

### Run container on network

```bash
docker run --network=mynet myimage
```

### Connect existing container

```bash
docker network connect mynet mycontainer
```

### Inspect

```bash
docker network inspect mynet
```

### Publish port

```bash
docker run -p 8080:80 myimage
```

### Create custom subnet

```bash
docker network create \
  --subnet 172.20.0.0/24 \
  mynet
```

### Enable IPv6

```bash
docker network create \
  --ipv6 \
  mynet
```

---

# 25. One-Minute Mental Model

Think of Docker networking like physical networking:

```text
Docker Network
      |
      +---- Container A
      |
      +---- Container B
      |
      +---- Container C
```

A network gives containers:

```text
IP
Gateway
Routing
DNS
Connectivity
```

A container can connect to multiple networks:

```text
             Network A
                |
             Container
                |
             Network B
```

For application design:

```text
Internet
   ↓
Published Port
   ↓
Frontend
   ↓
User-defined Docker Network
   ↓
Backend
   ↓
User-defined Docker Network
   ↓
Database
```

The key pattern is:

> **Publish only what needs external access; use private/user-defined networks for internal service-to-service communication.**

---

# 26. Exam / Viva Questions

### Q1. What is Docker networking?

Docker networking provides communication between containers, the Docker host, and external services.

### Q2. What network does a container use by default?

On Linux, a container started without `--network` is connected to Docker's default `bridge` network.

### Q3. Why use a user-defined bridge network?

Because containers on it can communicate using container names through Docker's embedded DNS, making multi-container applications easier to configure.

### Q4. What does `-p 8080:80` mean?

It maps:

```text
host port 8080 → container port 80
```

### Q5. What is Docker's embedded DNS address?

```text
127.0.0.11
```

### Q6. Can one container belong to multiple networks?

Yes.

### Q7. What does `--network container:redis` do?

It makes the new container share the Redis container's network stack.

### Q8. What is the purpose of `--subnet`?

It allows you to explicitly define the IP subnet used by a Docker network.

### Q9. What is `overlay` used for?

Connecting networks across multiple Docker daemons, particularly in Docker Swarm environments.

### Q10. What is the difference between `host` and `none`?

```text
host → removes network isolation with host
none → completely isolates networking
```

---

# 27. Final Revision Checklist

Before considering Docker networking understood, make sure you can explain:

- [ ] What Docker networking is
- [ ] Default `bridge` network
- [ ] User-defined networks
- [ ] Why container names work on custom networks
- [ ] Network drivers
- [ ] `bridge`, `host`, `none`, `overlay`, `ipvlan`, `macvlan`
- [ ] Multiple networks per container
- [ ] Default gateway and `gw-priority`
- [ ] Port publishing
- [ ] Host port vs container port
- [ ] Container IP addresses
- [ ] IPv4 and IPv6
- [ ] Docker subnets
- [ ] Default address pools
- [ ] Docker embedded DNS
- [ ] `127.0.0.11`
- [ ] `/etc/hosts`
- [ ] `--network container:<name/id>`
- [ ] `docker network ls`
- [ ] `docker network create`
- [ ] `docker network inspect`
- [ ] `docker network connect`
- [ ] `docker network disconnect`
- [ ] `docker network rm`

---

## The 5 Things to Remember Most

1. **Containers are network-enabled by default.**
2. **Default `bridge` is different from a user-defined bridge.**
3. **User-defined networks provide convenient container-name/DNS communication.**
4. **`-p HOST:CONTAINER` publishes a container port externally.**
5. **For multi-container applications, use networks to control which services can communicate.**
