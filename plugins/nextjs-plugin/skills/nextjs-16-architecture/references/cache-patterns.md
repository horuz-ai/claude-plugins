# Advanced Cache Patterns

## Cache Variants

### Standard Cache (`'use cache'`)

For static, shared data:

```typescript
// features/products/data/get-featured-products.ts
import { cacheLife, cacheTag } from 'next/cache'

export async function getFeaturedProducts() {
  'use cache'
  cacheTag('featured-products')
  cacheLife('hours')
  
  return db.query.products.findMany({
    where: eq(products.featured, true),
    limit: 10,
  })
}
```

### Private Cache (`'use cache: private'`)

For user-specific cacheable data:

```typescript
// features/cart/data/get-cart.ts
import { cacheLife, cacheTag } from 'next/cache'
import { cookies } from 'next/headers'

export async function getCart() {
  'use cache: private'
  cacheLife({ stale: 60 })  // Minimum 30s for private cache
  
  const sessionId = (await cookies()).get('session-id')?.value
  if (!sessionId) return null
  
  cacheTag(`cart-${sessionId}`)
  
  return db.query.carts.findFirst({
    where: eq(carts.sessionId, sessionId),
    with: { items: true },
  })
}
```

### Remote Cache (`'use cache: remote'`)

For shared data in dynamic contexts:

```typescript
// features/products/data/get-product-price.ts
import { cacheLife, cacheTag } from 'next/cache'
import { connection } from 'next/server'

export async function getProductWithDynamicPrice(id: string) {
  // Dynamic context established
  await connection()
  
  // Price can still be cached and shared
  const price = await getProductPrice(id)
  return price
}

async function getProductPrice(productId: string) {
  'use cache: remote'
  cacheTag(`price-${productId}`)
  cacheLife('minutes')
  
  return db.query.prices.findFirst({
    where: eq(prices.productId, productId),
  })
}
```

## Conditional Cache Lifetime

```typescript
// features/posts/data/get-post.ts
import { cacheLife, cacheTag } from 'next/cache'

export async function getPost(slug: string) {
  'use cache'
  cacheTag(`post-${slug}`)
  
  const post = await db.query.posts.findFirst({
    where: eq(posts.slug, slug),
  })
  
  if (!post) {
    cacheLife('minutes')  // Check again soon
    return null
  }
  
  if (post.status === 'draft') {
    cacheLife('seconds')  // Drafts change frequently
    return post
  }
  
  cacheLife('days')  // Published content stable
  return post
}
```

## Request Deduplication

Combine React `cache()` with `'use cache'`:

```typescript
// features/products/data/get-product-by-id.ts
import { cache } from 'react'
import { cacheLife, cacheTag } from 'next/cache'

// Layer 1: Request deduplication (same render)
export const getProductById = cache(async (id: string) => {
  return fetchProductFromCache(id)
})

// Layer 2: Persistent cache (across requests)
async function fetchProductFromCache(id: string) {
  'use cache'
  cacheTag(`product-${id}`)
  cacheLife('hours')
  
  return db.query.products.findFirst({
    where: eq(products.id, id),
  })
}
```

## Tag Hierarchy

```typescript
// features/products/data/get-products.ts
export async function getProducts() {
  'use cache'
  cacheTag('products')  // Broad tag
  cacheLife('hours')
  
  return db.query.products.findMany()
}

// features/products/data/get-product-by-id.ts
export async function getProductById(id: string) {
  'use cache'
  cacheTag('products', `product-${id}`)  // Both broad and specific
  cacheLife('days')
  
  return db.query.products.findFirst({ where: eq(products.id, id) })
}

// features/products/data/get-product-reviews.ts
export async function getProductReviews(productId: string) {
  'use cache'
  cacheTag('reviews', `product-${productId}-reviews`)
  cacheLife('minutes')
  
  return db.query.reviews.findMany({ where: eq(reviews.productId, productId) })
}

// Invalidation options:
// updateTag('products')                    // All products + individual
// updateTag(`product-${id}`)               // Single product only
// updateTag('reviews')                     // All reviews
// updateTag(`product-${id}-reviews`)       // Reviews for one product
```

## Parallel Data Fetching

```typescript
// features/dashboard/components/server/dashboard.tsx
import { getStats } from '../../data/get-stats'
import { getRecentActivity } from '../../data/get-recent-activity'
import { getNotifications } from '../../data/get-notifications'

export async function Dashboard() {
  // Start all fetches in parallel
  const [stats, activity, notifications] = await Promise.all([
    getStats(),
    getRecentActivity(),
    getNotifications(),
  ])
  
  return (
    <div>
      <StatsCard stats={stats} />
      <ActivityFeed activity={activity} />
      <NotificationList notifications={notifications} />
    </div>
  )
}
```

