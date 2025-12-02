---
description: Find and fix all Next.js errors automatically
allowed-tools: ["Read", "Write", "Edit", "Bash"]
---

Use the Next.js MCP server to detect and fix all errors in the application.

## Workflow

1. Call `get_errors` to retrieve current build, runtime, and type errors
2. If no errors found, confirm the app is healthy and stop
3. For each error found:
   - Read the affected file
   - Analyze the root cause
   - Apply the fix
4. After all fixes, call `get_errors` again to verify resolution

## Constraints

- Fix one error at a time
- Explain each fix briefly before applying
- If an error cannot be auto-fixed, explain why and suggest manual steps
- Do not modify unrelated code
