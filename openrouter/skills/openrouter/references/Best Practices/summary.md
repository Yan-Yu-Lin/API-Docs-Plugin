# OpenRouter Best Practices Summary

This document provides a comprehensive summary of OpenRouter's best practices documentation, covering latency and performance optimization, prompt caching, uptime optimization, and reasoning tokens.

---

## Latency and Performance

OpenRouter is designed with performance as a top priority, adding minimal latency to requests.

### Base Latency

Under typical production conditions, OpenRouter adds approximately **15ms of latency** to requests. This is achieved through:

- **Edge computing** using Cloudflare Workers to stay close to your application
- **Efficient caching** of user and API key data at the edge
- **Optimized routing logic** that minimizes processing time

### Performance Considerations

#### Cache Warming
When OpenRouter's edge caches are cold (typically during the first 1-2 minutes of operation in a new region), slightly higher latency may occur. This normalizes once caches are populated.

#### Credit Balance Checks
Additional database checks are performed when:
- A user's credit balance is low (single digit dollars)
- An API key is approaching its configured credit limit

OpenRouter expires caches more aggressively under these conditions to ensure proper billing, which increases latency until additional credits are added.

#### Model Fallback
When using model routing or provider routing, if the primary model or provider fails, OpenRouter automatically tries the next option. OpenRouter tracks provider failures and attempts to intelligently route around unavailable providers.

### Best Practices for Optimal Performance

1. **Maintain Healthy Credit Balance**
   - Set up auto-topup with a higher threshold and amount
   - Recommended minimum balance: $10-20 for smooth operation

2. **Use Provider Preferences**
   - Leverage provider routing features for specific latency requirements (time to first token or time to last)

---

## Prompt Caching

Prompt caching helps reduce inference costs on supported providers and models. Most providers automatically enable prompt caching, though some (like Anthropic) require per-message enablement.

When using caching, OpenRouter makes a best-effort to continue routing to the same provider to utilize the warm cache. If the provider with the cached prompt is unavailable, OpenRouter tries the next-best provider.

### Inspecting Cache Usage

To see caching savings:
1. Click the detail button on the Activity page
2. Use the `/api/v1/generation` API
3. Use `usage: {include: true}` in requests to get cache tokens at the end of the response

The `cache_discount` field in the response body shows how much the response saved on cache usage.

### Provider-Specific Caching

#### OpenAI
- **Cache writes**: No cost
- **Cache reads**: Charged at 0.25x or 0.50x the original input pricing (model-dependent)
- Automated caching with no additional configuration
- Minimum prompt size: 1024 tokens

#### Grok
- **Cache writes**: No cost
- **Cache reads**: Charged at reduced rate
- Automated caching with no additional configuration

#### Moonshot AI
- **Cache writes**: No cost
- **Cache reads**: Charged at reduced rate
- Automated caching with no additional configuration

#### Groq
- **Cache writes**: No cost
- **Cache reads**: Charged at reduced rate
- Automated caching, currently available on Kimi K2 models

#### Anthropic Claude
- **Cache writes**: Charged at higher rate than original input pricing
- **Cache reads**: Charged at reduced rate
- Requires explicit `cache_control` breakpoints
- Limit of four breakpoints with 5-minute cache expiration
- Best reserved for large text bodies (character cards, CSV data, RAG data, book chapters)

