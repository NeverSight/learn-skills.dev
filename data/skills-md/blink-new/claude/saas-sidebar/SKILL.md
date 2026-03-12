---
name: saas-sidebar
description: Build a modern, collapsible sidebar for SaaS dashboards following the ChatGPT/Notion design pattern
---

# SaaS Collapsible Sidebar

Build a polished, collapsible sidebar using the **shadcn/ui Sidebar component system**. Covers every detail: icon-mode centering, hover-swap expand button, auto-tooltips, keyboard shortcuts, mobile Sheet, state persistence, loading skeletons.

## When to Use

- SaaS dashboard with sidebar navigation
- Collapsible/minimizable sidebar (icon-only mode)
- Responsive layout with mobile sheet overlay

## Quick Start

```bash
npx shadcn@latest add sidebar tooltip avatar popover collapsible separator skeleton sheet
```

This generates `components/ui/sidebar.tsx` (~770 lines) with ALL sidebar primitives. Do NOT build a custom `<aside>`.

---

## Architecture

### How the Layout Works (Dual-Div Trick)

The `Sidebar` component renders **two divs** on desktop:

```
┌──────────────────────────────────────────────┐
│ SidebarProvider (flex container, min-h-svh)   │
│                                              │
│  ┌─ Sidebar outer div ──────────────────┐    │
│  │  [Spacer div]     ← reserves width   │    │
│  │   relative w-[--sidebar-width]        │    │
│  │   (pushes SidebarInset right)         │    │
│  │                                       │    │
│  │  [Fixed div]      ← actual sidebar   │    │
│  │   fixed inset-y-0 z-10               │    │
│  │   w-[--sidebar-width]                 │    │
│  │   (contains children)                 │    │
│  └───────────────────────────────────────┘    │
│                                              │
│  ┌─ SidebarInset (main) ────────────────┐    │
│  │  flex-1 overflow-y-auto h-dvh         │    │
│  └───────────────────────────────────────┘    │
└──────────────────────────────────────────────┘
```

Both divs transition width together: `transition-[width] duration-200 ease-linear`. The spacer ensures the main content never overlaps the sidebar.

### Width Constants (CSS Variables)

Set by `SidebarProvider` as inline CSS custom properties:

| State     | Variable               | Value           |
|-----------|------------------------|-----------------|
| Expanded  | `--sidebar-width`      | `16rem` (256px) |
| Collapsed | `--sidebar-width-icon` | `3rem` (48px)   |
| Mobile    | `--sidebar-width`      | `18rem` (288px) |

### State Context

```typescript
type SidebarContextProps = {
  state: "expanded" | "collapsed"  // derived from open
  open: boolean                     // true = expanded
  setOpen: (open: boolean) => void
  openMobile: boolean               // separate mobile Sheet state
  setOpenMobile: (open: boolean) => void
  isMobile: boolean                 // < 768px
  toggleSidebar: () => void         // smart: routes to mobile or desktop
}
```

Access anywhere via `useSidebar()`. Never pass `collapsed` as prop.

### Data Attribute Styling (No Prop Drilling)

The outer `Sidebar` div sets data attributes that children react to via Tailwind group selectors:

```html
<div data-state="collapsed" data-collapsible="icon" data-variant="sidebar" data-side="left">
```

Key selectors and what they do:

```css
/* Force menu buttons to 32×32px centered squares when collapsed */
group-data-[collapsible=icon]:!size-8
group-data-[collapsible=icon]:!p-2

/* Hide text labels smoothly (negative margin pulls up, opacity fades) */
group-data-[collapsible=icon]:-mt-8
group-data-[collapsible=icon]:opacity-0

/* Hard-hide sub-menus, group actions, badges when collapsed */
group-data-[collapsible=icon]:hidden

/* Prevent horizontal scrollbar in 48px-wide collapsed column */
group-data-[collapsible=icon]:overflow-hidden
```

### Peer Coordination (Sidebar ↔ Main Content)

The sidebar outer div has `group peer`. `SidebarInset` uses peer selectors:

```tsx
// SidebarInset reacts to sidebar state for inset variant
"md:peer-data-[variant=inset]:m-2"
"md:peer-data-[state=collapsed]:peer-data-[variant=inset]:ml-2"
```

---

## The Centering Magic (How Icons Align Perfectly)

This is the most important detail. `SidebarMenuButton` uses CVA variants:

