---
name: bible-epub-processing
description: Parse and extract structured content from Bible EPUBs (NWT) for parallel text alignment between Chuukese and English. Use when working with Bible data, verse extraction, parallel corpus building, or generating training data from Scripture.
---

# Bible EPUB Processing

## Overview

Parse and extract structured content from New World Translation (NWT) Bible EPUBs to build parallel corpora for Chuukese-English translation training. The NWT is available in both Chuukese (nwt_TE.epub) and English (nwt_E.epub), providing high-quality aligned translations.

## File Locations

```text
data/bible/
├── nwt_E.epub      # English NWT Bible
└── nwt_TE.epub     # Chuukese (Trukese) NWT Bible
```

## EPUB Structure

NWT EPUBs follow a specific structure:

```text
nwt_X.epub/
├── META-INF/
│   └── container.xml
├── OEBPS/
│   ├── content.opf
│   ├── toc.ncx
│   └── OEBPS/
│       ├── 01_Genesis.xhtml
│       ├── 02_Exodus.xhtml
│       └── ... (66 books)
```

## NWT EPUB Parser

### Core Parser Class

```python
# src/utils/nwt_epub_parser.py
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class NWTEpubParser:
    """
    Parser for New World Translation Bible EPUBs.
    Extracts books, chapters, and verses with proper structure.
    """
    
    # Book order in NWT (66 books)
    BOOK_ORDER = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles",
        "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
        "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
        "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos",
        "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah",
        "Haggai", "Zechariah", "Malachi", "Matthew", "Mark", "Luke",
        "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians",
        "Galatians", "Ephesians", "Philippians", "Colossians",
        "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
        "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter",
        "1 John", "2 John", "3 John", "Jude", "Revelation"
    ]
    
    def __init__(self, epub_path: str):
        self.epub_path = epub_path
        self.book = epub.read_epub(epub_path)
        self._book_cache = {}
        self._chapter_cache = {}
        
        logger.info(f"Loaded EPUB: {epub_path}")
    
    def get_book_list(self) -> List[str]:
        """Get list of available books in the EPUB."""
        books = []
        
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                name = item.get_name()
                # Extract book name from filename
                match = re.search(r'\d+_(\w+)\.xhtml', name)
                if match:
                    books.append(match.group(1))
        
        return books
    
    def get_chapters(self, book_name: str) -> List[int]:
        """Get list of chapter numbers for a book."""
        content = self._get_book_content(book_name)
        if not content:
            return []
        
        soup = BeautifulSoup(content, 'lxml')
        
        # Find chapter markers
        chapters = set()
        for elem in soup.find_all(class_=re.compile(r'chapter|chapterNum')):
            text = elem.get_text(strip=True)
            try:
                chapter_num = int(re.search(r'\d+', text).group())
                chapters.add(chapter_num)
            except (ValueError, AttributeError):
                continue
        
        return sorted(chapters)
    
    def get_verses(self, book_name: str, chapter: int) -> Dict[int, str]:
        """
        Get all verses for a specific chapter.
        
        Returns:
            Dictionary mapping verse numbers to verse text
        """
        content = self._get_book_content(book_name)
        if not content:
            return {}
        
        soup = BeautifulSoup(content, 'lxml')
        verses = {}
        
        # Find the chapter section
        chapter_section = self._find_chapter_section(soup, chapter)
        if not chapter_section:
            return {}
        
        # Extract verses
        for verse_elem in chapter_section.find_all(class_=re.compile(r'verse|v\d+')):
            verse_num = self._extract_verse_number(verse_elem)
            if verse_num:
                verse_text = self._extract_verse_text(verse_elem)
                if verse_text:
                    verses[verse_num] = verse_text
        
        return verses
    
    def get_verse(self, book_name: str, chapter: int, verse: int) -> Optional[str]:
        """Get a specific verse."""
        verses = self.get_verses(book_name, chapter)
        return verses.get(verse)
    
    def get_verse_range(
        self, 
        book_name: str, 
        chapter: int, 
        start_verse: int, 
        end_verse: int
    ) -> str:
        """Get a range of verses as combined text."""
        verses = self.get_verses(book_name, chapter)
        
        verse_texts = []
        for v in range(start_verse, end_verse + 1):
            if v in verses:
                verse_texts.append(verses[v])
        
        return ' '.join(verse_texts)
    
    def _get_book_content(self, book_name: str) -> Optional[str]:
        """Get raw HTML content for a book."""
        if book_name in self._book_cache:
            return self._book_cache[book_name]
        
        for item in self.book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                if book_name.lower() in item.get_name().lower():
                    content = item.get_content().decode('utf-8')
                    self._book_cache[book_name] = content
                    return content
        
        return None
    
    def _find_chapter_section(self, soup: BeautifulSoup, chapter: int):
        """Find the DOM section for a specific chapter."""
        # Different strategies for finding chapter boundaries
        
        # Strategy 1: Look for chapter heading
        for heading in soup.find_all(['h2', 'h3', 'div'], class_=re.compile(r'chapter')):
            if str(chapter) in heading.get_text():
                return heading.find_parent('section') or heading.find_parent('div')
        
        # Strategy 2: Look for chapter number span
        for span in soup.find_all('span', class_=re.compile(r'chapterNum')):
            if span.get_text(strip=True) == str(chapter):
                return span.find_parent('section') or span.find_parent('div')
        
        return soup  # Return whole document if chapter not found
    
    def _extract_verse_number(self, elem) -> Optional[int]:
        """Extract verse number from element."""
        # Check for verse number class
        verse_class = elem.get('class', [])
        for cls in verse_class:
            match = re.search(r'v(\d+)', cls)
            if match:
                return int(match.group(1))
        
        # Check for data attribute
        verse_num = elem.get('data-verse')
        if verse_num:
            return int(verse_num)
        
        # Check for sup element with verse number
        sup = elem.find('sup')
        if sup:
            try:
                return int(sup.get_text(strip=True))
            except ValueError:
                pass
        
        return None
    
    def _extract_verse_text(self, elem) -> str:
        """Extract clean verse text from element."""
        # Remove verse number and footnote markers
        text = elem.get_text(separator=' ', strip=True)
        
        # Clean up the text
        text = re.sub(r'^\d+\s*', '', text)  # Remove leading verse number
        text = re.sub(r'\*+', '', text)  # Remove footnote markers
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        return text.strip()
```

