# Kubernetes Services — Theory Notes

> Scope: Today's Services theory. Crisp definitions, important code, and connections to the Docker + Kubernetes topics already studied.

## 1. Why Do We Need a Service?

Pods are temporary. A Deployment can replace a Pod, and the replacement can have a different IP.

```text
Deployment
    ↓
Pods
    ↓
Pod IPs can change
```

A Service gives a **stable network endpoint** for a changing group of Pods.

```text
Client
   ↓
Service
   ↓
Pod A / Pod B / Pod C
```

**One-liner:** Service = stable access point for one or more changing Pods.

---

## 2. Connection With Docker Networking

You already learned:

```text
Container
    ↓
Docker Network
    ↓
Docker DNS
    ↓
Container name
```

Kubernetes follows the same basic idea:

```text
Pod
 ↓
Service
 ↓
Kubernetes DNS
 ↓
Backend Pods
```

Docker taught us not to depend unnecessarily on changing container IPs. Kubernetes applies the same idea to changing Pod IPs.

---

## 3. Pod Networking

Each Pod gets its own cluster-wide IP. Pods can communicate through the cluster network.

```text
Pod A
  ↕
Pod B
```

But Pod IPs are not the stable endpoint applications should normally use.

---

## 4. Service

A Service is a Kubernetes object that provides a **stable IP/hostname** for accessing one or more backend Pods.

```text
Service
   ↓
Pod A
Pod B
Pod C
```

**One-liner:** Service = stable networking abstraction in front of changing Pods.

---

## 5. Service + Deployment

Deployment and Service solve different problems.

```text
Deployment
    ↓
manages Pods
    ↓
replicas
self-healing
updates
rollback

Service
    ↓
connects clients to Pods
    ↓
stable endpoint
service discovery
traffic routing
```

**Mental model:**

> Deployment manages the application. Service connects clients to the application.

---

## 6. Labels and Selectors

This connects directly to labels/selectors already studied.

Pod:

```yaml
metadata:
  labels:
    app: task-manager-backend
```

Service:

```yaml
selector:
  app: task-manager-backend
```

Meaning:

```text
Service
   ↓
find Pods with:
app=task-manager-backend
```

The selector determines which Pods become Service backends.

---

## 7. Basic Service YAML

For your FastAPI backend:

```yaml
apiVersion: v1
kind: Service

metadata:
  name: backend

spec:
  selector:
    app: task-manager-backend

  ports:
    - port: 80
      targetPort: 8000

  type: ClusterIP
```

Meaning:

```text
Service name → backend
Selector     → matching Pods
Service port → 80
Pod port     → 8000
Type         → ClusterIP
```

---

## 8. `port` vs `targetPort`

```yaml
ports:
  - port: 80
    targetPort: 8000
```

Means:

```text
Client
  ↓
Service :80
  ↓
Pod :8000
```

- `port` → Service port
- `targetPort` → Pod/application port

**Memory trick:**

```text
port       → Service
targetPort → Pod
```

---

## 9. ClusterIP

`ClusterIP` is the default Service type.

It provides an internal stable endpoint.

```text
Frontend Pod
     ↓
Backend Service
     ↓
Backend Pods
```

**One-liner:** ClusterIP = internal stable access to a group of Pods.

---

## 10. Kubernetes DNS

Kubernetes creates DNS records for Services.

Instead of using a changing Pod IP:

```text
10.x.x.x
```

a workload can use the Service name:

```text
http://backend:80
```

Conceptually:

```text
backend
   ↓
Kubernetes DNS
   ↓
Service IP
   ↓
Backend Pods
```

This is **Service Discovery**.

---

## 11. Service Discovery

Service Discovery means:

> Finding a service by a stable name instead of knowing the changing IP addresses of its Pods.

Example:

```text
Frontend
   ↓
http://backend
   ↓
Backend Service
   ↓
Backend Pods
```

---

## 12. EndpointSlices

EndpointSlices are the piece between a Service and its backend endpoints.

Think:

```text
Service
   ↓
EndpointSlices
   ↓
Pod IPs / endpoints
```

Suppose the Service selects:

```text
Pod A → 10.0.0.10
Pod B → 10.0.0.11
Pod C → 10.0.0.12
```

Kubernetes maintains EndpointSlice objects containing these backend endpoints.

```text
Service: backend
       ↓
EndpointSlice
 ┌─────┼─────┐
 ↓     ↓     ↓
 A     B     C
```

