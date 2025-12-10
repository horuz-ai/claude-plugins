---
allowed-tools: Bash(git:*), Bash(rm:*), Bash(ls:*)
description: Remove a Git worktree (interactive)
argument-hint: "[worktree-name]"
---

# Remove Worktree

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- All worktrees: !`git worktree list 2>/dev/null || echo "No worktrees found"`
- Current branch: !`git branch --show-current 2>/dev/null`

## Arguments

- **Worktree name:** $1 (optional) - The folder name of the worktree to remove (e.g., `feat-new-feature` or `pr-123`)

## Your Task

Safely remove a Git worktree through an interactive workflow.

### Steps to execute:

1. **If $1 is empty or not provided:**
   - Present the list of available worktrees in a clear, numbered format (excluding the main worktree)
   - Ask the user: "¿Cuál worktree quieres eliminar?"
   - Wait for user response before proceeding
   - **STOP HERE** - do not continue until user responds

2. **Once you have a worktree name (from $1 or user selection):**
   - Verify it exists in the worktree list
   - If not found, show available worktrees and exit

3. **Check for uncommitted changes:**
   - Run `git -C ../$1 status --porcelain`
   - If there are uncommitted changes, **STOP and warn the user**
   - Ask: "Este worktree tiene cambios sin commit. ¿Quieres perderlos? (sí/no)"
   - If user says no, abort the operation

4. **Get the branch name before removal:**
   - Store the branch name associated with this worktree for later

5. **Remove the worktree:**
   - Run `git worktree remove ../$1`
   - If that fails due to untracked files, ask user if they want to force: `git worktree remove --force ../$1`

6. **Ask about deleting the branch:**
   - Ask: "¿Quieres también eliminar el branch '[branch-name]'? (sí/no)"
   - Wait for user response
   - If user says yes:
     - Check if branch is merged: `git branch --merged | grep [branch-name]`
     - If merged, delete with: `git branch -d [branch-name]`
     - If not merged, warn and ask for confirmation: "El branch no está mergeado. ¿Estás seguro? (sí/no)"
     - If confirmed, use `git branch -D [branch-name]`
   - If user says no, skip branch deletion

7. **Clean up worktree references:**
   - Run `git worktree prune` to clean up stale worktree references

8. **Report success:**
   - Confirm worktree removed
   - Confirm branch deleted (if applicable)
   - Show remaining worktrees

## Notes

- This is an INTERACTIVE command - always wait for user input at decision points
- NEVER force-remove a worktree with uncommitted changes without explicit user confirmation
- The main worktree (bare repo or primary clone) cannot be removed
- If the worktree directory was manually deleted, use `git worktree prune` to clean up
