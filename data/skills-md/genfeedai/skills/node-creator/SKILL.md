---
name: node-creator
description: Create custom Genfeed nodes using the SDK. Triggers on "create a new node", "add a custom node type", "build a node for X".
license: MIT
metadata:
  author: genfeedai
  version: "1.0.0"
---

# Node Creator

You are an expert at creating custom nodes for Genfeed using the SDK. When the user describes a node they want to create, you generate the complete TypeScript code for the node definition.

## SDK Overview

The Genfeed SDK provides a fluent builder API for creating custom nodes:

```typescript
import { createNode, registerNode } from '@genfeedai/sdk';

const myNode = createNode('myOrg/customNode')
  .name('My Custom Node')
  .description('Does something useful')
  .category('processing')
  .input('image', 'image', 'Input Image', { required: true })
  .output('image', 'image', 'Processed Image')
  .config({ key: 'intensity', type: 'slider', label: 'Intensity', min: 0, max: 100 })
  .process(async (data, ctx) => {
    // Processing logic
    return { outputs: { image: processedImageUrl } };
  })
  .build();

registerNode(myNode);
```

## Core Interfaces

### CustomNodeDefinition

```typescript
interface CustomNodeDefinition<TData extends CustomNodeData = CustomNodeData> {
  /** Unique identifier for the node type (e.g., 'myOrg/customNode') */
  type: string;

  /** Human-readable name displayed in the UI */
  name: string;

  /** Short description of what the node does */
  description: string;

  /** Category for organizing in the node palette */
  category: NodeCategory | 'custom';

  /** Icon name (Lucide icon names) */
  icon?: string;

  /** Input handles (data the node receives) */
  inputs: HandleDefinition[];

  /** Output handles (data the node produces) */
  outputs: HandleDefinition[];

  /** Default data values when creating a new instance */
  defaultData: Partial<TData>;

  /** Configuration schema for the node's settings panel */
  configSchema?: ConfigField[];

  /** Processing function executed when the node runs */
  process: NodeProcessor<TData>;

  /** Optional validation function */
  validate?: NodeValidator<TData>;

  /** Optional cost estimator for workflow cost calculations */
  estimateCost?: CostEstimator<TData>;
}
```

### HandleDefinition

```typescript
interface HandleDefinition {
  /** Unique ID within the node */
  id: string;

  /** Data type this handle accepts/produces */
  type: HandleType; // 'image' | 'text' | 'video' | 'number' | 'audio'

  /** Human-readable label */
  label: string;

  /** Can accept multiple connections (for inputs) */
  multiple?: boolean;

  /** Is this handle required? */
  required?: boolean;
}
```

### ConfigField

```typescript
interface ConfigField {
  /** Field key in node data */
  key: string;

  /** Field type */
  type: 'text' | 'number' | 'select' | 'checkbox' | 'slider' | 'textarea' | 'color';

  /** Human-readable label */
  label: string;

  /** Optional description/help text */
  description?: string;

  /** Default value */
  defaultValue?: unknown;

  /** Is this field required? */
  required?: boolean;

  /** Options for select fields */
  options?: Array<{ value: string; label: string }>;

  /** Min/max for number/slider fields */
  min?: number;
  max?: number;
  step?: number;

  /** Placeholder text */
  placeholder?: string;

  /** Conditional display based on other field values */
  showWhen?: Record<string, unknown>;
}
```

### ProcessorContext

```typescript
interface ProcessorContext {
  /** Node instance ID */
  nodeId: string;

  /** Current execution ID */
  executionId: string;

  /** Workflow ID */
  workflowId: string;

  /** Input values resolved from connected nodes */
  inputs: Record<string, unknown>;

  /** Update progress (0-100) */
  updateProgress: (percent: number, message?: string) => Promise<void>;

  /** Log a message */
  log: (message: string) => Promise<void>;

  /** Abort signal for cancellation */
  signal: AbortSignal;
}
```

### ProcessorResult

```typescript
interface ProcessorResult {
  /** Output values keyed by output handle ID */
  outputs: Record<string, unknown>;

  /** Optional metadata about the processing */
  metadata?: Record<string, unknown>;
}
```

## Handle Types

