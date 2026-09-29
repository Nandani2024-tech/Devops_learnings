# Kubernetes — Module 06

# Fundamentals & Workloads

> **Goal:** Understand Kubernetes architecture, Pods, Labels, Selectors, ReplicaSets, Deployments, Scaling, Rolling Updates, and Rollbacks.
>
> **Scope:** This README covers **ONLY Module 1 — Kubernetes Fundamentals + Workloads**.
>
> Topics such as Services, Ingress, ConfigMaps, Secrets, Storage, Probes, HPA, RBAC, and StatefulSets are **intentionally not included**.

---

# 1. Kubernetes — The Big Picture

Docker is mainly responsible for running containers.

```text
Application
    ↓
Dockerfile
    ↓
Docker Image
    ↓
Container
```

But when we have:

```text
100 containers
10 servers
multiple applications
containers crashing
scaling requirements
new application versions
```

managing everything manually becomes difficult.

Kubernetes is a **container orchestration platform**.

Its job is to manage containerized workloads across machines and continuously maintain the state we specify.

```text
Docker
    ↓
"Run this container"

Kubernetes
    ↓
"Make sure my application is running
 with the desired number of replicas,
 on suitable machines,
 and manage changes."
```

---

# 2. Kubernetes Cluster

A Kubernetes environment is called a **Cluster**.

A cluster broadly contains:

```text
Kubernetes Cluster
│
├── Control Plane
│
└── Worker Nodes
    ├── Node 1
    ├── Node 2
    └── Node 3
```

## Control Plane

The Control Plane manages the cluster.

## Worker Node

Worker Nodes are where application workloads run.

Simple mental model:

```text
Control Plane
     ↓
"WHAT should happen?"

Worker Nodes
     ↓
"RUN the workloads"
```

---

# 3. Kubernetes Architecture

The major components studied in this module are:

```text
Control Plane
│
├── kube-apiserver
├── etcd
├── kube-scheduler
└── kube-controller-manager


Worker Node
│
├── kubelet
├── Container Runtime
└── Pods


User
│
└── kubectl
       ↓
   API Server
```

---

# 4. kube-apiserver

The **Kubernetes API Server** is the central communication point for the Kubernetes API.

Think of it as the **front door of Kubernetes**.

When we run:

```bash
kubectl get pods
```

`kubectl` communicates with the API Server.

```text
User
  ↓
kubectl
  ↓
API Server
  ↓
Kubernetes Cluster
```

### Remember

```text
API Server = Central communication/API entry point
```

---

# 5. etcd

`etcd` is Kubernetes' distributed key-value data store.

It stores important Kubernetes cluster state.

Conceptually:

```text
Kubernetes
    ↓
  etcd
    ↓
Cluster State / Data
```

Examples of information Kubernetes needs to keep track of:

```text
Deployments
Pods
Desired configuration
Cluster state
Resource information
```

### Remember

```text
etcd = stores Kubernetes cluster state
```

---

# 6. kube-scheduler

When a Pod needs to run, Kubernetes needs to decide:

> Which Worker Node should run this Pod?

The **kube-scheduler** makes this scheduling decision.

```text
New Pod
   ↓
Scheduler
   ↓
Choose suitable Worker Node
   ↓
Pod assigned to Node
```

### Remember

```text
Scheduler = decides WHERE a Pod should run
```

---

# 7. kube-controller-manager

Kubernetes follows the concept of **desired state**.

Suppose:

```text
Desired = 3 Pods
Actual  = 2 Pods
```

A controller notices the difference and works to correct it.

```text
Desired State
      ↓
Controller
      ↓
Compare with Actual State
      ↓
Take corrective action
      ↓
Actual State moves toward Desired State
```

For example:

```text
Desired = 3
Actual  = 2

       ↓

Controller notices mismatch

       ↓

Create another Pod

       ↓

Desired = 3
Actual  = 3
```

### Remember

```text
Controller = continuously works toward desired state
```

---

# 8. Worker Node

A Worker Node is a machine where workloads actually run.

Important components:

```text
Worker Node
│
├── kubelet
├── Container Runtime
└── Pods
```

---

# 9. kubelet

`kubelet` runs on Worker Nodes.

It is responsible for making sure Pods assigned to that node are running correctly.

