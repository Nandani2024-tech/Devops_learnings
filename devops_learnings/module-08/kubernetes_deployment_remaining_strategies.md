# Kubernetes Deployment — Remaining Topics & Deployment Strategies

> **Status:** Deployment fundamentals and hands-on are already completed.
>
> This document covers the **remaining Deployment reading/theory portion only**:
> deployment strategies, rollout controls, important Deployment fields, and the meaning of the important commands.
>
> **No hands-on is included here.**

---

# 1. Where We Are

Already studied:

- Deployment YAML
- `replicas`
- selectors
- Pod templates
- labels
- Deployment → ReplicaSet → Pod
- scaling
- reconciliation / self-healing
- rolling updates
- rollout status
- rollout history
- Deployment revisions
- rollback

The remaining part is mainly:

```text
Deployment
│
├── Deployment strategies
│   ├── Recreate
│   └── RollingUpdate
│
├── RollingUpdate controls
│   ├── maxUnavailable
│   └── maxSurge
│
├── Release/deployment patterns
│   ├── Blue-Green
│   └── Canary
│
├── Rollout controls
│   ├── pause
│   └── resume
│
├── Deployment update commands
│
├── Revision history
│
└── Deployment status / rollout behavior
```

---

# 2. First: What Does "Deployment Strategy" Mean?

A Deployment strategy answers:

> **When I replace the old version of my application with a new version, how should Kubernetes replace the Pods?**

Suppose we have:

```text
v1
v1
v1
```

and want:

```text
v2
v2
v2
```

The strategy determines **how the transition happens**.

The Kubernetes Deployment API has two built-in strategy types:

```text
Recreate
RollingUpdate
```

`RollingUpdate` is the default. citeturn0search2turn0search0

---

# 3. Recreate Strategy

## Definition

With `Recreate`:

```text
Stop old Pods
      ↓
Old Pods are gone
      ↓
Create new Pods
```

Kubernetes terminates all existing Pods before creating the new revision's Pods during an upgrade. citeturn0search1

---

## Mental Model

Suppose:

```text
3 replicas
```

Before:

```text
v1   v1   v1
```

During Recreate:

```text
(no old Pods)
```

Then:

```text
v2   v2   v2
```

---

## YAML

```yaml
spec:
  strategy:
    type: Recreate
```

Meaning:

> Replace the old version by first removing the existing Pods.

---

## Main Advantage

Simple and predictable replacement.

---

## Main Disadvantage

There can be **downtime** because the old Pods are removed before the new Pods are available. citeturn0search3

---

## When Recreate Makes Sense

Conceptually useful when:

- old and new versions must not run simultaneously
- simultaneous versions could conflict
- downtime is acceptable
- the application cannot safely have two versions running at once

---

# 4. RollingUpdate Strategy

This is the strategy you already observed in your Task Manager hands-on.

## Definition

Instead of deleting everything at once:

```text
Old Pods
   ↓
Gradually replace
   ↓
New Pods
```

Kubernetes gradually scales down the old ReplicaSet and scales up the new ReplicaSet. citeturn0search1

---

## Mental Model

Initial:

```text
v1   v1   v1
```

Transition:

```text
v1   v1   v2
```

Then:

```text
v1   v2   v2
```

Then:

```text
v2   v2   v2
```

The exact number of Pods at each point is controlled by:

```text
maxUnavailable
maxSurge
```

---

# 5. RollingUpdate YAML

```yaml
spec:
  strategy:
    type: RollingUpdate

    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

`RollingUpdate` is the default Deployment strategy, so it does not have to be written explicitly, but defining it makes the intended behavior clear. citeturn0search2turn0search4

---

# 6. `maxUnavailable`

## Meaning

`maxUnavailable` controls:

> **How many Pods can be unavailable during the update.**

It can be:

```yaml
maxUnavailable: 1
```

or:

```yaml
maxUnavailable: 25%
```

Kubernetes allows either an absolute number or a percentage. Percentage values are rounded down for `maxUnavailable`. The default is `25%`. citeturn0search1turn0search2

---

## Example

Suppose:

```yaml
replicas: 4
```

and:

```yaml
maxUnavailable: 1
```

Then during the rollout, at most one desired Pod can be unavailable according to this rollout constraint.

Mental model:

```text
Desired = 4

Maximum unavailable = 1

