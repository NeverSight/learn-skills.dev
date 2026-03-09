---
name: react-review
description: Review React components for best practices and performance issues
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: development
---

# React Review Skill

Review React components for best practices, performance issues, and common patterns.

## When to use me

Use this skill when:
- Reviewing React component code
- Optimizing component performance
- Checking for React best practices
- Refactoring legacy components
- Auditing component architecture

## What I do

- Analyze React components for performance issues (unnecessary re-renders, large bundles)
- Check for React best practices (hooks usage, prop patterns, state management)
- Identify anti-patterns (prop drilling, useEffect misuse, missing keys)
- Suggest optimizations (memoization, code splitting, lazy loading)
- Review TypeScript usage and type safety

## Examples

```bash
# Review a specific component file
agent: Review the component in src/components/UserProfile.tsx

# Review all components in a directory  
agent: Review React components in src/components/

# Check for performance issues
agent: Find performance issues in the Button component
```

## Output format

```
## React Component Review

### Component: UserProfile.tsx

**Issues Found:**
1. Performance: Missing React.memo on component that receives object props
2. Best Practice: useEffect missing dependency array
3. Type Safety: Missing TypeScript interfaces for props

**Recommendations:**
1. Wrap component with React.memo
2. Add dependency array to useEffect
3. Create interface for component props

**Code Suggestions:**
```typescript
interface UserProfileProps {
  user: User;
  onUpdate: (user: User) => void;
}

const UserProfile = React.memo(({ user, onUpdate }: UserProfileProps) => {
  // implementation
});
```
```

## Notes

- Focuses on React 18+ patterns and best practices
- Considers both class and function components
- Includes TypeScript and JavaScript variants
- References official React documentation and community patterns
