# Vercel AI SDK Foundation - Summary

This document provides a comprehensive summary of the foundational concepts in the Vercel AI SDK, covering the core building blocks needed to build AI-powered applications.

---

## Overview: Core AI Concepts

### Generative Artificial Intelligence

Generative AI refers to models that predict and generate various types of outputs (text, images, audio) based on patterns learned from training data. Examples include:

- Generating captions from photos
- Transcribing audio files
- Creating images from text descriptions

### Large Language Models (LLMs)

LLMs are a subset of generative models focused primarily on text. Key characteristics:

- Takes a sequence of words as input
- Predicts the most likely sequence to follow
- Assigns probabilities to potential next sequences
- Continues generating until a stopping criterion is met

**Important Limitations**: LLMs can "hallucinate" or fabricate information when asked about less-known or absent information. The quality of responses depends on how well-represented the information is in the model's training data.

### Embedding Models

Embedding models convert complex data (words, images) into dense vector representations (embeddings). Unlike generative models:

- They do not generate new text or data
- They provide representations of semantic and syntactic relationships
- Used as input for other models or NLP tasks

---

## Providers and Models

### The Provider Architecture Problem

Different AI providers (OpenAI, Anthropic, etc.) have unique interfaces for their models, creating:

- Complexity when switching providers
- Risk of vendor lock-in

### AI SDK Solution

The AI SDK offers a standardized approach through a language model specification that abstracts provider differences, allowing developers to switch between providers using the same API.

### Official AI SDK Providers

The SDK includes providers for major platforms:

- **xAI Grok** (`@ai-sdk/xai`)
- **OpenAI** (`@ai-sdk/openai`)
- **Azure OpenAI** (`@ai-sdk/azure`)
- **Anthropic** (`@ai-sdk/anthropic`)
- **Amazon Bedrock** (`@ai-sdk/amazon-bedrock`)
- **Google Generative AI** (`@ai-sdk/google`)
- **Google Vertex** (`@ai-sdk/google-vertex`)
- **Mistral** (`@ai-sdk/mistral`)
- **Together.ai** (`@ai-sdk/togetherai`)
- **Cohere** (`@ai-sdk/cohere`)
- **Fireworks** (`@ai-sdk/fireworks`)
- **DeepInfra** (`@ai-sdk/deepinfra`)
- **DeepSeek** (`@ai-sdk/deepseek`)
- **Cerebras** (`@ai-sdk/cerebras`)
- **Groq** (`@ai-sdk/groq`)
- **Perplexity** (`@ai-sdk/perplexity`)
- **ElevenLabs** (`@ai-sdk/elevenlabs`)
- **And many more...**

### Community Providers

The open-source community has created additional providers including:

- Ollama, FriendliAI, Portkey, Cloudflare Workers AI, OpenRouter, and many others

### Self-Hosted Models

Access self-hosted models through:

- Ollama Provider
- LM Studio
- Baseten
- Built-in AI
- Any OpenAI-compatible provider

### Model Capabilities

Models vary in their support for:

- **Image Input**: Processing images as input
- **Object Generation**: Structured output generation
- **Tool Usage**: Function calling capabilities
- **Tool Streaming**: Streaming tool call results

---

## Prompts

Prompts are instructions given to LLMs. The AI SDK simplifies prompting with three types: text, message, and system prompts.

### Text Prompts

Simple string prompts ideal for straightforward generation tasks:

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Invent a new holiday and describe its traditions.',
});
```

Template literals can inject dynamic data:

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt:
    `I am planning a trip to ${destination} for ${lengthOfStay} days. ` +
    `Please suggest the best tourist activities for me to do.`,
});
```

### System Prompts

