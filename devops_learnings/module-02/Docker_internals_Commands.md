

```markdown
# Module 2: Docker Internals & Runtime Diagnostics Log

## 1. What is a Container? (Core Architecture)

A container is not a virtual machine with a guest operating system; it is a standard Linux process isolated directly at the host kernel level. Isolation of visibility (what the process can see, including PID trees, network routes, and mount points) is enforced via **Linux Namespaces**, while hard constraints on physical resources (what the process can use, such as RAM and CPU quotas) are enforced via **Control Groups (cgroups)**. Layered filesystems are merged dynamically via copy-on-write drivers (**OverlayFS**), and the entire lifecycle is orchestrated by the OCI runtime (`runc`) through `containerd`.

---

## 2. Command Reference & Terminal Run Log

### Container Execution & Process Tracking

* **`docker run -d --name web-sandbox -p 8080:80 nginx:latest`**
  * *Purpose:* Instantiates and runs an Nginx container in detached mode (`-d`), binding host port `8080` to container port `80` with the custom name `web-sandbox`.
```powershell
PS C:\devops_N\devops_learnings\module-02> docker run -d --name web-sandbox -p 8080:80 nginx:latest
be99b407df6363682f73823215acfa2d88f88bb97d732adc1272101074c6fc83

```

* **`docker top web-sandpox`**
* *Purpose:* Attempts to query running processes for a misspelled container name, resulting in a daemon lookup error.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker top web-sandpox
Error response from daemon: No such container: web-sandpox

```

* **`docker top web-sandbox`**
* *Purpose:* Lists the active processes running inside the container directly mapped to their actual host-level Kernel PIDs (`96039`, `96083`, etc.).



```powershell
PS C:\devops_N\devops_learnings\module-02> docker top web-sandbox
UID                 PID                 PPID                C                   STIME               TTY                 TIME                CMD
root                96039               96015               0                   10:55               ?                   00:00:00            nginx: master process nginx -g daemon off;
statd               96083               96039               0                   10:55               ?                   00:00:00            nginx: worker process
statd               96084               96039               0                   10:55               ?                   00:00:00            nginx: worker process
statd               96085               96039               0                   10:55               ?                   00:00:00            nginx: worker process
... [truncated worker processes]

```

---

### Interactive Shell & Ephemeral Filesystem

* **`docker exec -it web-sandbox bash`**
* *Purpose:* Opens an interactive pseudo-TTY session inside the running container's namespace to inspect and modify its writable layer.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker exec -it web-sandbox bash
root@be99b407df63:/# ls
bin  boot  dev  docker-entrypoint.d  docker-entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@be99b407df63:/# touch index.txt
root@be99b407df63:/# echo "Hellooo hihih" > index.txt
root@be99b407df63:/# cat index.txt
Hellooo hihih
root@be99b407df63:/# exit 
exit

```

*Takeaway:* Files created inside the container (like `index.txt`) exist exclusively in the ephemeral `upperdir` writable layer and will be destroyed if the container is removed without a persistent volume.

---

### Logs & Low-Level Metadata Inspection

* **`docker logs --tail 20 web-sandbox`**
* *Purpose:* Streams the last 20 lines of standard output/error (stdout/stderr) from container PID 1.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker logs --tail 20 web-sandbox
2026/09/22 10:55:17 [notice] 1#1: built by gcc 14.2.0 (Debian 14.2.0-19) 
2026/09/22 10:55:17 [notice] 1#1: OS: Linux 6.6.87.2-microsoft-standard-WSL2
2026/09/22 10:55:17 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2026/09/22 10:55:17 [notice] 1#1: start worker processes
... [truncated worker logs]

```

* **`docker inspect web-sandbox`**
* *Purpose:* Returns the complete low-level JSON configuration schema of the container, including networking, host resource configs, state, and storage drivers.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker inspect web-sandbox
# Key extracted properties:
# State.Status: "running"
# State.Pid: 96039
# NetworkSettings.Networks.bridge.IPAddress: "172.17.0.2"
# NetworkSettings.Ports: 80/tcp -> HostPort 8080
# HostConfig.NetworkMode: "bridge"

