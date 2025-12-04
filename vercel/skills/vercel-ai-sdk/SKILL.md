---
name: vercel-ai-sdk
description: >-
  This skill should be used when building AI-powered applications with the Vercel AI SDK,
  including text generation, structured data generation, tool calling, chatbots, agents,
  streaming UIs, and integrating LLMs into React, Next.js, Vue, Svelte, or Node.js applications.
  Use this skill when working with generateText, streamText, generateObject, streamObject,
  useChat, useCompletion, useObject hooks, or when implementing MCP clients, embeddings,
  transcription, speech synthesis, or language model middleware.
---

# Vercel AI SDK

The AI SDK is the TypeScript toolkit for building AI-powered applications and agents with React, Next.js, Vue, Svelte, Node.js, and more. It standardizes LLM integrations across providers, allowing focus on building applications rather than managing provider-specific implementations.

## When to Use This Skill

This skill provides guidance for:

- Building chatbots and conversational interfaces
- Generating text with `generateText` and `streamText`
- Creating structured data with `generateObject` and `streamObject`
- Implementing tool calling and multi-step agent workflows
- Building generative user interfaces
- Working with the Agent class for autonomous task execution
- Integrating MCP (Model Context Protocol) servers and tools
- Creating embeddings for semantic search and RAG
- Implementing speech-to-text and text-to-speech
- Using language model middleware for caching, logging, and guardrails
- Deploying AI applications to Vercel

---

## Documentation Structure & Navigation

This skill contains comprehensive reference documentation organized into six main folders. **Always start with the `summary.md` file** in each folder for an overview before diving into specific topics.

### How to Navigate

1. **Start with the relevant `summary.md`** - Each folder contains a summary.md that provides an overview of all topics in that folder
2. **Drill into specific files** - Based on the summary, navigate to the specific file that covers your topic
3. **Use the Topic Quick Reference** below to jump directly to the right file for common questions
4. **Largest files contain the most comprehensive coverage** - Files like `Chatbot.md` (35KB), `Tool Calling.md` (29KB), and `Image Generation.md` (24KB) are the primary references for their topics

---

### Getting Started (`references/Getting Started/`)

**Start here:** `summary.md` - Overview of library navigation and all framework quickstarts

**When to use:** New to the AI SDK, setting up a project, or working with a specific framework

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `Navigating the Library.md` | 7KB | Understanding AI SDK Core, UI, and RSC components and when to use each |
| `Next.js App Router Quickstart.md` | 23KB | Complete setup guide for Next.js App Router with useChat and tools |
| `Next.js Pages Router Quickstart.md` | 23KB | Setup guide for Next.js Pages Router projects |
| `Svelte Quickstart.md` | 25KB | SvelteKit setup with Chat class (note: different API from React) |
| `Vue.js (Nuxt) Quickstart.md` | 23KB | Nuxt/Vue.js setup with Chat class |
| `Node.js Quickstart.md` | 19KB | CLI application setup without UI framework |
| `Expo Quickstart.md` | 28KB | React Native/Expo setup with polyfills and custom transport |

**Key topics covered:**
- Environment setup and prerequisites
- Provider configuration (Vercel AI Gateway, direct providers)
- Basic streaming chat implementation
- Tool calling basics
- Framework-specific patterns and gotchas

---

### Foundation (`references/foundation/`)

**Start here:** `summary.md` - Core AI concepts, providers, prompts, tools, and streaming

**When to use:** Understanding core concepts, working with providers, defining prompts or tools

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `Overview.md` | 3KB | High-level introduction to generative AI and LLMs |
| `Providers and Models.md` | 17KB | All supported providers, model capabilities, and configuration |
| `Prompts.md` | 17KB | Text, system, and message prompts; multi-modal inputs (images, files) |
| `Tools.md` | 9KB | Tool definition, schemas, tool packages, and MCP tools |
| `Streaming.md` | 3KB | Why streaming matters and basic streaming patterns |

