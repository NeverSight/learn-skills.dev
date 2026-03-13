---
name: translation-quality-assessment
description: Assess and validate translation quality between Chuukese and English with cultural context awareness, linguistic accuracy checking, and automated quality metrics. Supports Helsinki-NLP model evaluation with BLEU, chrF, and model-specific scoring. Use when evaluating translation outputs, building quality control systems, or validating translation models.
---

# Translation Quality Assessment

## Overview

A specialized skill for assessing translation quality between Chuukese and English, incorporating cultural context validation, linguistic accuracy checking, and automated quality metrics. Designed to ensure high-quality translations that preserve both linguistic meaning and cultural nuances.

**Supported Models**: Helsinki-NLP OPUS-MT, fine-tuned Chuukese models, hybrid translation systems

## Capabilities

- **Cultural Context Validation**: Ensure translations maintain cultural appropriateness and traditional concepts
- **Linguistic Accuracy Assessment**: Check grammatical correctness and meaning preservation
- **Automated Quality Metrics**: BLEU, chrF, ROUGE, and custom Chuukese-specific scoring
- **Helsinki-NLP Model Evaluation**: Model-specific metrics for OPUS-MT fine-tuned models
- **Consistency Checking**: Verify terminology consistency across translations
- **Fluency Evaluation**: Assess naturalness and readability of translations
- **Back-Translation Validation**: Round-trip translation quality assessment
- **Low-Resource Language Metrics**: chrF preferred for morphologically rich languages

## Core Components

### 1. Cultural Context Validator

```python
class ChuukeseCulturalValidator:
    def __init__(self):
        self.cultural_mappings = {
            # Family relationships with cultural significance
            'family_terms': {
                'semei': {'english': 'older brother', 'cultural_note': 'implies respect and responsibility'},
                'jinej': {'english': 'older sister', 'cultural_note': 'implies respect and responsibility'},
                'pwis': {'english': 'grandchild', 'cultural_note': 'special bond in Chuukese culture'}
            },
            
            # Traditional concepts that require cultural explanation
            'traditional_concepts': {
                'emon': {'english': 'traditional house', 'cultural_note': 'communal living structure'},
                'chomw': {'english': 'to help/cooperate', 'cultural_note': 'fundamental community value'},
                'nous': {'english': 'traditional gift exchange', 'cultural_note': 'important social practice'}
            },
            
            # Respect and formality indicators
            'respect_markers': {
                'oupwe': {'english': 'please (formal)', 'cultural_note': 'high respect level'},
                'kose mochen': {'english': 'thank you (formal)', 'cultural_note': 'deep gratitude expression'},
                'tipeew': {'english': 'excuse me (formal)', 'cultural_note': 'polite interruption'}
            }
        }
    
    def validate_cultural_preservation(self, chuukese_text, english_translation):
        """Validate that cultural concepts are properly translated"""
        validation_results = {
            'cultural_terms_found': [],
            'proper_translations': [],
            'missing_context': [],
            'cultural_accuracy_score': 0.0
        }
        
        total_cultural_terms = 0
        correctly_translated = 0
        
        for category, terms in self.cultural_mappings.items():
            for chuukese_term, translation_info in terms.items():
                if chuukese_term in chuukese_text.lower():
                    total_cultural_terms += 1
                    validation_results['cultural_terms_found'].append({
                        'term': chuukese_term,
                        'category': category,
                        'expected_translation': translation_info['english'],
                        'cultural_note': translation_info['cultural_note']
                    })
                    
                    # Check if English translation contains expected terms
                    if translation_info['english'] in english_translation.lower():
                        correctly_translated += 1
                        validation_results['proper_translations'].append(chuukese_term)
                    else:
                        validation_results['missing_context'].append({
                            'term': chuukese_term,
                            'expected': translation_info['english'],
                            'suggestion': f"Consider translating as '{translation_info['english']}' with note: {translation_info['cultural_note']}"
                        })
        
        if total_cultural_terms > 0:
            validation_results['cultural_accuracy_score'] = correctly_translated / total_cultural_terms
        
        return validation_results
```

### 2. Linguistic Accuracy Checker

