---
name: nextjs-16-architecture
description: "Comprehensive Next.js v16 development with Cache Components, feature-based architecture, and best practices. Use for ANY Next.js 16 task to know: (1) Project structure with features folder pattern, (2) Where to fetch data with 'use cache', (3) Server vs Client component decisions, (4) One file per query/type/schema/hook pattern, (5) Cache invalidation with updateTag/revalidateTag, (6) Proper component organization within features. Apply to all Next.js 16 development tasks."
---

# Next.js 16 Architecture & Cache Components

This skill teaches Claude Code the complete approach to building Next.js 16 applications with feature-based architecture, Cache Components, and proper code organization.

## Project Structure

Root folder contains ONLY three directories:

```
├── app/                    # Next.js App Router (routes only)
├── db/                     # Database configuration & schema
├── features/               # ALL application code lives here
├── next.config.ts
├── package.json
└── tsconfig.json
```

### The `features/` Folder

All application code is organized by feature. Each feature is self-contained:

```
features/
├── shared/                 # Shared across all features
│   ├── components/
│   │   └── ui/            # shadcn/ui components
│   │       ├── button.tsx
│   │       ├── input.tsx
│   │       └── card.tsx
│   ├── layouts/           # Shared layouts
│   │   └── dashboard-layout.tsx
│   ├── lib/               # Shared utilities
│   │   └── utils.ts
│   ├── hooks/
│   │   └── use-media-query.ts
│   └── types/
│       └── common.ts
│
├── auth/                   # Auth feature
│   ├── components/
│   │   ├── login-form.tsx
│   │   └── signup-form.tsx
│   ├── data/              # Server-side data fetching
│   │   ├── get-current-user.ts
│   │   └── get-session.ts
│   ├── actions/           # Server Actions
│   │   ├── login.ts
│   │   └── logout.ts
│   ├── hooks/
│   │   └── use-auth-state.ts
│   ├── types/
│   │   └── user.ts
│   ├── schemas/           # Zod schemas
│   │   └── login-schema.ts
│   └── contexts/
│       └── auth-context.tsx
│
├── products/               # Products feature
│   ├── components/
│   │   ├── server/        # Server Components
│   │   │   ├── product-list.tsx
│   │   │   └── product-card.tsx
│   │   └── client/        # Client Components
│   │       ├── add-to-cart-button.tsx
│   │       └── product-filters.tsx
│   ├── data/
│   │   ├── get-products.ts
│   │   ├── get-product-by-id.ts
│   │   └── get-categories.ts
│   ├── actions/
│   │   ├── create-product.ts
│   │   └── update-product.ts
│   ├── hooks/
│   │   └── use-product-filters.ts
│   ├── types/
│   │   ├── product.ts
│   │   └── category.ts
│   └── schemas/
│       ├── product-schema.ts
│       └── product-filter-schema.ts
```

### Key Rules

1. **One file = One export** for queries, types, schemas, hooks, actions
2. **Feature isolation**: Features import from `shared/` or their own folder, never from other features
3. **Colocation**: Data fetching (`data/`) lives in the feature that uses it
4. **Server/Client split**: Separate Server and Client Components in `components/server/` and `components/client/`

## The `app/` Folder

Routes only. Pages orchestrate, don't contain business logic:

```
app/
├── layout.tsx              # Root layout with providers
├── page.tsx                # Home page
├── loading.tsx             # Root loading
├── (auth)/                 # Auth route group
│   ├── login/
│   │   └── page.tsx
│   └── signup/
│       └── page.tsx
├── (dashboard)/            # Dashboard route group
│   ├── layout.tsx
│   ├── products/
│   │   ├── page.tsx
│   │   ├── loading.tsx
│   │   └── [id]/
│   │       └── page.tsx
│   └── settings/
│       └── page.tsx
└── api/                    # API routes (if needed)
```

### Page Pattern

Pages import from features and compose:

```typescript
// app/(dashboard)/products/page.tsx
import { Suspense } from 'react'
import { ProductList } from '@/features/products/components/server/product-list'
import { ProductFilters } from '@/features/products/components/client/product-filters'
import { ProductListSkeleton } from '@/features/products/components/skeletons'

export default function ProductsPage({
  searchParams,
}: {
  searchParams: Promise<{ category?: string; sort?: string }>
}) {
  return (
    <main className="grid grid-cols-4 gap-8">
      <aside>
        <ProductFilters />
      </aside>
      <section className="col-span-3">
        <Suspense fallback={<ProductListSkeleton />}>
          <ProductList searchParams={searchParams} />
        </Suspense>
      </section>
    </main>
  )
}
```

