# Kubernetes Ingress --- Revision Notes

## 1. Ingress in one line

**Ingress** is a Kubernetes API resource that defines rules for routing
incoming HTTP/HTTPS requests to Services, commonly by hostname and URL
path.

> Ingress defines the rules; an **Ingress Controller** implements them
> and handles traffic.

## 2. Why Ingress exists

-   **ClusterIP:** exposes a Service internally within the cluster.
-   **NodePort:** exposes a Service through a port on cluster nodes.
-   **LoadBalancer:** requests an external load-balancing endpoint from
    a supported provider or implementation.
-   **Ingress:** routes HTTP/HTTPS requests to multiple Services through
    rules, often using one shared entry point.

Ingress does not replace Services and is not a universal solution for
arbitrary TCP/UDP traffic.

## 3. Important terms --- one-liners

  -----------------------------------------------------------------------
  Term                                One-line meaning
  ----------------------------------- -----------------------------------
  Client                              Browser, mobile app, or program
                                      making a request.

  DNS                                 Resolves a hostname such as
                                      `shop.example.com` to an IP
                                      address.

  Cloud load balancer                 Infrastructure component that
                                      receives and forwards traffic to
                                      configured targets.

  Kubernetes cluster                  Control-plane and worker-node
                                      components that manage and run
                                      workloads.

  Control plane                       Manages cluster state and makes
                                      orchestration decisions.

  API server                          Kubernetes API entry point used by
                                      `kubectl`, controllers, and other
                                      clients.

  etcd                                Key-value store holding Kubernetes
                                      cluster state.

  Scheduler                           Chooses a suitable node for a newly
                                      scheduled Pod.

  Controller manager                  Runs controllers that reconcile
                                      actual state toward desired state.

  Worker node                         Machine that runs Pods and
                                      node-level Kubernetes components.

  kubelet                             Node agent that ensures assigned
                                      Pods run as specified.

  Container runtime                   Software such as containerd that
                                      runs containers on a node.

  Pod                                 Smallest deployable Kubernetes
                                      unit, usually containing one
                                      application container or closely
                                      related containers.

  Application container               Runs the actual application
                                      process/code.

  Deployment                          Manages stateless application
                                      rollouts and desired replicas
                                      through ReplicaSets.

  ReplicaSet                          Keeps the desired number of
                                      matching Pod replicas running.

  Service                             Stable network endpoint for
                                      accessing a logical set of Pods or
                                      another configured destination.

  EndpointSlice                       Represents network endpoints
                                      associated with a Service.

  Ingress resource                    Stores HTTP/HTTPS routing rules in
                                      the Kubernetes API.

  Ingress Controller                  Software that watches
                                      Ingress-related resources and
                                      implements their routing behavior.

  IngressClass                        Identifies the controller class
                                      intended to handle an Ingress.

  Host-based routing                  Routes by hostname,
                                      e.g. `admin.example.com`.

  Path-based routing                  Routes by URL path, e.g. `/api`.

  TLS                                 Protocol used to secure
                                      connections; HTTPS is HTTP over
                                      TLS.

  TLS termination                     Point where the incoming TLS
                                      connection is decrypted, commonly
                                      at the Ingress Controller.

  TLS Secret                          Usually a Kubernetes Secret
                                      containing the certificate and
                                      private key referenced by an
                                      Ingress.

  Annotation                          Metadata often used for
                                      controller-specific configuration,
                                      such as rewrites.

  Path rewrite                        Changes the request path before
                                      forwarding, when supported and
                                      configured.

  Gateway API                         More expressive Kubernetes
                                      networking API family including
                                      GatewayClass, Gateway, and route
                                      resources.
  -----------------------------------------------------------------------

## 4. Complete end-to-end flow

Example request: `https://shop.example.com/api/products`

### Request path (data plane)

``` text
Client / Browser
      |
      | 1. Requests https://shop.example.com/api/products
      v
DNS
      |
      | 2. Resolves shop.example.com to the configured address
      v
Public entry point / Cloud Load Balancer / Node entry point
      |
      | 3. Forwards traffic toward the Ingress Controller
      v
Ingress Controller / Proxy
      |
      | 4. Handles TLS (if configured) and evaluates host + path
      v
Ingress rule: host=shop.example.com, path=/api
      |
      | 5. Selects backend-service:8080
      v
Kubernetes Service
      |
      | 6. Stable destination for usable backend endpoints
      v
EndpointSlice / backend endpoint
      |
      v
Backend Pod -> application container
      |
      | Response returns through the network path
      v
Client / Browser
```