```python
class ChuukeseLinguisticChecker:
    def __init__(self):
        # Common Chuukese grammatical patterns
        self.grammar_patterns = {
            'verb_patterns': {
                'present': r'(ko|ka|ke)\s+\w+',  # Present tense markers
                'past': r'(a|aa)\s+\w+',         # Past tense markers
                'future': r'(pwe|pwene)\s+\w+'   # Future tense markers
            },
            
            'noun_patterns': {
                'plural': r'\w+(kan|kin)$',      # Plural endings
                'possessive': r'\w+(y|i|ey)$'    # Possessive forms
            },
            
            'sentence_structure': {
                'basic_word_order': 'VSO',       # Verb-Subject-Object typical order
                'question_markers': ['ya', 'ese', 'iwe', 'mei']
            }
        }
    
    def check_grammatical_accuracy(self, chuukese_text, english_translation):
        """Check if translation preserves grammatical structures"""
        accuracy_report = {
            'tense_consistency': True,
            'structure_preservation': True,
            'grammatical_errors': [],
            'suggestions': []
        }
        
        # Check tense consistency
        chuukese_tenses = self.detect_tenses(chuukese_text)
        english_tenses = self.detect_english_tenses(english_translation)
        
        if not self.tenses_match(chuukese_tenses, english_tenses):
            accuracy_report['tense_consistency'] = False
            accuracy_report['grammatical_errors'].append('Tense mismatch between source and translation')
        
        # Check question structure preservation
        if any(marker in chuukese_text.lower() for marker in self.grammar_patterns['sentence_structure']['question_markers']):
            if not english_translation.strip().endswith('?'):
                accuracy_report['structure_preservation'] = False
                accuracy_report['grammatical_errors'].append('Question structure not preserved in translation')
        
        return accuracy_report
    
    def detect_tenses(self, text):
        """Detect tenses in Chuukese text"""
        detected_tenses = []
        for tense, pattern in self.grammar_patterns['verb_patterns'].items():
            if re.search(pattern, text, re.IGNORECASE):
                detected_tenses.append(tense)
        return detected_tenses
```

### 3. Automated Quality Metrics

```python
import math
from collections import Counter
import sacrebleu
from typing import List, Dict, Optional

class TranslationQualityMetrics:
    """
    Quality metrics for translation evaluation.
    Optimized for low-resource languages like Chuukese.
    """
    
    def __init__(self):
        self.reference_translations = {}  # Load from reference corpus
    
    def calculate_bleu_score(self, candidate: str, reference: str) -> float:
        """
        Calculate BLEU score using sacrebleu for consistency.
        Note: chrF is preferred for morphologically rich languages.
        """
        try:
            bleu = sacrebleu.sentence_bleu(candidate, [reference])
            return bleu.score / 100.0  # Normalize to 0-1
        except Exception:
            return self._fallback_bleu(candidate, reference)
    
    def _fallback_bleu(self, candidate: str, reference: str) -> float:
        """Fallback BLEU calculation if sacrebleu unavailable"""
        candidate_tokens = candidate.lower().split()
        reference_tokens = reference.lower().split()
        
        precisions = []
        for n in range(1, 5):
            candidate_ngrams = self.get_ngrams(candidate_tokens, n)
            reference_ngrams = self.get_ngrams(reference_tokens, n)
            
            if len(candidate_ngrams) == 0:
                precision = 0
            else:
                matches = sum(min(candidate_ngrams[ngram], reference_ngrams.get(ngram, 0)) 
                            for ngram in candidate_ngrams)
                precision = matches / len(candidate_ngrams)
            
            precisions.append(precision)
        
        candidate_length = len(candidate_tokens)
        reference_length = len(reference_tokens)
        
        if candidate_length > reference_length:
            bp = 1
        else:
            bp = math.exp(1 - reference_length / max(candidate_length, 1))
        
        if min(precisions) > 0:
            bleu = bp * math.exp(sum(math.log(p) for p in precisions if p > 0) / 4)
        else:
            bleu = 0
        
        return bleu
    
    def calculate_chrf_score(self, candidate: str, reference: str) -> float:
        """
        Calculate chrF score - PREFERRED for low-resource and morphologically rich languages.
        chrF is character-based and handles Chuukese accents better than BLEU.
        """
        try:
            chrf = sacrebleu.sentence_chrf(candidate, [reference])
            return chrf.score / 100.0  # Normalize to 0-1
        except Exception:
            return self._fallback_chrf(candidate, reference)
    
    def _fallback_chrf(self, candidate: str, reference: str) -> float:
        """Simple character F-score fallback"""
        candidate_chars = set(candidate.lower())
        reference_chars = set(reference.lower())
        
        if not candidate_chars or not reference_chars:
            return 0.0
        
        intersection = candidate_chars & reference_chars
        precision = len(intersection) / len(candidate_chars)
        recall = len(intersection) / len(reference_chars)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * precision * recall / (precision + recall)
    
    def get_ngrams(self, tokens: List[str], n: int) -> Counter:
        """Extract n-grams from token list"""
        ngrams = Counter()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n])
            ngrams[ngram] += 1
        return ngrams
    
    def calculate_cultural_preservation_score(self, cultural_validation_results: Dict) -> float:
        """Calculate score based on cultural context preservation"""
        base_score = cultural_validation_results.get('cultural_accuracy_score', 0.0)
        
        missing_context_penalty = len(cultural_validation_results.get('missing_context', [])) * 0.1
        proper_translations_bonus = len(cultural_validation_results.get('proper_translations', [])) * 0.05
        
        final_score = max(0.0, min(1.0, base_score - missing_context_penalty + proper_translations_bonus))
        
        return final_score


class HelsinkiModelEvaluator:
    """
    Specialized evaluator for Helsinki-NLP OPUS-MT models.
    Handles fine-tuned Chuukese translation models.
    """
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self.metrics = TranslationQualityMetrics()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def evaluate_model(
        self, 
        test_pairs: List[Dict[str, str]],
        direction: str = "chk_to_en"
    ) -> Dict[str, float]:
        """
        Evaluate Helsinki-NLP model on test set.
        
        Args:
            test_pairs: List of {'source': str, 'target': str}
            direction: 'chk_to_en' or 'en_to_chk'
        
        Returns:
            Dictionary with aggregate metrics
        """
        bleu_scores = []
        chrf_scores = []
        
        for pair in test_pairs:
            source = pair['source']
            target = pair['target']
            
            # Get model prediction
            prediction = self.translate(source, direction)
            
            # Calculate metrics
            bleu = self.metrics.calculate_bleu_score(prediction, target)
            chrf = self.metrics.calculate_chrf_score(prediction, target)
            
            bleu_scores.append(bleu)
            chrf_scores.append(chrf)
        
        return {
            'bleu_mean': sum(bleu_scores) / len(bleu_scores),
            'chrf_mean': sum(chrf_scores) / len(chrf_scores),
            'bleu_scores': bleu_scores,
            'chrf_scores': chrf_scores,
            'samples_evaluated': len(test_pairs)
        }
    
    def compare_models(
        self, 
        base_model_path: str,
        finetuned_model_path: str,
        test_pairs: List[Dict[str, str]]
    ) -> Dict[str, Dict[str, float]]:
        """
        Compare base vs fine-tuned model performance.
        
        Returns improvement metrics for the fine-tuned model.
        """
        base_results = self._evaluate_with_model(base_model_path, test_pairs)
        finetuned_results = self._evaluate_with_model(finetuned_model_path, test_pairs)
        
        return {
            'base_model': base_results,
            'finetuned_model': finetuned_results,
            'improvement': {
                'bleu_improvement': finetuned_results['bleu_mean'] - base_results['bleu_mean'],
                'chrf_improvement': finetuned_results['chrf_mean'] - base_results['chrf_mean'],
                'bleu_percent_improvement': (
                    (finetuned_results['bleu_mean'] - base_results['bleu_mean']) / 
                    max(base_results['bleu_mean'], 0.01) * 100
                ),
                'chrf_percent_improvement': (
                    (finetuned_results['chrf_mean'] - base_results['chrf_mean']) / 
                    max(base_results['chrf_mean'], 0.01) * 100
                )
            }
        }
    
    def translate(self, text: str, direction: str = "chk_to_en") -> str:
        """Translate text using loaded model"""
        # Implementation uses HelsinkiChuukeseTranslator
        pass
    
    def _evaluate_with_model(
        self, 
        model_path: str, 
        test_pairs: List[Dict[str, str]]
    ) -> Dict[str, float]:
        """Evaluate specific model"""
        # Load model and evaluate
        pass
```

