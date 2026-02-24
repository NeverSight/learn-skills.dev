---
name: arkui-api-design
description: This skill should be used when the user asks to "design ArkUI API", "add component property", "create Modifier method", "review ArkUI API", "deprecate API", "write JSDOC for ArkUI", or mentions OpenHarmony API design standards. Provides comprehensive guidance for ArkUI component API design following OpenHarmony coding guidelines, including static/dynamic interface synchronization, SDK compilation, and verification.
version: 2.0.0
---

# ArkUI API Design Skill

This skill provides comprehensive guidance for designing, reviewing, and maintaining ArkUI component APIs that follow OpenHarmony Application TypeScript/JavaScript coding guidelines.

## Core Design Principles

### 1. Follow OpenHarmony Coding Standards

All API definitions and code examples must comply with the *OpenHarmony Application TypeScript/JavaScript Coding Guide*. Key standards include:

- **Naming conventions**: Use camelCase for properties and methods, PascalCase for types/interfaces
- **Type safety**: Provide proper TypeScript type definitions for all parameters
- **Code style**: Follow 4-space indentation, consistent formatting
- **Documentation**: Comprehensive JSDOC comments for all public APIs

For detailed standards, refer to: **`references/OpenHarmony-Application-Typescript-JavaScript-coding-guide.md`**

### 2. Synchronize Static and Dynamic Interfaces

**CRITICAL**: When adding or modifying component properties, you must update **both** static and dynamic interface files:

#### Static API (`.static.d.ets`)
- **Location**: `OpenHarmony/interface/sdk-js/api/arkui/component/<component>.static.d.ets`
- **Purpose**: Declarative UI API for ArkTS static type system
- **Usage**: Component declaration in `@Builder` functions
- **JSDOC Tags**: Add `@static` after `@since [version]` (e.g., `@since 26 static`)
- **Example**:
```typescript
// File: text.static.d.ets
/**
 * Provides a text component.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 7 static
 */
declare class Text {
  /**
   * Text content.
   *
   * @type { string | Resource }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 static
   * @stagemodelonly
   */
  content: string | Resource;

  /**
   * Creates a text component.
   *
   * @param content - Text content.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 static
   * @stagemodelonly
   */
  constructor(content: string | Resource);
}
```

#### Dynamic API (`.d.ts` Attribute Interface)
- **Location**: `OpenHarmony/interface/sdk-js/api/@internal/component/ets/<component>.d.ts`
- **Purpose**: Imperative modifier API for command-style property setting
- **Usage**: Chained property modification
- **JSDOC Tags**: Add `dynamic` after `@since [version]` (e.g., `@since 26 dynamic`)
- **Example**:
```typescript
// File: text.d.ts (in @internal/component/ets/)
/**
 * Text Attribute interface.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 7 dynamic
 */
declare class TextAttribute extends CommonMethod<TextAttribute> {
  /**
   * Sets the text content.
   *
   * @param value - Text content to display.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   * @stagemodelonly
   */
  content(value: string | Resource): TextAttribute;
}
```

**Note**: The `*Modifier.d.ts` files in `arkui/` directory only define the Modifier class (for `AttributeModifier` pattern), not the Attribute interface itself.

#### Synchronization Rules

| Scenario | Static API | Dynamic API |
|----------|-----------|-------------|
| **Add property** | Add to class/interface | Add to Attribute class |
| **Deprecate property** | Mark as `@deprecated` | Mark as `@deprecated` |
| **Change signature** | Update class definition | Update Attribute method |
| **File location** | `arkui/component/*.static.d.ets` | `@internal/component/ets/*.d.ts` |
| **Version tag** | `@since X static` | `@since X dynamic` |
| **Return type** | Use `this` for chainable | Use concrete Attribute type |

### 3. Support Resource Type for Configurable Properties

**IMPORTANT**: Not all properties need Resource type support. Only add Resource type when the property is intended to be configured through resource files (theming, i18n, etc.).

**When to support Resource type:**
- ✅ **YES**: Colors, fonts, sizes, strings, images - anything developers might configure through resource files for theming or internationalization
- ❌ **NO**: State flags, mode selectors, event callbacks - these are runtime-only configurations

**Type Simplification Rule:**
**CRITICAL**: Only use `ResourceStr` for **NEW APIs (API 13+)**. Do NOT use `ResourceStr` to modify existing APIs (API 12 and earlier).