Conceptually:

```text
Control Plane
      ↓
"This node should run this Pod"
      ↓
kubelet
      ↓
Container Runtime
      ↓
Container
```

### Remember

```text
kubelet = Node-level agent responsible for Pods
```

---

# 10. Container Runtime

The Container Runtime is responsible for actually running containers.

Conceptually:

```text
Kubernetes
    ↓
kubelet
    ↓
Container Runtime
    ↓
Container
```

Common container runtimes include:

```text
containerd
CRI-O
```

For this module, focus on the **role**, not implementation details.

### Remember

```text
Container Runtime = actually runs containers
```

---

# 11. kubectl

`kubectl` is the Kubernetes command-line tool.

It is used to communicate with the Kubernetes API.

```text
User
  ↓
kubectl
  ↓
API Server
  ↓
Kubernetes
```

Examples:

```bash
kubectl get pods
kubectl get nodes
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl apply -f pod.yaml
kubectl delete pod <pod-name>
```

---

# 12. Kubernetes Objects / Resources

Kubernetes manages different types of objects/resources.

Examples:

```text
Pod
ReplicaSet
Deployment
Service
ConfigMap
Secret
...
```

For **this module**, focus only on:

```text
Pod
ReplicaSet
Deployment
```

---

# 13. YAML Manifests

Kubernetes resources are commonly described using YAML manifests.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-app

spec:
  replicas: 3
```

Basic meaning:

```text
apiVersion
    ↓
Which Kubernetes API version?

kind
    ↓
What type of resource?

metadata
    ↓
Resource information/name

spec
    ↓
What state do we want?
```

---

# 14. Declarative Configuration

Kubernetes is heavily based on a **declarative model**.

## Imperative

You tell the system what actions to perform.

```text
Create container
Start container
Create another container
```

## Declarative

You describe the desired final state.

```yaml
replicas: 3
```

Meaning:

> I want 3 replicas.

Kubernetes determines how to achieve that state.

```text
Desired State
      ↓
Kubernetes
      ↓
Actual State
```

---

# 15. Desired State — Core Kubernetes Concept

This is one of the most important concepts in Kubernetes.

Suppose we specify:

```yaml
replicas: 3
```

This means:

```text
Desired State = 3 Pods
```

If the actual state is:

```text
Actual State = 2 Pods
```

Kubernetes tries to correct the difference.

```text
Desired = 3
Actual  = 2

     ↓

Kubernetes reconciles

     ↓

Create another Pod

     ↓

Desired = 3
Actual  = 3
```

### Core idea

```text
Kubernetes continuously works
to make:

Actual State → Desired State
```

This process is called **reconciliation**.

---

# 16. Namespace — Basic Understanding

A Namespace provides logical grouping/isolation of resources within a cluster.

Example:

```text
Cluster
│
├── default
│   ├── Pod
│   └── Deployment
│
├── development
│   ├── Pod
│   └── Deployment
│
└── production
    ├── Pod
    └── Deployment
```

For this module, remember only:

```text
Namespace = logical grouping of Kubernetes resources
```

---

# 17. Pods

A **Pod is the smallest deployable unit that Kubernetes manages.**

Important:

```text
Kubernetes manages Pods
rather than directly managing individual containers.
```

A Pod can contain one or more containers.

Most beginner applications use:

```text
Pod
└── Container
```

A multi-container Pod can look like:

```text
Pod
├── Main Container
└── Sidecar Container
```

---

# 18. Pod vs Container

### Container

Runs the application process.

### Pod

Kubernetes' unit of deployment that contains one or more containers.

```text
Kubernetes
    ↓
   Pod
    ↓
Container
    ↓
Application
```

For a simple application:

```text
1 Pod
  ↓
1 Container
```

---

# 19. Example Pod YAML

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: flask-pod

spec:
  containers:
    - name: flask
      image: my-flask-app:v1
```

Structure:

```text
Pod
 ↓
flask container
 ↓
my-flask-app:v1
```

---

# 20. Create a Pod

Create:

```text
pod.yaml
```

Then:

```bash
kubectl apply -f pod.yaml
```

Check:

```bash
kubectl get pods
```

Example:

```text
NAME         READY   STATUS    RESTARTS   AGE
flask-pod    1/1     Running   0          10s
```

