
# Linux Fundamentals & Shell Scripting — Quick Revision Notes

> Format: **Definition** → One-line explanation | **Example** → Linux command or Bash code.

# 1. Linux Fundamentals

## 1.1 Linux File System

- **File System Hierarchy (FHS):** Standard structure defining where Linux stores files and directories.  
  `ls /`

- **Root (`/`):** The top-level directory containing the entire Linux file system.  
  `ls /`

- **Home (`~`):** The current user's home directory.  
  `cd ~`

- **Current Directory (`.`):** Represents the directory you are currently in.  
  `ls .`

- **Parent Directory (`..`):** Represents the directory one level above the current directory.  
  `cd ..`

- **Absolute Path:** A complete path starting from `/`.  
  `cd /home/user/Documents`

- **Relative Path:** A path interpreted relative to the current directory.  
  `cd Documents`

- **Hidden Files and Directories:** Names beginning with `.` are hidden by default in normal directory listings.  
  `ls -la`

- **`/bin`:** Contains essential user commands; often linked to `/usr/bin` on modern systems.  
  `ls /bin`

- **`/etc`:** Stores system-wide configuration files.  
  `ls /etc`

- **`/home`:** Contains regular users' home directories.  
  `ls /home`

- **`/var`:** Stores variable data such as logs, caches, and spool files.  
  `ls /var`

- **`/tmp`:** Stores temporary files that may be automatically deleted.  
  `ls -la /tmp`

- **`/usr`:** Contains many user applications, libraries, and shared resources.  
  `ls /usr`

- **`/opt`:** Commonly stores optional or third-party application software.  
  `ls /opt`

- **`/dev`:** Contains device files representing hardware and virtual devices.  
  `ls /dev`

- **`/proc`:** A virtual filesystem exposing process and kernel information.  
  `cat /proc/cpuinfo`

- **`/sys`:** A virtual filesystem exposing kernel, device, and hardware information.  
  `ls /sys`

- **`/root`:** The root administrator's home directory.  
  `sudo ls /root`

- **Files vs Directories:** Files hold data, while directories organize files and other directories.  
  `file myfile.txt`

- **File Types:** Linux supports regular files, directories, symbolic links, device files, sockets, and FIFOs.  
  `ls -l`

- **Symbolic Links vs Hard Links:** A symbolic link points to a pathname; a hard link references the same filesystem inode.  
  `ln -s original.txt shortcut.txt`  
  `ln original.txt hardlink.txt`

- **File Creation:** Creates an empty file or updates an existing file's timestamp.  
  `touch notes.txt`

- **File Deletion:** Removes a file or, with suitable options, a directory tree.  
  `rm notes.txt`

- **Directory Navigation:** Changes the current working directory.  
  `cd /var/log`

- **Mounting:** Makes a filesystem accessible at a directory called a mount point.  
  `sudo mount /dev/sdb1 /mnt`

- **Unmounting:** Detaches a mounted filesystem from its mount point.  
  `sudo umount /mnt`

## 1.2 Essential Linux Commands

### Navigation

- **`pwd`:** Prints the current working directory.  
  `pwd`

- **`ls`:** Lists directory contents.  
  `ls -lah`

- **`cd`:** Changes the current working directory.  
  `cd /etc`

- **`tree`:** Displays directory contents as a tree, if installed.  
  `tree -L 2`

### File Operations

- **`touch`:** Creates an empty file or updates timestamps.  
  `touch file.txt`

- **`mkdir`:** Creates directories.  
  `mkdir -p project/src`

- **`cp`:** Copies files or directories.  
  `cp file.txt backup.txt`

- **`mv`:** Moves or renames files and directories.  
  `mv old.txt new.txt`

- **`rm`:** Removes files and directories.  
  `rm file.txt`

- **`rmdir`:** Removes empty directories.  
  `rmdir empty_dir`

- **`ln`:** Creates hard links or symbolic links.  
  `ln -s file.txt shortcut.txt`

### File Reading

- **`cat`:** Displays or concatenates file contents.  
  `cat file.txt`

- **`less`:** Reads a file interactively with scrolling and search.  
  `less /var/log/syslog`

- **`more`:** Displays file contents one screen at a time.  
  `more file.txt`

- **`head`:** Displays the first lines of a file.  
  `head -n 10 file.txt`

- **`tail`:** Displays the last lines of a file or follows new log entries.  
  `tail -f app.log`

### Searching

- **`find`:** Searches for files and directories by specified criteria.  
  `find . -name "*.txt"`

- **`grep`:** Searches text for matching patterns.  
  `grep -in "error" app.log`

- **`locate`:** Searches a filename database; results may be outdated until the database is updated.  
  `locate notes.txt`

- **`which`:** Shows the executable selected through the shell's `PATH` lookup.  
  `which python3`

- **`whereis`:** Locates common binary, source, and manual-file paths for a command.  
  `whereis bash`

### Text Processing

- **`sort`:** Sorts lines of text.  
  `sort names.txt`

