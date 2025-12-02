---
description: Quick investigation of what's wrong with the app
argument-hint: "[symptom or page]"
---

Quickly investigate why something is broken or behaving unexpectedly.

**Problem description:** $ARGUMENTS

## Workflow

1. Call `get_errors` to check for obvious errors
2. If a page/route is mentioned, call `get_page_metadata` for that route
3. Call `get_logs` if runtime behavior is the issue
4. Correlate findings with the described symptom

## Output

Provide a direct answer:
- **Root cause**: What's actually wrong
- **Location**: File and line if applicable
- **Fix**: Quick solution or next step

Be concise. This is for rapid debugging, not comprehensive analysis.

If the symptom is vague, ask one clarifying question before investigating.
