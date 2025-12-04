---
name: openrouter
description: This skill provides comprehensive documentation for the OpenRouter API, a unified interface for accessing 400+ AI models from multiple providers through a single endpoint. Use this skill when working with OpenRouter API integration, model routing, provider selection, authentication (BYOK, OAuth PKCE, API key provisioning), multimodal capabilities (images, audio, PDFs, video), tool calling, structured outputs, prompt caching, reasoning tokens, web search plugins, or when needing to understand OpenRouter pricing, rate limits, and best practices.
---

# OpenRouter API Documentation

## Overview

OpenRouter is a unified API gateway providing access to 400+ AI models from multiple providers (OpenAI, Anthropic, Google, Meta, Mistral, and others) through a single endpoint. It offers automatic failover, cost optimization, and provider-agnostic model access.

This skill provides complete reference documentation for integrating with the OpenRouter API, including authentication methods, model routing strategies, multimodal capabilities, and best practices for production deployments.

### Key Capabilities

- **Unified API**: OpenAI-compatible API for all major LLMs with no code changes when switching models
- **Model Routing**: Auto model selection, fallbacks, and provider preferences
- **Provider Selection**: Route by price, throughput, latency, or specific providers
- **Multimodal Support**: Images, audio, PDFs, and video inputs
- **Advanced Features**: Tool calling, structured outputs, web search, prompt caching, reasoning tokens

---

## When to Use This Skill

Use this skill when:

- Integrating OpenRouter API into an application
- Setting up authentication (API keys, BYOK, OAuth PKCE)
- Configuring model routing or fallbacks
- Selecting providers based on price, latency, or throughput
- Implementing tool calling or function calling
- Working with structured outputs or JSON schema validation
- Processing multimodal inputs (images, audio, PDFs, video)
- Enabling web search capabilities
- Optimizing costs with prompt caching
- Implementing reasoning tokens for complex tasks
- Setting up observability with Broadcast
- Managing organizations and team access
- Configuring Zero Data Retention (ZDR)
- Using the Vercel AI SDK or other framework integrations

---

## Code Examples

### Basic API Usage

**curl:**
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}]
  }'
```

**TypeScript SDK:**
```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  defaultHeaders: {
    'HTTP-Referer': '<YOUR_SITE_URL>',
    'X-Title': '<YOUR_SITE_NAME>',
  },
});

const completion = await openRouter.chat.send({
  model: 'openai/gpt-4o',
  messages: [{ role: 'user', content: 'What is the meaning of life?' }],
  stream: false,
});
```

**Python (OpenAI SDK):**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_API_KEY",
)

response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
)
```

### Streaming Text

```typescript
import { OpenRouter } from '@openrouter/sdk';
import { streamText } from 'ai';

const openrouter = createOpenRouter({ apiKey: 'YOUR_API_KEY' });

const response = streamText({
  model: openrouter('openai/gpt-4o'),
  prompt: 'Write a vegetarian lasagna recipe.',
});

await response.consumeStream();
console.log(response.text);
```

### Tool Calling

```json
{
  "model": "google/gemini-2.0-flash-001",
  "messages": [{"role": "user", "content": "Search for books by James Joyce"}],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "search_books",
        "description": "Search for books by author",
        "parameters": {
          "type": "object",
          "properties": {
            "author": { "type": "string" }
          },
          "required": ["author"]
        }
      }
    }
  ]
}
```

### Model Fallbacks

```typescript
const completion = await openRouter.chat.send({
  models: ['anthropic/claude-3.5-sonnet', 'openai/gpt-4o', 'google/gemini-2.0-flash'],
  messages: [{ role: 'user', content: 'Hello' }],
});
// Response includes `model` field showing which model was used
```

### Provider Selection

```typescript
// Sort by throughput (fastest)
const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.1-70b-instruct:nitro',
  messages: [{ role: 'user', content: 'Hello' }],
});

// Or use provider object
const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.1-70b-instruct',
  messages: [{ role: 'user', content: 'Hello' }],
  provider: {
    sort: 'throughput',  // or 'price' or 'latency'
    order: ['together', 'fireworks'],  // prefer these providers
    allow_fallbacks: true,
  },
});
```

### Structured Outputs

```json
{
  "model": "openai/gpt-4o",
  "messages": [{"role": "user", "content": "Get weather for Paris"}],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "weather",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "location": { "type": "string" },
          "temperature": { "type": "number" }
        },
        "required": ["location", "temperature"],
        "additionalProperties": false
      }
    }
  }
}
```

### Web Search

```json
{
  "model": "openai/gpt-4o:online",
  "messages": [{"role": "user", "content": "What happened in tech news today?"}]
}
```

### Reasoning Tokens