| Type | Description | Example Use Cases |
|------|-------------|-------------------|
| `image` | Image URL (string) | Photos, generated images, frames |
| `video` | Video URL (string) | Generated videos, clips |
| `audio` | Audio URL (string) | Voice, music, sound effects |
| `text` | Text string | Prompts, transcripts, captions |
| `number` | Numeric value | Counts, dimensions, timestamps |

## Node Categories

| Category | Description | Placement |
|----------|-------------|-----------|
| `input` | Data source nodes | Left side of canvas |
| `ai` | AI generation/processing | Middle-left |
| `processing` | Transform/modify media | Middle-right |
| `output` | Final output collectors | Right side |
| `composition` | Subworkflow nodes | Variable |
| `custom` | User-defined nodes | Based on function |

## Common Icons (Lucide)

```
Image, Video, AudioLines, MessageSquare, FileText, Sparkles, Brain, Mic,
Wand2, Layers, Scissors, Film, Crop, Maximize, Grid3X3, Pencil, Subtitles,
CheckCircle, GitBranch, ArrowRightToLine, Navigation
```

## NodeBuilder Methods

| Method | Description |
|--------|-------------|
| `.name(string)` | Set display name |
| `.description(string)` | Set description |
| `.category(string)` | Set category ('input', 'ai', 'processing', 'output', 'custom') |
| `.icon(string)` | Set Lucide icon name |
| `.input(id, type, label, options?)` | Add input handle |
| `.output(id, type, label, options?)` | Add output handle |
| `.config(ConfigField)` | Add configuration field |
| `.defaults(Partial<TData>)` | Set default data values |
| `.process(ProcessorFunction)` | Set processing function |
| `.validate(ValidatorFunction)` | Set validation function |
| `.cost(CostEstimator)` | Set cost estimator |
| `.build()` | Build the final definition |

## Example Nodes

### Image Filter Node

```typescript
import { createNode, registerNode } from '@genfeedai/sdk';

interface ImageFilterData {
  label: string;
  status: 'idle' | 'pending' | 'processing' | 'complete' | 'error';
  inputImage: string | null;
  outputImage: string | null;
  filterType: 'blur' | 'sharpen' | 'grayscale' | 'sepia';
  intensity: number;
}

const imageFilterNode = createNode<ImageFilterData>('custom/imageFilter')
  .name('Image Filter')
  .description('Apply visual filters to images')
  .category('processing')
  .icon('Wand2')
  .input('image', 'image', 'Input Image', { required: true })
  .output('image', 'image', 'Filtered Image')
  .config({
    key: 'filterType',
    type: 'select',
    label: 'Filter Type',
    defaultValue: 'blur',
    options: [
      { value: 'blur', label: 'Blur' },
      { value: 'sharpen', label: 'Sharpen' },
      { value: 'grayscale', label: 'Grayscale' },
      { value: 'sepia', label: 'Sepia' },
    ],
  })
  .config({
    key: 'intensity',
    type: 'slider',
    label: 'Intensity',
    defaultValue: 50,
    min: 0,
    max: 100,
    step: 1,
    showWhen: { filterType: ['blur', 'sharpen'] },
  })
  .defaults({
    label: 'Image Filter',
    status: 'idle',
    inputImage: null,
    outputImage: null,
    filterType: 'blur',
    intensity: 50,
  })
  .process(async (data, ctx) => {
    const { inputImage, filterType, intensity } = data;
    const imageUrl = ctx.inputs.image as string;

    await ctx.updateProgress(10, 'Applying filter...');

    // Call your filter API
    const response = await fetch('https://your-api.com/filter', {
      method: 'POST',
      body: JSON.stringify({ imageUrl, filterType, intensity }),
      signal: ctx.signal,
    });

    const result = await response.json();

    await ctx.updateProgress(100, 'Complete');

    return {
      outputs: { image: result.filteredImageUrl },
      metadata: { filterApplied: filterType },
    };
  })
  .validate((data, inputs) => {
    if (!inputs.image) {
      return { valid: false, errors: ['Input image is required'] };
    }
    return { valid: true };
  })
  .cost((data) => ({
    estimated: 0.01,
    description: 'Image filter processing',
  }))
  .build();

registerNode(imageFilterNode);
```

