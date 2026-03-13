---
name: cia-data-integration
description: Expert knowledge in consuming CIA platform JSON exports, validation, caching strategies, and data pipeline integration
license: CC-BY-4.0
---

# CIA Data Integration Skill

## Purpose

This skill provides expertise in consuming JSON exports from the CIA (Citizen Intelligence Agency) platform, implementing robust caching strategies, and ensuring data quality through schema validation.

## Core Principles

1. **CIA is Source of Truth** - Never modify CIA's pre-computed data
2. **Validate Before Cache** - Always validate against CIA-provided JSON schemas
3. **Version Tracking** - Track all CIA data updates with timestamps
4. **Graceful Degradation** - Fall back to cached data if CIA unavailable
5. **Data Freshness** - Monitor and alert on stale data (> 24 hours)
6. **Audit Logging** - Log all data operations for traceability

## Enforces

### CIA Export Consumption
- Fetch 19 visualization products from CIA platform
- Handle rate limiting and connection failures
- Implement retry logic with exponential backoff
- Circuit breaker pattern for API failures

### JSON Schema Validation
```javascript
// Validate CIA export against schema
import Ajv from 'ajv';

const ajv = new Ajv({ allErrors: true });
const schema = await fetchCIASchema(productName);
const validate = ajv.compile(schema);

if (!validate(data)) {
  throw new ValidationError(validate.errors);
}
```

### Caching Strategy
```
data/cia-exports/
  current/          # Latest CIA exports (19 files)
  archive/          # Historical versions (date-stamped)
  metadata/         # Fetch timestamps, validation status
```

### Data Freshness Monitoring
- Track last fetch timestamp
- Alert if data > 24 hours old
- Display staleness warnings to users
- Automatic fallback to cached data

## When to Use

- Implementing CIA export fetch workflows
- Validating CIA JSON data
- Designing caching strategies
- Building data consumption pipelines
- Monitoring data freshness
- Handling API failures gracefully

## Examples

### CIA Export Client
```javascript
class CIAExportClient {
  async fetchExport(productName) {
    const url = `https://www.hack23.com/cia/api/export/${productName}.json`;
    const data = await fetch(url, { timeout: 30000 });
    
    await this.validateSchema(productName, data);
    await this.cacheWithVersion(productName, data);
    
    return data;
  }
}
```

### Automated Workflow
```yaml
# .github/workflows/fetch-cia-exports.yml
name: Fetch CIA Exports
on:
  schedule:
    - cron: '0 2 * * *'  # 02:00 CET daily

jobs:
  fetch:
    steps:
      - name: Fetch CIA exports
        run: node scripts/fetch-cia-exports.js
      
      - name: Validate schemas
        run: node scripts/validate-cia-data.js
      
      - name: Commit if changed
        run: |
          if git diff --quiet data/cia-exports/; then
            echo "No changes"
          else
            git add data/cia-exports/
            git commit -m "Update CIA exports"
            git push
          fi
```

## Remember

- CIA maintains the digital twin - riksdagsmonitor consumes it
- Validate all data before caching
- Monitor freshness and alert on staleness
- Provide graceful fallback to cached data
- Never modify CIA's pre-computed intelligence
- Log all operations for audit trail
- Respect rate limits and implement backoff

## References

- [CIA Platform](https://www.hack23.com/cia)
- [CIA Export Specs](https://github.com/Hack23/cia/tree/master/json-export-specs)
- [JSON Schema Validation](https://json-schema.org/)
- [Hack23 Secure Development Policy](https://github.com/Hack23/ISMS-PUBLIC/blob/main/Secure_Development_Policy.md)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Category**: Data Integration  
**Maintained by**: Hack23 AB
