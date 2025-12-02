---
description: Get guidance on Next.js Cache Components setup
argument-hint: "[component-path]"
---

Use the Next.js MCP server knowledge base to assist with Cache Components.

**Component to optimize (optional):** $ARGUMENTS

## If component path provided:

1. Read the specified component
2. Analyze if it's a good candidate for caching
3. Show how to convert it to a Cache Component using `"use cache"`
4. Explain the caching behavior and invalidation strategy

## If no path provided:

Explain Cache Components concepts:
- What `"use cache"` directive does
- When to use Cache Components vs regular Server Components
- How cache invalidation works with `revalidateTag` / `updateTag`
- Common patterns and gotchas

## Key Points to Cover

- Cache Components run at build time or on first request
- Use `cacheLife()` and `cacheTag()` for fine-grained control
- Difference between static caching and dynamic caching
- How to debug cache behavior