If Pod B disappears:

```text
Old: A B C
New: A C D
```

Kubernetes updates the EndpointSlices.

**One-liner:** EndpointSlice = Kubernetes-managed list of network endpoints currently backing a Service.

For normal selector-based Services, the control plane creates and updates EndpointSlices automatically.

EndpointSlices are stable in Kubernetes and are the modern replacement for the older Endpoints API.

---

## 13. Why EndpointSlices Exist

For a Service with many backend Pods, Kubernetes can divide endpoints into multiple slices.

```text
Service
   │
   ├── EndpointSlice 1
   │      ├── Pod A
   │      ├── Pod B
   │      └── Pod C
   │
   ├── EndpointSlice 2
   │      ├── Pod D
   │      ├── Pod E
   │      └── Pod F
   │
   └── EndpointSlice 3
```

This makes endpoint updates and large-scale Services more efficient.

**For now remember only:**

```text
Service
   ↓
EndpointSlices
   ↓
Backend endpoints
```

---

## 14. Service Traffic Flow

For your Task Manager:

```text
Frontend
   │
   │ request
   ↓
Backend Service
   │
   ├───────────────┐
   ↓               ↓
Backend Pod A   Backend Pod B
   │               │
   └───────┬───────┘
           ↓
       FastAPI :8000
```

The Service hides changing Pod IPs from the client.

---

## 15. NodePort

NodePort exposes a Service through a port on the Kubernetes nodes.

```text
Browser
   ↓
NodeIP:NodePort
   ↓
Service
   ↓
Backend Pods
```

**One-liner:** NodePort = access a Service through a port on the Kubernetes nodes.

It also includes ClusterIP behavior.

---

## 16. LoadBalancer

LoadBalancer exposes a Service using an external load balancer when the environment supports it.

```text
Internet
   ↓
External Load Balancer
   ↓
Service
   ↓
Pods
```

**One-liner:** LoadBalancer = expose a Service through an external load balancer.

In cloud environments, the cloud provider can provision/manage the external load balancer.

---

## 17. Service Types — Quick Comparison

| Type | Main purpose |
|---|---|
| `ClusterIP` | Internal cluster access |
| `NodePort` | Access through a node port |
| `LoadBalancer` | External load balancer |
| `ExternalName` | DNS alias to an external name |

For current learning:

```text
ClusterIP → learn first
NodePort → learn next
LoadBalancer → understand now, use seriously with cloud later
```

---

## 18. Service Does NOT Create Pods

Important distinction:

```text
Deployment
    ↓
creates/manages Pods

Service
    ↓
finds/routes traffic to Pods
```

A Service is not a workload controller.

---

## 19. What Happens When a Pod Dies?

Suppose:

```text
Service
  ↓
Pod A
Pod B
Pod C
```

Pod B dies.

Deployment/ReplicaSet creates a replacement:

```text
Service
  ↓
Pod A
Pod C
Pod D
```

The client still uses:

```text
backend
```

It does not need to know about Pod B or Pod D.

---

## 20. Selector Mistake — Important Troubleshooting Case

Pods:

```yaml
labels:
  app: task-manager-backend
```

Service:

```yaml
selector:
  app: backend
```

They do not match.

```text
Service
   ↓
selector
   ↓
❌ no matching Pods
```

The Service can exist but have no useful backend endpoints.

This is why **labels + selectors + Services** are an important combination.

---

## 21. EndpointSlices and Readiness

EndpointSlices can contain endpoint conditions such as:

```text
ready
serving
terminating
```

For normal application behavior:

```text
Ready backend
    ↓
eligible for Service traffic
```

This becomes especially important later when studying **Readiness Probes** and rolling updates.

You do not need deep EndpointSlice-condition study yet.

---

## 22. Important Commands

View Services:

```bash
kubectl get services
kubectl get svc
```

Detailed Service information:

```bash
kubectl describe service <service-name>
```

View EndpointSlices:

```bash
kubectl get endpointslices
```

Detailed EndpointSlice information:

```bash
kubectl describe endpointslice <name>
```

View Pods and labels:

```bash
kubectl get pods --show-labels
```

Useful for troubleshooting Service selectors.

---

## 23. Docker vs Kubernetes Networking

### Docker

```text
Container
   ↓
Docker Network
   ↓
Docker DNS
   ↓
Container name
```

### Kubernetes

```text
Pod
   ↓
Service
   ↓
EndpointSlices
   ↓
Pod endpoints
```

