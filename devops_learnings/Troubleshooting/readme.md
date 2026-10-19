
# Kubernetes Troubleshooting — Revision Notes

## 1. Kubernetes Troubleshooting Fundamentals

- **Kubernetes:** Container orchestration platform that manages deployment, scaling, networking, and recovery of applications.
- **Troubleshooting:** Finding the root cause of a failure using resource status, events, logs, and diagnostic commands.
- **kubectl:** CLI used to communicate with the Kubernetes API server.
- **Cluster:** Collection of control-plane and worker-node components.
- **Node:** Machine that runs Kubernetes workloads.
- **Pod:** Smallest deployable Kubernetes unit, containing one or more containers.
- **Deployment:** Manages replicated Pods and rolling updates.
- **Service:** Provides a stable network endpoint for accessing Pods.
- **Namespace:** Logical grouping of Kubernetes resources.
- **Control Plane:** Components that manage and reconcile the cluster's desired state.
- **Desired State:** Configuration declared by the user, such as three replicas.
- **Actual State:** The current state of resources running in the cluster.
- **Reconciliation:** Kubernetes controllers continuously work to make actual state match desired state.

Official docs: https://kubernetes.io/docs/

---

## 2. kubectl Command Syntax

General syntax:

```bash
kubectl <command> <resource-type> <resource-name> [flags]
```

Examples:

```bash
kubectl get pods
kubectl describe pod my-pod
kubectl logs my-pod
kubectl delete pod my-pod
```

### 2.1 kubectl Global Flags

- `-n`: Select a namespace.
- `-A` or `--all-namespaces`: Display resources across all namespaces.
- `-o wide`: Display additional resource information.
- `-o yaml`: Print the resource as YAML.
- `-o json`: Print the resource as JSON.
- `-w` or `--watch`: Watch for resource changes.
- `-l`: Filter resources using label selectors.
- `--show-labels`: Display resource labels.
- `--all`: Include all resources of the applicable type.
- `--context`: Select a Kubernetes context.
- `--kubeconfig`: Specify a kubeconfig file.
- `--dry-run=client`: Validate/generate a request locally without persisting it.
- `--dry-run=server`: Ask the API server to process a dry-run request without persisting it.

Examples:

```bash
kubectl get pods -n default
kubectl get pods -A
kubectl get pods -o wide
kubectl get pod my-pod -o yaml
kubectl get pods -w
kubectl get pods --show-labels
kubectl get pods -l app=web
kubectl config current-context
kubectl config get-contexts
```

---

## 3. Essential Troubleshooting Commands

### 3.1 kubectl get

Definition: Displays the status and summary of Kubernetes resources.

```bash
kubectl get pods
kubectl get pods -o wide
kubectl get deployments
kubectl get services
kubectl get nodes
kubectl get configmaps
kubectl get secrets
kubectl get events
kubectl get all
```

Important: `kubectl get all` does not display every Kubernetes resource type.

### 3.2 kubectl describe

Definition: Displays detailed resource information, conditions, configuration, and events.

```bash
kubectl describe pod my-pod
kubectl describe deployment my-app
kubectl describe service my-service
kubectl describe node my-node
kubectl describe hpa my-hpa
```

Use it to identify scheduling failures, image-pull errors, failed probes, and resource constraints.

### 3.3 kubectl logs

Definition: Displays stdout/stderr logs produced by a container.

```bash
kubectl logs my-pod
kubectl logs -f my-pod
kubectl logs my-pod --previous
kubectl logs my-pod -c app
kubectl logs my-pod --tail=100
kubectl logs my-pod --since=10m
kubectl logs deployment/my-app
```

Flags:

- `-f`: Follow logs continuously.
- `--previous`: Read logs from the previous terminated container instance.
- `-c`: Select a container.
- `--tail=100`: Show the last 100 lines.
- `--since=10m`: Show logs from the last 10 minutes.

### 3.4 kubectl exec

Definition: Executes a command inside a running container.

