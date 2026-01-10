---
description: Debug Laravel errors - check browser/server logs, explain the issue, suggest fixes without implementing
---

# Debug Laravel Error

Use the Laravel Boost MCP server to investigate the current error.

## Tools to Use

1. **`last-error`** - Get details of the last backend exception
2. **`browser-logs`** - Check for frontend/console errors
3. **`read-log-entries`** - Read recent Laravel log entries for more context

If the error points to a specific area, also use:
- **`database-schema`** - If it's a database/migration/model issue
- **`list-routes`** - If it's a routing or 404 issue
- **`get-config`** - If it's a configuration issue

## Constraints

- **DO NOT implement any code changes**
- **DO NOT modify any files**
- Only explain what is happening and why

## Output Format

After investigating, provide:

1. **What's happening** - A clear explanation of the error and its root cause
2. **Suggested fixes** - Present 2-4 different options to resolve the issue, each with:
   - Brief description of the approach
   - Pros/cons if relevant
   - Files that would need to change

Then wait for me to choose an option or request something different.