---
name: nuxt-pages
description: File-based routing with page patterns for lists, details, and navigation. Use when creating pages, defining page meta (permissions, layouts), implementing list/detail patterns, or setting up breadcrumbs and headers.
---

# Nuxt Pages

File-based routing with common page patterns and navigation.

## Core Concepts

**[pages.md](references/pages.md)** - Page patterns, meta, layouts, navigation

## Directory Structure

```
pages/
├── index.vue              # Dashboard/redirect
├── profile.vue            # User profile
├── auth/
│   └── login.vue          # Login page
├── posts/
│   ├── index.vue          # List view
│   └── [ulid].vue         # Detail view
└── users/
    ├── index.vue
    └── [ulid].vue
```

## List Page Pattern

```vue
<script lang="ts" setup>
import getPostsQueryFactory, { type GetPostsFilters } from '~/features/posts/queries/get-posts-query'
import { ListPosts, CreatePost } from '~/constants/permissions'

definePageMeta({ permissions: ListPosts })

const { setAppHeader } = useAppHeader()
setAppHeader({ title: 'Posts', icon: 'lucide:file-text' })

const { filters } = useReactiveFilters<GetPostsFilters>({
  status: undefined,
  page: 1,
  size: 25,
})

const getPostsQuery = getPostsQueryFactory()
const { data: posts, isLoading, pagination } = getPostsQuery(filters)
</script>

<template>
  <div>
    <UInput v-model="filters.search" placeholder="Search..." />
    <PostsTable :posts="posts?.data || []" :loading="isLoading" />
    <XPagination v-if="pagination" v-model:page="filters.page" :pagination="pagination" />
  </div>
</template>
```

## Detail Page Pattern

```vue
<script lang="ts" setup>
import getPostQueryFactory from '~/features/posts/queries/get-post-query'

definePageMeta({ permissions: 'posts.show' })

const route = useRoute()
const ulid = computed(() => route.params.ulid as string)

const getPostQuery = getPostQueryFactory()
const { data: post, isLoading } = getPostQuery(ulid)
</script>

<template>
  <UTabs v-if="!isLoading && post" :items="tabs">
    <template #details><PostDetail :post="post.data" /></template>
  </UTabs>
</template>
```
