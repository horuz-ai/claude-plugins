---
allowed-tools: Bash(git:*), Bash(ls:*), Bash(cat:*)
description: List all Git worktrees with their status and details
---

# List All Worktrees

## Context

- Current directory: !`pwd`
- Git root: !`git rev-parse --show-toplevel 2>/dev/null || echo "Not in a git repo"`
- All worktrees: !`git worktree list 2>/dev/null || echo "No worktrees found"`
- Worktrees with details: !`git worktree list --porcelain 2>/dev/null`

## Your Task

Display a comprehensive overview of all Git worktrees in this repository.

### Information to gather and display:

1. **List all worktrees** using `git worktree list`

2. **For each worktree, show:**
   - Path
   - Branch name
   - Current commit (short hash)
   - Whether it has uncommitted changes (run `git -C [path] status --porcelain` for each)

3. **Format the output nicely:**
   ```
   📁 Worktrees for [repo-name]
   ═══════════════════════════════════════
   
   1. /path/to/main (main branch)
      └─ ✅ Clean
   
   2. /path/to/feat-something (feat/something)  
      └─ ⚠️  Has uncommitted changes
   
   3. /path/to/pr-123 (pr-123)
      └─ ✅ Clean
   ```

4. **Show summary:**
   - Total worktrees count
   - How many have uncommitted changes

## Notes

- Use emojis to make the output scannable
- If a worktree path doesn't exist (orphaned), flag it with ❌
- This is a read-only command, don't modify anything
