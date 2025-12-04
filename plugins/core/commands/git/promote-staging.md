---
allowed-tools: Bash(git:*)
description: "Promote dev to staging"
disable-model-invocation: true
---

# Promote Dev → Staging

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

### 1. Check state
- If uncommitted changes: **Stop** → "Stash or commit first."

### 2. Show what will be promoted
```bash
git fetch origin
git log origin/staging..origin/dev --oneline
```

If no commits: **Stop** → "Nothing to promote. Branches are in sync."

**Ask for confirmation before proceeding.**

### 3. Merge
```bash
git checkout staging
git pull origin staging
git merge origin/dev --no-ff -m "chore: promote dev to staging"
```

### 4. Handle conflicts
If conflicts occur: **Stop immediately.**

Show each conflict:
```bash
git diff --name-only --diff-filter=U
```

For each file, show the conflict and explain:
- What staging has
- What dev has  
- Your recommendation

**Wait for approval on each resolution.** Options:
- Accept staging
- Accept dev
- Custom merge
- Abort (`git merge --abort`)

### 5. Push and return
```bash
git push origin staging
git checkout dev
```

Confirm what was promoted.