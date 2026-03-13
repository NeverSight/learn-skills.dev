---
name: transformers
description: State-of-the-art Machine Learning for PyTorch, TensorFlow, and JAX. Provides thousands of pretrained models to perform tasks on different modalities such as text, vision, and audio. The industry standard for Large Language Models (LLMs) and foundation models in science.
version: 4.37
license: Apache-2.0
---

# Hugging Face Transformers - Modern AI Models

Transformers provides APIs and tools to easily download and train state-of-the-art pretrained models. It reduces compute costs and carbon footprint by allowing researchers to reuse models instead of training from scratch.

## When to Use

- Natural Language Processing (Summarization, Translation, Named Entity Recognition).
- Scientific Sequence Analysis (Protein folding, DNA/RNA sequence modeling).
- Chemical Property Prediction (Using molecular strings like SMILES).
- Computer Vision (Vision Transformers - ViT, Image Classification).
- Time Series Forecasting with foundation models.
- Fine-tuning Large Language Models (LLMs) on domain-specific scientific literature.
- Multimodal tasks (Document AI, Visual Question Answering).

## Reference Documentation

**Official docs**: https://huggingface.co/docs/transformers/  
**Model Hub**: https://huggingface.co/models  
**Search patterns**: `pipeline`, `AutoModel`, `AutoTokenizer`, `Trainer`, `PEFT` (Parameter-Efficient Fine-Tuning)

## Core Principles

### The "Auto" Classes

Hugging Face uses "Auto" classes (`AutoModel`, `AutoTokenizer`) that automatically infer the correct architecture from the model name/path. This makes code highly portable.

### Tokenization

Before data enters a model, it must be converted into numerical tokens. The Tokenizer handles this, including padding, truncation, and special tokens (like `[CLS]`, `[SEP]`).

### Pipelines

The simplest way to use a model. It abstracts away tokenization, model execution, and post-processing into a single `pipe(data)` call.

## Quick Reference

### Installation

```bash
pip install transformers datasets tokenizers
# Requires a backend (PyTorch or JAX)
pip install torch
```

### Standard Imports

```python
from transformers import pipeline, AutoModel, AutoTokenizer, TrainingArguments, Trainer
import torch
```

### Basic Pattern - Using a Pretrained Pipeline

```python
from transformers import pipeline

# 1. Initialize a pipeline (automatically downloads model)
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# 2. Run inference
results = classifier("The molecular structure of this compound is fascinating.")
print(results)
```

## Critical Rules

### ✅ DO

- **Use the Auto Classes** - Always prefer `AutoTokenizer.from_pretrained()` and `AutoModel.from_pretrained()` for flexibility.
- **Set the Device** - Explicitly set `device=0` (for CUDA) or `device="mps"` (for Mac) in pipelines to ensure GPU acceleration.
- **Cache Models** - Models are large. Use the `HF_HOME` environment variable to manage where models are stored on disk.
- **Handle Truncation** - Most models have a maximum sequence length (usually 512). Always use `truncation=True` in tokenizers.
- **Use Datasets Library** - For training, use the `datasets` library to handle data loading and streaming without filling RAM.
- **Save Tokenizers with Models** - When fine-tuning, always save the tokenizer alongside the model to ensure consistency.

### ❌ DON'T

- **Load Models in a Loop** - Loading a model takes seconds and GBs of RAM. Load once, reuse many times.
- **Upload Private Data** - Be careful when using models that might send data to an API (though transformers is mostly local execution).
- **Ignore Padding** - For batch processing, ensure `padding=True` so all sequences in the batch have the same length.
- **Use Wrong Model for Task** - A "BERT" model is for understanding; "GPT" is for generation. Use the right architecture.

## Anti-Patterns (NEVER)

```python
from transformers import AutoModel, AutoTokenizer

# ❌ BAD: Re-initializing the model inside a function called frequently
def get_prediction(text):
    model = AutoModel.from_pretrained("bert-base-uncased") # ❌ SLOW & RAM HEAVY
    return model(text)

# ✅ GOOD: Load once globally or in a class
model = AutoModel.from_pretrained("bert-base-uncased")
def get_prediction(text):
    return model(text)

# ❌ BAD: Manual string splitting for "tokens"
# tokens = text.split(" ") # ❌ Not compatible with model vocabulary

# ✅ GOOD: Use the model's specific tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
inputs = tokenizer(text, return_tensors="pt")

# ❌ BAD: Forgetting to move model to GPU
# model = AutoModel.from_pretrained("...")
# output = model(inputs.to("cuda")) # ❌ Error: Model is on CPU!
```

## Tokenization Deep Dive

### Preparing Data for Models

```python
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

texts = ["Science is cool.", "Quantum physics is hard."]

# Batch encoding
inputs = tokenizer(
    texts, 
    padding=True, 
    truncation=True, 
    max_length=128, 
    return_tensors="pt" # Returns PyTorch tensors
)

print(inputs['input_ids'].shape) # (batch_size, seq_len)
```

## The Trainer API

### Simplified Training Loop

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    evaluation_strategy="epoch",
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
)

# trainer.train()
```

## Scientific Applications

### 1. Protein Sequence Analysis (ESM)

```python
# ESM-2 is a powerful protein language model
tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t6_8M_UR50D")
model = AutoModel.from_pretrained("facebook/esm2_t6_8M_UR50D")

protein_seq = "MAPLRKTYLLG"
inputs = tokenizer(protein_seq, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    # The 'last_hidden_state' represents a "feature vector" for each amino acid
    embeddings = outputs.last_hidden_state
```

### 2. Chemical Property Prediction (SMILES)

```python
# Using a model trained on molecular strings
pipe = pipeline("text-classification", model="seyonec/ChemBERTa-zinc-base-v1")

smiles = "CC(=O)Oc1ccccc1C(=O)O" # Aspirin
result = pipe(smiles)
print(f"Prediction: {result}")
```

### 3. Named Entity Recognition (NER) for Papers

```python
# Extracting genes, proteins, or chemicals from text
ner_pipe = pipeline("ner", model="dslim/bert-base-NER")
text = "The expression of the BRCA1 gene was observed in the sample."
entities = ner_pipe(text)
```

## Performance and Efficiency

### 1. Quantization (bitsandbytes)

Running large models on consumer GPUs by reducing precision (8-bit or 4-bit).

```python
from transformers import BitsAndBytesConfig

# Load model in 4-bit precision
quant_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModel.from_pretrained("model_name", quantization_config=quant_config)
```

### 2. Using pipeline with GPU

```python
# 'device=0' targets the first CUDA device
pipe = pipeline("translation_en_to_fr", model="t5-base", device=0)
```

## Common Pitfalls and Solutions

### "Out of Memory" (OOM) on GPU

```python
# ❌ Problem: Batch size is too large for GPU RAM
# ✅ Solution: 
# 1. Reduce 'per_device_train_batch_size'
# 2. Use 'gradient_accumulation_steps' to keep effective batch size
# 3. Use 'fp16=True' in TrainingArguments
```

### Model Output is a Dictionary, not a Tensor

```python
# ❌ Problem: outputs[0] works, but is confusing
# ✅ Solution: Access by name
outputs = model(**inputs)
hidden_states = outputs.last_hidden_state
```

### Slow Tokenization

```python
# ✅ Solution: Use "Fast" tokenizers (written in Rust, usually default)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=True)
```

Hugging Face Transformers has democratized AI for the scientific community. By providing a unified interface to the world's most powerful models, it allows researchers to spend less time on engineering and more time on discovering insights from data.