```bash
kubectl exec -it my-pod -- sh
kubectl exec my-pod -- hostname
kubectl exec my-pod -- printenv
kubectl exec my-pod -- ls /
kubectl exec my-pod -c app -- sh
```

Flags:

- `-i`: Keep standard input open.
- `-t`: Allocate a terminal.
- `--`: Separates kubectl options from the command executed inside the container.

Note: Minimal containers might not contain `bash`, `curl`, `ping`, or other debugging utilities.

### 3.5 kubectl events

Definition: Displays recorded Kubernetes events associated with resource operations and failures.

```bash
kubectl get events
kubectl get events -A
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl describe pod my-pod
kubectl events --watch
```

Events may expire or be aggregated; they are not permanent logs.

### 3.6 Resource and Configuration Inspection

```bash
kubectl get pod my-pod -o yaml
kubectl get deployment my-app -o yaml
kubectl get pod my-pod -o json
kubectl get pods --show-labels
kubectl get endpointslices
kubectl get serviceaccounts
kubectl get hpa
kubectl get ingress
```

### 3.7 Cluster and Namespace Inspection

```bash
kubectl cluster-info
kubectl get nodes
kubectl describe node my-node
kubectl get namespaces
kubectl get pods -n kube-system
kubectl config current-context
kubectl config get-contexts
```

Official docs:
https://kubernetes.io/docs/reference/kubectl/

---

## 4. Understanding Pod STATUS, READY, RESTARTS and AGE

Example:

```text
NAME      READY   STATUS             RESTARTS   AGE
web-1     1/1     Running            0          5m
api-1     0/1     CrashLoopBackOff   5          3m
db-1      0/1     Pending            0          2m
```

- `NAME`: Resource name.
- `READY`: Number of ready containers / total containers.
- `STATUS`: Current Pod phase or a more specific displayed condition.
- `RESTARTS`: Number of container restarts.
- `AGE`: Time since resource creation.

### 4.1 READY Values

- `1/1`: One container is ready.
- `0/1`: The single container is not ready.
- `2/2`: Both containers are ready.
- `1/2`: One of two containers is ready.

A Pod can be `Running` but not `Ready`.

### 4.2 Common Pod Statuses

- `Pending`: Pod has not completed scheduling or startup.
- `Running`: Pod has been bound to a node and at least one container is running or starting/restarting.
- `Succeeded`: All containers terminated successfully.
- `Failed`: All containers terminated, and at least one failed.
- `Unknown`: Kubernetes cannot determine the Pod's state.
- `Terminating`: Pod deletion is in progress; this is commonly shown by kubectl rather than being a Pod phase.
- `ContainerCreating`: Container setup is in progress.
- `CrashLoopBackOff`: Container keeps failing, and Kubernetes is delaying retries.
- `ImagePullBackOff`: Kubernetes cannot pull the container image and is delaying retries.
- `ErrImagePull`: Image retrieval failed.
- `CreateContainerConfigError`: Container configuration could not be prepared.
- `CreateContainerError`: Container creation failed.
- `RunContainerError`: Container startup failed.
- `InvalidImageName`: Image reference is invalid.
- `OOMKilled`: Container was terminated due to an out-of-memory condition.
- `Evicted`: Pod was removed from a node, commonly due to resource pressure.
- `PodInitializing`: Container initialization is still in progress.
- `Init:0/1`: Init containers have not all completed.
- `Init:CrashLoopBackOff`: An init container is repeatedly failing.

Important: Values such as `CrashLoopBackOff`, `ContainerCreating`, and `Terminating` are displayed statuses, not official Pod phase values.

Official docs:
https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/

---

## 5. Understanding kubectl describe Output

Typical output:

```text
Name:           web-app
Namespace:      default
Node:           worker-1
Labels:         app=web
Status:         Running
IP:             10.244.0.5

Containers:
  app:
    Image:       nginx:1.27
    State:       Running
    Ready:       True
    Restart Count: 0

Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True

Events:
  Type     Reason     Message
  Normal   Scheduled  Successfully assigned ...
  Normal   Pulled     Container image pulled
  Normal   Started    Started container
```

