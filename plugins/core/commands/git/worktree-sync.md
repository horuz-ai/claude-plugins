---
allowed-tools: Bash(git:*), Bash(pnpm:*)
description: Sync a worktree with the latest changes from the default/base branch
argument-hint: "<worktree-name> [base-branch]"
---

# Sync Worktree with Base Branch

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- All worktrees: !`git worktree list 2>/dev/null || echo "No worktrees found"`
- Remote default branch: !`git remote show origin 2>/dev/null | grep 'HEAD branch' | sed 's/.*: //' || echo "unknown"`

## Arguments

- **Worktree name:** $1 (required) - The folder name of the worktree to sync (e.g., `feat-new-feature`)
- **Base branch:** $2 (optional) - The branch to rebase from. If not provided, auto-detect from remote.

## Your Task

Update a worktree with the latest changes from the base branch.

### Steps to execute:

1. **Determine the base branch:**
   - If $2 is provided, use $2 as the base branch
   - If $2 is NOT provided, detect the default branch using: `git remote show origin | grep 'HEAD branch' | sed 's/.*: //'`
   - This will correctly detect `main`, `master`, `develop`, or whatever the repo uses

2. **Fetch latest from origin:**
   - Run `git fetch origin` from the main repo

3. **Navigate to the worktree:**
   - Change to `../$1`

4. **Check for uncommitted changes:**
   - Run `git status --porcelain`
   - If there are changes, stash them: `git stash push -m "worktree-sync auto-stash"`

5. **Rebase on base branch:**
   - Run `git rebase origin/[base-branch]`
   - If rebase fails due to conflicts, abort and notify user

6. **Restore stashed changes:**
   - If we stashed changes earlier, run `git stash pop`

7. **Reinstall dependencies if needed:**
   - Check if package.json or pnpm-lock.yaml changed: `git diff HEAD@{1} --name-only | grep -E "(package.json|pnpm-lock.yaml)"`
   - If they changed, run `pnpm install`

8. **Report success:**
   - Show which base branch was used
   - Show how many commits were applied
   - Show if dependencies were reinstalled
   - Show if there were stashed changes restored

## Notes

- This uses rebase by default for a cleaner history
- If the user prefers merge, they should do it manually
- If rebase has conflicts, the user will need to resolve manually
- The default branch is auto-detected from the remote, not assumed to be `main`
