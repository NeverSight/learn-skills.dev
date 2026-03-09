---
name: spec-gap-analysis
description: Analyze gaps between formal specifications (API specs, interface specs, architecture specs) and actual implementations with specialized support for structured specification formats
license: MIT
compatibility: opencode
metadata:
  audience: API developers, architects, contract-first developers, integration engineers
  category: analysis
---

# Specification Gap Analysis

Specialized analysis of discrepancies between formal specifications (OpenAPI/Swagger, Protobuf, GraphQL, architecture diagrams) and actual implementations, with focused support for structured specification formats and contract-first development approaches.

## When to use me

Use this skill when:
- Working with contract-first or API-first development approaches
- API specifications exist but implementation status is unclear
- Interface definitions (Protobuf, GraphQL schemas) need validation against implementations
- Architecture specifications require verification against deployed systems
- Ensuring backward compatibility during API evolution
- Validating that implementations adhere to defined contracts
- Detecting specification drift in microservices architectures
- Preparing for API version releases or compatibility checks
- Onboarding new developers to complex specification-based systems
- Auditing compliance with interface contracts

## What I do

### 1. Specification Format Analysis
- **Parse structured specifications**: OpenAPI/Swagger, AsyncAPI, Protobuf, GraphQL schemas, RAML, API Blueprint
- **Analyze architecture specifications**: UML diagrams, C4 models, deployment manifests, infrastructure-as-code
- **Extract interface definitions**: Endpoints, methods, parameters, responses, data types, constraints
- **Validate specification syntax and semantics**: Schema validation, reference resolution, constraint checking
- **Extract behavioral specifications**: Request/response patterns, error handling, state transitions

### 2. Implementation Analysis
- **Analyze API implementations**: Route definitions, request handlers, response formatting
- **Expose interface implementations**: gRPC services, GraphQL resolvers, REST endpoints
- **Inspect data model implementations**: Database schemas, object-relational mappings, serialization formats
- **Verify architecture compliance**: Component relationships, dependency patterns, deployment configurations
- **Test behavioral compliance**: Request processing, error responses, state management

### 3. Specification-Implementation Gap Detection
- **Endpoint coverage analysis**: Specified vs. implemented endpoints
- **Parameter validation gaps**: Specified vs. accepted parameters
- **Response structure mismatches**: Specified vs. actual response formats
- **Data type inconsistencies**: Specified vs. actual data types
- **Constraint enforcement gaps**: Specified vs. enforced constraints
- **Behavioral compliance gaps**: Specified vs. actual behavior

### 4. Specialized Gap Types
- **OpenAPI compliance gaps**: Paths, operations, parameters, responses, schemas
- **Protobuf service gaps**: Service definitions, RPC methods, message formats
- **GraphQL schema gaps**: Types, queries, mutations, subscriptions, resolvers
- **Architecture compliance gaps**: Component boundaries, dependency directions, interface contracts
- **Contract evolution gaps**: Version compatibility, backward/forward compatibility

### 5. Compliance Scoring & Reporting
- **Calculate specification compliance scores**: Percentage of spec implemented correctly
- **Generate compliance reports**: Detailed gap analysis with severity ratings
- **Provide remediation guidance**: Specific fixes for each gap type
- **Track compliance trends**: Over time, across versions, between services
- **Generate compliance badges**: Ready for CI/CD pipeline integration

## Supported Specification Formats

### OpenAPI/Swagger
```yaml
analysis:
  openapi:
    version_detection: "2.0|3.0|3.1"
    gap_types:
      - missing_paths
      - missing_operations
      - parameter_mismatches
      - response_mismatches
      - schema_violations
      - security_scheme_gaps
    validation:
      - schema_validation
      - reference_resolution
      - example_consistency
```

### Protocol Buffers (Protobuf)
```proto
analysis:
  protobuf:
    service_gap_types:
      - missing_services
      - missing_rpc_methods
      - message_format_mismatches
      - streaming_mode_gaps
    message_gap_types:
      - field_missing
      - type_mismatch
      - cardinality_mismatch
      - default_value_gaps
```

### GraphQL
```graphql
analysis:
  graphql:
    schema_gap_types:
      - missing_types
      - missing_fields
      - type_mismatches
      - interface_implementation_gaps
    operation_gap_types:
      - missing_queries
      - missing_mutations
      - missing_subscriptions
      - resolver_implementation_gaps
```

### Architecture Specifications
```yaml
analysis:
  architecture:
    formats:
      - c4_models
      - uml_diagrams
      - deployment_manifests
      - infrastructure_as_code
    gap_types:
      - component_boundary_violations
      - dependency_direction_violations
      - interface_contract_violations
      - deployment_configuration_gaps
```

## Gap Classification

