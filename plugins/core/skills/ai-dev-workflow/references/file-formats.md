# File Formats Reference

## status.md

```markdown
# Status: {task-name}

## Current Phase
- [x] Task Definition
- [ ] Explore
- [ ] Research
- [ ] Spec
- [ ] Build
- [ ] Review
- [ ] Refactor

## Activity Log
- [YYYY-MM-DD HH:MM] Task initialized
- [YYYY-MM-DD HH:MM] Explore complete
```

## task.md

```markdown
# Task: {task-name}

## Objective
[Clear statement of what needs to be accomplished]

## Requirements
- Requirement 1
- Requirement 2

## Constraints
- Constraint 1

## Clarifications

### Q: [Question Claude asked]
A: [User's answer]

### Q: [Another question]
A: [User's answer]
```

## explore.md

```markdown
# Explore: {task-name}

## Project Structure
[Relevant directories]

## Stack Detected
- Framework: Next.js 15.1.0
- ORM: Drizzle 0.30.0
- Auth: Better Auth 1.2.3

## Relevant Files
- `src/lib/db.ts` - Database connection
- `src/app/api/` - API routes

## Existing Patterns
[Conventions found in codebase]

## Considerations
[Things to keep in mind]
```

## research.md

```markdown
# Research: {task-name}

## Stack Reference
[Installed versions for compatibility]

## Topic 1: [Name]

### Summary
[What we learned]

### Code Snippets
```typescript
// Copy-paste ready code
```

### Source
[Link to official docs]

## Topic 2: [Name]
...

## Key Considerations
[Patterns, pitfalls, best practices]
```

## spec.md

```markdown
# Spec: {task-name}

## Overview
[What we're building and why]

## Phase 1: [Name]

### Scope
[Exactly what this phase accomplishes]

### Files
- `path/to/file.ts` - [purpose]

### Dependencies
None | Phase X must be complete

### Implementation Guide
```typescript
// Code showing HOW to implement
```

### Done When
- [ ] Criteria 1
- [ ] Criteria 2

## Phase 2: [Name]
...
```

## review.md

```markdown
# Review: {task-name}

## Summary
- ✅ Passed: X checks
- ⚠️ Warnings: X items
- ❌ Issues: X items

## Issues

### ❌ [HIGH] Issue title
**File:** path/to/file.ts:42
**Problem:** Description of the problem
**Fix:** Specific suggestion on how to fix

### ⚠️ [MEDIUM] Issue title
**File:** path/to/file.ts:15
**Problem:** Description
**Fix:** How to fix

### 💡 [LOW] Suggestion
**File:** path/to/file.ts:100
**Suggestion:** Improvement idea

## Passed Checks
- ✅ Naming conventions
- ✅ No hardcoded secrets
- ✅ Proper error handling
```

## refactor.md

```markdown
# Refactor: {task-name}

## Fixes Applied

### ✅ [HIGH] Issue title
**Original:** Brief description of issue from review.md
**Changes:**
- Modified `path/to/file.ts`: [what changed]
- Created `path/to/new-file.ts`: [purpose]
**Verified:** How we confirmed the fix works

### ✅ [MEDIUM] Another issue
**Original:** Issue description
**Changes:**
- [changes made]

## Deferred

### ⏭️ [LOW] Deferred issue title
**Reason:** Why this was deferred (low priority, needs discussion, etc.)

## New Issues Discovered
[Any new issues found during refactor that need future attention]
```