**Key topics covered:**
- LLM fundamentals and limitations (hallucinations)
- Provider packages (@ai-sdk/openai, @ai-sdk/anthropic, etc.)
- Text, system, and message prompt types
- Multi-modal inputs (images, PDFs, audio)
- Tool structure (description, inputSchema, execute)
- Ready-to-use tool packages

---

### AI SDK Core (`references/AI SDK Core/`)

**Start here:** `summary.md` - Comprehensive coverage of all core functions and APIs

**When to use:** Server-side text generation, structured data, tool calling, embeddings, or any core SDK functionality

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `AI SDK Core.md` | 2KB | Quick overview of core functions |
| `Generating and Streaming Text.md` | 18KB | `generateText` and `streamText` with all options and callbacks |
| `Generating Structured Data.md` | 13KB | `generateObject` and `streamObject` with Zod schemas |
| `Tool Calling.md` | **29KB** | **Primary reference** - Complete tool calling guide with multi-step, dynamic tools, errors |
| `Model Context Protocol (MCP).md` | 10KB | MCP client setup, transports (HTTP, SSE, stdio), resources, prompts |
| `Prompt Engineering.md` | 5KB | Tips for effective prompts, schema best practices, debugging |
| `Settings.md` | 4KB | Common settings (temperature, maxOutputTokens, etc.) |
| `Embeddings.md` | 8KB | `embed` and `embedMany` functions, similarity calculations |
| `Image Generation.md` | **24KB** | `generateImage` (experimental), multi-modal outputs |
| `Transcription.md` | 7KB | `transcribe` function for speech-to-text |
| `Speech.md` | 5KB | `generateSpeech` for text-to-speech |
| `Language Model Middleware.md` | 13KB | Middleware for caching, logging, RAG, guardrails |
| `Provider & Model Management.md` | 10KB | Custom providers, provider registry, global configuration |
| `Error Handling.md` | 4KB | Error types and handling patterns |
| `Testing.md` | 5KB | Mock providers and test helpers |
| `Telemetry.md` | 17KB | OpenTelemetry integration for observability |

**Key topics covered:**
- All core generation functions and their options
- Streaming with callbacks (onChunk, onFinish, onError)
- Multi-step tool execution with `stopWhen`
- MCP integration for external tools
- Middleware for extending model behavior
- Testing and observability

---

### AI SDK UI (`references/AI SDK UI/`)

**Start here:** `summary.md` - Complete guide to UI hooks and frontend integration

**When to use:** Building chat interfaces, using useChat/useCompletion/useObject hooks, handling streaming in the browser

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `Overview.md` | 3KB | Introduction to AI SDK UI and framework support matrix |
| `Chatbot.md` | **36KB** | **Primary reference** - Complete useChat guide with all options, states, callbacks |
| `Chatbot Message Persistence.md` | 16KB | Storing and loading chat messages, server-side ID generation |
| `Chatbot Resume Streams.md` | 9KB | Resuming streams after page reload for long-running generations |
| `Chatbot Tool Usage.md` | 19KB | Client-side tools, tool rendering, multi-step in UI |
| `Completion.md` | 6KB | useCompletion hook for single-turn text completion |
| `Object Generation.md` | 9KB | useObject hook for streaming structured JSON |
| `Generative User Interfaces.md` | 12KB | Connecting tools to React components for dynamic UI |
| `Streaming Custom Data.md` | 11KB | Data parts, transient data, server-to-client streaming |
| `Error Handling and warnings.md` | 5KB | Client-side error handling and warning suppression |
| `Transport.md` | 3KB | Custom transport configuration for fetch options |
| `Message Metadata.md` | 5KB | Attaching custom metadata to messages |
| `Reading UI Message Streams.md` | 3KB | Consuming streams outside useChat |
| `Stream Protocols.md` | 11KB | Text stream vs UI message stream protocol details |

**Key topics covered:**
- useChat hook with all configuration options
- Status states (submitted, streaming, ready, error)
- Message persistence and database integration
- Stream resumption for long-running tasks
- Tool rendering with part states (input-streaming, output-available, etc.)
- Custom data streaming and metadata
- Transport customization

