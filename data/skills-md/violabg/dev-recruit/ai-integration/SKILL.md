---
name: ai-integration
description: Integrating AI and LLM capabilities into applications for enhanced functionalities. Use when implementing AI features, processing data with ML models, building generative workflows, or integrating AI APIs.
license: MIT
metadata:
  author: devrecruit
  version: "1.0"
compatibility: Requires Vercel AI SDK v6+, works with various LLM APIs (OpenAI, Anthropic, Groq) and AI services
---

# AI Integration Skills

This skill covers best practices for integrating artificial intelligence and large language models into applications using the Vercel AI SDK v6, including agent patterns, tool management, and advanced LLM integration patterns.

## Agents with AI SDK v6

### Purpose

Build production-ready AI agents that can autonomously use tools, make decisions, and handle multi-step tasks using the ToolLoopAgent abstraction in AI SDK v6.

### ToolLoopAgent Basics

The `ToolLoopAgent` class provides a complete agent implementation that handles the tool execution loop automatically:

```typescript
import { ToolLoopAgent } from "ai";
import { anthropic } from "@ai-sdk/anthropic";

export const weatherAgent = new ToolLoopAgent({
  model: anthropic("claude-3-5-sonnet-20241022"),
  instructions: "You are a helpful weather assistant.",
  tools: {
    weather: weatherTool,
    forecast: forecastTool,
  },
});

// Use the agent
const result = await weatherAgent.generate({
  prompt: "What is the weather in San Francisco?",
});

console.log(result.text);
```

### Streaming Agent Responses

Stream agent responses for real-time user feedback:

```typescript
import { createAgentUIStreamResponse } from "ai";

export async function POST(request: Request) {
  const { messages } = await request.json();

  return createAgentUIStreamResponse({
    agent: weatherAgent,
    uiMessages: messages,
  });
}
```

### Call Options and Dynamic Configuration

Customize agent behavior per request using call options:

````typescript
import { z } from 'zod';

const supportAgent = new ToolLoopAgent({
  model: anthropic('claude-3-5-sonnet-20241022'),
  callOptionsSchema: z.object({
    userId: z.string(),
    accountType: z.enum(['free', 'pro', 'enterprise']),
  }),
  prepareCall: ({ options, ...settings }) => ({
    ...settings,
    instructions:  with AI SDK v6

### Purpose

Connect to AI services and LLM APIs using the Vercel AI SDK v6 for unified API access across providers.

### Basic Text Generation

```typescript
// lib/services/ai/api-client.ts
import { generateText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

export async function generateText(prompt: string) {
  const { text } = await generateText({
    model: anthropic('claude-3-5-sonnet-20241022'),
    prompt,
    temperature: 0.7,
  });

  return text;
}
````

### Streaming Responses with AI SDK v6

```typescript
import { streamText } from "ai";

// Prefer server actions for AI operations
export async function streamTextResponse(prompt: string) {
  const result = streamText({
    model: anthropic("claude-3-5-sonnet-20241022"),
    prompt,
  });

  return result.toTextStreamResponse();
}

// Use API route ONLY for streaming responses (server actions don't support streaming yet)
// For non-streaming AI calls, use server actions instead
export async function POST(request: Request) {
  const { prompt } = await request.json();
  return streamTextResponse(prompt);
}

// For non-streaming AI generation, use server action:
("use server");
export async function generateQuizAction(params: QuizParams) {
  const user = await requireUser();

  const { text } = await generateText({
    model: anthropic("claude-3-5-sonnet-20241022"),
    prompt: buildQuizPrompt(params),
  });

  const quiz = await saveQuiz(text);
  updateTag("quizzes");

  return { success: true, data: quiz };
}
```

### Tool Definition and Execution (v6)

```typescript
import { tool } from "ai";
import { z } from "zod";

export const weatherTool = tool({
  description: "Get the weather in a location",
  inputSchema: z.object({
    location: z.string().describe("The city or location"),
  }),
  needsApproval: false, // Set to true for actions requiring user approval
  execute: async ({ location }) => {
    const weather = await fetchWeather(location);
    return {
      temperature: weather.temp,
      condition: weather.condition,
      location,
    };
  },
  // Control what the model sees
  toModelOutput: async ({ input, output }) => {
    return {
      type: "text",
      value: `The weather in ${input.location} is ${output.temperature}°F and ${output.condition}.`,
    };
  },
});
```

### Tool Execution Approval (Human-in-the-Loop)

```typescript
const deleteFileTool = tool({
  description: "Delete a file from the system",
  inputSchema: z.object({
    filePath: z.string(),
  }),
  // Require approval for destructive commands
  needsApproval: async ({ filePath }) => filePath.includes("rm -rf"),
  execute: async ({ filePath }) => {
    await deleteFile(filePath);
    return { success: true, filePath };
  },
});

// In your UI component
function DeleteToolView({
  invocation,
  addToolApprovalResponse,
}: {
  invocation: UIToolInvocation<typeof deleteFileTool>;
  addToolApprovalResponse: ChatAddToolApproveResponseFunction;
}) {
  if (invocation.state === "approval-requested") {
    return (
      <div>
        <p>Delete file: {invocation.input.filePath}?</p>
        <button
          onClick={() =>
            addToolApprovalResponse({
              id: invocation.approval.id,
              approved: true,
            })
          }
        >
          Approve
        </button>
        <button
          onClick={() =>
            addToolApprovalResponse({
              id: invocation.approval.id,
              approved: false,
            })
          }
        >
          Deny
        </button>
      </div>
    );
  }

  if (invocation.state === "output-available") {
    return <div>File deleted: {invocation.output.filePath}</div>;
  }
}
```

### Error Handling and Retry Logic with AI SDK v6

```typescript
import { generateText, LanguageModelError } from "ai";

async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (error instanceof LanguageModelError && attempt < maxRetries - 1) {
        const delay = baseDelay * Math.pow(2, attempt);
        await new Promise((resolve) => setTimeout(resolve, delay));
        continue;
      }
      throw error;
    }
  }
}

export async function generateWithRetry(prompt: string) {
  return callWithRetry(() =>
    generateText({
      model: anthropic("claude-3-5-sonnet-20241022"),
      prompt,
    })
  );
}
```

### Structured Output with Tool Calling

```typescript
import { Output, ToolLoopAgent } from "ai";

const agent = new ToolLoopAgent({
  model: anthropic("claude-3-5-sonnet-20241022"),
  tools: {
    searchDocs: documentSearchTool,
  },
  output: Output.object({
    schema: z.object({
      summary: z.string(),
      relevantDocs: z.array(z.string()),
      recommendations: z.array(z.string()),
    }),
  }),
});

const result = await agent.generate({
  prompt: "Find documentation about authentication",
});

console.log(result.output); // Strongly typed output
```

### Extended Token Usage Information

```typescript
const { text, usage } = await generateText({
  model: anthropic("claude-3-5-sonnet-20241022"),
  prompt: "Your prompt here",
});

// Access detailed usage breakdown
console.log(usage.inputTokens);
console.log(usage.outputTokens);
console.log(usage.inputTokenDetails?.cacheReadTokens); // Cache tokens
console.log(usage.outputTokenDetails?.reasoningTokens); // Reasoning tokens
console.log(usage.finishReason);
console.log(usage.rawFinishReason); // Provider-specific finish reason
```

### API Key Management with AI SDK v6

```typescript
// lib/env.ts
export const env = {
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  GROQ_API_KEY: process.env.GROQ_API_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
} as const;

// Validate environment variables
if (!env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY environment variable is not set');
}

// Never expose API keys to client
if (typeof window !== 'undefined') {
  throw new Error('API keys must not be loaded on client'
       model: "claude-3-5-sonnet-20241022",
       max_tokens: 1024,
       messages: [{ role: "user", content: prompt }],
     });

     for await (const event of stream) {
       if (event.type === "content_block_delta") {
         yield event.delta.text;
       }
     }
   }