**When to use ResourceStr:**
- ✅ **YES**: For NEW properties/methods (introduced in API 13 or later)
- ❌ **NO**: For existing properties/methods (API 12 and earlier)

```typescript
// ❌ WRONG: Using ResourceStr for API 12 (existing property)
content(value: ResourceStr): TextAttribute  // API 12 - DO NOT MODIFY

// ✅ CORRECT: Using string | Resource for API 12 (maintaining backward compatibility)
content(value: string | Resource): TextAttribute  // API 12 - KEEP AS IS

// ✅ CORRECT: Using ResourceStr for NEW API 13 (new property)
fontSize(value: number | string | Length | ResourceStr): TextAttribute  // API 13 - NEW PROPERTY

// Benefits:
// - Maintains backward compatibility for existing APIs
// - Allows simplification for new APIs
// - Clear version boundary at API 13
```

**Examples of properties that SHOULD support Resource:**
```typescript
// Theme-related - YES, support Resource (API 12: keep original type)
fontSize(value: number | string | Length | Resource): TextAttribute
// API 12 and earlier: Maintain string | Resource for compatibility

// Theme-related - YES, support Resource (API 13+: use ResourceStr)
fontSize(value: number | string | Length | ResourceStr): TextAttribute
// API 13 and later: Simplified type

// Usage examples (API 12 - old API, keep string | Resource):
Text().fontSize(16)                              // number
Text().fontSize('16vp')                          // string
Text().fontSize($r('app.float.font_size_large')) // Resource

// Usage examples (API 13+ - new API, use ResourceStr):
Text().fontSize(16)                               // number
Text().fontSize('16vp')                          // string
Text().fontSize($r('app.float.font_size_large')) // Resource (ResourceStr covers this too)
```

**Examples of properties that SHOULD NOT support Resource:**
```typescript
// State flags - NO, these are runtime-only
stateEffect(value: boolean): ButtonAttribute
enabled(value: boolean): CommonMethod

// Event callbacks - NO, these are runtime-only
onClick(callback: () => void): CommonMethod
```

**Benefits of ResourceStr support (for NEW APIs only):**
- Enables centralized theme management through resource files
- Supports internationalization with locale-specific resources
- Allows dynamic theming without code changes
- **Type simplification**: Use `ResourceStr` instead of `string | Resource`
- **Backward compatibility**: Preserve existing API signatures for API 12 and earlier

### 4. Document undefined/null Behavior

JSDOC comments must explicitly specify how `undefined` and `null` values are handled:

```typescript
/**
 * Sets font size of text.
 * @param value Font size value. If undefined, restores to default size (16fp).
 *              If null, removes the font size setting and uses inherited value.
 * @throws {Error} Throws error if value is negative.
 * @since 10
 */
fontSize(value: number | string | Length | Resource | undefined | null): TextAttribute;
```

**Common patterns:**
- `undefined` → Restore default value
- `null` → Remove setting, use inherited value
- Invalid values → Throw error with clear message

### 5. Use vp as Default Length Unit

Always use `vp` (virtual pixels) as default unit for length measurements:

```typescript
// Good: Default to vp
width(value: number | string): ButtonAttribute  // 100 means 100vp

// Good: Explicit vp
width(value: Length): ButtonAttribute  // Length.type defaults to vp

// Avoid: Require px without good reason
width(value: number): ButtonAttribute  // 100px - avoid unless necessary
```

### 6. Specify Constraints in JSDOC

JSDOC comments must include specification limits and constraints:

```typescript
/**
 * Sets border radius of component.
 * @param value Border radius value. Valid range: 0-1000vp.
 *              Values exceeding 1000vp will be clamped to 1000vp.
 *              Negative values are treated as 0.
 * @unit vp
 * @since 10
 */
borderRadius(value: number | string | Length): CommonMethod;
```

**Required documentation:**
- Valid ranges (min/max values)
- Special value handling (negative, zero, etc.)
- Unit of measurement
- Clamping behavior (if applicable)

### 7. Consider Cross-Component Impact

When adding common properties, evaluate impact on all components:

**Before adding common property:**
1. Check if property applies to most components (layout, style, event)
2. Define consistent behavior across component types
3. Document component-specific exceptions (if any)
4. Consider backward compatibility

