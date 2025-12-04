# OpenRouter Overview Summary

This document provides a comprehensive summary of OpenRouter's documentation, covering core concepts, API usage, authentication methods, and multimodal capabilities.

---

## Table of Contents

1. [Core Principles](#core-principles)
2. [Quickstart Guide](#quickstart-guide)
3. [Models](#models)
4. [Frequently Asked Questions](#frequently-asked-questions)
5. [Authentication](#authentication)
   - [BYOK (Bring Your Own Key)](#byok-bring-your-own-key)
   - [OAuth PKCE](#oauth-pkce)
   - [Provisioning API Keys](#provisioning-api-keys)
6. [Multimodal Capabilities](#multimodal-capabilities)
   - [Overview](#multimodal-overview)
   - [Image Inputs](#image-inputs)
   - [Image Generation](#image-generation)
   - [Audio Inputs](#audio-inputs)
   - [PDF Inputs](#pdf-inputs)
   - [Video Inputs](#video-inputs)

---

## Core Principles

OpenRouter helps developers source and optimize AI usage, built on the belief that the future is multi-model and multi-provider.

### Why OpenRouter?

- **Price and Performance**: Scouts for the best prices, lowest latencies, and highest throughput across dozens of providers with configurable prioritization
- **Standardized API**: No code changes needed when switching between models or providers; users can choose and pay for their own models
- **Real-World Insights**: Early access to new models with real-world usage data showing how often models are used for different purposes
- **Consolidated Billing**: Simple and transparent billing regardless of provider count
- **Higher Availability**: Fallback providers and automatic smart routing ensure requests work even when providers go down
- **Higher Rate Limits**: Direct partnerships with providers enable better rate limits and throughput

---

## Quickstart Guide

OpenRouter provides a unified API giving access to hundreds of AI models through a single endpoint with automatic fallbacks and cost optimization.

### Installation Options

**OpenRouter SDK (Beta):**
```bash
npm install @openrouter/sdk
# or
yarn add @openrouter/sdk
# or
pnpm add @openrouter/sdk
```

### Basic Usage Examples

**Using TypeScript SDK:**
```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  defaultHeaders: {
    'HTTP-Referer': '<YOUR_SITE_URL>',  // Optional - for rankings
    'X-Title': '<YOUR_SITE_NAME>',       // Optional - for rankings
  },
});

const completion = await openRouter.chat.send({
  model: 'openai/gpt-4o',
  messages: [{ role: 'user', content: 'What is the meaning of life?' }],
  stream: false,
});
```

**Using OpenAI SDK:**
```typescript
import OpenAI from 'openai';

const openai = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: '<OPENROUTER_API_KEY>',
});

const completion = await openai.chat.completions.create({
  model: 'openai/gpt-4o',
  messages: [{ role: 'user', content: 'What is the meaning of life?' }],
});
```

**Direct API Call (curl):**
```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [{"role": "user", "content": "What is the meaning of life?"}]
  }'
```

### API Endpoint
- Base URL: `https://openrouter.ai/api/v1/chat/completions`
- OpenRouter is a drop-in replacement for OpenAI SDK

---

## Models

OpenRouter provides access to 400+ AI models through a unified API.

### Models API Schema

**Root Response:**
```json
{
  "data": [/* Array of Model objects */]
}
```

**Model Object Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique model identifier (e.g., `"google/gemini-2.5-pro-preview"`) |
| `canonical_slug` | string | Permanent slug that never changes |
| `name` | string | Human-readable display name |
| `created` | number | Unix timestamp when added to OpenRouter |
| `description` | string | Model capabilities description |
| `context_length` | number | Maximum context window in tokens |
| `architecture` | object | Technical capabilities (modalities, tokenizer) |
| `pricing` | object | Cost structure per token/request/unit |
| `supported_parameters` | string[] | Supported API parameters |

**Architecture Object:**
```typescript
{
  "input_modalities": string[],  // ["file", "image", "text"]
  "output_modalities": string[], // ["text"]
  "tokenizer": string,
  "instruct_type": string | null
}
```

**Pricing Object (USD per token/request/unit):**
```typescript
{
  "prompt": string,              // Cost per input token
  "completion": string,          // Cost per output token
  "request": string,             // Fixed cost per request
  "image": string,               // Cost per image input
  "web_search": string,          // Cost per web search
  "internal_reasoning": string,  // Cost for reasoning tokens
  "input_cache_read": string,    // Cost per cached token read
  "input_cache_write": string    // Cost per cached token write
}
```

### Model Variants

**Static Variants (model-specific):**
- `:free` - Free with low rate limits
- `:extended` - Longer context length
- `:exacto` - OpenRouter-curated high-quality endpoints only
- `:thinking` - Reasoning by default

**Dynamic Variants (all models):**
- `:online` - Web results attached to prompt
- `:nitro` - Sorted by throughput for faster responses
- `:floor` - Sorted by price for cost-effectiveness

### Supported Parameters
- `tools`, `tool_choice` - Function calling
- `max_tokens`, `temperature`, `top_p` - Response control
- `reasoning`, `include_reasoning` - Internal reasoning
- `structured_outputs`, `response_format` - Output formatting
- `stop`, `frequency_penalty`, `presence_penalty`, `seed`

---

## Frequently Asked Questions

### Getting Started
- **Why OpenRouter?** Unified API for all major LLMs with pass-through pricing and pooled uptime
- **How to start?** Create account, add credits, use API or chat interface
- **Support:** Discord (#help forum) for technical; support@openrouter.ai for billing

### Pricing and Fees
- Credit purchase fee charged (varies by payment method)
- No markup on inference pricing
- BYOK: First requests free monthly, then percentage fee of normal cost

### Rate Limits
- Free models: Rate limited based on credit purchase history
- Paid accounts: See rate limits documentation

### API Features
- OpenAI-compatible `/completions` and `/chat/completions` endpoints
- Streaming via server-sent events (SSE) with `stream: true`
- Supports text, images, and PDFs

### Privacy
- Basic metadata logged (timestamps, model, token counts)
- Prompts/completions NOT logged by default
- Optional 1% discount for opting into logging
- Providers that log are not routed to unless enabled in settings

### Credits
- USD-based credit system
- Manual top-up or auto top-up available
- Credits may expire after one year (per terms)
- Payment methods: Credit cards, AliPay, USDC cryptocurrency

---

## Authentication

OpenRouter supports three authentication methods:
1. Cookie-based authentication for web interface
2. API keys (Bearer tokens) for API access
3. Provisioning API keys for programmatic key management

### BYOK (Bring Your Own Key)

Bring your own provider API keys to control rate limits and costs directly with providers.

**Key Features:**
- Keys securely encrypted
- Prioritizes your keys when available
- Falls back to OpenRouter credits if key fails (configurable)
- "Always use this key" option prevents fallbacks

**Pricing:**
- First requests per month: FREE
- Subsequent usage: Percentage of normal OpenRouter cost, deducted from credits

**Supported Providers:**

**Azure AI Services:**
```json
{
  "model_slug": "openai/gpt-4o",
  "endpoint_url": "https://<resource>.services.ai.azure.com/deployments/<model-id>/chat/completions?api-version=<version>",
  "api_key": "your-azure-api-key",
  "model_id": "gpt-4o"
}
```

**AWS Bedrock:**
- Option 1: Bedrock API key (simpler, region-locked)
- Option 2: AWS credentials JSON with `accessKeyId`, `secretAccessKey`, `region`
- Required IAM permissions: `bedrock:InvokeModel`, `bedrock:InvokeModelWithResponseStream`

**Google Vertex AI:**
- Service account JSON with optional `region` field
- Required permissions: `aiplatform.endpoints.predict`, `aiplatform.endpoints.streamingPredict`

### OAuth PKCE

Enable users to connect to OpenRouter in one click using PKCE (Proof Key for Code Exchange).

**Step 1: Redirect to OpenRouter**
```
https://openrouter.ai/auth?callback_url=<YOUR_SITE_URL>&code_challenge=<CODE_CHALLENGE>&code_challenge_method=S256
```

**Step 2: Generate Code Challenge (S256 recommended)**
```typescript
import { Buffer } from 'buffer';

async function createSHA256CodeChallenge(input: string) {
  const encoder = new TextEncoder();
  const data = encoder.encode(input);
  const hash = await crypto.subtle.digest('SHA-256', data);
  return Buffer.from(hash).toString('base64url');
}

const codeVerifier = 'your-random-string';
const generatedCodeChallenge = await createSHA256CodeChallenge(codeVerifier);
```

**Step 3: Exchange Code for API Key**
```typescript
const response = await fetch('https://openrouter.ai/api/v1/auth/keys', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: '<CODE_FROM_QUERY_PARAM>',
    code_verifier: '<CODE_VERIFIER>',
    code_challenge_method: 'S256',
  }),
});
const { key } = await response.json();
```

**Error Codes:**
- `400`: Invalid code_challenge_method
- `403`: Invalid code or code_verifier
- `405`: Must use POST and HTTPS

### Provisioning API Keys

Programmatically manage API keys for automated distribution and rotation.

**Use Cases:**
- SaaS applications: Create unique keys per customer
- Key rotation for security compliance
- Usage monitoring with automatic disable on limit exceed

**Create Provisioning Key:**
1. Go to Settings > Provisioning API Keys
2. Create new key (cannot be used for completions, only key management)

**API Endpoints:** `/api/v1/keys`

**Operations:**
```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({ apiKey: 'your-provisioning-key' });

// List keys (paginated)
const keys = await openRouter.apiKeys.list();
const keysPage2 = await openRouter.apiKeys.list({ offset: 100 });

// Create key
const newKey = await openRouter.apiKeys.create({
  name: 'Customer Instance Key',
  limit: 1000,  // Optional credit limit
});

// Get specific key
const key = await openRouter.apiKeys.get(keyHash);

// Update key
const updatedKey = await openRouter.apiKeys.update(keyHash, {
  name: 'Updated Key Name',
  disabled: true,
  limitReset: 'daily',  // Reset limit at midnight UTC
});

// Delete key
await openRouter.apiKeys.delete(keyHash);
```

**Response Format:**
```json
{
  "data": [{
    "hash": "<KEY_HASH>",
    "label": "sk-or-v1-abc...123",
    "name": "Customer Key",
    "disabled": false,
    "limit": 10,
    "limit_remaining": 10,
    "limit_reset": null,
    "usage": 0,
    "usage_daily": 0,
    "usage_weekly": 0,
    "usage_monthly": 0
  }]
}
```

---

## Multimodal Capabilities

OpenRouter supports multiple input modalities beyond text through the unified `/api/v1/chat/completions` endpoint.

### Multimodal Overview

**Supported Modalities:**
- **Images**: Vision analysis, description, OCR
- **Image Generation**: Create images from text prompts
- **PDFs**: Document processing with any model
- **Audio**: Transcription, analysis, processing
- **Video**: Analysis, description, object detection

**Content Types:**
- Images: `image_url`
- PDFs: `file`
- Audio: `input_audio`
- Video: `video_url`

**Input Formats:**
- **URLs** (recommended for public content): More efficient, reduces payload size
- **Base64** (required for local/private files): `data:<mime-type>;base64,{data}`

**Pricing by Modality:**
- Images: Per image or as input tokens
- PDFs: Free text extraction, paid OCR, or native model pricing
- Audio: Priced as input tokens by duration
- Video: Priced as input tokens by duration and resolution

### Image Inputs

Send images to vision-capable models via `image_url` content type.

**Using URL:**
```typescript
const result = await openRouter.chat.send({
  model: 'google/gemini-2.0-flash-001',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: "What's in this image?" },
      { type: 'image_url', imageUrl: { url: 'https://example.com/image.jpg' } },
    ],
  }],
});
```

**Using Base64:**
```typescript
async function encodeImageToBase64(imagePath: string): Promise<string> {
  const imageBuffer = await fs.promises.readFile(imagePath);
  const base64Image = imageBuffer.toString('base64');
  return `data:image/jpeg;base64,${base64Image}`;
}

const base64Image = await encodeImageToBase64('path/to/image.jpg');
// Use in imageUrl.url field
```

**Supported Formats:** `image/png`, `image/jpeg`, `image/webp`, `image/gif`

**Tips:**
- Send text prompt first, then images
- If images must come first, put them in system prompt
- Multiple images supported (varies by provider/model)

### Image Generation

Generate images from text prompts using models with `"image"` in `output_modalities`.

**Basic Generation:**
```typescript
const result = await openRouter.chat.send({
  model: 'google/gemini-2.5-flash-image-preview',
  messages: [{ role: 'user', content: 'Generate a beautiful sunset over mountains' }],
  modalities: ['image', 'text'],
  stream: false,
});

// Access generated images
if (result.choices[0].message.images) {
  result.choices[0].message.images.forEach(image => {
    const imageUrl = image.imageUrl.url; // Base64 data URL
  });
}
```

**Aspect Ratio Configuration (Gemini models):**
```typescript
{
  modalities: ['image', 'text'],
  image_config: {
    aspect_ratio: '16:9'  // See supported ratios below
  }
}
```

**Supported Aspect Ratios:**
- `1:1` (1024x1024, default)
- `2:3`, `3:2`, `3:4`, `4:3`
- `4:5`, `5:4`
- `9:16`, `16:9`
- `21:9`

**Response Format:**
```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Description text...",
      "images": [{
        "type": "image_url",
        "image_url": { "url": "data:image/png;base64,..." }
      }]
    }
  }]
}
```

**Compatible Models:**
- `google/gemini-2.5-flash-image-preview`
- `black-forest-labs/flux.2-pro`
- `black-forest-labs/flux.2-flex`

### Audio Inputs

Send audio files to speech-capable models. **Audio must be base64-encoded** (URLs not supported).

**Sending Audio:**
```typescript
async function encodeAudioToBase64(audioPath: string): Promise<string> {
  const audioBuffer = await fs.readFile(audioPath);
  return audioBuffer.toString("base64");
}

const base64Audio = await encodeAudioToBase64("audio.wav");

const result = await openRouter.chat.send({
  model: "google/gemini-2.5-flash",
  messages: [{
    role: "user",
    content: [
      { type: "text", text: "Please transcribe this audio file." },
      { type: "input_audio", inputAudio: { data: base64Audio, format: "wav" } },
    ],
  }],
});
```

**Supported Formats:**
- `wav`, `mp3`, `aiff`, `aac`
- `ogg`, `flac`, `m4a`
- `pcm16`, `pcm24`

Note: Format support varies by provider/model.

### PDF Inputs

Process PDF documents with **any model** on OpenRouter via `file` content type.

**Using URL:**
```typescript
const result = await openRouter.chat.send({
  model: 'anthropic/claude-sonnet-4',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What are the main points in this document?' },
      { type: 'file', file: { filename: 'document.pdf', fileData: 'https://example.com/doc.pdf' } },
    ],
  }],
  plugins: [{ id: 'file-parser', pdf: { engine: 'mistral-ocr' } }],
});
```

**PDF Processing Engines:**

| Engine | Best For | Pricing |
|--------|----------|---------|
| `pdf-text` | Well-structured PDFs with clear text | Free |
| `mistral-ocr` | Scanned documents or PDFs with images | Per 1,000 pages |
| `native` | Models with native file support | As input tokens |

**Default Behavior:** Uses model's native capabilities first, then falls back to `pdf-text`.

**Reusing Annotations (Skip Re-parsing):**
```typescript
// First request - get annotations
const response = await openRouter.chat.send({...});
const fileAnnotations = response.choices[0].message.annotations;

// Follow-up request - include annotations
const followUp = await openRouter.chat.send({
  messages: [
    { role: 'user', content: [...] },
    { role: 'assistant', content: '...', annotations: fileAnnotations },
    { role: 'user', content: 'Follow-up question' },
  ],
});
```

**Using Base64:**
```typescript
function encodePDFToBase64(pdfPath: string): string {
  const pdfBuffer = fs.readFileSync(pdfPath);
  return `data:application/pdf;base64,${pdfBuffer.toString('base64')}`;
}
```

### Video Inputs

Send video files to video-capable models via `video_url` content type.

**Supported Input Methods:**
- Base64 encoding: `data:video/mp4;base64,{data}`
- URLs: Provider-specific (e.g., YouTube links for Gemini on AI Studio)

**Content Type:** `video_url`

**Use Cases:**
- Video analysis and description
- Object detection
- Action recognition

**Note:** Video URL support varies by provider. Check model documentation for specific format and duration limits.

---

## Additional Resources

- **Models Browser:** https://openrouter.ai/models
- **Models API:** https://openrouter.ai/api/v1/models
- **RSS Feed:** https://openrouter.ai/api/v1/models?use_rss=true
- **Discord:** https://discord.gg/openrouter
- **Activity Dashboard:** https://openrouter.ai/activity
- **Support:** support@openrouter.ai
