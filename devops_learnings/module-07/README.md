# Kubernetes Module 06 — Pod & Deployment Hands-On

> **Project:** Task Manager Application
> **Hands-on focus:** Kubernetes Pods, Pod YAML, Deployments, ReplicaSets, scaling, self-healing, rollout revisions, rolling updates, and rollback
> **Environment:** Windows + Docker + Minikube + kubectl

---

# 1. Goal of This Hands-On

The goal of this practical was to take the **existing Dockerized Task Manager backend** and deploy it using Kubernetes.

Instead of using a random demo application, we used the actual backend from our Task Manager project.

We started with:

```text
Task Manager Backend
        ↓
Dockerfile
        ↓
Docker Image
        ↓
Kubernetes Pod
        ↓
Kubernetes Deployment
        ↓
ReplicaSet
        ↓
Multiple Pods
        ↓
Scaling
        ↓
Rolling Update
        ↓
Rollback
```

We intentionally did **not** use Kubernetes Services, Ingress, ConfigMaps, Secrets, MySQL, or Redis in this hands-on.

---

# 2. Existing Project

The project already had Docker configuration from the previous Docker hands-on.

Relevant structure:

```text
task_manager/
│
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   └── ...
│
├── compose.yaml
│
└── k8s/
```

For this Kubernetes practical, we started with **only the backend**.

---

# 3. Existing Backend Dockerfile

The backend already had a working Dockerfile:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The important point:

> Kubernetes does not replace Docker.

Kubernetes uses container images.

Our flow was:

```text
Dockerfile
    ↓
Docker Image
    ↓
Kubernetes
    ↓
Pod
    ↓
Container
```

---

# 4. Build the Backend Image

We built the backend image:

```powershell
docker build -t task-manager-backend:v1 ./backend
```

Then verified it:

```powershell
docker images
```

We found:

```text
task-manager-backend:v1
```

---

# 5. Test the Docker Image First

Before involving Kubernetes, we verified that the Docker image itself worked.

```powershell
docker run --rm -p 8000:8000 task-manager-backend:v1
```

Then we opened:

```text
http://localhost:8000/docs
```

This showed the FastAPI Swagger UI.

This confirmed:

```text
Docker image
      ↓
Container
      ↓
FastAPI
      ↓
Port 8000
```

was working correctly.

---

# 6. Minikube and Local Images

We were using **Minikube**.

A key issue appeared because:

```text
task-manager-backend:v1
```

existed in our Docker environment, but Kubernetes was running inside Minikube.

Therefore, Minikube did not automatically have the image available.

We loaded the image into Minikube:

```powershell
minikube image load task-manager-backend:v1
```

This gave us:

```text
Docker image
     ↓
Minikube image environment
```

For local Kubernetes development, this is important.

---

# 7. First Kubernetes Resource — Pod

We created:

```text
k8s/backend-pod.yaml
```

Final version:

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: task-manager-backend

spec:
  containers:
    - name: backend
      image: task-manager-backend:v1
      imagePullPolicy: IfNotPresent

      ports:
        - containerPort: 8000
```

---

# 8. Understanding the Pod YAML

## `apiVersion`

```yaml
apiVersion: v1
```

Specifies the Kubernetes API version used by the Pod resource.

---

## `kind`

```yaml
kind: Pod
```

Tells Kubernetes what type of object we want.

Important:

Kubernetes resource kinds are case-sensitive.

Correct:

```yaml
kind: Pod
```

Incorrect:

```yaml
kind: pod
```

---

## `metadata`

```yaml
metadata:
  name: task-manager-backend
```

Gives the Pod its name.

We can later use this name:

```powershell
kubectl get pod task-manager-backend
```

---

## `spec`

```yaml
spec:
```

Defines the desired configuration of the Pod.

---

## `containers`

```yaml
containers:
  - name: backend
