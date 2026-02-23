---
name: figma-storybook-workflow
description: "STRICT pixel-perfect Figma to Storybook workflow with ENFORCED extraction and iterative component implementation. MANDATORY: Extract exact design → Implement → Iterate until perfect → Move to next. NO shortcuts, NO assumptions, NO batch processing. Use when implementing Figma designs as Storybook components with 100% accuracy requirement."
---

# Figma to Storybook - STRICT Pixel-Perfect Workflow

## ⚠️ CRITICAL RULES (NEVER VIOLATE)

1. **ONE COMPONENT AT A TIME** - Finish completely before moving to next
2. **ALWAYS EXTRACT FRESH** - Never use cached/old Figma data
3. **ITERATE UNTIL PERFECT** - Don't move on until user confirms it's correct
4. **EXTRACT ONLY WHAT'S NEEDED** - Don't load entire page context, only current component
5. **NO ASSUMPTIONS** - If unclear, extract again or ask user

## Description
Strict workflow enforcing pixel-perfect-ui methodology with iterative refinement. Each component is extracted, implemented, and perfected before moving to the next.

## When to Use
- Implementing Figma designs as Storybook components
- Pixel-perfect accuracy required
- User wants quality over speed
- Multiple components need implementation

## 🔒 MANDATORY WORKFLOW (FOLLOW EXACTLY)

### Phase -1: 🚨 VISUAL VERIFICATION (ALWAYS FIRST)

**For EACH component, ALWAYS:**
1. `mcp0_get_screenshot(nodeId)` → SEE the design
2. **DESCRIBE what you SEE** - not what you assume
3. Check if similar component exists → REUSE with props
4. **NEVER assume from names** - verify visually

### Phase 0: Component Planning (QUICK - Don't Over-Analyze)

**Identify components to implement:**
1. List component names from Figma/user request
2. Quick check: does similar component exist?
3. Present simple list to user

**Present to user:**
```markdown
## Components to Implement

1. **ComponentName1** - [New/Reuse ExistingComponent]
2. **ComponentName2** - [New/Reuse ExistingComponent]
3. **ComponentName3** - [New/Reuse ExistingComponent]

**Approach**: Implement one at a time, iterate until perfect.
**Ready to start with Component 1?**
```

**Wait for user approval, then START with first component.**

---

## 🔄 PER-COMPONENT WORKFLOW (Repeat for Each)

### Step 1: EXTRACT (MANDATORY - Never Skip)

**For current component ONLY:**
```bash
# Visual reference
mcp0_get_screenshot --nodeId <component-node-id>

# Exact design extraction
mcp0_get_design_context --nodeId <component-node-id> --forceCode true
| Hero section | HeroSection | HeroSection | title, subtitle, image |
| Card grid | GridSection | GridSection | cards array |
| Two column | TwoColumnSection | TwoColumnSection | items array |

### New Components to Create:
| Component | Reason | Generic Name | Where |
|-----------|--------|--------------|-------|
| Special layout | No similar pattern exists | UniqueSection | organisms/ |
| Custom card | Different structure needed | SpecialCard | molecules/ |

### Inline Components to Extract:
| Current Location | Component Type | New Generic Name |
|-----------------|----------------|------------------|
| page.tsx:45-89 | Card component | Card |
| page.tsx:120-150 | List item | ListItem |

### Components to Generalize:
| Current Components | Pattern | New Generic Component |
|-------------------|---------|----------------------|
| AboutSection, TeamSection | Same layout | TwoColumnSection |
| ProductCard, ServiceCard | Same structure | Card |

### Summary:
- ✅ Will REUSE: 3 existing components  
- 🔨 Will CREATE: 2 new components
- 📦 Will EXTRACT: 2 inline components
- 🔄 Will GENERALIZE: 2 pairs into generic components

**Questions for User:**
1. Do you agree with this component strategy?
2. Should any of these be handled differently?
3. Any specific naming preferences?
```

**⛔ DO NOT PROCEED WITHOUT USER SAYING: "Yes, proceed" or similar approval**

### Phase 0.5: Decide Scope (CRITICAL - ASK FIRST)

