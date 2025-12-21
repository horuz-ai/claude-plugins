---
description: Execute fixes from review using refactor sub-agent. Systematically addresses review issues.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
argument-hint: "[priority: all|high|medium or specific issue]"
---

# Refactor

**What to fix (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/review.md` (issues to fix)
   - `.tasks/{task-name}/status.md` (current state)

2. Determine scope:
   - If "all": fix everything HIGH → MEDIUM → LOW
   - If "high": only HIGH severity issues
   - If specific issue mentioned: just that one
   - Default: HIGH and MEDIUM issues

3. Delegate to the `refactor` sub-agent to execute fixes

4. The refactor agent should:
   - Fix issues in priority order
   - Make surgical, focused changes
   - NOT change anything outside issue scope
   - Verify each fix doesn't break anything
   - Document what was changed

5. Create/update `.tasks/{task-name}/refactor.md`:
````markdown
   # Refactor: {task-name}
   
   ## Fixes Applied
   
   ### ✅ [HIGH] Issue title
   **Original:** Brief description of issue
   **Changes:**
   - Modified `path/to/file.ts`: [what changed]
   **Verified:** How we confirmed the fix
   
   ### ⏭️ [LOW] Deferred issue
   **Reason:** Why deferred
   
   ## New Issues Discovered
   [Any new issues found during refactor]
````

6. Update `.tasks/{task-name}/status.md` activity log

7. Use plan mode to:
   - Summarize fixes applied
   - Report any deferred items
   - Decide if another review cycle needed
   - Mark task complete if all done

## Notes

- Be surgical - fix exactly what's needed
- Run tests after fixes if available
- If a fix is risky, discuss before applying
- Don't over-engineer or gold-plate