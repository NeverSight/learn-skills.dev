---
name: file-converter-development
description: |
  Development guide for @rytass/file-converter base package (檔案轉換器開發指南). Use when creating new file converter adapters (新增檔案轉換 adapter), understanding converter interfaces, or building image processing pipelines. Covers Converter interface, ConverterManager, and Sharp integration patterns. Keywords: file converter, 檔案轉換, 圖片處理, image processing, Sharp, resize, watermark, transcode
---

# File Converter Adapter Development Guide (檔案轉換 Adapter 開發指南)

## Overview

本指南說明如何基於 `@rytass/file-converter` 基礎套件開發新的檔案轉換適配器。

## Base Package Architecture

```
@rytass/file-converter (Base)
├── ConvertableFile        # 輸入類型 (Readable | Buffer)
├── FileConverter<O>       # 轉換器介面
└── ConverterManager       # 管道式轉換管理器
```

## Core Interfaces

### FileConverter Interface

```typescript
import { Readable } from 'stream';

type ConvertableFile = Readable | Buffer;

interface FileConverter<O = Record<string, unknown>> {
  convert<Buffer>(file: ConvertableFile): Promise<Buffer>;
  convert<Readable>(file: ConvertableFile): Promise<Readable>;
}
```

### ConverterManager

```typescript
class ConverterManager {
  constructor(converters: FileConverter[]);

  convert<ConvertableFileFormat extends ConvertableFile>(
    file: ConvertableFile
  ): Promise<ConvertableFileFormat>;
}
```

> **注意**: ConverterManager 不提供 `pipe()` 方法。所有轉換器必須在建構時透過陣列傳入。

## Existing Adapters Reference

| Adapter | 功能 | 輸入 | 輸出 |
|---------|------|------|------|
| `image-resizer` | 圖片縮放 | Buffer / Readable | Buffer / Readable |
| `image-transcoder` | 格式轉換 | Buffer / Readable | Buffer / Readable |
| `image-watermark` | 浮水印疊加 | Buffer / Readable | Buffer / Readable |

## Implementing a New Adapter

### Step 1: Define Configuration

```typescript
// my-converter/src/typings.ts
export interface MyConverterOptions {
  someOption?: string;
  concurrency?: number;
  // ... other options
}
```

### Step 2: Implement FileConverter

```typescript
// my-converter/src/my-converter.ts
import { FileConverter, ConvertableFile } from '@rytass/file-converter';
import sharp from 'sharp';
import { Readable } from 'stream';
import { MyConverterOptions } from './typings';

sharp.cache(false);

export class MyConverter implements FileConverter<MyConverterOptions> {
  private readonly options: MyConverterOptions;

  constructor(options: MyConverterOptions) {
    this.options = options;

    // 設定 Sharp 並行處理數量
    sharp.concurrency(options.concurrency ?? 1);
  }

  async convert<Output extends ConvertableFile>(file: ConvertableFile): Promise<Output> {
    let converter;

    if (file instanceof Buffer) {
      converter = sharp(file);
    } else {
      converter = sharp();
    }

    // 套用轉換設定
    // converter.resize(...) 等

    // Stream 輸入需要 pipe
    if (file instanceof Readable) {
      file.pipe(converter);
    }

    // 根據輸入類型回傳對應輸出
    if (file instanceof Buffer) {
      return converter.toBuffer() as Promise<Output>;
    }

    return converter as Readable as Output;
  }
}
```

### Step 3: Export Package

```typescript
// my-converter/src/index.ts
export * from './typings';
export * from './my-converter';
```

## Actual Adapter Implementations

### ImageResizer (image-resizer)

實際選項介面：

```typescript
export interface ImageResizerOptions {
  maxWidth?: number;       // 最大寬度（必須提供 maxWidth 或 maxHeight 至少一個）
  maxHeight?: number;      // 最大高度（必須提供 maxWidth 或 maxHeight 至少一個）
  keepAspectRatio?: boolean;  // 保持比例（預設 true，使用 fit: 'inside'）
  concurrency?: number;    // Sharp 並行數（預設 1）
}
```