### Text Summarizer Node

```typescript
import { createNode, registerNode } from '@genfeedai/sdk';

interface TextSummarizerData {
  label: string;
  status: 'idle' | 'pending' | 'processing' | 'complete' | 'error';
  inputText: string | null;
  outputText: string | null;
  maxLength: number;
  style: 'bullet' | 'paragraph' | 'tldr';
}

const textSummarizerNode = createNode<TextSummarizerData>('custom/textSummarizer')
  .name('Text Summarizer')
  .description('Summarize long text into concise summaries')
  .category('ai')
  .icon('FileText')
  .input('text', 'text', 'Input Text', { required: true })
  .output('text', 'text', 'Summary')
  .config({
    key: 'style',
    type: 'select',
    label: 'Summary Style',
    defaultValue: 'paragraph',
    options: [
      { value: 'bullet', label: 'Bullet Points' },
      { value: 'paragraph', label: 'Paragraph' },
      { value: 'tldr', label: 'TL;DR' },
    ],
  })
  .config({
    key: 'maxLength',
    type: 'number',
    label: 'Max Length (words)',
    defaultValue: 100,
    min: 10,
    max: 500,
  })
  .defaults({
    label: 'Text Summarizer',
    status: 'idle',
    inputText: null,
    outputText: null,
    maxLength: 100,
    style: 'paragraph',
  })
  .process(async (data, ctx) => {
    const inputText = ctx.inputs.text as string;
    const { maxLength, style } = data;

    await ctx.updateProgress(20, 'Analyzing text...');

    // Call summarization API
    const summary = await summarizeText(inputText, { maxLength, style });

    await ctx.updateProgress(100, 'Complete');

    return {
      outputs: { text: summary },
    };
  })
  .build();

registerNode(textSummarizerNode);
```

### Video Watermark Node

```typescript
import { createNode, registerNode } from '@genfeedai/sdk';

interface VideoWatermarkData {
  label: string;
  status: 'idle' | 'pending' | 'processing' | 'complete' | 'error';
  inputVideo: string | null;
  inputImage: string | null;
  outputVideo: string | null;
  position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' | 'center';
  opacity: number;
  scale: number;
}

const videoWatermarkNode = createNode<VideoWatermarkData>('custom/videoWatermark')
  .name('Video Watermark')
  .description('Add a watermark image overlay to videos')
  .category('processing')
  .icon('Layers')
  .input('video', 'video', 'Input Video', { required: true })
  .input('image', 'image', 'Watermark Image', { required: true })
  .output('video', 'video', 'Watermarked Video')
  .config({
    key: 'position',
    type: 'select',
    label: 'Position',
    defaultValue: 'bottom-right',
    options: [
      { value: 'top-left', label: 'Top Left' },
      { value: 'top-right', label: 'Top Right' },
      { value: 'bottom-left', label: 'Bottom Left' },
      { value: 'bottom-right', label: 'Bottom Right' },
      { value: 'center', label: 'Center' },
    ],
  })
  .config({
    key: 'opacity',
    type: 'slider',
    label: 'Opacity',
    defaultValue: 80,
    min: 10,
    max: 100,
    step: 5,
  })
  .config({
    key: 'scale',
    type: 'slider',
    label: 'Scale (%)',
    defaultValue: 20,
    min: 5,
    max: 50,
    step: 5,
  })
  .defaults({
    label: 'Video Watermark',
    status: 'idle',
    inputVideo: null,
    inputImage: null,
    outputVideo: null,
    position: 'bottom-right',
    opacity: 80,
    scale: 20,
  })
  .process(async (data, ctx) => {
    const videoUrl = ctx.inputs.video as string;
    const watermarkUrl = ctx.inputs.image as string;
    const { position, opacity, scale } = data;

    await ctx.updateProgress(10, 'Processing video...');

    // Call watermark API (FFmpeg-based)
    const result = await addWatermark(videoUrl, watermarkUrl, {
      position,
      opacity: opacity / 100,
      scale: scale / 100,
    });

    await ctx.updateProgress(100, 'Complete');

    return {
      outputs: { video: result.outputUrl },
    };
  })
  .build();

registerNode(videoWatermarkNode);
```

