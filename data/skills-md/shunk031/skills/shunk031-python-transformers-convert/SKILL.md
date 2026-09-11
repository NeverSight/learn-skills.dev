---
name: shunk031-python-transformers-convert
description: "Use this skill when converting custom PyTorch models to Hugging Face Transformers format. Helps with: (1) Creating PretrainedConfig and PreTrainedModel classes, (2) Writing ImageProcessor/Tokenizer, (3) Compatibility testing, (4) Hub upload preparation. Use when the user wants to make their model compatible with transformers library."
---

> [!NOTE]
> After reading this `SKILL.md`, say: `🤗 I read shunk031-python-transformers-convert.`

# Hugging Face Transformers Model Conversion

Convert custom PyTorch models to Hugging Face Transformers format while maintaining exact compatibility with the original implementation.

## Overview

This skill provides a systematic workflow for transformers conversion:

- Extract hardcoded values into PretrainedConfig
- Create PreTrainedModel wrapper
- Build ImageProcessor/Tokenizer
- Test equivalence thoroughly
- Prepare for Hub upload

**Important**: Use validation mode (parallel implementations) first to verify equivalence, then replace the original.

## Conversion Workflow

### Step 1: Analyze the Custom Model

Ask the user to specify:

- Path to the custom model implementation
- Model type (vision, text, multimodal)
- Task (classification, segmentation, generation, etc.)
- Validation mode or replacement mode

Then identify:

- Model architecture and components
- Input/output formats
- Key hyperparameters and hardcoded values
- Pretrained weights location
- Preprocessing pipeline
- Custom layers or modules

### Step 2: Create PretrainedConfig Class

**Key principle**: Extract ALL hardcoded values from the model as configurable parameters.

Template:

```python
from transformers import PretrainedConfig
from typing import List, Optional

class {ModelName}Config(PretrainedConfig):
    model_type = "{model_name}"

    def __init__(
        self,
        # Core architecture parameters
        hidden_dim: int = 128,
        num_layers: int = 4,

        # Input/output parameters
        image_size: int = 1024,
        num_channels: int = 3,
        num_labels: int = 1,

        # Component-specific parameters (extract from original)
        component_param: List[int] | None = None,

        **kwargs,
    ):
        super().__init__(**kwargs)

        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.image_size = image_size
        self.num_channels = num_channels
        self.num_labels = num_labels

        # Use default if not specified
        self.component_param = (
            component_param if component_param is not None else [1, 2, 4]
        )
```

**Critical**: Ensure default values match what the pretrained weights expect!

### Step 3: Create PreTrainedModel Class

Template:

```python
from transformers import PreTrainedModel
from transformers.modeling_outputs import SemanticSegmenterOutput

class {ModelName}ForTask(PreTrainedModel):
    config_class = {ModelName}Config

    def __init__(self, config: {ModelName}Config):
        super().__init__(config)
        self.config = config

        # Initialize layers using config parameters (no hardcoded values!)
        self.encoder = Encoder(
            hidden_dim=config.hidden_dim,
            num_layers=config.num_layers,
        )

    def forward(
        self,
        pixel_values: torch.FloatTensor,
        labels: Optional[torch.LongTensor] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
    ) -> Union[Tuple, SemanticSegmenterOutput]:
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # Forward pass
        logits = self.encoder(pixel_values)

        # Calculate loss if needed
        loss = None
        if labels is not None:
            # Compute loss
            pass

        if not return_dict:
            output = (logits,)
            return ((loss,) + output) if loss is not None else output

        return SemanticSegmenterOutput(
            loss=loss,
            logits=logits,
            hidden_states=None,
            attentions=None,
        )
```

### Step 4: Create ImageProcessor/Tokenizer

**For vision models** - Create ImageProcessor:

```python
from transformers import BaseImageProcessor

class {ModelName}ImageProcessor(BaseImageProcessor):
    model_input_names = ["pixel_values"]

    def __init__(
        self,
        size: int = 1024,
        resample: str = "bilinear",
        do_normalize: bool = True,
        image_mean: List[float] | None = None,
        image_std: List[float] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.size = size
        self.resample = resample
        self.do_normalize = do_normalize
        self.image_mean = image_mean if image_mean is not None else [0.485, 0.456, 0.406]
        self.image_std = image_std if image_std is not None else [0.229, 0.224, 0.225]

    def preprocess(
        self,
        images: ImageInput,
        return_tensors: Optional[Union[str, TensorType]] = None,
        **kwargs,
    ) -> BatchFeature:
        # Implement preprocessing matching original
        # Return BatchFeature with pixel_values
```

**For text models** - Create tokenizer configuration.

### Step 5: Create Compatibility Tests

**Critical**: Always use the SAME preprocessed tensor for both models when comparing outputs.

