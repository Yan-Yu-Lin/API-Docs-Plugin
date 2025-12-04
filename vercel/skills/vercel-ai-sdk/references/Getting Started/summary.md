# Vercel AI SDK - Getting Started Summary

This document provides a comprehensive summary of the Vercel AI SDK getting started documentation, covering library navigation and framework-specific quickstart guides.

---

## Navigating the Library

The AI SDK is a powerful toolkit for building AI applications, comprised of three main parts:

### Core Components

| Component | Purpose | Environment Compatibility |
|-----------|---------|--------------------------|
| **AI SDK Core** | Unified, provider-agnostic API for generating text, structured objects, and tool calls with LLMs | Any JS environment (Node.js, Deno, Browser) |
| **AI SDK UI** | Framework-agnostic hooks for building chat and generative user interfaces | React & Next.js, Vue & Nuxt, Svelte & SvelteKit |
| **AI SDK RSC** | Stream generative UIs with React Server Components (experimental) | Next.js App Router only |

### Environment Compatibility Matrix

| Environment | AI SDK Core | AI SDK UI | AI SDK RSC |
|-------------|-------------|-----------|------------|
| Node.js / Deno | Yes | No | No |
| Vue / Nuxt | Yes | Yes | No |
| Svelte / SvelteKit | Yes | Yes | No |
| Next.js Pages Router | Yes | Yes | No |
| Next.js App Router | Yes | Yes | Yes |

### AI SDK UI Framework Support

| Function | React | Svelte | Vue.js |
|----------|-------|--------|--------|
| `useChat` | Yes | Yes | Yes |
| `useChat` tool calling | Yes | Yes | No |
| `useCompletion` | Yes | Yes | Yes |
| `useObject` | Yes | No | No |

### When to Use Each Component

**AI SDK UI** - Recommended for:
- Production-ready AI-native applications
- Full support for streaming chat and client-side generative UI
- Utilities for common AI interaction patterns (chat, completion, assistant)

**AI SDK RSC** - Currently experimental with limitations:
- Cannot abort streams using Server Actions
- `createStreamableUI` can lead to quadratic data transfer
- Components re-mount on `.done()`, causing flickering
- **Recommendation**: Use AI SDK UI for production applications

---

## Common Concepts Across All Frameworks

### Prerequisites

All quickstart guides require:
- Node.js 18+ and pnpm installed
- A Vercel AI Gateway API key

### Key Dependencies

```bash
# Core packages
ai                    # AI SDK core package
zod                   # Schema validation for tool inputs

# Framework-specific UI packages
@ai-sdk/react         # For React/Next.js/Expo
@ai-sdk/svelte        # For Svelte/SvelteKit
@ai-sdk/vue           # For Vue.js/Nuxt
```

### Provider Configuration

The AI SDK supports multiple model providers through:
- First-party packages
- OpenAI-compatible packages
- Community packages

**Default Provider (Vercel AI Gateway)**:
```typescript
// Simple string format (uses global provider)
model: 'anthropic/claude-sonnet-4.5'

// Explicit import options
import { gateway } from 'ai';
model: gateway('openai/gpt-5.1');

// Or from dedicated package
import { gateway } from '@ai-sdk/gateway';
model: gateway('openai/gpt-5.1');
```

**Using Other Providers**:
```typescript
import { openai } from '@ai-sdk/openai';
model: openai('gpt-5.1');
```

### Core API Pattern: streamText

The `streamText` function is central to all implementations:

```typescript
import { streamText, UIMessage, convertToModelMessages } from 'ai';

const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  messages: convertToModelMessages(messages),
});

return result.toUIMessageStreamResponse();
```

**Key Concepts**:
- `UIMessage[]` - Messages designed for UI with metadata (timestamps, sender info)
- `ModelMessage[]` - Messages for model consumption without UI metadata
- `convertToModelMessages()` - Converts UIMessage to ModelMessage format
- `toUIMessageStreamResponse()` - Converts result to streamed response

### Message Parts Structure

Messages contain a `parts` array representing model outputs:

```typescript
message.parts.map((part, i) => {
  switch (part.type) {
    case 'text':
      return part.text;
    case 'tool-weather':
      return JSON.stringify(part);
  }
});
```

Parts can include:
- Plain text
- Reasoning tokens
- Tool calls and results

---

## Tools and Tool Calling

Tools enable LLMs to perform discrete tasks and interact with external systems.

### Defining a Tool