**Example common properties:**
- Layout: `width()`, `height()`, `padding()`, `margin()`
- Style: `opacity()`, `visibility()`, `borderRadius()`
- Event: `onClick()`, `onTouch()`

### 8. Respect Interface Directory Boundaries

During API design and compilation verification, work only with files within `interface/` directory:

**Allowed modifications:**
- `interface/sdk-js/api/arkui/component/*.static.d.ets` - Static API definitions
- `interface/sdk-js/api/@internal/component/ets/*.d.ts` - Dynamic API definitions (Attribute classes)
- `interface/sdk-js/api/arkui/*Modifier.d.ts` - Modifier class definitions (for AttributeModifier pattern)
- Type definition files (*.d.ts, *.static.d.ets)

**Do NOT modify:**
- Framework implementation code in `ace_engine/`
- Component pattern files
- Layout or render implementations

---

## API Design Workflow

### Complete Workflow for New Component Properties

```
1. Design API
   ├─ Define property types and constraints
   ├─ Document undefined/null behavior
   └─ Check cross-component impact

2. Create Static API (.static.d.ets)
   ├─ Add property to component class
   ├─ Write complete JSDOC
   └─ Include @since, @syscap tags

3. Create Dynamic API (@internal/component/ets/*.d.ts)
   ├─ Add method to Attribute class
   ├─ Match signature with static API
   └─ Synchronize JSDOC documentation

4. Verify Type Safety
   ├─ Check TypeScript compilation
   ├─ Validate type definitions
   └─ Ensure signature consistency

5. Build SDK
   ├─ Run SDK build command
   └─ Monitor compilation errors

6. Verify SDK Output
   ├─ Check generated API files
   ├─ Verify new APIs are exported
   └─ Test API availability
```

### For New Component APIs

1. **Design API interface** with proper TypeScript types
2. **Create Static API** (`component/*.static.d.ets`)
   - Define component class with properties
   - Add constructor and methods
   - Write complete JSDOC comments
3. **Create Dynamic API** (`@internal/component/ets/*.d.ts`)
   - Define Attribute class methods
   - Add all property methods
   - Sync with static API signatures
4. **Add JSDOC comments** including:
   - Parameter descriptions
   - undefined/null handling
   - Value constraints and ranges
   - Default values
   - @since version
   - @syscap capability
   - @throws documentation (if applicable)
5. **Support Resource type** for theme-able properties
6. **Specify units** (default to vp for lengths)
7. **Verify cross-component impact** if adding common property
8. **Build SDK** to verify compilation

### For API Reviews

Use the following checklist to verify:
- [ ] Static API (`.static.d.ets`) exists and is complete
- [ ] Dynamic API (`@internal/component/ets/*.d.ts`) exists and is synchronized
- [ ] Parameter types match between static and dynamic
- [ ] Version tags correct (`@since X static` vs `@since X dynamic`)
- [ ] Return type convention correct (`this` in static, concrete type in dynamic)
- [ ] Compliance with coding standards
- [ ] Resource type support where appropriate
- [ ] Complete JSDOC documentation
- [ ] Constraint specifications
- [ ] Cross-component consistency
- [ ] @since and @syscap tags present

### For API Deprecation

**CRITICAL**: When deprecating an API, you MUST mark BOTH the static API property/method AND the corresponding dynamic API method as `@deprecated`.

1. Mark both static and dynamic APIs as `@deprecated`
2. Provide migration path in JSDOC
3. Specify removal version (@obsoleted)
4. Update documentation and examples

**Synchronization Requirement:**
- If you deprecate a property in static API → MUST deprecate in dynamic API
- If you deprecate a method in static API → MUST deprecate in dynamic API
- Both must have matching @deprecated, @obsoleted, @see, and @migration tags

---

## SDK Build and Verification

### Building the SDK

After completing API design changes, build the SDK to verify compilation and generate output:

```bash
# From OpenHarmony root directory
./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache
```

**Build Parameters:**
- `--export-para PYCACHE_ENABLE:true` - Enable Python cache for faster builds
- `--product-name ohos-sdk` - Build SDK target
- `--ccache` - Use compiler cache for incremental builds

**Build Output Location:**
```
out/ohos-sdk/
├── interfaces/
│   └── sdk-js/
│       └── api/
│           └── arkui/
│               ├── component/           # Generated .static.d.ets files
│               │   ├── button.static.d.ets
│               │   ├── text.static.d.ets
│               │   └── ...
│               ├── ButtonModifier.d.ts  # Generated .d.ts files
│               ├── TextModifier.d.ts
│               └── ...
```

