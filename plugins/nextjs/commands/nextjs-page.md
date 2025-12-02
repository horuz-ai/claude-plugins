---
description: Get metadata about a specific Next.js page
argument-hint: "[route-path]"
---

Use the Next.js MCP server to get detailed metadata about a specific page.

**Route to analyze:** $ARGUMENTS

Call `get_page_metadata` for the specified route and present:
- Route path and segments
- Page component location
- Layout hierarchy
- Rendering mode (static/dynamic)
- Associated metadata
- Server Actions used (if any)

If no route is specified, ask which route to analyze or suggest checking the most recently viewed page.