The exact request path varies by controller and cluster. Some
controllers send traffic directly to backend Pod endpoints; others may
use the Service networking path. The control plane normally configures
and coordinates resources---it is not in the path of every application
request.

### Where the control plane fits

``` text
Developer / kubectl
        |
        v
Kubernetes API Server <----> etcd (cluster state)
        |
        +--> Deployment / ReplicaSet controllers reconcile replicas
        +--> Scheduler assigns new Pods to nodes
        +--> Ingress Controller watches resources
                    |
                    +--> Configures its proxy/data plane

Worker Node:
  kubelet + container runtime -> Pod(s) -> application container(s)
```

### Workload hierarchy

``` text
Deployment
   |
   v
ReplicaSet
   |
   +--> Pod 1 --> application container
   +--> Pod 2 --> application container
   +--> Pod 3 --> application container

Service -> stable endpoint for the selected Pod set
EndpointSlices -> represent current Service endpoints
```

-   Deployment manages ReplicaSets and rollouts.
-   ReplicaSet maintains the requested number of matching Pods.
-   Service selects matching Pods (typically by labels) and provides a
    stable destination.
-   EndpointSlices represent the Service's current endpoints.
-   Pods are scheduled onto worker nodes; the container runtime runs
    their containers.

## 5. Service types --- quick revision

  -----------------------------------------------------------------------
  Service type                        One-line meaning
  ----------------------------------- -----------------------------------
  `ClusterIP`                         Internal cluster IP by default;
                                      common for internal app-to-app
                                      traffic.

  `NodePort`                          Exposes a Service on a port on each
                                      node's address, subject to cluster
                                      networking.

  `LoadBalancer`                      Requests an external load balancer
                                      through a supported provider or
                                      implementation.

  `ExternalName`                      Maps a Service name to an external
                                      DNS name using a CNAME response; it
                                      does not proxy traffic or create
                                      normal Pod endpoints.
  -----------------------------------------------------------------------

## 6. Host and path routing

Example: - `shop.example.com/` → `frontend-service:80` -
`shop.example.com/api` → `backend-service:8080` - `admin.example.com/` →
`admin-service:80`

### Path types

-   **`Exact`:** matches the exact URL path.
-   **`Prefix`:** matches by path segments; `/api` matches `/api` and
    `/api/products`, but not `/apix`.
-   **`ImplementationSpecific`:** interpretation depends on the
    controller.

When multiple paths match, Kubernetes prefers the longest matching path;
for equal-length matches, `Exact` takes precedence over `Prefix`.

**Routing is not rewriting:** a `/api` rule does not automatically strip
`/api` from the request. Rewriting requires supported
controller-specific configuration.

## 7. Ingress YAML --- basic example

Assumptions: an appropriate controller and `IngressClass` exist; both
Services are in the same namespace as this Ingress; their Service ports
are 80 and 8080; DNS and network access are configured.

``` yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shopeasy-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: shop.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port:
                  number: 8080
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port:
                  number: 80
```

### YAML fields

-   `apiVersion`: API group/version.
-   `kind`: resource type (`Ingress`).
-   `metadata.name`: resource name.
-   `spec`: desired configuration.
-   `ingressClassName`: intended `IngressClass`; a matching controller
    must serve it.
-   `rules`: routing rules.
-   `host`: hostname to match.
-   `http.paths`: HTTP path rules.
-   `path`: path to match.
-   `pathType`: `Exact`, `Prefix`, or `ImplementationSpecific`.
-   `backend.service.name`: destination Service.
-   `backend.service.port.number`: destination **Service port**, not
    automatically the container port.

### Default backend

A fallback backend can be specified:

``` yaml
spec:
  defaultBackend:
    service:
      name: fallback-service
      port:
        number: 80
```

Without a configured default backend, unmatched-request behavior depends
on the controller and its configuration.

## 8. HTTPS / TLS

``` yaml
spec:
  tls:
    - hosts:
        - shop.example.com
      secretName: shopeasy-tls
```

-   HTTPS is HTTP over TLS.
-   The browser validates the certificate and hostname.
-   With TLS termination at the controller, the external connection is
    decrypted there; the internal backend connection may be HTTP unless
    separately encrypted.
-   `secretName` references a TLS Secret, normally in the same namespace
    as the Ingress.
-   The Secret normally contains a certificate and private key; it must
    exist and contain valid material.
-   An Ingress TLS section does not automatically issue a trusted
    certificate.

## 9. Controllers, classes, annotations

-   **Controller:** watches Kubernetes resources and implements routing
    using its proxy/infrastructure.
