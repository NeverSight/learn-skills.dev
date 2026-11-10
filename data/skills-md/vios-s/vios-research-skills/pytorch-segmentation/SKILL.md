---
name: pytorch-segmentation
description: Use this skill when implementing or evaluating image segmentation in PyTorch. Triggers include "implement semantic segmentation", "which loss function for segmentation", "compute mIoU in PyTorch", "set up a UNet with segmentation_models_pytorch", "evaluate segmentation with torchmetrics", "my Dice score is wrong", "class imbalance in segmentation", "multi-class segmentation evaluation", or "benchmark segmentation models". Handles architecture selection, loss functions, metric computation, data pipelines, and evaluation protocol. Do not use for instance segmentation benchmarks like COCO — use a separate detection skill.
license: MIT
metadata:
  category: "Domain: Computer Vision"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# PyTorch Segmentation

A practical skill for building, training, and evaluating segmentation models in PyTorch — covering architecture selection, loss functions, metric computation with `torchmetrics`, data augmentation with `albumentations`, and evaluation protocol. Grounded in real library APIs rather than pseudo-code.

## When to invoke this skill

- You are implementing semantic or binary segmentation from scratch or adapting a pre-trained model
- You need to compute Dice, IoU, or mIoU correctly (the wrong reduction is one of the most common bugs)
- You are choosing between segmentation libraries (`segmentation_models_pytorch`, `mmsegmentation`, `monai`)
- You have class imbalance (background >> foreground) and need an appropriate loss function
- You want to set up a reproducible evaluation protocol for a segmentation benchmark

## Architecture selection

### Library: `segmentation_models_pytorch` (SMP)

Best default for research: clean API, pre-trained encoder weights from ImageNet/medical data, supports most architectures.

```python
import segmentation_models_pytorch as smp

model = smp.Unet(
    encoder_name="resnet50",        # or "efficientnet-b4", "mit_b2" (SegFormer encoder)
    encoder_weights="imagenet",     # None to train from scratch
    in_channels=1,                  # 1 for grayscale (MRI, X-ray), 3 for RGB
    classes=4,                      # number of output classes including background
    activation=None,                # return logits; apply softmax/sigmoid outside
)
```

**Architecture guide:**

| Architecture | When to use |
|-------------|------------|
| `smp.Unet` | Default for medical imaging; strong skip connections for fine detail |
| `smp.DeepLabV3Plus` | Natural images; ASPP captures multi-scale context |
| `smp.Segformer` | Large datasets; transformer encoder; best ImageNet transfer |
| `smp.MAnet` | Multi-scale attention; useful when object scales vary |
| `monai.networks.nets.UNet` | 3D volumetric segmentation (CT, MRI volumes) |

For 3D volumes (e.g. cardiac MRI), use `monai` instead of SMP — SMP is 2D only.

## Loss functions

Class imbalance (background >> foreground) is the primary challenge. Never use vanilla cross-entropy alone.

### Binary segmentation (one foreground class)

```python
import segmentation_models_pytorch as smp

# Recommended default: Dice + BCE combo
loss_fn = smp.losses.DiceLoss(mode="binary") + smp.losses.SoftBCEWithLogitsLoss()

# Focal loss: better when foreground is very rare (<5% of pixels)
loss_fn = smp.losses.FocalLoss(mode="binary", alpha=0.25, gamma=2.0)
```

### Multi-class segmentation

```python
# Dice loss averaged over classes (macro) — treats all classes equally
loss_fn = smp.losses.DiceLoss(mode="multiclass", classes=None)  # None = all classes

# Ignore index for unlabelled pixels (common in cityscapes-style datasets)
loss_fn = smp.losses.DiceLoss(mode="multiclass", ignore_index=255)

# Tversky loss: control FP/FN trade-off (alpha=FP weight, beta=FN weight)
loss_fn = smp.losses.TverskyLoss(mode="multiclass", alpha=0.3, beta=0.7)
# alpha < 0.5 = penalise FP more; beta > 0.5 = penalise FN more
# Use alpha=0.3, beta=0.7 when missing a positive (FN) is clinically worse
```

**Common mistake:** SMP `DiceLoss` returns `1 - Dice` (a loss, not a score). Do not add it to BCE with a negative sign.

## Metric computation with `torchmetrics`

Use `torchmetrics` for all evaluation — it handles batch accumulation correctly and avoids the common mistake of averaging per-batch metrics.

### Binary segmentation

```python
from torchmetrics.segmentation import MeanIoU
from torchmetrics import Dice

dice_metric = Dice(num_classes=1, threshold=0.5).to(device)
iou_metric = MeanIoU(num_classes=2).to(device)  # 2 = background + foreground

# Inside eval loop:
preds = torch.sigmoid(logits)              # (B, 1, H, W) — probabilities
preds_binary = (preds > 0.5).long()       # (B, 1, H, W) — binary

dice_metric.update(preds_binary, masks)
iou_metric.update(preds_binary, masks)

# After all batches:
print(dice_metric.compute())   # scalar — accumulated over full dataset
print(iou_metric.compute())    # scalar — accumulated over full dataset
dice_metric.reset()
iou_metric.reset()
```