### Multi-Input Combiner Node

```typescript
import { createNode, registerNode } from '@genfeedai/sdk';

interface ImageCombinerData {
  label: string;
  status: 'idle' | 'pending' | 'processing' | 'complete' | 'error';
  inputImages: string[];
  outputImage: string | null;
  layout: 'grid' | 'horizontal' | 'vertical';
  gap: number;
}

const imageCombinerNode = createNode<ImageCombinerData>('custom/imageCombiner')
  .name('Image Combiner')
  .description('Combine multiple images into a single image')
  .category('processing')
  .icon('Grid3X3')
  .input('images', 'image', 'Input Images', { multiple: true, required: true })
  .output('image', 'image', 'Combined Image')
  .config({
    key: 'layout',
    type: 'select',
    label: 'Layout',
    defaultValue: 'grid',
    options: [
      { value: 'grid', label: 'Grid' },
      { value: 'horizontal', label: 'Horizontal Strip' },
      { value: 'vertical', label: 'Vertical Strip' },
    ],
  })
  .config({
    key: 'gap',
    type: 'slider',
    label: 'Gap (pixels)',
    defaultValue: 10,
    min: 0,
    max: 50,
    step: 2,
  })
  .defaults({
    label: 'Image Combiner',
    status: 'idle',
    inputImages: [],
    outputImage: null,
    layout: 'grid',
    gap: 10,
  })
  .process(async (data, ctx) => {
    const images = ctx.inputs.images as string[];
    const { layout, gap } = data;

    if (images.length < 2) {
      throw new Error('At least 2 images required');
    }

    await ctx.updateProgress(20, `Combining ${images.length} images...`);

    const result = await combineImages(images, { layout, gap });

    await ctx.updateProgress(100, 'Complete');

    return {
      outputs: { image: result.combinedImageUrl },
    };
  })
  .build();

registerNode(imageCombinerNode);
```

## Backend Processor Pattern (BullMQ)

For nodes that require long-running jobs:

```typescript
// In your NestJS processor
import { Processor, WorkerHost } from '@nestjs/bullmq';
import { Job } from 'bullmq';

@Processor('custom-node-queue')
export class CustomNodeProcessor extends WorkerHost {
  async process(job: Job<CustomNodeJobData>) {
    const { nodeId, executionId, data, inputs } = job.data;

    // Update progress
    await job.updateProgress(10);

    // Do work...
    const result = await this.processNode(data, inputs);

    // Update progress
    await job.updateProgress(100);

    return result;
  }
}
```

## Registration Pattern

```typescript
// nodes/index.ts - Export all custom nodes
import { imageFilterNode } from './imageFilter';
import { textSummarizerNode } from './textSummarizer';
import { videoWatermarkNode } from './videoWatermark';

export const customNodes = [
  imageFilterNode,
  textSummarizerNode,
  videoWatermarkNode,
];

// Register all at once
import { nodeRegistry } from '@genfeedai/sdk';

nodeRegistry.registerAll(customNodes);
```

## Plugin Manifest

For distributing as a plugin:

```typescript
import { PluginManifest } from '@genfeedai/sdk';

export const manifest: PluginManifest = {
  name: '@myorg/genfeed-plugin-filters',
  version: '1.0.0',
  description: 'Image and video filter nodes for Genfeed',
  author: 'My Organization',
  license: 'MIT',
  nodes: ['custom/imageFilter', 'custom/videoWatermark'],
  minGenfeedVersion: '1.0.0',
  homepage: 'https://github.com/myorg/genfeed-plugin-filters',
};
```

## Instructions

When the user describes a custom node they want to create:

1. **Understand the purpose**: What does the node do? What inputs/outputs does it need?
2. **Define the data interface**: Create a typed interface for the node's data
3. **Choose appropriate handles**: Select input/output types based on data flow
4. **Design configuration**: Add config fields for user-adjustable settings
5. **Implement processing**: Write the async process function with progress updates
6. **Add validation**: Include input validation where appropriate
7. **Estimate costs**: Add cost estimation if the node uses paid APIs

Always output complete, runnable TypeScript code that follows the SDK patterns.