### Important Fields

- `Name`: Resource name.
- `Namespace`: Namespace containing the resource.
- `Node`: Node assigned to the Pod.
- `Labels`: Key-value metadata used for selection.
- `Image`: Container image and tag.
- `State`: Current container state.
- `Last State`: Previous container state.
- `Restart Count`: Number of container restarts.
- `Ready`: Whether the container is ready to serve traffic.
- `Conditions`: Evaluations of Pod status.
- `Events`: Recorded scheduling, image, startup, and health-check activity.

### Common Condition Types

- `PodScheduled`: Whether the Pod has been assigned to a node.
- `Initialized`: Whether init-container processing has completed.
- `ContainersReady`: Whether all containers are ready.
- `Ready`: Whether the Pod is ready to serve traffic, subject to its readiness conditions.

Condition status values generally include `True`, `False`, and `Unknown`.

---

## 6. Understanding Kubernetes Events and Error Tags

Event types:

- `Normal`: Expected lifecycle activity.
- `Warning`: Something abnormal or potentially problematic happened.

Common event reasons:

- `Scheduled`: Pod assigned to a node.
- `FailedScheduling`: Scheduler could not place the Pod.
- `Pulling`: Image download started.
- `Pulled`: Image successfully downloaded.
- `Failed`: An operation failed.
- `BackOff`: Kubernetes is delaying another attempt.
- `Started`: Container started.
- `Created`: Container was created.
- `Killing`: Kubernetes is terminating a container.
- `Unhealthy`: Health probe failed.
- `FailedMount`: Volume could not be mounted.
- `FailedAttachVolume`: Volume attachment failed.
- `Evicted`: Pod was evicted from a node.
- `OOMKilling`: Node/kernel recorded an out-of-memory kill event.

Example:

```text
Type: Warning
Reason: FailedScheduling
Message: 0/2 nodes are available: insufficient memory.
```

Meaning: No eligible node has enough allocatable memory for the Pod's requested resources.

Example:

```text
Type: Warning
Reason: Failed
Message: Failed to pull image.
```

Meaning: Investigate image name, tag, registry availability, authentication, and network access.

Do not diagnose an issue from the `Reason` alone; always read the event message and inspect the resource.

Official docs:
https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/

---

## 7. Error: CrashLoopBackOff

Definition: A container repeatedly exits or fails and Kubernetes applies a delay before restarting it.

Common causes:

- Application crash or unhandled exception.
- Invalid startup command.
- Missing environment variables.
- Incorrect configuration.
- Database or dependency unavailable at startup.
- Failed liveness probe.
- Out-of-memory termination.
- Application exits immediately.

Diagnosis:

```bash
kubectl get pods
kubectl describe pod my-pod
kubectl logs my-pod
kubectl logs my-pod --previous
kubectl get events --sort-by=.metadata.creationTimestamp
```

Check:

1. Container exit code.
2. Termination reason.
3. Previous logs.
4. Startup and liveness probe configuration.
5. Environment variables and mounted configuration.
6. Resource limits.

Example exit codes:

- `0`: Process exited successfully.
- `1`: General application error.
- `137`: Often indicates SIGKILL; check whether the container was OOMKilled.
- `139`: Often indicates a segmentation fault.
- `143`: Often indicates termination by SIGTERM.

Exit codes are clues, not definitive diagnoses.

Fix the actual root cause and verify:

```bash
kubectl get pods -w
kubectl logs my-pod
```

---

## 8. Error: ImagePullBackOff / ErrImagePull

Definition: Kubernetes cannot download the specified container image.

Common causes:

- Wrong repository name.
- Nonexistent image tag.
- Private registry authentication failure.
- Registry unavailable.
- Network or DNS failure.
- Image reference syntax error.

Diagnosis:

```bash
kubectl describe pod my-pod
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get pod my-pod -o yaml
```

Look for messages such as:

- `manifest unknown`: Requested image/tag is not available under that reference.
- `not found`: Requested image or registry resource was not found.
- `unauthorized`: Authentication failed or credentials are insufficient.
- `pull access denied`: Access is denied or the image reference is invalid.
- `no such host`: DNS resolution failed.
- `i/o timeout`: Network operation timed out.

Fix the image reference:

```yaml
containers:
  - name: app
    image: nginx:1.27
```

For private registries, configure appropriate image pull credentials:

```yaml
spec:
  imagePullSecrets:
    - name: registry-credentials
```

The Secret must exist in the Pod's namespace and contain valid registry credentials.

Verify:

```bash
kubectl get pods -w
kubectl describe pod my-pod
```

Official docs:
https://kubernetes.io/docs/concepts/containers/images/

---

## 9. Error: Pending / FailedScheduling

Definition: Pod cannot progress to normal execution; a common cause is that the scheduler cannot find a suitable node.

Common causes:

- Insufficient CPU.
- Insufficient memory.
- Node selector matches no nodes.
- Affinity rules cannot be satisfied.
- Untolerated node taints.
- PersistentVolumeClaim is unbound.
- Nodes are unavailable or unsuitable.

Diagnosis:

```bash
kubectl get pods -o wide
kubectl describe pod my-pod
kubectl get nodes
kubectl describe node my-node
kubectl get pvc
kubectl get events
```

Example resource request:

```yaml
resources:
  requests:
    cpu: "500m"
    memory: "256Mi"
  limits:
    cpu: "1"
    memory: "512Mi"
```

Meanings:

- `500m` CPU = 0.5 CPU core.
- `1` CPU = 1 CPU core.
- `256Mi` = 256 mebibytes.
- `512Mi` = 512 mebibytes.

Important:

- Requests influence scheduling and resource guarantees.
- Limits constrain container resource usage.
- A request that cannot fit on an eligible node can prevent scheduling.
- CPU limits can throttle a container.
- Exceeding a container memory limit can cause an OOM kill.

Fix resource requests or scheduling constraints based on actual requirements and node capacity.

Official docs:
https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

---

## 10. Error: OOMKilled

Definition: A container was killed because of an out-of-memory condition.

Diagnosis:

```bash
kubectl describe pod my-pod
kubectl get pod my-pod -o yaml
kubectl top pod my-pod
kubectl top nodes
```

Check:

- `lastState.terminated.reason`
- Container memory limit.
- Memory usage over time.
- Application memory leaks.
- Node memory pressure.
- Container restart count.

Example:

```yaml
resources:
  requests:
    memory: "128Mi"
  limits:
    memory: "256Mi"
```

Fix:

- Profile application memory consumption.
- Fix memory leaks.
- Adjust memory limits when justified.
- Check whether node-level memory pressure is affecting workloads.

`kubectl top` requires a working metrics pipeline, commonly Metrics Server.

Official docs:
https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/

---

## 11. Error: CreateContainerConfigError

Definition: Kubernetes cannot prepare the container due to a configuration problem.

Common causes:

- Missing ConfigMap.
- Missing Secret.
- Incorrect referenced key.
- Invalid environment variable reference.
- Invalid volume or mount configuration.

Diagnosis:

```bash
kubectl describe pod my-pod
kubectl get configmaps
kubectl get secrets
kubectl get pod my-pod -o yaml
```

ConfigMap example:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
```

Reference:

```yaml
envFrom:
  - configMapRef:
      name: app-config
