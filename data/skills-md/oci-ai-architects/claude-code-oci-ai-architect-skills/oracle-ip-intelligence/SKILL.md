---
name: Oracle IP Intelligence
description: AI-powered intellectual property analysis patterns for enterprise innovation protection
version: 1.0.0
keywords: [oracle, oci, patent, ip, intellectual-property, prior-art, innovation]
triggers:
  - "prior art"
  - "patent search"
  - "freedom to operate"
  - "ip analysis"
  - "innovation protection"
---

# Oracle IP Intelligence Skill

## Purpose

Transform AI coding assistants into IP-aware innovation partners. Combines OCI GenAI, Database 26ai Vector + Graph, and Document Understanding for comprehensive intellectual property analysis.

## Cross-Platform Compatibility

This skill is designed for **universal AI coding assistant integration**:

| Platform | Integration | Status |
|----------|-------------|--------|
| Claude Code | Native skill | ✅ Primary |
| Cline / Oracle Code Assistant | .cline rules | ✅ Supported |
| GitHub Copilot | Custom instructions | 🔜 Planned |
| Cursor | .cursorrules | 🔜 Planned |
| Gemini Code Assist | Context file | 🔜 Planned |

## When to Use

**Activate when:**
- Reviewing code for potential patentability
- Searching prior art before R&D investment
- Analyzing competitive patent landscapes
- Generating innovation documentation
- Checking freedom-to-operate for new features

## Architecture Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                    IP Intelligence Platform                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Prior Art    │  │ Claim        │  │ Freedom to       │  │
│  │ Agent        │  │ Analyzer     │  │ Operate Agent    │  │
│  │              │  │              │  │                  │  │
│  │ - Semantic   │  │ - Element    │  │ - Risk scoring   │  │
│  │   search     │  │   extraction │  │ - Workaround     │  │
│  │ - Citation   │  │ - Overlap    │  │   suggestions    │  │
│  │   network    │  │   detection  │  │ - Export legal   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
│                           │                                  │
│              ┌────────────┴────────────┐                    │
│              │  Oracle Database 26ai    │                    │
│              │  Vector + Graph + SQL    │                    │
│              │  ───────────────────     │                    │
│              │  • Patent embeddings     │                    │
│              │  • Citation graph        │                    │
│              │  • Claim mapping         │                    │
│              └──────────────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Model Selection for IP Tasks

| Task | Recommended Model | Why |
|------|-------------------|-----|
| Patent semantic search | Cohere Embed + Command R | Purpose-built RAG, EU residency |
| Claim extraction | Gemini 2.5 Flash | Multimodal doc processing |
| Legal risk analysis | Cohere Command A Reasoning | Multi-step reasoning |
| Citation graph analysis | Database 26ai Graph | Native graph traversal |
| Innovation summarization | Llama 4 Maverick | Long context (1M tokens) |

## Integration with Code Development

### Pre-Commit IP Check
```python
from oci_ip_intelligence import IPAnalyzer

def pre_commit_ip_hook(code_changes: str) -> dict:
    """
    Analyze code changes for IP implications.
    Runs before commit to catch innovation opportunities.
    """
    analyzer = IPAnalyzer(
        compartment_id=os.environ["OCI_COMPARTMENT_ID"],
        patent_collection="enterprise_patents"
    )
    
    # Extract technical concepts from code
    concepts = analyzer.extract_concepts(code_changes)
    
    # Search prior art
    prior_art = analyzer.search_prior_art(
        concepts=concepts,
        search_mode="hybrid",  # Vector + Graph
        date_range="last_10_years"
    )
    
    # Assess novelty score
    novelty = analyzer.assess_novelty(concepts, prior_art)
    
    return {
        "novelty_score": novelty.score,
        "recommendation": novelty.action,  # "document", "review", "proceed"
        "related_patents": prior_art[:5],
        "innovation_summary": novelty.summary
    }
```

### IDE Integration Pattern
```javascript
// VS Code / Cursor extension pattern
const ipCheck = async (document) => {
  const analysis = await fetch('/api/ip-check', {
    method: 'POST',
    body: JSON.stringify({
      code: document.getText(),
      language: document.languageId,
      context: getProjectContext()
    })
  });
  
  if (analysis.novelty_score > 0.7) {
    showNotification("🎯 Potential innovation detected! Consider documenting.");
  }
  
  if (analysis.risk_score > 0.5) {
    showWarning("⚠️ Similar patents found. Review before proceeding.");
  }
};
```

## Chemical Industry Specialization

For chemistry/pharma applications (ChemPatent pattern):

| Capability | OCI Services | Specialization |
|------------|--------------|----------------|
| Structure Search | OCI Vision + Custom Model | SMILES, InChI notation |
| Compound Detection | OCI Document Understanding | Named entity extraction |
| Reaction Analysis | Cohere Command A | Chemical equation parsing |
| Formulation IP | Database 26ai Vector | Similarity search |

## OCI Services Required

| Service | Purpose | Tier |
|---------|---------|------|
| OCI Generative AI | Embeddings, reasoning | Standard |
| Autonomous Database 26ai | Vector + Graph storage | Advanced |
| OCI Document Understanding | Patent PDF processing | Standard |
| OCI Object Storage | Patent corpus | Standard |
| OCI Functions | Serverless IP checks | Standard |

## Reference Implementations

### Working Prototypes
- `projects/Patent AI Agent/chemical-industry/workbench.html` - Analyst workflow
- `projects/Patent AI Agent/chemical-industry/search.html` - Structure search
- `projects/Patent AI Agent/portal/index.html` - Executive showcase

### API Endpoints (Reference)
```
POST /api/v1/prior-art/search
POST /api/v1/claims/analyze
POST /api/v1/fto/check
GET  /api/v1/patents/{id}/citations
POST /api/v1/innovation/document
```

---

## Cross-Platform Skills Vision

This skill is part of the **Unified AI Coding Skills** initiative:

```
┌─────────────────────────────────────────────────────────────────┐
│              UNIFIED SKILLS ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Claude Code │  │   Cline     │  │   Cursor    │   ...more    │
│  │   Skills    │  │   Rules     │  │   Rules     │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          │                                       │
│              ┌───────────┴───────────┐                          │
│              │   Skill Translator    │                          │
│              │   (Format Adapter)    │                          │
│              └───────────┬───────────┘                          │
│                          │                                       │
│              ┌───────────┴───────────┐                          │
│              │  Universal Skill Spec │                          │
│              │   (Markdown + YAML)   │                          │
│              └───────────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

*Part of OCI AI Architect Skills - Building the future of IP-aware development*
*Reference: oracle-devrel/technology-engineering/ai-solutions/ip-intelligence*
