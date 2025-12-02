---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(pnpm:*), Bash(yarn:*), Bash(bun:*), Read, Glob, Grep
description: "Smart commit with branch validation, linting, and conventional commits"
---

# Smart Commit

You are helping a developer commit their changes following the organization's git workflow conventions.

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status`
- Git diff summary: !`git diff --stat HEAD 2>/dev/null || git diff --stat`
- Git diff (for understanding changes): !`git diff HEAD 2>/dev/null | head -200`
- Git user name: !`git config user.name`
- Recent commits on this branch: !`git log --oneline -5 2>/dev/null`
- Check if branch is merged to dev: !`git branch -r --contains HEAD 2>/dev/null | grep -q "origin/dev" && echo "MERGED_TO_DEV" || echo "NOT_MERGED"`
- Package manager detection: !`[ -f "bun.lockb" ] && echo "bun" || ([ -f "pnpm-lock.yaml" ] && echo "pnpm" || ([ -f "yarn.lock" ] && echo "yarn" || echo "npm"))`

## Protected Branches

These branches are protected and direct commits are NOT allowed:
- `dev` (default branch - must branch from here)
- `staging` (pre-production)
- `main` (production)

## Your Task

Analyze the context above and follow the appropriate scenario:

---

### SCENARIO A: On a Protected Branch (dev, staging, or main)

If the current branch is `dev`, `staging`, or `main`:

1. **Check for changes to commit**
   - If NO changes (git status is clean): Inform developer "Nothing to commit. Working tree clean."
   - If there ARE changes: Proceed to create a feature branch

2. **Analyze the changes to determine branch name**
   - Read the git diff to understand what the developer is working on
   - Determine the appropriate:
     - **Branch type**: `feature/`, `bugfix/`, `hotfix/`, or `chore/`
     - **Branch name**: Concise kebab-case description (2-5 words)

3. **Pull latest dev and create branch**
   ```bash
   git stash  # Temporarily stash changes
   git checkout dev
   git pull origin dev
   git checkout -b {type}/{branch-name}
   git stash pop  # Restore changes
   ```

4. **Proceed to run checks and commit** (continue to Validation Steps below)

---

### SCENARIO B: On a Personal Branch (feature/{username})

If the current branch matches the pattern `feature/{git-username}` (e.g., `feature/nelson-rosa`):

This is a temporary personal branch that should be renamed to something more descriptive.

1. **Analyze the changes to determine proper branch name**
   - Read the git diff to understand the work being done
   - Determine appropriate branch type and descriptive name

2. **Rename the branch**
   ```bash
   git branch -m {new-type}/{new-branch-name}
   ```

3. **Proceed to run checks and commit** (continue to Validation Steps below)

---

### SCENARIO C: On a Proper Feature Branch

If the current branch is already a properly named branch (e.g., `feature/user-authentication`, `bugfix/login-fix`):

1. **Check for changes to commit**
   - If NO changes: Inform developer "Nothing to commit. Working tree clean."
   - If there ARE changes: Proceed to Validation Steps below

---

### SCENARIO D: Branch Already Merged to Dev

If the context shows "MERGED_TO_DEV" and there are new changes:

1. **Inform the developer** that this branch has already been merged to dev
2. **Recommend** they run `/branch` to start fresh from dev with a new branch
3. **Do NOT commit** to a merged branch

---

## Validation Steps (Before Committing)

Before creating the commit, run these validation checks:

### Step 1: Run Linter
Based on the detected package manager, run:
```bash
{package-manager} run lint 2>&1 || echo "LINT_CHECK_DONE"
```

- If lint errors are found: **STOP** and inform the developer
  - Show the lint errors clearly
  - Ask them to fix the errors before committing
  - Do NOT proceed with the commit

- If lint passes or no lint script exists: Proceed to Step 2

### Step 2: Run Type Check (if TypeScript project)
Check if tsconfig.json exists, if so:
```bash
{package-manager} run typecheck 2>&1 || {package-manager} run type-check 2>&1 || npx tsc --noEmit 2>&1 || echo "TYPE_CHECK_DONE"
```

- If type errors are found: **STOP** and inform the developer
  - Show the type errors clearly
  - Ask them to fix the errors before committing
  - Do NOT proceed with the commit

- If type check passes or not a TypeScript project: Proceed to Step 3

### Step 3: Run Build Check
```bash
{package-manager} run build 2>&1 || echo "BUILD_CHECK_DONE"
```

- If build fails: **STOP** and inform the developer
  - Show the build errors clearly
  - Ask them to fix the errors before committing
  - Do NOT proceed with the commit

- If build passes or no build script: Proceed to Commit Step

---

## Commit Step

### Generate Conventional Commit Message

Based on the git diff, create a **single-line** commit message following Conventional Commits:

**Format:** `{type}({scope}): {description}`

**Types:**
- `feat` - New feature or functionality
- `fix` - Bug fix
- `chore` - Maintenance, dependencies, config
- `docs` - Documentation only
- `refactor` - Code change that neither fixes a bug nor adds a feature
- `test` - Adding or updating tests
- `style` - Code style changes (formatting, semicolons, etc.)
- `perf` - Performance improvement

**Scope:** Optional, short identifier for the area of code (e.g., `auth`, `api`, `ui`)

**Description:**
- Use imperative mood ("add" not "added" or "adds")
- Lowercase first letter
- No period at the end
- Max 72 characters total for the entire message

**Examples:**
- `feat(auth): add user login functionality`
- `fix(api): resolve null pointer in user service`
- `chore: update dependencies to latest versions`
- `refactor(ui): simplify button component logic`

### Execute Commit

```bash
git add -A
git commit -m "{conventional-commit-message}"
```

### Confirm to Developer

After successful commit, inform the developer:
- The commit message that was used
- The branch they are on
- Remind them to use `/pr` when ready to create a pull request

---

## Constraints

- NEVER commit directly to `dev`, `staging`, or `main`
- ALWAYS run lint and build checks before committing
- Commit messages MUST follow conventional commit format
- Commit messages MUST be a single line (no multi-line messages)
- If ANY validation fails, do NOT commit - inform the developer of the issues
- Do NOT skip validation steps even if developer asks to