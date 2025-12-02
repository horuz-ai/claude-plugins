---
allowed-tools: Bash(git:*)
description: "Promote dev branch to staging with conflict review"
disable-model-invocation: true
---

# Promote Dev to Staging

You are helping promote changes from the `dev` branch to the `staging` branch.

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Commits in dev not in staging: !`git fetch origin && git log origin/staging..origin/dev --oneline 2>/dev/null | head -20`
- Files that will change: !`git diff origin/staging..origin/dev --stat 2>/dev/null | tail -15`

## Your Task

Follow these steps precisely:

### Step 1: Validate State

**Check for uncommitted changes:**
- If there are uncommitted changes: **STOP**
  - "You have uncommitted changes. Please stash or commit them before promoting."

**Check if there are changes to promote:**
- If dev and staging are identical (no commits ahead): **STOP**
  - "No new changes in dev to promote to staging. The branches are already in sync."

### Step 2: Show What Will Be Promoted

Before proceeding, clearly show:
- Number of commits that will be merged
- List of commits (from the context above)
- Summary of files affected

Ask: **"Do you want to proceed with promoting these changes to staging? (Yes/No)"**

Wait for confirmation before proceeding.

### Step 3: Fetch Latest and Checkout Staging

```bash
git fetch origin
git checkout staging
git pull origin staging
```

### Step 4: Merge Dev into Staging

```bash
git merge origin/dev --no-ff -m "chore: promote dev to staging"
```

### Step 5: Handle Merge Result

**If merge is successful (no conflicts):**
- Proceed to Step 6

**If there are CONFLICTS:**

**⚠️ STOP and do NOT auto-resolve. Present the conflicts for review.**

1. **List all conflicted files:**
   ```bash
   git diff --name-only --diff-filter=U
   ```

2. **For each conflicted file, show:**
   - The file name
   - The conflict markers and surrounding context
   ```bash
   git diff {file}
   ```

3. **Explain the conflict:**
   - What the `staging` branch has (marked with `<<<<<<< HEAD`)
   - What the `dev` branch has (marked with `>>>>>>> origin/dev`)
   - Your suggestion for resolution (but DO NOT apply it automatically)

4. **Ask for resolution:**
   - "How would you like to resolve this conflict?"
   - Options:
     a) Accept staging version (keep current)
     b) Accept dev version (take incoming)
     c) Manual merge (you will specify the desired content)
     d) Abort the merge

5. **Only after receiving resolution for EACH conflict:**
   - Apply the resolution
   - Stage the resolved file: `git add {file}`

6. **After ALL conflicts are resolved:**
   ```bash
   git commit -m "chore: promote dev to staging (resolved conflicts)"
   ```

### Step 6: Push to Remote

```bash
git push origin staging
```

### Step 7: Return to Dev Branch

```bash
git checkout dev
```

### Step 8: Confirm Completion

After successful promotion:
- Summarize what was promoted (number of commits, key changes)
- Confirm that staging is now up to date with dev
- Remind: "When ready to release to production, use `/promote-prod`"

---

## Conflict Resolution Guidelines

When explaining conflicts, provide:

1. **Context:** What each version is trying to do
2. **Impact:** What accepting each version would mean
3. **Recommendation:** Your suggested resolution and why (but wait for approval)

**Example conflict explanation:**
```
📍 Conflict in: src/services/auth.ts

STAGING version (current):
- Uses legacy authentication method
- Last modified 3 days ago

DEV version (incoming):
- Implements new OAuth2 flow
- Added error handling for token refresh

💡 Recommendation: Accept DEV version
Reason: The dev changes appear to be an intentional upgrade to the auth system.

How would you like to proceed?
a) Accept staging (keep legacy auth)
b) Accept dev (use new OAuth2)
c) Custom merge (specify what you want)
d) Abort merge
```

---

## Constraints

- NEVER auto-resolve conflicts without explicit approval
- ALWAYS show what will be promoted before merging
- ALWAYS wait for explicit confirmation before proceeding
- Use `--no-ff` flag to preserve merge history
- After promotion, always return to `dev` branch
- If user chooses to abort, clean up properly: `git merge --abort`