-   **IngressClass:** associates an Ingress with the intended controller
    class.
-   **Annotation:** optional metadata used by some controllers for extra
    features.
-   **NGINX-based controller:** one implementation; its annotations are
    not universal Kubernetes fields.
-   **Path rewrite:** transforms a path before forwarding when supported
    and configured.
-   **Load balancing:** requests can be distributed among backend
    endpoints; behavior depends on the controller and networking
    implementation.

Example controller-specific annotation (only for a compatible
controller):

``` yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
```

Do not copy controller-specific annotations blindly; check the
documentation for the controller installed in the cluster.

## 10. Common troubleshooting checks

  -----------------------------------------------------------------------
  Symptom                             What to check
  ----------------------------------- -----------------------------------
  No usable external address /        Controller, controller Service,
  connection fails                    entry point, local/cloud
                                      networking.

  Wrong app receives request          Host/path rules and path
                                      precedence.

  404                                 Rule mismatch, controller fallback,
                                      or missing application route.

  502/503                             Backend endpoints, Pod readiness,
                                      Service port, targetPort,
                                      controller logs.

  TLS warning                         Certificate hostname/trust chain,
                                      TLS Secret, controller
                                      configuration.

  Works by IP but not hostname        DNS and HTTP Host header.

  `/api/products` reaches app but     Whether backend expects
  fails                               `/api/products` or `/products`;
                                      inspect rewrite rules.
  -----------------------------------------------------------------------

Suggested investigation order: 1. Inspect Ingress and its events. 2.
Confirm `ingressClassName` and that a controller is running. 3. Verify
the entry point and DNS. 4. Confirm host/path matching. 5. Confirm
Service exists in the same namespace and the port is correct. 6. Check
EndpointSlices and backend Pod readiness. 7. Inspect controller logs. 8.
Check TLS Secret/certificate if HTTPS fails. 9. Test the application
route directly if possible.

## 11. Useful `kubectl` commands

``` bash
# Ingress resources
kubectl get ingress
kubectl get ingress -A
kubectl describe ingress shopeasy-ingress

# Ingress classes
kubectl get ingressclass

# Services and endpoints
kubectl get services
kubectl get endpointslices
kubectl get endpoints
kubectl describe service backend-service

# Deployments, ReplicaSets, Pods
kubectl get deployments
kubectl get replicasets
kubectl get pods -o wide
kubectl describe pod <pod-name>

# Discover controller resources (namespaces/names vary)
kubectl get pods -A
kubectl get deployments -A
kubectl get services -A

# Logs (replace placeholders)
kubectl logs <pod-name>
kubectl logs deployment/<controller-deployment-name> -n <controller-namespace>

# Apply/remove manifest
kubectl apply -f ingress.yaml
kubectl delete -f ingress.yaml

# Context and namespaces
kubectl config current-context
kubectl get namespaces
```

For local testing, a hostname may need to resolve to the local cluster's
entry point. Do not assume a public cloud load balancer or public DNS
exists automatically in Minikube.

## 12. Ingress vs Gateway API

-   **Ingress:** stable, widely used HTTP/HTTPS routing API; its API is
    frozen and is not planned to receive new features.
-   **Gateway API:** more expressive and extensible Kubernetes
    networking API family recommended for consideration in new designs.
-   **`GatewayClass`:** identifies a Gateway implementation class.
-   **`Gateway`:** describes a traffic entry point and its listeners.
-   **`HTTPRoute`:** describes HTTP routing rules associated with a
    Gateway.
-   Gateway API also requires a supporting implementation/controller.

## 13. Final mental model

``` text
CLIENT
  -> DNS resolves hostname
  -> public/local entry point (often a load balancer)
  -> Ingress Controller / proxy
  -> Ingress host + path rule
  -> Service
  -> EndpointSlice / backend endpoint
  -> Pod on a worker node
  -> application container
  -> response returns to client

CONTROL PLANE (coordinates; not normally in every request's data path)
  API Server + etcd + Scheduler + Controller Manager
  -> controllers reconcile Deployments, ReplicaSets, Services, and other resources
  -> Ingress Controller watches relevant resources and configures traffic handling

WORKLOAD MANAGEMENT
  Deployment -> ReplicaSet -> Pods -> application containers
  Service -> stable destination for matching Pods
  EndpointSlices -> represent current Service endpoints
```

**Remember:** Ingress is the routing-rule resource, the Ingress
Controller implements it, a Service provides a stable backend
destination, and a Deployment/ReplicaSet keeps application Pods running.
