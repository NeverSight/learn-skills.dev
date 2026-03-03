---
name: gdpr-compliance
description: GDPR compliance planning including lawful bases, data subject rights, DPIA, and implementation patterns
allowed-tools: Read, Glob, Grep, Write, Edit, Task
---

# GDPR Compliance Planning

Comprehensive guidance for General Data Protection Regulation compliance before development begins.

## When to Use This Skill

- Planning systems that process EU residents' personal data
- Designing consent management and preference centers
- Implementing data subject rights (access, erasure, portability)
- Conducting Data Protection Impact Assessments (DPIA)
- Defining data processing agreements and controller/processor relationships

## GDPR Fundamentals

### The 7 Principles

| Principle | Description | Implementation Focus |
|-----------|-------------|---------------------|
| **Lawfulness, Fairness, Transparency** | Valid legal basis, fair processing, clear privacy notices | Consent flows, privacy policies |
| **Purpose Limitation** | Collect for specified, explicit purposes | Purpose tracking, use restriction |
| **Data Minimization** | Adequate, relevant, limited to purpose | Field-level justification |
| **Accuracy** | Keep data accurate and up to date | Update mechanisms, verification |
| **Storage Limitation** | Keep only as long as necessary | Retention policies, auto-deletion |
| **Integrity and Confidentiality** | Appropriate security measures | Encryption, access control |
| **Accountability** | Demonstrate compliance | Audit logs, documentation |

### Lawful Bases for Processing

```text
1. Consent - Freely given, specific, informed, unambiguous
2. Contract - Necessary for contract performance
3. Legal Obligation - Required by law
4. Vital Interests - Protect someone's life
5. Public Task - Official authority/public interest
6. Legitimate Interest - Balanced against data subject rights
```

**Legitimate Interest Assessment (LIA):**

1. Purpose test: Is there a legitimate interest?
2. Necessity test: Is processing necessary for that interest?
3. Balancing test: Do subject's interests override?

## Data Subject Rights Implementation

### Rights Checklist

| Right | Description | Response Time | Implementation |
|-------|-------------|---------------|----------------|
| Access | Copy of personal data | 1 month | Export endpoint |
| Rectification | Correct inaccurate data | 1 month | Update endpoint |
| Erasure ("Right to be Forgotten") | Delete personal data | 1 month | Deletion pipeline |
| Restrict Processing | Limit use of data | 1 month | Processing flags |
| Data Portability | Machine-readable export | 1 month | JSON/CSV export |
| Object | Stop processing | Without undue delay | Opt-out mechanism |
| Automated Decision-Making | Human review of decisions | Varies | Review queue |

### .NET Implementation Patterns

```csharp
// Data Subject Request Handling
public interface IDataSubjectRequestHandler
{
    Task<DataExport> HandleAccessRequest(Guid subjectId, CancellationToken ct);
    Task HandleErasureRequest(Guid subjectId, ErasureScope scope, CancellationToken ct);
    Task<PortableData> HandlePortabilityRequest(Guid subjectId, string format, CancellationToken ct);
}

public class DataSubjectRequestService : IDataSubjectRequestHandler
{
    private readonly IPersonalDataLocator _dataLocator;
    private readonly IAuditLogger _auditLogger;
    private readonly TimeProvider _timeProvider;

    public async Task<DataExport> HandleAccessRequest(Guid subjectId, CancellationToken ct)
    {
        await _auditLogger.LogRequestReceived(subjectId, "Access", _timeProvider.GetUtcNow());

        var locations = await _dataLocator.LocateAllPersonalData(subjectId, ct);
        var export = new DataExport
        {
            SubjectId = subjectId,
            GeneratedAt = _timeProvider.GetUtcNow(),
            Categories = new List<DataCategory>()
        };

        foreach (var location in locations)
        {
            var data = await location.ExtractData(ct);
            export.Categories.Add(new DataCategory
            {
                Name = location.CategoryName,
                Purpose = location.ProcessingPurpose,
                LawfulBasis = location.LawfulBasis,
                RetentionPeriod = location.RetentionPolicy,
                Data = data
            });
        }

        await _auditLogger.LogRequestCompleted(subjectId, "Access", _timeProvider.GetUtcNow());
        return export;
    }

    public async Task HandleErasureRequest(Guid subjectId, ErasureScope scope, CancellationToken ct)
    {
        // Check for legal holds or retention requirements
        var blocks = await CheckErasureBlocks(subjectId, ct);
        if (blocks.Any())
        {
            throw new ErasureBlockedException(blocks);
        }

        var locations = await _dataLocator.LocateAllPersonalData(subjectId, ct);

        foreach (var location in locations)
        {
            if (scope.IncludesCategory(location.CategoryName))
            {
                // Soft delete with scheduled hard delete
                await location.MarkForDeletion(_timeProvider.GetUtcNow().AddDays(30), ct);
            }
        }

        await _auditLogger.LogErasureInitiated(subjectId, scope, _timeProvider.GetUtcNow());
    }
}
```

