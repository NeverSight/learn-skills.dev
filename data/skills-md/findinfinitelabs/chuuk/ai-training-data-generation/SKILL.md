---
name: ai-training-data-generation
description: Generate high-quality training datasets from documents, text corpora, EPUBs, and structured content. Use when creating AI training data from dictionaries, Bible EPUBs, brochures, or when generating examples for machine learning models. Optimized for low-resource languages and domain-specific knowledge extraction. Supports parallel corpus extraction from NWT Bible EPUBs.
---

# AI Training Data Generation

## Overview

A comprehensive skill for automatically generating high-quality training datasets from documents, text corpora, and structured content. Optimized for low-resource languages, dictionary content, and domain-specific knowledge extraction.

**Key Sources**: Dictionary databases, Bible EPUBs (NWT), JW brochures, parallel text corpora

## Capabilities

- **Multi-strategy Generation**: Dictionary pairs, contextual definitions, completion tasks, classification examples
- **Quality Filtering**: Confidence scoring, duplicate removal, and content validation
- **Format Flexibility**: Support for multiple AI training formats (JSONL, HuggingFace, Ollama, OpenAI)
- **Language Awareness**: Multi-language support with special handling for accented characters
- **Scalable Processing**: Generate thousands of examples from large documents
- **Balance Management**: Ensure dataset diversity and prevent category imbalance
- **EPUB Processing**: Extract parallel verses from Bible EPUBs for translation training
- **Sentence Alignment**: Align parallel sentences from bilingual documents

## Core Strategies

### 1. Dictionary Pair Extraction

Extract word-definition pairs from structured and semi-structured text.

**Detection Patterns**:

- Separator-based: `word – definition`, `term: meaning`
- Linguistic indicators: `means`, `is defined as`, `refers to`
- Structural cues: Indentation, formatting, list structures
- Context analysis: Surrounding text for validation

### 2. Bible EPUB Parallel Corpus Extraction

Extract aligned verse pairs from Chuukese and English NWT Bible EPUBs.

```python
from ebooklib import epub
from src.utils.nwt_epub_parser import NWTEpubParser

class BibleTrainingDataExtractor:
    """
    Extract parallel training data from NWT Bible EPUBs.
    Aligns verses between Chuukese (nwt_TE.epub) and English (nwt_E.epub).
    """
    
    def __init__(self, chuukese_epub_path: str, english_epub_path: str):
        self.chk_parser = NWTEpubParser(chuukese_epub_path)
        self.en_parser = NWTEpubParser(english_epub_path)
    
    def extract_parallel_verses(
        self, 
        books: list = None,
        min_verse_length: int = 10
    ) -> list:
        """
        Extract aligned verse pairs for training.
        
        Args:
            books: List of book names to extract (None = all)
            min_verse_length: Minimum characters per verse
        
        Returns:
            List of {'chuukese': str, 'english': str, 'reference': str}
        """
        parallel_pairs = []
        
        # Get list of books
        if books is None:
            books = self.chk_parser.get_book_list()
        
        for book in books:
            # Get chapters
            chapters = self.chk_parser.get_chapters(book)
            
            for chapter in chapters:
                # Get verses from both languages
                chk_verses = self.chk_parser.get_verses(book, chapter)
                en_verses = self.en_parser.get_verses(book, chapter)
                
                # Align by verse number
                for verse_num, chk_text in chk_verses.items():
                    if verse_num in en_verses:
                        en_text = en_verses[verse_num]
                        
                        # Filter by length
                        if len(chk_text) >= min_verse_length and len(en_text) >= min_verse_length:
                            parallel_pairs.append({
                                'chuukese': chk_text.strip(),
                                'english': en_text.strip(),
                                'reference': f"{book} {chapter}:{verse_num}",
                                'source': 'bible',
                                'confidence': 0.95  # Bible translations are high-quality
                            })
        
        return parallel_pairs
    
    def export_for_helsinki_training(
        self, 
        output_path: str,
        direction: str = "chk_to_en"
    ) -> dict:
        """
        Export parallel data in format suitable for Helsinki-NLP fine-tuning.
        
        Args:
            output_path: Path for output files
            direction: 'chk_to_en' or 'en_to_chk'
        
        Returns:
            Statistics about exported data
        """
        pairs = self.extract_parallel_verses()
        
        # Split into train/val/test (80/10/10)
        from sklearn.model_selection import train_test_split
        
        train_pairs, test_pairs = train_test_split(pairs, test_size=0.2, random_state=42)
        val_pairs, test_pairs = train_test_split(test_pairs, test_size=0.5, random_state=42)
        
        # Export in TSV format for transformers
        for split_name, split_data in [
            ('train', train_pairs), 
            ('val', val_pairs), 
            ('test', test_pairs)
        ]:
            with open(f"{output_path}/{split_name}.tsv", 'w', encoding='utf-8') as f:
                for pair in split_data:
                    if direction == "chk_to_en":
                        f.write(f"{pair['chuukese']}\t{pair['english']}\n")
                    else:
                        f.write(f"{pair['english']}\t{pair['chuukese']}\n")
        
        return {
            'total_pairs': len(pairs),
            'train_size': len(train_pairs),
            'val_size': len(val_pairs),
            'test_size': len(test_pairs)
        }
```

