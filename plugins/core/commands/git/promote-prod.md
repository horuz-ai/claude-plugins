---
allowed-tools: Bash(git:*), Read
description: "Promote staging branch to main/production with version tagging"
disable-model-invocation: true
---

# Promote Staging to Production

You are helping promote changes from the `staging` branch to the `main` (production) branch with proper version tagging.

**⚠️ This will deploy to PRODUCTION. Proceed with caution.**

## Context

- Current branch: !`git branch --show-current`
- Git status: !`git status --short`
- Current latest tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "NO_TAGS_YET"`
- All version tags (latest 10): !`git tag -l "v*" --sort=-version:refname | head -10`
- Commits in staging not in main: !`git fetch origin && git log origin/main..origin/staging --oneline 2>/dev/null | head -20`
- Commit types since last release: !`git log origin/main..origin/staging --pretty=format:"%s" 2>/dev/null`
- Files that will change: !`git diff origin/main..origin/staging --stat 2>/dev/null | tail -15`

## Your Task

Follow these steps precisely:

### Step 1: Validate State

**Check for uncommitted changes:**
- If there are uncommitted changes: **STOP**
  - "You have uncommitted changes. Please stash or commit them before promoting to production."

**Check if there are changes to promote:**
- If staging and main are identical: **STOP**
  - "No new changes in staging to promote to production. The branches are already in sync."

### Step 2: Determine Version Bump

Analyze the commits being promoted to determine the appropriate version bump:

**Semantic Versioning Rules (MAJOR.MINOR.PATCH):**

- **MAJOR** (X.0.0): Breaking changes
  - Look for: commits with `!` after type (e.g., `feat!:`, `fix!:`)
  - Look for: "BREAKING CHANGE" in commit messages
  - Look for: Major API changes, incompatible changes

- **MINOR** (0.X.0): New features (backward compatible)
  - Look for: `feat:` commits
  - New functionality that doesn't break existing behavior

- **PATCH** (0.0.X): Bug fixes and minor changes
  - Look for: `fix:`, `chore:`, `docs:`, `refactor:`, `style:`, `perf:`, `test:` commits
  - No new features, just fixes and maintenance

**Determine the version:**
1. If no tags exist yet, start with `v1.0.0`
2. If tags exist, parse the latest tag and increment appropriately
3. The highest-impact change type determines the bump:
   - Any breaking change → MAJOR bump
   - Any `feat:` without breaking → MINOR bump
   - Only fixes/chores → PATCH bump

### Step 3: Show What Will Be Promoted

Present the release summary:

```
🚀 PRODUCTION RELEASE SUMMARY
==============================

📦 Current Version: {current-tag or "None"}
📦 New Version: {calculated-new-version}

📝 Commits to be released ({count}):
{list of commits}

📁 Files affected ({count}):
{summary of changed files}

Version bump reason: {explanation of why this bump type}
```

Ask: **"Do you want to proceed with releasing {new-version} to production? (Yes/No)"**

Wait for explicit confirmation before proceeding.

### Step 4: Fetch Latest and Checkout Main

```bash
git fetch origin
git checkout main
git pull origin main
```

### Step 5: Merge Staging into Main

```bash
git merge origin/staging --no-ff -m "chore: release {new-version}"
```

### Step 6: Handle Merge Result

**If merge is successful (no conflicts):**
- Proceed to Step 7

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

3. **Explain the conflict clearly:**
   - What `main` (production) currently has
   - What `staging` is trying to bring in
   - Your recommendation (but wait for approval)

4. **⚠️ PRODUCTION WARNING:**
   - Emphasize this is production
   - Recommend extra caution
   - Suggest testing implications

5. **Ask for resolution for EACH conflict:**
   - a) Accept main version (keep production as-is)
   - b) Accept staging version (take staged changes)
   - c) Custom merge (you specify content)
   - d) Abort the release

6. **Only after receiving resolution for ALL conflicts:**
   - Apply each resolution
   - Stage resolved files: `git add {file}`
   - Complete the merge: `git commit -m "chore: release {new-version} (resolved conflicts)"`

### Step 7: Create Version Tag

```bash
git tag -a {new-version} -m "Release {new-version}

Changes in this release:
{bullet list of key changes from commits}"
```

**Tag message should include:**
- The version number
- A summary of key changes (2-5 bullet points)
- Based on the actual commits being released

### Step 8: Push to Remote

```bash
git push origin main
git push origin {new-version}
```

### Step 9: Return to Dev Branch

```bash
git checkout dev
```

### Step 10: Confirm Completion

After successful release:

```
✅ PRODUCTION RELEASE COMPLETE
================================

🏷️  Version: {new-version}
📍 Branch: main
🔗 Tag: {new-version}

📝 Released changes:
{summary of what was released}

🔄 You are now back on the dev branch.

Next steps:
- Monitor production for any issues
- Communicate release to team if needed
```

---

## Conflict Resolution Guidelines for Production

**⚠️ Extra caution for production conflicts:**

1. **Understand the risk:** Explain what could break if resolved incorrectly
2. **Recommend conservative approach:** When in doubt, suggest keeping production stable
3. **Suggest testing:** Recommend testing the resolution before finalizing
4. **Document the decision:** Include resolution reasoning in commit message

**Example conflict explanation for production:**
```
⚠️ PRODUCTION CONFLICT DETECTED

📍 File: src/services/payment.ts

🔴 MAIN (current production):
- Payment processing with rate limiting
- In production since 2 weeks ago

🟡 STAGING (incoming):
- Updated payment flow with new provider
- Includes new error handling

⚠️ RISK ASSESSMENT:
- Accepting staging: May affect live payment processing
- Accepting main: New payment features won't be released

💡 Recommendation: Accept STAGING version
Reason: This appears to be a planned upgrade that passed staging testing.
However, recommend monitoring payment metrics closely after release.

How would you like to proceed?
a) Accept main (keep current production payment flow)
b) Accept staging (deploy new payment flow)
c) Custom merge (specify what you want)
d) Abort release (do not deploy to production)
```

---

## Constraints

- NEVER auto-resolve conflicts in production releases
- ALWAYS show full release summary before proceeding
- ALWAYS wait for explicit "Yes" confirmation
- ALWAYS create an annotated tag with meaningful message
- Version tags MUST follow semantic versioning (vX.Y.Z)
- Use `--no-ff` flag to preserve merge history
- After release, always return to `dev` branch
- If user aborts, clean up: `git merge --abort` and return to dev
- Push both the branch AND the tag to remote