**Before ANY implementation, ask the user:**
```
Are you building:
1. Only Storybook components (no page assembly)? 
2. Full page with components?
```

- If **Components Only** → Skip page.tsx creation, focus ONLY on components and Storybook stories
- If **Full Page** → Create both components and page assembly

# DON'T load entire page context
# DON'T extract multiple components at once
```

**CRITICAL**: Extract shows EXACT:
- Dimensions (width, height, padding, margin, gap)
- Colors (hex codes, gradients)
- Typography (font-family, size, line-height, weight)
- Images (URLs to download)
- Spacing (exact pixel values)

### Step 2: DOWNLOAD ASSETS (If Any)

**From extraction output, download ALL images:**
```bash
# Extract image URLs from mcp0_get_design_context output
# Example: const img = "http://localhost:3845/assets/[hash].png"

curl -o /Users/mdascal/Projects/fuse/landing/public/assets/component-image-1.png "http://localhost:3845/assets/[hash].png"
curl -o /Users/mdascal/Projects/fuse/landing/public/assets/component-image-2.png "http://localhost:3845/assets/[hash].png"

# Verify file sizes (should be >10KB for real images)
ls -lh /Users/mdascal/Projects/fuse/landing/public/assets/component-*
```

**If file size <10KB → Wrong image, re-download correct one**

### Step 3: IMPLEMENT EXACTLY

**Use EXACT values from extraction:**
- Copy dimensions: `h-[696px]`, `w-[149.68%]`, `left-[-1.64%]`
- Copy spacing: `gap-[24px]`, `p-[96px]`, `px-[40px]`
- Copy colors: `#084EDD`, `rgba(255,255,255,0.6)`
- Copy typography: `text-[56px]`, `leading-[64px]`

**NO rounding, NO "close enough", NO assumptions**

**🚨 CRITICAL: FUNCTIONAL COMPONENTS (Not Just Visual)**

**ALWAYS implement as a PROFESSIONAL SOFTWARE ENGINEER:**

1. **Interactive Elements MUST Work:**
   - ✅ Search bars → filter data in real-time
   - ✅ Dropdowns → show/hide options, update selection
   - ✅ Pagination → change pages, calculate page numbers
   - ✅ Tabs → switch content, highlight active tab
   - ✅ Buttons → trigger actions, show hover/active states
   - ✅ Forms → validate, submit, show errors

2. **State Management:**
   - Use `useState` for local state
   - Use `useMemo` for expensive calculations
   - Use `useCallback` for event handlers (if needed)
   - Reset dependent state (e.g., page 1 when filtering)

3. **Data Filtering Logic:**
   ```tsx
   // Example: Combined filtering
   const filteredData = useMemo(() => {
     return allData.filter(item => {
       const matchesSearch = searchQuery === '' || 
         item.title.toLowerCase().includes(searchQuery.toLowerCase())
       const matchesCategory = selectedCategory === 'All' || 
         item.category === selectedCategory
       return matchesSearch && matchesCategory
     })
   }, [allData, searchQuery, selectedCategory])
   ```

4. **Pagination Logic:**
   ```tsx
   const totalPages = Math.ceil(filteredData.length / itemsPerPage)
   const paginatedData = filteredData.slice(
     (currentPage - 1) * itemsPerPage, 
     currentPage * itemsPerPage
   )
   ```

5. **Props for Parent Control:**
   - Add callback props: `onTabChange`, `onSearch`, `onFilterChange`
   - Add controlled props: `activeTab`, `searchQuery`, `selectedFilters`
   - Allow both controlled and uncontrolled usage

6. **Empty States:**
   - Show "No results found" when filters return empty
   - Provide helpful messages
   - Don't show pagination when no results

7. **Icons:**
   - Use inline SVG for simple icons (search, arrows, chevrons)
   - Download complex icons from Figma
   - Ensure proper sizing and colors

**❌ FORBIDDEN - Non-Functional Components:**
- Search that doesn't filter
- Dropdowns that don't open
- Pagination that doesn't change pages
- Tabs that are just decorative
- Buttons that do nothing

