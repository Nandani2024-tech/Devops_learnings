# Git & GitHub — Commands Cheat Sheet

## 1. Git vs GitHub

- **Git:** A distributed version control system that tracks changes in files.
  - Example: `git --version`
- **GitHub:** An online platform for hosting Git repositories and collaborating with others.
  - Example: `git clone https://github.com/username/repository.git`
- **Check Git Version:** Displays the installed Git version.
  - Example: `git --version`
- **Get Command Help:** Displays documentation for a Git command.
  - Example: `git help commit`

## 2. Repository & Commits

### Repository Initialization and Cloning

- **Initialize Repository:** Creates a new Git repository in the current directory.
  - Example: `git init`
- **Clone Repository:** Downloads a remote repository to your local machine.
  - Example: `git clone https://github.com/username/project.git`
- **Check Repository Status:** Shows modified, staged, and untracked files.
  - Example: `git status`
- **Show Repository Root:** Displays the root directory of the current repository.
  - Example: `git rev-parse --show-toplevel`

### Adding and Committing Changes

- **Stage a File:** Adds a specific file to the staging area.
  - Example: `git add solution.sh`
- **Stage All Changes:** Stages all modifications, deletions, and untracked files in the current directory and its subdirectories.
  - Example: `git add -A`
- **Commit Changes:** Records staged changes with a message.
  - Example: `git commit -m "Add solution script"`
- **Commit with Author Name and Email:** Records a commit using explicitly specified author details.
  - Example: `git -c user.name="Nandani" -c user.email="nandani@example.com" commit -m "Add solution script"`
- **Set Global Author Name:** Sets the default author name for future commits.
  - Example: `git config --global user.name "Nandani"`
- **Set Global Author Email:** Sets the default author email for future commits.
  - Example: `git config --global user.email "nandani@example.com"`
- **Check Author Name:** Displays the configured Git author name.
  - Example: `git config user.name`
- **Check Author Email:** Displays the configured Git author email.
  - Example: `git config user.email`
- **Show Last Commit:** Displays the latest commit and its changes.
  - Example: `git show HEAD`
- **Amend Last Commit:** Replaces the latest commit with a new commit containing the current staged changes and optionally an updated message.
  - Example: `git commit --amend -m "Update solution script"`
- **Unstage a File:** Removes a file from staging without discarding its changes.
  - Example: `git restore --staged solution.sh`
- **Discard Uncommitted File Changes:** Restores a tracked file to its last committed state, permanently discarding its unstaged modifications.
  - Example: `git restore solution.sh`

### Viewing Commit History

- **View Commit History:** Displays the repository's commit history.
  - Example: `git log`
- **View Compact Commit History:** Displays each commit on one line.
  - Example: `git log --oneline`
- **View the 5 Most Recent Commits:** Displays only the five latest commits.
  - Example: `git log -5 --oneline`
- **View the 10 Most Recent Commits:** Displays only the ten latest commits.
  - Example: `git log -10 --oneline`
- **Count All Commits:** Counts commits reachable from the current `HEAD`.
  - Example: `git rev-list --count HEAD`
- **Count the 5 Most Recent Commits:** Counts commits displayed by limiting the current history to five entries.
  - Example: `git rev-list --count --max-count=5 HEAD`
- **Show the Latest Commit:** Displays details of the latest commit.
  - Example: `git log -1`
- **Show Commit Hashes:** Displays full commit hashes.
  - Example: `git log --format="%H"`
- **Show Commit Hash and Message:** Displays abbreviated hashes and commit messages.
  - Example: `git log --format="%h %s"`
- **Show Commit Author:** Displays the author name and email for each commit.
  - Example: `git log --format="%h | %an | %ae | %s"`
- **Show Commit Date:** Displays commit hashes, dates, and messages.
  - Example: `git log --date=short --format="%h | %ad | %s"`
- **Find Commits by Author Name:** Displays commits authored by a particular person.
  - Example: `git log --author="Nandani" --oneline`