```

Defines the container that should run inside the Pod.

---

## `image`

```yaml
image: task-manager-backend:v1
```

Tells Kubernetes which container image to use.

---

## `imagePullPolicy`

```yaml
imagePullPolicy: IfNotPresent
```

Means:

> If the image already exists on the Kubernetes node, use it. Otherwise, try to pull it.

This was useful because we loaded the image into Minikube.

---

## `containerPort`

```yaml
ports:
  - containerPort: 8000
```

Documents that the containerized application listens on port `8000`.

Important:

`containerPort` does **not** expose the application to our Windows machine.

---

# 9. Error 1 — `kind: pod`

Initially, Kubernetes returned:

```text
no kind "pod" is registered for version "v1"
```

The issue was:

```yaml
kind: pod
```

Instead of:

```yaml
kind: Pod
```

### Lesson

Kubernetes resource kinds are case-sensitive.

```yaml
Pod
Deployment
Service
```

are different from:

```yaml
pod
deployment
service
```

---

# 10. Error 2 — Incorrect Container Indentation

We then had:

```yaml
containers:
  - name: backend
  - image: task-manager-backend:v1
```

This accidentally created the structure:

```text
Container 1
    name = backend
    image = missing

Container 2
    name = missing
    image = task-manager-backend:v1
```

Kubernetes reported:

```text
spec.containers[0].image: Required value
spec.containers[1].name: Required value
```

### Correct structure

```yaml
containers:
  - name: backend
    image: task-manager-backend:v1
```

There should be only one `-` because there is only one container.

---

# 11. Creating the Pod

Once the YAML was fixed:

```powershell
kubectl apply -f k8s/backend-pod.yaml
```

Kubernetes returned:

```text
pod/task-manager-backend created
```

We checked:

```powershell
kubectl get pods
```

Eventually:

```text
NAME                   READY   STATUS    RESTARTS   AGE
task-manager-backend   1/1     Running   0          ...
```

Our Docker container was now running inside a Kubernetes Pod.

---

# 12. Inspecting the Pod

We used:

```powershell
kubectl describe pod task-manager-backend
```

This lets us inspect information such as:

```text
Name
Namespace
Status
IP
Containers
Image
Ports
Events
```

This is one of the main debugging commands for Pods.

---

# 13. Viewing Pod Logs

We used:

```powershell
kubectl logs task-manager-backend
```

This allowed us to see the application/Uvicorn logs from the container.

The important idea:

```text
kubectl logs
      ↓
Pod
      ↓
Container
      ↓
Application logs
```

---

# 14. Accessing the Pod With Port Forwarding

The Pod had:

```yaml
containerPort: 8000
```

but that does not mean:

```text
localhost:8000
```

is automatically exposed.

For this hands-on we used:

```powershell
kubectl port-forward pod/task-manager-backend 8000:8000
```

Then:

```text
http://localhost:8000/docs
```

worked.

The traffic flow was:

```text
Browser
   ↓
localhost:8000
   ↓
kubectl port-forward
   ↓
Kubernetes Pod
   ↓
Backend container
   ↓
FastAPI
```

Port forwarding was used only for this local experiment.

---

# 15. Testing the Real Application

We opened:

```text
http://localhost:8000/docs
```

and used the actual FastAPI endpoints.

For example, we created a task and retrieved tasks through the API.

This proved that:

```text
Task Manager Backend
        ↓
Docker Image
        ↓
Kubernetes Pod
        ↓
FastAPI
        ↓
API
```

was working.

---

# 16. Why a Pod Alone Is Not Enough

We deleted the Pod:

```powershell
kubectl delete pod task-manager-backend
```

Then:

```powershell
kubectl get pods
```

The Pod was gone.

Nothing recreated it.

This demonstrated an important limitation:

```text
Pod deleted
    ↓
No controller
    ↓