使用範例：

```typescript
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';

// 必須提供至少一個 maxWidth 或 maxHeight
const resizer = new ImageResizer({
  maxWidth: 800,
  maxHeight: 600,
  keepAspectRatio: true,  // 預設 true
  concurrency: 1,
});

// 轉換 - 支援 Buffer 或 Readable 輸入
const result = await resizer.convert<Buffer>(inputBuffer);
// 或
const resultStream = await resizer.convert<Readable>(inputStream);
```

**注意**: 使用 `withoutEnlargement: true`，不會放大小於目標尺寸的圖片。

### ImageTranscoder (image-transcoder)

實際選項介面（使用 Sharp 的格式特定選項）：

```typescript
import type { AvifOptions, GifOptions, HeifOptions, JpegOptions, PngOptions, TiffOptions, WebpOptions } from 'sharp';

// 根據目標格式使用對應的選項類型
type ImageTranscoderOptions =
  | ({ targetFormat: 'avif' } & AvifOptions)
  | ({ targetFormat: 'heif' } & HeifOptions)
  | ({ targetFormat: 'gif' } & GifOptions)
  | ({ targetFormat: 'tif' | 'tiff' } & TiffOptions)
  | ({ targetFormat: 'png' } & PngOptions)
  | ({ targetFormat: 'webp' } & WebpOptions)
  | ({ targetFormat: 'jpg' | 'jpeg' } & JpegOptions);

// constructor 實際接受的類型（額外包含 concurrency）
type ImageTranscoderConstructorOptions = ImageTranscoderOptions & { concurrency?: number };
```

支援的來源格式：`['jpg', 'png', 'webp', 'gif', 'avif', 'tif', 'svg']`

使用範例：

```typescript
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';

// 轉換為 WebP
const transcoder = new ImageTranscoder({
  targetFormat: 'webp',
  quality: 80,      // WebpOptions 的選項
  lossless: false,  // WebpOptions 的選項
  concurrency: 1,   // Sharp 並行數（預設 1）
});

// 轉換為 JPEG
const jpegTranscoder = new ImageTranscoder({
  targetFormat: 'jpeg',
  quality: 85,
  progressive: true,  // JpegOptions 的選項
});

// 轉換為 AVIF
const avifTranscoder = new ImageTranscoder({
  targetFormat: 'avif',
  quality: 50,
  effort: 4,  // AvifOptions 的選項
});

const result = await transcoder.convert<Buffer>(inputBuffer);
```

**注意**: 不支援的來源格式會拋出 `UnsupportedSource` 錯誤。

### ImageWatermark (image-watermark)

實際選項介面：

```typescript
import type { Gravity } from 'sharp';

type FilePath = string;

interface Watermark {
  image: FilePath | Buffer;  // 浮水印圖片（檔案路徑或 Buffer）
  gravity?: Gravity;         // Sharp gravity（預設 southeast 右下角）
}

export interface ImageWatermarkOptions {
  watermarks: Watermark[];   // 浮水印陣列（支援多個浮水印）
  concurrency?: number;      // Sharp 並行數（預設 1）
}
```

Sharp Gravity 值：

```typescript
import { gravity } from 'sharp';

// 可用的 gravity 值：
// gravity.north, gravity.northeast, gravity.east, gravity.southeast,
// gravity.south, gravity.southwest, gravity.west, gravity.northwest,
// gravity.center (或 gravity.centre)
```

使用範例：