---

### Agents (`references/Agents/`)

**Start here:** `summary.md` - Complete guide to building agents with the AI SDK

**When to use:** Building autonomous agents, implementing agentic workflows, using the Agent class

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `Agents.md` | 3KB | Introduction to agents (LLMs + tools + loop) |
| `Building Agents.md` | 9KB | Agent class configuration, tools, system prompts, usage patterns |
| `Loop Control.md` | 8KB | Stop conditions (stepCountIs, hasToolCall), prepareStep for dynamic behavior |
| `Workflow Patterns.md` | **13KB** | Sequential chains, routing, parallel processing, orchestrator-worker, evaluator-optimizer |

**Key topics covered:**
- Agent class (Experimental_Agent)
- Tool definition and tool choice options
- Stop conditions (built-in and custom)
- prepareStep callback for dynamic model/tool selection
- Workflow patterns: chains, routing, parallel, orchestrator-worker
- Manual loop control for complete flexibility
- Type safety with InferAgentUIMessage

---

### Advanced (`references/Advanced/`)

**Start here:** `summary.md` - Production patterns, optimization, and deployment

**When to use:** Optimizing performance, deploying to production, implementing advanced patterns

**Files in this folder:**
| File | Size | Description |
|------|------|-------------|
| `Prompt Engineering.md` | 6KB | LLM understanding, prompt crafting, temperature settings |
| `Stopping Streams.md` | 6KB | Server-side (abortSignal) and client-side (stop) stream cancellation |
| `Stream Back-pressure and Cancellation.md` | 9KB | Lazy streaming with pull handler for memory efficiency |
| `Caching Responses.md` | 6KB | Middleware-based caching with Redis, lifecycle callbacks |
| `Multiple Streams.md` | 2KB | Multiple and nested streamable UIs (RSC) |
| `Rate Limiting.md` | 2KB | Protecting APIs with Upstash Ratelimit |
| `Rendering User Interfaces with Language Models.md` | 8KB | Tool results to React components (client and server-side) |
| `Generative User Interfaces.md` | 6KB | LLMs as routers, probabilistic routing by parameters/sequence |
| `Multistep Interfaces.md` | 7KB | Tool composition, application context, complex workflows |
| `Sequential Generations.md` | 2KB | Chaining generations where output becomes next input |
| `Vercel Deployment Guide.md` | 6KB | Deployment steps, function duration, security measures |

**Key topics covered:**
- Production prompt engineering
- Stream cancellation and cleanup
- Back-pressure handling for resource efficiency
- Response caching strategies
- Rate limiting implementation
- Generative UI patterns
- Deployment best practices

---

## Topic Quick Reference

Map common questions directly to the right documentation:

### Chat & Messaging
| Question | File |
|----------|------|
| How do I build a chat interface? | `AI SDK UI/Chatbot.md` |
| How do I persist chat messages? | `AI SDK UI/Chatbot Message Persistence.md` |
| How do I resume a stream after page reload? | `AI SDK UI/Chatbot Resume Streams.md` |
| How do I use tools in my chat UI? | `AI SDK UI/Chatbot Tool Usage.md` |
| How do I handle errors in the chat UI? | `AI SDK UI/Error Handling and warnings.md` |
| How do I add metadata to messages? | `AI SDK UI/Message Metadata.md` |

### Text & Object Generation
| Question | File |
|----------|------|
| How do I generate text? | `AI SDK Core/Generating and Streaming Text.md` |
| How do I stream text? | `AI SDK Core/Generating and Streaming Text.md` |
| How do I generate structured JSON? | `AI SDK Core/Generating Structured Data.md` |
| How do I use useObject for streaming objects? | `AI SDK UI/Object Generation.md` |
| What settings can I configure? | `AI SDK Core/Settings.md` |