- **`uniq`:** Removes or counts adjacent duplicate lines.  
  `sort names.txt | uniq`

- **`wc`:** Counts lines, words, and bytes or characters.  
  `wc -l file.txt`

- **`cut`:** Extracts selected fields or character positions.  
  `cut -d',' -f1 data.csv`

- **`tr`:** Translates or deletes characters.  
  `echo "hello" | tr 'a-z' 'A-Z'`

- **`sed`:** Performs stream editing, such as replacing text.  
  `sed 's/old/new/g' file.txt`

- **`awk`:** Processes text using fields, patterns, and actions.  
  `awk '{print $1}' file.txt`

### System Information

- **`uname`:** Displays kernel and system information.  
  `uname -a`

- **`hostname`:** Displays or configures the system hostname.  
  `hostname`

- **`date`:** Displays or formats the current date and time.  
  `date '+%Y-%m-%d %H:%M:%S'`

- **`uptime`:** Displays system uptime and load averages.  
  `uptime`

- **`whoami`:** Prints the effective username.  
  `whoami`

- **`id`:** Displays user ID, primary group, and supplementary groups.  
  `id`

### Disk Usage

- **`df`:** Shows available and used filesystem space.  
  `df -h`

- **`du`:** Estimates file or directory disk usage.  
  `du -sh ~/Documents`

- **`lsblk`:** Lists block devices and their partitions.  
  `lsblk`

### Archives

- **`tar`:** Creates or extracts archives, optionally compressed.  
  `tar -czf backup.tar.gz project/`

- **`gzip`:** Compresses a file, usually producing a `.gz` file.  
  `gzip file.txt`

- **`zip`:** Creates a ZIP archive.  
  `zip -r archive.zip project/`

- **`unzip`:** Extracts a ZIP archive.  
  `unzip archive.zip -d extracted/`

### Help

- **`man`:** Opens a command's manual page.  
  `man ls`

- **`info`:** Opens detailed documentation in Info format, when available.  
  `info coreutils`

- **`--help`:** Displays a command's built-in usage information, when supported.  
  `ls --help`

### Command Chaining

- **`&&`:** Runs the next command only if the previous command succeeds.  
  `mkdir demo && cd demo`

- **`||`:** Runs the next command only if the previous command fails.  
  `cd missing_dir || echo "Directory not found"`

- **`;`:** Runs commands sequentially regardless of the previous command's exit status.  
  `date; whoami`

### Wildcards

- **`*`:** Matches zero or more characters in filename expansion.  
  `ls *.txt`

- **`?`:** Matches exactly one character in filename expansion.  
  `ls file?.txt`

- **`[]`:** Matches one character from a specified set or range.  
  `ls file[1-3].txt`

### Pipes and Redirection

- **Pipe (`|`):** Sends one command's standard output to another command's standard input.  
  `ls -l | grep ".txt"`

- **Output Redirection (`>`):** Sends standard output to a file, replacing its contents.  
  `echo "Hello" > output.txt`

- **Append Redirection (`>>`):** Appends standard output to a file.  
  `echo "New line" >> output.txt`

- **Input Redirection (`<`):** Supplies a file as a command's standard input.  
  `sort < names.txt`

- **Error Redirection (`2>`):** Sends standard error to a file.  
  `ls missing 2> errors.txt`

## 1.3 Users & Permissions

- **Root vs Regular User:** Root has UID 0 and broad administrative privileges; regular users have restricted permissions.  
  `id`

- **Users and Groups:** Users represent accounts, while groups organize users for shared access permissions.  
  `id username`

- **`/etc/passwd`:** Stores account metadata, including usernames, UIDs, GIDs, and login shells.  
  `grep '^root:' /etc/passwd`

- **`/etc/shadow`:** Stores password hashes and password-aging information, normally accessible only to privileged users.  
  `sudo less /etc/shadow`

- **`/etc/group`:** Stores group metadata and supplementary group membership information.  
  `cat /etc/group`

- **`whoami`:** Displays the effective username.  
  `whoami`

- **`id`:** Displays numeric user and group IDs.  
  `id`

- **`who`:** Shows users currently logged in.  
  `who`

- **`groups`:** Shows a user's group memberships.  
  `groups`

- **`useradd`:** Creates a user account.  
  `sudo useradd -m alice`

- **`usermod`:** Modifies an existing user account.  
  `sudo usermod -aG developers alice`

- **`userdel`:** Deletes a user account.  
  `sudo userdel alice`

- **`passwd`:** Changes a user's password.  
  `passwd`

- **`groupadd`:** Creates a group.  
  `sudo groupadd developers`

- **`groupmod`:** Modifies a group.  
  `sudo groupmod -n engineers developers`

- **`groupdel`:** Deletes a group, provided system restrictions are satisfied.  
  `sudo groupdel engineers`

- **`su`:** Switches to another user account.  
  `su - alice`

- **`sudo`:** Executes an authorized command with elevated privileges.  
  `sudo systemctl status ssh`

