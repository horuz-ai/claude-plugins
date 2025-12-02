# Migration Guide: Next.js 15 → 16

## Key Breaking Changes

| Next.js 15 | Next.js 16 |
|------------|------------|
| `params` sync | `params` is `Promise` |
| `searchParams` sync | `searchParams` is `Promise` |
| `cookies()` sync | `cookies()` is `Promise` |
| `headers()` sync | `headers()` is `Promise` |
| Implicit caching | Explicit `'use cache'` |
| `middleware.ts` | `proxy.ts` |
| `revalidateTag(tag)` | `revalidateTag(tag, 'max')` |
| Node.js 18 supported | Node.js 20.9+ required |

## Async Dynamic APIs

### Before (Next.js 15)

```typescript
export default function Page({ 
  params, 
  searchParams 
}: { 
  params: { id: string }
  searchParams: { q?: string }
}) {
  const cookieStore = cookies()
  const headersList = headers()
  
  return <div>{params.id}</div>
}
```

### After (Next.js 16)

```typescript
export default async function Page({ 
  params, 
  searchParams 
}: { 
  params: Promise<{ id: string }>
  searchParams: Promise<{ q?: string }>
}) {
  const { id } = await params
  const { q } = await searchParams
  const cookieStore = await cookies()
  const headersList = await headers()
  
  return <div>{id}</div>
}
```

## Caching Changes

### Before: Implicit Caching

```typescript
// Cached by default (confusing)
const data = await fetch('/api/data')

// Opt OUT of caching
const data = await fetch('/api/data', { cache: 'no-store' })

// ISR
export const revalidate = 3600
```

### After: Explicit Caching

```typescript
// NOT cached by default (predictable)
const data = await fetch('/api/data')

// Opt INTO caching with 'use cache'
import { cacheLife, cacheTag } from 'next/cache'

export async function getData() {
  'use cache'
  cacheTag('data')
  cacheLife('hours')
  
  return fetch('/api/data')
}
```

## Configuration

### Before

```typescript
// next.config.ts
const nextConfig = {
  experimental: {
    ppr: true,
  },
}
```

### After

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  cacheComponents: true,
}
```

## Route Segment Configs

### `force-static` → `'use cache'`

```typescript
// BEFORE
export const dynamic = 'force-static'

export default async function Page() {
  const data = await fetch('/api/data')
  return <div>{data}</div>
}

// AFTER
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('max')
  
  const data = await fetch('/api/data')
  return <div>{data}</div>
}
```

### `revalidate` → `cacheLife`

```typescript
// BEFORE
export const revalidate = 3600

// AFTER
import { cacheLife } from 'next/cache'

export default async function Page() {
  'use cache'
  cacheLife('hours')
  // ...
}
```

## Cache Invalidation

### Before

```typescript
'use server'
import { revalidateTag } from 'next/cache'

export async function updateData() {
  await db.update()
  revalidateTag('data')  // Single argument
}
```

### After

```typescript
'use server'
import { revalidateTag, updateTag } from 'next/cache'

// For Server Actions (immediate update)
export async function updateData() {
  await db.update()
  updateTag('data')  // Immediate invalidation
}

// For Route Handlers / webhooks (stale-while-revalidate)
export async function POST() {
  await db.update()
  revalidateTag('data', 'max')  // Background refresh
}
```

## `unstable_cache` → `'use cache'`

### Before

```typescript
import { unstable_cache } from 'next/cache'

const getCachedUser = unstable_cache(
  async (id: string) => db.users.findById(id),
  ['user'],
  { revalidate: 3600, tags: ['user'] }
)
```

### After

```typescript
import { cacheLife, cacheTag } from 'next/cache'

export async function getUser(id: string) {
  'use cache'
  cacheTag(`user-${id}`, 'users')
  cacheLife('hours')
  
  return db.users.findById(id)
}
```

## Middleware → Proxy

### Before (`middleware.ts`)

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/admin')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

export const config = {
  matcher: '/admin/:path*',
}
```

### After (`proxy.ts`)

```typescript
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export default function proxy(request: NextRequest) {
  if (request.nextUrl.pathname.startsWith('/admin')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

export const config = {
  matcher: '/admin/:path*',
}
```

## Migration Checklist

### Configuration
- [ ] Update to Node.js 20.9+
- [ ] Add `cacheComponents: true` to next.config.ts
- [ ] Remove `experimental.ppr` if present

### Routes & Pages
- [ ] Make all page components `async`
- [ ] Await `params` in dynamic routes
- [ ] Await `searchParams` where used
- [ ] Await `cookies()` calls
- [ ] Await `headers()` calls

### Caching
- [ ] Replace `dynamic = 'force-static'` with `'use cache'` + `cacheLife('max')`
- [ ] Replace `revalidate` exports with `cacheLife()`
- [ ] Replace `unstable_cache` with `'use cache'`
- [ ] Update `revalidateTag()` to use two arguments

### Server Actions
- [ ] Use `updateTag()` for immediate invalidation
- [ ] Use `revalidateTag(..., 'max')` for background refresh

### Middleware
- [ ] Rename `middleware.ts` → `proxy.ts`
- [ ] Rename `middleware()` → `proxy()` (default export)

### Images
- [ ] Note: `next/image` now uses `decoding="sync"` by default
- [ ] `localPatterns` now enabled by default

## Codemod

Run the official codemod to automate most changes:

```bash
npx @next/codemod@latest upgrade
```

This handles:
- Async dynamic APIs
- Route segment configs
- Some caching patterns

Manual review still needed for:
- Custom caching logic
- Complex `unstable_cache` usage
- Middleware logic

## Testing Migration

### Build Check

```bash
npm run build
```

Look for:
- ○ (Static) - Prerendered at build
- λ (Server) - Server-rendered
- ◐ (Partial) - Partially prerendered (PPR)

### Cache Headers

Check in browser DevTools:
- `x-nextjs-cache: HIT | MISS | STALE`
- `x-nextjs-stale-time: <seconds>`

### Logging

Add logging to verify cache behavior:

```typescript
export async function getData() {
  'use cache'
  cacheTag('data')
  cacheLife('hours')
  
  console.log('Cache miss at:', new Date().toISOString())
  return db.query()
}
```

## Common Issues

### Error: Async params not awaited

```typescript
// BAD
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>
}

// GOOD
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  return <div>{id}</div>
}
```

### Error: cookies() in cached function

```typescript
// BAD
export async function getData() {
  'use cache'
  const session = await cookies()  // Error!
}

// GOOD - Read outside, pass as arg
export async function getData(sessionId: string) {
  'use cache'
  cacheTag(`data-${sessionId}`)
  // ...
}

// OR - Use private cache
export async function getData() {
  'use cache: private'
  const session = await cookies()  // OK in private cache
}
```

### Error: revalidateTag single argument deprecated

```typescript
// BAD (deprecated)
revalidateTag('products')

// GOOD
revalidateTag('products', 'max')  // Stale-while-revalidate
// OR
updateTag('products')  // Immediate (Server Actions only)
```