- **Find Commits by Author Email:** Displays commits authored using a particular email address.
  - Example: `git log --author="nandani@example.com" --oneline`
- **Find Commits by Exact Message Text:** Searches commit messages for a specified text.
  - Example: `git log --grep="bug fix" --oneline`
- **Find Commits by Message Pattern (Case-Insensitive):** Searches commit messages without distinguishing uppercase and lowercase.
  - Example: `git log --grep="login" --regexp-ignore-case --oneline`
- **Find Commits by Author and Message:** Filters history by both author and commit message.
  - Example: `git log --author="Nandani" --grep="feature" --oneline`
- **Find Commits That Changed a File:** Displays commits that modified a particular file.
  - Example: `git log --oneline -- solution.sh`
- **Find Commits by Date:** Displays commits made after a specified date.
  - Example: `git log --since="2026-01-01" --oneline`
- **Find Commits Within a Date Range:** Displays commits made between two dates.
  - Example: `git log --since="2026-01-01" --until="2026-06-30" --oneline`
- **Search Commit Contents:** Finds commits whose diffs contain a specified string.
  - Example: `git log -S"API_KEY" --oneline`
- **Search Commit Diffs Using a Pattern:** Finds commits whose changes match a regular expression.
  - Example: `git log -G"password|token" --oneline`
- **Show Commit Statistics:** Displays the number of changed files and lines for each commit.
  - Example: `git log --stat`
- **Show Commit Differences:** Displays changes introduced by a particular commit.
  - Example: `git show abc1234`
- **Compare Two Commits:** Displays the differences between two commits.
  - Example: `git diff abc1234 def5678`

> Note: Replace example author names, emails, dates, file names, and commit hashes with your actual values. `--author` searches author metadata, while `--grep` searches commit messages. Git commit history records the author and committer separately.

## 3. Branching

- **List Local Branches:** Displays all local branches.
  - Example: `git branch`
- **List All Branches:** Displays local and remote-tracking branches.
  - Example: `git branch -a`
- **Create a Branch:** Creates a new branch without switching to it.
  - Example: `git branch feature-login`
- **Switch Branch:** Switches to an existing branch.
  - Example: `git switch feature-login`
- **Create and Switch Branch:** Creates a branch and switches to it.
  - Example: `git switch -c feature-login`
- **Rename Current Branch:** Renames the currently checked-out branch.
  - Example: `git branch -m feature-auth`
- **Delete a Merged Branch:** Deletes a local branch that Git considers safely merged.
  - Example: `git branch -d feature-login`
- **Force-Delete a Branch:** Deletes a local branch even if it contains unmerged changes.
  - Example: `git branch -D feature-login`
- **Show Current Branch:** Displays the name of the current branch.
  - Example: `git branch --show-current`
- **Compare Branches:** Displays changes between two branches.
  - Example: `git diff main..feature-login`
- **Show Branch Commit History:** Displays commits reachable from one branch but not another.
  - Example: `git log main..feature-login --oneline`

## 4. Merge & Rebase

### Merge

- **Merge a Branch:** Integrates the specified branch into the current branch.
  - Example: `git switch main && git merge feature-login`
- **Fast-Forward-Only Merge:** Merges only when the current branch can advance without creating a merge commit.
  - Example: `git merge --ff-only feature-login`
- **Create a Merge Commit:** Creates a merge commit when merging two branches, even if a fast-forward is possible.
  - Example: `git merge --no-ff feature-login`
- **Abort a Merge:** Cancels an in-progress merge and restores the pre-merge state when possible.
  - Example: `git merge --abort`

### Rebase

- **Rebase a Branch:** Replays the current branch's commits on top of another branch.
  - Example: `git switch feature-login && git rebase main`
- **Continue Rebase:** Continues a rebase after conflicts have been resolved and changes staged.
  - Example: `git add solution.sh && git rebase --continue`
- **Abort Rebase:** Cancels an in-progress rebase.
  - Example: `git rebase --abort`
- **Interactive Rebase:** Allows editing, reordering, squashing, or dropping recent commits.
  - Example: `git rebase -i HEAD~3`

