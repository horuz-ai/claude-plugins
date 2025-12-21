---
description: Generate technical specification with phases using spec sub-agent. Creates implementation plan with code snippets.
allowed-tools: Bash, Read, Write, Edit, Task
argument-hint: "[considerations for the spec]"
---

# Generate Specification

**Additional considerations (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/task.md` (requirements)
   - `.tasks/{task-name}/explore.md` (codebase context)
   - `.tasks/{task-name}/research.md` (documentation and patterns)

2. Delegate to the `spec` sub-agent to create a detailed technical specification

3. The spec sub-agent should create `.tasks/{task-name}/spec.md` with:
````markdown
   # Spec: {task-name}
   
   ## Overview
   [What we're building and why]
   
   ## Phase 1: [Name]
   ### Scope
   [Exactly what this phase accomplishes]
   ### Files
   - `path/to/file.ts` - [what it does]
   ### Dependencies
   None | Phase X must be complete
   ### Implementation Guide
   [Code snippets from research showing HOW to implement]
```typescript
   // Example code here
```
   ### Done When
   - [ ] Criteria 1
   - [ ] Criteria 2
   
   ## Phase 2: [Name]
   ...
````

4. Update `.tasks/{task-name}/status.md` activity log

5. Use plan mode to:
   - Walk through each phase with the user
   - Get feedback on the approach
   - Adjust phases if needed
   - Confirm the spec is approved before build

## Notes

- Each phase must be independently executable in a separate session
- Include code snippets - the build phase should be able to follow them
- Phases should be small enough to complete without getting lost
- Define clear "done" criteria for each phase