- **Read (`r`):** Allows reading a file or listing directory entries.  
  `chmod u+r file.txt`

- **Write (`w`):** Allows modifying a file or changing directory entries, subject to other restrictions.  
  `chmod u+w file.txt`

- **Execute (`x`):** Allows executing a file or traversing a directory.  
  `chmod u+x script.sh`

- **User, Group, Others:** Permission classes representing the file owner, owning group, and everyone else.  
  `ls -l file.txt`

- **Numeric Permissions:** Represent `r=4`, `w=2`, and `x=1`; each digit defines owner, group, or others.  
  `chmod 644 file.txt`

- **`chmod`:** Changes file or directory permissions.  
  `chmod 755 script.sh`

- **`chown`:** Changes file ownership.  
  `sudo chown alice file.txt`

- **`chgrp`:** Changes the owning group.  
  `sudo chgrp developers file.txt`

- **`umask`:** Defines which permission bits are removed from default creation permissions.  
  `umask 022`

- **SUID:** On executable files, runs the program with the file owner's effective UID, subject to filesystem and execution rules.  
  `chmod u+s program`

- **SGID:** On executable files, sets the effective group to the file's group; on directories, new entries generally inherit that group.  
  `chmod g+s shared_dir`

- **Sticky Bit:** On shared directories, restricts deletion or renaming of entries to authorized users, such as their owners or root.  
  `chmod +t shared_dir`

- **Least Privilege Principle:** Give each user or process only the permissions required for its task.  
  `sudo -u alice cat /home/alice/file.txt`

## 1.4 Processes

- **Program vs Process:** A program is stored code; a process is a running instance of that program.  
  `sleep 60 &`

- **PID and PPID:** PID identifies a process; PPID identifies its parent process.  
  `ps -o pid,ppid,cmd -p $$`

- **Process States and Lifecycle:** Processes may be running, sleeping, stopped, or zombie while moving through their lifecycle.  
  `ps -eo pid,stat,cmd`

- **Foreground vs Background:** Foreground jobs interact with the terminal; background jobs run without occupying its foreground.  
  `sleep 60 &`

- **`ps`:** Displays process information.  
  `ps aux`

- **`top`:** Provides a live view of processes and resource usage.  
  `top`

- **`htop`:** Provides an interactive process monitor, if installed.  
  `htop`

- **`pstree`:** Displays processes in a parent-child tree.  
  `pstree -p`

- **`pgrep`:** Finds process IDs matching a name or pattern.  
  `pgrep -a python`

- **`pidof`:** Finds process IDs associated with an executable name, when supported.  
  `pidof nginx`

- **`kill`:** Sends a signal to a process ID.  
  `kill -TERM 1234`

- **`pkill`:** Sends a signal to processes matching a pattern.  
  `pkill -TERM -x myapp`

- **`killall`:** Sends a signal to processes matching a command name; availability and behavior vary by system.  
  `killall myapp`

- **`SIGTERM`:** Requests a process to terminate gracefully.  
  `kill -TERM 1234`

- **`SIGKILL`:** Forces a process to stop and cannot be caught or ignored.  
  `kill -KILL 1234`

- **`SIGINT`:** Interrupts a process, commonly generated by Ctrl+C.  
  `kill -INT 1234`

- **`SIGHUP`:** Traditionally signals terminal hangup; some daemons use it to reload configuration.  
  `kill -HUP 1234`

- **`nice`:** Starts a process with a scheduling niceness value.  
  `nice -n 10 command`

- **`renice`:** Changes the niceness value of a running process.  
  `renice 10 -p 1234`

- **`jobs`:** Lists jobs associated with the current shell.  
  `jobs -l`

- **`bg`:** Resumes a stopped shell job in the background.  
  `bg %1`

- **`fg`:** Brings a shell job into the foreground.  
  `fg %1`

- **`nohup`:** Runs a command so it ignores hangup signals, commonly allowing it to outlive terminal closure.  
  `nohup ./script.sh > output.log 2>&1 &`

- **CPU and Memory Usage:** Process resource metrics show how much processor time and memory a process consumes.  
  `ps -eo pid,%cpu,%mem,cmd --sort=-%cpu | head`

- **Load Average:** Measures system load over 1, 5, and 15 minutes, including runnable and certain uninterruptible tasks.  
  `uptime`

- **`ulimit`:** Displays or changes shell resource limits.  
  `ulimit -a`

## 1.5 Services

- **Service or Daemon:** A service is a background system function; a daemon is a process that commonly provides such a function.  
  `systemctl status cron`

- **Service vs Process:** A process is a running program instance; a service is a managed function that may involve one or more processes.  
  `systemctl status ssh`

- **`systemd`:** A common Linux init and service manager that manages startup, services, and system units.  
  `systemctl is-system-running`

- **`systemctl`:** Controls and inspects systemd units.  
  `systemctl status cron`

- **Starting a Service:** Starts a service immediately.  
  `sudo systemctl start cron`

