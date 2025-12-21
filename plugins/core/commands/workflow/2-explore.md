---
description: Explore codebase for current task context. Uses builtin explore agent and saves findings to explore.md
allowed-tools: Bash, Read, Glob, Grep, Task
argument-hint: "[specific areas to explore]"
---

# Explore Codebase

**Additional context (optional):** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. First, identify which task we're working on:
   - Check `.tasks/` for the most recent or active task
   - Read `.tasks/{task-name}/task.md` to understand what we need to find
   - If unclear which task, ask the user

2. Use the builtin Explore agent (or explore yourself) to analyze the codebase:
   - Find files relevant to the task requirements
   - Understand the current project structure
   - Identify existing patterns, conventions, and architecture
   - Find related code that might be affected or reused
   - Check for existing similar implementations

3. Write findings to `.tasks/{task-name}/explore.md`:
````markdown
   # Explore: {task-name}
   
   ## Project Structure
   [Relevant directory structure]
   
   ## Stack Detected
   [Framework, libraries, versions from package.json etc.]
   
   ## Relevant Files
   [Files that relate to this task with brief descriptions]
   
   ## Existing Patterns
   [Conventions, patterns used in the project]
   
   ## Considerations
   [Things to keep in mind during implementation]
````

4. Update `.tasks/{task-name}/status.md` activity log

5. Use plan mode to:
   - Summarize what you found
   - Ask if there are specific areas to explore deeper
   - Confirm we have enough context to proceed to research

## Notes

- Be thorough but focused on what's relevant to the task
- Include file paths so they can be referenced later
- Note any inconsistencies or tech debt discovered