## Next.js 16 Configuration

```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,  // Enable Cache Components
  // Optional: Custom cache life profiles
  cacheLife: {
    products: {
      stale: 60 * 5,      // 5 minutes
      revalidate: 60 * 60, // 1 hour
      expire: 60 * 60 * 24 // 1 day
    }
  }
}

export default nextConfig
```

## Data Fetching Pattern

### One Query Per File

```typescript
// features/products/data/get-products.ts
import { cacheLife, cacheTag } from 'next/cache'
import { db } from '@/db'
import type { Product } from '../types/product'

interface GetProductsParams {
  category?: string
  sort?: 'price-asc' | 'price-desc' | 'newest'
}

export async function getProducts(params?: GetProductsParams): Promise<Product[]> {
  'use cache'
  cacheTag('products')
  cacheLife('hours')
  
  return db.query.products.findMany({
    where: params?.category ? eq(products.category, params.category) : undefined,
    orderBy: getOrderBy(params?.sort),
  })
}
```

```typescript
// features/products/data/get-product-by-id.ts
import { cacheLife, cacheTag } from 'next/cache'
import { db } from '@/db'
import type { Product } from '../types/product'

export async function getProductById(id: string): Promise<Product | null> {
  'use cache'
  cacheTag(`product-${id}`, 'products')
  cacheLife('days')
  
  return db.query.products.findFirst({
    where: eq(products.id, id),
  })
}
```

### Server Component Using Data

```typescript
// features/products/components/server/product-list.tsx
import { getProducts } from '../../data/get-products'
import { ProductCard } from './product-card'

interface ProductListProps {
  searchParams: Promise<{ category?: string; sort?: string }>
}

export async function ProductList({ searchParams }: ProductListProps) {
  const params = await searchParams
  const products = await getProducts(params)
  
  if (products.length === 0) {
    return <EmptyState message="No products found" />
  }
  
  return (
    <div className="grid grid-cols-3 gap-4">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

## Types Pattern

### One Type Per File

```typescript
// features/products/types/product.ts
export interface Product {
  id: string
  name: string
  description: string
  price: number
  category: string
  imageUrl: string
  createdAt: Date
  updatedAt: Date
}
```

```typescript
// features/products/types/category.ts
export interface Category {
  id: string
  name: string
  slug: string
}
```

## Schemas Pattern (Zod)

### One Schema Per File

```typescript
// features/products/schemas/product-schema.ts
import { z } from 'zod'

export const productSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  description: z.string().max(500).optional(),
  price: z.number().positive('Price must be positive'),
  category: z.string().min(1, 'Category is required'),
  imageUrl: z.string().url('Must be a valid URL').optional(),
})

export type ProductFormData = z.infer<typeof productSchema>
```

```typescript
// features/products/schemas/product-filter-schema.ts
import { z } from 'zod'

export const productFilterSchema = z.object({
  category: z.string().optional(),
  minPrice: z.coerce.number().optional(),
  maxPrice: z.coerce.number().optional(),
  sort: z.enum(['price-asc', 'price-desc', 'newest']).optional(),
})

export type ProductFilterData = z.infer<typeof productFilterSchema>
```

## Server Actions Pattern

### One Action Per File

```typescript
// features/products/actions/create-product.ts
'use server'

import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'
import { db } from '@/db'
import { productSchema } from '../schemas/product-schema'

export async function createProduct(formData: FormData) {
  const raw = Object.fromEntries(formData.entries())
  const validated = productSchema.safeParse(raw)
  
  if (!validated.success) {
    return { error: validated.error.flatten().fieldErrors }
  }
  
  const product = await db.insert(products).values(validated.data).returning()
  
  // Immediate cache invalidation for read-your-own-writes
  updateTag('products')
  
  redirect(`/products/${product[0].id}`)
}
```

```typescript
// features/products/actions/update-product.ts
'use server'

import { updateTag } from 'next/cache'
import { db } from '@/db'
import { productSchema } from '../schemas/product-schema'

export async function updateProduct(id: string, formData: FormData) {
  const raw = Object.fromEntries(formData.entries())
  const validated = productSchema.safeParse(raw)
  
  if (!validated.success) {
    return { error: validated.error.flatten().fieldErrors }
  }
  
  await db.update(products).set(validated.data).where(eq(products.id, id))
  
  // Invalidate both specific product and list
  updateTag(`product-${id}`)
  updateTag('products')
  
  return { success: true }
}
```

## Cache Invalidation

### `updateTag` vs `revalidateTag`

| Function | Use Case | Behavior |
|----------|----------|----------|
| `updateTag(tag)` | Server Actions (read-your-own-writes) | Immediate expiration, blocks until fresh |
| `revalidateTag(tag, 'max')` | Route Handlers, webhooks | Stale-while-revalidate |

```typescript
// Server Action: Use updateTag for immediate UI update
'use server'
import { updateTag } from 'next/cache'