### Tools & Agents
| Question | File |
|----------|------|
| How do I define tools? | `foundation/Tools.md` or `AI SDK Core/Tool Calling.md` |
| How do I implement multi-step tool calling? | `AI SDK Core/Tool Calling.md` |
| How do I build an agent? | `Agents/Building Agents.md` |
| How do I control the agent loop? | `Agents/Loop Control.md` |
| What workflow patterns should I use? | `Agents/Workflow Patterns.md` |
| How do I use MCP tools? | `AI SDK Core/Model Context Protocol (MCP).md` |

### Framework Setup
| Question | File |
|----------|------|
| How do I set up Next.js App Router? | `Getting Started/Next.js App Router Quickstart.md` |
| How do I set up SvelteKit? | `Getting Started/Svelte Quickstart.md` |
| How do I set up Vue/Nuxt? | `Getting Started/Vue.js (Nuxt) Quickstart.md` |
| How do I set up Expo/React Native? | `Getting Started/Expo Quickstart.md` |
| How do I build a CLI app? | `Getting Started/Node.js Quickstart.md` |
| Which SDK component should I use? | `Getting Started/Navigating the Library.md` |

### Advanced Topics
| Question | File |
|----------|------|
| How do I cache LLM responses? | `Advanced/Caching Responses.md` |
| How do I add rate limiting? | `Advanced/Rate Limiting.md` |
| How do I cancel/stop a stream? | `Advanced/Stopping Streams.md` |
| How do I handle back-pressure? | `Advanced/Stream Back-pressure and Cancellation.md` |
| How do I deploy to Vercel? | `Advanced/Vercel Deployment Guide.md` |
| How do I write effective prompts? | `Advanced/Prompt Engineering.md` |

### Multimedia & Embeddings
| Question | File |
|----------|------|
| How do I generate embeddings? | `AI SDK Core/Embeddings.md` |
| How do I generate images? | `AI SDK Core/Image Generation.md` |
| How do I transcribe audio? | `AI SDK Core/Transcription.md` |
| How do I generate speech? | `AI SDK Core/Speech.md` |

### Testing & Observability
| Question | File |
|----------|------|
| How do I test AI SDK code? | `AI SDK Core/Testing.md` |
| How do I add telemetry/tracing? | `AI SDK Core/Telemetry.md` |
| How do I handle errors? | `AI SDK Core/Error Handling.md` |

### Providers & Configuration
| Question | File |
|----------|------|
| What providers are available? | `foundation/Providers and Models.md` |
| How do I configure providers? | `AI SDK Core/Provider & Model Management.md` |
| How do I use middleware? | `AI SDK Core/Language Model Middleware.md` |

---

## Library Architecture

The AI SDK consists of three main components:

| Component | Purpose | Environment |
|-----------|---------|-------------|
| **AI SDK Core** | Unified API for text/object generation, tool calls, and agents | Node.js, Deno, Browser |
| **AI SDK UI** | Framework-agnostic hooks for chat and generative UIs | React, Vue, Svelte, Angular |
| **AI SDK RSC** | Stream generative UIs with React Server Components (experimental) | Next.js App Router only |

## Core Functions

### Text Generation

Generate text using `generateText` for blocking responses or `streamText` for streaming:

```ts
import { generateText, streamText } from 'ai';

// Blocking generation
const { text } = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a poem about AI.',
});

// Streaming generation
const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  system: 'You are a helpful assistant.',
  prompt: 'Explain quantum computing.',
});

for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

### Structured Data Generation

Generate typed objects validated against Zod schemas:

```ts
import { generateObject, streamObject } from 'ai';
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

### Tool Calling

Define tools with descriptions, input schemas, and execute functions:

```ts
import { generateText, tool } from 'ai';
import { z } from 'zod';

const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: {
    weather: tool({
      description: 'Get the weather in a location',
      inputSchema: z.object({
        location: z.string().describe('The location to get weather for'),
      }),
      execute: async ({ location }) => ({
        location,
        temperature: 72,
        conditions: 'sunny',
      }),
    }),
  },
  prompt: 'What is the weather in San Francisco?',
});
```

