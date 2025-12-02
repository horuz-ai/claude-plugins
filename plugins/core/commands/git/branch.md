---
allowed-tools: Bash(git:*), Read, Glob
description: "Create a new feature branch from dev"
argument-hint: "[task description]"
---

# Create Feature Branch from Dev

You are helping a developer start new work by creating a properly named feature branch from the `dev` branch.

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Git user name: !`git config user.name`
- Remote dev branch status: !`git fetch origin dev 2>/dev/null && git log HEAD..origin/dev --oneline 2>/dev/null | head -5`

## Task Description (from user)

"$ARGUMENTS"

## Your Task

Follow these steps precisely:

### Step 1: Ensure Clean State
- Check if there are uncommitted changes (from git status above)
- If there ARE uncommitted changes, STOP and inform the developer:
  - "You have uncommitted changes. Please stash them with `git stash` or use `/commit` first before creating a new branch."
- If clean, proceed to Step 2

### Step 2: Switch to Dev and Pull Latest
Execute these commands:
```bash
git checkout dev
git pull origin dev
```

### Step 3: Determine Branch Name

**If task description was provided ($ARGUMENTS is not empty):**
- Analyze the task description to determine:
  - **Branch type**: Choose ONE based on the task intent:
    - `feature/` - New functionality, enhancements, additions
    - `bugfix/` - Fixing a bug or issue
    - `hotfix/` - Urgent production fix
    - `chore/` - Maintenance, refactoring, dependencies, config
  - **Branch name**: Create a concise kebab-case name (2-5 words max) that describes the work
  - Format: `{type}/{descriptive-name}`
  - Examples:
    - "add user authentication" → `feature/user-authentication`
    - "fix login button not working" → `bugfix/login-button-click`
    - "update dependencies" → `chore/update-dependencies`
    - "urgent fix for payment processing" → `hotfix/payment-processing`

**If NO task description was provided ($ARGUMENTS is empty):**
- Use the git user name to create a personal workspace branch
- Format: `feature/{git-username-kebab-case}`
- Example: If git user is "John Doe" → `feature/john-doe`
- Convert spaces to hyphens, lowercase everything, remove special characters

### Step 4: Create and Checkout the Branch
```bash
git checkout -b {branch-name}
```

### Step 5: Confirm to Developer
After creating the branch, inform the developer:
- The branch name that was created
- That they are now on the new branch
- Remind them to use `/commit` when ready to commit their changes

## Constraints

- NEVER create branches from `staging` or `main`
- ALWAYS pull latest `dev` before branching
- Branch names must be lowercase kebab-case
- Branch names should be descriptive but concise (max 50 characters)
- Do not include issue numbers unless explicitly mentioned in the task description