---

# 21. `kubectl get pods`

Command:

```bash
kubectl get pods
```

Purpose:

> Show the Pods in the current namespace.

Think:

```text
get = quick overview
```

---

# 22. `kubectl describe`

Command:

```bash
kubectl describe pod flask-pod
```

Purpose:

> Show detailed information about a Pod.

Mental model:

```text
kubectl get
    ↓
Quick overview

kubectl describe
    ↓
Detailed information
```

Very useful for troubleshooting.

---

# 23. `kubectl logs`

Command:

```bash
kubectl logs flask-pod
```

Purpose:

> View the container's application logs.

Mental model:

```text
Pod
 ↓
Container
 ↓
Application
 ↓
Logs
```

Useful when an application isn't behaving as expected.

---

# 24. `kubectl exec`

Command:

```bash
kubectl exec -it flask-pod -- sh
```

Purpose:

> Execute a command inside a running container.

This is similar to Docker:

```bash
docker exec -it <container> sh
```

Kubernetes:

```bash
kubectl exec -it <pod> -- sh
```

Mental model:

```text
Your Terminal
     ↓
kubectl exec
     ↓
Pod
     ↓
Container Shell
```

---

# 25. Pod Lifecycle

Important Pod phases:

```text
Pending
Running
Succeeded
Failed
Unknown
```

## Pending

Pod has been accepted but has not started running yet.

```text
Created
   ↓
Pending
```

## Running

The Pod has started and containers are running.

## Succeeded

Containers completed successfully.

Useful for workloads that are expected to finish.

## Failed

Containers completed but one or more failed.

## Unknown

Kubernetes cannot determine the current state of the Pod.

---

# 26. Delete a Pod

Command:

```bash
kubectl delete pod flask-pod
```

If the Pod was created directly:

```text
Pod
 ↓
Delete
 ↓
Pod disappears
```

There is no ReplicaSet/Deployment responsible for recreating it.

This is an important reason why production workloads are generally managed through higher-level workload objects.

---

# 27. Labels

Labels are key-value metadata attached to Kubernetes objects.

Example:

```yaml
metadata:
  labels:
    app: backend
```

This gives the Pod:

```text
app=backend
```

Think:

```text
Label = Tag / Identity
```

Example:

```text
Pod A
app=backend

Pod B
app=backend

Pod C
app=frontend
```

---

# 28. Selectors

A selector is used to find resources based on labels.

Example:

```yaml
matchLabels:
  app: backend
```

Meaning:

> Find resources whose label is `app=backend`.

Mental model:

```text
Label
  ↓
"Who am I?"

Selector
  ↓
"Find resources matching this label."
```

---

# 29. Labels + Selectors

Suppose:

```text
Pod A
app=backend

Pod B
app=backend

Pod C
app=frontend
```

Selector:

```yaml
matchLabels:
  app: backend
```

Matches:

```text
Pod A
Pod B
```

Does not match:

```text
Pod C
```

Therefore:

```text
LABEL    = tag
SELECTOR = filter
```

This relationship becomes very important with ReplicaSets and Deployments.

---

# 30. ReplicaSet

A ReplicaSet maintains a specified number of matching Pods.

Suppose:

```yaml
replicas: 3
```

Desired state:

```text
3 Pods
```

ReplicaSet works to maintain:

```text
Pod
Pod
Pod
```

Mental model:

```text
ReplicaSet
    │
    ├── Pod
    ├── Pod
    └── Pod
```

### Main responsibility

```text
ReplicaSet =
"Keep the desired number of matching Pods running."
```

---

# 31. ReplicaSet Self-Healing

Suppose:

```text
ReplicaSet

Pod A
Pod B
Pod C
```

One Pod gets deleted:

```text
Pod A
Pod C
```

Now:

```text
Desired = 3
Actual  = 2
```

ReplicaSet notices the mismatch.

It creates another Pod:

```text
Pod A
Pod C
Pod D
```

Now:

```text
Desired = 3
Actual  = 3
```

This is an example of Kubernetes reconciliation.

---

# 32. Deployment

A Deployment is a higher-level workload object used to manage application Pods and their ReplicaSets.

The important relationship is:

```text
Deployment
     ↓
ReplicaSet
     ↓
Pods
     ↓
Containers
```

Deployment allows us to manage:

```text
Desired replicas
Rolling updates
Rollbacks
Application versions
```

---

# 33. Basic Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-app

spec:
  replicas: 3

  selector:
    matchLabels:
      app: my-app

  template:
    metadata:
      labels:
        app: my-app

    spec:
      containers:
        - name: my-app
          image: myapp:v1
```

---

# 34. Understanding the Deployment YAML

## `replicas`

```yaml
replicas: 3
```

Means:

```text
Desired number of Pods = 3
```

---

## `selector`

```yaml
selector:
  matchLabels:
    app: my-app
```

Tells the Deployment which Pods it manages.

---

## `template`

```yaml
template:
  metadata:
    labels:
      app: my-app
```

Defines the template used to create Pods.

---

## Container

```yaml
containers:
  - name: my-app
    image: myapp:v1
```

Defines the container that runs inside the Pod.

---

# 35. Deployment → ReplicaSet → Pods

Suppose:

```yaml
replicas: 3
```

Kubernetes maintains:

```text
Deployment
     ↓
ReplicaSet
     ↓
+-----------+-----------+-----------+
|           |           |           |
↓           ↓           ↓
Pod 1       Pod 2       Pod 3
|           |           |
↓           ↓           ↓
Container   Container   Container
```

This is one of the most important diagrams in Module 1.

---

# 36. Pod Template

A Deployment contains a Pod template:

```yaml
template:
  metadata:
    labels:
      app: my-app

  spec:
    containers:
      - name: my-app
        image: myapp:v1
```

It tells Kubernetes:

> "When creating Pods for this Deployment, use this definition."

Mental model:

```text
Deployment
    ↓
Pod Template
    ↓
Creates Pods
```

---

# 37. Scaling

Scaling means changing the desired number of replicas.

Suppose:

```text
replicas = 3
```

Current state:

```text
Pod 1
Pod 2
Pod 3
```

Scale to 5:

```bash
kubectl scale deployment my-app --replicas=5
```

Now:

```text
Pod 1
Pod 2
Pod 3
Pod 4
Pod 5
```

---

# 38. Scaling Down

Scale from 5 to 2:

```bash
kubectl scale deployment my-app --replicas=2
```

Desired state becomes:

```text
2 Pods
```

Kubernetes removes Pods until the actual state matches the desired state.

```text
5 Pods
  ↓
Scaling
  ↓
2 Pods
```

---

# 39. Rolling Updates

Suppose the current application version is:

```text
myapp:v1
```

We release:

```text
myapp:v2
```

Instead of immediately replacing everything, a Deployment can perform a **rolling update**.

Conceptually:

```text
v1   v1   v1
 ↓
v2   v1   v1
 ↓
v2   v2   v1
 ↓
v2   v2   v2
```

The old Pods are gradually replaced by Pods using the new version.

### Remember

```text
Rolling Update =
Gradually replace old application Pods with new ones.
```

---

# 40. Old and New ReplicaSets

During a Deployment update, different ReplicaSets can exist.

Conceptually:

```text
Deployment
    |
    +---- New ReplicaSet
    |       |
    |      v2 Pods
    |
    +---- Old ReplicaSet
            |
           v1 Pods
```

As the rollout progresses:

```text
New ReplicaSet
    ↑
Pods increase

Old ReplicaSet
    ↓
Pods decrease
```

Eventually the new version becomes active and the old ReplicaSet is scaled down.

---

# 41. Watching a Rollout

Command:

```bash
kubectl rollout status deployment/my-app
```

Purpose:

> Monitor the progress of a Deployment rollout.

You can also watch Pods:

```bash
kubectl get pods -w
```

---

# 42. Rollout History

Command:

```bash
kubectl rollout history deployment/my-app
```

This allows you to inspect Deployment revisions.

Conceptually:

```text
Revision 1 → v1
Revision 2 → v2
Revision 3 → v3
```

---

# 43. Rollback

Suppose:

```text
v1 = previous version
v2 = newly deployed version
```

After deploying v2, something goes wrong.

We can undo the rollout:

```bash
kubectl rollout undo deployment/my-app
```

Conceptually:

```text
v1
 ↓
