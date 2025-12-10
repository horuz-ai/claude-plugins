---
allowed-tools: Bash(git:*), Bash(cursor:*), Bash(ls:*), Bash(cd:*)
description: Open an existing Git worktree in Cursor
argument-hint: "[worktree-name]"
---

# Open Worktree in Cursor

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- All worktrees: !`git worktree list 2>/dev/null || echo "No worktrees found"`

## Arguments

- **Worktree name:** $1 (optional) - The folder name of the worktree to open (e.g., `feat-new-feature` or `pr-123`)

## Your Task

Open an existing Git worktree in Cursor.

### Steps to execute:

1. **If $1 is empty or not provided:**
   - Present the list of available worktrees in a clear, numbered format
   - Ask the user: "¿Cuál worktree quieres abrir?"
   - Wait for user response before proceeding
   - **STOP HERE** - do not continue until user responds

2. **Once you have a worktree name (from $1 or user selection):**
   - Check if the worktree exists in the worktree list
   - If not found as a sibling `../$1`, search the full worktree list for a matching path

3. **Verify the path exists:**
   - If the worktree path doesn't exist on disk, report error and suggest running `git worktree prune`

4. **Open in Cursor:**
   - Run `cursor [worktree-path]`

5. **Report success:**
   - Confirm which worktree was opened
   - Show the branch it's on

## Notes

- This is an interactive command - always wait for user input if no argument provided
- Keep output minimal and clean
