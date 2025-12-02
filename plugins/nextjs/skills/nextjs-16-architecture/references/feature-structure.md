# Feature Structure Examples

## Complete Feature Example: Products

```
features/products/
├── components/
│   ├── server/
│   │   ├── product-list.tsx
│   │   ├── product-card.tsx
│   │   ├── product-details.tsx
│   │   └── category-nav.tsx
│   ├── client/
│   │   ├── add-to-cart-button.tsx
│   │   ├── product-filters.tsx
│   │   ├── quantity-selector.tsx
│   │   └── product-image-gallery.tsx
│   └── skeletons/
│       ├── product-list-skeleton.tsx
│       ├── product-card-skeleton.tsx
│       └── product-details-skeleton.tsx
├── data/
│   ├── get-products.ts
│   ├── get-product-by-id.ts
│   ├── get-product-by-slug.ts
│   ├── get-categories.ts
│   ├── get-featured-products.ts
│   └── get-related-products.ts
├── actions/
│   ├── create-product.ts
│   ├── update-product.ts
│   ├── delete-product.ts
│   └── add-to-cart.ts
├── hooks/
│   ├── use-product-filters.ts
│   ├── use-cart.ts
│   └── use-wishlist.ts
├── types/
│   ├── product.ts
│   ├── category.ts
│   ├── cart-item.ts
│   └── product-filter.ts
├── schemas/
│   ├── product-schema.ts
│   ├── product-filter-schema.ts
│   └── add-to-cart-schema.ts
└── contexts/
    └── cart-context.tsx
```

### Data Files

```typescript
// features/products/data/get-products.ts
import { cacheLife, cacheTag } from 'next/cache'
import { db } from '@/db'
import { products } from '@/db/schema'
import { eq, desc, asc } from 'drizzle-orm'
import type { Product } from '../types/product'
import type { ProductFilter } from '../types/product-filter'

export async function getProducts(filters?: ProductFilter): Promise<Product[]> {
  'use cache'
  cacheTag('products')
  cacheLife('hours')
  
  return db.query.products.findMany({
    where: filters?.category 
      ? eq(products.categoryId, filters.category) 
      : undefined,
    orderBy: getOrderBy(filters?.sort),
    limit: filters?.limit ?? 50,
  })
}

function getOrderBy(sort?: string) {
  switch (sort) {
    case 'price-asc': return asc(products.price)
    case 'price-desc': return desc(products.price)
    case 'newest': return desc(products.createdAt)
    default: return desc(products.createdAt)
  }
}
```

```typescript
// features/products/data/get-product-by-slug.ts
import { cacheLife, cacheTag } from 'next/cache'
import { db } from '@/db'
import { products } from '@/db/schema'
import { eq } from 'drizzle-orm'
import type { Product } from '../types/product'

export async function getProductBySlug(slug: string): Promise<Product | null> {
  'use cache'
  cacheTag(`product-${slug}`, 'products')
  cacheLife('days')
  
  const result = await db.query.products.findFirst({
    where: eq(products.slug, slug),
    with: {
      category: true,
      images: true,
    },
  })
  
  return result ?? null
}
```

### Type Files

```typescript
// features/products/types/product.ts
export interface Product {
  id: string
  name: string
  slug: string
  description: string | null
  price: number
  compareAtPrice: number | null
  categoryId: string
  imageUrl: string
  featured: boolean
  inStock: boolean
  createdAt: Date
  updatedAt: Date
}

export interface ProductWithCategory extends Product {
  category: {
    id: string
    name: string
    slug: string
  }
}
```

```typescript
// features/products/types/product-filter.ts
export interface ProductFilter {
  category?: string
  minPrice?: number
  maxPrice?: number
  inStock?: boolean
  sort?: 'price-asc' | 'price-desc' | 'newest' | 'popular'
  limit?: number
  offset?: number
}
```

### Schema Files