```typescript
import { tool } from 'ai';
import { z } from 'zod';

tools: {
  weather: tool({
    description: 'Get the weather in a location (fahrenheit)',
    inputSchema: z.object({
      location: z.string().describe('The location to get the weather for'),
    }),
    execute: async ({ location }) => {
      const temperature = Math.round(Math.random() * (90 - 32) + 32);
      return { location, temperature };
    },
  }),
}
```

**Tool Components**:
- `description` - Helps the model understand when to use the tool
- `inputSchema` - Zod schema defining required inputs
- `execute` - Async function that performs the action

**Tool Part Naming**: Tool parts are named `tool-{toolName}` (e.g., `tool-weather`)

### Multi-Step Tool Calls

By default, generation stops after a tool call. Enable multi-step execution with `stopWhen`:

```typescript
import { stepCountIs } from 'ai';

const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  messages: convertToModelMessages(messages),
  stopWhen: stepCountIs(5), // Allow up to 5 steps
  tools: { /* ... */ },
});
```

**Multi-step workflow example** (asking for weather in Celsius):
1. Model calls weather tool for location
2. Tool returns temperature in Fahrenheit
3. Model calls conversion tool
4. Conversion tool returns Celsius
5. Model provides natural language response

### Monitoring Tool Execution

```typescript
onStepFinish: async ({ toolResults }) => {
  if (toolResults.length) {
    console.log(JSON.stringify(toolResults, null, 2));
  }
},
```

---

## Framework-Specific Implementations

### Next.js App Router

**File: `app/api/chat/route.ts`**
```typescript
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

**File: `app/page.tsx`**
```typescript
'use client';
import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, sendMessage } = useChat();
  // ... render messages and input
}
```

### Next.js Pages Router

Uses Route Handlers (App Router) alongside Pages Router for streaming support.

**File: `app/api/chat/route.ts`** - Same as App Router

**File: `pages/index.tsx`**
```typescript
import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

export default function Chat() {
  const [input, setInput] = useState('');
  const { messages, sendMessage } = useChat();
  // ... render with local state management
}
```

### Svelte / SvelteKit

**Key Differences from React**:
- Uses `Chat` class instead of `useChat` hook
- Arguments to classes are not reactive by default (pass references, not values)
- Cannot destructure class properties
- Instance synchronization requires `createAIContext`

**File: `src/routes/api/chat/+server.ts`**
```typescript
import { streamText, type UIMessage, convertToModelMessages, createGateway } from 'ai';
import { AI_GATEWAY_API_KEY } from '$env/static/private';

const gateway = createGateway({ apiKey: AI_GATEWAY_API_KEY });

export async function POST({ request }) {
  const { messages }: { messages: UIMessage[] } = await request.json();
  const result = streamText({
    model: gateway('openai/gpt-5.1'),
    messages: convertToModelMessages(messages),
  });
  return result.toUIMessageStreamResponse();
}
```

**File: `src/routes/+page.svelte`**
```svelte
<script lang="ts">
  import { Chat } from '@ai-sdk/svelte';

  let input = '';
  const chat = new Chat({});

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    chat.sendMessage({ text: input });
    input = '';
  }
</script>
```

**Passing Reactive Arguments in Svelte**:
```svelte
// Won't update when id changes
let chat = new Chat({ id });

// Will update - passes by reference
let chat = new Chat({
  get id() { return id; }
});
```

**Instance Synchronization**:
```svelte
import { createAIContext } from '@ai-sdk/svelte';
createAIContext(); // All child components share state
```

### Vue.js / Nuxt

**File: `server/api/chat.ts`**
```typescript
import { streamText, UIMessage, convertToModelMessages, createGateway } from 'ai';

export default defineLazyEventHandler(async () => {
  const apiKey = useRuntimeConfig().aiGatewayApiKey;
  const gateway = createGateway({ apiKey });

  return defineEventHandler(async (event) => {
    const { messages }: { messages: UIMessage[] } = await readBody(event);
    const result = streamText({
      model: gateway('openai/gpt-5.1'),
      messages: convertToModelMessages(messages),
    });
    return result.toUIMessageStreamResponse();
  });
});
```

**File: `pages/index.vue`**
```vue
<script setup lang="ts">
import { Chat } from "@ai-sdk/vue";
import { ref } from "vue";

const input = ref("");
const chat = new Chat({});

