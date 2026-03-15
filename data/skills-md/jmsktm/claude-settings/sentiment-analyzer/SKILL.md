---
name: Sentiment Analyzer
slug: sentiment-analyzer
description: Analyze text sentiment at scale with nuanced understanding
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "analyze sentiment"
  - "sentiment analysis"
  - "opinion mining"
  - "emotion detection"
  - "text sentiment"
tags:
  - sentiment
  - NLP
  - opinion-mining
  - emotion
  - text-analysis
---

# Sentiment Analyzer

The Sentiment Analyzer skill guides you through implementing sentiment analysis systems that understand the emotional tone and opinion in text. From simple positive/negative classification to nuanced aspect-based sentiment and emotion detection, this skill covers the full spectrum of sentiment analysis capabilities.

Sentiment analysis is deceptively complex. Sarcasm, context, domain-specific language, and cultural nuances all challenge simple approaches. This skill helps you choose the right techniques for your accuracy requirements, whether that's fast rule-based systems, fine-tuned classifiers, or LLM-based analysis.

Whether you're analyzing customer reviews, social media mentions, support tickets, or survey responses, this skill ensures your sentiment analysis captures the true voice of your users.

## Core Workflows

### Workflow 1: Choose Sentiment Analysis Approach
1. **Define** requirements:
   - Granularity: Binary, ternary, or continuous?
   - Aspects: Overall or aspect-based?
   - Emotions: Sentiment or specific emotions?
   - Languages: Single or multilingual?
   - Volume: Batch or real-time?
2. **Evaluate** options:
   | Approach | Speed | Accuracy | Customizable | Best For |
   |----------|-------|----------|--------------|----------|
   | Rule-based (VADER) | Very fast | Moderate | Limited | Social media, quick analysis |
   | Pre-trained (RoBERTa) | Fast | Good | Fine-tunable | General text |
   | Fine-tuned | Fast | Best | Requires data | Domain-specific |
   | LLM (GPT-4, Claude) | Slow | Excellent | Prompt-based | Nuanced, complex |
3. **Select** based on tradeoffs
4. **Plan** implementation

### Workflow 2: Implement Sentiment Pipeline
1. **Preprocess** text:
   ```python
   def preprocess_for_sentiment(text):
       # Preserve sentiment-relevant features
       text = normalize_unicode(text)

       # Handle social media conventions
       text = expand_contractions(text)  # don't -> do not
       text = normalize_elongation(text)  # loooove -> love
       text = handle_negation(text)       # Mark negation scope

       # Preserve but normalize emoji/emoticons
       text = convert_emoji_to_text(text)  # :) -> [HAPPY]

       return text
   ```
2. **Analyze** sentiment:
   ```python
   class SentimentAnalyzer:
       def __init__(self, model_type="transformer"):
           if model_type == "transformer":
               self.model = pipeline("sentiment-analysis",
                                   model="cardiffnlp/twitter-roberta-base-sentiment")
           elif model_type == "vader":
               self.model = SentimentIntensityAnalyzer()

       def analyze(self, text):
           preprocessed = preprocess_for_sentiment(text)
           result = self.model(preprocessed)
           return {
               "text": text,
               "sentiment": result["label"],
               "confidence": result["score"]
           }
   ```
3. **Aggregate** for insights:
   - Overall sentiment distribution
   - Sentiment over time
   - Sentiment by segment/topic
4. **Validate** results

### Workflow 3: Aspect-Based Sentiment Analysis
1. **Identify** aspects to track:
   - Product features (price, quality, service)
   - Experience dimensions (speed, accuracy, friendliness)
   - Custom aspects for your domain
2. **Extract** aspects from text:
   ```python
   def extract_aspects(text, aspect_list):
       # Find mentions of known aspects
       found_aspects = []
       for aspect in aspect_list:
           if aspect.lower() in text.lower():
               found_aspects.append(aspect)

       # Also extract using NER or LLM for unknown aspects
       extracted = extract_noun_phrases(text)
       return found_aspects + extracted
   ```
3. **Analyze** sentiment per aspect:
   ```python
   def aspect_sentiment(text, aspects):
       results = {}
       for aspect in aspects:
           # Extract sentences mentioning aspect
           relevant = extract_aspect_context(text, aspect)

           # Analyze sentiment of relevant text
           if relevant:
               sentiment = analyze_sentiment(relevant)
               results[aspect] = sentiment

       return results
   ```
4. **Aggregate** aspect sentiments across documents

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Analyze sentiment | "Analyze sentiment of [text]" |
| Choose approach | "Best sentiment analysis for [use case]" |
| Aspect-based | "Sentiment by feature for [reviews]" |
| Detect emotions | "Detect emotions in [text]" |
| Handle sarcasm | "How to handle sarcasm in sentiment" |
| Aggregate results | "Summarize sentiment trends" |

## Best Practices

- **Preserve Sentiment Signals**: Don't preprocess away important cues
  - Keep punctuation (!! vs .)
  - Preserve capitalization patterns
  - Keep emoji/emoticons (convert to text)
  - Handle negation explicitly

