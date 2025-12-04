# OpenRouter Models & Routing Summary

This document provides a comprehensive summary of OpenRouter's model routing capabilities, including auto model selection, model fallbacks, provider selection, and model variants.

---

## Auto Model Selection

The **Auto Router** (`openrouter/auto`) is a special model ID that automatically selects the best model for your prompt. It is powered by [NotDiamond](https://www.notdiamond.ai/).

### How to Use

Set your model to `openrouter/auto` and OpenRouter will intelligently select the optimal model for your specific prompt:

```typescript
const completion = await openRouter.chat.send({
  model: 'openrouter/auto',
  messages: [{ role: 'user', content: 'What is the meaning of life?' }],
});
```

### Response Behavior

The response will include the actual `model` field set to the model that was used for the request, allowing you to track which model was selected.

---

## Model Fallbacks

The `models` parameter enables automatic failover between models when the primary model's providers are unavailable.

### How It Works

Provide an array of model IDs in priority order. If the first model returns an error, OpenRouter will automatically try the next model in the list:

```typescript
const completion = await openRouter.chat.send({
  models: ['anthropic/claude-3.5-sonnet', 'gryphe/mythomax-l2-13b'],
  messages: [{ role: 'user', content: 'What is the meaning of life?' }],
});
```

### Fallback Triggers

By default, any error can trigger fallback usage:
- Context length validation errors
- Moderation flags for filtered models
- Rate-limiting
- Downtime

### Pricing

Requests are priced based on the model that was ultimately used, which is returned in the `model` attribute of the response body.

### Using with OpenAI SDK

Include the `models` array in the `extra_body` parameter:

```python
completion = openai_client.chat.completions.create(
    model="openai/gpt-4o",
    extra_body={
        "models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"],
    },
    messages=[{"role": "user", "content": "What is the meaning of life?"}]
)
```

---

## Provider Selection (Provider Routing)

OpenRouter routes requests to the best available providers for your model. By default, requests are load balanced across top providers to maximize uptime.

### Provider Object Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `order` | string[] | - | List of provider slugs to try in order |
| `allow_fallbacks` | boolean | `true` | Allow backup providers when primary is unavailable |
| `require_parameters` | boolean | `false` | Only use providers supporting all request parameters |
| `data_collection` | "allow" \| "deny" | "allow" | Control providers that may store data |
| `zdr` | boolean | - | Restrict to Zero Data Retention endpoints |
| `enforce_distillable_text` | boolean | - | Restrict to models allowing text distillation |
| `only` | string[] | - | List of provider slugs to allow |
| `ignore` | string[] | - | List of provider slugs to skip |
| `quantizations` | string[] | - | Filter by quantization levels |
| `sort` | string | - | Sort by "price", "throughput", or "latency" |
| `max_price` | object | - | Maximum pricing for the request |

### Price-Based Load Balancing (Default Strategy)

1. Prioritize providers without significant outages in the last 30 seconds
2. For stable providers, select based on inverse square of price
3. Use remaining providers as fallbacks

**Example**: If Provider A costs $1/M tokens, Provider B costs $2, and Provider C costs $3:
- Provider A is 9x more likely to be selected than Provider C (inverse square: 1/3^2 = 1/9)

### Provider Sorting Options

- `"price"`: Prioritize lowest price
- `"throughput"`: Prioritize highest throughput
- `"latency"`: Prioritize lowest latency

```typescript
const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.1-70b-instruct',
  messages: [{ role: 'user', content: 'Hello' }],
  provider: { sort: 'throughput' },
});
```

### Shortcut Suffixes

- **`:nitro`** - Sort by throughput (equivalent to `provider.sort: "throughput"`)
- **`:floor`** - Sort by price (equivalent to `provider.sort: "price"`)

```typescript
model: 'meta-llama/llama-3.1-70b-instruct:nitro'
```

### Ordering Specific Providers

Use the `order` field to specify provider priority:

```typescript
provider: {
  order: ['openai', 'together'],
}
```

### Targeting Specific Provider Endpoints

Providers may offer multiple endpoints (e.g., default and "turbo"):
- Default endpoint: `deepinfra`
- Turbo endpoint: `deepinfra/turbo`

### Disabling Fallbacks

```typescript
provider: {
  allowFallbacks: false,
}
```

### Allowing/Ignoring Specific Providers

```typescript
// Allow only Azure
provider: { only: ['azure'] }

// Ignore DeepInfra
provider: { ignore: ['deepinfra'] }
```

### Requiring Parameter Support

Only route to providers that support all parameters in your request:

```typescript
provider: {
  requireParameters: true,
}
```

### Data Collection Policies

- `"allow"`: Allow providers that may store/train on data
- `"deny"`: Only use providers that don't collect user data

### Zero Data Retention (ZDR)

Enforce ZDR on a per-request basis:

```typescript
provider: { zdr: true }
```

### Distillable Text Enforcement

Only route to models that allow text distillation:

```typescript
provider: { enforceDistillableText: true }
```

### Quantization Levels

Available quantization options:
- `int4`, `int8`: Integer quantization
- `fp4`, `fp6`, `fp8`, `fp16`, `fp32`: Floating point
- `bf16`: Brain floating point
- `unknown`

```typescript
provider: { quantizations: ['fp8'] }
```

### Maximum Price

Filter providers by maximum acceptable price:

```json
{
  "max_price": {
    "prompt": 1,
    "completion": 2
  }
}
```

Additional attributes: `request` (per-request pricing), `image` (per-image pricing)

### Provider-Specific Headers

#### Anthropic Beta Features

Pass beta headers for Claude models:

| Feature | Header Value | Description |
|---------|--------------|-------------|
| Fine-Grained Tool Streaming | `fine-grained-tool-streaming-2025-05-14` | Granular streaming during tool calls |
| Interleaved Thinking | `interleaved-thinking-2025-05-14` | Interleaved reasoning with output |

```typescript
headers: { 'x-anthropic-beta': 'fine-grained-tool-streaming-2025-05-14' }
```

Combine multiple features:
```
x-anthropic-beta: fine-grained-tool-streaming-2025-05-14,interleaved-thinking-2025-05-14
```

---

## Model Variants

Model variants are suffixes appended to model IDs that modify routing behavior or enable special capabilities.

### Exacto Variant (`:exacto`)

**Purpose**: Curated routing for higher tool-calling accuracy.

Routes to a sub-group of providers with measurably better tool-use success rates. Focused on quality-sensitive, agentic workflows.

**Usage**:
```json
{ "model": "moonshotai/kimi-k2-0905:exacto" }
```

**Supported Models**:
- `moonshotai/kimi-k2-0905:exacto`
- `deepseek/deepseek-v3.1-terminus:exacto`
- `z-ai/glm-4.6:exacto`
- `openai/gpt-oss-120b:exacto`
- `qwen/qwen3-coder:exacto`

**Provider Selection Criteria**:
1. Top-tier tool-calling accuracy
2. Normal range of tool-calling propensity
3. Not frequently ignored/blacklisted by users

Data sources: Real traffic telemetry, user preferences, benchmarks (tau2-Bench, LiveMCPBench, etc.)

### Extended Variant (`:extended`)

**Purpose**: Access extended context window versions of models.

```json
{ "model": "anthropic/claude-3.5-sonnet:extended" }
```

Allows processing longer inputs and maintaining more conversation history.

### Free Variant (`:free`)

**Purpose**: Access free versions of models.

```json
{ "model": "meta-llama/llama-3.2-3b-instruct:free" }
```

Free variants may have different rate limits or availability compared to paid versions.

### Nitro Variant (`:nitro`)

**Purpose**: High-speed inference for faster response times.

```json
{ "model": "openai/gpt-4o:nitro" }
```

Equivalent to setting `provider.sort: "throughput"`. Ideal for real-time applications requiring low latency.

### Online Variant (`:online`)

**Purpose**: Enable real-time web search capabilities.

```json
{ "model": "openai/gpt-4o:online" }
```

Equivalent to using the web plugin:
```json
{
  "model": "openrouter/auto",
  "plugins": { "web": {} }
}
```

Incorporates web search results for up-to-date information beyond training data.

### Thinking Variant (`:thinking`)

**Purpose**: Enable extended reasoning capabilities.

```json
{ "model": "deepseek/deepseek-r1:thinking" }
```

Provides chain-of-thought reasoning for complex problem-solving tasks requiring thorough analysis.

---

## Quick Reference: Model Variant Suffixes

| Variant | Suffix | Purpose |
|---------|--------|---------|
| Exacto | `:exacto` | Curated providers for tool-calling accuracy |
| Extended | `:extended` | Extended context windows |
| Free | `:free` | Free model access |
| Nitro | `:nitro` | High-speed/throughput prioritization |
| Floor | `:floor` | Lowest price prioritization |
| Online | `:online` | Real-time web search |
| Thinking | `:thinking` | Extended reasoning capabilities |

---

## API Endpoints

All routing features work with:
- **Chat Completions**: `https://openrouter.ai/api/v1/chat/completions`
- **Completions**: `https://openrouter.ai/api/v1/completions`

## Enterprise Features

- **EU Data Residency**: Prompts and completions processed entirely within the EU (enterprise customers)
