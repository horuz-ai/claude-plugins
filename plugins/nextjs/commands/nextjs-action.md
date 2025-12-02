---
description: Look up a Server Action by its ID
argument-hint: "[action-id]"
---

Use the Next.js MCP server to find a Server Action by its ID.

**Action ID:** $ARGUMENTS

Call `get_server_action_by_id` with the provided ID and present:
- Source file path
- Function name
- Brief description of what the action does (from reading the code)

If the action is found, offer to:
- Open the file for editing
- Show the full implementation
- Explain how it's being used

If no ID is provided, explain that a Server Action ID is required (usually visible in error messages or network requests).
