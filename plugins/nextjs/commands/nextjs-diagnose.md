---
description: Run a full diagnostic scan of the Next.js application
allowed-tools: ["Bash", "Read"]
---

Run a comprehensive diagnostic of the Next.js application using the MCP server.

## Workflow

Execute these checks in sequence:

1. **Errors Check** - Call `get_errors` for build/runtime/type errors
2. **Project Health** - Call `get_project_metadata` for config issues
3. **Logs Analysis** - Call `get_logs` and scan for warnings/errors
4. **Dev Server Status** - Verify the dev server is responding

## Output Format

Present a health report:

```
## Application Health Report

✅ Build Status: [passing/failing]
✅ Type Checking: [passing/X errors]
✅ Runtime: [stable/X issues]
✅ Dev Server: [running on port XXXX]

### Issues Found
[List any problems with severity and suggested fixes]

### Recommendations
[Any optimization suggestions]
```

Be concise - this is meant for a quick health check.