### Consent Management

```csharp
// Consent tracking with granular purposes
public class ConsentRecord
{
    public Guid SubjectId { get; init; }
    public string Purpose { get; init; } = string.Empty;
    public bool IsGranted { get; init; }
    public DateTimeOffset Timestamp { get; init; }
    public string ConsentMechanism { get; init; } = string.Empty; // e.g., "WebForm", "API"
    public string ConsentVersion { get; init; } = string.Empty; // Version of consent text
    public string? WithdrawalTimestamp { get; set; }
}

public interface IConsentManager
{
    Task RecordConsent(ConsentRecord consent, CancellationToken ct);
    Task WithdrawConsent(Guid subjectId, string purpose, CancellationToken ct);
    Task<bool> HasValidConsent(Guid subjectId, string purpose, CancellationToken ct);
    Task<IReadOnlyList<ConsentRecord>> GetConsentHistory(Guid subjectId, CancellationToken ct);
}

public class GdprConsentManager : IConsentManager
{
    private readonly IConsentRepository _repository;
    private readonly IEventPublisher _events;

    public async Task<bool> HasValidConsent(Guid subjectId, string purpose, CancellationToken ct)
    {
        var latest = await _repository.GetLatestConsent(subjectId, purpose, ct);

        if (latest is null)
            return false;

        if (latest.WithdrawalTimestamp is not null)
            return false;

        // Check if consent version is still current
        var currentVersion = await _repository.GetCurrentConsentVersion(purpose, ct);
        if (latest.ConsentVersion != currentVersion)
        {
            // Consent was given under old terms - needs re-consent
            return false;
        }

        return latest.IsGranted;
    }
}
```

## Data Protection Impact Assessment (DPIA)

### When DPIA is Required

DPIA is mandatory when processing is likely to result in high risk:

- Systematic and extensive profiling with significant effects
- Large-scale processing of special category data
- Systematic monitoring of public areas
- New technologies with unknown privacy impact
- Automated decision-making with legal/similar effects
- Large-scale processing of children's data

### DPIA Template Structure

```markdown
## 1. Description of Processing
- Nature: What will you do with the data?
- Scope: How much data, how many subjects, geographic area?
- Context: Internal/external factors affecting expectations?
- Purpose: What are you trying to achieve?

## 2. Necessity and Proportionality
- Lawful basis and justification
- Purpose limitation assessment
- Data minimization measures
- Data quality approach
- Storage limitation policy

## 3. Risk Assessment

### Risks to Individuals
| Risk | Likelihood | Severity | Score | Mitigation |
|------|------------|----------|-------|------------|
| Unauthorized access | Medium | High | 6 | Encryption, MFA |
| Data breach | Low | Critical | 4 | Monitoring, IR plan |
| Inaccurate profiling | Medium | Medium | 4 | Human review |

### Residual Risk
[After mitigations applied]

## 4. Consultation
- DPO advice obtained: [Date]
- Supervisory authority consulted: [If required]
- Data subject views considered: [How]

## 5. Sign-Off
| Role | Name | Approval | Date |
|------|------|----------|------|
| Project Owner | | [ ] | |
| DPO | | [ ] | |
| CISO | | [ ] | |
```