```

Ensure the referenced resource exists in the same namespace as the Pod.

---

## 12. Error: FailedMount / FailedAttachVolume

Definition: Kubernetes cannot mount or attach a required volume.

Common causes:

- PersistentVolumeClaim is missing.
- PersistentVolumeClaim is Pending.
- StorageClass configuration is invalid.
- Storage provider or CSI driver issue.
- Permission problems.
- Volume is already attached elsewhere.

Diagnosis:

```bash
kubectl describe pod my-pod
kubectl get pvc
kubectl describe pvc my-pvc
kubectl get pv
kubectl get storageclass
```

Example volume reference:

```yaml
volumes:
  - name: app-storage
    persistentVolumeClaim:
      claimName: my-pvc
```

Do not delete persistent volumes or claims blindly; they may contain important application data.

Official docs:
https://kubernetes.io/docs/concepts/storage/persistent-volumes/

---

## 13. Service Troubleshooting

Definition: A Service provides a stable network endpoint for a set of selected Pods.

### Service Types

- `ClusterIP`: Internal cluster access; default Service type.
- `NodePort`: Exposes a Service on a port on eligible nodes.
- `LoadBalancer`: Requests an external load balancer from a supported environment.
- `ExternalName`: Maps the Service to an external DNS name.

Example Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: ClusterIP
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 8080
```

Meanings:

- `selector`: Matches Pod labels.
- `port`: Port exposed by the Service.
- `targetPort`: Destination port on the backend Pod.
- `protocol`: Defaults to TCP if omitted.

Diagnosis:

```bash
kubectl get services
kubectl describe service web-service
kubectl get pods --show-labels
kubectl get endpoints web-service
kubectl get endpointslices
```

Common problems:

- Selector does not match Pod labels.
- No ready backend Pods.
- Incorrect `targetPort`.
- Application listens on a different port.
- NetworkPolicy blocks traffic.
- DNS or routing issue.

An empty endpoint list commonly means the Service has no eligible backends. Check labels and readiness before investigating DNS.

Official docs:
https://kubernetes.io/docs/concepts/services-networking/service/

---

## 14. DNS and CoreDNS Troubleshooting

Definition: Kubernetes DNS resolves Service names and other supported cluster DNS names.

Typical Service DNS name:

```text
<service>.<namespace>.svc.cluster.local
```

The cluster domain may differ.

Examples:

```bash
kubectl get pods -n kube-system
kubectl get services -n kube-system
kubectl get configmap coredns -n kube-system
```

From a diagnostic Pod containing the necessary utilities:

```bash
nslookup web-service
nslookup web-service.other-namespace
curl -v http://web-service:80
```

Diagnosis:

- Name does not resolve: inspect DNS settings, CoreDNS, and DNS connectivity.
- Name resolves but connection fails: inspect Service endpoints, ports, policies, and application listeners.
- Service IP works but name fails: investigate DNS.
- No Service endpoints: inspect selectors, Pod labels, and readiness.

Official docs:
https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/

---

## 15. Liveness, Readiness and Startup Probes

### Liveness Probe

Definition: Determines whether a container should be restarted.

### Readiness Probe

Definition: Determines whether a Pod should receive Service traffic.

### Startup Probe

Definition: Gives a slow-starting application time to initialize before liveness and readiness probes take effect.

Example:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5

startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

Important:

- Liveness failure can trigger container restarts.
- Readiness failure removes the Pod from normal ready Service backends.
- Startup probes protect slow-starting applications from premature liveness failures.
- Probe endpoints and ports must match the actual application.

Official docs:
https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/

---

## 16. ConfigMap and Secret Troubleshooting

### ConfigMap

Definition: Stores non-sensitive configuration data.

```bash
kubectl get configmaps
kubectl describe configmap app-config
kubectl get configmap app-config -o yaml
```

### Secret

Definition: Stores sensitive configuration data such as credentials. Base64 encoding is not encryption.

```bash
kubectl get secrets
kubectl describe secret app-secret
```

Avoid printing Secret contents into terminal logs or shared debugging output.

Common failures:

- Missing resource.
- Wrong resource name.
- Wrong key.
- Resource in the wrong namespace.
- Application requires a restart to consume updated environment variables.

ConfigMap or Secret values mounted as files can update eventually, subject to the mount method. Values injected as environment variables do not automatically update inside an already-running process.