## Streaming with Independent Suspense

```typescript
// app/(dashboard)/page.tsx
import { Suspense } from 'react'
import { Stats } from '@/features/dashboard/components/server/stats'
import { Activity } from '@/features/dashboard/components/server/activity'
import { Chart } from '@/features/dashboard/components/server/chart'

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-2 gap-4">
      {/* Each streams independently */}
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>
      
      <Suspense fallback={<ChartSkeleton />}>
        <Chart />
      </Suspense>
      
      <div className="col-span-2">
        <Suspense fallback={<ActivitySkeleton />}>
          <Activity />
        </Suspense>
      </div>
    </div>
  )
}
```

## Preloading Pattern

```typescript
// features/products/data/get-product-by-id.ts
import { cache } from 'react'

// Preload function for eager fetching
export const preloadProduct = (id: string) => {
  void getProductById(id)  // Fire and forget
}

export const getProductById = cache(async (id: string) => {
  'use cache'
  cacheTag(`product-${id}`)
  cacheLife('hours')
  
  return db.query.products.findFirst({ where: eq(products.id, id) })
})
```

```typescript
// app/(dashboard)/products/[id]/page.tsx
import { preloadProduct, getProductById } from '@/features/products/data/get-product-by-id'
import { getRecommendations } from '@/features/products/data/get-recommendations'

export default async function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  
  // Start loading immediately
  preloadProduct(id)
  
  // Do other work (e.g., get recommendations)
  const recommendations = await getRecommendations(id)
  
  // Product likely ready by now
  const product = await getProductById(id)
  
  return <ProductDetails product={product} recommendations={recommendations} />
}
```

## Batch Invalidation

```typescript
// features/products/actions/bulk-update-products.ts
'use server'

import { updateTag } from 'next/cache'

export async function bulkUpdateProducts(ids: string[], data: Partial<Product>) {
  await db.update(products).set(data).where(inArray(products.id, ids))
  
  // Invalidate all affected caches
  updateTag('products')  // List
  ids.forEach(id => updateTag(`product-${id}`))  // Individual
}
```

## Error Handling in Cache

```typescript
// features/external/data/get-weather.ts
import { cacheLife, cacheTag } from 'next/cache'

export async function getWeather(city: string) {
  'use cache'
  cacheTag(`weather-${city}`)
  
  try {
    const response = await fetch(`https://api.weather.com/${city}`)
    
    if (!response.ok) {
      cacheLife('minutes')  // Cache error briefly
      return { data: null, error: 'Failed to fetch weather' }
    }
    
    cacheLife('hours')  // Cache success longer
    return { data: await response.json(), error: null }
  } catch (error) {
    cacheLife('seconds')  // Network error, retry soon
    return { data: null, error: 'Network error' }
  }
}
```

## Children Pass-Through

Cached wrapper doesn't affect children's caching:

```typescript
// features/shared/layouts/cached-layout.tsx
import { cacheLife, cacheTag } from 'next/cache'
import { getNavigation } from '../data/get-navigation'
import { getFooter } from '../data/get-footer'

export async function CachedLayout({ children }: { children: React.ReactNode }) {
  'use cache'
  cacheTag('layout')
  cacheLife('days')
  
  const [nav, footer] = await Promise.all([
    getNavigation(),
    getFooter(),
  ])
  
  return (
    <>
      <Nav items={nav} />
      {children}  {/* Children have independent caching */}
      <Footer data={footer} />
    </>
  )
}
```

## updateTag vs revalidateTag Reference

| Scenario | Function | Example |
|----------|----------|---------|
| Form submission | `updateTag` | User creates post, sees it immediately |
| CMS webhook | `revalidateTag(..., 'max')` | Content update, serve stale while refreshing |
| Admin bulk update | `updateTag` | Admin updates prices, sees changes |
| Scheduled job | `revalidateTag(..., 'max')` | Nightly data sync |
| User action | `updateTag` | Add to cart, quantity updates |

```typescript
// features/posts/actions/create-post.ts
'use server'
import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.insert(posts).values({...}).returning()
  
  updateTag('posts')  // Immediate - user sees their post
  
  redirect(`/posts/${post[0].slug}`)
}
```

```typescript
// app/api/webhooks/cms/route.ts
import { revalidateTag } from 'next/cache'

export async function POST(request: Request) {
  const { type, slug } = await request.json()
  
  // Background revalidation - serve stale while refreshing
  revalidateTag(`post-${slug}`, 'max')
  revalidateTag('posts', 'max')
  
  return Response.json({ revalidated: true })
}
```