### Multi-class segmentation (mIoU)

```python
from torchmetrics.segmentation import MeanIoU

# num_classes includes background
miou_metric = MeanIoU(num_classes=num_classes, per_class=True).to(device)

preds_class = logits.argmax(dim=1)   # (B, H, W) — class indices

miou_metric.update(preds_class, masks)   # masks: (B, H, W) — class indices

per_class_iou = miou_metric.compute()  # tensor of shape (num_classes,)
miou = per_class_iou.mean()            # scalar mean IoU
miou_metric.reset()
```

**Report per-class IoU in a table, not just mIoU.** mIoU hides class-specific failures — a model can have 0.85 mIoU with 0.0 IoU on a rare but important class.

### Dice vs. IoU: which to report

| Context | Primary metric |
|---------|---------------|
| Medical imaging (binary or few classes) | Dice coefficient |
| Computer vision benchmarks (ADE20K, Cityscapes, Pascal VOC) | mIoU |
| MICCAI challenges | Usually Dice; check the challenge page |
| Both audiences | Report both |

Dice and IoU are monotonically related: `IoU = Dice / (2 - Dice)`. A model that ranks first on Dice will also rank first on IoU.

## Data pipeline

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

train_transform = A.Compose([
    A.RandomResizedCrop(height=512, width=512, scale=(0.5, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),       # skip for MRI — intensity is clinically meaningful
    A.Normalize(mean=[0.485, 0.456, 0.406],  # ImageNet stats for RGB; use dataset stats otherwise
                std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

val_transform = A.Compose([
    A.Resize(512, 512),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])
```

**Mask transform:** Albumentations applies the same spatial transform to both image and mask automatically when you pass `mask=mask` to the transform call. Intensity transforms (Normalize, Brightness) are applied only to the image.

For **medical images** (MRI, X-ray): do **not** use ImageNet normalisation stats. Compute per-dataset mean and std from the training set, or normalise to [0, 1] using `A.Normalize(mean=0, std=1)` with a dataset-specific min/max clip.

## Training loop skeleton

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-4)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)

for epoch in range(num_epochs):
    model.train()
    for images, masks in train_loader:
        images, masks = images.to(device), masks.to(device)
        logits = model(images)
        loss = loss_fn(logits, masks)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    scheduler.step()

    model.eval()
    with torch.no_grad():
        for images, masks in val_loader:
            images, masks = images.to(device), masks.to(device)
            logits = model(images)
            preds = logits.argmax(dim=1)
            miou_metric.update(preds, masks)
    val_miou = miou_metric.compute()
    miou_metric.reset()
```

**Gradient accumulation** for large models with small batch size:
```python
accumulation_steps = 4
optimizer.zero_grad()
for i, (images, masks) in enumerate(train_loader):
    loss = loss_fn(model(images), masks) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

## Evaluation protocol

1. **Never tune on the test set.** Use train/val split for hyperparameter search; report final numbers on test.
2. **Run 3 seeds**, report mean ± std. Segmentation models have non-trivial variance across seeds.
3. **Report both overall and per-class metrics** — mIoU alone is not sufficient.
4. **Boundary metrics** for fine-grained evaluation: `torchmetrics` does not have boundary F1 built in; use the `boundary_iou` implementation from the Mask2Former paper if needed.
5. **Statistical testing**: Wilcoxon signed-rank test (paired, per-image comparison) when comparing two models on the same test set.

## Anti-patterns

- **Do not** compute Dice as the mean of per-batch Dice scores — batch sizes vary and samples contribute unequally. Always accumulate TP/FP/FN across the full dataset and compute Dice at the end. `torchmetrics` does this correctly; manual implementations often don't.
- **Do not** use `torch.nn.CrossEntropyLoss` as your only loss on imbalanced segmentation data — it will converge to predicting background everywhere and report a misleadingly low loss.
- **Do not** apply `softmax` before `smp.losses.DiceLoss` in multi-class mode — SMP losses apply `softmax` internally; applying it twice gives wrong gradients.
- **Do not** use the same data normalisation stats for training and a new test domain — if the test set comes from a different scanner or dataset, recompute stats or use a domain-robust normalisation.
- **Do not** report mIoU computed from logits without a threshold/argmax — always apply `argmax` (multi-class) or threshold (binary) before metric computation.

## See also

- `cardiac-mri-analysis` for MRI-specific evaluation conventions (Dice, Hausdorff, Bland-Altman) and the ACDC/UK Biobank benchmarks.
- `fairness-medical-imaging` for evaluating segmentation model performance gaps across demographic subgroups.
- `medical-image-synthesis` for generating synthetic training data when annotations are scarce.
