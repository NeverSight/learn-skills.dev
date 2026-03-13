---
name: ui-guidelines
description: Comprehensive UI/UX guidelines for building React/Next.js components with Ant Design, shadcn/ui charts, and consistent styling. Use when creating forms, tables, modals, cards, or any UI component. Enforces color palette, typography, spacing (8px/12px/16px/24px), animations, and component patterns specific to the application.
---

# UI Guidelines for Application

## Overview

This skill provides comprehensive UI/UX guidelines for building components in a React/Next.js application using Ant Design, shadcn/ui, and consistent design tokens. It ensures all new components match the existing design system with proper colors, spacing, typography, and interaction patterns.

## When to Use This Skill

Trigger this skill when:
- **Creating UI components**: forms, tables, modals, cards, lists
- **Adding new features** that require UI elements
- **Building data visualizations** or dashboards
- **Implementing loading states** or animations
- **Styling components** to match the design system
- **User asks to build/create/add** any visual component

## Quick Start

### Step 1: Identify Component Type

Determine what you're building:
- **Drawer/Side Panel** → Read `references/component-patterns.md` (Drawer Patterns section) **[MANDATORY PATTERN]**
- **Data Table** → Read `references/codebase-patterns.md` (Tables section)
- **Form/Modal** → Read `references/codebase-patterns.md` (Modal Patterns section)
- **Card/Grid** → Read `references/codebase-patterns.md` (Card Patterns section)
- **Need colors/spacing** → Read `references/design-tokens.md`
- **Need animations/loading** → Read `references/animations.md`

### Step 2: Follow the Component Checklist

Every component must:
- [ ] Use Ant Design components as the base
- [ ] Apply consistent spacing (8px, 12px, 16px, 24px)
- [ ] Use theme tokens (`token.colorText`, `token.colorBgContainer`)
- [ ] Include proper TypeScript types
- [ ] Handle loading states (Skeleton, Spin, or loading prop)
- [ ] Show feedback with `message.success()` / `message.error()`
- [ ] Support responsive design
- [ ] Include proper error handling

### Step 3: Apply Core Design Tokens

**Colors:**
- Brand Orange: `#F79402` (primary brand color)
- Product Owner: `#7C4DFF` (purple)
- Tech Owner: `#52c41a` (green)
- Error/Overdue: `#ff4d4f` (red)
- Always use `theme.useToken()` for dynamic colors

**Spacing:**
- Small gap: `8px`
- Medium gap: `12px`
- Standard padding: `16px`
- Section margin: `24px`

**Typography:**
- Table cells: `fontSize: 12`
- Secondary text: `fontSize: '11px'`
- Strong text: `<Text strong>`
- Secondary: `<Text type="secondary">`

## Core Patterns

### Pattern 1: Data Tables

All data tables should follow this structure:

```tsx
import { Table, Input, Select, ConfigProvider, theme } from "antd";
import { SearchOutlined } from "@ant-design/icons";

export default function DataTable() {
  const { token } = theme.useToken();
  
  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
      {/* Filters row */}
      <div style={{ marginBottom: 16, display: "flex", gap: "8px" }}>
        <Input placeholder="Search..." prefix={<SearchOutlined />} style={{ flex: 1 }} allowClear />
        <Select style={{ flex: 1 }} placeholder="Filter" allowClear />
      </div>

      {/* Table with custom theme */}
      <ConfigProvider theme={{
        components: { Table: { headerBg: token.colorBgContainer, fontSize: 12 } }
      }}>
        <Table
          dataSource={data}
          loading={isLoading}
          rowKey="id"
          size="small"
          pagination={false}
          scroll={{ y: 'calc(100vh - 220px)', x: 'max-content' }}
        />
      </ConfigProvider>
    </div>
  );
}
```

**Key details:**
- Use `ConfigProvider` for table theme customization
- Set `fontSize: 12` for compact display
- Use `scroll={{ y: 'calc(100vh - 220px)' }}` for proper scrolling
- Always include `rowKey="id"`
- Set `size="small"` for compact tables