- **Stopping a Service:** Stops a running service.  
  `sudo systemctl stop cron`

- **Restarting a Service:** Stops and starts a service again.  
  `sudo systemctl restart cron`

- **Reloading a Service:** Requests a service to reload configuration without a full restart, if supported.  
  `sudo systemctl reload nginx`

- **Checking Service Status:** Displays a service's current state and recent status information.  
  `systemctl status nginx`

- **Enabling at Boot:** Configures a service to start automatically during system startup.  
  `sudo systemctl enable cron`

- **Disabling at Boot:** Prevents automatic startup without necessarily stopping the running service.  
  `sudo systemctl disable cron`

- **Active State:** Indicates that a unit is running or otherwise considered active by systemd.  
  `systemctl is-active cron`

- **Inactive State:** Indicates that a unit is not currently active.  
  `systemctl is-active cron`

- **Failed State:** Indicates that systemd considers a unit to have failed.  
  `systemctl --failed`

- **Viewing Service Logs:** Displays journal entries associated with a service.  
  `journalctl -u nginx`

- **Systemd Unit Files:** Configuration files define services, timers, sockets, mounts, and other systemd-managed units.  
  `systemctl cat nginx`

- **Basic Service Configuration:** A service unit specifies how systemd should start and manage a program.  
  `systemctl cat cron`

- **Service Dependencies:** Unit relationships define startup ordering and dependency requirements.  
  `systemctl list-dependencies nginx`

- **Creating a Custom Service:** A custom unit can run a script or application under systemd.  
  `sudo nano /etc/systemd/system/myapp.service`

  Example unit content:

  ```ini
  [Unit]
  Description=My Custom Application
  After=network.target

  [Service]
  Type=simple
  ExecStart=/usr/local/bin/myapp
  Restart=on-failure

  [Install]
  WantedBy=multi-user.target
  ```

  Apply and start it:

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable --now myapp.service
  systemctl status myapp.service
  ```

- **Troubleshooting Failed Services:** Inspect unit status and logs to identify configuration or startup failures.  
  `journalctl -u myapp.service -b --no-pager`

## 1.6 Logs & Basic Troubleshooting

- **System and Application Logs:** Logs record system events, application activity, warnings, and failures.  
  `journalctl -b`

- **`/var/log/`:** Common directory for traditional system and application log files.  
  `ls -lah /var/log`

- **`syslog`:** A common system log filename on some distributions.  
  `sudo less /var/log/syslog`

- **`messages`:** A general system log filename on some distributions.  
  `sudo less /var/log/messages`

- **`auth.log`:** Common Debian/Ubuntu log for authentication and authorization events.  
  `sudo less /var/log/auth.log`

- **`kern.log`:** Common log file for kernel messages on some distributions.  
  `sudo less /var/log/kern.log`

- **`cat`:** Displays log file contents.  
  `cat app.log`

- **`less`:** Opens a log interactively for searching and scrolling.  
  `less app.log`

- **`tail`:** Shows recent log lines or follows a growing log.  
  `tail -f app.log`

- **`grep`:** Filters logs for matching text.  
  `grep -i "error" app.log`

- **`journalctl`:** Reads logs stored in the systemd journal.  
  `journalctl -b -p warning`

- **`dmesg`:** Displays kernel ring-buffer messages, subject to system access restrictions.  
  `dmesg --level=err,warn`

- **Log Levels:** Debug, Info, Warning, Error, and Critical indicate increasing severity in common logging conventions.  
  `logger -p user.warning "Disk space is low"`

- **`logrotate`:** Rotates, compresses, and manages log retention.  
  `logrotate --debug /etc/logrotate.conf`

- **Exit Codes:** A command usually returns `0` for success and a nonzero value for failure.  
  `ls /missing; echo $?`

- **Permission Errors:** Permission errors occur when a user or process lacks required access rights.  
  `ls -l restricted.txt`

- **Missing Files and Commands:** Check paths and executable lookup when a file or command cannot be found.  
  `command -v python3`

- **Disk Space Issues:** Compare filesystem capacity and directory usage to locate storage problems.  
  `df -h; du -sh /var/log`

- **High CPU and Memory Usage:** Inspect processes and available memory to identify resource pressure.  
  `top; free -h`

- **Process and Service Failures:** Inspect process status and service logs to diagnose crashes or startup failures.  
  `systemctl --failed`

- **Port Conflicts:** Identify listening sockets and the processes using them.  
  `sudo ss -lntup`

- **`lsof`:** Lists open files, including network sockets when supported.  
  `sudo lsof -i :8080`

- **`ping`:** Tests network reachability using ICMP echo requests, when permitted.  
  `ping -c 4 8.8.8.8`

- **`curl`:** Makes requests to URLs and helps diagnose HTTP connectivity.  
  `curl -I https://example.com`

- **`ip`:** Displays or manages network interfaces, addresses, and routes.  
  `ip addr`

