---
allowed-tools: Bash(git:*)
description: "Create a feature branch from dev"
argument-hint: "[task description]"
---

# Create Branch from Dev

## Rule
All feature branches MUST be created from `dev`. Never branch from `staging` or `main`.

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

**If there are uncommitted changes:** Stop and tell the user to stash or commit first.

**Otherwise, execute:**

```bash
git checkout dev
git pull origin dev
git checkout -b {branch-name}
```

**Branch naming rules:**
- Analyze `$ARGUMENTS` or ask the user what they're working on
- Pick type: `feature/`, `bugfix/`, `hotfix/`, or `chore/`
- Create kebab-case name (2-4 words max)
- Examples: `feature/user-auth`, `bugfix/login-error`, `chore/update-deps`

After creating, confirm the branch name and remind to use `/commit` when ready.