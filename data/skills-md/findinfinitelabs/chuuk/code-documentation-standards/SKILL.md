---
name: code-documentation-standards
description: Comprehensive code documentation standards and guidelines for maintaining up-to-date documentation across Python, HTML, CSS, and JavaScript codebases. Use when creating or modifying code to ensure proper documentation practices and maintainable code.
---

# Code Documentation Standards

## Core Principle

**ALWAYS maintain up-to-date documentation when creating or modifying code.**
**Documentation must be updated simultaneously with code changes.**
**ALWAYS fix markdown validation errors promptly before committing any changes.**

### Pre-Commit Markdown Validation

Before any commit, ALWAYS:

1. **Run markdown validation** on all .md files in the repository
2. **Fix all markdown syntax errors** including:
   - Unclosed code blocks
   - Missing link destinations
   - Invalid heading structures
   - Broken table formatting
   - Incorrect list indentation
3. **Validate code block syntax** in documentation
4. **Check internal links** are properly formatted
5. **Ensure consistent formatting** across all markdown files

## Documentation Requirements

### 1. Python Functions/Classes

```python
def process_document(file_path: str, patterns: List[str]) -> ProcessResult:
    """
    Process a document for redaction using specified patterns.
    
    Args:
        file_path (str): Path to the document file to process
        patterns (List[str]): List of redaction patterns to apply
        
    Returns:
        ProcessResult: Object containing processed document and metadata
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValidationError: If patterns are invalid
        
    Example:
        >>> result = process_document('doc.pdf', ['ssn', 'email'])
        >>> print(result.redacted_count)
    """
    pass
```

### 2. Class Documentation

```python
class DocumentProcessor:
    """
    Handles document processing operations for various file formats.
    
    This class provides methods for parsing, analyzing, and transforming
    documents while maintaining original formatting and metadata.
    
    Attributes:
        supported_formats (List[str]): File formats supported by processor
        max_file_size (int): Maximum file size in bytes
        
    Example:
        >>> processor = DocumentProcessor()
        >>> result = processor.process('document.pdf')
    """
    
    def __init__(self, config: ProcessingConfig = None):
        """Initialize processor with optional configuration."""
        pass
```

### 3. Template Documentation

```html
<!-- 
Template: translation_interface.html
Purpose: Main interface for Chuukese-English translation
Variables:
  - dictionary_entries: List of recent dictionary entries
  - user_translations: User's translation history
  - cultural_context: Cultural context data for assistance
Dependencies:
  - static/css/translation.css
  - static/js/translation-ui.js
  - Bootstrap 5.1+
-->
<div class="translation-container">
    <!-- Translation form content -->
</div>
```

### 4. CSS Class Documentation

```css
/* 
 * Chuukese Text Display
 * Purpose: Styles for displaying Chuukese text with proper accent handling
 * Usage: Apply to containers holding Chuukese language content
 * Dependencies: Requires font-family supporting Unicode accents
 */
.chuukese-text {
    font-family: 'Noto Sans', 'Arial Unicode MS', sans-serif;
    font-size: 1.1em;
    line-height: 1.5;
    direction: ltr;
}

/* 
 * Responsive adaptation: Increase font size on mobile
 * Context: Better readability for accented characters
 */
@media (max-width: 768px) {
    .chuukese-text {
        font-size: 1.2em;
    }
}
```

### 5. JavaScript Function Documentation

```javascript
/**
 * Normalize Chuukese text for search operations
 * @param {string} text - The Chuukese text to normalize
 * @param {boolean} preserveAccents - Whether to preserve accent marks
 * @returns {string} Normalized text suitable for searching
 * @throws {TypeError} If text is not a string
 * 
 * @example
 * const normalized = normalizeChuukeseText('kápás', false);
 * console.log(normalized); // 'kapas'
 */
function normalizeChuukeseText(text, preserveAccents = true) {
    if (typeof text !== 'string') {
        throw new TypeError('Text parameter must be a string');
    }
    // Implementation...
}
```

## Documentation Standards by Context

### Database Models

```python
class DictionaryEntry(Base):
    """
    Represents a Chuukese-English dictionary entry.
    
    This model stores bilingual dictionary data with cultural context,
    pronunciation guides, and usage information for language learning
    and translation applications.
    
    Attributes:
        chuukese_word (str): Primary Chuukese term (required)
        english_definition (str): English definition or translation
        pronunciation (str): IPA or phonetic pronunciation guide
        cultural_context (str): Cultural significance and usage notes
        part_of_speech (str): Grammatical category (noun, verb, etc.)
        difficulty_level (str): Learning difficulty (beginner/intermediate/advanced)
        usage_frequency (float): Frequency score 0.0-1.0
        
    Relationships:
        phrases: Related phrase entries using this word
        translations: Translation pairs containing this entry
        
    Example:
        >>> entry = DictionaryEntry(
        ...     chuukese_word="chomong",
        ...     english_definition="to help, assist",
        ...     cultural_context="Community cooperation value"
        ... )
    """
    __tablename__ = 'dictionary_entries'
    
    id = Column(Integer, primary_key=True)
    chuukese_word = Column(String(200), nullable=False, index=True)
    # ... rest of model
```

### API Routes