v2
 ↓
Problem
 ↓
Rollback
 ↓
v1
```

### Remember

```text
Rollback =
Return the Deployment to a previous revision.
```

---

# 44. Complete Deployment Lifecycle

The complete flow is:

```text
Create Deployment
        ↓
Deployment creates/manages ReplicaSet
        ↓
ReplicaSet creates Pods
        ↓
Pods run Containers
        ↓
Application runs
```

If a Pod dies:

```text
Pod dies
   ↓
ReplicaSet detects fewer replicas
   ↓
Replacement Pod
   ↓
Desired state restored
```

If we scale:

```text
replicas: 3
   ↓
replicas: 5
   ↓
More Pods created
```

If we update:

```text
v1
 ↓
v2
 ↓
Rolling Update
```

If the update has a problem:

```text
v2
 ↓
Rollback
 ↓
Previous revision
```

---

# 45. Complete Kubernetes Module 1 Architecture

```text
                         KUBERNETES CLUSTER
                                |
                +---------------+---------------+
                |                               |
          CONTROL PLANE                    WORKER NODE
                |                               |
        +-------+--------+                      |
        |       |        |                   kubelet
        |       |        |                      |
   API Server  etcd  Scheduler                  |
        |              |                        |
        |        Controller Manager              |
        |                                       |
        +---------------------------------------+
                        |
                    Workloads
                        |
                   Deployment
                        |
                   ReplicaSet
                        |
              +---------+---------+
              |         |         |
              ↓         ↓         ↓
            Pod       Pod       Pod
              |         |         |
          Container Container Container
              |         |         |
              +---------+---------+
                        |
                   Application
```

And:

```text
kubectl
   ↓
API Server
   ↓
Kubernetes
```

---

# 46. The Most Important Chain

Memorize this:

```text
kubectl
   ↓
API Server
   ↓
Deployment
   ↓
ReplicaSet
   ↓
Pod
   ↓
Container
   ↓
Application
```

This is the backbone of Module 1.

---

# 47. What Happens When a Pod Dies?

Example:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod A
Pod B
Pod C
```

Pod B dies:

```text
Pod A
Pod C
```

Actual:

```text
2 Pods
```

Desired:

```text
3 Pods
```

ReplicaSet reconciles:

```text
Actual != Desired
       ↓
Create replacement
       ↓
Pod D
```

Final:

```text
Pod A
Pod C
Pod D
```

Again:

```text
Desired = 3
Actual  = 3
```

---

# 48. What Happens During Scaling?

Initial:

```text
Deployment
    ↓
replicas = 3
    ↓
3 Pods
```

Command:

```bash
kubectl scale deployment my-app --replicas=5
```

Then:

```text
Deployment
    ↓
replicas = 5
    ↓
ReplicaSet
    ↓
5 Pods
```

---

# 49. What Happens During an Update?

Initial:

```text
Deployment
    ↓
ReplicaSet
    ↓
v1 Pods
```

Update:

```text
v1 → v2
```

Kubernetes creates/manages the new revision:

```text
Deployment
    |
    +---- New ReplicaSet
    |        |
    |       v2 Pods
    |
    +---- Old ReplicaSet
             |
            v1 Pods
```

During the rolling update:

```text
v1 v1 v1
 ↓
v2 v1 v1
 ↓
v2 v2 v1
 ↓
v2 v2 v2
```

---

# 50. Important Command Cheat Sheet

## Cluster

```bash
kubectl version
kubectl cluster-info
kubectl get nodes
```

## Pods

```bash
kubectl get pods
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec -it <pod-name> -- sh
kubectl delete pod <pod-name>
```

## Apply / Delete YAML

```bash
kubectl apply -f <file>.yaml
kubectl delete -f <file>.yaml
```

## Deployments

```bash
kubectl get deployments
kubectl describe deployment <deployment-name>
```

## ReplicaSets

```bash
kubectl get rs
```

## Scaling

```bash
kubectl scale deployment <deployment-name> --replicas=5
```

## Rollouts

```bash
kubectl rollout status deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name>
kubectl rollout undo deployment/<deployment-name>
```

## Watch resources

```bash
kubectl get pods -w
```

---

# 51. Important Differences

## Pod vs Container