- **`dig`:** Queries DNS records.  
  `dig example.com`

- **`nslookup`:** Queries DNS information using a DNS server.  
  `nslookup example.com`

- **Configuration and Dependencies:** Inspect configuration files and validate required services, packages, and paths.  
  `systemctl cat nginx`

# 2. Shell Scripting

## 2.1 Shell Scripting Fundamentals

- **Shell:** A command interpreter that executes commands and supports scripting.  
  `echo "$SHELL"`

- **Bash vs sh:** Bash is a feature-rich shell; `sh` refers to a shell interface that may be provided by a different implementation.  
  `bash --version`

- **Shell Script:** A text file containing commands executed by a shell.  
  `bash script.sh`

- **Creating a Script File:** Create a text file to store shell commands.  
  `touch script.sh`

- **Shebang (`#!/bin/bash`):** Specifies the interpreter used when an executable script is launched directly.  
  `head -n 1 script.sh`

- **Making a Script Executable:** Adds execute permission to a script.  
  `chmod +x script.sh`

- **Running a Script:** Executes a script using Bash or its executable path.  
  `bash script.sh`  
  `./script.sh`

- **Comments:** Lines beginning with `#` outside the shebang are used for human-readable notes.  
  `# This script prints a message`

- **Exit Status:** A command's numeric status indicates success or failure; zero conventionally means success.  
  `exit 0`

- **`$?`:** Contains the exit status of the most recently executed command or pipeline.  
  `ls; echo $?`

## 2.2 Variables

- **Declaring and Assigning Variables:** Assign values using `name=value` without spaces around `=`.  
  `name="Ayush"`

- **Accessing Variables:** Prefix a variable name with `$` to expand its value.  
  `echo "$name"`

- **Variable Naming Rules:** Use valid shell identifiers, typically letters, digits, and underscores, with no leading digit.  
  `user_name="Ayush"`

- **Strings and Numbers:** Variables store text; arithmetic contexts can interpret suitable values numerically.  
  `age=21; echo "$age"`

- **Single vs Double Quotes:** Single quotes preserve literal characters; double quotes allow variable and command substitution.  
  `name="Ayush"; echo "Hello $name"`

- **Environment Variables:** Environment variables are values made available to processes through their inherited environment.  
  `printenv PATH`

- **Local Shell vs Exported Variables:** Ordinary shell variables stay within the shell unless exported to child processes.  
  `name="Ayush"; export name`

- **`export`:** Marks variables for inclusion in the environment of subsequently launched child processes.  
  `export APP_ENV=development`

- **`readonly`:** Marks a variable as read-only in the current shell.  
  `readonly PI=3.14`

- **Command Substitution:** `$(command)` captures a command's standard output as text.  
  `today=$(date +%F); echo "$today"`

- **`$0`:** Contains the script name or invocation path.  
  `echo "$0"`

- **`$1`:** Contains the first positional argument.  
  `echo "$1"`

- **`$#`:** Contains the number of positional arguments.  
  `echo "$#"`

- **`$@`:** Expands to all positional arguments as separate words when quoted as `"$@"`.  
  `printf '<%s>\n' "$@"`

- **`$?`:** Contains the last command's exit status.  
  `echo "$?"`

- **`$$`:** Contains the current shell's process ID.  
  `echo "$$"`

- **Default Values and Parameter Expansion:** `${var:-default}` supplies a default when a variable is unset or empty.  
  `echo "${USER_NAME:-Guest}"`

- **`read`:** Reads user input into a variable.  
  `read -r -p "Name: " name; echo "$name"`

- **`unset`:** Removes a variable or function definition from the current shell.  
  `unset name`

## 2.3 Conditions

- **`if`:** Executes a block when a condition succeeds.  
  `if [[ -f file.txt ]]; then echo "Exists"; fi`

- **`if-else`:** Chooses between two branches based on a condition.  
  `if [[ -f file.txt ]]; then echo "Yes"; else echo "No"; fi`

- **`if-elif-else`:** Tests multiple conditions in sequence.  
  `if (( n > 0 )); then echo "Positive"; elif (( n < 0 )); then echo "Negative"; else echo "Zero"; fi`

- **Nested Conditions:** An `if` statement can contain another `if` statement.  
  `if [[ -f file.txt ]]; then if [[ -r file.txt ]]; then echo "Readable"; fi; fi`

- **`test`:** Evaluates a condition and returns a success or failure exit status.  
  `test -f file.txt && echo "Exists"`

- **`[ ]`:** A command-style syntax for testing conditions; spaces are required inside the brackets.  
  `[ -d project ] && echo "Directory exists"`

- **`[[ ]]`:** Bash conditional syntax supporting pattern matching and safer string comparisons.  
  `[[ "$name" == A* ]] && echo "Starts with A"`

- **Numeric Comparisons:** `-eq`, `-ne`, `-gt`, `-lt`, `-ge`, and `-le` compare integers in test expressions.  
  `[[ "$a" -gt "$b" ]] && echo "a is greater"`

