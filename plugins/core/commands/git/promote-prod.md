---
allowed-tools: Bash(git:*)
description: "Promote staging to production with version tag"
disable-model-invocation: true
---

# Promote Staging → Production

⚠️ **This deploys to PRODUCTION.**

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

### 1. Check state
- If uncommitted changes: **Stop** → "Stash or commit first."

### 2. Gather info
```bash
git fetch origin
git describe --tags --abbrev=0
git log origin/main..origin/staging --oneline
git log origin/main..origin/staging --pretty=format:"%s"
```

If no commits: **Stop** → "Nothing to promote."

### 3. Determine version
Parse latest tag (or start at v1.0.0). Bump based on commits:
- `feat!:` or BREAKING → **MAJOR** (v2.0.0)
- `feat:` → **MINOR** (v1.1.0)
- `fix:`, `chore:` → **PATCH** (v1.0.1)

Show summary:
- Current version
- New version
- Commits being released

**Ask for confirmation.**

### 4. Merge
```bash
git checkout main
git pull origin main
git merge origin/staging --no-ff -m "chore: release {version}"
```

### 5. Handle conflicts
Same as promote-staging: **Stop on conflicts**, show each one, wait for approval.

### 6. Tag and push
```bash
git tag -a {version} -m "Release {version}"
git push origin main
git push origin {version}
git checkout dev
```

Confirm the release with version number and key changes.