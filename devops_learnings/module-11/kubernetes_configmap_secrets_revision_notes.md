# Kubernetes ConfigMap and Secret --- Revision Notes

> **Scope:** Theory and reference snippets for ConfigMaps and Secrets.
> These notes prepare us for the hands-on session; they do not mean we
> are starting the lab yet.

## 1. Why do we need them?

An application often needs configuration such as its environment, log
level, database host, or credentials. We should not need to rebuild the
application image just because a value changes between development,
testing, and production.

Kubernetes provides two resources for storing configuration separately
from the application image:

-   **ConfigMap:** for ordinary, non-sensitive configuration.
-   **Secret:** for sensitive values such as passwords, API tokens, and
    TLS private keys.

A ConfigMap or Secret does not automatically affect every Pod. A Pod's
container must explicitly reference the resource.

## 2. ConfigMap vs Secret

  -----------------------------------------------------------------------
  Feature                 ConfigMap               Secret
  ----------------------- ----------------------- -----------------------
  Intended data           Non-sensitive           Sensitive configuration
                          configuration           

  Examples                `APP_ENV`, `LOG_LEVEL`, `DB_PASSWORD`, API
                          `DB_HOST`               token, TLS key

  Common consumption      Environment variables   Environment variables
  methods                 or mounted files        or mounted files

  Automatically injected  No                      No
  into every Pod?                                 

  Safe to commit real     Only if the values are  **No** --- do not
  values to Git?          appropriate to publish  commit real credentials
  -----------------------------------------------------------------------

**Important:** Secret values shown in Kubernetes YAML as Base64 are
encoded, not automatically encrypted. A Secret resource is not a reason
to expose credentials in Git or grant broad access. Restrict access with
RBAC and configure encryption at rest where appropriate.

## 3. Example ConfigMap YAML

Save as `configmap.yaml`:

``` yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "development"
  LOG_LEVEL: "info"
  DB_HOST: "postgres-service"
  DB_PORT: "5432"
```

Key points:

-   `apiVersion: v1`: core Kubernetes API.
-   `kind: ConfigMap`: the resource type.
-   `metadata.name`: the name other resources will reference.
-   `data`: ordinary string key/value configuration.

Do not put passwords, tokens, or private keys in a ConfigMap.

## 4. Example Secret YAML

Save as `secret.yaml`:

``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  DB_USERNAME: "app_user"
  DB_PASSWORD: "replace-with-a-local-test-value"
```

Key points:

-   `kind: Secret`: identifies the resource as a Secret.
-   `type: Opaque`: a general-purpose Secret type.
-   `stringData`: lets you write plain strings in the manifest;
    Kubernetes converts them for storage.
-   The example value is a placeholder, **not a real credential**.

Avoid committing real Secret manifests containing credentials. For
actual environments, use an appropriate secret-management workflow.

## 5. How a Deployment passes values to a container

Creating a ConfigMap or Secret is only one part of the setup. A workload
must reference it in its Pod template.

### A. Import all keys as environment variables

``` yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: demo-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: demo-app
  template:
    metadata:
      labels:
        app: demo-app
    spec:
      containers:
        - name: app
          image: nginx:stable
          envFrom:
            - configMapRef:
                name: app-config
            - secretRef:
                name: app-secret
```

`envFrom` imports the keys from the referenced resources as environment
variables. This example demonstrates the Kubernetes wiring; the NGINX
image itself does not automatically use the sample application-specific
variables.

### B. Import selected keys only

``` yaml
env:
  - name: APP_ENV
    valueFrom:
      configMapKeyRef:
        name: app-config
        key: APP_ENV
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: DB_PASSWORD
```

-   `configMapKeyRef` reads one key from a ConfigMap.
-   `secretKeyRef` reads one key from a Secret.
-   `name` is the resource name; `key` is the key inside that resource.

These entries go under the relevant container in the Pod template.

## 6. Environment variables vs mounted files

### Environment variables

Use `env` or `envFrom` when the application expects configuration
through environment variables.

Remember: when a ConfigMap or Secret changes, environment variables
already set in a running container do **not** update automatically. A
workload restart/rollout may be needed to make new values available.

### Mounted files

A ConfigMap or Secret can also be mounted into a container as files.
This is useful when an application expects a configuration file or
certificate/key files.

Illustrative snippet for a ConfigMap volume:

``` yaml
spec:
  containers:
    - name: app
      image: nginx:stable
      volumeMounts:
        - name: app-config-volume
          mountPath: /etc/app-config
          readOnly: true
  volumes:
    - name: app-config-volume
      configMap:
        name: app-config