So Kubernetes tries to preserve:
at least 3 available Pods
```

---

# 7. `maxSurge`

## Meaning

`maxSurge` controls:

> **How many extra Pods can temporarily exist above the desired replica count during an update.**

It can be:

```yaml
maxSurge: 1
```

or:

```yaml
maxSurge: 25%
```

Percentage values are rounded up for `maxSurge`. The default is `25%`. citeturn0search1turn0search2

---

## Example

Suppose:

```yaml
replicas: 4
```

and:

```yaml
maxSurge: 1
```

During the rollout Kubernetes may temporarily have:

```text
4 desired
+
1 extra
=
5 Pods
```

This gives Kubernetes room to start new Pods before removing old ones.

---

# 8. `maxUnavailable` vs `maxSurge`

This is extremely important.

```text
maxUnavailable
        ↓
How many existing desired Pods
can be unavailable?

maxSurge
        ↓
How many EXTRA Pods
can temporarily exist?
```

Think:

```text
maxUnavailable
    = sacrifice capacity

maxSurge
    = temporarily add capacity
```

---

# 9. Example Together

```yaml
spec:
  replicas: 4

  strategy:
    type: RollingUpdate

    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
```

Conceptually:

```text
Desired Pods = 4

Maximum unavailable = 1
Maximum extra       = 1
```

So the rollout can temporarily operate within the boundaries defined by those two values.

---

# 10. Why `maxSurge` and `maxUnavailable` Exist

Without these controls, you would have little control over the balance between:

```text
Availability
     vs
Deployment speed
     vs
Temporary resource usage
```

For example:

### More availability

Use a smaller:

```text
maxUnavailable
```

### Faster replacement / more temporary capacity

Allow a larger:

```text
maxSurge
```

But larger surge means:

```text
more Pods
→ more CPU/memory usage
```

So these are operational tuning parameters.

---

# 11. RollingUpdate Is What You Already Did

Your Task Manager experiment:

```text
task-manager-backend:v1
```

changed to:

```text
task-manager-backend:v2
```

The Deployment created a new ReplicaSet and gradually moved the workload toward the new Pod template.

Conceptually:

```text
Deployment
     │
     ├── Old ReplicaSet → v1
     │
     └── New ReplicaSet → v2
```

Eventually:

```text
Old ReplicaSet → 0 Pods
New ReplicaSet → desired Pods
```

That is a RollingUpdate.

---

# 12. Blue-Green Deployment

## Important clarification

**Blue-Green is not a separate Kubernetes `Deployment.spec.strategy.type`.**

Kubernetes itself officially supports:

```text
Recreate
RollingUpdate
```

Blue-Green is a broader **release/deployment pattern** that can be implemented using Kubernetes resources such as Deployments and Services. citeturn0search2

---

## Idea

Maintain two environments:

```text
BLUE
↓
Current production version

GREEN
↓
New version
```

Example:

```text
Blue Deployment
    ↓
v1 Pods

Green Deployment
    ↓
v2 Pods
```

Both can exist at the same time.

---

## Traffic

Initially:

```text
Users
  ↓
Service
  ↓
Blue / v1
```

After validating Green:

```text
Users
  ↓
Service
  ↓
Green / v2
```

The traffic destination is switched.

---

## Why Blue-Green Exists

It allows:

- full new version to be prepared before switching users
- quick traffic switch
- easier rollback
- old version to remain available for a period

---

## Main Cost

You may temporarily need resources for:

```text
v1 environment
+
v2 environment
```

So Blue-Green can require significantly more capacity.

---

# 13. Canary Deployment

## Important clarification

Like Blue-Green, **Canary is a deployment/release pattern, not one of Kubernetes Deployment's two built-in `spec.strategy.type` values.**

---

## Idea

Instead of sending everyone to the new version:

```text
100% → v2
```

start with a small portion:

```text
95% → v1
5%  → v2
```

Observe the new version.

If it behaves correctly:

```text
90% → v1
10% → v2
```

then:

```text
50% → v1
50% → v2
```

and eventually:

```text
0%  → v1
100% → v2
```

---

# 14. Why Canary Exists

Canary reduces deployment risk.

Instead of:

```text
Old version
    ↓
Everyone gets new version
    ↓
Something breaks
```

you do:

```text
Old version
    ↓
Small amount of traffic
    ↓
New version
    ↓
Observe metrics/errors
    ↓
