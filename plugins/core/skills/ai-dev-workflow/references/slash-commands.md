# Slash Commands Reference

All commands go in `.claude/commands/` as individual `.md` files.

---

## /task

**File:** `.claude/commands/task.md`

```markdown
---
description: Initialize a new task with requirements. Creates .tasks/{task-name}/ structure and organizes requirements in task.md
allowed-tools: Bash, Read, Write, Edit, TodoWrite
argument-hint: "<requirements> (required)"
---

# Initialize New Task

**User input:** $ARGUMENTS

## Your Task

You MUST have input to create a task. If $ARGUMENTS is empty, ask the user what they want to build.

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

- $ARGUMENTS is REQUIRED - if empty, ask the user what they want to build
- YOU generate the task name, not the user
- Be thorough in asking questions - better to clarify now than assume wrong
- Document ALL clarifying Q&A in the Clarifications section
- Keep asking questions until requirements are crystal clear
```

---

## /explore

**File:** `.claude/commands/explore.md`

```markdown
---
description: Explore codebase for current task context. Uses builtin explore agent and saves findings to explore.md
allowed-tools: Bash, Read, Glob, Grep, Task
argument-hint: "[specific areas to explore]"
---

# Explore Codebase

**Additional context:** $ARGUMENTS

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
   ```markdown
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
   ```

4. Update `.tasks/{task-name}/status.md` activity log

5. Use plan mode to:
   - Summarize what you found
   - Ask if there are specific areas to explore deeper
   - Confirm we have enough context to proceed to research

## Notes

- Be thorough but focused on what's relevant to the task
- Include file paths so they can be referenced later
- Note any inconsistencies or tech debt discovered
```

---

## /research

**File:** `.claude/commands/research.md`

```markdown
---
description: Deep research for current task using research sub-agent. Finds documentation, patterns, and code examples for installed versions.
allowed-tools: Bash, Read, Glob, Grep, Task, WebFetch, WebSearch
argument-hint: "[specific topics to research]"
---

# Research

**Additional focus:** $ARGUMENTS

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
   ```markdown
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
   ```

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
```

---

## /spec

**File:** `.claude/commands/spec.md`

```markdown
---
description: Generate technical specification with phases using spec sub-agent. Creates implementation plan with code snippets.
allowed-tools: Bash, Read, Write, Edit, Task
argument-hint: "[considerations for the spec]"
---

# Generate Specification

**Additional considerations:** $ARGUMENTS

## Context

- Current tasks: !`ls -la .tasks/ 2>/dev/null || echo "No .tasks directory"`

## Your Task

1. Identify the current task and read:
   - `.tasks/{task-name}/task.md` (requirements)
   - `.tasks/{task-name}/explore.md` (codebase context)
   - `.tasks/{task-name}/research.md` (documentation and patterns)

2. Delegate to the `spec` sub-agent to create a detailed technical specification

3. The spec sub-agent should create `.tasks/{task-name}/spec.md` with:
   ```markdown
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
   ```

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
```

---

## /build

**File:** `.claude/commands/build.md`

```markdown
---
description: Build/implement phases from spec. Executes implementation following the spec phases.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
argument-hint: "[phase number or 'next' or 'all']"
---

# Build

**Phase to build:** $ARGUMENTS

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
```

---

## /review

**File:** `.claude/commands/review.md`

```markdown
---
description: Code review using review sub-agent. Checks implementation against spec and project standards.
allowed-tools: Bash, Read, Glob, Grep, Task
argument-hint: "[specific areas to focus review]"
---

# Code Review

**Focus areas:** $ARGUMENTS

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
   ```markdown
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
   ```

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
```

---

## /refactor

**File:** `.claude/commands/refactor.md`

```markdown
---
description: Execute fixes from review using refactor sub-agent. Systematically addresses review issues.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task
argument-hint: "[priority: all|high|medium or specific issue]"
---

# Refactor

**What to fix:** $ARGUMENTS

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
   ```markdown
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
   ```

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
```
