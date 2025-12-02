---
description: Get and analyze Next.js development logs
allowed-tools: ["Bash", "Read"]
---

Use the Next.js MCP server to retrieve and analyze development logs.

## Workflow

1. Call `get_logs` to get the log file path
2. Read the log file contents
3. Analyze for:
   - Console errors and warnings
   - Server-side exceptions
   - Failed API calls
   - Slow operations or performance warnings
   - Deprecation notices

## Output Format

Present findings grouped by severity:
- 🔴 Errors (requires attention)
- 🟡 Warnings (should investigate)
- 🔵 Info (notable but not urgent)

Include timestamps and relevant context for each entry.