Gradually increase traffic
```

---

# 15. Blue-Green vs Canary

| Feature | Blue-Green | Canary |
|---|---|---|
| Main idea | Switch between two environments | Gradually expose users |
| New version | Usually fully deployed first | Starts with small exposure |
| Traffic | Switches from old → new | Gradually shifts |
| Rollback | Usually very fast traffic switch | Reduce/stop new-version traffic |
| Resource usage | Higher | Can be lower |
| Main goal | Fast environment switch | Risk-controlled gradual release |

---

# 16. The Four Strategies/Patterns You Should Remember

```text
Recreate
    ↓
Old OFF → New ON

RollingUpdate
    ↓
Old gradually OFF
New gradually ON

Blue-Green
    ↓
Blue ON + Green ready
Then switch traffic

Canary
    ↓
Small traffic → New
Then gradually increase
```

### Important terminology

```text
Recreate
RollingUpdate
```

are Kubernetes Deployment strategy types.

```text
Blue-Green
Canary
```

are broader deployment/release patterns.

---

# 17. Rollout Commands

You have already used some of these, but they belong to the Deployment topic.

## Check rollout

```bash
kubectl rollout status deployment/<name>
```

Meaning:

> Show whether the current Deployment rollout has completed.

---

## View rollout history

```bash
kubectl rollout history deployment/<name>
```

Meaning:

> Show the Deployment's stored revisions.

---

## Inspect a specific revision

```bash
kubectl rollout history deployment/<name> --revision=<number>
```

Meaning:

> Show the Pod template associated with that revision.

---

## Roll back

```bash
kubectl rollout undo deployment/<name>
```

Meaning:

> Move the Deployment back to the previous available revision.

---

## Roll back to a specific revision

```bash
kubectl rollout undo deployment/<name> --to-revision=<number>
```

Meaning:

> Explicitly choose which stored revision to restore.

---

# 18. Pause a Rollout

```bash
kubectl rollout pause deployment/<name>
```

Meaning:

> Pause the Deployment rollout so changes to the Pod template do not immediately trigger a new rollout.

This can be useful when you want to group multiple changes before resuming. citeturn0search0turn0search3

---

# 19. Resume a Rollout

```bash
kubectl rollout resume deployment/<name>
```

Meaning:

> Resume a paused Deployment rollout.

After resuming, Kubernetes proceeds with the accumulated changes. citeturn0search0

---

# 20. Important Pause/Resume Mental Model

```text
Normal
  ↓
Update Deployment
  ↓
Rollout happens

Pause
  ↓
Make changes
  ↓
No new rollout yet

Resume
  ↓
Kubernetes proceeds with rollout
```

A paused Deployment cannot be rolled back until it is resumed. citeturn0search0

---

# 21. Updating a Deployment

There are several ways to update a Deployment.

## Method 1 — Modify YAML

Change:

```yaml
image: task-manager-backend:v1
```

to:

```yaml
image: task-manager-backend:v2
```

Then:

```bash
kubectl apply -f deployment.yaml
```

This is the declarative approach.

---

# 22. Method 2 — `kubectl set image`

```bash
kubectl set image deployment/<deployment-name> \
  <container-name>=<image>:<tag>
```

Example:

```bash
kubectl set image deployment/task-manager-backend \
  backend=task-manager-backend:v2
```

Meaning:

> Change the container image used by the Deployment.

Kubernetes detects the changed Pod template and starts the appropriate rollout.

---

# 23. Why Changing the Pod Template Matters

A Deployment rollout happens when the Deployment's Pod template changes.

For example:

```yaml
spec:
  template:
    spec:
      containers:
        - image: app:v1
```

changes to:

```yaml
spec:
  template:
    spec:
      containers:
        - image: app:v2
```

This changes the Pod template.

Therefore:

```text
Pod Template changed
        ↓
New ReplicaSet
        ↓
Rollout
```

Scaling the Deployment alone does **not** create a new rollout. citeturn0search0

---

# 24. Deployment Revision vs Image Tag

These are different.

## Image tag

```text
task-manager-backend:v2
```

This identifies the container image version.

## Deployment revision

```text
REVISION 3
```

This identifies a stored Deployment revision.

Therefore:

```text
Image tag
    ≠
Deployment revision
```

A revision stores the Deployment's Pod template configuration.

---

# 25. Revision History Limit

Deployment revision history is stored through the ReplicaSets controlled by the Deployment.

Important field:

```yaml
spec:
  revisionHistoryLimit: 10
```

The default is `10` old ReplicaSets.

Why does this matter?

```text
Old ReplicaSets
      ↓
