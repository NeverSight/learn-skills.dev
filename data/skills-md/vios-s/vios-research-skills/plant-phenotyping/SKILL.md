---
name: plant-phenotyping
description: Use this skill when the user is working on plant phenotyping with computer vision or AI agents — including leaf segmentation, trait estimation, conversational phenotyping systems, or multi-agent workflows for plant science. Triggers include "segment plant leaves", "count leaves automatically", "estimate plant traits from images", "build a phenotyping assistant", "leaf instance segmentation", "PhenoAssistant", "GMT for plant segmentation", or "multi-agent plant science pipeline". Do not use for generic instance segmentation not related to plants — use a general object detection skill instead.
license: MIT
metadata:
  category: "Domain: Plant Phenotyping"
  version: "0.1.0"
  author: "VIOS Lab, University of Edinburgh"
---

# Plant Phenotyping

A skill for designing and evaluating AI pipelines for plant phenotyping — covering leaf instance segmentation, trait estimation, and conversational multi-agent systems for plant science. VIOS has deep expertise here, including PhenoAssistant (conversational AI for phenotyping, Chen et al. 2024), GMT (graph-matching transformer for leaf instance segmentation, Guo et al. 2023), and multi-modal plant trait estimation.

## When to invoke this skill

- You are building a pipeline to segment individual plant leaves from overhead or side-view images
- You want to estimate quantitative plant traits (leaf area, leaf count, plant height, NDVI proxy) from images
- You are building a conversational AI system for phenotyping queries or lab automation
- You are working on multi-agent workflows that combine vision models, LLMs, and domain tools for plant science
- You want to benchmark a segmentation model on a standard plant phenotyping dataset (A1, Ara2013, CVppp)
- You are designing an active learning or data-efficient pipeline for trait annotation in crop science

## Background

Plant phenotyping bridges computer vision and plant biology: measuring visible plant traits from images to understand genotype-phenotype relationships, track growth, and improve crop breeding. The core challenges differ from medical imaging:

- **High intra-class variability**: same species looks different across growth stages, lighting, and camera angle
- **Severe occlusion**: mature rosette plants have leaves occluding each other — standard instance segmentation fails
- **Small datasets**: large-scale annotated plant datasets are rare; data-efficient methods are critical
- **Multi-modal inputs**: RGB, depth, hyperspectral, fluorescence — models must specify which modality they use
- **Biological interpretation**: outputs must be biologically interpretable traits, not just segmentation masks

## Workflow

### 1. Define the phenotyping task

Before any modelling, specify:

```
Task: [leaf segmentation / trait estimation / growth tracking / conversational query]
Input modality: [RGB / depth / hyperspectral / multi-modal]
Species: [Arabidopsis thaliana / tobacco / maize / wheat / other]
Growth stage: [seedling / vegetative / flowering]
Dataset: [A1 / Ara2013 / CVppp / CVPPP2017 / custom]
Primary output: [instance masks / leaf count / leaf area / trait table]
```

Different species and growth stages require different models. A model trained on Arabidopsis rosettes (2D overhead view, radial symmetry) will not transfer to maize or wheat without retraining.

### 2. Leaf instance segmentation

#### Standard datasets and splits

| Dataset | Species | Images | Annotations | Primary task |
|---------|---------|--------|-------------|--------------|
| A1 (CVPPP) | Arabidopsis | 128 | Instance masks | Leaf segmentation + count |
| Ara2013 | Arabidopsis | 624 | Instance masks | Leaf segmentation |
| CVPPP2017 | Arabidopsis, tobacco | ∼500 | Instance masks | Leaf segmentation + count |

Always use the official challenge split. Report on the test set — do not report only on validation.

#### Evaluation metrics

| Metric | Definition | Notes |
|--------|-----------|-------|
| SBD (Symmetric Best Dice) | Best-matching Dice averaged symmetrically | Primary metric for CVPPP; captures shape quality |
| DiC (Difference in Count) | |predicted count − true count| | Secondary; captures count accuracy |
| |DiC| (absolute DiC) | Mean absolute count error | Use alongside DiC |
| PQ (Panoptic Quality) | Detection × Segmentation quality | Required for newer benchmarks |

**Do not** report only mAP (COCO-style) for plant leaf segmentation — mAP is designed for diverse object categories and is misleading when all instances are the same class (leaf) with severe occlusion.

#### GMT protocol (Guo et al., 2023)

The Graph-Matching Transformer (GMT) addresses the severe occlusion problem by formulating leaf instance segmentation as a graph-matching problem:

1. Extract candidate leaf proposals (use a Mask R-CNN backbone or similar).
2. Build a graph where nodes are proposals and edges encode spatial overlap and appearance similarity.
3. Apply the graph-matching transformer to assign proposals to leaf instances — this handles cases where a single leaf is partially occluded by multiple neighbours.
4. Post-process: merge matched proposals into final instance masks.

When implementing GMT-style approaches, verify that the graph construction step correctly handles plants with > 20 leaves (memory scales quadratically with leaf count for dense adjacency).

### 3. Trait estimation

From instance segmentation outputs, derive quantitative traits:

