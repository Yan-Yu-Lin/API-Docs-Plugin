# Vercel AI SDK - Advanced Topics Summary

This document provides a comprehensive summary of advanced concepts and patterns for working with the Vercel AI SDK.

---

## Table of Contents

1. [Prompt Engineering](#prompt-engineering)
2. [Stopping Streams](#stopping-streams)
3. [Stream Back-pressure and Cancellation](#stream-back-pressure-and-cancellation)
4. [Caching Responses](#caching-responses)
5. [Multiple Streams](#multiple-streams)
6. [Rate Limiting](#rate-limiting)
7. [Rendering User Interfaces with Language Models](#rendering-user-interfaces-with-language-models)
8. [Generative User Interfaces](#generative-user-interfaces)
9. [Multistep Interfaces](#multistep-interfaces)
10. [Sequential Generations](#sequential-generations)
11. [Vercel Deployment Guide](#vercel-deployment-guide)

---

## Prompt Engineering

### Understanding Large Language Models (LLMs)

A Large Language Model is a prediction engine that takes a sequence of words as input and predicts the most likely sequence to follow by assigning probabilities to potential next sequences. Models learn by training on massive text corpora, making them better suited for certain use cases depending on their training data.

### What is a Prompt?

Prompts are the starting points for LLMs - the inputs that trigger text generation. Prompt engineering encompasses:
- Crafting effective prompts
- Understanding hidden prompts and tokens
- Managing token limits
- Preventing prompt hacking (jailbreaks and leaks)

### Key Prompt Engineering Techniques

1. **Clear Instructions**: Start with specific instructions. Adding descriptive terms influences the completion.
   ```
   "Create a slogan for an organic coffee shop."
   ```

2. **Include Examples**: Show the model your requirements by providing examples of expected outputs (few-shot prompting).
   ```
   Business: Bookstore with cats
   Slogans: "Purr-fect Pages", "Books and Whiskers", "Novels and Nuzzles"
   ```

3. **Temperature Settings**:
   - Temperature 0: Deterministic, same output each time
   - Temperature 1: More varied, creative outputs
   - Moderate temperature (0.6): Good for generating diverse suggestions while maintaining relevance

### Trade-offs

Different models have varying performance, context windows, and costs. GPT-4 is more expensive and slower than GPT-3.5-turbo but can be more effective at certain tasks.

---

## Stopping Streams

### AI SDK Core - Server-Side Cancellation

Use the `abortSignal` argument to cancel streams from the server side:

```tsx
import { streamText } from 'ai';

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt,
    abortSignal: req.signal,
    onAbort: ({ steps }) => {
      console.log('Stream aborted after', steps.length, 'steps');
      // Persist partial results to database
    },
  });

  return result.toTextStreamResponse();
}
```

### AI SDK UI - Client-Side Cancellation

Use the `stop` helper function from hooks like `useChat` or `useCompletion`:

```tsx
const { input, completion, stop, status, handleSubmit, handleInputChange } =
  useCompletion();

// Call stop() to cancel the stream
<button type="button" onClick={() => stop()}>Stop</button>
```

**Important**: Stream abort functionality is not compatible with stream resumption (`resume: true`).

### Handling Stream Abort Cleanup

The `onAbort` callback is called when a stream is aborted via `AbortSignal`:

```tsx
const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a long story...',
  abortSignal: controller.signal,
  onAbort: ({ steps }) => {
    await savePartialResults(steps);
    await logAbortEvent(steps.length);
  },
  onFinish: ({ steps, totalUsage }) => {
    await saveFinalResults(steps, totalUsage);
  },
});
```

### UI Message Streams

For `toUIMessageStreamResponse`, use `consumeStream` for proper abort handling:

```tsx
return result.toUIMessageStreamResponse({
  onFinish: async ({ isAborted }) => {
    if (isAborted) {
      console.log('Stream was aborted');
    }
  },
  consumeSseStream: consumeStream,
});
```

**Note**: AI SDK RSC does not currently support stopping streams.

---

## Stream Back-pressure and Cancellation

### The Problem with Eager Streams

When wrapping generators into streams using an eager `for await (...)` approach in the `start` handler, streams don't respect back-pressure. This leads to:
- Ever-expanding queues of items pushed but not pulled
- Memory issues as the buffer grows indefinitely
- No way to signal the producer to stop

### Solution: Lazy Streaming with `pull`

Use the `pull` handler for lazy, on-demand data production:

```jsx
function createStream(iterator) {
  return new ReadableStream({
    async pull(controller) {
      const { value, done } = await iterator.next();

      if (done) {
        controller.close();
      } else {
        controller.enqueue(value);
      }
    },
  });
}
```

### Benefits of Lazy Streaming

1. **Back-pressure**: Production matches consumption rate
2. **Cancellation**: When reads stop, yields stop automatically
3. **Resource Management**: Stream lifetime is tied to reader lifetime
4. **Memory Efficiency**: Only one item maintained in the buffer

### Application to AI Responses

When a user navigates away or a connection is closed:
- **Eager approach**: Connection continues, memory grows until exhaustion
- **Lazy approach**: Resources automatically freed when fetch connection aborts

---

## Caching Responses

### Using Language Model Middleware (Recommended)

Language model middleware intercepts and modifies calls to language models. Use `simulateReadableStream` for cached streaming responses:

```ts
import { simulateReadableStream, type LanguageModelV2Middleware } from 'ai';
import { Redis } from '@upstash/redis';

export const cacheMiddleware: LanguageModelV2Middleware = {
  wrapGenerate: async ({ doGenerate, params }) => {
    const cacheKey = JSON.stringify(params);
    const cached = await redis.get(cacheKey);

    if (cached !== null) {
      return cached;
    }

    const result = await doGenerate();
    redis.set(cacheKey, result);
    return result;
  },
  wrapStream: async ({ doStream, params }) => {
    const cacheKey = JSON.stringify(params);
    const cached = await redis.get(cacheKey);

    if (cached !== null) {
      return {
        stream: simulateReadableStream({
          initialDelayInMs: 0,
          chunkDelayInMs: 10,
          chunks: cached,
        }),
      };
    }

    const { stream, ...rest } = await doStream();
    // Cache the full response after streaming completes
    // using TransformStream
  },
};
```

### Using Lifecycle Callbacks

Use the `onFinish` callback to cache responses:

```tsx
const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  messages: convertToModelMessages(messages),
  async onFinish({ text }) {
    await redis.set(key, text);
    await redis.expire(key, 60 * 60); // 1 hour TTL
  },
});
```

---

## Multiple Streams

### Multiple Streamable UIs

Create and return multiple independent streamable UIs in a single request:

```tsx
import { createStreamableUI } from '@ai-sdk/rsc';

export async function getWeather() {
  const weatherUI = createStreamableUI();
  const forecastUI = createStreamableUI();

  weatherUI.update(<div>Loading weather...</div>);
  forecastUI.update(<div>Loading forecast...</div>);

  getWeatherData().then(weatherData => {
    weatherUI.done(<div>{weatherData}</div>);
  });

  getForecastData().then(forecastData => {
    forecastUI.done(<div>{forecastData}</div>);
  });

  return {
    requestedAt: Date.now(),
    weather: weatherUI.value,
    forecast: forecastUI.value,
  };
}
```

### Nested Streamable UIs

Stream UI components within other UI components for complex, composable interfaces:

```tsx
async function getStockHistoryChart({ symbol: string }) {
  'use server';

  const ui = createStreamableUI(<Spinner />);

  (async () => {
    const price = await getStockPrice({ symbol });
    const historyChart = createStreamableUI(<Spinner />);
    ui.done(<StockCard historyChart={historyChart.value} price={price} />);

    const historyData = await fetch('https://my-stock-data-api.com');
    historyChart.done(<HistoryChart data={historyData} />);
  })();

  return ui;
}
```

---

## Rate Limiting

### Implementation with Vercel KV and Upstash Ratelimit

Protect APIs from abuse by setting a maximum request threshold:

```tsx
import kv from '@vercel/kv';
import { streamText } from 'ai';
import { Ratelimit } from '@upstash/ratelimit';

export const maxDuration = 30;

const ratelimit = new Ratelimit({
  redis: kv,
  limiter: Ratelimit.fixedWindow(5, '30s'), // 5 requests per 30 seconds
});

export async function POST(req: NextRequest) {
  const ip = req.ip ?? 'ip';
  const { success, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return new Response('Ratelimited!', { status: 429 });
  }

  const { messages } = await req.json();

  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    messages,
  });

  return result.toUIMessageStreamResponse();
}
```

---

## Rendering User Interfaces with Language Models

### From Text to Components

Instead of returning text from tools, return JSON objects that can render React components:

```tsx
tools: {
  getWeather: {
    description: 'Get the weather for a location',
    parameters: z.object({
      city: z.string(),
      unit: z.enum(['C', 'F']),
    }),
    execute: async ({ city, unit }) => {
      const weather = getWeather({ city, unit });
      return {
        temperature: weather.temperature,
        unit,
        description: weather.description,
        forecast: weather.forecast,
      };
    },
  },
},
```

### Client-Side Rendering

Conditionally render components based on tool call responses:

```tsx
{messages.map(message => {
  if (message.role === 'tool') {
    return (
      <WeatherCard
        weather={{
          temperature: message.content.temperature,
          unit: message.content.unit,
          description: message.content.description,
        }}
      />
    );
  }
})}
```

### Server-Side Rendering with RSC

Use `createStreamableUI` from `@ai-sdk/rsc` to stream React components directly from the server:

```tsx
import { createStreamableUI } from '@ai-sdk/rsc';

const uiStream = createStreamableUI();

// In tool execute:
uiStream.done(
  <WeatherCard
    weather={{
      temperature: 47,
      unit: 'F',
      description: 'sunny',
      forecast,
    }}
  />
);

return { display: uiStream.value };
```

Client-side becomes simplified:
```tsx
{messages.map(message => (
  <div>{message.display}</div>
))}
```

---

## Generative User Interfaces

### Deterministic Routes vs Probabilistic Routing

Generative UIs are not deterministic - they depend on model generation output. However, language models can limit their generations using function calling:

- Execute a function most relevant to the user query
- Not execute any function if the query is out of bounds

```tsx
tools: {
  getWeather: {
    description: 'Get the weather in a location',
    parameters: z.object({
      location: z.string(),
    }),
    execute: async ({ location }) => ({
      location,
      temperature: 72 + Math.floor(Math.random() * 21) - 10,
    }),
  },
},

sendMessage('What is the weather in San Francisco?'); // getWeather is called
sendMessage('What events are happening in London?'); // No function is called
```

### Language Models as Routers

LLMs can act as intelligent routers, replacing traditional route-based navigation:

**Routing by Parameters**:
- For dynamic routes like `/profile/[username]` or `/search?q=[query]`
- Model generates correct parameters and renders appropriate UI

**Routing by Sequence**:
- For multi-step actions requiring navigation through different routes
- Example: "Schedule a happy hour with friends" triggers:
  1. Lookup your calendar
  2. Lookup friends' calendars
  3. Determine best time
  4. Search for nearby locations
  5. Create event and send invites

---

## Multistep Interfaces

### Key Concepts

1. **Tool Composition**: Combining multiple tools to create complex workflows
2. **Application Context**: The conversation history and state that informs model responses

### Application Context Example

Meal logging application with `log_meal` and `delete_meal` tools:

```txt
User: Log a chicken shawarma for lunch.
Tool: log_meal("chicken shawarma", "250g", "12:00 PM")
Model: Chicken shawarma has been logged for lunch.
...
User: I skipped lunch today, can you update my log?
Tool: delete_meal("chicken shawarma")
Model: Chicken shawarma has been deleted from your log.
```

The model uses previous context to identify what to delete.

### Tool Composition Example

Flight booking assistant with composable tools:

```txt
User: I want to book a flight from New York to London.
Tool: searchFlights("New York", "London")
Model: Here are the available flights.
User: I want to book flight BA123 on 12th December for myself and my wife.
Tool: lookupContacts() -> ["John Doe", "Jane Doe"]
Tool: bookFlight("BA123", "12th December", ["John Doe", "Jane Doe"])
Model: Your flight has been booked!
```

Tools like `lookupContacts` can populate context, reducing user input required.

---

## Sequential Generations

### Chaining Generations

Create sequences where one generation's output becomes the next generation's input:

```typescript
import { generateText } from 'ai';

async function sequentialActions() {
  // Step 1: Generate ideas
  const ideasGeneration = await generateText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt: 'Generate 10 ideas for a blog post about making spaghetti.',
  });

  // Step 2: Pick the best idea
  const bestIdeaGeneration = await generateText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt: `Here are some ideas:
${ideasGeneration}

Pick the best idea and explain why.`,
  });

  // Step 3: Generate outline
  const outlineGeneration = await generateText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt: `We've chosen:
${bestIdeaGeneration}

Create a detailed outline for this blog post.`,
  });
}
```

---

## Vercel Deployment Guide

### Prerequisites

- Vercel account
- Git provider account (GitHub, GitLab, Bitbucket)
- OpenAI API key

### Deployment Steps

1. **Commit Changes**: Ensure `.gitignore` excludes `.env` and `node_modules`
2. **Create Git Repository**: Create repo on GitHub and push your code
3. **Import to Vercel**: On Vercel's New Project page, import your Git repository
4. **Add Environment Variables**: Paste your `.env.local` contents in the Environment Variables section
5. **Deploy**: Press Deploy button

### Important Considerations

#### Function Duration

Default serverless function timeout is 10 seconds (Hobby Tier). Extend with route segment config:

```ts
export const maxDuration = 30; // Up to 60 seconds on Hobby Tier
```

#### Security Measures

1. **Rate Limiting**: Protect against abuse by limiting requests per time frame
2. **Firewall**: Vercel Firewall provides DDoS protection and custom rules for IP blocking

### Troubleshooting

- Streaming not working when proxied
- Experiencing timeouts on Vercel

---

## Quick Reference: Key Imports

```typescript
// Core functions
import { generateText, streamText, convertToModelMessages } from 'ai';

// UI streaming (RSC)
import { createStreamableUI } from '@ai-sdk/rsc';

// React hooks
import { useChat, useCompletion } from '@ai-sdk/react';

// Middleware and utilities
import {
  simulateReadableStream,
  consumeStream,
  formatDataStreamPart,
  type LanguageModelV2Middleware,
} from 'ai';

// Rate limiting
import { Ratelimit } from '@upstash/ratelimit';
import kv from '@vercel/kv';
```
