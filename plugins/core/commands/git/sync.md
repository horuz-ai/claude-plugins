---
allowed-tools: Bash(git:*)
description: "Sync local dev with remote"
---

# Sync Dev Branch

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

### 1. Check for uncommitted changes
If there are uncommitted changes, ask the user:
- **Stash** them (`git stash` - can recover later with `git stash pop`)
- **Discard** them (`git checkout -- .` - permanently lost)
- **Cancel** the sync

Wait for their choice before proceeding.

### 2. Check for unpushed commits
If not on dev, check if current branch has unpushed commits:
```bash
git log origin/{current-branch}..HEAD --oneline
```

If there are unpushed commits, warn the user and ask if they want to:
- **Push first** (`git push origin {branch}`)
- **Continue anyway** (commits stay local)
- **Cancel**

### 3. Sync dev
```bash
git checkout dev
git pull origin dev
```

Confirm sync complete and show if there were new changes pulled.