Official docs:

https://kubernetes.io/docs/concepts/configuration/configmap/

https://kubernetes.io/docs/concepts/configuration/secret/

---

## 17. Deployment Troubleshooting

Definition: A Deployment manages ReplicaSets and provides declarative updates for Pods.

Commands:

```bash
kubectl get deployments
kubectl describe deployment my-app
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app
kubectl rollout restart deployment/my-app
```

Common symptoms:

- Desired replicas differ from ready replicas.
- New ReplicaSet cannot create healthy Pods.
- Image pull failures.
- Readiness probe failures.
- Insufficient resources.
- Incorrect Deployment selector or Pod template.

Inspect:

```bash
kubectl get replicasets
kubectl get pods -o wide
kubectl describe deployment my-app
kubectl logs deployment/my-app
```

Important: `kubectl rollout undo` rolls back a Kubernetes Deployment. `helm rollback` rolls back a Helm release. These are related but different operations.

Official docs:
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

---

## 18. HPA Troubleshooting

Definition: HorizontalPodAutoscaler adjusts the replica count based on observed metrics.

Commands:

```bash
kubectl get hpa
kubectl describe hpa my-hpa
kubectl top pods
kubectl top nodes
```

Common issues:

- Metrics unavailable.
- CPU or memory requests missing where utilization-based calculations require them.
- Replica limits reached.
- Resource constraints prevent new Pods from scheduling.
- Application cannot scale effectively.

HPA changes replica counts; it does not automatically fix broken Pods or application errors.

Official docs:
https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

---

## 19. Ingress and HTTPRoute Troubleshooting

### Ingress

Definition: Configures HTTP/HTTPS routing into a cluster through an Ingress controller.

```bash
kubectl get ingress
kubectl describe ingress my-ingress
kubectl get services
```

Check:

- Ingress controller exists and is healthy.
- Host and path rules match the request.
- Backend Service exists.
- Backend Service has ready endpoints.
- TLS configuration is correct.

Official docs:
https://kubernetes.io/docs/concepts/services-networking/ingress/

### HTTPRoute

Definition: Gateway API resource defining HTTP routing rules.

```bash
kubectl get httproute
kubectl describe httproute my-route
kubectl get gateway
```

Check:

- Gateway API CRDs and compatible controller are installed.
- Parent Gateway references are valid.
- Route attachment and status conditions.
- Backend Service and port.
- Controller and network health.

Official docs:
https://gateway-api.sigs.k8s.io/api-types/httproute/

---

## 20. ServiceAccount Troubleshooting

Definition: Provides an identity for a workload or process interacting with the Kubernetes API.

Commands:

```bash
kubectl get serviceaccounts
kubectl describe serviceaccount my-account
kubectl auth can-i get pods \
  --as=system:serviceaccount:default:my-account
```

Common errors:

- `Forbidden`: Authenticated identity lacks the required authorization.
- `Unauthorized`: Authentication credentials or identity are not accepted.
- `serviceaccount not found`: Referenced ServiceAccount does not exist in the namespace.

Check the ServiceAccount, Role or ClusterRole, and RoleBinding or ClusterRoleBinding.

Official docs:
https://kubernetes.io/docs/concepts/security/service-accounts/

---

## 21. Common Kubernetes API and Networking Errors

- `NotFound`: Requested resource does not exist at the specified name/namespace.
- `AlreadyExists`: Resource with that name already exists.
- `Forbidden`: Request is not authorized.
- `Unauthorized`: Authentication failed or credentials are missing/invalid.
- `Conflict`: Resource update conflicts with its current version or state.
- `Invalid`: Submitted object does not satisfy API validation.
- `BadRequest`: Request is malformed or invalid.
- `InternalError`: API server or another component encountered an internal error.
- `context deadline exceeded`: Operation did not finish within the deadline.
- `connection refused`: Connection reached a destination that refused it, or no process is listening at that endpoint.
- `i/o timeout`: Network or I/O operation timed out.
- `no such host`: DNS lookup failed.
- `certificate signed by unknown authority`: Certificate trust validation failed.
- `TLS handshake timeout`: TLS negotiation did not complete in time.
- `port is already allocated`: Requested port is already in use or reserved.
- `no matches for kind`: API server does not recognize the requested resource type; check API version and installed CRDs.