Nothing recreates it
```

A standalone Pod does not provide the Deployment-style management we wanted.

This led to the next practical: **Deployment**.

---

# 17. Deployment

We created:

```text
k8s/backend-deployment.yaml
```

Final version:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: task-manager-backend

spec:
  replicas: 2

  selector:
    matchLabels:
      app: task-manager-backend

  template:
    metadata:
      labels:
        app: task-manager-backend

    spec:
      containers:
        - name: backend
          image: task-manager-backend:v1
          imagePullPolicy: IfNotPresent

          ports:
            - containerPort: 8000
```

---

# 18. Deployment YAML Explained

## `apiVersion`

```yaml
apiVersion: apps/v1
```

The Deployment resource uses the `apps/v1` API.

---

## `kind`

```yaml
kind: Deployment
```

Tells Kubernetes that we want a Deployment.

---

## `metadata`

```yaml
metadata:
  name: task-manager-backend
```

The Deployment's name.

---

# 19. `replicas`

```yaml
replicas: 2
```

This tells the Deployment:

> Maintain two Pods matching the Deployment's Pod template.

Therefore:

```text
Deployment
    ↓
2 desired Pods
```

---

# 20. Selector

```yaml
selector:
  matchLabels:
    app: task-manager-backend
```

The Deployment uses this label to identify the Pods it manages.

---

# 21. Pod Template

The Deployment contains a Pod template:

```yaml
template:
  metadata:
    labels:
      app: task-manager-backend
```

This label matches:

```yaml
selector:
  matchLabels:
    app: task-manager-backend
```

So:

```text
Deployment selector
        ↓
find/manage Pods
        ↓
matching label
```

---

# 22. Deployment → ReplicaSet → Pods

This was one of the most important things we observed.

The relationship is:

```text
Deployment
     ↓
ReplicaSet
     ↓
Pods
     ↓
Containers
```

More specifically:

```text
Task Manager Backend Deployment
             ↓
        ReplicaSet
             ↓
      ┌──────┴──────┐
      ↓             ↓
    Pod 1         Pod 2
      ↓             ↓
 Container       Container
```

The Deployment does not directly manage the individual containers.

It manages the desired state through a ReplicaSet.

---

# 23. Creating the Deployment

We ran:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
```

Kubernetes created the Deployment.

We then inspected it using:

```powershell
kubectl get deployments
```

Then:

```powershell
kubectl get replicasets
```

Then:

```powershell
kubectl get pods
```

This allowed us to observe the complete hierarchy.

---

# 24. Deployment Error — Incorrect `ports` Indentation

We initially wrote:

```yaml
containers:
  - name: backend
    image: task-manager-backend:v1
    imagePullPolicy: IfNotPresent

  - ports:
      containerPort: 8000
```

This again accidentally created a second container.

Kubernetes returned:

```text
json: cannot unmarshal object into Go struct field
Container.spec.template.spec.containers.ports
of type []v1.ContainerPort
```

The problem was the extra `-`.

### Incorrect

```yaml
containers:
  - name: backend
    image: ...
  - ports:
```

### Correct

```yaml
containers:
  - name: backend
    image: ...
    ports:
      - containerPort: 8000
```

The two levels of lists are important:

```text
containers:
  - container
      ports:
        - port
```

---

# 25. Scaling the Deployment

Our Deployment initially used:

```yaml
replicas: 2
```

This meant Kubernetes maintained two Pods.

We also experimented with changing the number of replicas.

For example:

```yaml
replicas: 3
```

Then:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
```

We could observe multiple Pods:

```text
task-manager-backend-xxxxx
task-manager-backend-yyyyy
task-manager-backend-zzzzz
```

---

# 26. Scaling With `kubectl`

We also learned that replicas can be changed directly from the command line.

Scale up:

```powershell
kubectl scale deployment task-manager-backend --replicas=5
```

Scale down:

```powershell
kubectl scale deployment task-manager-backend --replicas=2
```

Then:

```powershell
kubectl get pods
```

shows the change.

The important idea:

```text
Desired replicas = 5
        ↓
Kubernetes creates Pods
        ↓
5 Pods running
```

---

# 27. Self-Healing / Reconciliation Experiment

