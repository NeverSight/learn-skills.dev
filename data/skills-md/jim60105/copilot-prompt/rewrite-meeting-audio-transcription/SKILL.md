---
name: rewrite-meeting-audio-transcription
description: Rewrite raw meeting audio transcriptions into clean, accurate meeting minutes in Traditional Chinese. Use when the user has an unprocessed audio transcription file with recognition errors and needs it cleaned up into proper meeting minutes.
metadata:
  original-prompt: rewrite-meeting-audio-transcription.prompt.md
  output-language: 正體中文
  suggested-model: Claude Sonnet 4
---

# Rewrite Meeting Audio Transcription

Rewrite raw meeting audio transcriptions into clean, accurate meeting minutes.

## Steps

1. Read the entire transcription file completely.
2. Analyze what is correct and what contains transcription/recognition errors.
3. Produce a new meeting record.
4. Review the new record, confirming every point can be traced back to the transcription file.
5. Fix any errors found in the meeting record.

## Important Rules

- Base everything entirely on the provided transcription file.
- Do not generate imagined suggestions or future developments.
- Maintain chronological and causal ordering from beginning to end.
- Write in paragraphs. Only use bullet point lists when necessary.

## Wording Instructions

Use the following translation mappings: create = 建立, object = 物件, queue = 佇列, stack = 堆疊, information = 資訊, invocation = 呼叫, code = 程式碼, running = 執行, library = 函式庫, schematics = 原理圖, building = 建構, Setting up = 設定, package = 套件, video = 影片, for loop = for 迴圈, class = 類別, Concurrency = 平行處理, Transaction = 交易, Transactional = 交易式, Code Snippet = 程式碼片段, Code Generation = 程式碼產生器, Any Class = 任意類別, Scalability = 延展性, Dependency Package = 相依套件, Dependency Injection = 相依性注入, Reserved Keywords = 保留字, Metadata =  Metadata, Clone = 複製, Memory = 記憶體, Built-in = 內建, Global = 全域, Compatibility = 相容性, Function = 函式, Refresh = 重新整理, document = 文件, example = 範例, demo = 展示, quality = 品質, tutorial = 指南, recipes = 秘訣, byte = 位元組, bit = 位元

## Language Instructions

- Write in 正體中文 (zh-tw) unless the user specifies another language.
- Always communicate in 正體中文. Think of users as someone who can speak English but cannot read English.
- Use full-width punctuation marks.
- Always add a space between Chinese characters and alphanumeric characters.

Let's do this step by step.