```typescript
const sidebarMenuButtonVariants = cva(
  // Base: flex row, gap-2, overflow-hidden, rounded-md, p-2
  "peer/menu-button flex w-full items-center gap-2 overflow-hidden rounded-md p-2 text-left text-sm " +
  // Auto-truncate the last span (label text)
  "[&>span:last-child]:truncate " +
  // Icons: always 16×16, never shrink
  "[&>svg]:size-4 [&>svg]:shrink-0 " +
  // COLLAPSED: force to 32×32 square with centered icon
  "group-data-[collapsible=icon]:!size-8 group-data-[collapsible=icon]:!p-2 " +
  // Transitions on width, height, padding (not all)
  "transition-[width,height,padding] " +
  // Active state
  "data-[active=true]:bg-sidebar-accent data-[active=true]:font-medium",
  {
    variants: {
      size: {
        default: "h-8 text-sm",                                    // 32px — nav items
        sm: "h-7 text-xs",                                         // 28px — compact
        lg: "h-12 text-sm group-data-[collapsible=icon]:!p-0",    // 48px — header (workspace switcher)
      },
    },
  }
)
```

**Why everything centers when collapsed:**
- Container is `3rem` (48px) wide with `p-2` (8px each side) = 32px usable
- Button forced to `!size-8` (32px) with `!p-2` (8px padding) = icon at center
- `overflow-hidden` clips any text that hasn't faded yet
- Icons have `[&>svg]:size-4 [&>svg]:shrink-0` = always 16×16, never compressed

**Size `"lg"` for header:**
- `h-12` (48px) gives room for two-line text (name + subtitle)
- `group-data-[collapsible=icon]:!p-0` removes padding so the h-7 w-7 avatar fits cleanly

### Built-in Tooltip System

`SidebarMenuButton` has a `tooltip` prop. NO manual wrapping needed:

```tsx
<SidebarMenuButton asChild isActive={isActive} tooltip="Home">
  <Link href="/"><Home className="h-4 w-4" /><span>Home</span></Link>
</SidebarMenuButton>
```

Internally, it wraps the button in `<Tooltip>` with auto-visibility:

```tsx
<TooltipContent
  side="right"
  align="center"
  hidden={state !== "collapsed" || isMobile}  // only show when collapsed + desktop
/>
```

`TooltipProvider delayDuration={0}` is set at the `SidebarProvider` level = instant tooltips.

### The `asChild` / Slot Pattern

Every component supports `asChild` (Radix Slot). When true, it merges its props into the child element instead of rendering a wrapper. This is why this works:

```tsx
// SidebarMenuButton renders as <Link> not <button><Link>
<SidebarMenuButton asChild tooltip="Home">
  <Link href="/">...</Link>
</SidebarMenuButton>
```

---

## The Expand/Collapse Pattern

### How It Works

When collapsed, hovering **anywhere on the sidebar** swaps the header avatar for an expand button:

```
Collapsed (idle):    [OrgAvatar]                    ← icon only, 7×7
Collapsed (hover):   [ExpandBtn]                    ← replaces avatar on sidebar hover
Expanded:            [OrgSwitcher ——— CollapseBtn]  ← full row
```

### Implementation

```tsx
<Sidebar collapsible="icon" className="border-r group/sidebar">
  <SidebarHeader className="pb-0">
    <SidebarMenu>
      <SidebarMenuItem className="flex items-center gap-1">
        <ExpandButton />           {/* hidden → shows on sidebar hover */}
        <OrgSwitcher />            {/* avatar hides on sidebar hover when collapsed */}
        <CollapseToggle />         {/* early-returns null when collapsed */}
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarHeader>
```

### ExpandButton

```tsx
function ExpandButton() {
  const { toggleSidebar, state } = useSidebar()
  if (state !== 'collapsed') return null

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          onClick={(e) => { e.stopPropagation(); toggleSidebar() }}
          className="hidden group-hover/sidebar:flex items-center justify-center h-7 w-7 rounded-md bg-accent text-foreground cursor-pointer hover:bg-accent/80 transition-colors shrink-0"
        >
          <PanelLeftOpen className="h-4 w-4" />
        </button>
      </TooltipTrigger>
      <TooltipContent side="right" align="center">Expand sidebar</TooltipContent>
    </Tooltip>
  )
}
```

