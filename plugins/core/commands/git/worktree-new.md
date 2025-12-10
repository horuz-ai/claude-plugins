---
allowed-tools: Bash(git:*), Bash(cp:*), Bash(pnpm:*), Bash(cursor:*), Bash(ls:*), Bash(mkdir:*)
description: Create a new Git worktree for a feature branch with full setup
argument-hint: "[branch-name] [base-branch]"
---

# Create New Feature Worktree

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- Existing worktrees: !`git worktree list 2>/dev/null || echo "No worktrees"`
- Existing branches: !`git branch -a 2>/dev/null | head -20`
- Current branch: !`git branch --show-current 2>/dev/null`
- Available .env files: !`ls -la .env* 2>/dev/null || echo "No .env files found"`

## Arguments

- **Branch name:** $1 (optional) - Name for the new feature branch. If not provided, auto-generate one.
- **Base branch:** $2 (optional) - Branch to base the worktree from. If not provided, auto-detect default branch.

## Your Task

Create a new Git worktree for feature development with full project setup.

### Steps to execute:

1. **Determine branch name:**
   - If $1 is provided, use it as the branch name
   - If $1 is NOT provided, generate a random branch name:
     - Format: `feat/[word]-[word]` (e.g., `feat/quick-orbit`, `feat/blue-spark`, `feat/nova-drift`)
     - Use creative, short, memorable word combinations (adjective-noun or noun-noun)
     - Verify the generated name doesn't already exist in worktrees or branches
     - Examples of good words: swift, pixel, lunar, cyber, flux, nexus, proto, micro, turbo, hyper, alpha, beta, spark, wave, pulse, core, sync, fast, lite, mini

2. **Determine base branch:**
   - If $2 is provided, use it as base
   - If $2 is NOT provided, detect default branch: `git remote show origin | grep 'HEAD branch' | sed 's/.*: //'`

3. **Determine worktree location:**
   - Get the git root directory
   - The new worktree should be created as a sibling directory to the current repo
   - Convert branch name to folder name (replace `/` with `-`, e.g., `feat/new-feature` → `feat-new-feature`)
   - Worktree path: `../[folder-name]`

4. **Create the worktree:**
   - Run: `git worktree add ../[folder-name] -b [branch-name] [base-branch]`

5. **Copy environment files:**
   - Copy all `.env*` files to the new worktree: `cp .env* ../[folder-name]/`
   - If no .env files exist, skip this step

6. **Install dependencies:**
   - Change to the new worktree directory
   - Run `pnpm install`

7. **Open in Cursor:**
   - Run `cursor ../[folder-name]` to open the new worktree in Cursor

8. **Report success:**
   - Show the path to the new worktree
   - Confirm branch name (especially important if auto-generated)
   - Show base branch used
   - List any .env files copied

## Notes

- If no branch name provided, just generate one and proceed - don't ask the user
- If the branch already exists, the command should fail gracefully with a helpful message
- If pnpm install fails, still report the worktree was created but note the install failure
- The user may need to run additional setup commands depending on the project