```

3. **Error Handling and Retry Logic**

   ```typescript
   import { Anthropic, RateLimitError } from "@anthropic-ai/sdk";

   async function callWithRetry(
     fn: () => Promise<any>,
     maxRetries: number = 3,
     baseDelay: number = 1000
   ) {
     for (let attempt = 0; attempt < maxRetries; attempt++) {
       try {
         return await fn();
       } catch (error) {
         if (error instanceof RateLimitError && attempt < maxRetries - 1) {
           const delay = baseDelay * Math.pow(2, attempt);
           await new Promise((resolve) => setTimeout(resolve, delay));
           continue;
         }
         throw error;
       }
     }
   }

   export async function generateWithRetry(prompt: string) {
     return callWithRetry(() => generateText(prompt));
   }
   ```

4. **Request/Response Validation**

   ```typescript
   import { z } from "zod";

   const quizSchema = z.object({
     title: z.string(),
     questions: z.array(
       z.object({
         question: z.string(),
         type: z.enum(["multiple_choice", "open_question"]),
         options: z.array(z.string()).optional(),
         correctAnswer: z.string(),
       })
     ),
   });

   export async function generateValidatedQuiz(params: QuizParams) {
     const response = await generateText(buildPrompt(params));
     const parsed = JSON.parse(response);
     return quizSchema.parse(parsed);
   }
   ```

### API Key Management

````typescript
// lib/env.ts
export const env = {
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  GROQ_API_KEY: process.env.GROQ_API_KEY,
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
} as const;

// Never expose API keys to client
if (typeof window ! with SDK v6:

- [ ] Using Vercel AI SDK v6+ with latest features
- [ ] ToolLoopAgent is used for agent-based workflows
- [ ] Tools are properly defined with descriptions and schemas
- [ ] Tool execution approval is configured for sensitive operations
- [ ] API keys are stored securely in environment variables
- [ ] Error handling includes retry logic for transient failures
- [ ] Input data is validated and normalized
- [ ] Output is parsed, validated, and sanitized
- [ ] Response streaming is implemented for real-time UX
- [ ] Structured output is used with Output.object() or Output.array()
- [ ] Tool approval flow is implemented for human-in-the-loop
- [ ] Token usage is monitored for cost optimization
Prepare, validate, and process data for AI models to ensure quality inputs and reliable outputs.

### Input Processing

1. **Text Normalization**

   ```typescript
   export function normalizeText(text: string): string {
     return text.trim().replace(/\s+/g, " ").toLowerCase();
   }