Key classes:
- `hidden group-hover/sidebar:flex` — invisible by default, appears when sidebar hovered
- `h-7 w-7` — matches the org avatar exactly (zero layout shift)
- `e.stopPropagation()` — prevents the click from reaching the PopoverTrigger behind it

### CollapseToggle

```tsx
function CollapseToggle() {
  const { toggleSidebar, state } = useSidebar()
  if (state !== 'expanded') return null

  return (
    <Tooltip>
      <TooltipTrigger asChild>
        <button
          onClick={toggleSidebar}
          className="h-7 w-7 flex items-center justify-center rounded-md text-muted-foreground/50 hover:text-muted-foreground hover:bg-accent transition-colors cursor-pointer shrink-0"
        >
          <PanelLeftOpen className="h-4 w-4 rotate-180" />
        </button>
      </TooltipTrigger>
      <TooltipContent side="right">Close sidebar</TooltipContent>
    </Tooltip>
  )
}
```

Key: same `PanelLeftOpen` icon with `rotate-180` — not a separate `PanelLeftClose` icon.

### Org/Team Avatar (Hides on Hover When Collapsed)

```tsx
<SidebarMenuButton size="lg" className={cn("w-full cursor-pointer", collapsed && "justify-center")}>
  <div className={cn(
    "flex items-center justify-center h-7 w-7 rounded-md bg-primary text-primary-foreground text-xs font-bold shrink-0",
    collapsed && "group-hover/sidebar:hidden"  // ← KEY: hides when sidebar hovered
  )}>
    {initial}
  </div>
  {!collapsed && (
    <>
      <div className="flex-1 min-w-0 text-left">
        <p className="text-sm font-semibold truncate leading-tight">{name}</p>
        <p className="text-[10px] text-muted-foreground leading-tight">{subtitle}</p>
      </div>
      <ChevronDown className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
    </>
  )}
</SidebarMenuButton>
```

Note: `leading-tight` on both lines keeps them compact within the `h-12` (size="lg") button.

---

## Navigation Items

### Standard Nav Item

```tsx
function NavItem({ href, label, icon: Icon, badge, onClick }: {
  href?: string; label: string; icon: ComponentType<{ className?: string }>
  badge?: string; onClick?: () => void
}) {
  const pathname = usePathname()
  const isActive = href ? pathname === href : false

  const content = (
    <>
      <Icon className="h-4 w-4" />
      <span>{label}</span>
      {badge && (
        <span className="ml-auto flex items-center gap-0.5 text-[10px] text-muted-foreground/50">
          <kbd className="inline-flex h-5 items-center rounded border border-border/50 bg-muted/50 px-1 font-mono text-[10px]">⌘</kbd>
          <kbd className="inline-flex h-5 items-center rounded border border-border/50 bg-muted/50 px-1 font-mono text-[10px]">{badge}</kbd>
        </span>
      )}
    </>
  )

  if (onClick) {
    return (
      <SidebarMenuItem>
        <SidebarMenuButton isActive={isActive} tooltip={label} onClick={onClick} className="cursor-pointer">
          {content}
        </SidebarMenuButton>
      </SidebarMenuItem>
    )
  }

  return (
    <SidebarMenuItem>
      <SidebarMenuButton asChild isActive={isActive} tooltip={label}>
        <Link href={href!}>{content}</Link>
      </SidebarMenuButton>
    </SidebarMenuItem>
  )
}
```

When collapsed: icon centers at 32×32, span truncates to invisible, badge hides (overflow-hidden clips it), tooltip appears on hover.

### Collapsible Nested Section

```tsx
function CollapsibleSection({ label, icon: Icon, items }: { ... }) {
  const [open, setOpen] = useState(true)

  return (
    <Collapsible open={open} onOpenChange={setOpen}>
      <SidebarMenuItem>
        <CollapsibleTrigger asChild>
          <SidebarMenuButton className="cursor-pointer" tooltip={label}>
            <Icon className="h-4 w-4" />
            <span>{label}</span>
            <ChevronRight className={cn(
              "ml-auto h-3.5 w-3.5 shrink-0 text-muted-foreground/50 transition-transform duration-200",
              open && "rotate-90"
            )} />
          </SidebarMenuButton>
        </CollapsibleTrigger>
        <CollapsibleContent>
          <SidebarMenuSub>
            {items.map((item) => (
              <SidebarMenuSubItem key={item.id}>
                <SidebarMenuSubButton asChild>
                  <Link href={item.href}><span className="truncate">{item.name}</span></Link>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            ))}
          </SidebarMenuSub>
        </CollapsibleContent>
      </SidebarMenuItem>
    </Collapsible>
  )
}
```

