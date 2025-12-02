---
description: Check all Next.js errors (build, runtime, type)
---

Use the Next.js MCP server to retrieve all current errors from the running dev server.

Call the `get_errors` tool and present a clear summary of:
- Build errors
- Runtime errors
- Type errors

Format the output as:
- Total error count
- Errors grouped by type with file location and brief description
- If no errors, confirm the app is error-free

Do not attempt fixes - just report what you find.