### Multi-Step Tool Execution

Enable automatic tool result processing with `stopWhen`:

```ts
import { streamText, stepCountIs } from 'ai';

const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  tools: { /* tools with execute functions */ },
  stopWhen: stepCountIs(5),
  prompt: 'Research and summarize the latest AI news.',
});
```

## UI Hooks

### useChat Hook (React)

Build chat interfaces with automatic state management:

```tsx
'use client';
import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, sendMessage, status, error } = useChat();

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          {message.parts.map((part, i) => {
            if (part.type === 'text') return <p key={i}>{part.text}</p>;
          })}
        </div>
      ))}
    </div>
  );
}
```

### Server API Route

```ts
import { streamText, UIMessage, convertToModelMessages } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

## Agent Class

The Agent class provides a structured approach to building autonomous agents:

```ts
import { Experimental_Agent as Agent, stepCountIs, tool } from 'ai';
import { z } from 'zod';

const myAgent = new Agent({
  model: 'anthropic/claude-sonnet-4.5',
  system: 'You are a helpful research assistant.',
  tools: {
    search: tool({
      description: 'Search the web',
      inputSchema: z.object({ query: z.string() }),
      execute: async ({ query }) => ({ results: ['...'] }),
    }),
  },
  stopWhen: stepCountIs(10),
});

// Generate response
const result = await myAgent.generate({
  prompt: 'Research the latest developments in quantum computing.',
});

// Or stream response
const stream = myAgent.stream({ prompt: 'Tell me about AI agents.' });
```

## Provider Configuration

The SDK supports multiple providers through a unified interface:

```ts
// Default: Vercel AI Gateway
model: 'anthropic/claude-sonnet-4.5'

// Explicit gateway
import { gateway } from 'ai';
model: gateway('openai/gpt-5.1')

// Direct provider packages
import { anthropic } from '@ai-sdk/anthropic';
model: anthropic('claude-sonnet-4-20250514')
```

## Key Concepts

### Message Types

- **UIMessage**: Messages for UI with metadata (timestamps, sender info)
- **ModelMessage**: Messages for model consumption without UI metadata
- **convertToModelMessages()**: Convert UIMessage to ModelMessage format

### Message Parts

Messages contain a `parts` array with different content types:

- `text`: Plain text content
- `reasoning`: Model reasoning (when available)
- `tool-{toolName}`: Tool calls and results
- `data-{dataType}`: Custom data parts
- `file`: Generated files

### Tool Part States

Tool parts transition through states:

- `input-streaming`: Tool input being generated
- `input-available`: Complete input ready
- `output-available`: Tool execution complete
- `output-error`: Tool execution failed

## Advanced Features

### Language Model Middleware

Intercept and modify model calls for caching, logging, RAG, or guardrails:

```ts
import { wrapLanguageModel, type LanguageModelV2Middleware } from 'ai';

const cachingMiddleware: LanguageModelV2Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    const cached = await cache.get(params);
    if (cached) return cached;
    const result = await doGenerate();
    await cache.set(params, result);
    return result;
  },
};

const wrappedModel = wrapLanguageModel({
  model: yourModel,
  middleware: cachingMiddleware,
});
```

### MCP Integration

Connect to MCP servers for tool discovery:

```ts
import { experimental_createMCPClient as createMCPClient } from '@ai-sdk/mcp';

const mcpClient = await createMCPClient({
  transport: { type: 'sse', url: 'https://your-mcp-server.com/sse' },
});

const tools = await mcpClient.tools();
```

### Embeddings

Generate vector embeddings for semantic search:

```ts
import { embed, embedMany, cosineSimilarity } from 'ai';

const { embedding } = await embed({
  model: 'openai/text-embedding-3-small',
  value: 'sunny day at the beach',
});

const { embeddings } = await embedMany({
  model: 'openai/text-embedding-3-small',
  values: ['text1', 'text2', 'text3'],
});
```