`SidebarMenuSub` auto-hides when collapsed: `group-data-[collapsible=icon]:hidden`. The parent button still shows as an icon-only tooltip item.

### Group Labels (Auto-Hide Trick)

```tsx
<SidebarGroup className="py-1">
  <SidebarGroupLabel className="text-[10px] uppercase tracking-wider text-muted-foreground/60 font-medium">
    Projects
  </SidebarGroupLabel>
  <SidebarMenu>{/* items */}</SidebarMenu>
</SidebarGroup>
```

Built-in auto-hide uses `-mt-8 opacity-0` (NOT `display:none`). This keeps the label in DOM so items below shift up with a smooth `transition-[margin,opacity] duration-200 ease-linear` instead of a hard jump.

### Inline Action Button (Show on Hover)

```tsx
<SidebarMenuItem>
  <SidebarMenuButton asChild tooltip="Projects">
    <Link href="/projects"><FolderOpen className="h-4 w-4" /><span>Projects</span></Link>
  </SidebarMenuButton>
  <SidebarMenuAction showOnHover>
    <Plus className="h-4 w-4" />
  </SidebarMenuAction>
</SidebarMenuItem>
```

The action is positioned `absolute right-1` and uses `md:opacity-0 group-hover/menu-item:opacity-100` to appear only on hover. Auto-hidden when collapsed.

---

## Footer Widgets (Collapsed ↔ Expanded Pattern)

Footer items must gracefully transform between full content (expanded) and centered icon + tooltip (collapsed).

### Pattern: Early Return for Collapsed

```tsx
function UsageWidget() {
  const { state } = useSidebar()
  const collapsed = state === 'collapsed'

  // Collapsed: centered icon with tooltip
  if (collapsed) {
    return (
      <Tooltip>
        <TooltipTrigger asChild>
          <button className="flex items-center justify-center mx-auto w-8 h-8 cursor-pointer hover:bg-accent/50 rounded-md transition-colors">
            <Gauge className="h-4 w-4 text-muted-foreground" />
          </button>
        </TooltipTrigger>
        <TooltipContent side="right">75% credits used</TooltipContent>
      </Tooltip>
    )
  }

  // Expanded: full widget
  return (
    <div className="mx-2 px-3 py-2 rounded-md hover:bg-accent/50 transition-colors cursor-pointer space-y-1.5">
      <div className="flex items-center justify-between">
        <span className="text-[11px] text-muted-foreground">250 credits left</span>
        <span className="text-[10px] text-muted-foreground/60">75%</span>
      </div>
      <div className="h-1.5 rounded-full bg-muted overflow-hidden">
        <div className="h-full rounded-full bg-primary transition-all duration-300" style={{ width: '75%' }} />
      </div>
    </div>
  )
}
```

### User Row (Using SidebarMenuButton)

```tsx
function UserRow() {
  const { state } = useSidebar()
  const collapsed = state === 'collapsed'

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <SidebarMenuButton asChild tooltip={userName} className={cn(collapsed && "flex items-center justify-center")}>
          <Link href="/settings" className="flex items-center gap-2 cursor-pointer">
            <Avatar className="h-6 w-6 shrink-0">
              <AvatarImage src={photo} />
              <AvatarFallback className="text-[10px] bg-muted">{initial}</AvatarFallback>
            </Avatar>
            {!collapsed && (
              <>
                <span className="truncate text-sm font-medium">{userName}</span>
                <Settings className="ml-auto h-3.5 w-3.5 shrink-0 text-muted-foreground/50 hover:text-muted-foreground transition-colors" />
              </>
            )}
          </Link>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
```

Uses `SidebarMenuButton tooltip=` so collapsed state gets auto-tooltip. Avatar at `h-6 w-6` fits within the `!size-8` collapsed button.

---

## Org/Team Switcher (Popover in Header)

**Critical: DO NOT wrap PopoverTrigger in Tooltip** — breaks click handling.