### 4. Comprehensive Quality Assessment Pipeline

```python
class TranslationQualityAssessment:
    def __init__(self, reference_corpus_path=None):
        self.cultural_validator = ChuukeseCulturalValidator()
        self.linguistic_checker = ChuukeseLinguisticChecker()
        self.metrics_calculator = TranslationQualityMetrics()
        
        if reference_corpus_path:
            self.load_reference_corpus(reference_corpus_path)
    
    def assess_translation_quality(self, chuukese_text, english_translation, reference_translation=None):
        """Comprehensive translation quality assessment"""
        assessment_report = {
            'overall_quality_score': 0.0,
            'cultural_validation': {},
            'linguistic_accuracy': {},
            'automated_metrics': {},
            'recommendations': []
        }
        
        # Cultural context validation
        cultural_results = self.cultural_validator.validate_cultural_preservation(
            chuukese_text, english_translation
        )
        assessment_report['cultural_validation'] = cultural_results
        
        # Linguistic accuracy check
        linguistic_results = self.linguistic_checker.check_grammatical_accuracy(
            chuukese_text, english_translation
        )
        assessment_report['linguistic_accuracy'] = linguistic_results
        
        # Automated metrics
        metrics = {}
        if reference_translation:
            metrics['bleu_score'] = self.metrics_calculator.calculate_bleu_score(
                english_translation, reference_translation
            )
        
        metrics['cultural_preservation_score'] = self.metrics_calculator.calculate_cultural_preservation_score(
            cultural_results
        )
        
        assessment_report['automated_metrics'] = metrics
        
        # Calculate overall quality score
        overall_score = self.calculate_overall_score(cultural_results, linguistic_results, metrics)
        assessment_report['overall_quality_score'] = overall_score
        
        # Generate recommendations
        recommendations = self.generate_recommendations(cultural_results, linguistic_results, metrics)
        assessment_report['recommendations'] = recommendations
        
        return assessment_report
    
    def calculate_overall_score(self, cultural_results, linguistic_results, metrics):
        """Calculate weighted overall quality score"""
        cultural_score = metrics.get('cultural_preservation_score', 0.0)
        linguistic_score = 1.0 if linguistic_results.get('tense_consistency', False) and linguistic_results.get('structure_preservation', False) else 0.5
        bleu_score = metrics.get('bleu_score', 0.0)
        
        # Weighted average (cultural context heavily weighted for Chuukese)
        overall_score = (cultural_score * 0.4 + linguistic_score * 0.4 + bleu_score * 0.2)
        
        return round(overall_score, 3)
    
    def generate_recommendations(self, cultural_results, linguistic_results, metrics):
        """Generate actionable recommendations for translation improvement"""
        recommendations = []
        
        # Cultural recommendations
        if cultural_results.get('cultural_accuracy_score', 0) < 0.8:
            recommendations.append("Consider adding cultural context or explanations for traditional terms")
        
        for missing in cultural_results.get('missing_context', []):
            recommendations.append(f"Improve translation of '{missing['term']}': {missing['suggestion']}")
        
        # Linguistic recommendations
        if not linguistic_results.get('tense_consistency', True):
            recommendations.append("Review tense consistency between source and target languages")
        
        if not linguistic_results.get('structure_preservation', True):
            recommendations.append("Preserve sentence structure and question forms from source language")
        
        # Metric-based recommendations
        if metrics.get('bleu_score', 0) < 0.3:
            recommendations.append("Consider improving lexical similarity with reference translations")
        
        return recommendations
```

