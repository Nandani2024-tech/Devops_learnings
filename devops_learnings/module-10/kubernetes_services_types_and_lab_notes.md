# Kubernetes Services — Types, Purpose, and Hands-on Results

> Based on the uploaded Task Manager Services lab output. Environment: Windows + Git Bash + Minikube Docker driver; kubectl client v1.36.1.

## 1. Why do we need a Service?

A **Pod is temporary**. When it is deleted and replaced, its IP can change. A **Service** provides a stable network endpoint for a set of Pods selected by labels, so clients do not need to track individual Pod IPs.

```text
Client
  ↓
backend-service (stable name / ClusterIP)
  ↓
EndpointSlice (current eligible endpoints)
  ├── Pod 1:8000
  ├── Pod 2:8000
  └── Pod 3:8000
```

**One-liner:** A Service provides a stable way to reach the changing set of Pods behind an application.

## 2. Our application Service

File: `k8s/backend-service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: task-manager-backend
  ports:
    - port: 80
      targetPort: 8000
      protocol: TCP
```

| Field | Meaning |
|---|---|
| `kind: Service` | Creates a Service resource. |
| `metadata.name` | Stable Service name: `backend-service`. |
| `type: ClusterIP` | Internal cluster endpoint by default. |
| `selector` | Selects Pods labelled `app: task-manager-backend`. |
| `port: 80` | Port clients use on the Service. |
| `targetPort: 8000` | Destination port on the selected Pod. |
| `protocol: TCP` | Uses TCP. |

### `port` vs `targetPort`

```text
http://backend-service:80
          ↓
     Service port 80
          ↓
     Pod port 8000
          ↓
       FastAPI
```

- **`port`** = Service-facing port.
- **`targetPort`** = destination port on the Pod.
- They do not have to be the same.

## 3. Kubernetes Service types

| Type | What it does | Typical use | Exposure |
|---|---|---|---|
| **ClusterIP** | Gives the Service an internal cluster IP. | Internal traffic, e.g. frontend → backend. | Inside the cluster by default. |
| **NodePort** | Exposes the Service through a port on each node, while retaining the Service endpoint. | Learning or setups that need node-level access. | Through node IP + allocated NodePort, if network-reachable. |
| **LoadBalancer** | Requests an external load balancer from an environment that supports it. | Public/external access in a suitably integrated environment. | Through the provisioned load balancer. |
| **ExternalName** | Maps a Service name to an external DNS name using a CNAME response. | Giving an in-cluster DNS alias to an external hostname. | DNS alias only; it does not proxy to Pod endpoints. |

### Which type should we use?

- **ClusterIP:** default choice for internal app-to-app communication.
- **NodePort:** useful when node-IP-and-port access is appropriate; not guaranteed reachable from every host.
- **LoadBalancer:** useful when an external load balancer is needed and the cluster environment supports provisioning one.
- **ExternalName:** use for a DNS alias to an external hostname, not for selecting a group of Pods.

For this lab, **ClusterIP is the app's intended configuration**. NodePort is a temporary experiment. LoadBalancer is theory for now.

## 4. What the lab output showed

### A. ClusterIP was created

Observed output:

```text
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
backend-service   ClusterIP   10.109.68.191   <none>        80/TCP
```

- `backend-service` = Service name.
- `ClusterIP` = Service type.
- `10.109.68.191` = internal IP assigned in this run.
- `80/TCP` = Service-facing port.
- `<none>` external IP is expected for ClusterIP.

Do not hard-code this run-specific IP in application code; use the Service DNS name.

### B. The selector matched three Pods

The output showed three Running backend Pods with IPs `10.244.0.8`, `10.244.0.9`, and `10.244.0.10`. Their label matched:

```yaml
selector:
  app: task-manager-backend
```

### C. EndpointSlice showed the current backends

Observed:

```text
NAME                    ADDRESSTYPE   PORTS   ENDPOINTS
backend-service-jr99d   IPv4          8000    10.244.0.9,10.244.0.10,10.244.0.8
```

The detailed output showed `Ready: true` and a Pod `TargetRef` for each endpoint.

**EndpointSlice:** a Kubernetes-managed collection of network endpoints backing a Service.

```text
Service selector
      ↓
EndpointSlice
      ├── 10.244.0.8:8000
      ├── 10.244.0.9:8000
      └── 10.244.0.10:8000
```

### D. Service-to-Pod HTTP test worked

The temporary debug Pod requested `http://backend-service:80/docs` and received FastAPI Swagger UI HTML. This is evidence that the in-cluster request reached the app through the Service.

The output also showed a `kubectl run --rm -i` attach warning and fallback to streaming logs. The HTML response was printed and the temporary Pod was deleted. That warning concerns attaching to the short-lived test Pod; it does not by itself mean the Service request failed.