### Verification Steps

After SDK build completes successfully:

#### 1. Verify Static API

```bash
# Check if .static.d.ets file contains your changes
grep -n "yourNewProperty" out/ohos-sdk/interfaces/sdk-js/api/arkui/component/<yourcomponent>.static.d.ets
```

#### 2. Verify Dynamic API

```bash
# Check if @internal/component/ets/*.d.ts file contains your changes
grep -n "yourNewMethod" out/ohos-sdk/interfaces/sdk-js/api/@internal/component/ets/<your_component>.d.ts
```

#### 3. Verification Checklist

- [ ] Build completes without errors
- [ ] Static API file (`.static.d.ets`) contains new/modified properties
- [ ] Dynamic API file (`@internal/component/ets/*.d.ts`) contains corresponding methods
- [ ] JSDOC comments are present and complete
- [ ] Type signatures match between static and dynamic APIs
- [ ] Version tags correct (`@since X static` vs `@since X dynamic`)
- [ ] No compilation warnings or errors in interface files

#### 4. Common Build Issues

| Issue | Symptom | Solution |
|-------|----------|----------|
| Type mismatch | Build fails with type error | Check signatures match between static/dynamic APIs |
| Missing import | Cannot find type | Add proper import statements |
| JSDOC error | Documentation warning | Fix JSDOC syntax, ensure all tags are valid |
| Sync error | API exists in one file only | Add to both static and dynamic files |

---

## Code Examples

### Example 1: Complete Static + Dynamic API

#### Static API: `button.static.d.ets`

```typescript
/**
 * Provides a button component.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 7
 */
declare class Button {
  /**
   * Button type.
   *
   * @type { ButtonType }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7
   */
  type: ButtonType;

  /**
   * Button state.
   *
   * @type { ButtonState }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7
   */
  stateEffect: boolean;

  /**
   * Creates a button component.
   *
   * @param label - Button label text.
   * @param options - Button options.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7
   */
  constructor(label: string | Resource, options?: ButtonOptions);
}
```

#### Dynamic API: `button.d.ts` (in `@internal/component/ets/`)

```typescript
/**
 * Button Attribute class.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 7 dynamic
 */
declare class ButtonAttribute extends CommonMethod<ButtonAttribute> {
  /**
   * Sets the button type.
   *
   * @param value - Button type to set.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   */
  type(value: ButtonType): ButtonAttribute;

  /**
   * Enables or disables state effect.
   *
   * @param value - Whether to enable state effect. Default is true.
   *              If undefined, enables state effect.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   */
  stateEffect(value: boolean): ButtonAttribute;
}
```

### Example 2: Adding a New Property

#### Adding `iconSize` to Button

**Static API Update:**
```typescript
// File: button.static.d.ets
declare class Button {
  // Existing properties...
  /**
   * Icon size.
   *
   * @type { number | string }
   * @unit vp
   * @default 24vp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 12
   */
  iconSize: number | string;
}
```

**Dynamic API Update:**
```typescript
// File: button.d.ts (in @internal/component/ets/)
declare class ButtonAttribute extends CommonMethod<ButtonAttribute> {
  // Existing methods...

  /**
   * Sets the icon size.
   *
   * @param value - Icon size in vp. Valid range: 0-100vp.
   *              If undefined, restores to default size (24vp).
   * @unit vp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 12 dynamic
   */
  iconSize(value: number | string | Length | undefined): ButtonAttribute;
}
```

### Example 3: API Deprecation

#### Deprecating `setFontSize` in favor of `fontSize`

**Static API:**
```typescript
declare class Text {
  /**
   * Font size.
   *
   * @type { number | string | Resource }
   * @unit fp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7
   */
  fontSize: number | string | Resource;

  /**
   * Sets the font size.
   *
   * @param value - Font size value.
   * @deprecated since 10. Use fontSize property instead.
   * @see fontSize
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7
   * @obsoleted 10
   */
  setFontSize(value: number | string | Resource): void;
}
```

