---
name: Fine-Tuning Assistant
slug: fine-tuning-assistant
description: Guide model fine-tuning processes for customized AI performance
category: ai-ml
complexity: advanced
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "fine-tune model"
  - "fine-tuning"
  - "customize LLM"
  - "train custom model"
  - "adapt model"
tags:
  - fine-tuning
  - training
  - customization
  - LLM
  - machine-learning
---

# Fine-Tuning Assistant

The Fine-Tuning Assistant skill guides you through the process of adapting pre-trained models to your specific use case. Fine-tuning can dramatically improve model performance on specialized tasks, teach models your preferred style, and add capabilities that prompting alone cannot achieve.

This skill covers when to fine-tune versus prompt engineer, preparing training data, selecting base models, configuring training parameters, evaluating results, and deploying fine-tuned models. It applies modern techniques including LoRA, QLoRA, and instruction tuning to make fine-tuning practical and cost-effective.

Whether you are fine-tuning GPT models via API, running local training with open-source models, or using platforms like Hugging Face, this skill ensures you approach fine-tuning strategically and effectively.

## Core Workflows

### Workflow 1: Decide Whether to Fine-Tune
1. **Assess** the problem:
   - Can prompting achieve the goal?
   - Is the task format or style consistent?
   - Do you have quality training data?
   - Is this worth the investment?
2. **Compare** approaches:
   | Approach | When to Use | Investment |
   |----------|-------------|------------|
   | Better prompts | First attempt, variable tasks | Low |
   | Few-shot examples | Consistent format, limited data | Low |
   | RAG | Knowledge-intensive, dynamic data | Medium |
   | Fine-tuning | Consistent style, specialized task | High |
3. **Evaluate** requirements:
   - Minimum 100-1000 quality examples
   - Clear evaluation criteria
   - Budget for training and hosting
4. **Decision**: Fine-tune only if prompting/RAG insufficient

### Workflow 2: Prepare Fine-Tuning Dataset
1. **Collect** training examples:
   - Representative of target use case
   - High quality (no errors in outputs)
   - Diverse coverage of task variations
2. **Format** for training:
   ```jsonl
   {"messages": [
     {"role": "system", "content": "You are a helpful assistant..."},
     {"role": "user", "content": "User input here"},
     {"role": "assistant", "content": "Ideal response here"}
   ]}
   ```
3. **Quality assurance**:
   - Review sample of examples manually
   - Check for consistency in style/format
   - Remove duplicates and low-quality entries
4. **Split** train/validation/test sets
5. **Validate** dataset format

### Workflow 3: Execute Fine-Tuning
1. **Select** base model:
   - Consider size vs capability tradeoff
   - Match model to task complexity
   - Check licensing for your use case
2. **Configure** training:
   ```python
   # OpenAI fine-tuning
   training_config = {
       "model": "gpt-4o-mini-2024-07-18",
       "training_file": "file-xxx",
       "hyperparameters": {
           "n_epochs": 3,
           "batch_size": "auto",
           "learning_rate_multiplier": "auto"
       }
   }

   # LoRA fine-tuning (local)
   lora_config = {
       "r": 16,  # Rank
       "lora_alpha": 32,
       "lora_dropout": 0.05,
       "target_modules": ["q_proj", "v_proj"]
   }
   ```
3. **Monitor** training:
   - Watch loss curves
   - Check for overfitting
   - Validate on held-out set
4. **Evaluate** results:
   - Compare to baseline model
   - Test on diverse inputs
   - Check for regressions

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Decide approach | "Should I fine-tune for [task]" |
| Prepare data | "Format data for fine-tuning" |
| Choose model | "Which model to fine-tune for [task]" |
| Configure training | "Fine-tuning parameters for [goal]" |
| Evaluate results | "Evaluate fine-tuned model" |
| Debug training | "Fine-tuning loss not decreasing" |

## Best Practices