## Usage Examples

### Basic Translation Assessment

```python
# Initialize assessment system
assessor = TranslationQualityAssessment("reference_corpus.json")

# Assess a translation
chuukese_text = "Kopwe pwan chomong ngonuk ekkewe chon Chuuk"
english_translation = "We will help those Chuukese people"
reference_translation = "We shall assist the people of Chuuk"

assessment = assessor.assess_translation_quality(
    chuukese_text, 
    english_translation, 
    reference_translation
)

print(f"Overall Quality Score: {assessment['overall_quality_score']}")
for recommendation in assessment['recommendations']:
    print(f"- {recommendation}")
```

### Batch Translation Evaluation

```python
def evaluate_translation_batch(translation_pairs):
    """Evaluate multiple translations and generate summary report"""
    results = []
    total_score = 0
    
    for pair in translation_pairs:
        assessment = assessor.assess_translation_quality(
            pair['chuukese'],
            pair['english'],
            pair.get('reference')
        )
        results.append(assessment)
        total_score += assessment['overall_quality_score']
    
    average_score = total_score / len(translation_pairs)
    
    summary_report = {
        'average_quality_score': average_score,
        'total_assessments': len(translation_pairs),
        'individual_results': results,
        'common_issues': identify_common_issues(results)
    }
    
    return summary_report
```

## Best Practices

### Quality Assessment

1. **Multiple validation layers**: Combine automated metrics with cultural validation
2. **Reference corpus usage**: Maintain high-quality reference translations for comparison
3. **Community validation**: Involve native speakers in quality assessment
4. **Continuous improvement**: Update assessment criteria based on feedback

### Cultural Sensitivity

1. **Context preservation**: Ensure cultural concepts are properly explained
2. **Respect levels**: Validate appropriate formality and respect markers
3. **Traditional knowledge**: Incorporate understanding of Chuukese customs
4. **Community standards**: Align with community expectations for translation quality

### Technical Implementation

1. **Comprehensive metrics**: Use multiple quality indicators
2. **Actionable feedback**: Provide specific, implementable recommendations
3. **Scalable assessment**: Design for batch processing and automation
4. **Continuous learning**: Adapt assessment criteria based on new insights

## Dependencies

- `re`: Regular expression pattern matching
- `math`: Mathematical operations for scoring
- `collections`: Counter for n-gram analysis
- `json`: Reference corpus data handling
- `nltk`: Natural language processing utilities

## Validation Criteria

A successful implementation should:

- ✅ Accurately assess cultural context preservation
- ✅ Validate linguistic accuracy and grammatical consistency
- ✅ Provide meaningful quality scores and metrics
- ✅ Generate actionable recommendations for improvement
- ✅ Handle both individual and batch assessments
- ✅ Integrate with existing translation workflows
- ✅ Support continuous quality monitoring and improvement