**Dynamic API:**
```typescript
// File: text.d.ts (in @internal/component/ets/)
declare class TextAttribute extends CommonMethod<TextAttribute> {
  /**
   * Sets the font size.
   *
   * @param value - Font size in fp. Valid range: 0-1000fp.
   * @unit fp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 10 dynamic
   */
  fontSize(value: number | string | Length | Resource | undefined | null): TextAttribute;

  /**
   * Sets the font size (deprecated method).
   *
   * @param value - Font size value.
   * @deprecated since 10. Use fontSize() instead.
   * @see fontSize
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   * @obsoleted 10
   */
  setFontSize(value: number | string | Resource): TextAttribute;
}
```

---

## Common Pitfalls

### Missing Static/Dynamic Synchronization

```typescript
// ❌ Bad: Only static API defined
// File: text.static.d.ets
declare class Text {
  content: string | Resource;
}

// Missing: @internal/component/ets/text.d.ts has no content() method

// ✅ Good: Both APIs synchronized
// File: text.static.d.ets
declare class Text {
  content: string | Resource;
}

// File: text.d.ts (in @internal/component/ets/)
declare class TextAttribute extends CommonMethod<TextAttribute> {
  content(value: string | Resource): TextAttribute;
}
```

### Inconsistent Signatures

```typescript
// ❌ Bad: Signatures don't match
// Static: .static.d.ets
iconSize: number;

// Dynamic: @internal/component/ets/*.d.ts
iconSize(value: number | string | Resource): ButtonAttribute; // Different types!

// ✅ Good: Consistent types
// Static: .static.d.ets
iconSize: number | string;

// Dynamic: @internal/component/ets/*.d.ts
iconSize(value: number | string): ButtonAttribute; // Matches
```

### Incomplete JSDOC

```typescript
// ❌ Bad: Missing null/undefined handling, constraints
/**
 * Sets the width.
 */
width(value: number): CommonMethod;

// ✅ Good: Complete documentation
/**
 * Sets the component width.
 * @param value Width value in vp. Valid range: 0-10000vp.
 *              If undefined, restores default width.
 * @unit vp
 * @since 8
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 */
width(value: number | string | Length | undefined): CommonMethod;
```

### Forgetting Resource Type

```typescript
// ⚠️ Less optimal: Only accepts number/string
fontSize(value: number | string): TextAttribute;

// ✅ Better: Supports resource theming
fontSize(value: number | string | Length | Resource): TextAttribute;
```

---

## Additional Resources

### Coding Standards

- **`references/OpenHarmony-Application-Typescript-JavaScript-coding-guide.md`**
  - OpenHarmony TypeScript/JavaScript Coding Guide (official complete version)
  - Contains naming conventions, type definitions, code formatting, and all coding standards
  - All design principles in this skill are based on this document

### Example Code

- **`examples/interface-definition.ts`** - Complete interface definition example
- **`examples/modifier-implementation.ts`** - Modifier method implementation example
- **`examples/deprecation-pattern.ts`** - API deprecation with migration example
- **`examples/static-dynamic-sync.ts`** - Static/Dynamic API synchronization example

### Knowledge Base References

- **`docs/sdk/Component_API_Knowledge_Base_CN.md`** - ArkUI 组件 API 知识库
  - Explains difference between static and dynamic APIs
  - File structure and organization
  - Component API classification

- **`docs/sdk/ArkUI_SDK_API_Knowledge_Base.md`** - ArkUI SDK API 结构化分析文档
  - SDK API vs ace_engine implementation mapping
  - Static API vs Dynamic API comparison
  - FrameNode/BuilderNode/Modifier patterns

---

## Quick Reference

### Essential JSDOC Tags

```typescript
/**
 * Brief description.
 * @param paramName Description including undefined/null behavior and constraints.
 * @unit vp | fp | px (for length values)
 * @throws {ErrorType} Description (when errors can occur)
 * @since version static (for Static API - use "static" after version)
 * @since version dynamic (for Dynamic API - use "dynamic" after version)
 * @syscap SystemCapability.ArkUI.ArkUI.Full (system capability)
 * @stagemodelonly (indicates this is a stage model only API)
 * @deprecated Use alternativeMethod() instead (for deprecated APIs)
 * @obsoleted version (when API was removed)
 */
```

**Important Tag Rules:**
- **Static API (`.static.d.ets`)**: Use `@since X static` format (e.g., `@since 26 static`)
- **Dynamic API (`*Modifier.d.ts`)**: Use `@since X dynamic` format (e.g., `@since 26 dynamic`)
- **All APIs**: Add `@stagemodelonly` tag to indicate stage model only

