---
description: Initialize a new task with requirements. Creates .tasks/{task-name}/ structure and organizes requirements in task.md
allowed-tools: Bash, Read, Write, Edit, TodoWrite
argument-hint: "<requirements> (required)"
---

# Initialize New Task

**User input:** $ARGUMENTS

## Your Task

You MUST have input to create a task. If **User input:** is empty, ask the user what they want to build.

1. **Understand the requirements** from user input and ask clarifying questions using plan mode. Keep asking until you have a clear picture of:
   - What needs to be built
   - Any specific constraints or preferences
   - Technical requirements if mentioned

2. **Generate a task name** based on the requirements (kebab-case, descriptive, e.g., "implement-user-auth", "add-payment-integration", "refactor-api-routes")

3. Create the directory `.tasks/{generated-task-name}/`

4. Create `.tasks/{generated-task-name}/status.md`:
```markdown
   # Status: {generated-task-name}
   
   ## Current Phase
   - [x] Task Definition
   - [ ] Explore
   - [ ] Research  
   - [ ] Spec
   - [ ] Build
   - [ ] Review
   - [ ] Refactor
   
   ## Activity Log
   - [timestamp] Task initialized
```

5. Create `.tasks/{generated-task-name}/task.md` with:
```markdown
   # Task: {generated-task-name}
   
   ## Objective
   [Clear statement of what needs to be accomplished]
   
   ## Requirements
   [Specific requirements extracted from user input and clarifications]
   
   ## Constraints
   [Any limitations or specific approaches mentioned]
   
   ## Clarifications
   [Questions asked by Claude Code and user's answers]
   
   ### Q: [Question you asked]
   A: [User's answer]
   
   ### Q: [Another question]
   A: [User's answer]
```

6. Present the final task.md to the user and confirm it captures everything correctly

## Notes

- **User input:** is REQUIRED - if empty, ask the user what they want to build
- YOU generate the task name, not the user
- Be thorough in asking questions - better to clarify now than assume wrong
- Document ALL clarifying Q&A in the Clarifications section
- Keep asking questions until requirements are crystal clear