- **Start with Prompting**: Fine-tuning is expensive; exhaust cheaper options first
  - Can better prompts achieve 80% of the goal?
  - Try few-shot examples in the prompt
  - Consider RAG for knowledge tasks

- **Quality Over Quantity**: 100 excellent examples beat 10,000 mediocre ones
  - Each example should be a gold standard
  - Better to have humans verify examples
  - Remove anything you wouldn't want the model to learn

- **Match Format to Use Case**: Training examples should mirror real usage
  - Same prompt structure as production
  - Realistic input variations
  - Cover edge cases explicitly

- **Don't Over-Train**: More epochs isn't always better
  - Watch validation loss for overfitting
  - Start with 1-3 epochs
  - Early stopping when validation plateaus

- **Evaluate Properly**: Training loss isn't the goal
  - Use held-out test set
  - Compare to baseline on same tests
  - Check for capability regressions
  - Test on edge cases explicitly

- **Version Everything**: Fine-tuning is iterative
  - Version your training data
  - Track experiment configurations
  - Document what worked and what didn't

## Advanced Techniques

### LoRA (Low-Rank Adaptation)
Efficient fine-tuning for large models:
```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,                           # Rank of update matrices
    lora_alpha=32,                  # Scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA to base model
model = get_peft_model(base_model, lora_config)

# Only ~0.1% of parameters are trainable
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
```

### QLoRA (Quantized LoRA)
Fine-tune large models on consumer hardware:
```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config
)

# Apply LoRA on top
model = get_peft_model(model, lora_config)
```

### Instruction Tuning Dataset Creation
Convert raw data to instruction format:
```python
def create_instruction_example(raw_data):
    return {
        "messages": [
            {
                "role": "system",
                "content": "You are a customer service agent for TechCorp..."
            },
            {
                "role": "user",
                "content": f"Customer inquiry: {raw_data['inquiry']}"
            },
            {
                "role": "assistant",
                "content": raw_data['ideal_response']
            }
        ]
    }

# Apply to dataset
instruction_dataset = [create_instruction_example(d) for d in raw_dataset]
```

### Evaluation Framework
Comprehensive assessment of fine-tuned models:
```python
def evaluate_fine_tuned_model(model, test_set, baseline_model=None):
    results = {
        "task_accuracy": [],
        "format_compliance": [],
        "style_match": [],
        "regression_check": []
    }

    for example in test_set:
        output = model.generate(example.input)

        # Task-specific accuracy
        results["task_accuracy"].append(
            check_correctness(output, example.expected)
        )

        # Format compliance
        results["format_compliance"].append(
            matches_expected_format(output)
        )

        # Style matching (for style transfer tasks)
        results["style_match"].append(
            style_similarity(output, example.expected)
        )

        # Regression on general capabilities
        if baseline_model:
            results["regression_check"].append(
                compare_general_capability(model, baseline_model, example)
            )

    return {k: np.mean(v) for k, v in results.items()}
```

### Curriculum Learning
Order training data by difficulty:
```python
def create_curriculum(dataset):
    # Score examples by complexity
    scored = [(score_complexity(ex), ex) for ex in dataset]
    scored.sort(key=lambda x: x[0])

    # Create epochs with increasing difficulty
    n = len(scored)
    curriculum = {
        "epoch_1": [ex for _, ex in scored[:n//3]],           # Easy
        "epoch_2": [ex for _, ex in scored[:2*n//3]],         # Easy + Medium
        "epoch_3": [ex for _, ex in scored],                   # All
    }
    return curriculum
```

## Common Pitfalls to Avoid

- Fine-tuning when better prompting would suffice
- Using low-quality or inconsistent training examples
- Not holding out a proper test set
- Training for too many epochs (overfitting)
- Ignoring capability regressions from fine-tuning
- Not versioning training data and configurations
- Expecting fine-tuning to add factual knowledge (use RAG instead)
- Fine-tuning on data that doesn't match production use