```tsx
function OrgSwitcher() {
  const { state } = useSidebar()
  const [open, setOpen] = useState(false)
  const collapsed = state === 'collapsed'

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <SidebarMenuButton size="lg" className={cn("w-full cursor-pointer", collapsed && "justify-center")}>
          <div className={cn(
            "flex items-center justify-center h-7 w-7 rounded-md bg-primary text-primary-foreground text-xs font-bold shrink-0",
            collapsed && "group-hover/sidebar:hidden"
          )}>
            {initial}
          </div>
          {!collapsed && (
            <>
              <div className="flex-1 min-w-0 text-left">
                <p className="text-sm font-semibold truncate leading-tight">{orgName}</p>
                <p className="text-[10px] text-muted-foreground leading-tight">{planLabel}</p>
              </div>
              <ChevronDown className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
            </>
          )}
        </SidebarMenuButton>
      </PopoverTrigger>
      <PopoverContent
        align="start"
        side={collapsed ? 'right' : 'bottom'}
        sideOffset={4}
        className="w-60 p-1"
      >
        {/* Org list items */}
        {orgs.map((org) => (
          <button
            key={org.id}
            onClick={() => switchOrg(org.id)}
            className="flex items-center gap-2 rounded-md px-2 py-1.5 text-left hover:bg-accent transition-colors w-full cursor-pointer text-sm"
          >
            <div className="flex items-center justify-center h-6 w-6 rounded bg-primary/10 text-primary text-[10px] font-bold shrink-0">
              {org.name.charAt(0)}
            </div>
            <span className="flex-1 truncate font-medium">{org.name}</span>
            {org.id === active.id && <Check className="h-3.5 w-3.5 shrink-0 text-primary" />}
          </button>
        ))}
        <SidebarSeparator className="my-1" />
        <Link href="/settings" className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-foreground transition-colors cursor-pointer">
          <Settings className="h-3.5 w-3.5" /> Settings
        </Link>
        <button className="flex items-center gap-2 rounded-md px-2 py-1.5 text-sm text-muted-foreground hover:bg-accent hover:text-foreground transition-colors cursor-pointer w-full">
          <Plus className="h-3.5 w-3.5" /> New workspace
        </button>
      </PopoverContent>
    </Popover>
  )
}
```

Popover `side` flips to `"right"` when collapsed so it doesn't overlap the narrow sidebar.

---

## SidebarRail (Edge Hover Toggle)

```tsx
<SidebarRail />
```

An invisible `w-4` hit area positioned at `-right-4` of the sidebar. On hover, it shows a `2px` vertical line (`hover:after:bg-sidebar-border`). Clicking toggles the sidebar. Users discover this naturally — it's a secondary toggle alongside the header buttons.

---

## Mobile Behavior

**Automatic.** The `Sidebar` component checks `useIsMobile()` (768px breakpoint) and renders:
- Desktop: `hidden md:block` with collapse animation
- Mobile: Radix `Sheet` overlay (slide-in from left, with backdrop)

`toggleSidebar()` routes to the correct behavior:

```tsx
const toggleSidebar = () => isMobile ? setOpenMobile(o => !o) : setOpen(o => !o)
```

Mobile trigger in your page header:

```tsx
<SidebarTrigger className="md:hidden" />  // PanelLeft icon, h-7 w-7
```

The `useIsMobile` hook:

```tsx
const MOBILE_BREAKPOINT = 768
export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)
  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    const onChange = () => setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    return () => mql.removeEventListener("change", onChange)
  }, [])
  return !!isMobile
}
```

---

## Keyboard Shortcut

Built into `SidebarProvider`: **⌘B** (Mac) / **Ctrl+B** (Windows). No configuration needed. Calls `toggleSidebar()`.

---

## State Persistence

### localStorage (instant on mount)

```tsx
const SIDEBAR_KEY = 'sidebar_state'

const [open, setOpen] = useState(() => {
  if (typeof window === 'undefined') return true
  const stored = localStorage.getItem(SIDEBAR_KEY)
  return stored === null ? true : stored === 'true'
})

const handleOpenChange = (value: boolean) => {
  setOpen(value)
  localStorage.setItem(SIDEBAR_KEY, String(value))
}

<SidebarProvider open={open} onOpenChange={handleOpenChange}>
```

### Cookie (SSR, set by SidebarProvider internally)

```tsx
document.cookie = `sidebar_state=${openState}; path=/; max-age=${60 * 60 * 24 * 7}`
```