```typescript
import { ImageWatermark } from '@rytass/file-converter-adapter-image-watermark';
import { gravity } from 'sharp';

// 單一浮水印
const watermark = new ImageWatermark({
  watermarks: [
    {
      image: watermarkBuffer,  // 或 '/path/to/watermark.png'
      gravity: gravity.southeast,  // 右下角（預設）
    },
  ],
});

// 多個浮水印
const multiWatermark = new ImageWatermark({
  watermarks: [
    { image: logoBuffer, gravity: gravity.northwest },   // 左上角
    { image: copyrightBuffer, gravity: gravity.south },  // 下方置中
  ],
  concurrency: 2,
});

const result = await watermark.convert<Buffer>(inputBuffer);
```

## Pipeline Usage

### Using ConverterManager

ConverterManager 允許串接多個轉換器，按順序執行轉換。

```typescript
import { ConverterManager } from '@rytass/file-converter';
import { ImageResizer } from '@rytass/file-converter-adapter-image-resizer';
import { ImageWatermark } from '@rytass/file-converter-adapter-image-watermark';
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';
import { gravity } from 'sharp';

// 建立轉換管線：縮放 → 浮水印 → 格式轉換
const manager = new ConverterManager([
  new ImageResizer({
    maxWidth: 800,
    maxHeight: 600,
    keepAspectRatio: true,
  }),
  new ImageWatermark({
    watermarks: [
      { image: watermarkBuffer, gravity: gravity.southeast },
    ],
  }),
  new ImageTranscoder({
    targetFormat: 'webp',
    quality: 85,
  }),
]);

// 執行轉換 (支援 Buffer 或 Readable 輸入)
const result = await manager.convert<Buffer>(inputBuffer);
```

> **注意**: 所有轉換器必須在建構 ConverterManager 時透過陣列傳入，不支援動態添加轉換器。

## Error Handling

### UnsupportedSource Error

ImageTranscoder 會在不支援的來源格式時拋出此錯誤：

```typescript
import { ImageTranscoder } from '@rytass/file-converter-adapter-image-transcoder';

try {
  const transcoder = new ImageTranscoder({ targetFormat: 'webp' });
  await transcoder.convert(unsupportedFormatBuffer);
} catch (error) {
  // UnsupportedSource 類別未從套件導出，需透過 message 判斷
  if (error instanceof Error && error.message === 'UnsupportedSource') {
    console.error('不支援的圖片格式');
  }
}
```

> **注意**: `UnsupportedSource` 錯誤類別和 `SupportSources` 常數目前未從套件導出，僅供內部使用。

## Testing Guidelines

```typescript
// __tests__/my-converter.spec.ts
import { MyConverter } from '../src';
import * as fs from 'fs';
import * as path from 'path';

describe('MyConverter', () => {
  const testImage = fs.readFileSync(path.join(__dirname, 'fixtures/test.jpg'));

  it('should convert image', async () => {
    const converter = new MyConverter({ someOption: 'value' });
    const result = await converter.convert<Buffer>(testImage);

    expect(result).toBeInstanceOf(Buffer);
    expect(result.length).toBeGreaterThan(0);
  });
});
```

## Package Structure

```
my-converter/
├── src/
│   ├── index.ts
│   ├── typings.ts
│   └── my-converter.ts
├── __tests__/
│   ├── fixtures/
│   │   └── test.jpg
│   └── my-converter.spec.ts
├── package.json
└── tsconfig.build.json
```

## Publishing Checklist

- [ ] 實現 `FileConverter<O>` 介面
- [ ] 定義清楚的選項介面 (Options type)
- [ ] 支援 `ConvertableFile` (Buffer 或 Readable) 輸入
- [ ] 支援 Buffer 和 Readable 輸出
- [ ] 設定 `sharp.cache(false)` 避免記憶體問題
- [ ] 支援 `concurrency` 選項控制 Sharp 並行數
- [ ] 與 ConverterManager 相容
- [ ] 撰寫單元測試（含測試圖片）
- [ ] 更新 README 含使用範例
- [ ] 遵循 `@rytass/file-converter-adapter-*` 命名規範