````

2. **Chunking Long Documents**

   ```typescript
   export function chunkText(
     text: string,
     chunkSize: number = 1000,
     overlap: number = 100
   ): string[] {
     const chunks: string[] = [];
     let start = 0;

     while (start < text.length) {
       const end = Math.min(start + chunkSize, text.length);
       chunks.push(text.slice(start, end));
       start = end - overlap;
     }

     return chunks;
   }
   ```

3. **Prompt Template Building**

   ```typescript
   export function buildQuizPrompt(params: {
     position: string;
     difficulty: string;
     focusAreas: string[];
   }): string {
     return `
   You are an expert technical recruiter. Generate a quiz for the following position:
   
   Position: ${params.position}
   Difficulty Level: ${params.difficulty}
   Focus Areas: ${params.focusAreas.join(", ")}
   
   Requirements:
   - Generate 5-10 questions
   - Include a mix of question types
   - Ensure questions are clear and fair
   - Provide correct answers with explanations
   
   Return the quiz as a JSON object.
   `.trim();
   }
   ```

### Output Processing

1. **Response Parsing**

   ```typescript
   export function parseJsonResponse(content: string): Record<string, any> {
     const jsonMatch = content.match(/\{[\s\S]*\}/);
     if (!jsonMatch) throw new Error("No JSON found in response");
     return JSON.parse(jsonMatch[0]);
   }
   ```

2. **Data Sanitization**

   ```typescript
   import DOMPurify from "isomorphic-dompurify";

   export function sanitizeOutput(text: string): string {
     return DOMPurify.sanitize(text);
   }
   ```

3. **Post-Processing**
   ```typescript
   export function processQuizResponse(raw: any) {
     return {
       ...raw,
       questions: raw.questions.map((q: any) => ({
         ...q,
         question: sanitizeOutput(q.question),
         options: q.options?.map((o: string) => sanitizeOutput(o)),
       })),
     };
   }
   ```

### Performance Optimization

1. **Caching Results**

   ```typescript
   "use cache";
   import { cacheLife, cacheTag } from "next/cache";

   export async function getCachedQuizGeneration(params: QuizParams) {
     cacheLife({ max: 86400 }); // 24 hours
     cacheTag("ai-generated-quizzes");

     return await generateQuiz(params);
   }
   ```

2. **Batch Processing**

   ```typescript
   export async function batchEvaluateCandidates(
     candidates: string[],
     batchSize: number = 5
   ) {
     const results = [];

     for (let i = 0; i < candidates.length; i += batchSize) {
       const batch = candidates.slice(i, i + batchSize);
       const batchResults = await Promise.all(
         batch.map((candidate) => evaluateCandidate(candidate))
       );
       results.push(...batchResults);
     }

     return results;
   }
   ```

## Advanced Patterns

### Prompt Engineering

1. **System Prompts**

   ```typescript
   const SYSTEM_PROMPT = `
   You are an expert technical interviewer and recruiter.
   Your role is to evaluate candidates' technical competency and cultural fit.
   
   Guidelines:
   - Be fair and impartial
   - Consider multiple perspectives
   - Provide constructive feedback
   - Focus on learning potential, not just current knowledge
   `.trim();
   ```

2. **Few-Shot Examples**

   ```typescript
   const fewShotPrompt = `
   Example 1:
   Question: What is a closure in JavaScript?
   Answer: A closure is a function that has access to variables in another function's scope.
   Evaluation: Clear understanding, good explanation.
   
   Example 2:
   [More examples...]
   
   Now evaluate this answer:
   ${userAnswer}
   `;
   ```

3. **Chain-of-Thought Prompting**

   ```typescript
   const chainOfThoughtPrompt = `
   Let's think through this step by step:
   1. First, identify the key concepts
   2. Then, analyze each component
   3. Finally, provide your assessment
   
   ${userInput}
   `;
   ```

## Development Checklist

When integrating AI:

- [ ] AI operations are in server actions (not API routes) unless streaming
- [ ] API keys are stored securely in environment variables
- [ ] API calls include proper error handling and retry logic
- [ ] Input data is validated and normalized with Zod
- [ ] Output is parsed, validated, and sanitized
- [ ] Response streaming uses API routes only (server actions don't support streaming)
- [ ] Non-streaming AI calls use server actions for better type safety
- [ ] Rate limiting is handled appropriately
- [ ] Costs are tracked and optimized
- [ ] Results are cached where appropriate
- [ ] Cache invalidation (updateTag) is called after AI-generated mutations
- [ ] Fallback mechanisms exist for API failures
- [ ] Prompts are tested and version-controlled
- [ ] Data privacy and compliance requirements are met
- [ ] Performance is monitored in production