---

## Loading Skeleton (Zero Layout Shift)

Match sidebar width and element sizes:

```tsx
function SidebarSkeleton() {
  return (
    <div className="flex min-h-screen">
      <div className="w-64 shrink-0 border-r bg-sidebar p-3 space-y-4">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-md bg-muted animate-pulse" />
          <div className="flex-1 space-y-1.5">
            <div className="h-3 w-28 rounded bg-muted animate-pulse" />
            <div className="h-2 w-16 rounded bg-muted animate-pulse" />
          </div>
        </div>
        <div className="space-y-1 pt-2">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-8 rounded-md bg-muted/50 animate-pulse" />
          ))}
        </div>
      </div>
      <div className="flex-1 flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
      </div>
    </div>
  )
}
```

---

## Full Assembly

### Layout (wraps your app)

```tsx
'use client'
import { useState } from 'react'
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar'
import { AppSidebar } from './app-sidebar'

const SIDEBAR_KEY = 'sidebar_state'

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(() => {
    if (typeof window === 'undefined') return true
    const stored = localStorage.getItem(SIDEBAR_KEY)
    return stored === null ? true : stored === 'true'
  })

  const handleOpenChange = (value: boolean) => {
    setOpen(value)
    localStorage.setItem(SIDEBAR_KEY, String(value))
  }

  return (
    <SidebarProvider open={open} onOpenChange={handleOpenChange}>
      <AppSidebar />
      <SidebarInset className="overflow-y-auto h-dvh">
        {children}
      </SidebarInset>
    </SidebarProvider>
  )
}
```

Note: `h-dvh` (dynamic viewport height) is better than `h-screen` on mobile Safari.

### Sidebar (all sections)

```tsx
export function AppSidebar() {
  return (
    <Sidebar collapsible="icon" className="border-r group/sidebar">
      <SidebarHeader className="pb-0">
        <SidebarMenu>
          <SidebarMenuItem className="flex items-center gap-1">
            <ExpandButton />
            <OrgSwitcher />
            <CollapseToggle />
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup className="py-1">
          <SidebarMenu>
            <NavItem href="/dashboard" label="Home" icon={Home} />
            <NavItem label="Search" icon={Search} badge="K" onClick={openSearch} />
          </SidebarMenu>
        </SidebarGroup>

        <SidebarGroup className="py-1">
          <SidebarGroupLabel>Projects</SidebarGroupLabel>
          <SidebarMenu>
            <CollapsibleSection label="Recent" icon={Clock} items={recentItems} />
            <NavItem href="/projects" label="All projects" icon={FolderOpen} />
            <NavItem href="/starred" label="Starred" icon={Star} />
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="gap-0.5 pb-2">
        <SidebarSeparator />
        <UsageWidget />
        <UserRow />
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  )
}
```

---

## CSS Variables (globals.css)

```css
:root {
  --sidebar: 0 0% 98%;
  --sidebar-foreground: 240 5.3% 26.1%;
  --sidebar-border: 220 13% 91%;
  --sidebar-accent: 220 14.3% 95.9%;
  --sidebar-accent-foreground: 220.9 39.3% 11%;
  --sidebar-ring: 217.2 91.2% 59.8%;
}
.dark {
  --sidebar: 240 5.9% 10%;
  --sidebar-foreground: 240 4.8% 95.9%;
  --sidebar-border: 240 3.7% 15.9%;
  --sidebar-accent: 240 3.7% 15.9%;
  --sidebar-accent-foreground: 240 4.8% 95.9%;
  --sidebar-ring: 217.2 91.2% 59.8%;
}
```

Tailwind config (`theme.extend.colors`):

```ts
sidebar: {
  DEFAULT: "hsl(var(--sidebar))",
  foreground: "hsl(var(--sidebar-foreground))",
  border: "hsl(var(--sidebar-border))",
  accent: "hsl(var(--sidebar-accent))",
  "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
  ring: "hsl(var(--sidebar-ring))",
},
```

---

## Critical Rules

### DO