**Create component + story:**
1. Component file: `src/components/organisms/ComponentName.tsx`
2. Story file: `src/components/organisms/ComponentName.stories.tsx`
3. Use extracted values EXACTLY
4. **Make it FULLY FUNCTIONAL like production software**

### Step 4: ITERATE UNTIL PERFECT

**Show implementation to user:**
```markdown
## ComponentName - First Implementation

Implemented based on Figma extraction:
- ✅ Dimensions: [list key dimensions]
- ✅ Images: [list images used]
- ✅ Spacing: [list key spacing]
- ✅ Colors: [list key colors]

**Please review and let me know if anything needs adjustment.**
```

**User feedback loop:**
- User points out issues
- Re-extract if needed (don't assume fix)
- Implement corrections EXACTLY
- Show updated implementation
- Repeat until user says "perfect" or "move to next"

**ONLY when user confirms → Move to next component**

### Step 5: RESPONSIVE (After User Approves Desktop)

**Add mobile/tablet breakpoints:**
```tsx
// Mobile: 375px
className="px-6 py-12 lg:px-24 lg:py-24"

// Tablet: 768px  
className="flex-col md:flex-row"

// Desktop: 1440px (already implemented)
```

**Test: No horizontal scroll on any viewport**

---

## ✅ COMPLETION CRITERIA (Per Component)

**Don't move to next component until:**
- [ ] User confirms desktop layout is pixel-perfect
- [ ] User confirms spacing/dimensions are correct
- [ ] User confirms images are correct
- [ ] Responsive breakpoints added
- [ ] User says "move to next" or "perfect"

---

## 🚫 FORBIDDEN ACTIONS

1. ❌ **Batch extracting** all components at once
2. ❌ **Implementing from memory** or old extraction
3. ❌ **Moving to next component** before user approval
4. ❌ **Rounding dimensions** (use exact: `h-[696px]` not `h-[700px]`)
5. ❌ **Assuming image paths** (download from extraction)
6. ❌ **Loading full page context** (extract only current component)
7. ❌ **Skipping iteration** (always show to user, get feedback)

---

## 📝 WORKFLOW SUMMARY

```
For Component 1:
  1. Extract (mcp0_get_design_context)
  2. Download assets
  3. Implement EXACTLY
  4. Show to user
  5. User feedback → Iterate
  6. User confirms → Add responsive
  7. User says "perfect" → DONE

For Component 2:
  1. Extract (fresh, don't reuse Component 1 data)
  2. Download assets
  3. Implement EXACTLY
  ... repeat ...

For Component N:
  ... same process ...
```

**Key: ONE at a time, ITERATE until perfect, THEN move on**

## 🎯 SUCCESS METRICS

**Per component:**
- Zero assumptions made
- All dimensions from extraction used exactly
- All images downloaded and verified
- User confirms pixel-perfect match
- Responsive on all viewports

**Overall:**
- Each component perfect before moving to next
- No batch processing
- No shortcuts taken
- User satisfaction 100%

---

## ⚡ EFFICIENCY NOTES

**This workflow is SLOWER but CORRECT:**
- Takes more time per component
- Requires more user interaction
- Uses more tokens (multiple extractions)
- **BUT**: Zero rework, perfect first time (after iterations)

**User explicitly wants:**
- Quality over speed
- Multiple extractions if needed
- Iterative refinement
- Pixel-perfect results

**Don't try to optimize or take shortcuts!**

---

## 📋 OLD SECTIONS (Kept for Reference)

### Asset Validation (If Needed)

**Before creating ANY component:**

1. **Check what images exist:**
   ```bash
   list_dir("/public/assets")
   find_by_name("*.png", "/public/assets")
   find_by_name("*.svg", "/public/assets") 
   ```

2. **Map Figma assets to existing files:**
   ```markdown
   ## Asset Mapping
   ✅ Figma "hero.png" → /assets/hero.png (exists)
   ✅ Figma "logo" → /assets/logo-text.svg (exists)  
   ❌ Figma "team.png" → MISSING → use /assets/featured-team.png
   ⬇️ Figma "icon" → download from localhost:3845
   ```

3. **Download missing Figma assets:**
   ```bash
   # From mcp0_get_design_context output
   curl "http://localhost:3845/assets/[hash].png" -o /public/assets/[name].png
   ```

4. **NEVER reference non-existent images in code!**

### Phase 1.6: Port Conflict Detection (MANDATORY BEFORE STARTING SERVERS)

**Before starting dev server or Storybook:**

1. **Check if ports are already in use:**
   ```bash
   # Check if dev server is running (port 3001)
   lsof -ti:3001
   
   # Check if Storybook is running (port 6010)
   lsof -ti:6010
   ```

2. **Decision logic:**
   - If port is **FREE** → Start the server normally
   - If port is **IN USE** → Check if it's the correct service:
     ```bash
     # Test if it's the dev server
     curl -s http://localhost:3001 | grep -q "<title>" && echo "Dev server running"
     
     # Test if it's Storybook
     curl -s http://localhost:6010 | grep -q "Storybook" && echo "Storybook running"
     ```
   - If **correct service running** → Use existing server, don't start new one
   - If **wrong service or broken** → Kill and restart:
     ```bash
     # Kill process on port
     kill $(lsof -ti:3001)
     # or
     kill $(lsof -ti:6010)
     
     # Wait a moment
     sleep 2
     
     # Start the correct service
     npm run dev  # or npm run storybook
     ```

3. **Never start duplicate servers on different ports!**

2. **Use Figma MCP for Design Context**
   - Call `mcp0_get_design_context(nodeId)` to get design details
   - Call `mcp0_get_screenshot(nodeId)` to capture visual reference
   - Extract design specifications (colors, spacing, typography)

3. **Create TODO List**
   - Analyze design from Figma
   - Check existing implementation
   - Present plan to user
   - Wait for approval (if needed)
   - Create/refactor component
   - Add to Storybook
   - Verify pixel perfect with Playwright
   - Test responsive layouts

### Phase 2: Component Implementation with Immediate Testing

**After creating EACH component:**

1. **Create the component**
2. **Create story IMMEDIATELY**
3. **Test in Storybook RIGHT AWAY:**
   ```bash
   # Check for TypeScript errors
   npx tsc --noEmit | grep ComponentName
   
   # Verify story loads
   curl http://localhost:6010/index.json | grep -i "componentname"
   ```

4. **Fix issues BEFORE moving to next component**

### Phase 2.5: Storybook Story Creation

**Delegate to storybook skill for actual code:**
```
skill("storybook") to create stories with:
- CSF 3.0 format
- Responsive viewport variants (Mobile, Tablet, Desktop)
- Interactive args for props
- Multiple variants showing different states
```

**Required stories for each component:**
1. Default story
2. MobileView (375px)
3. TabletView (768px)
4. DesktopView (1440px)
5. Custom variants (if needed)

### Phase 3: Visual Verification

**Use Playwright MCP (if available) or manual testing:**

1. **Navigate to story in Storybook**
2. **Capture screenshots for each viewport:**
   - Desktop (1440px)
   - Tablet (768px)
   - Mobile (375px)
3. **Compare with Figma design:**
   - Spacing matches
   - Typography matches
   - Colors match
   - Layout structure matches

**If Playwright unavailable:** Use manual browser testing in Storybook UI

### Phase 4: Refinement

**When fixing issues, delegate to appropriate skill:**

1. **For Next.js/React component fixes:**
   ```
   skill("next-best-practices") for:
   - Component structure
   - Image optimization
   - Responsive design
   - Performance issues
   ```

2. **For Storybook story fixes:**
   ```
   skill("storybook") for:
   - Story structure
   - Args/decorators
   - Viewport configuration
   - Story variants
   ```

3. **Common issues to fix:**
   - Adjust spacing to match Figma
   - Fix responsive breakpoints
   - Update typography variants
   - Ensure no hardcoded widths

### Phase 4.5: Verification Before Marking Complete (NEVER SKIP)

**DO NOT mark ANY task complete without:**

1. **Build verification:**
   ```bash
   # Check TypeScript
   npx tsc --noEmit
   
   # Build Storybook (if needed)
   npm run build-storybook
   ```

2. **Story verification in Storybook:**
   ```bash
   # List all component stories
   curl http://localhost:6010/index.json | jq '.entries | keys' | grep -i component
   
   # Verify story renders (should return > 0)
   curl "http://localhost:6010/iframe.html?id=organisms-component--default" | grep -c "ComponentName"
   ```

3. **Asset verification:**
   ```bash
   # Check for missing images (if page exists)
   curl http://localhost:3001/page | grep -o 'src="[^"]*"' | while read path; do
     [ ! -f "/public$path" ] && echo "Missing: $path"
   done
   ```

### Phase 5: Documentation

1. **Update TODO List**
   - Mark completed tasks
   - Add any new tasks discovered

2. **Summary Pattern**
   ```markdown
   ## ComponentName Implementation Complete ✅
   
   ### Verified Implementation
   - Desktop View: [description]
   - Tablet View: [description] 
   - Mobile View: [description]
   
   ### What Was Completed
   1. Created Storybook stories
   2. Fixed [specific issues]
   3. Responsive design verified
   
   ### Component Structure
   - Main component: [description]
   - Supporting components: [list]
   ```

## Key Principles

### Workflow Focus
This skill focuses on:
- Component planning and analysis
- Asset validation
- Port management
- Testing and verification
- Error recovery

### Code Writing Delegation
- **Next.js/React code** → Use `skill("next-best-practices")`
- **Storybook stories** → Use `skill("storybook")`

### Component Organization
- Organisms: Full sections (HeroSection, StatsSection, etc.)
- Molecules: Reusable components (StatCard, FeatureCard, etc.)
- Atoms: Basic elements (Button, Typography, etc.)

## Tools Required
- **Figma MCP**: For design context and screenshots
- **Playwright MCP**: For browser testing and verification
- **Storybook**: Running on port 6008 (or configured port)
- **File operations**: edit, write_to_file, read_file

## Success Criteria
- [ ] All components have Storybook stories
- [ ] Desktop, tablet, mobile views tested
- [ ] No hardcoded widths
- [ ] Matches Figma design specifications
- [ ] No horizontal scroll on any viewport
- [ ] All images loading correctly
- [ ] Responsive breakpoints working

## Example Workflow Sequence

1. **Analysis:** Check existing components, identify patterns
2. **Figma:** Get design context and screenshot
3. **Assets:** Validate images exist, download missing ones
4. **Ports:** Check if Storybook running, reuse or restart
5. **Component:** Delegate to `skill("next-best-practices")`
6. **Story:** Delegate to `skill("storybook")`
7. **Verify:** Check story loads in Storybook
8. **Visual:** Compare with Figma design
9. **Refine:** Fix issues using appropriate skills
10. **Complete:** Update TODO list

## Real Example: How Planning Matrix Prevents Mistakes

### Without Planning Matrix ❌
```
Developer sees Security page → starts creating:
- SecurityHero (duplicate of HeroSection)
- CaseStudyCard (duplicate of ImageCard) 
- SecurityRevenue (duplicate of GridSection)
Result: 3 unnecessary components created
```

### With Planning Matrix ✅
```
Phase 0 Analysis reveals:
- Hero section → REUSE HeroSection with props
- Case study cards → REUSE ImageCard 
- Revenue section → REUSE GridSection
Result: 0 unnecessary components, everything reused
```

## Common Mistakes to Avoid

### 🚨 0. CRITICAL: Making Assumptions Without Visual Verification ❌
**This is the #1 mistake that MUST be avoided!**

**Wrong:** 
- Seeing "ContactForm" in a name → assuming it has form inputs
- Reading text description → creating component without checking screenshot
- Assuming component structure from name alone

**Right:**
1. **ALWAYS call `mcp0_get_screenshot()` FIRST**
2. **LOOK at the actual visual** before writing ANY code
3. **Describe what you SEE** in the screenshot, not what you assume
4. **If user says "it's a variation"** → check existing component, add props, DON'T create new

**Verification Checklist Before ANY Component:**
```
□ Did I call mcp0_get_screenshot()?
□ Did I LOOK at the screenshot image?
□ Did I describe what I SEE (not assume)?
□ Does an existing component match this visual pattern?
□ If user said "variation" → am I reusing existing component?
```

**Example of this mistake:**
```
User: "Contact Form is a variation of BusinessSection"
❌ Wrong: Create new ContactFormSection with textarea
✅ Right: Look at screenshot → see it's just title+subtitle+button+images → reuse BusinessSection with props
```

### 1. Creating Duplicate Components ❌
**Wrong:** Creating `ProductHero`, `ServiceCard` when similar components exist
**Right:** Use existing `HeroSection`, `Card` components with different props

### 2. Not Generalizing Patterns ❌
**Wrong:** Keeping `TeamSection` and `AboutSection` as separate components when they share same layout
**Right:** Create generic `TwoColumnSection` or `GridSection`

### 3. Component Naming ❌
**Wrong:** Page-specific names like `HomeFeatures`, `AboutCard`, `ContactHero`
**Right:** Generic names like `FeatureGrid`, `Card`, `HeroSection`

## Generalization Principles

### When to Create Generic Components
1. **Visual Pattern Matching**: If 2+ sections have same layout but different content
2. **Props Over Duplication**: Use props for variations, not new components
3. **Generic Names**: Name by pattern, not content (e.g., `CardGrid` not `CaseStudies`)

### Component Hierarchy
```
Pages (compose components with content props)
  ↓
Organisms (full sections: HeroSection, GridSection, FeatureSection)
  ↓
Molecules (reusable blocks: Card, ListItem, Accordion)
  ↓
Atoms (basic elements: Button, Typography, Icon, Link)
```

## Common Patterns

### Figma Node ID Issues
If Figma node ID doesn't work:
1. Try using `mcp0_get_metadata("0:1")` to explore structure
2. Check project documentation for node ID references
3. Use grep_search to find node IDs in existing files

### Playwright Timeout Issues
If Playwright times out:
1. Close and restart: `mcp1_browser_close()`
2. Navigate to base URL first: `mcp1_browser_navigate("http://localhost:6008")`
3. Then navigate to specific story

### Image Loading Issues
- Ensure images are in `public/assets/`
- Use Next.js Image component
- Check browser console for 404 errors
- Verify image paths in Storybook static dirs config

## Error Recovery Procedures

### When Playwright Browser Fails
1. Check if browser already running
2. Try manual Storybook testing:
   ```bash
   curl "http://localhost:6010/iframe.html?id=component--story"
   ```
3. Take manual screenshots if needed
4. Continue with Storybook verification only

### When Images Are Missing
1. Find similar existing image:
   ```bash
   ls /public/assets/ | grep -i "similar_name"
   ```
2. Use existing image as fallback
3. Download from Figma localhost if available
4. Document the substitution

### When Component Doesn't Render in Storybook
1. Check import paths
2. Verify all props have defaults
3. Check browser console for errors
4. Start with minimal props, add complexity gradually
5. Test component in isolation first

### When TypeScript Errors Occur
1. Run `npx tsc --noEmit` to see all errors
2. Check missing imports
3. Verify prop types match
4. Ensure all dependencies installed

### When Port Conflicts Occur
1. **Check what's running on the port:**
   ```bash
   # Check port 3001 (dev server)
   lsof -ti:3001
   curl -s http://localhost:3001 | head -n 1
   
   # Check port 6010 (Storybook)
   lsof -ti:6010
   curl -s http://localhost:6010 | grep -o '<title>.*</title>'
   ```

2. **If correct service is running:**
   - Use the existing server
   - Don't start a new one
   - Example: "Storybook already running on port 6010, using existing instance"

3. **If wrong service or broken:**
   ```bash
   # Kill the process
   kill $(lsof -ti:6010)
   sleep 2
   
   # Start correct service
   npm run storybook
   ```

4. **Never start on alternative ports** - Always use the configured ports (3001 for dev, 6010 for Storybook)