### Parallel Corpus Builder

```python
class ParallelCorpusBuilder:
    """
    Build parallel corpora from Chuukese and English NWT EPUBs.
    """
    
    def __init__(self, chuukese_epub: str, english_epub: str):
        self.chk_parser = NWTEpubParser(chuukese_epub)
        self.en_parser = NWTEpubParser(english_epub)
        
    def build_parallel_corpus(
        self,
        books: List[str] = None,
        min_length: int = 10,
        max_length: int = 500
    ) -> List[Dict]:
        """
        Build parallel verse pairs.
        
        Args:
            books: List of books to include (None = all)
            min_length: Minimum verse length in characters
            max_length: Maximum verse length in characters
        
        Returns:
            List of parallel pairs with metadata
        """
        if books is None:
            books = self.chk_parser.get_book_list()
        
        pairs = []
        
        for book in books:
            logger.info(f"Processing {book}...")
            
            chapters = self.chk_parser.get_chapters(book)
            
            for chapter in chapters:
                chk_verses = self.chk_parser.get_verses(book, chapter)
                en_verses = self.en_parser.get_verses(book, chapter)
                
                # Align verses by number
                for verse_num in chk_verses:
                    if verse_num in en_verses:
                        chk_text = chk_verses[verse_num]
                        en_text = en_verses[verse_num]
                        
                        # Filter by length
                        if (min_length <= len(chk_text) <= max_length and
                            min_length <= len(en_text) <= max_length):
                            
                            pairs.append({
                                'chuukese': chk_text,
                                'english': en_text,
                                'reference': f"{book} {chapter}:{verse_num}",
                                'book': book,
                                'chapter': chapter,
                                'verse': verse_num,
                                'source': 'nwt_bible',
                                'confidence': 0.95  # High quality translations
                            })
        
        logger.info(f"Built {len(pairs)} parallel pairs")
        return pairs
    
    def export_for_training(
        self,
        output_dir: str,
        direction: str = "chk_to_en",
        test_split: float = 0.1,
        val_split: float = 0.1
    ) -> Dict[str, int]:
        """
        Export parallel corpus for model training.
        
        Args:
            output_dir: Directory for output files
            direction: 'chk_to_en' or 'en_to_chk'
            test_split: Fraction for test set
            val_split: Fraction for validation set
        
        Returns:
            Statistics about exported data
        """
        import os
        from sklearn.model_selection import train_test_split
        
        os.makedirs(output_dir, exist_ok=True)
        
        pairs = self.build_parallel_corpus()
        
        # Split data
        train, test = train_test_split(pairs, test_size=test_split, random_state=42)
        train, val = train_test_split(train, test_size=val_split/(1-test_split), random_state=42)
        
        # Export TSV files
        for split_name, split_data in [('train', train), ('val', val), ('test', test)]:
            filepath = os.path.join(output_dir, f'{split_name}.tsv')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for pair in split_data:
                    if direction == "chk_to_en":
                        source = pair['chuukese']
                        target = pair['english']
                    else:
                        source = pair['english']
                        target = pair['chuukese']
                    
                    f.write(f"{source}\t{target}\n")
        
        return {
            'total': len(pairs),
            'train': len(train),
            'val': len(val),
            'test': len(test)
        }
    
    def export_jsonl(self, output_path: str, format_type: str = "ollama") -> int:
        """
        Export parallel corpus as JSONL for LLM training.
        
        Args:
            output_path: Path for output file
            format_type: 'ollama', 'openai', or 'huggingface'
        
        Returns:
            Number of examples exported
        """
        import json
        
        pairs = self.build_parallel_corpus()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for pair in pairs:
                if format_type == "ollama":
                    example = {
                        "prompt": f"Translate this Chuukese verse to English: {pair['chuukese']}",
                        "response": pair['english'],
                        "system": "You are a Chuukese-English Bible translator."
                    }
                elif format_type == "openai":
                    example = {
                        "messages": [
                            {"role": "system", "content": "You are a Chuukese-English translator."},
                            {"role": "user", "content": f"Translate: {pair['chuukese']}"},
                            {"role": "assistant", "content": pair['english']}
                        ]
                    }
                else:  # huggingface
                    example = {
                        "text": f"### Instruction:\nTranslate this Chuukese text to English.\n\n### Input:\n{pair['chuukese']}\n\n### Response:\n{pair['english']}"
                    }
                
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        return len(pairs)
```

