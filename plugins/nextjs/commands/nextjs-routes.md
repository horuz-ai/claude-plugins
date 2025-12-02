---
description: List all routes in the Next.js application
allowed-tools: ["Bash", "Glob"]
---

Discover and list all routes in the Next.js App Router application.

## Workflow

1. Call `get_project_metadata` to confirm app structure
2. Scan the `app/` directory for `page.tsx` and `route.ts` files
3. Present a clear route map

## Output Format

```
## Application Routes

📄 Pages
  / → app/page.tsx
  /about → app/about/page.tsx
  /blog/[slug] → app/blog/[slug]/page.tsx

🔌 API Routes
  /api/users → app/api/users/route.ts
  /api/auth/[...nextauth] → app/api/auth/[...nextauth]/route.ts

📁 Route Groups
  (marketing) → app/(marketing)/...
  (dashboard) → app/(dashboard)/...
```

Include dynamic segments, catch-all routes, and route groups.
