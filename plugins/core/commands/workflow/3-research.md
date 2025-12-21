---
description: Deep research for current task using research sub-agent. Finds documentation, patterns, and code examples for installed versions.
allowed-tools: Bash, Read, Glob, Grep, Task, WebFetch, WebSearch
argument-hint: "[specific topics to research]"
---

# Research

**Additional focus (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/task.md` (requirements)
   - `.tasks/{task-name}/explore.md` (codebase context)

2. Identify what needs to be researched based on requirements and stack

3. **IMPORTANT**: Delegate research to the `research` sub-agent with GRANULAR, SPECIFIC questions. Do NOT send one big research request. Instead, spawn MULTIPLE research agents for specific topics:
   
   Example - if implementing auth:
   - Agent 1: "How to configure Better Auth 1.2.3 with session strategy"
   - Agent 2: "Drizzle ORM schema patterns for auth tables"
   - Agent 3: "Next.js 15 middleware for route protection"
   - Agent 4: "Better Auth + Drizzle adapter configuration"
   
   Each agent should focus on ONE specific thing and go deep.

4. Aggregate all research findings into `.tasks/{task-name}/research.md`:
````markdown
   # Research: {task-name}
   
   ## Stack Reference
   [Installed versions for reference]
   
   ## Topic 1: [Name]
   ### Summary
   [What we learned]
   ### Code Snippets
   [Copy-paste ready examples]
   ### Source
   [Links to official docs]
   
   ## Topic 2: [Name]
   ...
   
   ## Key Considerations
   [Important patterns, pitfalls, best practices]
````

5. Update `.tasks/{task-name}/status.md` activity log

6. Use plan mode to:
   - Summarize research findings
   - Ask if any areas need deeper research
   - Confirm we have enough info to create the spec

## Notes

- Research must match INSTALLED versions, not latest
- Better to over-research than miss something
- Code snippets should be actionable and copy-paste ready
- Always cite official documentation sources