```typescript
// features/products/schemas/product-schema.ts
import { z } from 'zod'

export const productSchema = z.object({
  name: z
    .string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters'),
  slug: z
    .string()
    .min(1, 'Slug is required')
    .regex(/^[a-z0-9-]+$/, 'Slug must be lowercase with dashes'),
  description: z
    .string()
    .max(2000, 'Description must be less than 2000 characters')
    .optional(),
  price: z
    .number()
    .positive('Price must be positive')
    .multipleOf(0.01, 'Price must have at most 2 decimal places'),
  compareAtPrice: z
    .number()
    .positive()
    .optional(),
  categoryId: z.string().uuid('Invalid category'),
  imageUrl: z.string().url('Must be a valid URL'),
  featured: z.boolean().default(false),
  inStock: z.boolean().default(true),
})

export type ProductFormData = z.infer<typeof productSchema>
```

```typescript
// features/products/schemas/product-filter-schema.ts
import { z } from 'zod'

export const productFilterSchema = z.object({
  category: z.string().optional(),
  minPrice: z.coerce.number().min(0).optional(),
  maxPrice: z.coerce.number().min(0).optional(),
  inStock: z.coerce.boolean().optional(),
  sort: z.enum(['price-asc', 'price-desc', 'newest', 'popular']).optional(),
})

export type ProductFilterParams = z.infer<typeof productFilterSchema>
```

### Action Files

```typescript
// features/products/actions/create-product.ts
'use server'

import { updateTag } from 'next/cache'
import { redirect } from 'next/navigation'
import { db } from '@/db'
import { products } from '@/db/schema'
import { productSchema } from '../schemas/product-schema'
import { auth } from '@/features/auth/data/get-session'

export async function createProduct(formData: FormData) {
  const session = await auth()
  if (!session?.user || session.user.role !== 'admin') {
    return { error: 'Unauthorized' }
  }
  
  const raw = Object.fromEntries(formData.entries())
  const validated = productSchema.safeParse({
    ...raw,
    price: Number(raw.price),
    compareAtPrice: raw.compareAtPrice ? Number(raw.compareAtPrice) : undefined,
    featured: raw.featured === 'true',
    inStock: raw.inStock !== 'false',
  })
  
  if (!validated.success) {
    return { 
      error: 'Validation failed',
      fieldErrors: validated.error.flatten().fieldErrors 
    }
  }
  
  const [product] = await db.insert(products).values({
    ...validated.data,
    id: crypto.randomUUID(),
    createdAt: new Date(),
    updatedAt: new Date(),
  }).returning()
  
  updateTag('products')
  
  redirect(`/admin/products/${product.slug}`)
}
```

```typescript
// features/products/actions/add-to-cart.ts
'use server'

import { updateTag } from 'next/cache'
import { cookies } from 'next/headers'
import { db } from '@/db'
import { cartItems } from '@/db/schema'
import { addToCartSchema } from '../schemas/add-to-cart-schema'

export async function addToCart(productId: string, quantity: number = 1) {
  const validated = addToCartSchema.safeParse({ productId, quantity })
  
  if (!validated.success) {
    return { error: 'Invalid input' }
  }
  
  const cookieStore = await cookies()
  const sessionId = cookieStore.get('session-id')?.value
  
  if (!sessionId) {
    return { error: 'No session' }
  }
  
  await db.insert(cartItems).values({
    id: crypto.randomUUID(),
    sessionId,
    productId: validated.data.productId,
    quantity: validated.data.quantity,
  }).onConflictDoUpdate({
    target: [cartItems.sessionId, cartItems.productId],
    set: { 
      quantity: sql`${cartItems.quantity} + ${validated.data.quantity}` 
    },
  })
  
  updateTag(`cart-${sessionId}`)
  
  return { success: true }
}
```

### Hook Files

```typescript
// features/products/hooks/use-product-filters.ts
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback, useMemo } from 'react'
import { productFilterSchema, type ProductFilterParams } from '../schemas/product-filter-schema'

export function useProductFilters() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()
  
  const filters = useMemo<ProductFilterParams>(() => {
    const raw = Object.fromEntries(searchParams.entries())
    const parsed = productFilterSchema.safeParse(raw)
    return parsed.success ? parsed.data : {}
  }, [searchParams])
  
  const setFilter = useCallback(<K extends keyof ProductFilterParams>(
    key: K,
    value: ProductFilterParams[K]
  ) => {
    const params = new URLSearchParams(searchParams.toString())
    
    if (value === undefined || value === '') {
      params.delete(key)
    } else {
      params.set(key, String(value))
    }
    
    router.push(`${pathname}?${params.toString()}`)
  }, [router, pathname, searchParams])
  
  const clearFilters = useCallback(() => {
    router.push(pathname)
  }, [router, pathname])
  
  return { filters, setFilter, clearFilters }
}
```

