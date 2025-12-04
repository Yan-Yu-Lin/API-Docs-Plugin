# OpenRouter Community Integrations Summary

This document provides a comprehensive summary of the OpenRouter community frameworks and integrations documentation.

---

## Frameworks and Integrations Overview

OpenRouter provides seamless integration with popular AI frameworks and SDKs, making it easy to incorporate OpenRouter's capabilities into various application environments.

### Available Framework Integrations

OpenRouter officially supports the following major frameworks:

| Framework | Description |
|-----------|-------------|
| **Effect AI SDK** | Integration with TypeScript Effect applications |
| **LangChain** | Integration for Python and JavaScript applications |
| **LlamaIndex** | Integration for Python and TypeScript RAG (Retrieval-Augmented Generation) applications |
| **Mastra** | Unified interface for AI model access |
| **OpenAI SDK** | Direct integration using the official OpenAI SDK for Python and TypeScript |
| **PydanticAI** | High-level interface for Python applications |
| **Vercel AI SDK** | Integration with Next.js applications |

### Other Integrations

OpenRouter also integrates with various coding assistants and development tools:

- **Aider** - Coding assistant integration
- **Cline** - Coding assistant integration
- **Kilo Code** - Coding assistant integration
- **Langfuse** - Observability and tracing integration
- **Roo Code** - Coding assistant integration
- **VSCode Copilot** - Bring your own language model key support
- **Xcode** - Coding assistant integration

Additional examples are available in the [OpenRouter GitHub repository](https://github.com/OpenRouterTeam/openrouter-examples).

---

## Vercel AI SDK Integration

The Vercel AI SDK integration allows developers to use OpenRouter with Next.js applications for building AI-powered features.

### Installation

Install the OpenRouter AI SDK provider package:

```bash
npm install @openrouter/ai-sdk-provider
```

### Core API Usage

#### Creating an OpenRouter Client

```typescript
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

const openrouter = createOpenRouter({
  apiKey: 'YOUR_OPENROUTER_API_KEY',
});
```

#### Streaming Text with `streamText()`

The `streamText()` API enables streaming text responses from OpenRouter models:

```typescript
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { streamText } from 'ai';

export const getLasagnaRecipe = async (modelName: string) => {
  const openrouter = createOpenRouter({
    apiKey: 'YOUR_OPENROUTER_API_KEY',
  });

  const response = streamText({
    model: openrouter(modelName),
    prompt: 'Write a vegetarian lasagna recipe for 4 people.',
  });

  await response.consumeStream();
  return response.text;
};
```

### Tool Usage with Vercel AI SDK

The integration supports tool definitions using Zod schemas for parameter validation. This allows AI models to call functions with structured parameters:

```typescript
import { createOpenRouter } from '@openrouter/ai-sdk-provider';
import { streamText } from 'ai';
import { z } from 'zod';

export const getWeather = async (modelName: string) => {
  const openrouter = createOpenRouter({
    apiKey: 'YOUR_OPENROUTER_API_KEY',
  });

  const response = streamText({
    model: openrouter(modelName),
    prompt: 'What is the weather in San Francisco, CA in Fahrenheit?',
    tools: {
      getCurrentWeather: {
        description: 'Get the current weather in a given location',
        parameters: z.object({
          location: z
            .string()
            .describe('The city and state, e.g. San Francisco, CA'),
          unit: z.enum(['celsius', 'fahrenheit']).optional(),
        }),
        execute: async ({ location, unit = 'celsius' }) => {
          // Implementation to fetch or return weather data
          const weatherData = {
            'Boston, MA': { celsius: '15°C', fahrenheit: '59°F' },
            'San Francisco, CA': { celsius: '18°C', fahrenheit: '64°F' },
          };

          const weather = weatherData[location];
          if (!weather) {
            return `Weather data for ${location} is not available.`;
          }

          return `The current weather in ${location} is ${weather[unit]}.`;
        },
      },
    },
  });

  await response.consumeStream();
  return response.text;
};
```

### Key Patterns for Vercel AI SDK Integration

1. **Provider Creation**: Use `createOpenRouter()` to initialize the provider with your API key
2. **Model Selection**: Pass the model name dynamically via `openrouter(modelName)`
3. **Streaming Responses**: Use `streamText()` for streaming text generation
4. **Tool Definitions**: Define tools with Zod schemas for type-safe parameter validation
5. **Stream Consumption**: Call `response.consumeStream()` to process the stream before accessing `response.text`

---

## Key Resources

- [OpenRouter Examples GitHub Repository](https://github.com/OpenRouterTeam/openrouter-examples)
- [Vercel AI SDK npm Package](https://www.npmjs.com/package/ai)
- [@openrouter/ai-sdk-provider GitHub](https://github.com/OpenRouterTeam/ai-sdk-provider)
- [Vercel AI SDK streamText() Documentation](https://sdk.vercel.ai/docs/reference/ai-sdk-core/stream-text)
- [LlamaIndex OpenRouter Integration](https://developers.llamaindex.ai/python/framework-api-reference/llms/openrouter/)