> Important: Rebasing rewrites commit history. Avoid rebasing commits that others are already using unless your team agrees.

## 5. Pull Requests

- **Add a Remote:** Connects a local repository to a remote repository.
  - Example: `git remote add origin https://github.com/username/project.git`
- **List Remotes:** Displays configured remote repositories and their URLs.
  - Example: `git remote -v`
- **Push a Branch:** Uploads a local branch to the remote repository.
  - Example: `git push -u origin feature-login`
- **Fetch Remote Changes:** Downloads remote updates without integrating them into the current branch.
  - Example: `git fetch origin`
- **Pull Remote Changes:** Fetches changes and integrates them into the current branch.
  - Example: `git pull origin main`
- **Push New Commits:** Uploads local commits to the tracked remote branch.
  - Example: `git push`
- **Push After Rebase:** Updates a remote branch after rewriting its history; use only when appropriate.
  - Example: `git push --force-with-lease origin feature-login`
- **Remove a Remote-Tracking Reference:** Prunes references to remote branches that no longer exist on the remote.
  - Example: `git fetch --prune origin`

> A **Pull Request (PR)** is a GitHub collaboration feature for proposing, reviewing, and merging changes; it is created on GitHub's website or through the GitHub CLI, not by a standard `git` command alone.

## 6. Merge Conflicts

- **Check Conflicts:** Shows files with unresolved merge conflicts.
  - Example: `git status`
- **Show Conflict Markers:** Displays the conflict markers inside a conflicted file.
  - Example: `cat solution.sh`
- **Open a File to Resolve Conflicts:** Opens the conflicted file in a terminal editor.
  - Example: `nano solution.sh`
- **Mark a Conflict as Resolved:** Stages the file after resolving its conflicts.
  - Example: `git add solution.sh`
- **Complete a Merge:** Creates the merge commit after all conflicts are resolved.
  - Example: `git merge --continue`
- **Complete a Rebase:** Continues rebasing after resolving conflicts and staging the affected files.
  - Example: `git rebase --continue`
- **Abort a Merge:** Cancels the current merge.
  - Example: `git merge --abort`
- **Abort a Rebase:** Cancels the current rebase.
  - Example: `git rebase --abort`

Conflict markers typically look like this:

```text
<<<<<<< HEAD
Your current branch's changes
=======
Incoming branch's changes
>>>>>>> feature-login
```

Remove the markers, keep the intended final content, save the file, and stage it before continuing.

## 7. Basic Git Workflow

- **Check Current Changes:** Shows which files are modified, staged, or untracked.
  - Example: `git status`
- **Review Changes:** Displays unstaged modifications.
  - Example: `git diff`
- **Review Staged Changes:** Displays changes that will be included in the next commit.
  - Example: `git diff --staged`
- **Stage Changes:** Adds all changes to the staging area.
  - Example: `git add -A`
- **Commit Changes:** Records the staged changes.
  - Example: `git commit -m "Implement login validation"`
- **Pull Latest Changes:** Integrates updates from the remote branch.
  - Example: `git pull --rebase origin main`
- **Push Changes:** Uploads local commits to the remote branch.
  - Example: `git push`
- **Temporarily Save Changes:** Stashes tracked modifications and staged changes.
  - Example: `git stash`
- **List Stashes:** Displays saved stashes.
  - Example: `git stash list`
- **Restore Latest Stash:** Reapplies the latest stash and removes it from the stash list if successful.
  - Example: `git stash pop`
- **Apply Stash Without Removing It:** Reapplies the latest stash while retaining it in the stash list.
  - Example: `git stash apply`
- **Cherry-Pick a Commit:** Applies the changes from a specific commit to the current branch.
  - Example: `git cherry-pick abc1234`
- **Revert a Commit:** Creates a new commit that undoes the changes introduced by a specified commit.
  - Example: `git revert abc1234`
- **Reset to an Earlier Commit:** Moves the current branch reference to a previous commit and resets the index and working tree according to the selected mode.
  - Example: `git reset --soft HEAD~1`