### E. Scaling to three replicas

The script requested three replicas and the Deployment reported a successful rollout. There were already three replicas before this command, so this run verified the three-replica state but did **not** demonstrate a replica-count change.

To see EndpointSlices change clearly in a future run, compare before/after output while scaling from a different count to three.

### F. Deleting a Pod demonstrated replacement

The script deleted `task-manager-backend-57f9ffd665-mh76x`. A replacement appeared: `task-manager-backend-57f9ffd665-l2hqm`, with new IP `10.244.0.12` instead of `10.244.0.8`.

The EndpointSlice then listed `10.244.0.12` along with the other two endpoints.

This demonstrates:
1. The **Deployment/ReplicaSet controllers** replace deleted Pods to maintain the desired count.
2. The **Service's endpoint data** updates to reflect current eligible Pods.

The Service does not create Pods itself.

### G. Kubernetes DNS test worked

The test used `http://backend-service:80/docs` from another Pod and received the FastAPI HTML. This showed that the Service name could be used instead of a fixed ClusterIP.

A namespace-qualified name commonly looks like `backend-service.default.svc.cluster.local`; the DNS suffix can vary by cluster configuration.

### H. NodePort was assigned, but the captured run did not finish

Observed:

```text
NAME              TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)
backend-service   NodePort   10.109.68.191   <none>        80:30148/TCP
```

- Service port = `80`
- NodePort assigned in this run = `30148`
- The Service retains its ClusterIP; NodePort adds another access path.

**Important:** The uploaded output stops while `minikube service backend-service --url` is running. It reports that with Minikube's Docker driver on Windows, the terminal needs to stay open. Therefore, the captured output does **not** prove that the subsequent `curl` succeeded or that the script restored ClusterIP.

Check current state:

```bash
kubectl get service backend-service -o wide
```

If it still shows `NodePort`, restore the intended app configuration:

```bash
kubectl patch service backend-service -p '{"spec":{"type":"ClusterIP"}}'
kubectl get service backend-service -o wide
```

For the Minikube Docker driver on Windows, keep the terminal opened by `minikube service ... --url` running while testing the returned URL.

## 5. Request flow

```text
Debug Pod / in-cluster client
          ↓
Kubernetes DNS: backend-service
          ↓
Service endpoint (ClusterIP:80)
          ↓
Service routing using current endpoint data
          ↓
Eligible backend Pod IP:8000
          ↓
FastAPI
```

The Service is the stable access point; EndpointSlices represent the current backing endpoints. The cluster's Service networking implementation routes traffic to them.

## 6. Practical comparison

```text
CLUSTERIP — internal
Client Pod → Service ClusterIP:80 → Backend Pod:8000

NODEPORT — node-level access
External client (if network-reachable) → Node IP:NodePort → Service → Pod:8000

LOADBALANCER — external load balancer
External client → External Load Balancer → Service → Pod:8000
```

External reachability depends on cluster networking, firewalls, and provider integration.

## 7. Troubleshooting checklist

```bash
kubectl get service backend-service
kubectl describe service backend-service
kubectl get pods -l app=task-manager-backend -o wide
kubectl get endpointslice -l kubernetes.io/service-name=backend-service -o wide
kubectl describe endpointslice -l kubernetes.io/service-name=backend-service
kubectl logs deployment/task-manager-backend
kubectl get events --sort-by=.metadata.creationTimestamp
```

Common causes:
- **No endpoints:** selector mismatch or Pods not eligible/ready.
- **Wrong `targetPort`:** traffic is sent to a port where the app is not listening.
- **Application issue:** inspect container/application port and logs.
- **DNS failure:** check Service name and namespace from inside the cluster.
- **NodePort unreachable:** check node/network reachability and Minikube's Windows Docker-driver behavior.
- **Wrong expectation:** ClusterIP is internal by default, not direct external access.

## 8. Key one-liners

- **Deployment:** manages the desired number and versions of Pods.
- **Service:** provides a stable endpoint and selects matching Pods.
- **EndpointSlice:** records current network endpoints backing a Service.
- **ClusterIP:** internal Service endpoint.
- **NodePort:** exposes the Service through a node port where network access permits.
- **LoadBalancer:** requests an external load balancer when supported.
- **ExternalName:** DNS alias for an external hostname.
- **`port`:** Service port.
- **`targetPort`:** destination port on the Pod.
- **Service does not create Pods.** Deployment/ReplicaSet controllers do.
- **Use Service DNS instead of hard-coding Pod IPs.**

## 9. What comes next?

First verify that the Service has been restored to `ClusterIP`. Then study **Ingress**: why it is useful for a common HTTP entry point, host/path routing, the Ingress Controller, and routing to Services.

Cloud Kubernetes (EKS/GKE/AKS) comes later, after local Kubernetes networking and app configuration fundamentals.