### Key difference

Docker Compose gave you a stable service name.

Kubernetes gives you a richer abstraction:

```text
Service
  ↓
stable name/IP
  ↓
dynamic set of Pods
```

---

# 24. What We Have Studied So Far

## Docker

```text
Docker
│
├── Containers
├── Images
├── Dockerfiles
├── Multi-stage builds
├── Container lifecycle
├── Docker networking
│   ├── bridge
│   ├── host
│   ├── none
│   ├── overlay
│   ├── macvlan
│   ├── DNS
│   ├── container IP
│   └── port publishing
├── Docker storage
│   ├── writable layer
│   ├── volumes
│   ├── bind mounts
│   └── tmpfs
└── Docker Compose
    ├── services
    ├── service DNS
    ├── depends_on
    ├── healthchecks
    ├── volumes
    └── multi-container application
```

---

# 25. Kubernetes — Current Progress

```text
Kubernetes
│
├── Architecture
│   ├── Control Plane
│   ├── API Server
│   ├── etcd
│   ├── Scheduler
│   ├── Controller Manager
│   └── Worker Node
│
├── kubectl
├── YAML / Declarative configuration
├── Desired vs Actual State
│
├── Pod
│   ├── lifecycle
│   ├── logs
│   ├── exec
│   └── port-forward
│
├── Labels & Selectors
│
├── ReplicaSet
│   └── self-healing
│
├── Deployment
│   ├── replicas
│   ├── scaling
│   ├── rolling updates
│   ├── rollout history
│   ├── rollback
│   ├── Recreate
│   ├── RollingUpdate
│   ├── Blue-Green concept
│   └── Canary concept
│
└── Services ← CURRENT TOPIC
    ├── Pod networking
    ├── Service abstraction
    ├── selectors
    ├── ClusterIP
    ├── port / targetPort
    ├── DNS
    ├── Service Discovery
    ├── EndpointSlices
    ├── NodePort
    └── LoadBalancer
```

---

# 26. Complete Kubernetes Request Path — Current Stage

```text
Client
   │
   ↓
Service
   │
   ↓
EndpointSlices
   │
   ↓
Backend Pod
   │
   ↓
Container
   │
   ↓
Application
```

Workload-management side:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pods
    ↓
Containers
    ↓
Application
```

Together:

```text
                 Service
                    │
                    ↓
              EndpointSlices
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
      Pod A       Pod B       Pod C
        ↑           ↑           ↑
        └───────────┼───────────┘
                    │
               Deployment
                    ↓
                ReplicaSet
```

---

# 27. What Comes Next?

Based on the learning sequence in the provided material:

```text
Services
   ↓
Ingress
   ↓
ConfigMaps
   ↓
Secrets
   ↓
Storage
   ↓
Probes
   ↓
HPA
   ↓
Troubleshooting
```

The next major topic after Services is **Ingress**.

---

# 28. When Does Cloud Come?

Not immediately.

The planned progression is:

```text
Docker
   ↓
Kubernetes fundamentals
   ↓
Services
   ↓
Ingress
   ↓
ConfigMaps / Secrets
   ↓
Storage
   ↓
Probes / Resources
   ↓
HPA
   ↓
Troubleshooting
   ↓
Helm
   ↓
CI/CD
   ↓
DevSecOps
   ↓
Terraform / IaC
   ↓
Cloud + Terraform
   ↓
Cloud Kubernetes
   ├── EKS
   ├── GKE
   └── AKS
   ↓
Monitoring / Observability / GitOps
```

### Why cloud comes later

First learn:

> **How Kubernetes works.**

Then learn:

> **How Kubernetes is operated on cloud infrastructure.**

For example:

```text
AWS
 ↓
EKS
 ↓
Kubernetes
 ↓
Service
 ↓
AWS Load Balancer
 ↓
Internet
```

So **do not jump to AWS/EKS yet**. Build the Kubernetes networking foundation first.

---

# 29. Final Service Mental Model

Remember:

```text
Pod IP
  ↓
can change

Service
  ↓
stable IP + stable DNS name

Service
  ↓
selector
  ↓
EndpointSlices
  ↓
current backend Pods
```

And:

```text
Deployment
  → manages Pods

Service
  → connects clients to Pods

EndpointSlice
  → records the current backend endpoints
```

**Next hands-on:** Use the Task Manager backend to see the real:

```text
Selector
   ↓
EndpointSlice
   ↓
Service
   ↓
Pod
```