- **String Comparisons:** `=`, `!=`, `-z`, and `-n` compare strings or check whether they are empty.  
  `[[ -n "$name" ]] && echo "Not empty"`

- **File Tests:** `-f`, `-d`, `-e`, `-r`, `-w`, and `-x` test file type, existence, or access permissions.  
  `[[ -f file.txt && -r file.txt ]] && echo "Readable file"`

- **Logical Operators:** `&&` means AND, `||` means OR, and `!` means NOT in conditional expressions.  
  `[[ -f file.txt && -r file.txt ]]`

- **Arithmetic Conditions:** `(( ))` evaluates integer arithmetic expressions and returns a condition status.  
  `(( count > 10 )) && echo "Large"`

- **`case`:** Selects a matching branch from multiple pattern alternatives.  
  `case "$choice" in start) echo "Starting";; stop) echo "Stopping";; *) echo "Unknown";; esac`

- **Checking Command Success or Failure:** Use `if command` to branch according to its exit status.  
  `if grep -q "error" app.log; then echo "Found"; else echo "Not found"; fi`

## 2.4 Loops

- **`for` Loop:** Repeats commands for each item in a list.  
  `for x in a b c; do echo "$x"; done`

- **`while` Loop:** Repeats while a condition succeeds.  
  `while (( n < 5 )); do echo "$n"; ((n++)); done`

- **`until` Loop:** Repeats until a condition succeeds.  
  `until (( n >= 5 )); do echo "$n"; ((n++)); done`

- **Iterating Over Lists and Arrays:** Processes each element of a list or Bash array.  
  `arr=(red blue); for x in "${arr[@]}"; do echo "$x"; done`

- **Iterating Over Files:** Processes filenames matching a glob pattern.  
  `for f in ./*.txt; do [[ -f "$f" ]] && echo "$f"; done`

- **Iterating Over Command Output:** Processes output lines using a loop or a suitable text-processing command.  
  `while IFS= read -r line; do echo "$line"; done < file.txt`

- **C-Style `for` Loop:** Uses initialization, a condition, and an update expression.  
  `for ((i=0; i<5; i++)); do echo "$i"; done`

- **Nested Loops:** Places one loop inside another to process combinations or multidimensional data.  
  `for i in 1 2; do for j in a b; do echo "$i$j"; done; done`

- **`break`:** Exits the innermost loop immediately.  
  `for i in 1 2 3; do (( i == 2 )) && break; echo "$i"; done`

- **`continue`:** Skips the remaining commands in the current iteration.  
  `for i in 1 2 3; do (( i == 2 )) && continue; echo "$i"; done`

- **Infinite Loop:** Repeats continuously until interrupted or explicitly terminated.  
  `while true; do date; sleep 5; done`

- **Loop Control with Conditions:** Uses conditions to decide when to continue, skip, or exit iterations.  
  `for i in {1..10}; do (( i % 2 == 0 )) && echo "$i"; done`

- **Reading Files Line by Line:** Uses `read -r` to preserve backslashes and process each line safely.  
  `while IFS= read -r line; do printf '%s\n' "$line"; done < file.txt`

## 2.5 Functions

- **Defining Functions:** Groups commands under a reusable function name.  
  `greet() { echo "Hello"; }`

- **Calling Functions:** Executes a previously defined function by its name.  
  `greet() { echo "Hello"; }; greet`

- **Passing Arguments:** Function arguments are accessed through positional parameters such as `$1` and `$2`.  
  `greet() { echo "Hello $1"; }; greet Ayush`

- **Local Variables:** `local` restricts a variable's scope to the function and its dynamically scoped callees in Bash.  
  `demo() { local x=10; echo "$x"; }; demo`

- **Returning Exit Status:** `return` sets a function's status code, conventionally from 0 to 255.  
  `check() { return 0; }; check; echo "$?"`

- **Capturing Function Output:** Command substitution captures the function's standard output.  
  `greet() { echo "Hello"; }; result=$(greet); echo "$result"`

- **Function Scope:** Function variables and positional parameters follow shell-specific scope rules.  
  `demo() { local value=5; echo "$value"; }; demo`

- **Reusing Functions:** A function can be called repeatedly to avoid duplicating logic.  
  `square() { echo "$(( $1 * $1 ))"; }; square 4; square 5`

- **Handling Function Errors:** Check a function's exit status and handle failures explicitly.  
  `deploy() { command_that_may_fail; }; if deploy; then echo "OK"; else echo "Failed"; fi`

## 2.6 Arguments

- **Command-Line Arguments:** `$1`, `$2`, and `$3` access the first three positional arguments.  
  `echo "$1 $2 $3"`

- **Script Name (`$0`):** Identifies how the script was invoked.  
  `echo "$0"`

- **Argument Count (`$#`):** Reports the number of positional arguments.  
  `echo "$#"`

- **All Arguments (`$@`):** Represents all positional arguments, preserving their separation when quoted as `"$@"`.  
  `printf '%s\n' "$@"`