export async function addToCart(productId: string) {
  await db.carts.addItem(productId)
  updateTag('cart')  // User sees change immediately
}

// Route Handler: Use revalidateTag for background refresh
import { revalidateTag } from 'next/cache'

export async function POST(request: Request) {
  // Webhook from CMS
  const { type } = await request.json()
  revalidateTag('products', 'max')  // Stale-while-revalidate
  return Response.json({ revalidated: true })
}
```

## Hooks Pattern

### One Hook Per File

```typescript
// features/products/hooks/use-product-filters.ts
'use client'

import { useRouter, useSearchParams } from 'next/navigation'
import { useCallback } from 'react'
import type { ProductFilterData } from '../schemas/product-filter-schema'

export function useProductFilters() {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  const filters: ProductFilterData = {
    category: searchParams.get('category') ?? undefined,
    sort: searchParams.get('sort') as ProductFilterData['sort'] ?? undefined,
  }
  
  const setFilters = useCallback((newFilters: Partial<ProductFilterData>) => {
    const params = new URLSearchParams(searchParams.toString())
    
    Object.entries(newFilters).forEach(([key, value]) => {
      if (value) {
        params.set(key, String(value))
      } else {
        params.delete(key)
      }
    })
    
    router.push(`?${params.toString()}`)
  }, [router, searchParams])
  
  return { filters, setFilters }
}
```

## Client Components

### Minimal & Leaf Nodes Only

```typescript
// features/products/components/client/add-to-cart-button.tsx
'use client'

import { useTransition } from 'react'
import { addToCart } from '../../actions/add-to-cart'
import { Button } from '@/features/shared/components/ui/button'

interface AddToCartButtonProps {
  productId: string
}

export function AddToCartButton({ productId }: AddToCartButtonProps) {
  const [isPending, startTransition] = useTransition()
  
  const handleClick = () => {
    startTransition(async () => {
      await addToCart(productId)
    })
  }
  
  return (
    <Button onClick={handleClick} disabled={isPending}>
      {isPending ? 'Adding...' : 'Add to Cart'}
    </Button>
  )
}
```

## Decision Tree

```
Creating a new file?
├── Is it a route? → app/
├── Is it shared UI (shadcn)? → features/shared/components/ui/
├── Is it a shared layout? → features/shared/layouts/
└── Is it feature-specific?
    └── Which feature? → features/[feature]/
        ├── Server data fetching? → data/get-[entity].ts
        ├── Mutation/action? → actions/[action-name].ts
        ├── Type definition? → types/[entity].ts
        ├── Zod schema? → schemas/[entity]-schema.ts
        ├── React hook? → hooks/use-[name].ts
        ├── Server Component? → components/server/[name].tsx
        ├── Client Component? → components/client/[name].tsx
        └── Context? → contexts/[name]-context.tsx
```

## Cache Life Profiles

| Profile   | stale  | revalidate | expire  | Use Case                    |
|-----------|--------|------------|---------|----------------------------|
| `seconds` | 0      | 1 sec      | 1 min   | Near real-time             |
| `minutes` | 5 min  | 1 min      | 1 hour  | Frequently updated         |
| `hours`   | 30 min | 1 hour     | 1 day   | Updated few times per day  |
| `days`    | 1 day  | 1 day      | 1 week  | Rarely updated             |
| `weeks`   | 1 week | 1 day      | 1 month | Very stable content        |
| `max`     | 1 week | 1 month    | 1 year  | Static/archival content    |

## Quick Reference

| Need | Solution |
|------|----------|
| Static data, same for all users | `'use cache'` + `cacheLife('days')` |
| User-specific cacheable data | `'use cache: private'` |
| Dynamic data, never cache | `connection()` + `<Suspense>` |
| Interactive UI | `'use client'` (keep small!) |
| Loading state for component | Wrap in `<Suspense>` |
| Loading state for route | `loading.tsx` |
| Immediate cache invalidation | `updateTag('tag')` |
| Background revalidation | `revalidateTag('tag', 'max')` |

## References

For detailed patterns:
- [`references/cache-patterns.md`](references/cache-patterns.md) - Advanced caching strategies
- [`references/feature-structure.md`](references/feature-structure.md) - Complete feature folder examples
- [`references/migration-guide.md`](references/migration-guide.md) - Migrating from Next.js 15