### Risk Scoring Matrix

```text
         SEVERITY
         Low(1)  Medium(2)  High(3)  Critical(4)
L   High(4)    4      8         12       16
I   Med(3)     3      6          9       12
K   Low(2)     2      4          6        8
E   V.Low(1)   1      2          3        4
```

**Thresholds:**

- 1-4: Acceptable risk
- 5-8: Mitigations required
- 9-12: Senior approval required
- 13+: Consult supervisory authority

## Privacy by Design Checklist

### Architecture Phase

- [ ] Data flows documented with personal data highlighted
- [ ] Purpose for each data element defined
- [ ] Lawful basis identified per purpose
- [ ] Retention periods defined per category
- [ ] Access control requirements specified
- [ ] Encryption requirements defined
- [ ] Pseudonymization opportunities identified

### Development Phase

- [ ] Consent collection implemented correctly
- [ ] Data subject rights endpoints created
- [ ] Audit logging captures processing activities
- [ ] Data retention automation implemented
- [ ] Encryption at rest and in transit
- [ ] Input validation prevents excess collection
- [ ] Error messages don't leak personal data

### Testing Phase

- [ ] Consent flows tested (grant, withdraw, re-consent)
- [ ] All DSR endpoints functional
- [ ] Retention automation verified
- [ ] Access controls tested
- [ ] Audit logs complete and accurate
- [ ] Penetration testing for data exposure

## Record of Processing Activities (ROPA)

### Article 30 Requirements

Controllers must maintain records of:

```yaml
Processing Activity: Customer Account Management
Controller: [Organization Name]
DPO Contact: dpo@example.com
Purposes:
  - Account authentication
  - Order fulfillment
  - Customer support
Categories of Data Subjects:
  - Customers
  - Prospective customers
Categories of Personal Data:
  - Name, email, phone
  - Address
  - Order history
  - Payment tokens (not card numbers)
Recipients:
  - Payment processor (Stripe)
  - Shipping provider (FedEx)
  - Customer support platform (Zendesk)
International Transfers:
  - Stripe Inc. (US) - SCCs
  - None to third countries without safeguards
Retention:
  - Active account: Duration of relationship
  - Closed account: 7 years (legal requirement)
Security Measures:
  - TLS 1.3 in transit
  - AES-256 at rest
  - Role-based access control
  - Regular access reviews
```

## International Data Transfers

### Transfer Mechanisms Post-Schrems II

| Mechanism | Use Case | Requirements |
|-----------|----------|--------------|
| **Adequacy Decision** | EU-approved countries | None additional |
| **Standard Contractual Clauses (SCCs)** | Most common | TIA required |
| **Binding Corporate Rules** | Intra-group transfers | Supervisory approval |
| **Derogations (Art. 49)** | Occasional transfers | Limited scope |

### Transfer Impact Assessment (TIA)

```markdown
## Transfer Impact Assessment

### 1. Transfer Details
- Exporter: [EU entity]
- Importer: [Third country entity]
- Countries: [List]
- Data types: [Categories]
- Transfer mechanism: [SCCs/BCRs/etc.]

### 2. Third Country Assessment
- Laws requiring disclosure to authorities
- Surveillance legislation
- Rule of law / judicial independence
- Practical access by authorities

### 3. Supplementary Measures
- Technical: [Encryption, pseudonymization]
- Contractual: [Additional clauses]
- Organizational: [Policies, training]

### 4. Conclusion
- Risk level: [Acceptable/Requires mitigation/Unacceptable]
- Decision: [Proceed/Modify/Suspend]
```

## Cross-References

- **CCPA/CPRA**: See similar concepts (disclosure, deletion, opt-out)
- **AI Governance**: `ai-governance` skill for AI-specific requirements
- **Security Frameworks**: `security-frameworks` for technical controls
- **Data Classification**: `data-classification` for sensitivity levels

## Resources

- [GDPR Full Text](https://gdpr-info.eu/)
- [EDPB Guidelines](https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en)
- [ICO GDPR Guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