```text
Container
    ↓
Runs application

Pod
    ↓
Kubernetes unit containing one or more containers
```

---

## Pod vs ReplicaSet

```text
Pod
    ↓
Runs workload

ReplicaSet
    ↓
Maintains desired number of Pods
```

---

## ReplicaSet vs Deployment

```text
ReplicaSet
    ↓
Maintains Pods

Deployment
    ↓
Manages ReplicaSets
    ↓
Supports application updates and rollbacks
```

---

## Label vs Selector

```text
Label
    ↓
Tag / identity

Selector
    ↓
Find/filter using labels
```

---

## `kubectl get` vs `kubectl describe`

```text
get
 ↓
Quick overview

describe
 ↓
Detailed information
```

---

# 52. Common Mental Mistakes

## Mistake 1

Thinking:

```text
Kubernetes → Container
```

Better:

```text
Kubernetes
    ↓
Pod
    ↓
Container
```

---

## Mistake 2

Thinking a Deployment directly runs containers.

Better:

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod
    ↓
Container
```

---

## Mistake 3

Thinking `replicas: 3` means:

> "Run this command three times."

It actually means:

> **"The desired state contains three replicas."**

---

## Mistake 4

Thinking labels and selectors are the same thing.

They aren't.

```text
Label = information attached to object

Selector = mechanism used to find matching objects
```

---

## Mistake 5

Thinking Kubernetes only creates things once.

Kubernetes is continuously reconciling:

```text
Desired State
      ↕
Actual State
```

---

# 53. Hands-On Practice

Create a folder:

```text
module-06/
│
├── pod.yaml
├── deployment.yaml
└── README.md
```

---

## Part 1 — Create a Pod

Create:

```text
pod.yaml
```

Apply:

```bash
kubectl apply -f pod.yaml
```

Check:

```bash
kubectl get pods
```

Inspect:

```bash
kubectl describe pod <pod-name>
```

Check logs:

```bash
kubectl logs <pod-name>
```

Enter container:

```bash
kubectl exec -it <pod-name> -- sh
```

Delete:

```bash
kubectl delete pod <pod-name>
```

---

# 54. Part 2 — Create a Deployment

Create:

```text
deployment.yaml
```

Start with:

```yaml
replicas: 3
```

Apply:

```bash
kubectl apply -f deployment.yaml
```

Check:

```bash
kubectl get deployments
kubectl get rs
kubectl get pods
```

Expected relationship:

```text
Deployment
    ↓
ReplicaSet
    ↓
3 Pods
```

---

# 55. Part 3 — Test Self-Healing

Find Pods:

```bash
kubectl get pods
```

Delete one:

```bash
kubectl delete pod <pod-name>
```

Immediately check:

```bash
kubectl get pods
```

Observe:

```text
Old Pod deleted
      ↓
ReplicaSet notices
      ↓
Replacement Pod created
```

---

# 56. Part 4 — Test Scaling

Scale:

```bash
kubectl scale deployment my-app --replicas=5
```

Check:

```bash
kubectl get pods
```

Then scale down:

```bash
kubectl scale deployment my-app --replicas=2
```

Check again:

```bash
kubectl get pods
```

Observe:

```text
3 → 5 → 2
```

---

# 57. Part 5 — Test Rolling Update

Start with:

```text
myapp:v1
```

Change the Deployment image to:

```text
myapp:v2
```

Apply:

```bash
kubectl apply -f deployment.yaml
```

Watch:

```bash
kubectl get pods -w
```

Check rollout:

```bash
kubectl rollout status deployment/my-app
```

---

# 58. Part 6 — Test Rollback

Check history:

```bash
kubectl rollout history deployment/my-app
```

Rollback:

```bash
kubectl rollout undo deployment/my-app
```

Check:

```bash
kubectl rollout status deployment/my-app
```

---

# 59. Module 1 Revision Sheet

## Architecture

```text
Cluster
├── Control Plane
└── Worker Nodes
```

## Control Plane

```text
API Server
    = Kubernetes API entry point

etcd
    = Cluster state store

Scheduler
    = Decides where Pods run

Controller Manager
    = Reconciles desired and actual state
```

## Worker Node

```text
kubelet
    = Node-level Pod agent

Container Runtime
    = Runs containers