### Server Component Files

```typescript
// features/products/components/server/product-list.tsx
import { getProducts } from '../../data/get-products'
import { ProductCard } from './product-card'
import type { ProductFilter } from '../../types/product-filter'

interface ProductListProps {
  searchParams: Promise<Record<string, string | undefined>>
}

export async function ProductList({ searchParams }: ProductListProps) {
  const params = await searchParams
  
  const filters: ProductFilter = {
    category: params.category,
    sort: params.sort as ProductFilter['sort'],
    minPrice: params.minPrice ? Number(params.minPrice) : undefined,
    maxPrice: params.maxPrice ? Number(params.maxPrice) : undefined,
  }
  
  const products = await getProducts(filters)
  
  if (products.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No products found</p>
      </div>
    )
  }
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

```typescript
// features/products/components/server/product-card.tsx
import Link from 'next/link'
import Image from 'next/image'
import { formatPrice } from '@/features/shared/lib/utils'
import { AddToCartButton } from '../client/add-to-cart-button'
import type { Product } from '../../types/product'

interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <div className="group border rounded-lg overflow-hidden">
      <Link href={`/products/${product.slug}`}>
        <div className="relative aspect-square">
          <Image
            src={product.imageUrl}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-105 transition-transform"
          />
        </div>
      </Link>
      
      <div className="p-4">
        <Link href={`/products/${product.slug}`}>
          <h3 className="font-medium hover:underline">{product.name}</h3>
        </Link>
        
        <div className="flex items-center justify-between mt-2">
          <span className="font-bold">{formatPrice(product.price)}</span>
          <AddToCartButton productId={product.id} />
        </div>
      </div>
    </div>
  )
}
```

### Client Component Files

```typescript
// features/products/components/client/product-filters.tsx
'use client'

import { useProductFilters } from '../../hooks/use-product-filters'
import { Button } from '@/features/shared/components/ui/button'
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/features/shared/components/ui/select'

export function ProductFilters() {
  const { filters, setFilter, clearFilters } = useProductFilters()
  
  return (
    <div className="space-y-4">
      <div>
        <label className="text-sm font-medium">Sort By</label>
        <Select
          value={filters.sort ?? ''}
          onValueChange={(value) => setFilter('sort', value || undefined)}
        >
          <SelectTrigger>
            <SelectValue placeholder="Select..." />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="newest">Newest</SelectItem>
            <SelectItem value="price-asc">Price: Low to High</SelectItem>
            <SelectItem value="price-desc">Price: High to Low</SelectItem>
            <SelectItem value="popular">Most Popular</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      <Button variant="outline" onClick={clearFilters}>
        Clear Filters
      </Button>
    </div>
  )
}
```

```typescript
// features/products/components/client/add-to-cart-button.tsx
'use client'

import { useTransition } from 'react'
import { ShoppingCart } from 'lucide-react'
import { addToCart } from '../../actions/add-to-cart'
import { Button } from '@/features/shared/components/ui/button'
import { useToast } from '@/features/shared/hooks/use-toast'

interface AddToCartButtonProps {
  productId: string
  quantity?: number
}

