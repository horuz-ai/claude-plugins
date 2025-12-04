---
allowed-tools: Bash(git:*), Bash(gh:*)
description: "Create a pull request to dev"
---

# Create Pull Request

## Context
- Current branch: !`git branch --show-current`
- Git status: !`git status --short`

## Task

### 1. Validate
- If on `dev`, `staging`, or `main`: **Stop** → "Use `/branch` first."
- If uncommitted changes: **Stop** → "Use `/commit` first."

### 2. Check commits and existing PR
```bash
git fetch origin
git log origin/dev..HEAD --oneline
gh pr view --json url
```
- If no commits ahead: **Stop** → "No commits to create PR for."
- If PR exists: Show URL and ask if they want to update it.

### 3. Push and create PR
```bash
git push -u origin {branch}
```

Analyze commits to generate:
- **Title:** `{type}: {summary}` (max 72 chars)
- **Body:** Use this template:

```markdown
## Summary
[2-3 sentences about what and why]

## Changes
- [Key change 1]
- [Key change 2]

## Type
- [ ] ✨ Feature
- [ ] 🐛 Bug fix
- [ ] 🧹 Chore

## Testing
- [ ] Tested locally
```

```bash
gh pr create --base dev --title "{title}" --body "{body}" --reviewer nelsonrosa3
```

Show the PR URL when done.