### Pattern 2: Forms in Modals

Standard form modal pattern:

```tsx
import { Modal, Form, Input, Button, message } from "antd";

export default function AddModal({ isOpen, onClose, onSuccess }) {
  const [form] = Form.useForm();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setIsSubmitting(true);
      await api.post('/endpoint', values);
      message.success("Created successfully");
      form.resetFields();
      onSuccess();
      onClose();
    } catch (error) {
      message.error(error.response?.data?.error || "Failed to create");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal title="Add Item" open={isOpen} onCancel={onClose} footer={null} maskClosable={true}>
      <Form form={form} layout="vertical" onFinish={handleSubmit}>
        <Form.Item name="name" label="Name" rules={[{ required: true, message: "Please enter name" }]}>
          <Input placeholder="Enter name" />
        </Form.Item>
        
        <Form.Item style={{ marginBottom: 0, marginTop: 16, textAlign: "right" }}>
          <Button onClick={onClose} style={{ marginRight: 8 }}>Cancel</Button>
          <Button htmlType="submit" loading={isSubmitting}>Create</Button>
        </Form.Item>
      </Form>
    </Modal>
  );
}
```

**Key details:**
- Use `layout="vertical"` for labels above inputs
- Include validation rules with clear messages
- Reset form on success: `form.resetFields()`
- Show feedback: `message.success()` / `message.error()`
- Set `maskClosable={true}` for better UX

### Pattern 3: Selectable Card Grids

Horizontal scrolling cards with selection:

```tsx
import { theme, Typography, Avatar } from "antd";

const { Text } = Typography;
const { token } = theme.useToken();

<div style={{
  display: "flex",
  gap: "12px",
  overflowX: "auto",
  paddingBottom: "4px"
}}>
  {items.map((item) => {
    const isSelected = selectedId === item.id;
    return (
      <div
        key={item.id}
        onClick={() => setSelectedId(isSelected ? null : item.id)}
        style={{
          flex: 1,
          minWidth: '200px',
          maxWidth: '280px',
          padding: '12px',
          cursor: 'pointer',
          borderRadius: '8px',
          border: isSelected ? '1px solid #F79400' : `1px solid ${token.colorBorder}`,
          backgroundColor: isSelected ? token.colorFillSecondary : token.colorBgContainer,
          boxShadow: '0 1px 2px rgba(0, 0, 0, 0.04)',
        }}
      >
        <Text strong style={{ fontSize: '14px' }}>{item.name}</Text>
        {/* Additional content */}
      </div>
    );
  })}
</div>
```

**Key details:**
- Selected state: border with brand primary color
- Subtle shadow: `0 1px 2px rgba(0, 0, 0, 0.04)`
- Border radius: `8px`
- Use `token.colorBorder` for unselected state

### Pattern 4: Loading States

Always show loading feedback:

```tsx
// Table loading
<Table loading={isLoading} dataSource={data} />

// Card loading skeleton
{data === undefined ? (
  <Card loading style={{ minWidth: '200px' }} />
) : (
  <Card>{content}</Card>
)}

// Button loading
<Button htmlType="submit" loading={isSubmitting}>Submit</Button>

// Page content skeleton
<Skeleton active paragraph={{ rows: 4 }} />
```

### Pattern 5: Avatars with Fallbacks

```tsx
{user.profilePic ? (
  <Avatar size={24} src={getCachedAvatarUrl(user.profilePic)} />
) : (
  <Avatar size={24} style={{ backgroundColor: getAvatarColor(user.name) }}>
    {user.name.charAt(0).toUpperCase()}
  </Avatar>
)}
```

## Styling Approach

### Priority Order
1. **Ant Design props** first (type, size, danger, etc.)
2. **Theme tokens** for colors (`token.colorBgContainer`)
3. **Inline styles** for layout and spacing
4. **Tailwind** rarely (only for utility classes)

