---
name: chuukese-language-processing
description: Specialized processing for Chuukese language text including tokenization, accent handling, cultural context preservation, and language-specific patterns. Use when working with Chuukese text, translation tasks, or when building language models for this Micronesian language.
---

# Chuukese Language Processing

## Overview

A specialized skill for processing Chuukese language text, focusing on proper handling of accented characters, cultural context preservation, and language-specific linguistic patterns. Essential for building accurate translation systems and language models for this low-resource Micronesian language.

## Capabilities

- **Accent Character Normalization**: Proper handling of Chuukese diacritical marks (á, é, í, ó, ú, ā, ē, ī, ō, ū)
- **Cultural Context Preservation**: Maintain traditional concepts and cultural nuances
- **Phonetic Pattern Recognition**: Understanding of Chuukese sound patterns and phonology
- **Morphological Analysis**: Basic word formation and grammatical structure recognition
- **Dictionary Integration**: Seamless integration with Chuukese-English dictionaries
- **Translation Quality Assessment**: Validation of translation accuracy and cultural appropriateness

## Core Components

### 1. Chuukese Text Normalization

```python
import re
import unicodedata

class ChuukeseTextProcessor:
    def __init__(self):
        self.accent_patterns = {
            'acute': ['á', 'é', 'í', 'ó', 'ú'],
            'macron': ['ā', 'ē', 'ī', 'ō', 'ū'],
            'base': ['a', 'e', 'i', 'o', 'u']
        }
        
        self.normalize_map = {
            'á': 'á', 'à': 'á', 'â': 'á',  # Standardize to acute
            'ā': 'ā', 'ă': 'ā',           # Standardize to macron
            'é': 'é', 'è': 'é', 'ê': 'é',
            'ē': 'ē', 'ĕ': 'ē',
            'í': 'í', 'ì': 'í', 'î': 'í',
            'ī': 'ī', 'ĭ': 'ī',
            'ó': 'ó', 'ò': 'ó', 'ô': 'ó',
            'ō': 'ō', 'ŏ': 'ō',
            'ú': 'ú', 'ù': 'ú', 'û': 'ú',
            'ū': 'ū', 'ŭ': 'ū'
        }
    
    def normalize_chuukese_text(self, text):
        """Normalize Chuukese text with proper accent handling"""
        # First apply Unicode normalization
        normalized = unicodedata.normalize('NFC', text)
        
        # Then apply Chuukese-specific normalization
        for variant, standard in self.normalize_map.items():
            normalized = normalized.replace(variant, standard)
        
        return normalized
```

### 2. Cultural Context Recognition

```python
class ChuukeseCulturalProcessor:
    def __init__(self):
        self.cultural_concepts = {
            'family_terms': ['semei', 'jinej', 'seme', 'jina', 'pwis', 'pwisen'],
            'traditional_items': ['emon', 'uruf', 'nous', 'ruk', 'chomw'],
            'respect_terms': ['oupwe', 'kose mochen', 'tipeew', 'sokkun'],
            'time_concepts': ['ranem', 'ekis', 'ngang', 'pwong'],
            'spatial_terms': ['met', 'ese', 'won', 'ifa']
        }
    
    def detect_cultural_context(self, text):
        """Detect cultural context indicators in Chuukese text"""
        context = {
            'cultural_density': 0,
            'respect_level': 'casual',
            'traditional_concepts': [],
            'formality_indicators': []
        }
        
        for category, terms in self.cultural_concepts.items():
            found_terms = [term for term in terms if term in text.lower()]
            if found_terms:
                context['traditional_concepts'].extend(found_terms)
                context['cultural_density'] += len(found_terms)
        
        return context
```

## Usage Examples

### Basic Text Processing

```python
# Initialize processor
processor = ChuukeseTextProcessor()

# Process Chuukese text
text = "Kopwe pwan chomong ngonuk ekkewe chon Chuuk"
normalized = processor.normalize_chuukese_text(text)
words = processor.extract_chuukese_words(text)

print(f"Normalized: {normalized}")
print(f"Words: {words}")
```

### Cultural Context Analysis

```python
# Analyze cultural context
cultural_processor = ChuukeseCulturalProcessor()
context = cultural_processor.detect_cultural_context(text)

print(f"Cultural density: {context['cultural_density']}")
print(f"Traditional concepts: {context['traditional_concepts']}")
```

## Best Practices

### Text Processing

1. **Always normalize**: Apply Unicode and Chuukese-specific normalization
2. **Preserve accents**: Maintain diacritical marks for accurate meaning
3. **Context awareness**: Consider cultural and social context
4. **Quality validation**: Verify processing with native speaker input

### Cultural Sensitivity

1. **Respect traditions**: Honor traditional concepts and practices
2. **Appropriate register**: Use proper formality levels
3. **Community involvement**: Engage with Chuukese language community
4. **Continuous learning**: Stay updated with language evolution

## Dependencies

- `unicodedata`: Unicode normalization
- `re`: Regular expression pattern matching
- `difflib`: Fuzzy string matching
- `csv`: Dictionary file processing


## Multi-Language Document Processing

When documents contain a mix of Chuukese and English (or other languages), detect language at the
paragraph/sentence level before applying language-specific normalisation.

```python
from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        # 'id' (Indonesian) is the closest code langdetect returns for Chuukese
        return 'chuukese' if lang in ('id', 'ms') else lang
    except Exception:
        # Fall back to accent-pattern heuristic
        return 'chuukese' if re.search(r'[áéíóú]', text) else 'unknown'
```

Use the accent-pattern normalisation from this skill's main section after language detection.
Documents that are purely English (e.g., brochure English side) should skip Chuukese normalisation.