- **Match Model to Domain**: Pre-trained models have domain bias
  - Twitter models work differently than product review models
  - Fine-tune or select domain-appropriate models
  - Test on your actual data before deploying

- **Handle Negation Properly**: "Not bad" isn't negative
  - Rule-based: Mark negation scope
  - Neural models: Usually handle automatically
  - Test negation cases explicitly

- **Consider Context**: Sentiment depends on context
  - "Cheap" is positive for budget items, negative for luxury
  - Use aspect-based analysis for nuance
  - Include surrounding context when possible

- **Validate with Humans**: Machine sentiment != human sentiment
  - Sample and manually verify results
  - Calculate agreement metrics
  - Iterate on disagreements

- **Report Uncertainty**: Not all text has clear sentiment
  - Neutral is a valid class
  - Low confidence predictions should be flagged
  - Consider abstaining on ambiguous cases

## Advanced Techniques

### LLM-Based Nuanced Sentiment
Use language models for complex analysis:
```python
def llm_sentiment_analysis(text, aspects=None):
    prompt = f"""Analyze the sentiment of the following text.

Text: "{text}"

Provide:
1. Overall sentiment (positive/negative/neutral/mixed)
2. Confidence (0-1)
3. Key positive aspects mentioned
4. Key negative aspects mentioned
5. Notable emotional tones (joy, frustration, surprise, etc.)

{"Also rate sentiment specifically for these aspects: " + ", ".join(aspects) if aspects else ""}

Respond in JSON format."""

    response = llm.complete(prompt)
    return json.loads(response)
```

### Emotion Detection
Beyond positive/negative to specific emotions:
```python
from transformers import pipeline

# Multi-label emotion classification
emotion_classifier = pipeline(
    "text-classification",
    model="SamLowe/roberta-base-go_emotions",
    top_k=None
)

def detect_emotions(text):
    results = emotion_classifier(text)[0]
    # Filter to significant emotions
    significant = [r for r in results if r["score"] > 0.1]
    return sorted(significant, key=lambda x: x["score"], reverse=True)

# Example output:
# [{"label": "admiration", "score": 0.45},
#  {"label": "joy", "score": 0.32},
#  {"label": "gratitude", "score": 0.28}]
```

### Comparative Sentiment
Detect sentiment comparisons:
```python
def comparative_sentiment(text):
    """
    Detect: "A is better than B" patterns
    """
    prompt = f"""Analyze this text for comparative sentiment.

Text: "{text}"

If the text compares entities, identify:
1. Entity A (the preferred/better one)
2. Entity B (the less preferred/worse one)
3. Dimension of comparison (price, quality, etc.)
4. Strength of preference (slight, moderate, strong)

If no comparison, respond with: {{"comparison": false}}

Respond in JSON."""

    return llm.complete(prompt)
```

### Temporal Sentiment Tracking
Analyze sentiment over time:
```python
def sentiment_timeline(documents, time_field, window="day"):
    """
    Track sentiment trends over time.
    """
    # Analyze each document
    results = []
    for doc in documents:
        sentiment = analyze_sentiment(doc["text"])
        results.append({
            "timestamp": doc[time_field],
            "sentiment": sentiment["score"],
            "text": doc["text"]
        })

    # Aggregate by time window
    df = pd.DataFrame(results)
    df["window"] = df["timestamp"].dt.floor(window)

    trends = df.groupby("window").agg({
        "sentiment": ["mean", "std", "count"],
        "text": lambda x: list(x)[:3]  # Sample texts
    })

    return trends
```

### Sarcasm Detection
Handle sarcasm before sentiment analysis:
```python
def detect_sarcasm(text):
    """
    Detect potential sarcasm indicators.
    """
    indicators = {
        "exaggeration": bool(re.search(r'\b(best|worst|ever|always|never)\b', text.lower())),
        "air_quotes": '"' in text,
        "ellipsis": "..." in text,
        "positive_negative_mix": has_mixed_signals(text),
        "hashtags": "#sarcasm" in text.lower() or "#not" in text.lower()
    }

    # Use model for detection
    sarcasm_score = sarcasm_model.predict(text)

    return {
        "is_sarcastic": sarcasm_score > 0.5,
        "confidence": sarcasm_score,
        "indicators": indicators
    }

def sentiment_with_sarcasm(text):
    sarcasm = detect_sarcasm(text)
    base_sentiment = analyze_sentiment(text)

    if sarcasm["is_sarcastic"] and sarcasm["confidence"] > 0.7:
        # Flip sentiment
        return flip_sentiment(base_sentiment)
    return base_sentiment
```

## Common Pitfalls to Avoid

- Using generic models on domain-specific text
- Preprocessing away sentiment-relevant features (emoji, punctuation)
- Ignoring negation handling
- Treating neutral as absence of opinion vs explicit neutrality
- Not validating model outputs against human judgment
- Assuming sarcasm doesn't exist in your data
- Over-weighting extreme sentiments in aggregation
- Reporting sentiment without confidence/uncertainty