- **`"$@"` vs `"$*"`:** `"$@"` expands to separate quoted arguments; `"$*"` combines them into one string separated by the first character of `IFS`.  
  `printf '<%s>\n' "$@"`

- **`shift`:** Removes the first positional parameter and shifts the remaining arguments left.  
  `shift`

- **Validating Arguments:** Checks that required arguments are present and valid.  
  `[[ $# -ge 1 ]] || { echo "Usage: $0 FILE"; exit 1; }`

- **Default Argument Values:** Uses a fallback value when an argument is missing or empty.  
  `file="${1:-input.txt}"`

- **Missing or Invalid Arguments:** Reports invalid input and exits with a nonzero status.  
  `[[ $# -eq 1 ]] || { echo "Usage: $0 FILE"; exit 2; }`

- **`getopts`:** Parses short command-line options and flags in Bash and other POSIX-style shells.  
  `while getopts ":f:v" opt; do case "$opt" in f) file="$OPTARG";; v) verbose=1;; *) exit 2;; esac; done`

- **Usage Messages:** Explains how a script should be invoked.  
  `echo "Usage: $0 [-v] -f FILE"`

- **Help Options:** A `-h` or `--help` option can display usage information and exit.  
  `[[ "${1:-}" == "-h" ]] && { echo "Usage: $0 FILE"; exit 0; }`

## 2.7 Pipes & Redirection

- **Standard Input (`stdin`):** File descriptor `0`, from which a command reads input.  
  `sort < names.txt`

- **Standard Output (`stdout`):** File descriptor `1`, where normal command output is written.  
  `echo "Hello" > output.txt`

- **Standard Error (`stderr`):** File descriptor `2`, used for error and diagnostic messages.  
  `ls missing 2> errors.txt`

- **Output Redirection (`>`):** Redirects standard output to a file and truncates it first.  
  `echo "Hello" > output.txt`

- **Append Redirection (`>>`):** Adds standard output to the end of a file.  
  `echo "Next line" >> output.txt`

- **Input Redirection (`<`):** Reads command input from a file.  
  `wc -l < file.txt`

- **Error Redirection (`2>`):** Redirects standard error to a file.  
  `find /root -type f 2> errors.txt`

- **Redirecting Both Streams (`&>`):** In Bash, redirects both standard output and standard error to the same file.  
  `command &> output.log`

- **Alternative Combined Redirection:** Redirects standard output first and then standard error to the same destination.  
  `command > output.log 2>&1`

- **Pipes (`|`):** Connect standard output of one command to standard input of another.  
  `ps aux | grep python`

- **Combining Commands:** Chains commands so one command's output or status can feed the next operation.  
  `cat file.txt | sort | uniq`

- **`/dev/null`:** A special device that discards written data.  
  `command > /dev/null 2>&1`

- **Here Document (`<<EOF`):** Supplies multiple lines of input directly to a command.  
  `cat <<EOF`
  `Hello`
  `Linux`
  `EOF`

- **Here String (`<<<`):** Supplies a single string as standard input in Bash.  
  `grep "Linux" <<< "Linux is powerful"`

- **Process Substitution:** Exposes command output or input as a file-like path, commonly using `/dev/fd`.  
  `diff <(sort a.txt) <(sort b.txt)`

- **Pipeline Exit Status (`PIPESTATUS`):** Bash array containing exit statuses of commands in the most recent foreground pipeline.  
  `false | true; echo "${PIPESTATUS[@]}"`

- **`&&`, `||`, `;`:** Run commands based on success, failure, or simple sequential order.  
  `mkdir demo && cd demo || echo "Failed"; pwd`

## 2.8 Basic Automation Scripts

- **Automating Repetitive Tasks:** Uses scripts to execute recurring operations consistently.  
  `for i in {1..3}; do date; done`

- **File and Directory Management:** Automates creating, moving, and organizing files and directories.  
  `mkdir -p backups`

- **Batch File Processing:** Applies the same operation to multiple files.  
  `for f in ./*.txt; do [[ -f "$f" ]] && wc -l "$f"; done`

- **File Existence and Permission Checks:** Tests whether files exist and have the required access permissions.  
  `[[ -f file.txt && -r file.txt ]] && echo "Ready"`

- **Backup Scripts:** Copies important files into a backup location, optionally with timestamps.  
  `tar -czf "backup-$(date +%F).tar.gz" project/`

- **Log File Monitoring:** Watches log files for new entries or matching errors.  
  `tail -F app.log | grep --line-buffered -i "error"`

- **Disk Space Monitoring:** Checks filesystem capacity and reports usage.  
  `df -h`

- **Process and Service Checks:** Verifies whether a process or managed service is running.  
  `systemctl is-active --quiet cron && echo "Running" || echo "Not active"`

- **User Input and Validation:** Collects input and checks that it meets expected requirements.  
  `read -r -p "Name: " name; [[ -n "$name" ]] || exit 1`