```python
@app.route('/api/translate', methods=['POST'])
def translate_text():
    """
    Translate text between Chuukese and English.
    
    Endpoint for bidirectional text translation with quality assessment
    and cultural context preservation.
    
    Request Body:
        {
            "text": "string - Text to translate (required)",
            "source_language": "string - Source language code (required)",
            "target_language": "string - Target language code (required)",
            "include_cultural_context": "boolean - Include cultural notes
                                        (optional, default: false)"
        }
    
    Response:
        {
            "translated_text": "string - Translated result",
            "quality_score": "float - Translation quality 0.0-1.0",
            "cultural_notes": "array - Cultural context information (if requested)",
            "confidence": "float - Translation confidence score"
        }
    
    Status Codes:
        200: Translation successful
        400: Invalid request parameters
        422: Translation quality too low
        500: Internal server error
    
    Example:
        >>> POST /api/translate
        >>> {
        ...     "text": "chomong",
        ...     "source_language": "chuukese",
        ...     "target_language": "english"
        ... }
        
        Response:
        {
            "translated_text": "to help",
            "quality_score": 0.95,
            "confidence": 0.98
        }
    """
    pass
```

## Best Practices

### 1. Consistency Standards

- Use consistent parameter naming across similar functions
- Maintain uniform documentation formatting
- Follow established patterns for each language/framework
- Update documentation immediately when code changes
- **Fix all markdown validation errors before committing**

### 2. Content Guidelines

- Write for developers who don't know the codebase
- Include practical examples whenever possible
- Document edge cases and error conditions
- Explain the "why" behind implementation decisions

### 3. Cultural Context Documentation (Chuukese Project Specific)

- Document cultural significance of Chuukese terms
- Explain traditional concepts that may not translate directly
- Note appropriate usage contexts (formal/informal, traditional/modern)
- Include pronunciation guides for language learners

### 4. Maintenance Requirements

- Review documentation during code reviews
- Update documentation in the same commit as code changes
- Mark deprecated functions with alternatives
- Remove documentation for deleted code
- **Validate markdown syntax before each commit**

### 5. Quality Checks

- Verify all parameters are documented
- Ensure examples are current and functional
- Check that return types match actual implementation
- Validate that error conditions are accurately described
- **Run markdown linting tools on all documentation**

### 6. Markdown Validation Process

**MANDATORY before every commit:**

1. **Syntax Validation:**

   ```bash
   # Check for markdown syntax errors
   markdownlint **/*.md
   ```

2. **Code Block Validation:**
   - Ensure all code blocks have proper opening/closing backticks
   - Verify language tags are correct (python, javascript, html, css)
   - Test that code examples are syntactically valid

3. **Link Validation:**
   - Check all internal links reference existing files/sections
   - Verify external links are accessible
   - Ensure proper markdown link syntax: `[text](url)`

4. **Structure Validation:**
   - Confirm heading hierarchy is logical (h1 → h2 → h3)
   - Verify lists have consistent indentation
   - Check table formatting is complete

5. **Common Fixes:**
   - Close unclosed code blocks with proper backticks
   - Fix malformed tables with proper pipe alignment
   - Correct broken link references
   - Standardize heading styles (#, ##, ###)
   - Fix list item indentation and nesting

## Templates

### Function Documentation Template

```python
def function_name(param1: Type1, param2: Type2 = default) -> ReturnType:
    """
    Brief description of what the function does.
    
    Longer description if needed, explaining the purpose and any
    important implementation details or assumptions.
    
    Args:
        param1 (Type1): Description of first parameter
        param2 (Type2, optional): Description with default value
        
    Returns:
        ReturnType: Description of return value
        
    Raises:
        ExceptionType: When this exception occurs
        
    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        
    Note:
        Any special considerations or warnings
    """
```

### Class Documentation Template

```python
class ClassName:
    """
    Brief description of the class purpose.
    
    Detailed explanation of what the class represents,
    its main responsibilities, and how it fits into
    the larger system.
    
    Attributes:
        attr_name (Type): Description of attribute
        
    Example:
        >>> instance = ClassName(param)
        >>> result = instance.method()
        
    See Also:
        RelatedClass: For related functionality
    """
```

## Dependencies

- Follow project-specific documentation tools
- Use type hints for Python functions
- Include JSDoc for JavaScript when applicable
- Maintain README files for project overviews

## Validation Criteria

Proper documentation should:

- ✅ Explain the purpose clearly and concisely
- ✅ Document all parameters and return values
- ✅ Include practical usage examples
- ✅ Note error conditions and exceptions
- ✅ Use consistent formatting and style
- ✅ Stay current with code changes
- ✅ Provide cultural context for Chuukese-specific terms
- ✅ **Pass markdown validation without errors**
- ✅ **Have properly formatted code blocks and links**
- ✅ **Use consistent heading structure and list formatting**

## Pre-Commit Workflow

**MANDATORY checklist before every commit:**

1. ✅ **Code documentation updated**
2. ✅ **Markdown files validated and errors fixed**
3. ✅ **Code blocks properly formatted with language tags**
4. ✅ **All links functional and properly formatted**
5. ✅ **Heading hierarchy follows logical structure**
6. ✅ **Examples tested and verified working**

**Tools for validation:**

- `markdownlint` for syntax checking
- VS Code markdown preview for visual verification
- Link checkers for external references
- Code syntax validators for embedded examples
