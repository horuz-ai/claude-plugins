---
description: Create a comprehensive multi-phase plan capturing all session context for future Claude Code sessions
argument-hint: "[optional: plan filename]"
---

# Create Implementation Plan

Create a comprehensive implementation plan at the project root.

**Filename:** `$ARGUMENTS` (default to `plan.md` if not provided)

## Context Preservation (Critical)

This plan will be used by **future Claude Code sessions** that have no memory of this conversation. You must include:

### 1. Project Understanding
- What we're building and why
- The problem we're solving
- Key constraints or requirements discussed

### 2. Decisions Made
Document every significant decision from our conversation:
- What was decided
- Why we chose this approach
- What alternatives were considered and rejected

### 3. Questions & Answers
Include important Q&A from our brainstorming:
- Questions you asked me and my answers
- Clarifications that shaped the implementation
- Any assumptions we validated

### 4. Technical Context
- Architecture decisions
- Technology choices and rationale
- Patterns or conventions we agreed on

## Multi-Phase Plan Structure

Break the implementation into **small, focused phases** that can be:
- Reviewed independently
- Committed as atomic units
- Understood without prior context

### Phase Format
For each phase:
```markdown
## Phase N: [Clear Title]

### Objective
One sentence describing what this phase accomplishes.

### Context for Future Claude
Any phase-specific decisions or context needed.

### Research & Code Snippets
If during our conversation we researched documentation, found code examples, or discovered specific implementation patterns for this phase, include them here:
- Links to documentation consulted
- Code snippets that show the correct implementation approach
- API usage examples we found
- Any patterns or solutions discovered through research

### Tasks
- [ ] Task 1 (specific, actionable)
- [ ] Task 2
- [ ] ...

### Deliverables
What should exist when this phase is complete.
```

## Important Guidelines

1. **Be exhaustive with context** - Future Claude has zero memory of this conversation
2. **Keep phases small** - Each should be completable and reviewable in one session
3. **Include the "why"** - Not just what to do, but why we decided to do it this way
4. **Preserve research** - Any documentation lookups, code snippets, or implementation examples we found during brainstorming must be included in the relevant phase
5. **Make it standalone** - The plan should be usable without any other context
6. **Order phases logically** - Consider dependencies between phases

## Output

Write the complete plan to the specified file in the project root. The plan should be immediately usable by a fresh Claude Code session.