Always inspect the complete error and relevant events; a message may originate from kubectl, the API server, a controller, a container runtime, or the application.

---

## 22. Standard Troubleshooting Workflow

Step 1: Observe the resources.

```bash
kubectl get pods -o wide
kubectl get deployments
kubectl get services
```

Step 2: Inspect the failing resource.

```bash
kubectl describe pod my-pod
```

Step 3: Read current and previous logs.

```bash
kubectl logs my-pod
kubectl logs my-pod --previous
```

Step 4: Inspect recent events.

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
```

Step 5: Inspect related resources.

```bash
kubectl get pods --show-labels
kubectl get endpointslices
kubectl get pvc
kubectl get configmaps
```

Step 6: Test connectivity or container state if possible.

```bash
kubectl exec -it my-pod -- sh
```

Step 7: Fix the root cause and verify.

```bash
kubectl get pods -w
kubectl rollout status deployment/my-app
```

The best diagnostic command depends on the symptom. For example, image-pull failures need image and event inspection before application logs can exist.

---

## 23. Quick Troubleshooting Cheat Sheet

| Symptom | First command | Investigate |
|---|---|---|
| CrashLoopBackOff | `kubectl logs POD --previous` | Application exit, probes, config |
| ImagePullBackOff | `kubectl describe pod POD` | Image, tag, credentials |
| Pending | `kubectl describe pod POD` | Scheduling, resources, storage |
| OOMKilled | `kubectl describe pod POD` | Memory limit, memory pressure |
| Service unreachable | `kubectl describe svc SERVICE` | Selector, ports, endpoints |
| DNS failure | `nslookup SERVICE` inside a diagnostic Pod | CoreDNS, DNS settings |
| Pod not ready | `kubectl describe pod POD` | Readiness probe and dependencies |
| Deployment stuck | `kubectl rollout status deployment/NAME` | ReplicaSets, Pods, events |
| PVC Pending | `kubectl describe pvc PVC` | StorageClass and volumes |
| Forbidden | `kubectl auth can-i ...` | RBAC permissions |
| FailedMount | `kubectl describe pod POD` | PVC, storage driver, mount |
| HPA metrics missing | `kubectl describe hpa HPA` | Metrics pipeline and requests |

---

## 24. Important Official Documentation

- Kubernetes documentation: https://kubernetes.io/docs/
- kubectl reference: https://kubernetes.io/docs/reference/kubectl/
- Debugging applications: https://kubernetes.io/docs/tasks/debug/
- Pod lifecycle: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Container images: https://kubernetes.io/docs/concepts/containers/images/
- Resource management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Services: https://kubernetes.io/docs/concepts/services-networking/service/
- Service and Pod DNS: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
- Probes: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
- Persistent volumes: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- ConfigMaps: https://kubernetes.io/docs/concepts/configuration/configmap/
- Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
- Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- HPA: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- Ingress: https://kubernetes.io/docs/concepts/services-networking/ingress/
- Gateway API HTTPRoute: https://gateway-api.sigs.k8s.io/api-types/httproute/
- ServiceAccounts: https://kubernetes.io/docs/concepts/security/service-accounts/

---

## 25. Final Revision Principle

Kubernetes troubleshooting is about following evidence:

1. Identify the failing resource.
2. Read its state, conditions, and events.
3. Inspect application logs when the container has started.
4. Check related resources, configuration, networking, and resource constraints.
5. Correct the root cause.
6. Verify the application is healthy and reachable.

Do not blindly restart Pods, delete resources, or increase resource limits without identifying the actual cause.