```python
import pytest
import torch

def test_preprocessing_matches():
    """Test that preprocessing is equivalent."""
    old_tensor = old_preprocessing(image)
    new_tensor = processor(image, return_tensors="pt")["pixel_values"][0]
    assert torch.allclose(old_tensor, new_tensor, atol=1e-6)

def test_single_image_output_matches():
    """Test that model outputs match."""
    # Load models
    old_model = OldModel()
    new_model = NewModel(NewConfig())
    new_model.load_state_dict(old_model.state_dict())

    # Prepare SAME input
    preprocessed = preprocess(image)

    with torch.no_grad():
        old_output = old_model(preprocessed)
        new_output = new_model(pixel_values=preprocessed)

    # Use 0.5% tolerance for numerical differences
    assert torch.allclose(old_output, new_output.logits, atol=5e-3, rtol=1e-2)

def test_batch_output_matches():
    """Test batch processing."""
    # Test with batch of images

def test_state_dict_compatible():
    """Test that weights can be loaded."""
    new_model.load_state_dict(old_model.state_dict())
```

### Step 6: Create MODEL_CARD.md

Generate comprehensive model card following Hugging Face standards. Include:

- Model description
- Usage examples
- Training details
- Evaluation metrics
- Citation information

See Hugging Face model card documentation for template.

### Step 7: Create Hub Push Script

**Critical**: Register classes with `register_for_auto_class()` before pushing.

```python
#!/usr/bin/env python3
from huggingface_hub import HfApi
from {module}.transformers import {ModelName}Config, {ModelName}ForTask, {ModelName}ImageProcessor

def main():
    # CRITICAL: Register for Auto* support
    {ModelName}Config.register_for_auto_class()
    {ModelName}ForTask.register_for_auto_class("AutoModel")
    {ModelName}ImageProcessor.register_for_auto_class("AutoImageProcessor")

    # Load original model
    original_model = OriginalModel()

    # Create transformers-compatible model
    config = {ModelName}Config()
    model = {ModelName}ForTask(config)
    model.load_state_dict(original_model.state_dict())

    # Save and push
    model.save_pretrained(local_dir)
    config.save_pretrained(local_dir)
    processor = {ModelName}ImageProcessor()
    processor.save_pretrained(local_dir)

    api = HfApi(token=token)
    api.create_repo(repo_id=repo_id, exist_ok=True)
    api.upload_folder(repo_id=repo_id, folder_path=local_dir)
```

## Implementation Strategy

### Validation Mode (Recommended First)

Create parallel implementations:

```
{project}/
├── {module}/
│   ├── original_model.py           # Existing
│   └── transformers/               # NEW - for validation
│       ├── __init__.py
│       ├── configuration_{model}.py
│       ├── modeling_{model}.py
│       └── processing_{model}.py
└── tests/
    └── test_transformers_compatibility.py
```

Workflow:

1. Create transformers/ package alongside original
2. Run compatibility tests
3. Debug any discrepancies
4. Once tests pass → proceed to replacement

### Replacement Mode (After Validation)

Once equivalence is verified:

```
{project}/
└── {module}/
    ├── configuration_{model}.py    # Replaces original
    ├── modeling_{model}.py
    └── processing_{model}.py
```

Workflow:

1. Remove or archive original implementation
2. Move transformers/\* files up one level
3. Update all imports
4. Update tests
5. Update documentation

## Common Issues

For detailed troubleshooting, see [references/common-pitfalls.md](references/common-pitfalls.md).

Quick reference:

- **Hardcoded values**: Extract to config with matching defaults
- **Preprocessing mismatches**: Use exact same pipeline and parameters
- **State dict keys**: Keep layer names matching original
- **Test tolerance**: Use 0.5% tolerance (5e-3) for numerical differences
- **Device handling**: Use `self.device` from PreTrainedModel
- **Image size order**: `post_process_semantic_segmentation()` expects `(width, height)`

## Debugging Strategy

If outputs don't match:

1. Check preprocessing produces identical tensors
2. Check state dict loaded correctly
3. Step-by-step comparison of each layer
4. Check device placement
5. Check determinism with torch.manual_seed

See [references/common-pitfalls.md](references/common-pitfalls.md) for detailed debugging steps.

## Project Learnings

After completing a conversion, add learnings to [references/learnings.md](references/learnings.md).

This accumulates knowledge from each project to avoid repeating mistakes.

## Checklist

- [ ] Step 1: Model analyzed
  - [ ] Architecture identified
  - [ ] Hyperparameters extracted
  - [ ] Preprocessing understood
- [ ] Step 2: Config class created
  - [ ] All hardcoded values moved to config
  - [ ] Defaults match pretrained weights
  - [ ] Type hints added
- [ ] Step 3: Model class created
  - [ ] Inherits from PreTrainedModel
  - [ ] Uses only config parameters
  - [ ] Forward signature matches conventions
- [ ] Step 4: Processor created
  - [ ] Preprocessing matches original
  - [ ] Returns appropriate format
- [ ] Step 5: Tests created
  - [ ] Preprocessing test passes
  - [ ] Single image test passes
  - [ ] Batch test passes
  - [ ] State dict test passes
- [ ] Step 6: MODEL_CARD.md created
  - [ ] All sections filled
  - [ ] Usage examples tested
  - [ ] Citations included
- [ ] Step 7: Push script created
  - [ ] register_for_auto_class() called
  - [ ] Script tested locally
  - [ ] Successfully pushed to Hub
- [ ] Cleanup (if doing replacement)
  - [ ] Original implementation removed/archived
  - [ ] Imports updated
  - [ ] Documentation updated