Pods
    = Run workloads
```

---

## Workload Hierarchy

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod
    ↓
Container
```

---

## Desired State

```text
Desired State
      ↓
Kubernetes
      ↓
Actual State
      ↓
Reconciliation
      ↓
Desired State achieved
```

---

## Labels

```text
Label
= Tag / identity
```

## Selectors

```text
Selector
= Filter/search using labels
```

---

## Scaling

```text
replicas: 3
     ↓
3 Pods

replicas: 5
     ↓
5 Pods
```

---

## Rolling Update

```text
v1
 ↓
v2

Gradually replace old Pods with new Pods.
```

---

## Rollback

```text
v2
 ↓
Previous revision
```

---

# 60. Module 1 — Final Mental Model

If you remember only one diagram, remember this:

```text
                         USER
                           |
                        kubectl
                           |
                           ↓
                     API SERVER
                           |
             +-------------+-------------+
             |             |             |
            etcd       Scheduler    Controllers
             |
             |
             ↓
        Desired State
             |
             ↓
        DEPLOYMENT
             |
             ↓
        REPLICASET
             |
       +-----+-----+
       |     |     |
       ↓     ↓     ↓
      POD   POD   POD
       |     |     |
       ↓     ↓     ↓
    CONTAINER CONTAINER CONTAINER
       |     |     |
       +-----+-----+
             |
        APPLICATION
```

The core Kubernetes idea is:

```text
"I declare what I want.
Kubernetes continuously works
to make reality match that declaration."
```

---

# 61. Module 1 Checklist

## Concepts

* [ ] Kubernetes Cluster
* [ ] Control Plane
* [ ] Worker Node
* [ ] API Server
* [ ] etcd
* [ ] Scheduler
* [ ] Controller Manager
* [ ] kubelet
* [ ] Container Runtime
* [ ] kubectl
* [ ] Kubernetes Objects
* [ ] YAML manifests
* [ ] Declarative configuration
* [ ] Desired State
* [ ] Reconciliation
* [ ] Namespace — basic idea

## Pods

* [ ] What is a Pod?
* [ ] Pod vs Container
* [ ] Pod lifecycle
* [ ] Pending
* [ ] Running
* [ ] Succeeded
* [ ] Failed
* [ ] Unknown
* [ ] `kubectl get pods`
* [ ] `kubectl describe`
* [ ] `kubectl logs`
* [ ] `kubectl exec`
* [ ] Delete Pod

## Labels & Selectors

* [ ] Labels
* [ ] Selectors
* [ ] Label → Selector relationship

## ReplicaSets

* [ ] What is a ReplicaSet?
* [ ] Desired replica count
* [ ] Self-healing
* [ ] Pod replacement

## Deployments

* [ ] What is a Deployment?
* [ ] Deployment → ReplicaSet → Pod relationship
* [ ] Pod template
* [ ] Deployment YAML
* [ ] Scaling
* [ ] Rolling updates
* [ ] Rollout status
* [ ] Rollout history
* [ ] Rollback

## Hands-On

* [ ] Create Pod
* [ ] Inspect Pod
* [ ] Read logs
* [ ] Execute inside Pod
* [ ] Delete Pod
* [ ] Create Deployment
* [ ] Scale 3 → 5
* [ ] Scale 5 → 2
* [ ] Delete a managed Pod
* [ ] Observe replacement
* [ ] Perform rolling update
* [ ] Check rollout status
* [ ] Check rollout history
* [ ] Perform rollback

---

# 62. Module 1 — One-Line Summary

> **Kubernetes uses a declarative desired-state model where Deployments manage ReplicaSets, ReplicaSets maintain Pods, and Pods run containers; Kubernetes continuously reconciles the actual state with the desired state and provides scaling, rolling updates, and rollbacks.**

---

# 63. Scope Boundary

This README intentionally stops here.

### NOT part of this module:

```text
Services
ClusterIP
NodePort
LoadBalancer
Ingress
Ingress Controller
DNS
ConfigMaps
Secrets
Persistent Volumes
PVCs
StorageClasses
Health Probes
HPA
RBAC
StatefulSets
DaemonSets
Jobs
CronJobs
Helm
```

These belong to later modules and should be studied separately.

---