const handleSubmit = (e: Event) => {
  e.preventDefault();
  chat.sendMessage({ text: input.value });
  input.value = "";
};
</script>
```

**Nuxt Config for API Key**:
```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  runtimeConfig: {
    aiGatewayApiKey: '', // Set via NUXT_AI_GATEWAY_API_KEY env var
  },
});
```

### Node.js (CLI Application)

**File: `index.ts`**
```typescript
import { ModelMessage, streamText } from 'ai';
import 'dotenv/config';
import * as readline from 'node:readline/promises';

const terminal = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const messages: ModelMessage[] = [];

async function main() {
  while (true) {
    const userInput = await terminal.question('You: ');
    messages.push({ role: 'user', content: userInput });

    const result = streamText({
      model: 'anthropic/claude-sonnet-4.5',
      messages,
    });

    let fullResponse = '';
    process.stdout.write('\nAssistant: ');
    for await (const delta of result.textStream) {
      fullResponse += delta;
      process.stdout.write(delta);
    }
    process.stdout.write('\n\n');

    messages.push({ role: 'assistant', content: fullResponse });
  }
}

main().catch(console.error);
```

**Run**: `pnpm tsx index.ts`

### Expo (React Native)

**Special Considerations**:
- Requires Expo 52 or higher
- Uses `expo/fetch` instead of native fetch for streaming
- Requires custom transport configuration
- May need polyfills for mobile platforms

**File: `app/api/chat+api.ts`**
```typescript
import { streamText, UIMessage, convertToModelMessages } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();
  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    messages: convertToModelMessages(messages),
  });
  return result.toUIMessageStreamResponse({
    headers: {
      'Content-Type': 'application/octet-stream',
      'Content-Encoding': 'none',
    },
  });
}
```

**File: `app/(tabs)/index.tsx`**
```typescript
import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';
import { fetch as expoFetch } from 'expo/fetch';

const { messages, error, sendMessage } = useChat({
  transport: new DefaultChatTransport({
    fetch: expoFetch as unknown as typeof globalThis.fetch,
    api: generateAPIUrl('/api/chat'),
  }),
  onError: error => console.error(error),
});
```

**API URL Generator** (`utils.ts`):
```typescript
import Constants from 'expo-constants';

export const generateAPIUrl = (relativePath: string) => {
  const origin = Constants.experienceUrl.replace('exp://', 'http://');
  const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`;

  if (process.env.NODE_ENV === 'development') {
    return origin.concat(path);
  }

  if (!process.env.EXPO_PUBLIC_API_BASE_URL) {
    throw new Error('EXPO_PUBLIC_API_BASE_URL environment variable is not defined');
  }

  return process.env.EXPO_PUBLIC_API_BASE_URL.concat(path);
};
```

**Required Polyfills for Mobile**:
```typescript
// polyfills.js
import { Platform } from 'react-native';
import structuredClone from '@ungap/structured-clone';

if (Platform.OS !== 'web') {
  const setupPolyfills = async () => {
    const { polyfillGlobal } = await import(
      'react-native/Libraries/Utilities/PolyfillFunctions'
    );
    const { TextEncoderStream, TextDecoderStream } = await import(
      '@stardazed/streams-text-encoding'
    );

    if (!('structuredClone' in global)) {
      polyfillGlobal('structuredClone', () => structuredClone);
    }
    polyfillGlobal('TextEncoderStream', () => TextEncoderStream);
    polyfillGlobal('TextDecoderStream', () => TextDecoderStream);
  };
  setupPolyfills();
}
```

**Polyfill Packages**:
```bash
pnpm add @ungap/structured-clone @stardazed/streams-text-encoding
```

---

## Environment Variables Summary

| Framework | Variable Name | Location |
|-----------|---------------|----------|
| Next.js | `AI_GATEWAY_API_KEY` | `.env.local` |
| Svelte/SvelteKit | `AI_GATEWAY_API_KEY` | `.env.local` (import from `$env/static/private`) |
| Nuxt | `NUXT_AI_GATEWAY_API_KEY` | `.env` |
| Node.js | `AI_GATEWAY_API_KEY` | `.env` |
| Expo | `AI_GATEWAY_API_KEY` | `.env.local` |
| Expo (Production) | `EXPO_PUBLIC_API_BASE_URL` | Production environment |

---

## Next Steps

After completing the quickstart guides, explore:
- Full AI SDK documentation
- RAG (Retrieval-Augmented Generation) guide
- Multi-modal chatbot guide
- Vercel AI templates
