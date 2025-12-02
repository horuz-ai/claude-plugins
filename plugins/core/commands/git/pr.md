---
allowed-tools: Bash(git:*), Bash(gh:*), Read, Glob, Grep
description: "Create a pull request to dev with comprehensive description"
---

# Create Pull Request

You are helping a developer create a well-documented pull request targeting the `dev` branch.

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Commits on this branch (not in dev): !`git log origin/dev..HEAD --oneline 2>/dev/null || echo "NO_COMMITS_AHEAD"`
- Git diff from dev (summary): !`git diff origin/dev --stat 2>/dev/null | tail -20`
- All commit messages on this branch: !`git log origin/dev..HEAD --pretty=format:"%s" 2>/dev/null`
- Check if PR already exists: !`gh pr view --json url 2>/dev/null || echo "NO_PR_EXISTS"`
- GitHub username (reviewer): !`echo "nelsonrosa3"`

## PR Best Practices

A good pull request should:

1. **Have a clear, descriptive title** that summarizes the change
2. **Explain the "what" and "why"** of the changes
3. **Be easy to review** - not too large, focused on one thing
4. **Include context** for reviewers who may not know the background
5. **List any testing done** or instructions to test
6. **Mention breaking changes** if any
7. **Link related issues** if applicable

## Your Task

Follow these steps precisely:

### Step 1: Validate Current State

**Check if on a protected branch:**
- If on `dev`, `staging`, or `main`: **STOP**
  - Inform developer: "You cannot create a PR from a protected branch. Please use `/branch` to create a feature branch first."

**Check if there are uncommitted changes:**
- If git status shows uncommitted changes: **STOP**
  - Inform developer: "You have uncommitted changes. Please use `/commit` first before creating a PR."

**Check if there are commits to push:**
- If no commits ahead of dev: **STOP**
  - Inform developer: "This branch has no new commits compared to dev. Nothing to create a PR for."

**Check if PR already exists:**
- If PR already exists, inform the developer and provide the PR URL
- Ask if they want to update the PR description instead

### Step 2: Push the Branch

```bash
git push -u origin {current-branch}
```

### Step 3: Analyze Changes for PR Content

Read the commits and diff to understand:
- What was changed (features added, bugs fixed, etc.)
- Why it was changed (the motivation)
- What areas of the codebase are affected

### Step 4: Generate PR Title

Create a clear, concise title that:
- Starts with the type: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`
- Summarizes the main change in imperative mood
- Is max 72 characters
- Examples:
  - `feat: add user authentication with OAuth2`
  - `fix: resolve race condition in payment processing`
  - `chore: upgrade dependencies to latest versions`

### Step 5: Generate PR Description

Create a comprehensive PR description following this template:

```markdown
## Summary

[2-3 sentences explaining what this PR does and why]

## Changes

- [Bullet point for each significant change]
- [Group related changes together]
- [Be specific but concise]

## Type of Change

- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 🧹 Chore (maintenance, refactoring, dependencies)
- [ ] 📚 Documentation update

## Testing

[Describe how this was tested or how reviewers can test it]

- [ ] Tested locally
- [ ] Added/updated unit tests
- [ ] Tested in staging environment

## Screenshots (if applicable)

[Add screenshots for UI changes]

## Additional Notes

[Any additional context, concerns, or notes for reviewers]
```

**Fill in the template based on the actual changes:**
- Check the appropriate checkbox for type of change
- Write a meaningful summary based on the commits
- List the actual changes made
- Include realistic testing notes based on what you can infer

### Step 6: Create the Pull Request

```bash
gh pr create \
  --base dev \
  --title "{pr-title}" \
  --body "{pr-description}" \
  --reviewer nelsonrosa3
```

### Step 7: Confirm to Developer

After successful PR creation:
- Show the PR URL
- Summarize what was included in the PR
- Remind them that the PR is now ready for review

---

## Constraints

- ALWAYS target `dev` branch as the base
- ALWAYS assign `nelsonrosa3` as the reviewer
- NEVER create PRs from protected branches
- NEVER create PRs with uncommitted changes
- PR title MUST be concise (max 72 characters)
- PR description MUST follow the template structure
- Fill in the checkbox that matches the type of change (only ONE primary type)
- Do NOT leave placeholder text in the PR description - fill everything in based on actual changes