**System Message Caching Example:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "You are a historian studying the fall of the Roman Empire."
        },
        {
          "type": "text",
          "text": "HUGE TEXT BODY",
          "cache_control": {
            "type": "ephemeral"
          }
        }
      ]
    },
    {
      "role": "user",
      "content": [{"type": "text", "text": "What triggered the collapse?"}]
    }
  ]
}
```

#### DeepSeek
- **Cache writes**: Same price as original input pricing
- **Cache reads**: Charged at reduced rate
- Automated caching with no additional configuration

#### Google Gemini

**Implicit Caching (Gemini 2.5 Pro and Flash):**
- No cache write or storage costs
- Cached tokens charged at reduced rate
- No manual setup required
- TTL averages 3-5 minutes
- Minimum token requirements apply per model

**Tip:** To maximize implicit cache hits, keep the initial portion of message arrays consistent between requests. Push variations toward the end of prompts.

**Explicit Caching:**
- Cache writes charged at input token cost plus 5 minutes of storage
- Cache reads charged at reduced rate
- Requires `cache_control` breakpoints (similar to Anthropic)
- 5-minute TTL that does not update
- Minimum 4096 tokens typically required

---

## Uptime Optimization

OpenRouter continuously monitors the health and availability of AI providers to ensure maximum uptime.

### How It Works

OpenRouter tracks in real-time:
- Response times
- Error rates
- Availability across all providers

This data enables intelligent routing decisions and provides transparency about service reliability.

### Customizing Provider Selection

While smart routing helps maintain high availability, you can customize provider selection using request parameters. This provides control over which providers handle requests while still benefiting from automatic fallback when needed.

---

## Reasoning Tokens

Reasoning tokens (also known as thinking tokens) provide transparency into the reasoning steps taken by a model. OpenRouter normalizes different customization methods across providers into a unified interface.

### Key Concepts

- Reasoning tokens are considered **output tokens** and charged accordingly
- Included in responses by default if the model outputs them
- Appear in the `reasoning` field of each message
- Some models (OpenAI o-series, Gemini Flash Thinking) do not return their reasoning tokens

### Controlling Reasoning Tokens

Use the `reasoning` parameter in requests:

```json
{
  "model": "your-model",
  "messages": [],
  "reasoning": {
    "effort": "high",       // "high", "medium", "low", "minimal", or "none" (OpenAI-style)
    "max_tokens": 2000,     // Specific token limit (Anthropic-style)
    "exclude": false,       // Exclude reasoning from response
    "enabled": true         // Enable with default parameters
  }
}
```

**Note:** Use either `effort` OR `max_tokens`, not both.

### Max Tokens for Reasoning

Supported by:
- Gemini thinking models
- Anthropic reasoning models
- Some Alibaba Qwen thinking models (mapped to `thinking_budget`)

### Reasoning Effort Levels

Supported by OpenAI reasoning models (o1, o3 series, GPT-5 series) and Grok models:

| Effort | Token Allocation |
|--------|------------------|
| high | ~80% of max_tokens |
| medium | ~50% of max_tokens |
| low | ~20% of max_tokens |
| minimal | ~10% of max_tokens |
| none | Disabled |

### Excluding Reasoning from Response

Set `"exclude": true` to have the model use reasoning internally without including it in the response.

### Legacy Parameters

For backward compatibility:
- `include_reasoning: true` equivalent to `reasoning: {}`
- `include_reasoning: false` equivalent to `reasoning: { exclude: true }`

### Code Examples

**Basic Usage (TypeScript SDK):**
```typescript
import { OpenRouter } from '@openrouter/sdk';

const openRouter = new OpenRouter({ apiKey: 'YOUR_API_KEY' });

const response = await openRouter.chat.send({
  model: 'openai/o3-mini',
  messages: [{ role: 'user', content: "How would you build a skyscraper?" }],
  reasoning: { effort: 'high' },
  stream: false,
});

console.log('REASONING:', response.choices[0].message.reasoning);
console.log('CONTENT:', response.choices[0].message.content);
```

**Using Python with OpenAI SDK:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_API_KEY",
)

response = client.chat.completions.create(
    model="anthropic/claude-3.7-sonnet",
    messages=[{"role": "user", "content": "Your question here"}],
    extra_body={"reasoning": {"max_tokens": 2000}},
)

msg = response.choices[0].message
print(getattr(msg, "reasoning", None))
```

### Anthropic-Specific Implementation

For Anthropic models with reasoning:
- Use `reasoning.max_tokens` (minimum 1024 tokens) or `reasoning.effort`
- Budget tokens calculated as: `budget_tokens = max(min(max_tokens * effort_ratio, 32000), 1024)`
- `max_tokens` must be strictly higher than the reasoning budget
- The `:thinking` variant is no longer supported

### Preserving Reasoning Blocks

Important for tool calling workflows to maintain reasoning continuity across API calls.

Supported models:
- All OpenAI reasoning models (o1, o3, GPT-5 series)
- All Anthropic reasoning models (Claude 3.7, Claude 4, Claude 4.1)
- All Gemini Reasoning models
- All xAI reasoning models
- MiniMax M2, Kimi K2 Thinking, INTELLECT-3

**Key principle:** Pass `reasoning_details` back unmodified to preserve the model's reasoning flow.

### Responses API Shape

The `reasoning_details` array contains reasoning detail objects with three possible types:

1. **Summary Type (`reasoning.summary`)** - High-level reasoning summary
2. **Encrypted Type (`reasoning.encrypted`)** - Encrypted/protected reasoning data
3. **Text Type (`reasoning.text`)** - Raw text reasoning with optional signature

**Common fields:**
- `id`: Unique identifier
- `format`: Format specification (e.g., "anthropic-claude-v1", "openai-responses-v1")
- `index`: Sequential index

**Response locations:**
- Non-streaming: `choices[].message.reasoning_details`
- Streaming: `choices[].delta.reasoning_details`

---

## Summary of Key Recommendations

1. **For Performance:**
   - Maintain a credit balance of $10-20 or higher
   - Use provider routing features for specific latency requirements

2. **For Cost Optimization:**
   - Leverage prompt caching, especially for large static content
   - Use appropriate `cache_control` breakpoints for Anthropic and Gemini models
   - Keep static content at the beginning of prompts for better cache hits

3. **For Reliability:**
   - Rely on OpenRouter's intelligent routing for automatic failover
   - Use provider preferences when specific providers are required

4. **For Enhanced Responses:**
   - Use reasoning tokens for complex problems requiring step-by-step analysis
   - Choose appropriate effort levels based on task complexity
   - Preserve reasoning blocks in multi-turn conversations with tool calling