Revision history
      ↓
Possible rollback
```

If an old ReplicaSet is removed, that revision can no longer be used for rollback. citeturn0search1

---

# 26. Deployment Status

When inspecting a Deployment, important concepts include:

```text
DESIRED
CURRENT
UP-TO-DATE
AVAILABLE
```

### DESIRED

How many replicas the Deployment wants.

### CURRENT

How many replicas currently exist.

### UP-TO-DATE

How many Pods correspond to the latest Pod template.

### AVAILABLE

How many Pods are considered available.

---

# 27. Deployment Conditions

A Deployment can expose conditions describing its progress.

Important concepts include:

```text
Available
Progressing
ReplicaFailure
```

These help explain whether the Deployment has:

- enough available replicas
- made progress
- encountered a failure

---

# 28. Useful Inspection Commands

```bash
kubectl get deployment <name>
```

Basic Deployment status.

```bash
kubectl describe deployment <name>
```

Detailed Deployment information, including strategy, ReplicaSets, conditions, and events.

```bash
kubectl get rs
```

Shows the ReplicaSets created/managed by Deployments.

```bash
kubectl get pods
```

Shows the actual Pods.

Together:

```text
Deployment
    ↓
kubectl get deployment

ReplicaSets
    ↓
kubectl get rs

Pods
    ↓
kubectl get pods
```

---

# 29. Deployment Troubleshooting Mental Model

If a rollout is not progressing:

```text
Deployment
    ↓
Check Deployment status
    ↓
Check ReplicaSets
    ↓
Check Pods
    ↓
Describe failing resources
    ↓
Check logs
    ↓
Check events
```

Useful commands:

```bash
kubectl get deployment <name>

kubectl describe deployment <name>

kubectl get rs

kubectl get pods

kubectl describe pod <pod>

kubectl logs <pod>

kubectl get events
```

---

# 30. Common Deployment Failure Categories

A rollout can fail because the new Pods cannot become healthy.

Typical causes include:

```text
Wrong image
      ↓
ImagePullBackOff

Application crashes
      ↓
CrashLoopBackOff

Wrong configuration
      ↓
Container fails

Wrong port/application behavior
      ↓
Application inaccessible

Insufficient resources
      ↓
Pods cannot be scheduled

Readiness failure
      ↓
Pod does not become available
```

These will become much more important when you later study **Probes and Kubernetes Troubleshooting**.

---

# 31. `progressDeadlineSeconds`

A Deployment can define:

```yaml
spec:
  progressDeadlineSeconds: 600
```

This specifies how long Kubernetes should wait for Deployment progress before reporting that the Deployment has failed to make progress.

Mental model:

```text
Rollout starts
     ↓
Kubernetes expects progress
     ↓
No sufficient progress
     ↓
Progress deadline exceeded
     ↓
Deployment reports stalled progress
```

This is useful for detecting rollouts that are stuck rather than waiting indefinitely.

---

# 32. `minReadySeconds`

Another Deployment field is:

```yaml
spec:
  minReadySeconds: 10
```

Meaning:

> A newly created Pod must remain ready for at least this amount of time before the Deployment considers it available.

Mental model:

```text
Pod becomes Ready
      ↓
Wait 10 seconds
      ↓
Count as available
```

This can prevent a rollout from treating a briefly-ready Pod as immediately stable.

---

# 33. Important Deployment YAML — Reading Version

A useful complete example to understand is:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: task-manager-backend

spec:
  replicas: 3

  revisionHistoryLimit: 10
  progressDeadlineSeconds: 600
  minReadySeconds: 10

  strategy:
    type: RollingUpdate

    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1

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
          image: task-manager-backend:v2

          ports:
            - containerPort: 8000
```

You do **not** need to memorize this entire YAML.

Understand what each important section controls:

```text
replicas
    ↓
How many Pods?

strategy
    ↓
How are old Pods replaced?

maxUnavailable
    ↓
How many can be unavailable?

maxSurge
    ↓
How many extra can temporarily exist?

revisionHistoryLimit
    ↓
How many old revisions are retained?

progressDeadlineSeconds
    ↓
How long before lack of progress is reported?

minReadySeconds
    ↓
How long must a Pod stay ready before being counted available?

selector
    ↓
Which Pods belong to this Deployment?

template
    ↓
What should the Pods look like?
```

---

# 34. One Important Relationship

Keep this hierarchy fixed in your mind:

```text
Deployment
     │
     ├── Current ReplicaSet
     │       │
     │       ├── Pod
     │       ├── Pod
     │       └── Pod
     │
     └── Old ReplicaSet(s)
             │
             └── Old revision Pods
```

During a RollingUpdate:

```text
Old ReplicaSet
      ↓
gradually scaled down

New ReplicaSet
      ↓
gradually scaled up
```

This is why ReplicaSets are so important to understanding Deployments.

---

# 35. Deployment Strategy Decision Guide

## Choose Recreate when:

```text
Old + New versions must NOT coexist
        OR
Downtime is acceptable
```

---

## Choose RollingUpdate when:

```text
You want gradual replacement
        AND
Old + New can temporarily coexist
```

This is the normal/default Kubernetes Deployment strategy.

---

## Choose Blue-Green when:

```text
You want:
complete new environment
        +
controlled traffic switch
        +
fast rollback
```

---

## Choose Canary when:

```text
You want:
small initial exposure
        +
observe behavior
        +
gradually increase traffic
```

---

# 36. Final Comparison

```text
                    DEPLOYMENT / RELEASE APPROACHES

Recreate
   │
   └── Old OFF → New ON
       Simple
       Downtime possible


RollingUpdate
   │
   └── Old gradually replaced by New
       Default Kubernetes Deployment strategy
       Controls: maxUnavailable + maxSurge


Blue-Green
   │
   └── Old environment + New environment
       Switch traffic
       Fast rollback


Canary
   │
   └── Small traffic → New version
       Observe
       Gradually increase traffic
```

---

# 37. What You Have Now Completed

## Deployment Core

- [x] Deployment YAML
- [x] `replicas`
- [x] selectors
- [x] Pod template
- [x] Deployment → ReplicaSet → Pod
- [x] scaling
- [x] reconciliation
- [x] self-healing
- [x] RollingUpdate
- [x] rollout status
- [x] rollout history
- [x] revisions
- [x] rollback

## Remaining Deployment Reading

- [x] Recreate strategy
- [x] RollingUpdate strategy
- [x] `maxUnavailable`
- [x] `maxSurge`
- [x] Blue-Green pattern
- [x] Canary pattern
- [x] pause/resume
- [x] `kubectl set image`
- [x] revision history
- [x] `revisionHistoryLimit`
- [x] Deployment status
- [x] `progressDeadlineSeconds`
- [x] `minReadySeconds`
- [x] Deployment troubleshooting concepts

---

# 38. Most Important One-Liners

```text
Deployment
→ Manages application Pods through ReplicaSets.

ReplicaSet
→ Maintains the desired number of Pods.

Recreate
→ Remove old Pods before creating the new version.

RollingUpdate
→ Gradually replace old Pods with new Pods.

maxUnavailable
→ Maximum desired Pods allowed to be unavailable during a RollingUpdate.

maxSurge
→ Maximum extra Pods allowed above the desired replica count during a RollingUpdate.

Blue-Green
→ Maintain old and new environments, then switch traffic.

Canary
→ Gradually expose the new version to a small portion of traffic.

Rollout
→ The process of moving a Deployment from one Pod-template version to another.

Revision
→ Stored version of a Deployment's Pod template.

Rollback
→ Return a Deployment to an earlier available revision.

Pause
→ Temporarily stop a Deployment rollout from progressing.

Resume
→ Continue a paused rollout.

Pod Template
→ The specification Kubernetes uses to create Pods for the Deployment.

Desired State
→ What the Deployment declares it wants.

Actual State
→ What currently exists in the cluster.
```

---

# 39. Final Mental Model

You should now think about Deployment like this:

```text
                         Deployment
                              │
                 ┌────────────┴────────────┐
                 │                         │
             Desired State             Strategy
                 │                         │
             replicas                  Recreate
                 │                    RollingUpdate
                 ↓
            ReplicaSet(s)
                 │
          ┌──────┴──────┐
          ↓             ↓
       Old RS         New RS
          │             │
       old Pods       new Pods
                        │
                  Rollout controls
                  ├── maxUnavailable
                  ├── maxSurge
                  ├── pause
                  └── resume
```

And at the release-pattern level:

```text
Kubernetes Deployment Strategies
        │
        ├── Recreate
        └── RollingUpdate

Broader Release Patterns
        │
        ├── Blue-Green
        └── Canary
```

**After this reading, your Deployment topic is complete. The next Kubernetes topic should be Services.**
