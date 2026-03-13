---
name: Entity Extractor
slug: entity-extractor
description: Extract named entities from text with high accuracy and customization
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "extract entities"
  - "named entity recognition"
  - "NER"
  - "entity extraction"
  - "information extraction"
tags:
  - NER
  - entity-extraction
  - information-extraction
  - NLP
  - text-mining
---

# Entity Extractor

The Entity Extractor skill guides you through implementing named entity recognition (NER) systems that identify and classify entities in text. From people and organizations to domain-specific entities like products, medical terms, or financial instruments, this skill covers extraction approaches from simple pattern matching to advanced neural models.

Entity extraction is a foundational NLP task that powers applications from search engines to knowledge graphs. Getting it right requires understanding your domain, choosing appropriate techniques, and handling the inherent ambiguity in natural language.

Whether you need to extract standard entity types, define custom entities for your domain, or build relation extraction on top of entity recognition, this skill ensures your extraction pipeline is accurate and maintainable.

## Core Workflows

### Workflow 1: Choose Extraction Approach
1. **Define** target entities:
   - Standard types: PERSON, ORG, LOCATION, DATE, MONEY
   - Domain-specific: PRODUCT, SYMPTOM, GENE, CONTRACT
   - Relations: connections between entities
2. **Assess** available resources:
   - Labeled training data
   - Domain expertise
   - Compute constraints
3. **Select** approach:
   | Approach | Training Data | Accuracy | Speed | Customization |
   |----------|---------------|----------|-------|---------------|
   | spaCy (pre-trained) | None | Good | Very fast | Limited |
   | Rule-based | None | Variable | Fast | High |
   | Fine-tuned BERT | 100s-1000s | Excellent | Medium | Full |
   | LLM (zero-shot) | None | Good | Slow | Prompt-based |
   | LLM (few-shot) | Few examples | Very good | Slow | Prompt-based |
4. **Plan** implementation and evaluation

### Workflow 2: Implement Entity Extraction Pipeline
1. **Set up** extraction:
   ```python
   import spacy

   class EntityExtractor:
       def __init__(self, model="en_core_web_trf"):
           self.nlp = spacy.load(model)

       def extract(self, text):
           doc = self.nlp(text)
           entities = []
           for ent in doc.ents:
               entities.append({
                   "text": ent.text,
                   "type": ent.label_,
                   "start": ent.start_char,
                   "end": ent.end_char,
                   "confidence": getattr(ent, "confidence", None)
               })
           return entities

       def extract_batch(self, texts):
           docs = list(self.nlp.pipe(texts))
           return [self.extract_from_doc(doc) for doc in docs]
   ```
2. **Post-process** entities:
   - Normalize variations (IBM vs I.B.M.)
   - Resolve abbreviations
   - Link to knowledge base
3. **Validate** extraction quality
4. **Handle** edge cases

### Workflow 3: Build Custom Entity Recognizer
1. **Prepare** training data:
   ```python
   # Format for spaCy training
   TRAIN_DATA = [
       ("Apple released the new iPhone today.", {
           "entities": [(0, 5, "ORG"), (24, 30, "PRODUCT")]
       }),
       ("Dr. Smith prescribed metformin for diabetes.", {
           "entities": [(0, 9, "PERSON"), (21, 30, "DRUG"), (35, 43, "CONDITION")]
       })
   ]
   ```
2. **Configure** training:
   ```python
   # spaCy config for NER training
   config = {
       "training": {
           "optimizer": {"learn_rate": 0.001},
           "batch_size": {"@schedules": "compounding", "start": 4, "stop": 32}
       },
       "components": {
           "ner": {
               "factory": "ner",
               "model": {"@architectures": "spacy.TransitionBasedParser"}
           }
       }
   }
   ```
3. **Train** model:
   ```bash
   python -m spacy train config.cfg --output ./models --paths.train ./train.spacy --paths.dev ./dev.spacy
   ```
4. **Evaluate** on held-out data
5. **Iterate** based on errors

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Extract entities | "Extract entities from [text]" |
| Choose NER model | "Best NER for [domain]" |
| Custom entities | "Train custom entity recognizer" |
| Evaluate NER | "Evaluate entity extraction quality" |
| Handle ambiguity | "Resolve ambiguous entities" |
| Entity linking | "Link entities to knowledge base" |

## Best Practices

- **Start with Pre-trained**: Don't train from scratch unnecessarily
  - spaCy, Hugging Face, and cloud APIs cover common entities
  - Test pre-trained models first
  - Fine-tune only when needed

- **Define Clear Guidelines**: Entity boundaries are ambiguous
  - "Dr. John Smith" - one entity or two?
  - "New York Times" - ORG or GPE?
  - Create and follow consistent annotation guidelines

- **Handle Nested Entities**: Some entities contain others
  - "Bank of America headquarters" (ORG inside LOCATION)
  - Decide on nesting strategy upfront
  - Some models support flat only; others handle nested

