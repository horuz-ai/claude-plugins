---
description: Build/implement phases from spec. Executes implementation following the spec phases.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
argument-hint: "[phase number or 'next' or 'all']"
---

# Build

**Phase to build (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/spec.md` (the plan to follow)
   - `.tasks/{task-name}/research.md` (reference documentation)
   - `.tasks/{task-name}/status.md` (what's been done)

2. Determine which phase to implement:
   - If user specified a phase number, do that phase
   - If user said "next", find the next incomplete phase
   - If user said "all", do all remaining phases in order
   - If unclear, ask which phase to implement

3. For each phase:
   - Follow the spec exactly
   - Use code snippets from research.md and spec.md as guides
   - Create/modify files as specified
   - Check off "Done When" criteria as you complete them
   - Update status.md with progress

4. After completing a phase:
   - Update `.tasks/{task-name}/status.md`:
     - Mark phase as complete
     - Add activity log entry
   - Summarize what was implemented
   - Ask if ready to proceed to next phase or need adjustments

## Notes

- Follow the spec - don't deviate without discussing first
- If you encounter issues, document them and ask for guidance
- Keep implementation focused on current phase only
- Test as you go when possible