- **Date and Timestamp Handling:** Generates timestamps for logs, filenames, and scheduled jobs.  
  `date '+%Y-%m-%d_%H-%M-%S'`

- **Error Handling and Exit Codes:** Stops or branches when a command fails and returns meaningful status codes.  
  `mkdir project || exit 1`

- **Logging Script Output:** Records script messages and errors in a log file.  
  `echo "$(date '+%F %T') Task completed" >> task.log`

- **Command Failure Handling:** Uses conditional execution to respond to failed commands.  
  `if cp source.txt backup.txt; then echo "Success"; else echo "Copy failed"; fi`

- **Scheduling with `cron`:** Runs commands automatically at configured times using a user's crontab.  
  `crontab -e`

  Example cron entry (runs every day at 2 AM):

  ```cron
  0 2 * * * /home/user/backup.sh >> /home/user/backup.log 2>&1
  ```

- **Environment Variables in Automation:** Supplies configuration to scripts through environment variables.  
  `APP_ENV=production ./script.sh`

- **Safe Scripting Practices:** Quote variable expansions, validate input, handle errors, and avoid unsafe destructive operations.  
  `rm -- "$filename"`

- **Idempotency:** An operation is idempotent if repeating it produces the same intended final state.  
  `mkdir -p /tmp/myapp`

- **Debugging with `bash -x`:** Prints commands and their expanded arguments as Bash executes a script.  
  `bash -x script.sh`

- **ShellCheck:** A static analyzer that identifies common shell scripting mistakes and portability issues.  
  `shellcheck script.sh`

- **Reusable and Maintainable Scripts:** Organizes code into functions, uses meaningful names, and documents assumptions.  
  `bash -n script.sh`

---

# Quick Revision: Most Important Commands

| Task | Command |
|---|---|
| Current directory | `pwd` |
| List hidden files | `ls -la` |
| Create directory | `mkdir -p project` |
| Find files | `find . -name "*.txt"` |
| Search file content | `grep -in "error" app.log` |
| Read live logs | `tail -f app.log` |
| Check disk space | `df -h` |
| Check directory size | `du -sh folder/` |
| Check processes | `ps aux` |
| Monitor resources | `top` |
| Check listening ports | `sudo ss -lntup` |
| Change permissions | `chmod 755 script.sh` |
| Change ownership | `sudo chown user:group file.txt` |
| Check service | `systemctl status nginx` |
| Read service logs | `journalctl -u nginx` |
| Check exit status | `echo $?` |
| Run script | `bash script.sh` |
| Debug script | `bash -x script.sh` |
| Validate Bash syntax | `bash -n script.sh` |
| Analyze script | `shellcheck script.sh` |
| Schedule tasks | `crontab -e` |
| Show command help | `man ls` |

# Important Notes

1. **Use `sudo` carefully:** It grants elevated privileges and can make destructive changes.
2. **Quote variables:** Prefer `"$filename"` over `$filename` to preserve spaces and prevent unwanted word splitting.
3. **Be careful with `rm -r`:** Recursive deletion can permanently remove many files.
4. **Check exit codes:** `0` normally means success; nonzero normally means failure.
5. **Understand permissions:** `chmod 644` means owner can read/write; group and others can read.
6. **Understand pipes:** Ordinary pipelines pass standard output, not standard error, unless explicitly redirected.
7. **Know your distribution:** Log filenames, service names, and installed commands vary across Linux distributions.
8. **Test scripts first:** Use `bash -n script.sh` for syntax checking and `shellcheck script.sh` for static analysis.



Important ss commands
Command	Meaning
ss -tuln	Show listening TCP and UDP ports numerically
ss -tulpn	Show listening TCP/UDP ports and process information (usually needs sudo for full details)
ss -tan	Show all TCP sockets, including non-listening connections
ss -tln	Show listening TCP ports only
ss -uln	Show UDP sockets numerically
ss -tn state established	Show established TCP connections
sudo ss -lntp	Show listening TCP ports and associated processes
sudo ss -lunp	Show UDP sockets and associated processes

What does ss -tulpn mean?
- -t → TCP sockets
- -u → UDP sockets
- -l → Listening sockets
- -p → Process information
- -n → Numeric IP addresses and port numbers



- sudo → Runs a command with administrator privileges.
- apt → Advanced Package Tool, which manages software packages.
- install, update, remove → Actions performed by apt.
Important sudo apt commands
Command	One-line definition
sudo apt update	Refreshes the local package index from configured repositories.
sudo apt upgrade	Upgrades installed packages to newer available versions.
sudo apt install nginx	Installs the Nginx web server.
sudo apt remove nginx	Removes Nginx but may leave its configuration files.
sudo apt purge nginx	Removes Nginx and its system package configuration files.
sudo apt autoremove	Removes automatically installed packages no longer needed.
sudo apt search python3	Searches available package metadata for Python 3-related packages.
sudo apt show nginx	Displays information about the Nginx package.
sudo apt list --installed	Lists installed packages.