```

Each key is presented as a file in the mounted directory by default. A
Secret volume works similarly, using `secret:` instead of `configMap:`.

Mounted ConfigMap/Secret data can be refreshed by Kubernetes eventually,
but the application must reread or reload the file to use the new value.
Mounting with `subPath` does not receive these automatic updates. For
predictable changes, teams often deliberately trigger a rollout.

## 7. Namespace rule

A Pod generally references ConfigMaps and Secrets in **its own
namespace**. If a resource is missing, check that it exists in the same
namespace as the workload and that the name/key is correct.

## 8. Useful terminal commands

These commands are reference commands for the future lab. Do not run
them yet unless we explicitly start hands-on.

### Inspect the cluster and namespace

``` bash
kubectl get namespaces
kubectl config current-context
kubectl get pods
```

### Create resources from YAML

``` bash
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
```

`apply` creates the resource if needed and updates it when the manifest
changes.

### Inspect resources

``` bash
kubectl get configmaps
kubectl describe configmap app-config

kubectl get secrets
kubectl describe secret app-secret

kubectl get deployment demo-app
kubectl get pods
```

`describe secret` shows metadata and key names/lengths, rather than
printing the Secret values as ordinary output.

To inspect a manifest returned by the API, you can use:

``` bash
kubectl get configmap app-config -o yaml
kubectl get secret app-secret -o yaml
```

**Caution:** the Secret YAML output can expose encoded credential
material. Do not paste it into public chats, screenshots, logs, or Git.
Base64 is not encryption.

### Check a Pod's environment (only if the container has a shell and suitable tools)

``` bash
kubectl exec <pod-name> -- printenv
kubectl exec <pod-name> -- printenv APP_ENV
```

Replace `<pod-name>` with the actual Pod name. Minimal/distroless images
may not include `printenv` or a shell. Do not print real passwords into
shared terminal logs.

### Check rollout status

``` bash
kubectl rollout status deployment/demo-app
kubectl rollout restart deployment/demo-app
kubectl rollout history deployment/demo-app
```

A restart is one way to recreate Pods so environment variables are read
again. It does not change the ConfigMap or Secret itself.

### Clean up lab resources

``` bash
kubectl delete -f deployment.yaml
kubectl delete -f secret.yaml
kubectl delete -f configmap.yaml
```

Only delete resources you created for the lab. Confirm the active
Kubernetes context and namespace before making changes.

## 9. Updating configuration --- what changes and what does not?

  -----------------------------------------------------------------------
  How the value is consumed           What happens after the resource
                                      changes?
  ----------------------------------- -----------------------------------
  Environment variable                Existing container's environment
                                      does not change automatically

  Mounted ConfigMap/Secret file       Kubernetes may update the mounted
                                      files eventually; the app must
                                      reread/reload them

  Mounted using `subPath`             Does not receive the normal
                                      automatic projected-volume updates

  Application reads configuration     It may need a restart/rollout even
  only at startup                     if the mounted file changes
  -----------------------------------------------------------------------

## 10. Common mistakes to avoid

1.  Creating a ConfigMap/Secret but forgetting to reference it in the
    Deployment's Pod template.
2.  Referencing the wrong resource name or key.
3.  Creating the resource in a different namespace from the Pod.
4.  Assuming Base64 means a Secret is encrypted.
5.  Committing real passwords or tokens to Git.
6.  Expecting environment variables in a running container to change
    automatically.
7.  Assuming every application automatically reloads changed
    configuration files.
8.  Assuming Kubernetes Secret alone replaces RBAC, encryption-at-rest
    configuration, or a proper secret-management process.

## 11. Quick mental model

``` text
ConfigMap / Secret
        |
        | referenced explicitly by
        v
Deployment's Pod template
        |
        v
Pod -> Container
        |
        +-- environment variables
        |
        +-- mounted configuration files
```

-   **ConfigMap:** ordinary settings.
-   **Secret:** sensitive settings.
-   **Deployment/Pod template:** connects the resource to the workload.
-   **Container/application:** consumes the values.

## 12. What we will do in the hands-on session

We will proceed one small step at a time, using the instructor's Session
12 examples as the reference when their files are available:

1.  Inspect the instructor's ConfigMap/Secret examples and explain each
    field before running anything.
2.  Confirm the Kubernetes context and namespace so commands target the
    intended cluster.
3.  Create/apply a ConfigMap and verify that it exists.
4.  Create/apply a Secret using a **dummy local value only** and
    understand why its Base64 representation is not encryption.
5.  Connect both resources to a small Deployment.
6.  Verify that the Pod receives the selected values, without
    unnecessarily exposing sensitive output.
7.  Change a configuration value and observe the difference between
    environment variables and mounted files.
8.  Practise the relevant inspection and cleanup commands.

We will **not** start this sequence until you explicitly say to begin
hands-on. We will also avoid adding unrelated topics or extra resources
during the lab.

------------------------------------------------------------------------

### One-line revision

**A ConfigMap stores ordinary configuration, a Secret stores sensitive
configuration, and a Pod must explicitly reference either resource
before its container can consume the values.**
