---
allowed-tools: Bash(git:*), Bash(npm:*), Bash(pnpm:*), Bash(yarn:*), Bash(bun:*)
description: "Commit with validation and conventional commits"
---

# Smart Commit

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

### 1. Check branch
If on `dev`, `staging`, or `main`: **Stop** → "You're on a protected branch. Use `/branch` first."

### 2. Check for changes
If no changes: **Stop** → "Nothing to commit."

### 3. Run validations
Detect package manager (check for bun.lockb, pnpm-lock.yaml, yarn.lock, or use npm).

Run these two commands in parallel (as separate tool calls):
- `{pkg} run lint`
- `{pkg} run build`

If any errors: **Stop** and show them. Don't commit until fixed.

### 4. Commit
Read the diff to understand changes:
```bash
git diff HEAD
```

Create conventional commit message:
- Format: `{type}({scope}): {description}`
- Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`
- One line, imperative mood, max 72 chars
- Examples: `feat(auth): add login flow`, `fix(api): handle null response`

```bash
git add -A
git commit -m "{message}"
```

Confirm and remind to use `/pr` when ready.