## Usage Examples

### Basic Verse Extraction

```python
from src.utils.nwt_epub_parser import NWTEpubParser

# Load English Bible
parser = NWTEpubParser('data/bible/nwt_E.epub')

# Get list of books
books = parser.get_book_list()
print(f"Found {len(books)} books")

# Get chapters in Genesis
chapters = parser.get_chapters('Genesis')
print(f"Genesis has {len(chapters)} chapters")

# Get all verses in Genesis 1
verses = parser.get_verses('Genesis', 1)
print(f"Genesis 1 has {len(verses)} verses")

# Get specific verse
verse = parser.get_verse('Genesis', 1, 1)
print(f"Genesis 1:1 - {verse}")
```

### Building Parallel Corpus

```python
from src.utils.nwt_epub_parser import ParallelCorpusBuilder

# Build corpus from both Bibles
builder = ParallelCorpusBuilder(
    chuukese_epub='data/bible/nwt_TE.epub',
    english_epub='data/bible/nwt_E.epub'
)

# Get all parallel pairs
pairs = builder.build_parallel_corpus()
print(f"Total parallel pairs: {len(pairs)}")

# Export for Helsinki-NLP training
stats = builder.export_for_training(
    output_dir='training_data/bible',
    direction='chk_to_en'
)
print(f"Train: {stats['train']}, Val: {stats['val']}, Test: {stats['test']}")
```

### Exporting for LLM Training

```python
# Export for Ollama fine-tuning
count = builder.export_jsonl(
    output_path='training_data/bible_ollama.jsonl',
    format_type='ollama'
)
print(f"Exported {count} examples for Ollama")
```

## Quality Considerations

### High-Quality Pairs

- Bible translations are professionally reviewed
- Consistent terminology across verses
- Good for formal/religious register

### Potential Issues

- Religious vocabulary may not generalize
- Formal language style
- Some verses have complex structures

### Filtering Strategies

```python
def filter_pairs(pairs):
    """Filter pairs for training quality."""
    filtered = []
    
    for pair in pairs:
        # Skip very short pairs
        if len(pair['chuukese']) < 20 or len(pair['english']) < 20:
            continue
        
        # Skip pairs with unusual length ratios
        ratio = len(pair['chuukese']) / len(pair['english'])
        if ratio < 0.5 or ratio > 2.0:
            continue
        
        # Skip pairs with mostly numbers
        if sum(c.isdigit() for c in pair['chuukese']) / len(pair['chuukese']) > 0.3:
            continue
        
        filtered.append(pair)
    
    return filtered
```

## Dependencies

- `ebooklib>=0.18`: EPUB parsing
- `beautifulsoup4>=4.12.0`: HTML parsing
- `lxml>=4.9.0`: XML/HTML parser
- `scikit-learn>=1.0.0`: Data splitting (optional)