- **Normalize Extracted Entities**: Raw text has variations
  - "IBM", "I.B.M.", "International Business Machines"
  - Canonicalize to standard form
  - Link to knowledge base IDs when possible

- **Evaluate Granularly**: Aggregate metrics hide issues
  - Report precision/recall per entity type
  - Analyze error patterns
  - Test on edge cases explicitly

- **Consider Context Window**: Models have context limits
  - Long documents may need chunking
  - Preserve context across chunks when possible
  - Re-run on boundaries if entities might span

## Advanced Techniques

### LLM-Based Entity Extraction
Use language models for flexible extraction:
```python
def llm_extract_entities(text, entity_types):
    prompt = f"""Extract named entities from the following text.

Text: "{text}"

Entity types to extract:
{chr(10).join(f"- {t}: {desc}" for t, desc in entity_types.items())}

Return a JSON array of entities:
[{{"text": "entity text", "type": "ENTITY_TYPE", "start": 0, "end": 10}}]

Only include entities that clearly match the specified types.
"""

    response = llm.complete(prompt, response_format={"type": "json_object"})
    return json.loads(response)["entities"]

# Example usage
entity_types = {
    "COMPANY": "Business organizations",
    "PRODUCT": "Commercial products or services",
    "PERSON": "Individual people's names"
}
entities = llm_extract_entities(text, entity_types)
```

### Hybrid Rule + ML Approach
Combine patterns with neural extraction:
```python
class HybridExtractor:
    def __init__(self):
        self.ml_extractor = spacy.load("en_core_web_trf")
        self.patterns = load_pattern_rules()

    def extract(self, text):
        # ML extraction
        ml_entities = self.ml_extractor(text).ents

        # Pattern-based extraction
        pattern_entities = apply_patterns(text, self.patterns)

        # Merge with priority rules
        merged = merge_entities(
            ml_entities,
            pattern_entities,
            priority="pattern"  # Patterns override ML when overlap
        )

        return merged

    def add_pattern(self, pattern, entity_type):
        """Add domain-specific pattern."""
        self.patterns.append({
            "pattern": pattern,
            "type": entity_type
        })
```

### Entity Linking
Connect extracted entities to knowledge bases:
```python
def link_entity(entity_text, entity_type, knowledge_base):
    """
    Link extracted entity to canonical entry in knowledge base.
    """
    # Generate candidates
    candidates = knowledge_base.search(
        query=entity_text,
        type_filter=entity_type,
        limit=10
    )

    if not candidates:
        return {"entity": entity_text, "linked": None}

    # Score candidates
    scored = []
    for candidate in candidates:
        score = compute_linking_score(
            entity_text,
            candidate.name,
            candidate.aliases
        )
        scored.append((candidate, score))

    # Select best match
    best = max(scored, key=lambda x: x[1])

    if best[1] > LINKING_THRESHOLD:
        return {
            "entity": entity_text,
            "linked": best[0].id,
            "canonical_name": best[0].name,
            "confidence": best[1]
        }
    else:
        return {"entity": entity_text, "linked": None}
```

### Relation Extraction
Extract relationships between entities:
```python
def extract_relations(text, entities):
    """
    Given extracted entities, find relations between them.
    """
    prompt = f"""Given this text and extracted entities, identify relationships.

Text: "{text}"

Entities found:
{json.dumps(entities, indent=2)}

Identify relationships between entities. Return JSON:
[{{
    "subject": "entity text",
    "relation": "relationship type",
    "object": "entity text",
    "confidence": 0.9
}}]

Common relation types: WORKS_FOR, LOCATED_IN, FOUNDED, ACQUIRED, PARTNER_OF
"""

    response = llm.complete(prompt)
    return json.loads(response)
```

### Active Learning for NER
Efficiently improve extraction with targeted labeling:
```python
def active_learning_sample(unlabeled_texts, model, n_samples=100):
    """
    Select texts that would be most valuable to label.
    """
    uncertainties = []

    for text in unlabeled_texts:
        doc = model(text)
        # Calculate uncertainty (various strategies)
        uncertainty = calculate_ner_uncertainty(doc)
        uncertainties.append((text, uncertainty))

    # Select most uncertain
    uncertainties.sort(key=lambda x: x[1], reverse=True)
    return [text for text, _ in uncertainties[:n_samples]]

def calculate_ner_uncertainty(doc):
    """
    Calculate uncertainty based on entity confidence scores.
    """
    if not doc.ents:
        return 0.5  # No entities - medium uncertainty

    confidences = [ent._.confidence for ent in doc.ents if hasattr(ent._, "confidence")]
    if not confidences:
        return 0.5

    # High uncertainty = low confidence entities
    return 1 - min(confidences)
```

## Common Pitfalls to Avoid

- Inconsistent annotation guidelines leading to noisy training data
- Not handling entity boundary ambiguity (where does entity end?)
- Ignoring nested or overlapping entities when they matter
- Training on small datasets without augmentation
- Not normalizing entities before downstream use
- Assuming pre-trained models work on your domain without testing
- Not evaluating per-entity-type performance
- Forgetting about entity linking for disambiguation