### API Specification Gaps

#### 1. Endpoint Coverage Gaps
**Missing Endpoints**: Specification defines endpoint not implemented  
**Extra Endpoints**: Implementation has endpoint not in specification  
**Example**: OpenAPI defines `/users/{id}` but implementation missing

#### 2. Operation Method Gaps
**Missing Methods**: Specification defines HTTP method not supported  
**Extra Methods**: Implementation supports method not in specification  
**Example**: Spec defines GET and POST, implementation also supports PUT

#### 3. Parameter Compliance Gaps
**Missing Parameters**: Required parameters not accepted  
**Extra Parameters**: Implementation accepts parameters not in spec  
**Type Mismatches**: Parameter type differs from specification  
**Example**: Spec requires `page` as integer, implementation accepts string

#### 4. Response Compliance Gaps
**Missing Status Codes**: Expected status codes not returned  
**Extra Status Codes**: Unexpected status codes returned  
**Schema Mismatches**: Response structure differs from specification  
**Example**: Spec defines 201 Created response, implementation returns 200 OK

#### 5. Schema Validation Gaps
**Data Type Mismatches**: Actual data type differs from schema  
**Constraint Violations**: Data violates schema constraints  
**Required Field Gaps**: Required fields missing or extra fields present  
**Example**: Spec requires `email` format validation, implementation doesn't validate

### Protocol Specification Gaps

#### 1. Service Implementation Gaps
**Missing Services**: Protobuf service not implemented  
**Missing RPC Methods**: Service method not implemented  
**Streaming Mode Gaps**: Unary vs. streaming implementation mismatch  
**Example**: Protobuf defines `StreamChat` method, implementation uses unary

#### 2. Message Format Gaps
**Missing Fields**: Message fields not in implementation  
**Type Mismatches**: Field type differs from specification  
**Cardinality Violations**: Required/optional/repeated mismatch  
**Example**: Protobuf defines `repeated string tags`, implementation uses single string

### GraphQL Specification Gaps

#### 1. Schema Compliance Gaps
**Missing Types**: GraphQL type not implemented  
**Missing Fields**: Type fields not implemented  
**Interface Violations**: Type doesn't implement required interface  
**Example**: GraphQL schema defines `User` type with `email` field, implementation missing

#### 2. Resolver Implementation Gaps
**Missing Resolvers**: No resolver for field or operation  
**Type Resolution Gaps**: Resolver returns wrong type  
**Argument Handling Gaps**: Resolver doesn't accept specified arguments  
**Example**: GraphQL defines `search(query: String!)` but resolver doesn't accept query

## Examples

```bash
# Analyze OpenAPI specification compliance
npm run spec-gap-analysis:openapi -- --spec openapi.yaml --implementation src/api/ --output compliance.json

# Compare Protobuf service definition with implementation
npm run spec-gap-analysis:protobuf -- --proto service.proto --implementation src/grpc/ --output gaps.md

# Validate GraphQL schema against resolvers
npm run spec-gap-analysis:graphql -- --schema schema.graphql --resolvers src/resolvers/ --output validation.yaml

# Check architecture specification compliance
npm run spec-gap-analysis:architecture -- --spec architecture.c4 --code src/ --output compliance-report.html

# Continuous compliance monitoring
npm run spec-gap-analysis:monitor -- --spec openapi.yaml --implementation src/api/ --watch --threshold 95

# Generate compliance badge
npm run spec-gap-analysis:badge -- --compliance compliance.json --output badge.svg

# Compare API versions for compatibility
npm run spec-gap-analysis:compatibility -- --spec-v1 api-v1.yaml --spec-v2 api-v2.yaml --output compatibility.md
```

## Output format