> Caution: `git reset --hard HEAD~1` discards tracked working-tree changes and moves the current branch back one commit. Use it only when you understand the consequences.

## 8. .gitignore

- **Ignore Files:** Prevents specified untracked files from being added to Git.
  - Example: `echo ".env" >> .gitignore`
- **Ignore a Directory:** Excludes a directory and its contents from being tracked when untracked.
  - Example: `echo "node_modules/" >> .gitignore`
- **Check Ignored Files:** Lists files ignored by Git.
  - Example: `git status --ignored`
- **Check Why a File Is Ignored:** Displays the ignore rule responsible for a file being ignored.
  - Example: `git check-ignore -v .env`

> `.gitignore` does not automatically stop tracking a file that has already been committed. To stop tracking it while keeping the local file, use `git rm --cached .env` and commit the change.

## 9. Tags

- **List Tags:** Displays repository tags.
  - Example: `git tag`
- **Create a Tag:** Creates a lightweight tag for the current commit.
  - Example: `git tag v1.0.0`
- **Create an Annotated Tag:** Creates a tag with a message and tagger metadata.
  - Example: `git tag -a v1.0.0 -m "Release version 1.0.0"`
- **Push a Tag:** Uploads a specified tag to the remote.
  - Example: `git push origin v1.0.0`
- **Push All Tags:** Uploads all local tags to the remote.
  - Example: `git push origin --tags`
- **Delete a Local Tag:** Deletes a local tag.
  - Example: `git tag -d v1.0.0`

## 10. Git Configuration & Inspection

- **Show All Configuration:** Displays effective Git configuration values.
  - Example: `git config --list`
- **Show Configuration Sources:** Displays configuration values along with their source files.
  - Example: `git config --list --show-origin`
- **Set Default Branch Name:** Configures the initial branch name for newly initialized repositories.
  - Example: `git config --global init.defaultBranch main`
- **Show Remote Branches:** Displays remote-tracking branches.
  - Example: `git branch -r`
- **Show Recent Reference Updates:** Displays recent movements of local Git references, including branch changes and resets.
  - Example: `git reflog`
- **Check Repository Integrity:** Checks the connectivity and validity of objects in the repository.
  - Example: `git fsck --full`

## 11. Quick Revision — Most Important Commands

| Task | Command |
|---|---|
| Initialize repository | `git init` |
| Clone repository | `git clone <url>` |
| Check status | `git status` |
| Stage all changes | `git add -A` |
| Commit changes | `git commit -m "message"` |
| View recent commits | `git log -5 --oneline` |
| Count commits | `git rev-list --count HEAD` |
| Find commits by author | `git log --author="Name" --oneline` |
| Find commits by message | `git log --grep="keyword" --oneline` |
| Show commit author | `git log -1 --format="%an <%ae>"` |
| Create a branch | `git switch -c <branch>` |
| Merge a branch | `git merge <branch>` |
| Rebase a branch | `git rebase <branch>` |
| Add a remote | `git remote add origin <url>` |
| Push a branch | `git push -u origin <branch>` |
| Fetch changes | `git fetch origin` |
| Pull changes | `git pull` |
| Compare changes | `git diff` |
| Undo a commit safely | `git revert <commit>` |
| Inspect latest commit | `git show HEAD` |
| Save temporary changes | `git stash` |
| Inspect reference history | `git reflog` |




**Definition:** Searches commit messages across all branches (`--all`) for the words matching `fix` or `bug` (`--grep`), ignoring uppercase and lowercase (`-i`).

**Example:**
git log --all --grep="fix\|bug" -i --oneline

**Breakdown:**
- `git log` → Displays commit history.
- `--all` → Searches commits reachable from all references, including local and remote-tracking branches.
- `--grep="fix\|bug"` → Matches commit messages containing `fix` or `bug` (the `\|` means OR in Git's default regex mode).
- `-i` → Makes the search case-insensitive, matching `FIX`, `Bug`, etc.
- `--oneline` → Displays each matching commit in a compact, single-line format.