---
description: Code review using review sub-agent. Checks implementation against spec and project standards.
allowed-tools: Bash, Read, Glob, Grep, Task
argument-hint: "[specific areas to focus review]"
---

# Code Review

**Focus areas (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`
- Git status: !`git status --short 2>/dev/null || echo "Not a git repo"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/spec.md` (what should have been built)
   - `.tasks/{task-name}/status.md` (what phases were completed)

2. Delegate to the `review` sub-agent to perform exhaustive code review

3. The review agent should check:
   - Implementation matches spec requirements
   - Naming conventions (check CLAUDE.md if exists)
   - No duplicated code or logic
   - Files organized correctly
   - Security: no hardcoded secrets, proper env vars, input validation
   - Proper error handling
   - TypeScript types (if applicable)
   - Documentation present
   - No unused imports, dead code, console.logs

4. Create `.tasks/{task-name}/review.md`:
````markdown
   # Review: {task-name}
   
   ## Summary
   - ✅ Passed: X checks
   - ⚠️ Warnings: X items
   - ❌ Issues: X items
   
   ## Issues
   
   ### ❌ [HIGH] Issue title
   **File:** path/to/file.ts:42
   **Problem:** Description
   **Fix:** How to fix it
   
   ### ⚠️ [MEDIUM] Issue title
   ...
   
   ### 💡 [LOW] Suggestion
   ...
   
   ## Passed Checks
   - ✅ Naming conventions
   - ✅ No hardcoded secrets
   ...
````

5. Update `.tasks/{task-name}/status.md` activity log

6. Use plan mode to:
   - Present review findings
   - Discuss severity of issues
   - Decide what to fix vs defer
   - Proceed to refactor if needed

## Notes

- Be thorough but constructive
- Every issue needs a specific fix suggestion
- Prioritize security and correctness issues