Initial instructions that guide and constrain model behavior:

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  system:
    `You help planning travel itineraries. ` +
    `Respond to the users' request with a list ` +
    `of the best stops to make in their destination.`,
  prompt: `I am planning a trip to ${destination}...`,
});
```

### Message Prompts

Array of user, assistant, and tool messages for chat interfaces and multi-modal prompts:

```ts
const result = await generateText({
  model: 'anthropic/claude-sonnet-4.5',
  messages: [
    { role: 'user', content: 'Hi!' },
    { role: 'assistant', content: 'Hello, how can I help?' },
    { role: 'user', content: 'Where can I buy the best Currywurst in Berlin?' },
  ],
});
```

### Provider Options

Provider-specific metadata can be passed at three levels:

1. **Function Call Level**: Via `providerOptions` property
2. **Message Level**: Via `providerOptions` on message objects
3. **Message Part Level**: For specific content parts (e.g., image detail settings)

### User Message Content Types

#### Text Parts

Standard text content, can be string or array of parts.

#### Image Parts

Images can be provided as:

- Base64-encoded strings or data URLs
- Binary data (ArrayBuffer, Uint8Array, Buffer)
- URLs (http/https strings or URL objects)

#### File Parts

Supported by select providers (Google, OpenAI, Anthropic) for PDFs, audio files, etc. Requires specifying MIME type.

### Assistant Messages

Can contain:

- Text content
- Reasoning content
- Tool call parts

### Tool Messages

Contain tool output parts with results matching tool call IDs:

```ts
{
  role: 'tool',
  content: [
    {
      type: 'tool-result',
      toolCallId: '12345',
      toolName: 'get-nutrition-data',
      output: {
        type: 'json',
        value: { name: 'Cheese', calories: 369 },
      },
    },
  ],
}
```

### Multi-modal Tool Results (Experimental)

Tool results can include multiple parts (text, images) using `experimental_content` property. Currently only supported by Anthropic.

### Custom Download Function (Experimental)

The `experimental_download` property allows custom file download handling for throttling, retries, authentication, and caching.

---

## Tools

Tools extend LLM capabilities for discrete tasks and external interactions.

### Tool Structure

A tool consists of three properties:

1. **`description`**: Optional description influencing tool selection
2. **`inputSchema`**: Zod or JSON schema defining required input
3. **`execute`**: Optional async function called with tool arguments

### Schema Definition

The SDK supports Zod schemas and raw JSON schemas:

```ts
import z from 'zod';

const recipeSchema = z.object({
  recipe: z.object({
    name: z.string(),
    ingredients: z.array(
      z.object({
        name: z.string(),
        amount: z.string(),
      }),
    ),
    steps: z.array(z.string()),
  }),
});
```

### Tool Packages

Tools are JavaScript objects that can be packaged and distributed via npm:

```ts
// Using a tool package
import { searchTool } from 'some-tool-package';

const { text } = await generateText({
  model: 'anthropic/claude-haiku-4.5',
  prompt: 'When was Vercel Ship AI?',
  tools: {
    webSearch: searchTool,
  },
  stopWhen: stepCountIs(10),
});
```

### Ready-to-Use Tool Packages

Popular tool packages include:

- **@exalabs/ai-sdk** - Web search
- **@tavily/ai-sdk** - Search, extract, crawl, and map tools
- **@perplexity-ai/ai-sdk** - Real-time web search
- **Stripe agent tools** - Stripe interactions
- **Composio** - 250+ tools (GitHub, Gmail, Salesforce, etc.)
- **agentic** - 20+ tools for external APIs
- **Amazon Bedrock AgentCore** - Browser and Code Interpreter tools
- **JigsawStack** - 30+ custom fine-tuned models
- **Toolhouse** - 25+ different actions

### MCP Tools

Pre-built tools available as MCP servers:

- **Smithery** - 6,000+ MCPs marketplace
- **Pipedream** - 3,000+ integrations
- **Apify** - Web scraping and browser automation tools

### Publishing Custom Tools

Export tool objects from your package:

```ts
export const myTool = {
  description: 'A helpful tool',
  inputSchema: z.object({
    query: z.string(),
  }),
  execute: async ({ query }) => {
    return result;
  },
};
```

---

## Streaming

Streaming enables displaying LLM responses progressively as they become available.

### The Problem with Blocking UIs

LLMs can be slow when generating long outputs (5-40+ seconds), causing poor user experience with traditional blocking interfaces that display loading spinners until complete.

### Streaming UI Benefits

- Display parts of responses as they become available
- Significantly improved perceived performance
- Better user experience for conversational applications

### Implementation

The AI SDK makes streaming simple with the `streamText` function:

```ts
import { streamText } from 'ai';

const { textStream } = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  prompt: 'Write a poem about embedding models.',
});

for await (const textPart of textStream) {
  console.log(textPart);
}
```

### When to Use Streaming

- **Use streaming**: For larger models and longer outputs where latency would otherwise be noticeable
- **Consider blocking**: For smaller, faster models where streaming complexity isn't necessary

---

## Key API Functions Reference

| Function | Purpose |
|----------|---------|
| `generateText` | Generate text with blocking response |
| `streamText` | Generate text with streaming response |
| `generateObject` | Generate structured objects |
| `streamObject` | Generate structured objects with streaming |
| `streamUI` | Stream React components (uses `generate` function) |

---

## Best Practices Summary

1. **Choose the right provider** for your use case based on model capabilities
2. **Use system prompts** to guide and constrain model behavior consistently
3. **Leverage message prompts** for conversational interfaces
4. **Define clear tool schemas** using Zod for type safety and validation
5. **Implement streaming** for better UX with larger models
6. **Consider provider options** for provider-specific optimizations
7. **Use multi-step calls** for automatic tool result handling
8. **Handle LLM limitations** - be aware of potential hallucinations for obscure topics
