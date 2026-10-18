# Subnetting Cheat Sheet & Reference Guide

---

## 1. Core Principles
* **Structure:** 32 bits total = 4 octets (8 bits each).
* **Components:**
  * **Network Part:** Identifies the subnet (neighborhood).
  * **Host Part:** Identifies the specific device (house address).
* **Subnet Mask / CIDR (`/X`):** Indicates how many bits from the left belong to the network.

---

## 2. Magic Number Rule (Fast Block Size Calculation)
1. **Identify the "Interesting Octet":** The octet where the mask is neither `255` (fully locked) nor `0` (fully open).
2. **Calculate Block Size:**
   $$\text{Block Size} = 256 - (\text{Value in Interesting Octet})$$
3. **Find Subnet Multiples:** Count by the block size in that specific octet starting from `0`.

---

## 3. Worked Example: `172.16.88.200 /22`

### Step 1: Subnet Mask & Block Size
* **CIDR:** `/22` -> First 22 bits = `1s`, remaining 10 bits = `0s`.
* **Subnet Mask:** `255.255.252.0`
* **Interesting Octet:** 3rd octet (`252`).
* **Block Size:** $256 - 252 = 4$ (subnets increment by 4 in the 3rd octet).

### Step 2: Network & Broadcast Addresses
* **Subnet Multiples (3rd Octet):** `0, 4, 8, ..., 84, 88, 92`
* **Network ID:** `172.16.88.0` *(88 is an exact multiple of 4; 4th octet resets to 0)*
* **Next Subnet Starts At:** `172.16.92.0`
* **Broadcast Address:** `172.16.91.255` *(1 address below `172.16.92.0`)*

### Step 3: Address Range Summary
| Component | Value | Formula / Notes |
| :--- | :--- | :--- |
| **Subnet Mask** | `255.255.252.0` | `/22` CIDR |
| **Network Address** | `172.16.88.0` | First ID |
| **First Usable Host** | `172.16.88.1` | Network ID + 1 |
| **Last Usable Host** | `172.16.91.254` | Broadcast ID - 1 |
| **Broadcast Address** | `172.16.91.255` | Last ID |
| **Total Host IPs** | $1024$ | $2^{10}$ host bits |
| **Usable Host IPs** | $1022$ | $2^{10} - 2$ |

---

## 4. RFC 1918 Private IP Address Ranges

| Class | IP Range | Default CIDR | Total Addresses |
| :--- | :--- | :--- | :--- |
| **Class A** | `10.0.0.0` – `10.255.255.255` | `/8` | 16,777,216 |
| **Class B** | `172.16.0.0` – `172.31.255.255` | `/12` | 1,048,576 |
| **Class C** | `192.168.0.0` – `192.168.255.255` | `/16` | 65,536 |

> **Note:** Private IPs are unroutable on the public internet and require **NAT (Network Address Translation)** to access external resources.




# Networking Fundamentals: One-Liners

## IP Address
- An IP address is a unique logical identifier for a device on a network; IPv4 is 32-bit (four octets, 0-255), IPv6 is 128-bit.
- CIDR notation `/n` means the first n bits are the network part; usable hosts per subnet = 2^(32-n) - 2.
- Network address = IP AND subnet mask; the first address of a subnet is the network ID, the last is broadcast.

## Public vs Private IP
- Public IPs are globally routable on the internet; private IPs are only valid inside a local network.
- Private ranges (RFC 1918): `10.0.0.0/8`, `172.16.0.0-172.31.255.255`, `192.168.0.0/16`.
- NAT/PAT lets many private-IP hosts share one public IP by rewriting source IP:port and tracking it in a translation table.

## Ports
- A port is a 16-bit number (0-65535) that identifies a specific process/service on a host; socket = IP + port.
- Well-known: 0-1023, registered: 1024-49151, ephemeral: 49152-65535.
- Common ports: HTTP 80, HTTPS 443, SSH 22, FTP 21, DNS 53, SMTP 25, MySQL 3306.

## TCP vs UDP
- TCP is connection-oriented, reliable, ordered, with flow and congestion control (slower, heavier).
- UDP is connectionless, unreliable, no ordering, minimal overhead (faster; used for DNS, streaming, gaming).
- TCP 3-way handshake: SYN -> SYN-ACK -> ACK; SYN consumes one sequence number (ACK = seq + 1).
- Header sizes: TCP min 20 bytes, UDP 8 bytes.

## DNS
- DNS translates domain names to IP addresses; it is a distributed, hierarchical database (root -> TLD -> authoritative).
- Resolution flow: browser/OS cache -> recursive resolver -> root -> TLD -> authoritative server.
- Records: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (name server), TXT (text/verification).
- TTL defines how long a record may be cached before the resolver must re-fetch it; DNS uses port 53 (UDP mostly, TCP for large responses/zone transfers).

## HTTP / HTTPS
- HTTP is a stateless, request-response, application-layer protocol over TCP (port 80).
- HTTPS = HTTP over TLS (port 443): provides encryption, integrity, and server authentication via certificates.
- Methods: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove); GET/PUT/DELETE are idempotent.
- Status codes: 2xx success, 3xx redirect (301 permanent, 302 temporary), 4xx client error (404 not found, 401 unauthorized, 403 forbidden), 5xx server error (500, 502, 503).
- Non-persistent HTTP costs 2 RTT per object (handshake + request); persistent connections reuse the TCP connection.

## Basic Networking Commands
- `ping <host>`: tests reachability and latency using ICMP echo.
- `traceroute <host>` / `tracert` (Windows): shows each hop by exploiting TTL expiry.
- `nslookup <domain>` / `dig <domain>`: queries DNS records.
- `ip a` / `ifconfig` / `ipconfig`: shows interface IP configuration.
- `ip route` / `route`: shows the routing table and default gateway.
- `ss -tulpn` / `netstat -tulpn`: lists listening ports and owning processes.
- `curl -I <url>`: fetches HTTP response headers; `curl`/`wget` download over HTTP(S).
- `nc -zv <host> <port>` / `telnet`: tests if a specific TCP port is open.
- `arp -a`: shows IP-to-MAC mappings on the local network.