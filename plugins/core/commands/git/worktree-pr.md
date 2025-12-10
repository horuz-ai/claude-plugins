---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(cp:*), Bash(pnpm:*), Bash(cursor:*), Bash(ls:*)
description: Create a Git worktree from a GitHub PR for local testing
argument-hint: "<pr-number>"
---

# Checkout PR into Worktree

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- Existing worktrees: !`git worktree list 2>/dev/null || echo "No worktrees"`
- Available .env files: !`ls -la .env* 2>/dev/null || echo "No .env files found"`
- GitHub CLI available: !`which gh 2>/dev/null && gh auth status 2>&1 | head -3 || echo "gh CLI not found or not authenticated"`

## Arguments

- **PR number:** $1 (required) - The GitHub PR number to checkout (e.g., `123`)

## Your Task

Create a Git worktree from an existing GitHub Pull Request for local testing.

### Steps to execute:

1. **Fetch PR information:**
   - Use `gh pr view $1 --json headRefName,title,number` to get PR details
   - Extract the branch name from `headRefName`

2. **Fetch the PR branch:**
   - Run `gh pr checkout $1 --detach` first to fetch the refs (then go back)
   - Or use `git fetch origin pull/$1/head:pr-$1`

3. **Create the worktree:**
   - Worktree folder name: `pr-$1` (e.g., `pr-123`)
   - Worktree path: `../pr-$1`
   - Create worktree: `git worktree add ../pr-$1 pr-$1` (using the fetched branch)

4. **Copy environment files:**
   - Copy all `.env*` files to the new worktree: `cp .env* ../pr-$1/`
   - If no .env files exist, skip this step

5. **Install dependencies:**
   - Change to the new worktree directory: `cd ../pr-$1`
   - Run `pnpm install`

6. **Open in Cursor:**
   - Run `cursor ../pr-$1` to open the PR worktree in Cursor

7. **Report success:**
   - Show PR number and title
   - Show the path to the new worktree
   - Show the branch name
   - List any .env files copied
   - Remind user: "When done testing, use `/wt-remove pr-$1` to clean up"

## Notes

- This requires the `gh` CLI to be installed and authenticated
- The worktree is created in detached HEAD state or tracking the PR branch
- If the PR has been updated, user may need to pull latest changes
- User should not push changes from this worktree unless they intend to contribute to the PR