This was one of the most useful experiments.

We had a Deployment managing multiple Pods.

We deleted one Pod manually:

```powershell
kubectl delete pod <pod-name>
```

Then immediately checked:

```powershell
kubectl get pods
```

Kubernetes created a replacement Pod.

The reason:

```text
Deployment
    ↓
ReplicaSet
    ↓
Desired state = 2 Pods
```

If one disappears:

```text
Actual state = 1 Pod
Desired state = 2 Pods
```

The ReplicaSet detects the difference and creates another Pod.

Therefore:

```text
Pod deleted
      ↓
ReplicaSet notices
      ↓
New Pod created
      ↓
Desired number restored
```

This is the practical demonstration of **reconciliation**.

---

# 28. Desired State

The Deployment YAML describes the desired state.

For example:

```yaml
replicas: 2
```

means:

```text
I want 2 Pods.
```

Kubernetes continuously works toward:

```text
Desired State = Actual State
```

Example:

```text
Desired = 2
Actual  = 1
        ↓
Kubernetes creates another Pod
        ↓
Desired = 2
Actual  = 2
```

---

# 29. Deployment Revision

A Deployment can maintain rollout revisions.

We checked them using:

```powershell
kubectl rollout history deployment/task-manager-backend
```

At one point we had revisions such as:

```text
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
```

A revision represents a stored version of the Deployment's Pod template.

---

# 30. Docker Image Version vs Deployment Revision

These are different concepts.

## Docker image version

We had:

```text
task-manager-backend:v1
```

and then created:

```text
task-manager-backend:v2
```

These are Docker image tags.

---

## Deployment revision

Kubernetes separately maintains rollout revisions:

```text
Revision 2
Revision 3
```

For example:

```text
Revision 2
    ↓
task-manager-backend:v2

Revision 3
    ↓
task-manager-backend:v1
```

So:

```text
Docker image tag
        ≠
Deployment revision
```

The image version is part of the Pod template.

Changing the Pod template causes a new Deployment revision.

---

# 31. Viewing a Specific Revision

We used:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=2
```

It showed:

```text
Pod Template:
  Labels:
    app=task-manager-backend

  Containers:
   backend:
    Image: task-manager-backend:v2
    Port: 8000/TCP
```

This let us inspect exactly which image belonged to that revision.

---

# 32. Revision 3

We also inspected:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=3
```

It showed:

```text
Containers:
 backend:
   Image: task-manager-backend:v1
   Port: 8000/TCP
```

Therefore we could see:

```text
Revision 2 → v2
Revision 3 → v1
```

---

# 33. Why Revision 1 Was Not Available

We tried:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=1
```

and Kubernetes returned:

```text
error: unable to find the specified revision
```

This happened because Revision 1 was no longer available in the Deployment's retained rollout history.

The important practical lesson is:

> Do not assume every old revision will always remain available.

The Deployment keeps rollout history according to its revision/history retention behavior.

---

# 34. Rolling Update

We changed the backend image from:

```yaml
image: task-manager-backend:v1
```

to:

```yaml
image: task-manager-backend:v2
```

and applied the Deployment:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
```

Kubernetes detected that the Pod template had changed.

That created a new ReplicaSet and started a new rollout.

We could monitor it using:

```powershell
kubectl rollout status deployment/task-manager-backend
```

The basic idea was:

```text
Old Deployment version
        ↓
v1 Pods
        ↓
Deployment updated
        ↓
New ReplicaSet
        ↓
v2 Pods
        ↓
Old Pods gradually replaced
```

This is a **RollingUpdate**.

---

# 35. Rollout Status

We used:

```powershell
kubectl rollout status deployment/task-manager-backend
```

This lets us watch the progress of the Deployment rollout.

At one point it reported:

```text
Waiting for deployment "task-manager-backend" rollout to finish:
1 out of 3 new replicas have been updated...
```

Instead of blindly waiting, we inspected the Deployment, ReplicaSets, and Pods.

Useful commands for this situation:

```powershell
kubectl get deployment task-manager-backend
```

```powershell
kubectl get pods
```

```powershell
kubectl get replicasets
```

```powershell
kubectl describe deployment task-manager-backend
```

---

# 36. Rollback

We then tested rollback:

```powershell
kubectl rollout undo deployment/task-manager-backend
```

Kubernetes responded:

```text
deployment.apps/task-manager-backend rolled back
```

This moved the Deployment back to the previous available revision.

---

# 37. After Rollback

We checked:

```powershell
kubectl rollout history deployment/task-manager-backend
```

and saw:

```text
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
```

Then:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=2
```

showed:

```text
Image: task-manager-backend:v2
```

while:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=3
```

showed:

```text
Image: task-manager-backend:v1
```

So the practical history became:

```text
Revision 2
    ↓
task-manager-backend:v2
    ↓
Rollback
    ↓
Revision 3
    ↓
task-manager-backend:v1
```

---

# 38. Complete Architecture We Observed

The practical relationship can now be represented as:

```text
                 Deployment
                     │
                     │ manages
                     ↓
                 ReplicaSet
                     │
              creates/manages
                     ↓
             ┌───────┴───────┐
             ↓               ↓
           Pod 1           Pod 2
             │               │
             ↓               ↓
        Backend          Backend
        Container        Container
             │               │
             └───────┬───────┘
                     ↓
              Docker Image
```

When the image changes:

```text
Deployment
    │
    ├── Old ReplicaSet
    │       ↓
    │      v1 Pods
    │
    └── New ReplicaSet
            ↓
           v2 Pods
```

During rollback:

```text
v2
 ↓
rollback
 ↓
v1
```

---

# 39. Important Kubernetes Terms

## Pod

The smallest deployable unit in Kubernetes.

A Pod can contain one or more containers.

In our hands-on:

```text
Pod
 ↓
Backend container
```

---

## Container

The actual application container running from our Docker image.

Our container used:

```text
task-manager-backend:v1
```

or:

```text
task-manager-backend:v2
```

---

## Deployment

A Kubernetes controller used to manage application Pods and maintain the desired state.

In our project:

```text
Deployment
 ↓
ReplicaSet
 ↓
Pods
```

It allowed us to:

* Maintain replicas
* Scale
* Replace deleted Pods
* Perform rolling updates
* Roll back versions

---

## ReplicaSet

A controller responsible for maintaining the desired number of matching Pods.

Example:

```text
replicas: 2
```

means the ReplicaSet works toward:

```text
2 matching Pods
```

---

## Replica

A desired copy of a Pod.

Example:

```yaml
replicas: 3
```

means:

```text
3 desired Pod instances
```

---

## Label

A key-value pair attached to Kubernetes objects.

Our label:

```yaml
app: task-manager-backend
```

---

## Selector

Defines which Pods a Deployment manages.

Our selector:

```yaml
selector:
  matchLabels:
    app: task-manager-backend
```

It matches Pods having:

```yaml
app: task-manager-backend
```

---

## Desired State

What we declare that we want Kubernetes to maintain.

Example:

```yaml
replicas: 2
```

---

## Actual State

What is currently running in the cluster.

Example:

```text
Desired = 2
Actual  = 1
```

Kubernetes works to make:

```text
Desired = Actual
```

---

## Reconciliation

The continuous process of comparing desired state with actual state and taking action when they differ.

Example:

```text
Desired = 2 Pods
Actual = 1 Pod

        ↓

ReplicaSet creates another Pod

        ↓

Desired = 2
Actual = 2
```

---

## Rollout

The process of changing a Deployment from one Pod template version to another.

Example:

```text
v1 → v2
```

---

## Deployment Revision

A recorded revision of the Deployment's Pod template.

Example:

```text
Revision 2 → v2
Revision 3 → v1
```

---

## Rolling Update

Gradually replacing old Pods with new Pods when the Deployment's Pod template changes.

Example:

```text
v1 Pods
   ↓
v2 rollout
   ↓
v2 Pods
```

---

## Rollback

Returning the Deployment to a previous available revision.

Command:

```powershell
kubectl rollout undo deployment/task-manager-backend
```

---

# 40. Important Commands Learned

## Pod

Create/update from YAML:

```powershell
kubectl apply -f k8s/backend-pod.yaml
```

List Pods:

```powershell
kubectl get pods
```

Inspect a Pod:

```powershell
kubectl describe pod task-manager-backend
```

View logs:

```powershell
kubectl logs task-manager-backend
```

Delete a Pod:

```powershell
kubectl delete pod task-manager-backend
```

Port forward:

```powershell
kubectl port-forward pod/task-manager-backend 8000:8000
```

---

## Deployment

Create/update:

```powershell
kubectl apply -f k8s/backend-deployment.yaml
```

List Deployments:

```powershell
kubectl get deployments
```

List ReplicaSets:

```powershell
kubectl get replicasets
```

List Pods:

```powershell
kubectl get pods
```

Inspect Deployment:

```powershell
kubectl describe deployment task-manager-backend
```

Scale:

```powershell
kubectl scale deployment task-manager-backend --replicas=5
```

Scale down:

```powershell
kubectl scale deployment task-manager-backend --replicas=2
```

Check rollout:

```powershell
kubectl rollout status deployment/task-manager-backend
```

View rollout history:

```powershell
kubectl rollout history deployment/task-manager-backend
```

View a specific revision:

```powershell
kubectl rollout history deployment/task-manager-backend --revision=2
```

Rollback:

```powershell
kubectl rollout undo deployment/task-manager-backend
```

---

# 41. Troubleshooting We Practiced

## Problem 1 — Invalid `kind`

Error:

```text
no kind "pod" is registered
```

Cause:

```yaml
kind: pod
```

Fix:

```yaml
kind: Pod
```

---

## Problem 2 — Missing Container Image

Error:

```text
spec.containers[0].image: Required value
spec.containers[1].name: Required value
```

Cause:

Incorrect YAML:

```yaml
containers:
  - name: backend
  - image: task-manager-backend:v1
```

Fix:

```yaml
containers:
  - name: backend
    image: task-manager-backend:v1
```

---

## Problem 3 — `ImagePullBackOff`

The Pod showed:

```text
ImagePullBackOff
```

Cause:

The image existed in our Docker environment but was not available inside Minikube.

Fix:

```powershell
minikube image load task-manager-backend:v1
```

---

## Problem 4 — Deployment `ports` Error

Error:

```text
cannot unmarshal object into Go struct field
Container.spec.template.spec.containers.ports
```

Cause:

Another `-` accidentally created another container:

```yaml
containers:
  - name: backend
    image: ...
  - ports:
```

Correct:

```yaml
containers:
  - name: backend
    image: ...
    ports:
      - containerPort: 8000
```

---

## Problem 5 — Rollout Appeared Stuck

We saw:

```text
Waiting for deployment "task-manager-backend" rollout to finish:
1 out of 3 new replicas have been updated...
```

Instead of assuming it was simply taking time, we inspected:

```powershell
kubectl get deployment task-manager-backend
```

```powershell
kubectl get pods
```

```powershell
kubectl get replicasets
```

```powershell
kubectl describe deployment task-manager-backend
```

This is the correct Kubernetes debugging mindset:

```text
Something is not progressing
        ↓
Inspect resources
        ↓
Inspect Pods
        ↓
Inspect ReplicaSets
        ↓
Inspect Events
        ↓
Find the actual reason
```

---

# 42. Final Hands-On Flow

The entire practical can be summarized as:

```text
Existing Task Manager Backend
          ↓
Build Docker Image
          ↓
task-manager-backend:v1
          ↓
Load image into Minikube
          ↓
Create Pod YAML
          ↓
Create Pod
          ↓
Inspect Pod
          ↓
View Logs
          ↓
Port Forward
          ↓
Test FastAPI
          ↓
Delete Pod
          ↓
Observe that it stays deleted
          ↓
Create Deployment
          ↓
Deployment creates ReplicaSet
          ↓
ReplicaSet creates Pods
          ↓
Scale replicas
          ↓
Delete a Pod
          ↓
ReplicaSet recreates it
          ↓
Build v2 image
          ↓
Update Deployment
          ↓
Rolling Update
          ↓
Deployment Revision
          ↓
Rollback
```

---

# 43. Final Mental Model

The most important thing to remember from this hands-on:

```text
Docker
  ↓
Image
  ↓
Container
```

Kubernetes adds management around those containers:

```text
Docker Image
     ↓
   Pod
     ↓
ReplicaSet
     ↓
Deployment
```

And the responsibilities are roughly:

```text
Pod
→ Runs the container(s)

ReplicaSet
→ Maintains the desired number of Pods

Deployment
→ Manages ReplicaSets and application rollouts
```

So for our Task Manager backend:

```text
Deployment
    │
    │ desired replicas = 2
    ↓
ReplicaSet
    │
    ├──────────────┐
    ↓              ↓
  Pod 1          Pod 2
    │              │
    ↓              ↓
Backend          Backend
Container        Container
    │              │
    └──────┬───────┘
           ↓
   task-manager-backend:v1
```

When we update the image:

```text
v1
 ↓
Deployment update
 ↓
New ReplicaSet
 ↓
v2 Pods
```

When a Pod disappears:

```text
Pod deleted
    ↓
ReplicaSet detects mismatch
    ↓
Replacement Pod
```

When we rollback:

```text
v2
 ↓
kubectl rollout undo
 ↓
previous available revision
 ↓
v1
```

---

# 44. Hands-On Completion Checklist

### Pod

* [x] Created Pod YAML
* [x] Understood `apiVersion`
* [x] Understood `kind`
* [x] Understood `metadata`
* [x] Understood `spec`
* [x] Defined a container
* [x] Used Docker image
* [x] Used `containerPort`
* [x] Used `imagePullPolicy`
* [x] Applied Pod YAML
* [x] Inspected Pod
* [x] Viewed logs
* [x] Used port-forwarding
* [x] Tested real FastAPI application
* [x] Deleted Pod
* [x] Observed that standalone Pod was not recreated

### Deployment

* [x] Created Deployment YAML
* [x] Defined replicas
* [x] Defined selector
* [x] Defined Pod template
* [x] Used labels
* [x] Created Deployment
* [x] Observed ReplicaSet
* [x] Observed Pods created by Deployment
* [x] Scaled Deployment
* [x] Deleted a managed Pod
* [x] Observed automatic Pod recreation

### Updates

* [x] Created `task-manager-backend:v2`
* [x] Updated Deployment image
* [x] Observed rollout
* [x] Checked rollout status
* [x] Checked rollout history
* [x] Inspected specific revisions
* [x] Performed rollback
* [x] Verified the image associated with revisions

### Debugging

* [x] Fixed lowercase `kind`
* [x] Fixed container indentation
* [x] Fixed `ports` indentation
* [x] Diagnosed `ImagePullBackOff`
* [x] Loaded image into Minikube
* [x] Investigated rollout status

---

# 45. Scope Boundary

This hands-on is complete at:

```text
Pods
    ↓
Deployments
    ↓
ReplicaSets
    ↓
Scaling
    ↓
Reconciliation
    ↓
Rolling Updates
    ↓
Rollout Revisions
    ↓
Rollback
```

The following were **not part of this hands-on**:

```text
Services
ClusterIP
NodePort
LoadBalancer
Ingress
ConfigMaps
Secrets
MySQL deployment
Redis deployment
Persistent storage
```

Those will be handled separately after the Pod + Deployment layer is fully understood.


# Repository

Task Manager repository:

``` text
https://github.com/Nandani2024-tech/task_manager_docker_compose
```