export function AddToCartButton({ productId, quantity = 1 }: AddToCartButtonProps) {
  const [isPending, startTransition] = useTransition()
  const { toast } = useToast()
  
  const handleClick = () => {
    startTransition(async () => {
      const result = await addToCart(productId, quantity)
      
      if (result.error) {
        toast({ title: 'Error', description: result.error, variant: 'destructive' })
      } else {
        toast({ title: 'Added to cart', description: 'Item added successfully' })
      }
    })
  }
  
  return (
    <Button size="sm" onClick={handleClick} disabled={isPending}>
      <ShoppingCart className="h-4 w-4" />
    </Button>
  )
}
```

## Complete Feature Example: Auth

```
features/auth/
├── components/
│   ├── login-form.tsx         # Client Component
│   ├── signup-form.tsx        # Client Component
│   ├── logout-button.tsx      # Client Component
│   └── user-nav.tsx           # Server Component
├── data/
│   ├── get-current-user.ts
│   └── get-session.ts
├── actions/
│   ├── login.ts
│   ├── signup.ts
│   └── logout.ts
├── hooks/
│   └── use-auth.ts
├── types/
│   ├── user.ts
│   └── session.ts
├── schemas/
│   ├── login-schema.ts
│   └── signup-schema.ts
└── contexts/
    └── auth-context.tsx
```

### Auth Data Files

```typescript
// features/auth/data/get-session.ts
import { cookies } from 'next/headers'
import { db } from '@/db'
import { sessions, users } from '@/db/schema'
import { eq, and, gt } from 'drizzle-orm'
import type { Session } from '../types/session'

export async function getSession(): Promise<Session | null> {
  const cookieStore = await cookies()
  const token = cookieStore.get('session-token')?.value
  
  if (!token) return null
  
  const [session] = await db
    .select({
      id: sessions.id,
      userId: sessions.userId,
      expiresAt: sessions.expiresAt,
      user: {
        id: users.id,
        email: users.email,
        name: users.name,
        role: users.role,
      },
    })
    .from(sessions)
    .innerJoin(users, eq(sessions.userId, users.id))
    .where(
      and(
        eq(sessions.token, token),
        gt(sessions.expiresAt, new Date())
      )
    )
    .limit(1)
  
  return session ?? null
}

// Alias for convenience
export const auth = getSession
```

```typescript
// features/auth/data/get-current-user.ts
import { cacheLife, cacheTag } from 'next/cache'
import { db } from '@/db'
import { users } from '@/db/schema'
import { eq } from 'drizzle-orm'
import type { User } from '../types/user'

export async function getCurrentUser(userId: string): Promise<User | null> {
  'use cache: private'
  cacheTag(`user-${userId}`)
  cacheLife({ stale: 60 * 5 })  // 5 min stale
  
  const [user] = await db
    .select()
    .from(users)
    .where(eq(users.id, userId))
    .limit(1)
  
  return user ?? null
}
```

### Auth Schema Files

```typescript
// features/auth/schemas/login-schema.ts
import { z } from 'zod'

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(1, 'Password is required'),
})

export type LoginFormData = z.infer<typeof loginSchema>
```

```typescript
// features/auth/schemas/signup-schema.ts
import { z } from 'zod'

export const signupSchema = z.object({
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      'Password must contain uppercase, lowercase, and number'
    ),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
})

export type SignupFormData = z.infer<typeof signupSchema>
```

## Shared Feature Structure

```
features/shared/
├── components/
│   └── ui/                    # shadcn/ui components
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       ├── dialog.tsx
│       ├── dropdown-menu.tsx
│       ├── form.tsx
│       ├── select.tsx
│       ├── toast.tsx
│       └── toaster.tsx
├── layouts/
│   ├── root-layout.tsx
│   ├── dashboard-layout.tsx
│   └── auth-layout.tsx
├── lib/
│   ├── utils.ts               # cn(), formatPrice(), etc.
│   └── constants.ts
├── hooks/
│   ├── use-toast.ts
│   ├── use-media-query.ts
│   └── use-mounted.ts
└── types/
    ├── api.ts                 # API response types
    └── common.ts              # Shared utility types
```

### Shared Utility File

```typescript
// features/shared/lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatPrice(
  price: number,
  options: Intl.NumberFormatOptions = {}
) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    ...options,
  }).format(price)
}

export function formatDate(
  date: Date | string,
  options: Intl.DateTimeFormatOptions = {}
) {
  return new Intl.DateTimeFormat('en-US', {
    dateStyle: 'medium',
    ...options,
  }).format(new Date(date))
}
```