### 3. Brochure Sentence Extraction

Extract parallel sentences from JW brochures.

```python
class BrochureSentenceExtractor:
    """Extract training pairs from brochure sentences."""
    
    def __init__(self, sentences_json_path: str):
        with open(sentences_json_path, 'r', encoding='utf-8') as f:
            self.sentences = json.load(f)
    
    def extract_training_pairs(self) -> list:
        """Extract and format brochure sentences for training."""
        pairs = []
        
        for item in self.sentences:
            if 'chuukese' in item and 'english' in item:
                pairs.append({
                    'chuukese': item['chuukese'],
                    'english': item['english'],
                    'source': 'brochure',
                    'confidence': item.get('confidence', 0.8)
                })
        
        return pairs
```

### 4. Implementation Pattern

```python
from .ai_training_generator import AITrainingDataGenerator

# Initialize generator
generator = AITrainingDataGenerator(min_confidence=0.7)

# Generate comprehensive training data
training_data = generator.generate_comprehensive_training_data(
    parsed_document,
    target_count=10000
)

# Export in multiple formats
files = generator.export_training_data(
    training_data,
    output_dir="training_output",
    format_type="ollama"
)
```

## Output Format Examples

### JSONL Format (Standard)

```json
{"input": "What does 'ááfengen' mean?", "output": "very good, excellent", "type": "dictionary_pair", "confidence": 0.95}
```

### Ollama Format

```json
{"prompt": "Translate this Chuukese word: ngang", "response": "fish", "system": "You are a Chuukese-English translator."}
```

### HuggingFace Format

```json
{"text": "### Instruction:\nWhat does 'chomong' mean in Chuukese?\n\n### Response:\nto help, assist"}
```

### OpenAI Fine-tuning Format

```json
{"messages": [{"role": "user", "content": "Define: kúún"}, {"role": "assistant", "content": "to go, to leave"}]}
```

## Quality Assurance

- **Content validity**: Does the example make linguistic sense?
- **Pattern matching**: Does it follow expected language patterns?
- **Context appropriateness**: Is the context relevant and helpful?
- **Uniqueness**: Avoid repetitive or duplicate content

## Best Practices

1. **Multiple validation passes**: Automated and manual quality checks
2. **Confidence thresholds**: Adjust based on use case requirements
3. **Human review sampling**: Periodic manual validation of generated examples
4. **Balance management**: Ensure even distribution across categories

## Dependencies

- `re`: Regular expression pattern matching
- `json`: Data serialization and export
- `hashlib`: Duplicate detection and content hashing
- `collections`: Data structure utilities and counting