**Standard trait pipeline:**
1. **Leaf count**: directly from the number of instance masks.
2. **Leaf area** (pixels): sum of pixel area per instance mask. Convert to cm² using the known camera calibration (mm/pixel).
3. **Projected rosette area**: convex hull of all instance masks combined.
4. **Compactness**: projected rosette area / sum of individual leaf areas (captures how overlapping the rosette is).
5. **Leaf shape descriptors**: for each leaf, fit an ellipse and report major/minor axis ratio, circularity.

**Camera calibration requirement**: Pixel-to-area conversion requires a calibration target in the image or a known camera-object distance. Always report the pixel/mm ratio used. If the calibration target is missing from some images, exclude those images rather than using an estimated ratio.

**Multi-modal trait estimation:**
- Chlorophyll content: requires fluorescence or hyperspectral input; cannot be reliably estimated from RGB alone
- 3D architecture (leaf angle, stem height): requires depth or stereo RGB
- Water stress indicators: NIR reflectance; report which wavelengths were used

### 4. PhenoAssistant: conversational AI for phenotyping

PhenoAssistant (Chen et al., 2024) is a conversational AI system that lets researchers query plant phenotyping data in natural language and chain vision model calls through an LLM orchestrator.

**Architecture:**

```
User query → LLM orchestrator → [Tool router]
                                     │
               ┌─────────────────────┼─────────────────────┐
               ▼                     ▼                     ▼
        Vision tool               Trait DB           Knowledge base
    (segmentation model)    (query by species,      (plant biology
                             growth stage, etc.)      literature)
               └─────────────────────┼─────────────────────┘
                                     ▼
                            Structured response
```

**Design principles for a PhenoAssistant-style system:**
1. **Tool separation**: keep vision models and LLM orchestration separate — do not fine-tune the LLM to produce pixel coordinates or segmentation masks. The LLM routes and synthesises; the vision model detects.
2. **Trait schema**: define a fixed JSON schema for all phenotyping outputs (leaf_count, leaf_area_cm2, growth_stage, confidence). The LLM receives this schema; users can then ask "compare leaf area across these three images."
3. **Provenance tracking**: each trait estimate must reference the image ID, model version, and calibration used — phenotyping results feed into biological databases, and reproducibility requires full provenance.
4. **Failure communication**: when the vision model fails (image quality too low, species not in training distribution), the system must communicate failure to the user in plain language, not silently return a low-confidence estimate.

### 5. Multi-agent workflows for plant science

For complex phenotyping pipelines that combine segmentation, trait extraction, database lookup, and biological interpretation:

**Agent decomposition:**

| Agent role | Responsibility | Tool access |
|------------|---------------|-------------|
| Image processor | Segmentation + trait extraction | Vision model APIs |
| Data analyst | Trait statistics, growth curves | Pandas / SQL |
| Literature agent | Retrieve relevant phenotyping papers | arXiv, PubPeer |
| Interpreter | Synthesise trait data + literature | LLM only |

**Orchestration pattern**: use a supervisor-worker pattern, not a fully autonomous chain. The supervisor (LLM) decides which agent to call based on the current query; workers execute and return structured results. Do not allow workers to call each other directly — this creates circular loops when models disagree.

**Evaluation of multi-agent phenotyping systems:**
- End-to-end accuracy: does the final trait estimate match manual measurement? Report RMSE and R² vs. manual.
- Task completion rate: % of queries that return a structured answer (vs. failure / refusal).
- Hallucination rate: % of biological claims in the response that are factually incorrect (requires manual audit of a sample).

### 6. Data-efficient methods

Plant phenotyping datasets are small. Data efficiency strategies, in order of typical impact:

1. **Pre-training on natural image datasets**: ImageNet pre-training helps for RGB-input models. Do not pre-train on COCO for leaf segmentation — COCO object shapes are very different from rosette leaves.
2. **Synthetic data augmentation**: generate synthetic plant images using `medical-image-synthesis` (diffusion) or classical augmentation (random rotation — plants have rotational symmetry, so arbitrary rotation is valid).
3. **Semi-supervised learning**: use unlabelled images from the same growth chamber. Report the label efficiency curve (performance vs. N annotated images).
4. **Transfer across species**: evaluate zero-shot transfer from Arabidopsis models to tobacco or maize. Report the transfer gap explicitly.

## Anti-patterns

- **Do not** train on CVPPP and evaluate on a custom RGB dataset without reporting domain gap — plant imaging conditions (growth chamber vs. field, camera angle, lighting) affect performance drastically.
- **Do not** use mAP as the primary metric for leaf instance segmentation — use SBD and DiC, which are the community standards for this task.
- **Do not** report pixel-area leaf area without stating the pixel/mm calibration — area in pixels is meaningless for biological comparison across datasets.
- **Do not** build a conversational phenotyping system where the LLM generates trait values directly — always route through a calibrated vision model. LLMs hallucinate numerical measurements.
- **Do not** claim a model works for field phenotyping based on growth-chamber evaluation — lighting variation and background complexity are an order of magnitude higher in the field.

## See also

- `medical-image-synthesis` for synthetic data generation to augment small plant phenotyping datasets.
- `causal-dag-builder` for encoding the causal relationship between genotype, growth conditions, and observed phenotypic traits before designing a study.
- `fairness-medical-imaging` for evaluating whether phenotyping models have performance gaps across growth conditions or imaging devices (analogous to scanner bias in medical imaging).