### Type Support Decision Tree

```
Does the parameter accept length values?
├─ Yes → Add Length and Resource types
└─ No → Is it theme-able (color, size, string)?
    ├─ Yes → Add Resource type
    └─ No → Use basic types (number | string | undefined | null)
```

### Default Value Documentation

```typescript
// Document defaults in JSDOC:
"If undefined, restores to default [value] ([unit])."
"If null, removes setting and uses inherited value."
```

### Static vs Dynamic API Quick Reference

| Aspect | Static API (`.static.d.ets`) | Dynamic API (`*.d.ts`) |
|--------|----------------------------|-------------------------------|
| **File Location** | `arkui/component/` | `@internal/component/ets/` |
| **Usage** | `Text({ content: 'Hello' })` | `Text().content('Hello')` |
| **Type** | Class declaration | Class extending CommonMethod |
| **Pattern** | Constructor-based | Method chaining |
| **Return Type** | N/A (properties) | Concrete Attribute type |
| **Version Tag** | `@since X static` | `@since X dynamic` |
| **Both Required** | ✅ Yes | ✅ Yes |

### Static/Dynamic Synchronization Checklist

Before finalizing any API, verify:

#### Files Updated
- [ ] Static file: `interface/sdk-js/api/arkui/component/*.static.d.ets`
- [ ] Dynamic file: `interface/sdk-js/api/@internal/component/ets/*.d.ts`

#### Signatures Match
- [ ] Parameter types identical
- [ ] Optional parameters consistent
- [ ] Generic types aligned

#### JSDOC Complete
- [ ] @param descriptions match
- [ ] @returns descriptions match (dynamic only)
- [ ] Version tags: `@since XX static` vs `@since XX dynamic`
- [ ] @syscap tags identical
- [ ] @unit tags consistent

#### Return Type Convention
- [ ] Static: Properties (no return type for properties)
- [ ] Dynamic: Concrete type (e.g., `ButtonAttribute`)

#### Version Tags
- [ ] Static: `@since 26 static`
- [ ] Dynamic: `@since 26 dynamic`

#### Compilation Verified
- [ ] Static file compiles
- [ ] Dynamic file compiles
- [ ] No type errors
- [ ] No JSDOC warnings

---

## Common Mistakes to Avoid

### 1. Only Updating One File

❌ **Bad**: Only static file updated
```typescript
// Static: richEditor.static.d.ets
default lineSpacing(value: LengthMetrics | undefined): this;

// Dynamic: rich_editor.d.ts
// Method is missing! ✗
```

✅ **Good**: Both files updated
```typescript
// Static: richEditor.static.d.ets
default lineSpacing(value: LengthMetrics | undefined, options?: LineSpacingOptions): this;

// Dynamic: rich_editor.d.ts
lineSpacing(value: LengthMetrics | undefined, options?: LineSpacingOptions): RichEditorAttribute;
```

### 2. Inconsistent Parameter Types

❌ **Bad**: Different parameter types
```typescript
// Static:
default lineSpacing(value: LengthMetrics): this;

// Dynamic:
lineSpacing(value: LengthMetrics | undefined): RichEditorAttribute;
// ✗ Parameter types don't match!
```

✅ **Good**: Identical parameter types
```typescript
// Static:
default lineSpacing(value: LengthMetrics | undefined, options?: LineSpacingOptions): this;

// Dynamic:
lineSpacing(value: LengthMetrics | undefined, options?: LineSpacingOptions): RichEditorAttribute;
// ✓ Parameters match perfectly
```

### 3. Missing Version Tags

❌ **Bad**: Generic version tags
```typescript
// Static: @since 26
// Dynamic: @since 26
// ✗ Missing static/dynamic specification
```

✅ **Good**: Proper version tags
```typescript
// Static: @since 26 static
// Dynamic: @since 26 dynamic
// ✓ Clear distinction
```

### 4. Wrong File Location

❌ **Bad**: Looking for dynamic API in wrong location
```typescript
// Looking in: arkui/ButtonModifier.d.ts
// This file only defines Modifier class, not Attribute interface!
```

✅ **Good**: Correct file location
```typescript
// Dynamic API is in: @internal/component/ets/button.d.ts
// This file defines ButtonAttribute class with all methods
```