```

---

### Layer History & Image Diagnostics

* **`docker history nginx:latest`**
* *Purpose:* Breaks down the image into its constituent layers, displaying build instructions, layer sizes, and intermediate commands.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker history nginx:latest
IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
f0002216f237   4 weeks ago    CMD ["nginx" "-g" "daemon off;"]                0B        buildkit.dockerfile.v0
<missing>      4 weeks ago    STOPSIGNAL SIGQUIT                              0B        buildkit.dockerfile.v0
<missing>      4 weeks ago    EXPOSE map[80/tcp:{}]                           0B        buildkit.dockerfile.v0
<missing>      4 weeks ago    ENTRYPOINT ["/docker-entrypoint.sh"]            0B        buildkit.dockerfile.v0
<missing>      4 weeks ago    COPY 30-tune-worker-processes.sh /docker-ent…   16.4kB    buildkit.dockerfile.v0
<missing>      4 weeks ago    RUN /bin/sh -c set -x     && groupadd --syst…   87.6MB    buildkit.dockerfile.v0
<missing>      4 weeks ago    # debian.sh --arch 'amd64' out/ 'trixie' ...    87.5MB    debuerreotype 0.17

```

*Takeaway:* Metadata declarations (`CMD`, `EXPOSE`, `ENV`) consume 0 bytes, whereas package installations (`RUN`) and file injections (`COPY`) generate physical layers.

* **`docker history web-sandbox`**
* *Purpose:* Fails because `docker history` only operates on container image identifiers/tags, not running container names.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker history web-sandbox 
Error response from daemon: No such image: web-sandbox:latest

```

---

### Resource Constraints & cgroup Enforcement

* **`docker run -d --name myapp --memory=100m --cpus=0.5 nginx:latest`**
* *Purpose:* Launches a container with strict Linux cgroup limits: a hard RAM limit of 100 MiB and maximum CPU quota capped at 50% of a single core.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker run -d --name myapp --memory=100m --cpus=0.5 nginx:latest
c54701d249df48b78f0ae2630e73606bf002d7a1e57c5e37a8c0ce9dd8dbb769

```

* **`docker stats --no-stream myapp`**
* *Purpose:* Captures a single-point snapshot of runtime resource utilization, verifying the 100 MiB limit enforcement.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker stats --no-stream myapp
CONTAINER ID   NAME    CPU %   MEM USAGE / LIMIT   MEM %    NET I/O      BLOCK I/O     PIDS
c54701d249df   myapp   0.00%   13.28MiB / 100MiB   13.28%   872B / 126B  0B / 12.3kB   17

```

---

### Container Termination & System Garbage Collection

* **`docker stop myapp web-sandbox`**
* *Purpose:* Sends a `SIGTERM` signal (followed by `SIGKILL` if unresponsive) to gracefully shut down the specified containers.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker stop myapp web-sandbox
myapp
web-sandbox

```

* **`docker container prune`**
* *Purpose:* Deletes all stopped containers across the host, reclaiming local disk allocations.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker container prune 
Total reclaimed space: 5.521MB

```

* **`docker image prune`**
* *Purpose:* Deletes only dangling images (untagged intermediate layers marked as `<none>`).



```powershell
PS C:\devops_N\devops_learnings\module-02> docker image prune
Total reclaimed space: 0B

```

* **`docker system df`**
* *Purpose:* Displays the host-wide breakdown of Docker disk consumption across Images, Containers, Local Volumes, and Build Cache.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          36        2         40.09GB   16.95GB (42%)
Containers      2         2         87.66MB   0B (0%)
Local Volumes   28        2         4.338GB   1.734GB (39%)
Build Cache     149       0         23.96GB   8.647GB

```

* **`docker image prune -a -f`**
* *Purpose:* Forcefully deletes all unused images not currently referenced by an active container, freeing significant disk space.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker image prune -a -f
Total reclaimed space: 1.773GB

```

* **`docker system df` (Post-Cleanup Verification)**
* *Purpose:* Confirms image count dropped from 36 to 3, validating successful cleanup of unreferenced storage artifacts.



```powershell
PS C:\devops_N\devops_learnings\module-02> docker system df        
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          3         2         22.05GB   21.5GB (97%)
Containers      2         2         87.66MB   0B (0%)
Local Volumes   28        2         4.338GB   1.734GB (39%)
Build Cache     149       0         23.96GB   23.96GB

```

```

```