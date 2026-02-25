---
name: review-script-template
description: This skill should be used when the user asks to "review a script template", "audit a template", "check template implementation", "validate ts-templates code", or mentions reviewing BitCom templates like AIP, MAP, SIGMA, BAP. Validates ScriptTemplate implementations against best practices.
---

# Review Script Template

Review and validate script template implementations in ts-templates for correctness and best practices.

## When to Use

- Review a new template before merging
- Audit existing template implementations
- Validate template follows ts-templates patterns
- Check for common implementation errors

## Review Checklist

### Structure Validation

- [ ] File located in `src/template/` appropriate subdirectory
- [ ] Implements `ScriptTemplate` interface from @bsv/sdk
- [ ] Exports PREFIX constant
- [ ] Exports Data interface with all protocol fields
- [ ] Default export is the template class
- [ ] Added to mod.ts exports (class + types)

### Interface Requirements

- [ ] `data` property is `public readonly`
- [ ] Constructor accepts Data interface
- [ ] `bitcomIndex?: number` field for protocol position
- [ ] `valid?: boolean` field for verification status

### Required Methods

| Method | Purpose | Requirements |
|--------|---------|--------------|
| `decode()` | Static. Parse from BitComDecoded | Return array of instances |
| `lock()` | Generate LockingScript | Use BitCom for OP_RETURN protocols |
| `unlock()` | Generate UnlockingScript | Throw if not applicable |
| `verify()` | Check signature validity | Return boolean |

### Code Quality

- [ ] Uses `script.chunks` directly (no toASM().split())
- [ ] Uses @bsv/sdk Utils (no Buffer, TextEncoder)
- [ ] Proper error handling in decode()
- [ ] No hardcoded magic numbers
- [ ] Consistent with other templates in repo

### Chunk Parsing Review

Correct pattern:
```typescript
const script = Script.fromBinary(protocol.script)
const chunks = script.chunks
const field = Utils.toUTF8(chunks[0].data ?? [])
```

Incorrect patterns to flag:
```typescript
// BAD: String splitting
const parts = script.toASM().split(' ')

// BAD: Buffer usage
const field = Buffer.from(chunks[0].data).toString()

// BAD: TextEncoder
new TextEncoder().encode(field)
```

### Utils Usage Review

Verify correct Utils functions:
| Operation | Correct | Incorrect |
|-----------|---------|-----------|
| String → bytes | `Utils.toArray(str, 'utf8')` | `Buffer.from()`, `TextEncoder` |
| Bytes → string | `Utils.toUTF8(bytes)` | `Buffer.toString()`, `TextDecoder` |
| Bytes → hex | `Utils.toHex(bytes)` | `Buffer.toString('hex')` |
| Bytes → base64 | `Utils.toBase64(bytes)` | `Buffer.toString('base64')` |

### Signature Verification Review

For protocols with signatures:
- [ ] Uses BSM.sign() for signing
- [ ] Tries all 4 recovery factors (0-3)
- [ ] Uses Signature.fromCompact() for decoding
- [ ] Verifies address matches recovered public key
- [ ] Sets `valid` field after verification

### BitCom Integration Review

For OP_RETURN protocols:
- [ ] Uses BitCom class for lock()
- [ ] Creates Protocol array with correct structure
- [ ] Proper pipe delimiter handling
- [ ] decode() accepts BitComDecoded parameter

## Common Issues

### Issue 1: Missing Null Checks

```typescript
// BAD: Can throw on missing data
const field = Utils.toUTF8(chunks[0].data)

// GOOD: Handle missing data
const field = Utils.toUTF8(chunks[0].data ?? [])
```

### Issue 2: Wrong Chunk Index

Verify chunk indices match protocol specification:
- Check protocol documentation for field order
- Account for protocol prefix being separate

### Issue 3: Incomplete Error Handling

```typescript
// BAD: Crashes on parse error
static decode(bitcom: BitComDecoded): Protocol[] {
  const script = Script.fromBinary(protocol.script) // Can throw!
}

// GOOD: Handle parse errors
static decode(bitcom: BitComDecoded): Protocol[] {
  try {
    const script = Script.fromBinary(protocol.script)
  } catch {
    continue // Skip invalid protocols
  }
}
```

### Issue 4: Missing mod.ts Export

Check that mod.ts includes:
```typescript
export { default as Protocol, PREFIX } from './src/template/...'
export type { ProtocolData, ProtocolOptions } from './src/template/...'
```

## Review Output Format

Provide structured feedback:

```markdown
## Template Review: [TemplateName]

### Structure: ✅ PASS / ❌ FAIL
- [Details]

### Methods: ✅ PASS / ❌ FAIL
- [Details]

### Code Quality: ✅ PASS / ❌ FAIL
- [Details]

### Issues Found
1. [Issue description and fix]
2. [Issue description and fix]

### Recommendations
- [Optional improvements]
```

## Additional Resources

### Reference Files

- **`references/checklist-detailed.md`** - Extended validation criteria
- **`references/common-bugs.md`** - Known issues and fixes
