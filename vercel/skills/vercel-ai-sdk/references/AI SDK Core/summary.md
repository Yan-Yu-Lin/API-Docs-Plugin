# AI SDK Core - Comprehensive Summary

This document provides a detailed summary of the AI SDK Core documentation, covering all key concepts, API patterns, and best practices for working with large language models (LLMs) in your applications.

---

## Table of Contents

1. [Overview](#overview)
2. [Generating and Streaming Text](#generating-and-streaming-text)
3. [Generating Structured Data](#generating-structured-data)
4. [Tool Calling](#tool-calling)
5. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
6. [Prompt Engineering](#prompt-engineering)
7. [Settings](#settings)
8. [Embeddings](#embeddings)
9. [Image Generation](#image-generation)
10. [Transcription](#transcription)
11. [Speech](#speech)
12. [Language Model Middleware](#language-model-middleware)
13. [Provider and Model Management](#provider-and-model-management)
14. [Error Handling](#error-handling)
15. [Testing](#testing)
16. [Telemetry](#telemetry)

---

## Overview

AI SDK Core simplifies working with LLMs by offering a standardized way of integrating them into applications. It provides functions designed for text generation, structured data generation, and tool usage with a standardized approach to prompts and settings.

### Core Functions

- **`generateText`**: Generates text and tool calls. Ideal for non-interactive use cases like automation tasks (drafting emails, summarizing web pages) and agents that use tools.
- **`streamText`**: Streams text and tool calls. Used for interactive use cases like chatbots and content streaming.
- **`generateObject`**: Generates typed, structured objects matching a Zod schema. Used for information extraction, synthetic data generation, or classification tasks.
- **`streamObject`**: Streams structured objects matching a Zod schema. Used for streaming generated UIs.

---

## Generating and Streaming Text

### generateText Function

The `generateText` function generates text for a given prompt and model. It's ideal for non-interactive use cases.

```ts
import { generateText } from 'ai';

const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a vegetarian lasagna recipe for 4 people.',
});
```

**Advanced prompts with system messages:**

```ts
const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  system: 'You are a professional writer. You write simple, clear, and concise content.',
  prompt: `Summarize the following article in 3-5 sentences: ${article}`,
});
```

**Result object properties:**
- `result.text`: The generated text
- `result.content`: The content generated in the last step
- `result.reasoning` / `result.reasoningText`: Model reasoning (when available)
- `result.files`: Generated files
- `result.sources`: Sources used as references
- `result.toolCalls` / `result.toolResults`: Tool call information
- `result.finishReason`: Why the model finished generating
- `result.usage` / `result.totalUsage`: Token usage information
- `result.warnings`: Provider warnings
- `result.request` / `result.response`: Request/response metadata
- `result.providerMetadata`: Provider-specific metadata
- `result.steps`: Details for all steps in multi-step generations

### streamText Function

The `streamText` function streams text from LLMs for real-time interactive use cases.

```ts
import { streamText } from 'ai';

const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Invent a new holiday and describe its traditions.',
});

for await (const textPart of result.textStream) {
  console.log(textPart);
}
```

**Key features:**
- `result.textStream` is both a `ReadableStream` and an `AsyncIterable`
- Uses backpressure - only generates tokens as requested
- Immediately starts streaming (errors are suppressed by default)

**Helper functions for UI integration:**
- `result.toUIMessageStreamResponse()`: Creates UI Message stream HTTP response
- `result.pipeUIMessageStreamToResponse()`: Writes UI Message stream to Node.js response
- `result.toTextStreamResponse()`: Creates simple text stream HTTP response
- `result.pipeTextStreamToResponse()`: Writes text delta to Node.js response

**Callbacks:**
- `onError`: Triggered when errors occur during streaming
- `onChunk`: Triggered for each chunk (text, reasoning, source, tool-call, tool-result, raw)
- `onFinish`: Triggered when stream finishes with text, usage, finish reason, messages, steps

**fullStream property:**
Provides access to all stream events for custom UI implementations, including: `start`, `start-step`, `text-start`, `text-delta`, `text-end`, `reasoning-start`, `reasoning-delta`, `reasoning-end`, `source`, `file`, `tool-call`, `tool-input-start`, `tool-input-delta`, `tool-input-end`, `tool-result`, `tool-error`, `finish-step`, `finish`, `error`, `raw`.

### Stream Transformation

Use `experimental_transform` to transform streams (filtering, changing, or smoothing text):

```ts
import { smoothStream, streamText } from 'ai';

const result = streamText({
  model,
  prompt,
  experimental_transform: smoothStream(),
});
```

**Custom transformations** can convert text, stop streams conditionally, or apply multiple transformations in sequence.

### Sources

Some providers (Perplexity, Google Generative AI) include URL sources in responses with properties: `id`, `url`, `title`, and `providerMetadata`.

---

## Generating Structured Data

### generateObject Function

Generates structured data from prompts, validated against a schema.

```ts
import { generateObject } from 'ai';
import { z } from 'zod';

const { object } = await generateObject({
  model: 'anthropic/claude-sonnet-4.5',
  schema: z.object({
    recipe: z.object({
      name: z.string(),
      ingredients: z.array(z.object({ name: z.string(), amount: z.string() })),
      steps: z.array(z.string()),
    }),
  }),
  prompt: 'Generate a lasagna recipe.',
});
```

### streamObject Function

Streams structured data for interactive use cases:

```ts
import { streamObject } from 'ai';

const { partialObjectStream } = streamObject({ /* ... */ });

for await (const partialObject of partialObjectStream) {
  console.log(partialObject);
}
```

### Output Strategies

- **Object** (default): Returns generated data as an object
- **Array**: Generates array of objects with `elementStream` for streaming elements
- **Enum**: Generates specific enum values for classification tasks
- **No Schema**: Dynamic requests without schema validation

```ts
// Array output
const { elementStream } = streamObject({
  model: 'anthropic/claude-sonnet-4.5',
  output: 'array',
  schema: z.object({ name: z.string(), class: z.string() }),
  prompt: 'Generate 3 hero descriptions.',
});

// Enum output
const { object } = await generateObject({
  model: 'anthropic/claude-sonnet-4.5',
  output: 'enum',
  enum: ['action', 'comedy', 'drama', 'horror', 'sci-fi'],
  prompt: 'Classify the genre of this movie plot...',
});
```

### Schema Name and Description

Provide additional guidance to the model:

```ts
const { object } = await generateObject({
  model: 'anthropic/claude-sonnet-4.5',
  schemaName: 'Recipe',
  schemaDescription: 'A recipe for a dish.',
  schema: z.object({ /* ... */ }),
  prompt: 'Generate a lasagna recipe.',
});
```

### Error Handling

`AI_NoObjectGeneratedError` is thrown when generation fails. The error includes `text`, `response`, `usage`, and `cause` properties.

### Repairing Invalid JSON

Use `experimental_repairText` to attempt repairs on malformed JSON:

```ts
const { object } = await generateObject({
  model,
  schema,
  prompt,
  experimental_repairText: async ({ text, error }) => {
    return text + '}'; // Example repair
  },
});
```

### Structured Outputs with generateText/streamText

Use `experimental_output` for structured data with tool calling:

```ts
const { experimental_output } = await generateText({
  experimental_output: Output.object({
    schema: z.object({ name: z.string(), age: z.number().nullable() }),
  }),
  prompt: 'Generate an example person for testing.',
});
```

---

## Tool Calling

Tools are objects the model can call to perform specific tasks. Each tool has:
- **description**: Optional description influencing tool selection
- **inputSchema**: Zod or JSON schema for input validation
- **execute**: Optional async function called with tool inputs

```ts
import { z } from 'zod';
import { generateText, tool } from 'ai';

const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: {
    weather: tool({
      description: 'Get the weather in a location',
      inputSchema: z.object({
        location: z.string().describe('The location to get the weather for'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72 + Math.floor(Math.random() * 21) - 10,
      }),
    }),
  },
  prompt: 'What is the weather in San Francisco?',
});
```

### Multi-Step Calls

Use `stopWhen` for multi-step tool calling:

```ts
const { text, steps } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: { weather: weatherTool },
  stopWhen: stepCountIs(5),
  prompt: 'What is the weather in San Francisco?',
});
```

### Callbacks and Hooks

- **`onStepFinish`**: Called when a step completes
- **`prepareStep`**: Called before each step, allows modifying settings

### Response Messages

Use `response.messages` to add assistant and tool messages to conversation history.

### Dynamic Tools

Use `dynamicTool` for tools with unknown schemas at compile time:

```ts
const customTool = dynamicTool({
  description: 'Execute a custom function',
  inputSchema: z.object({}),
  execute: async input => {
    const { action, parameters } = input as any;
    return { result: `Executed ${action}` };
  },
});
```

### Preliminary Tool Results

Return `AsyncIterable` for streaming status during tool execution:

```ts
tool({
  async *execute({ location }) {
    yield { status: 'loading', text: `Getting weather for ${location}` };
    await new Promise(resolve => setTimeout(resolve, 3000));
    yield { status: 'success', text: `The weather is 72F`, temperature: 72 };
  },
});
```

### Tool Choice

Control when tools are selected:
- `auto`: Model chooses whether to call tools
- `required`: Model must call a tool
- `none`: Model must not call tools
- `{ type: 'tool', toolName: string }`: Model must call specific tool

### Tool Execution Options

Tools receive additional options: `toolCallId`, `messages`, `abortSignal`, and `experimental_context`.

### Tool Input Lifecycle Hooks

- `onInputStart`: Called when model starts generating tool input
- `onInputDelta`: Called for each chunk during streaming
- `onInputAvailable`: Called when complete input is available

### Error Handling

Three tool-related errors:
- `NoSuchToolError`: Unknown tool called
- `InvalidToolInputError`: Invalid tool inputs
- `ToolCallRepairError`: Error during repair

### Tool Call Repair

Use `experimental_repairToolCall` to fix invalid tool calls without polluting message history.

### Active Tools

Limit available tools with `activeTools`:

```ts
const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: myToolSet,
  activeTools: ['firstTool'],
});
```

### Multi-modal Tool Results

Use `toModelOutput` to convert screenshots and other media for model consumption.

---

## Model Context Protocol (MCP)

MCP enables AI applications to discover and use tools across services through a standardized interface.

### Transport Options

**HTTP Transport (Recommended for production):**

```ts
import { experimental_createMCPClient as createMCPClient } from '@ai-sdk/mcp';

const mcpClient = await createMCPClient({
  transport: {
    type: 'http',
    url: 'https://your-server.com/mcp',
    headers: { Authorization: 'Bearer my-api-key' },
    authProvider: myOAuthClientProvider,
  },
});
```

**SSE Transport:**

```ts
const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'https://my-server.com/sse',
    headers: { Authorization: 'Bearer my-api-key' },
  },
});
```

**Stdio Transport (Local servers only):**

```ts
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const mcpClient = await createMCPClient({
  transport: new StdioClientTransport({
    command: 'node',
    args: ['src/stdio/dist/server.js'],
  }),
});
```

### Using MCP Tools

**Schema Discovery:**
```ts
const tools = await mcpClient.tools();
```

**Schema Definition (for type safety):**
```ts
const tools = await mcpClient.tools({
  schemas: {
    'get-data': {
      inputSchema: z.object({
        query: z.string().describe('The data query'),
        format: z.enum(['json', 'text']).optional(),
      }),
    },
  },
});
```

### MCP Resources

- `mcpClient.listResources()`: List available resources
- `mcpClient.readResource({ uri })`: Read resource contents
- `mcpClient.listResourceTemplates()`: List resource templates

### MCP Prompts

- `mcpClient.listPrompts()`: List available prompts
- `mcpClient.getPrompt({ name, arguments })`: Get prompt messages

### Elicitation Handling

Enable and handle server requests for additional information:

```ts
const mcpClient = await experimental_createMCPClient({
  transport: { type: 'sse', url: 'https://your-server.com/sse' },
  capabilities: { elicitation: {} },
});

mcpClient.onElicitationRequest(ElicitationRequestSchema, async request => {
  const userInput = await getInputFromUser(request.params.message);
  return { action: 'accept', content: userInput };
});
```

### Closing MCP Clients

Close clients appropriately based on usage pattern:
- Short-lived: Close when response finishes
- Long-running: Close when application terminates

---

## Prompt Engineering

### Tips for Tool Prompts

1. Use strong tool-calling models (gpt-5, gpt-4.1)
2. Keep number of tools low (5 or less)
3. Keep tool parameter complexity low
4. Use semantically meaningful names
5. Add `.describe()` to Zod schema properties
6. Use tool `description` field for output information
7. Include example input/outputs in prompts

### Schema Tips

**Zod Dates:**
Use `z.string().date()` with transformer for Date objects:

```ts
date: z.string().date().transform(value => new Date(value))
```

**Optional Parameters:**
Use `.nullable()` instead of `.optional()` for strict schema validation compatibility:

```ts
workdir: z.string().nullable() // Works with strict validation
```

**Temperature Settings:**
Use `temperature: 0` for tool calls and object generation for deterministic results.

### Debugging

**Inspecting Warnings:**
```ts
console.log(result.warnings);
```

**HTTP Request Bodies:**
```ts
console.log(result.request.body);
```

---

## Settings

Common settings supported by all AI SDK functions:

| Setting | Description |
|---------|-------------|
| `maxOutputTokens` | Maximum tokens to generate |
| `temperature` | Randomness control (0 = deterministic) |
| `topP` | Nucleus sampling (0-1) |
| `topK` | Top K sampling (advanced) |
| `presencePenalty` | Penalty for repeating prompt information |
| `frequencyPenalty` | Penalty for repeated words/phrases |
| `stopSequences` | Sequences that stop generation |
| `seed` | Integer for deterministic results |
| `maxRetries` | Maximum retries (default: 2) |
| `abortSignal` | Cancel call or set timeout |
| `headers` | Additional HTTP headers |

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  maxOutputTokens: 512,
  temperature: 0.3,
  maxRetries: 5,
  abortSignal: AbortSignal.timeout(5000),
  prompt: 'Invent a new holiday.',
});
```

---

## Embeddings

### Single Value Embedding

```ts
import { embed } from 'ai';

const { embedding } = await embed({
  model: 'openai/text-embedding-3-small',
  value: 'sunny day at the beach',
});
```

### Batch Embedding

```ts
import { embedMany } from 'ai';

const { embeddings } = await embedMany({
  model: 'openai/text-embedding-3-small',
  values: [
    'sunny day at the beach',
    'rainy afternoon in the city',
    'snowy night in the mountains',
  ],
});
```

### Similarity Calculation

```ts
import { cosineSimilarity, embedMany } from 'ai';

const { embeddings } = await embedMany({
  model: 'openai/text-embedding-3-small',
  values: ['sunny day at the beach', 'rainy afternoon in the city'],
});

console.log(`cosine similarity: ${cosineSimilarity(embeddings[0], embeddings[1])}`);
```

### Settings

- **Provider Options**: Configure dimensions and other provider-specific settings
- **Parallel Requests**: `maxParallelCalls` for batch processing
- **Retries**: `maxRetries` parameter
- **Abort Signals**: `abortSignal` for cancellation
- **Custom Headers**: `headers` parameter

### Embedding Providers

| Provider | Model | Dimensions |
|----------|-------|------------|
| OpenAI | text-embedding-3-large | 3072 |
| OpenAI | text-embedding-3-small | 1536 |
| Google | gemini-embedding-001 | 3072 |
| Mistral | mistral-embed | 1024 |
| Cohere | embed-english-v3.0 | 1024 |
| Amazon Bedrock | amazon.titan-embed-text-v2:0 | 1024 |

---

## Image Generation

Image generation is an experimental feature.

```ts
import { experimental_generateImage as generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const { image } = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'Santa Claus driving a Cadillac',
});

const base64 = image.base64;
const uint8Array = image.uint8Array;
```

### Settings

- **Size**: Format `{width}x{height}` (e.g., '1024x1024')
- **Aspect Ratio**: Format `{width}:{height}` (e.g., '16:9')
- **Multiple Images**: Use `n` parameter
- **Seed**: For reproducible results
- **Provider Options**: Model-specific settings (e.g., `style: 'vivid'`)

### Image Generation with Language Models

Some language models (Google gemini-2.5-flash-image-preview) support multi-modal outputs:

```ts
const result = await generateText({
  model: google('gemini-2.5-flash-image-preview'),
  prompt: 'Generate an image of a comic cat',
});

for (const file of result.files) {
  if (file.mediaType.startsWith('image/')) {
    // Access file.base64, file.uint8Array, file.mediaType
  }
}
```

---

## Transcription

Transcription is an experimental feature.

```ts
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';
import { readFile } from 'fs/promises';

const transcript = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: await readFile('audio.mp3'),
});

const text = transcript.text;
const segments = transcript.segments;
const language = transcript.language;
const durationInSeconds = transcript.durationInSeconds;
```

The `audio` property accepts: `Uint8Array`, `ArrayBuffer`, `Buffer`, `string` (base64), or `URL`.

### Transcription Models

| Provider | Model |
|----------|-------|
| OpenAI | whisper-1, gpt-4o-transcribe, gpt-4o-mini-transcribe |
| ElevenLabs | scribe_v1 |
| Groq | whisper-large-v3-turbo |
| Deepgram | nova-3 (+ variants) |
| AssemblyAI | best, nano |

---

## Speech

Speech generation is an experimental feature.

```ts
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';

const audio = await generateSpeech({
  model: openai.speech('tts-1'),
  text: 'Hello, world!',
  voice: 'alloy',
  language: 'en', // Optional language setting
});

const audioData = audio.audioData; // Uint8Array
```

### Speech Models

| Provider | Model |
|----------|-------|
| OpenAI | tts-1, tts-1-hd, gpt-4o-mini-tts |
| ElevenLabs | eleven_v3, eleven_multilingual_v2, eleven_flash_v2_5 |
| LMNT | aurora, blizzard |
| Hume | default |

---

## Language Model Middleware

Middleware intercepts and modifies language model calls for features like guardrails, RAG, caching, and logging.

### Using Middleware

```ts
import { wrapLanguageModel } from 'ai';

const wrappedLanguageModel = wrapLanguageModel({
  model: yourModel,
  middleware: yourLanguageModelMiddleware,
});

// Multiple middlewares (applied in order)
const wrappedModel = wrapLanguageModel({
  model: yourModel,
  middleware: [firstMiddleware, secondMiddleware],
});
```

### Built-in Middleware

**extractReasoningMiddleware**: Extracts reasoning from special tags:
```ts
const model = wrapLanguageModel({
  model: yourModel,
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});
```

**simulateStreamingMiddleware**: Simulates streaming from non-streaming models:
```ts
const model = wrapLanguageModel({
  model: yourModel,
  middleware: simulateStreamingMiddleware(),
});
```

**defaultSettingsMiddleware**: Applies default settings:
```ts
const model = wrapLanguageModel({
  model: yourModel,
  middleware: defaultSettingsMiddleware({
    settings: { temperature: 0.5, maxOutputTokens: 800 },
  }),
});
```

### Implementing Custom Middleware

Three functions for modifying behavior:
- `transformParams`: Transform parameters before passing to model
- `wrapGenerate`: Wrap `doGenerate` method
- `wrapStream`: Wrap `doStream` method

**Example: Logging middleware:**
```ts
export const yourLogMiddleware: LanguageModelV2Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    console.log('doGenerate called', params);
    const result = await doGenerate();
    console.log('generated text:', result.text);
    return result;
  },
};
```

**Example: RAG middleware:**
```ts
export const yourRagMiddleware: LanguageModelV2Middleware = {
  transformParams: async ({ params }) => {
    const sources = findSources({ text: getLastUserMessageText(params) });
    return addToLastUserMessage({ params, text: sources });
  },
};
```

### Community Middleware

- **Custom tool call parser**: Enables function calling for models without native support (Hermes, Qwen, Gemma formats)

---

## Provider and Model Management

### Custom Providers

Create custom providers with `customProvider`:

```ts
import { customProvider, gateway, wrapLanguageModel, defaultSettingsMiddleware } from 'ai';

// Model aliases
export const anthropic = customProvider({
  languageModels: {
    opus: gateway('anthropic/claude-opus-4.1'),
    sonnet: gateway('anthropic/claude-sonnet-4.5'),
    haiku: gateway('anthropic/claude-haiku-4.5'),
  },
  fallbackProvider: gateway,
});

// Limit available models
export const myProvider = customProvider({
  languageModels: {
    'text-medium': gateway('anthropic/claude-sonnet-4.5'),
    'text-small': gateway('openai/gpt-5-mini'),
  },
  embeddingModels: {
    embedding: gateway.textEmbeddingModel('openai/text-embedding-3-small'),
  },
});
```

### Provider Registry

Manage multiple providers centrally:

```ts
import { createProviderRegistry, gateway } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';
import { openai } from '@ai-sdk/openai';

export const registry = createProviderRegistry({
  gateway,
  anthropic,
  openai,
});

// Custom separator
const customRegistry = createProviderRegistry(
  { gateway, anthropic },
  { separator: ' > ' }
);

// Usage
const model = registry.languageModel('openai:gpt-5.1');
const embeddingModel = registry.textEmbeddingModel('openai:text-embedding-3-small');
const imageModel = registry.imageModel('openai:dall-e-3');
```

### Global Provider Configuration

Set default provider globally:

```ts
// setup.ts
import { openai } from '@ai-sdk/openai';
globalThis.AI_SDK_DEFAULT_PROVIDER = openai;

// app.ts
const result = await streamText({
  model: 'gpt-5.1', // Uses OpenAI without prefix
  prompt: 'Invent a new holiday.',
});
```

---

## Error Handling

### Regular Errors

Use try/catch blocks:

```ts
try {
  const { text } = await generateText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt: 'Write a vegetarian lasagna recipe.',
  });
} catch (error) {
  // handle error
}
```

### Streaming Errors (Simple Streams)

Errors are thrown as regular errors - use try/catch.

### Streaming Errors (Full Streams)

Full streams support error parts:

```ts
for await (const part of fullStream) {
  switch (part.type) {
    case 'error':
      const error = part.error;
      // handle error
      break;
    case 'abort':
      // handle stream abort
      break;
    case 'tool-error':
      const toolError = part.error;
      // handle tool error
      break;
  }
}
```

### Stream Abort Handling

Use `onAbort` callback for cleanup:

```ts
const { textStream } = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a recipe.',
  onAbort: ({ steps }) => {
    console.log('Stream aborted after', steps.length, 'steps');
  },
  onFinish: ({ steps, totalUsage }) => {
    console.log('Stream completed normally');
  },
});
```

---

## Testing

The AI SDK includes mock providers and test helpers from `ai/test`:

- `MockLanguageModelV2`: Mock language model
- `MockEmbeddingModelV2`: Mock embedding model
- `mockId`: Incrementing integer ID
- `mockValues`: Iterates over values array
- `simulateReadableStream`: Simulates readable stream with delays

### Testing generateText

```ts
import { generateText } from 'ai';
import { MockLanguageModelV2 } from 'ai/test';

const result = await generateText({
  model: new MockLanguageModelV2({
    doGenerate: async () => ({
      finishReason: 'stop',
      usage: { inputTokens: 10, outputTokens: 20, totalTokens: 30 },
      content: [{ type: 'text', text: 'Hello, world!' }],
      warnings: [],
    }),
  }),
  prompt: 'Hello, test!',
});
```

### Testing streamText

```ts
import { streamText, simulateReadableStream } from 'ai';
import { MockLanguageModelV2 } from 'ai/test';

const result = streamText({
  model: new MockLanguageModelV2({
    doStream: async () => ({
      stream: simulateReadableStream({
        chunks: [
          { type: 'text-start', id: 'text-1' },
          { type: 'text-delta', id: 'text-1', delta: 'Hello' },
          { type: 'text-delta', id: 'text-1', delta: ', world!' },
          { type: 'text-end', id: 'text-1' },
          { type: 'finish', finishReason: 'stop', usage: { /* ... */ } },
        ],
      }),
    }),
  }),
  prompt: 'Hello, test!',
});
```

### Simulating UI Message Streams

```ts
import { simulateReadableStream } from 'ai';

return new Response(
  simulateReadableStream({
    initialDelayInMs: 1000,
    chunkDelayInMs: 300,
    chunks: [
      `data: {"type":"start","messageId":"msg-123"}\n\n`,
      `data: {"type":"text-start","id":"text-1"}\n\n`,
      `data: {"type":"text-delta","id":"text-1","delta":"This"}\n\n`,
      `data: {"type":"text-end","id":"text-1"}\n\n`,
      `data: {"type":"finish"}\n\n`,
    ],
  }).pipeThrough(new TextEncoderStream()),
  { headers: { 'Content-Type': 'text/event-stream' } }
);
```

---

## Telemetry

AI SDK uses OpenTelemetry for telemetry data collection (experimental).

### Enabling Telemetry

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a short story about a cat.',
  experimental_telemetry: { isEnabled: true },
});
```

### Telemetry Metadata

```ts
experimental_telemetry: {
  isEnabled: true,
  functionId: 'my-awesome-function',
  metadata: {
    something: 'custom',
    someOtherThing: 'other-value',
  },
}
```

### Custom Tracer

```ts
const tracerProvider = new NodeTracerProvider();
experimental_telemetry: {
  isEnabled: true,
  tracer: tracerProvider.getTracer('ai'),
}
```

### Collected Data

**generateText spans:**
- `ai.generateText`: Full call span
- `ai.generateText.doGenerate`: Provider call span
- `ai.toolCall`: Tool call span

**streamText spans:**
- `ai.streamText`: Full call span
- `ai.streamText.doStream`: Provider stream span
- `ai.stream.firstChunk`: First chunk event
- `ai.stream.finish`: Stream finish event
- `ai.toolCall`: Tool call span

**generateObject/streamObject spans:**
Similar structure with schema information and object generation details.

**embed/embedMany spans:**
- `ai.embed` / `ai.embedMany`: Full call spans
- `ai.embed.doEmbed` / `ai.embedMany.doEmbed`: Provider call spans

### Span Attributes

**Basic LLM span attributes:**
- `ai.model.id`, `ai.model.provider`
- `ai.usage.completionTokens`, `ai.usage.promptTokens`
- `ai.settings.maxRetries`
- `ai.telemetry.functionId`, `ai.telemetry.metadata.*`

**Tool call span attributes:**
- `ai.toolCall.name`, `ai.toolCall.id`
- `ai.toolCall.args`, `ai.toolCall.result`

---

## Summary

The AI SDK Core provides a comprehensive, standardized interface for working with LLMs across multiple providers. Key features include:

- Unified API for text generation (`generateText`, `streamText`)
- Structured data generation (`generateObject`, `streamObject`)
- Tool calling with multi-step support and error handling
- MCP integration for cross-service tool discovery
- Embeddings for semantic search and RAG
- Image generation, transcription, and speech synthesis
- Middleware for extending model behavior
- Provider management for multi-model applications
- Testing utilities for deterministic unit tests
- OpenTelemetry-based observability

All functions share common patterns for settings, error handling, and provider configuration, making it easy to switch between different models and providers while maintaining consistent application code.