### DO's ✅
- Use Ant Design components as base
- Use `theme.useToken()` for colors
- Apply consistent spacing (8px, 12px, 16px, 24px)
- Include loading states everywhere
- Show user feedback with messages
- Handle errors gracefully
- Use TypeScript types

### DON'Ts ❌
- Don't use CSS-in-JS libraries
- Don't create custom CSS files
- Don't hardcode colors (use tokens)
- Don't skip error handling
- Don't ignore responsive design
- Don't use excessive shadows

## Common Recipes

### Status Tag
```tsx
<Tag color={status.color || "#d9d9d9"} style={{ borderRadius: "8px", fontSize: 12 }}>
  {status.name || "Not Set"}
</Tag>
```

### Clickable Text
```tsx
<Text strong style={{ cursor: 'pointer', fontSize: 12 }} onClick={() => router.push(`/path/${id}`)}>
  {title}
</Text>
```

### Overdue Indicator
```tsx
{isOverdue && (
  <Tooltip title={`Overdue since ${date}`}>
    <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#ff4d4f' }} />
  </Tooltip>
)}
```

### Select with Item Counts
```tsx
<Select>
  {items.map(item => (
    <Option key={item.id} value={item.id}>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <span>{item.name}</span>
        <Text type="secondary" style={{ fontSize: '11px' }}>{item.count} items</Text>
      </div>
    </Option>
  ))}
</Select>
```

## Reference Files

Read these files for detailed information:

1. **[design-tokens.md](references/design-tokens.md)** - Colors, spacing, typography system
2. **[codebase-patterns.md](references/codebase-patterns.md)** - Real patterns from existing code
3. **[component-patterns.md](references/component-patterns.md)** - Ant Design component standards
4. **[styling-layout.md](references/styling-layout.md)** - Layout patterns and responsive design
5. **[animations.md](references/animations.md)** - Loading indicators and transitions

## Decision Tree

**Building something new?**

1. **Is it a table?** → Read `codebase-patterns.md` Tables section
2. **Is it a form?** → Read `codebase-patterns.md` Modal Patterns section
3. **Is it a card grid?** → Read `codebase-patterns.md` Card Patterns section
4. **Need specific colors?** → Read `design-tokens.md`
5. **Need loading animation?** → Read `animations.md`

**For ANY component:**
- Use TypeScript
- Handle loading states
- Show error messages
- Use theme tokens
- Test responsiveness

## Typography Scale

```tsx
// Strong text (table headers, card titles)
<Text strong style={{ fontSize: '12px' }}>Title</Text>

// Regular text (table cells, body)
<Text style={{ fontSize: '12px' }}>Content</Text>

// Secondary text (subtitles, metadata)
<Text type="secondary" style={{ fontSize: '11px' }}>Metadata</Text>

// Tertiary text (additional info)
<Text style={{ fontSize: '11px', color: token.colorTextTertiary }}>Info</Text>
```

## Page Layout

Standard full-height page layout:

```tsx
export default function Page() {
  return (
    <div style={{ 
      height: "100%", 
      display: "flex", 
      flexDirection: "column",
      overflow: "hidden",
      padding: "24px 40px 24px 24px"
    }}>
      {/* Page content with proper scrolling */}
    </div>
  );
}
```

## Data Fetching

Use SWR for data fetching:

```tsx
import useSWR from "swr";
import { fetcher } from "@/lib/axios";

const { data, error, isLoading, mutate } = useSWR(
  '/api/endpoint',
  fetcher,
  {
    revalidateOnFocus: false,
    revalidateOnReconnect: false,
  }
);
```

## Final Checklist

Before completing any component:
- [ ] Uses Ant Design as base
- [ ] Applies theme tokens for colors
- [ ] Has consistent spacing
- [ ] Includes loading states
- [ ] Shows error feedback
- [ ] Has TypeScript types
- [ ] Works responsively
- [ ] Matches existing patterns
- [ ] Uses `fontSize: 12` for tables
- [ ] Includes proper validation