### Specification Compliance Report:
```
Specification Compliance Analysis
─────────────────────────────────
Specification: User Service API (OpenAPI 3.0.3)
Implementation: src/api/
Analysis Date: 2026-02-26
Compliance Score: 78.5%

OpenAPI Compliance Summary:
┌──────────────────────┬──────────┬──────────┬─────────────┐
│ Compliance Area      │ Specified│ Implemented │ Compliance │
├──────────────────────┼──────────┼──────────┼─────────────┤
│ Paths               │ 12       │ 10       │ 83.3%       │
│ Operations           │ 24       │ 20       │ 83.3%       │
│ Parameters           │ 89       │ 75       │ 84.3%       │
│ Responses            │ 48       │ 36       │ 75.0%       │
│ Schemas              │ 15       │ 12       │ 80.0%       │
└──────────────────────┴──────────┴──────────┴─────────────┘

Critical Gaps Found:

1. ❌ Missing Endpoint: DELETE /users/{id}
   • Specification: Required for user deletion
   • Implementation: Not found
   • Impact: Critical functionality missing
   • Compliance: 0%

2. ❌ Parameter Mismatch: GET /users
   • Specified: page (integer, required, minimum: 1)
   • Implemented: page (string, optional)
   • Impact: Type safety violation, pagination broken
   • Compliance: 40%

3. ⚠️ Response Schema Violation: POST /users
   • Specified: 201 Created with Location header
   • Implemented: 200 OK without Location header
   • Impact: REST compliance violation
   • Compliance: 60%

4. ⚠️ Missing Response Code: PUT /users/{id}
   • Specified: 404 Not Found for non-existent users
   • Implemented: Always returns 200 or 400
   • Impact: Error handling incomplete
   • Compliance: 75%

Compliance Trend:
Previous: 72% → Current: 78.5% → Target: 95%
Improvement: +6.5% (positive trend)

Remediation Priority:
1. Implement DELETE /users/{id} (critical)
2. Fix GET /users parameter types (high)
3. Align POST /users response codes (medium)
4. Add PUT /users/{id} 404 response (medium)

Estimated Effort: 3-5 days
Target Compliance: 95% by 2026-03-05
```

### Compliance JSON Output:
```json
{
  "analysis": {
    "specification": {
      "format": "OpenAPI",
      "version": "3.0.3",
      "file": "openapi.yaml",
      "paths_count": 12,
      "operations_count": 24
    },
    "implementation": {
      "location": "src/api/",
      "files_analyzed": 42,
      "endpoints_detected": 10
    },
    "compliance_score": 78.5,
    "timestamp": "2026-02-26T19:00:00Z"
  },
  "gap_analysis": {
    "paths": {
      "specified": 12,
      "implemented": 10,
      "missing": ["/users/{id}"],
      "extra": [],
      "compliance": 83.3
    },
    "operations": {
      "specified": 24,
      "implemented": 20,
      "missing": ["DELETE /users/{id}"],
      "extra": [],
      "compliance": 83.3
    },
    "parameters": {
      "specified": 89,
      "implemented": 75,
      "type_mismatches": [
        {
          "endpoint": "GET /users",
          "parameter": "page",
          "specified_type": "integer",
          "implemented_type": "string",
          "severity": "high"
        }
      ],
      "compliance": 84.3
    },
    "responses": {
      "specified": 48,
      "implemented": 36,
      "status_code_gaps": [
        {
          "endpoint": "PUT /users/{id}",
          "missing_code": 404,
          "impact": "error_handling_incomplete",
          "severity": "medium"
        }
      ],
      "compliance": 75.0
    }
  },
  "critical_gaps": [
    {
      "id": "gap-api-001",
      "type": "missing_operation",
      "endpoint": "/users/{id}",
      "method": "DELETE",
      "severity": "critical",
      "impact": "user_deletion_missing",
      "remediation": "Implement DELETE handler with proper authorization",
      "effort": "1 day",
      "priority": 1
    }
  ],
  "compliance_trend": {
    "previous_score": 72.0,
    "current_score": 78.5,
    "change": 6.5,
    "direction": "improving",
    "velocity": 2.2
  }
}
```

### Compliance Badge (SVG):
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="120" height="20">
  <linearGradient id="bg" x2="0" y2="1">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect rx="3" width="120" height="20" fill="#555"/>
  <rect rx="3" x="80" width="40" height="20" fill="#4c1"/>
  <rect rx="3" width="120" height="20" fill="url(#bg)"/>
  <g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="5" y="14" fill="#010101" fill-opacity=".3">Compliance</text>
    <text x="5" y="13">Compliance</text>
    <text x="85" y="14" fill="#010101" fill-opacity=".3">78.5%</text>
    <text x="85" y="13">78.5%</text>
  </g>
</svg>
```

## Notes

- **Contract-first development benefits** from early gap detection - catch issues before implementation
- **Automated compliance checking** enables continuous validation in CI/CD pipelines
- **Specification evolution tracking** helps maintain backward compatibility
- **Compliance scores provide measurable quality metrics** for API governance
- **Different specification formats require specialized analysis** - one-size-fits-all doesn't work
- **Implementation completeness is different from correctness** - both matter for compliance
- **Specification gaps often indicate deeper issues** - design flaws, misunderstandings, or shortcuts
- **Regular compliance analysis prevents specification drift** - especially in microservices architectures
- **Compliance thresholds should be project-specific** - critical APIs need higher standards
- **Remediation should prioritize based on impact** - security and critical functionality first
- **Document why gaps exist** - sometimes intentional deviations are valid
- **Use compliance analysis proactively** - not just for problem detection but for quality improvement
- **Integrate with API lifecycle management** - from design through deprecation
- **Share compliance reports with stakeholders** - developers, product managers, consumers