- `collapsible="icon"` on `<Sidebar>` for icon-only collapse
- `group/sidebar` class on `<Sidebar>` for hover detection
- `useSidebar()` to read state — never prop-drill `collapsed`
- `SidebarMenuButton tooltip={label}` for auto-tooltips
- `group-data-[collapsible=icon]:` selectors for collapsed styling
- Match expand button and avatar sizes exactly (`h-7 w-7`)
- `e.stopPropagation()` on expand button (prevents popover trigger)
- `PanelLeftOpen` with `rotate-180` for collapse (one icon, not two)
- `leading-tight` for multi-line text in header button
- `shrink-0` on all icons and trailing elements
- `truncate` on all text that could overflow
- `min-w-0` on flex children that contain truncated text
- `cursor-pointer` on all clickable elements

### DO NOT

- Nest `Tooltip` inside `PopoverTrigger` or `DropdownMenuTrigger`
- Use `transition-all` — use specific properties (`transition-[width]`)
- Build a custom `<aside>` — use the shadcn/ui Sidebar system
- Use `w-16` (64px) for collapsed — it's `3rem` (48px) via CSS var
- Use `display:none` for group labels — use the `-mt-8 opacity-0` trick
- Use `h-screen` — use `h-dvh` for mobile Safari compatibility
- Add `TooltipProvider` yourself — it's already in `SidebarProvider`
- Put `Tooltip`-wrapped elements inside a `Popover`/`Dialog` content — Radix tooltips trigger on **focus**, not just hover. When a popover opens, focus moves into its content and auto-fires the tooltip on the first focusable element. See "Tooltip-on-Focus Gotcha" below.

---

## Tooltip-on-Focus Gotcha (Radix)

**Problem:** Radix `<Tooltip>` triggers on both hover AND focus. When you place tooltip-wrapped buttons inside a `<PopoverContent>`, opening the popover moves focus into the content, which immediately triggers the tooltip on the first focusable element — even without hovering.

**This affects any component with tooltips rendered inside:**
- `PopoverContent`
- `DialogContent`
- `SheetContent`
- Any container that receives focus on open

**Solution:** Add a `showTooltips` prop to components that contain tooltips, and disable them when used inside focus-trapping containers:

```tsx
interface ThemeToggleProps {
  showTooltips?: boolean  // default true
}

function ThemeToggle({ showTooltips = true }: ThemeToggleProps) {
  const btn = <button aria-label={label}>...</button>

  // Skip tooltip wrapper when inside popover/dialog
  if (!showTooltips) return btn

  return (
    <Tooltip>
      <TooltipTrigger asChild>{btn}</TooltipTrigger>
      <TooltipContent>{label}</TooltipContent>
    </Tooltip>
  )
}

// Usage inside popover — tooltips disabled (label "Theme" provides context)
<PopoverContent>
  <span>Theme</span>
  <ThemeToggle showTooltips={false} />
</PopoverContent>

// Usage in header — tooltips enabled (icon-only, needs tooltip)
<ThemeToggle showTooltips={true} />
```

**Why not just increase `delayDuration`?** The delay only affects hover. Focus-triggered tooltips ignore `delayDuration` in Radix and fire immediately regardless of the delay value.

**Rule of thumb:** If a tooltip-wrapped element appears inside a focus-trapping container, either disable tooltips or ensure adjacent text labels provide sufficient context.

---

## Checklist

- [ ] `npx shadcn@latest add sidebar tooltip avatar popover collapsible separator skeleton sheet`
- [ ] CSS variables in globals.css (light + dark) + Tailwind config
- [ ] `SidebarProvider` wraps app with `open`/`onOpenChange` + localStorage
- [ ] `Sidebar collapsible="icon" className="border-r group/sidebar"`
- [ ] `ExpandButton`: `hidden group-hover/sidebar:flex`, same size as avatar
- [ ] `CollapseToggle`: `PanelLeftOpen rotate-180`, conditional render
- [ ] Avatar: `group-hover/sidebar:hidden` when collapsed
- [ ] All nav items use `SidebarMenuButton tooltip={label}`
- [ ] Group labels use `SidebarGroupLabel` (auto-hides)
- [ ] Collapsible sections use `Collapsible` + `SidebarMenuSub`
- [ ] Footer widgets: collapsed=icon+tooltip, expanded=full content
- [ ] `SidebarRail` for edge hover toggle
- [ ] `SidebarInset className="overflow-y-auto h-dvh"`
- [ ] Loading skeleton matches sidebar width (`w-64`)
- [ ] Mobile renders as Sheet (automatic)
- [ ] Keyboard shortcut: ⌘B / Ctrl+B (automatic)