```typescript
const response = await openRouter.chat.send({
  model: 'openai/o3-mini',
  messages: [{ role: 'user', content: 'How would you build a skyscraper?' }],
  reasoning: { effort: 'high' },  // or { max_tokens: 2000 }
  stream: false,
});

console.log('REASONING:', response.choices[0].message.reasoning);
console.log('CONTENT:', response.choices[0].message.content);
```

---

## Documentation Structure & Navigation

All reference documentation is located in the `references/` folder. Each folder contains a `summary.md` that provides an overview of that section.

### Overview/

**Start here:** `references/Overview/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Principles.md` | Core principles and benefits of OpenRouter |
| `Quickstart.md` | Getting started guide with installation and basic usage |
| `Models.md` | Models API schema, variants, and supported parameters |
| `FAQ.md` | Frequently asked questions about pricing, rate limits, privacy |

**Subfolders:**

- **Authentication/** - Authentication methods
  - `BYOK.md` - Bring Your Own Key setup for Azure, AWS Bedrock, Google Vertex
  - `OAuth PKCE.md` - OAuth flow for user authentication
  - `Provisioning API Keys.md` - Programmatic key management

- **Multimodal/** - Multimodal input/output capabilities
  - `Overview.md` - Supported modalities and content types
  - `Image Inputs.md` - Sending images to vision models
  - `Image Generation.md` - Generating images from text
  - `Audio.md` - Audio transcription and processing
  - `PDF Inputs.md` - PDF document processing
  - `Video Inputs.md` - Video analysis

**When to use:** Getting started, understanding OpenRouter basics, authentication setup, multimodal processing.

**Key topics:** API basics, SDK installation, model schema, authentication (API keys, BYOK, OAuth), images, audio, PDFs, video.

---

### Features/

**Start here:** `references/Features/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Tool Calling.md` | Function calling, tool definitions, agentic loops |
| `Structured Outputs.md` | JSON schema validation for responses |
| `Web Search.md` | Real-time web data with `:online` variant |
| `Presets.md` | Named configurations for model settings |
| `Message Transforms.md` | Middle-out compression for long prompts |
| `Model Transforms.md` | Model routing and transformation options |
| `Zero Data Retention.md` | Privacy controls and ZDR enforcement |
| `Zero Completion Insurance.md` | Cost protection for failed responses |
| `App Attribution.md` | HTTP-Referer and X-Title headers for rankings |
| `Broadcast.md` | Observability integration (Langfuse, Datadog, etc.) |

**When to use:** Implementing advanced features like tool calling, structured outputs, web search, or observability.

**Key topics:** Tools, function calling, JSON schema, web search, presets, transforms, ZDR, observability.

---

### Models & Routing/

**Start here:** `references/Models & Routing/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Auto Model Selection.md` | Using `openrouter/auto` for intelligent model selection |
| `Model Fallbacks.md` | Configuring automatic failover between models |
| `Provider Selection.md` | Provider routing, sorting, filtering (comprehensive - 1325 lines) |

**Subfolder: Model Variants/**
| File | Description |
|------|-------------|
| `Exacto Variant.md` | `:exacto` for curated high-quality tool calling |
| `Extended.md` | `:extended` for longer context windows |
| `Free.md` | `:free` for free model access |
| `Nitro Variant.md` | `:nitro` for high throughput |
| `Online.md` | `:online` for web search |
| `Thinking.md` | `:thinking` for extended reasoning |

**When to use:** Configuring model routing, setting up fallbacks, selecting providers by price/latency/throughput, using model variants.

**Key topics:** Auto router, fallbacks, provider selection, `:nitro`, `:floor`, `:online`, `:free`, `:extended`, `:exacto`, `:thinking`.

---

### Guides/

**Start here:** `references/Guides/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Crypto API.md` | Purchasing credits with cryptocurrency (comprehensive - 1030 lines) |
| `Using MCP Servers with OpenRouter.md` | MCP protocol integration |
| `Organization Management.md` | Team collaboration and shared credits |
| `Provider Integration.md` | Requirements for becoming an OpenRouter provider |
| `Usage Accounting.md` | Token counting and cost tracking |
| `User Tracking.md` | Sub-user tracking for caching and analytics |
| `Distillation.md` | Using outputs for model training |

**When to use:** Advanced use cases like crypto payments, MCP integration, organization setup, usage tracking, or provider integration.

**Key topics:** Cryptocurrency, MCP servers, organizations, billing, user tracking, distillation compliance.

---

### Best Practices/

**Start here:** `references/Best Practices/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Latency and Performance.md` | Optimizing request latency |
| `Prompt Caching.md` | Provider-specific caching strategies (OpenAI, Anthropic, DeepSeek, Gemini) |
| `Reasoning Token.md` | Using reasoning tokens effectively |
| `Uptime Optimization.md` | Maximizing availability with intelligent routing |

**When to use:** Optimizing performance, reducing costs with caching, implementing reasoning capabilities.

**Key topics:** Latency, caching, performance, reasoning tokens, uptime, provider health.

---

### Community/

**Start here:** `references/Community/summary.md`

**Files in this folder:**
| File | Description |
|------|-------------|
| `Frameworks and Integrations Overview.md` | Supported frameworks and tools |
| `Vercel AI SDK.md` | Integration with Next.js applications |

**When to use:** Integrating OpenRouter with specific frameworks (Vercel AI SDK, LangChain, LlamaIndex, etc.).

**Key topics:** Vercel AI SDK, LangChain, LlamaIndex, PydanticAI, coding assistants (Aider, Cline, Kilo Code).

---

## How to Navigate

1. **Start with the relevant `summary.md`** - Each folder contains a summary that provides an overview of all topics in that section.

2. **For comprehensive topics, check file size:**
   - `Provider Selection.md` (1325 lines) - Exhaustive coverage of provider routing
   - `Crypto API.md` (1030 lines) - Complete cryptocurrency integration guide
   - These files contain detailed examples and edge cases

3. **Drill into specific topics** - After reading the summary, navigate to specific files for detailed information.

4. **Use subfolders for related content:**
   - `Overview/Authentication/` for auth methods
   - `Overview/Multimodal/` for image/audio/PDF/video
   - `Models & Routing/Model Variants/` for variant suffixes

---

## Topic Quick Reference

| Question | File Location |
|----------|---------------|
| How do I get started with OpenRouter? | `Overview/Quickstart.md` |
| How do I authenticate API requests? | `Overview/Authentication/` folder |
| How do I use BYOK (Bring Your Own Key)? | `Overview/Authentication/BYOK.md` |
| How do I set up OAuth for users? | `Overview/Authentication/OAuth PKCE.md` |
| How do I create API keys programmatically? | `Overview/Authentication/Provisioning API Keys.md` |
| How do I use model fallbacks? | `Models & Routing/Model Fallbacks.md` |
| How do I select providers by price/latency? | `Models & Routing/Provider Selection.md` |
| What model variants are available? | `Models & Routing/Model Variants/` folder |
| How do I use `:nitro` for fast responses? | `Models & Routing/Model Variants/Nitro Variant.md` |
| How do I enable web search? | `Features/Web Search.md` or `Models & Routing/Model Variants/Online.md` |
| How do I implement tool calling? | `Features/Tool Calling.md` |
| How do I get structured JSON outputs? | `Features/Structured Outputs.md` |
| How do I use presets? | `Features/Presets.md` |
| How do I handle long prompts? | `Features/Message Transforms.md` |
| How do I enable Zero Data Retention? | `Features/Zero Data Retention.md` |
| How do I set up observability? | `Features/Broadcast.md` |
| How do I send images to models? | `Overview/Multimodal/Image Inputs.md` |
| How do I generate images? | `Overview/Multimodal/Image Generation.md` |
| How do I process PDFs? | `Overview/Multimodal/PDF Inputs.md` |
| How do I send audio? | `Overview/Multimodal/Audio.md` |
| How do I optimize latency? | `Best Practices/Latency and Performance.md` |
| How does prompt caching work? | `Best Practices/Prompt Caching.md` |
| How do I use reasoning tokens? | `Best Practices/Reasoning Token.md` |
| How do I pay with cryptocurrency? | `Guides/Crypto API.md` |
| How do I use MCP servers? | `Guides/Using MCP Servers with OpenRouter.md` |
| How do I manage an organization? | `Guides/Organization Management.md` |
| How do I track usage per user? | `Guides/User Tracking.md` |
| How do I use Vercel AI SDK? | `Community/Vercel AI SDK.md` |
| What frameworks are supported? | `Community/Frameworks and Integrations Overview.md` |

---

## API Reference

**Base URL:** `https://openrouter.ai/api/v1`

**Key Endpoints:**
- `POST /chat/completions` - Chat completions (main endpoint)
- `POST /completions` - Text completions
- `GET /models` - List available models
- `GET /credits` - Check credit balance
- `POST /credits/coinbase` - Purchase credits with crypto
- `POST /auth/keys` - OAuth key exchange
- `GET /api/v1/keys` - List provisioned keys
- `POST /api/v1/keys` - Create provisioned key
- `GET /generation` - Get generation details by ID

**Authentication:** Bearer token in Authorization header
```
Authorization: Bearer $OPENROUTER_API_KEY
```
