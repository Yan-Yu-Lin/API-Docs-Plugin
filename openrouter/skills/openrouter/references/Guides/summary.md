# OpenRouter Guides Summary

This document provides a comprehensive summary of all OpenRouter guides, covering key concepts, API usage patterns, and best practices.

---

## Table of Contents

1. [Crypto API](#crypto-api)
2. [Using MCP Servers with OpenRouter](#using-mcp-servers-with-openrouter)
3. [Organization Management](#organization-management)
4. [Provider Integration](#provider-integration)
5. [Usage Accounting](#usage-accounting)
6. [User Tracking](#user-tracking)
7. [Distillation](#distillation)

---

## Crypto API

### Overview

OpenRouter supports purchasing credits using cryptocurrency through Coinbase integration. This can be done via the UI on the credits page or programmatically through the API.

### Three-Step Process for Headless Credit Purchases

1. **Get the calldata** for a new credit purchase
2. **Send a transaction on-chain** using that data
3. **Detect low account balance** and purchase more credits as needed

### Supported Chains (Mainnet Only)

- Ethereum
- Polygon
- Base (recommended)

### Getting Credit Purchase Calldata

Make a POST request to `/api/v1/credits/coinbase`:

```typescript
const response = await fetch('https://openrouter.ai/api/v1/credits/coinbase', {
  method: 'POST',
  headers: {
    Authorization: 'Bearer <OPENROUTER_API_KEY>',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    amount: 10, // Target credit amount in USD
    sender: '0x...', // Your wallet address
    chain_id: 8453, // Chain ID (8453 for Base)
  }),
});
```

The response includes charge details and transaction data with `web3_data.transfer_intent` containing the contract address and call data.

### Sending the Transaction

Use [viem](https://viem.sh) or similar EVM client to execute the transaction. The recommended method is `swapAndTransferUniswapV3Native()` from Coinbase's onchain payment protocol. A pool fees tier of 500 is typically sufficient for ETH transactions.

### Credit Processing Times

- Purchases under $500: Immediately credited
- Purchases over $500: ~15 minute confirmation delay to prevent chain reorganization issues

### Detecting Low Balance

Poll the `GET /api/v1/credits` endpoint to check available credits:

```typescript
const credits = await openRouter.credits.get();
console.log('Available credits:', credits.totalCredits - credits.totalUsage);
```

Note: Values are cached and may be up to 60 seconds stale.

---

## Using MCP Servers with OpenRouter

### Overview

MCP (Model Context Protocol) servers provide LLMs with tool calling abilities as an alternative to OpenAI-compatible tool calling. By converting MCP tool definitions to OpenAI-compatible format, you can use MCP servers with OpenRouter.

### Key Concepts

- MCP protocol is **stateful** and requires session management
- More complex than calling a REST endpoint
- Uses Anthropic's MCP client SDK

### Tool Format Conversion

Convert MCP tool definitions to OpenAI format:

```python
def convert_tool_format(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"],
                "required": tool.inputSchema["required"]
            }
        }
    }
```

### MCP Client Setup

The MCP client connects to OpenRouter using the base URL:

```python
self.openai = OpenAI(
    base_url="https://openrouter.ai/api/v1"
)
```

### Workflow

1. Connect to MCP server using `StdioServerParameters`
2. Initialize session and list available tools
3. Convert tools to OpenAI format
4. Process queries by calling OpenRouter with converted tools
5. Execute tool calls through the MCP session
6. Return results to the model for final response

---

## Organization Management

### Overview

Organizations enable teams to collaborate by sharing credits, managing API keys centrally, and tracking usage across team members.

### Creating an Organization

1. Navigate to Settings > Preferences
2. Click "Create Organization"
3. Configure organization details
4. Invite team members (max 10 members)

Requirements: Verified email address

### Credit Management

**Shared Credit Pool Benefits:**
- Centralized billing
- Simplified accounting
- Budget control across the team

**Admin-Only Credit Functions:**
- Purchase credits
- View billing information
- Manage payment methods

**Credit Transfers:** Personal to organization transfers require contacting support@openrouter.ai

### API Key Management

**Member Permissions:**
- Create API keys
- View and manage own keys
- Use any organization key

**Administrator Permissions:**
- View all organization keys
- Manage all keys (edit, disable, delete)
- Access usage analytics

### Activity Tracking

- Organization-wide activity feed shows all member usage
- Metadata visible: model used, cost, timing
- Filter by specific API key
- OpenRouter does not store prompts or responses

### Administrative Controls

Admin-only settings include:
- Provider settings and routing preferences
- Privacy settings and data retention policies
- Member management and role assignment
- Billing configuration

### Use Cases

- **Development Teams:** Shared resources, centralized management
- **Companies:** Budget control, compliance, scalability
- **Research Organizations:** Resource sharing, usage monitoring, reporting

---

## Provider Integration

### Overview

Model providers can sell inference on OpenRouter by meeting specific requirements and filling out the provider form.

### Requirements

#### 1. List Models Endpoint

Must return all models in this format:

```json
{
  "data": [
    {
      "id": "anthropic/claude-sonnet-4",
      "hugging_face_id": "",
      "name": "Anthropic: Claude Sonnet 4",
      "created": 1690502400,
      "input_modalities": ["text", "image", "file"],
      "output_modalities": ["text", "image", "file"],
      "quantization": "fp8",
      "context_length": 1000000,
      "max_output_length": 128000,
      "pricing": {
        "prompt": "0.000008",
        "completion": "0.000024",
        "image": "0",
        "request": "0",
        "input_cache_reads": "0",
        "input_cache_writes": "0"
      },
      "supported_sampling_parameters": ["temperature", "stop"],
      "supported_features": ["tools", "json_mode", "structured_outputs", "web_search", "reasoning"]
    }
  ]
}
```

**Valid Values:**
- Quantization: `int4`, `int8`, `fp4`, `fp6`, `fp8`, `fp16`, `bf16`, `fp32`
- Sampling parameters: `temperature`, `top_p`, `top_k`, `repetition_penalty`, `frequency_penalty`, `presence_penalty`, `stop`, `seed`
- Features: `tools`, `json_mode`, `structured_outputs`, `web_search`, `reasoning`

Note: Pricing fields must be strings in USD to avoid floating point precision issues.

#### 2. Auto Top Up or Invoicing

Automatic payment method required for inference billing.

#### 3. Uptime Monitoring & Traffic Routing

**Uptime Calculation:** successful requests / total requests (excluding user errors)

**Errors Affecting Uptime:**
- Authentication issues (401)
- Payment failures (402)
- Model not found (404)
- Server errors (500+)
- Mid-stream errors

**Errors NOT Affecting Uptime:**
- Bad requests (400) - user input
- Oversized payloads (413) - user input
- Rate limiting (429) - tracked separately
- Geographic restrictions (403) - tracked separately

**Traffic Routing Thresholds:**
- Minimum data: 100+ requests before calculation
- Normal routing: 95%+ uptime
- Degraded status: 80-94% uptime (lower priority)
- Down status: <80% uptime (fallback only)

---

## Usage Accounting

### Overview

Track AI model usage without additional API calls. Get detailed information about token counts, costs, and caching status directly in responses.

### Usage Information Provided

- Prompt and completion token counts (native tokenizer)
- Cost in credits
- Reasoning token counts (if applicable)
- Cached token counts (if available)

### Enabling Usage Accounting

```json
{
  "model": "your-model",
  "messages": [],
  "usage": {
    "include": true
  }
}
```

### Response Format

```json
{
  "usage": {
    "completion_tokens": 2,
    "completion_tokens_details": {
      "reasoning_tokens": 0
    },
    "cost": 0.95,
    "cost_details": {
      "upstream_inference_cost": 19
    },
    "prompt_tokens": 194,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "total_tokens": 196
  }
}
```

### Cost Breakdown

- `cost`: Total amount charged to your account
- `upstream_inference_cost`: Actual provider cost (BYOK requests only)

### Performance Note

Enabling usage accounting adds a few hundred milliseconds to the final response for token calculation. This only affects the final message, not streaming performance.

### Alternative: Generation ID Method

Retrieve usage asynchronously via generation ID:
1. Make chat completion request
2. Note the `id` field in response
3. Fetch usage via `/generation` endpoint

### Code Examples

**TypeScript SDK:**
```typescript
const response = await openRouter.chat.send({
  model: 'anthropic/claude-3-opus',
  messages: [{ role: 'user', content: 'What is the capital of France?' }],
  usage: { include: true },
  stream: false,
});
console.log('Usage Stats:', response.usage);
```

**Python (OpenAI SDK):**
```python
response = client.chat.completions.create(
    model="anthropic/claude-3-opus",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    extra_body={"usage": {"include": True}}
)
```

---

## User Tracking

### Overview

Track your own user IDs to improve caching performance and get detailed reporting on sub-users.

### Benefits

**Improved Caching:**
- Sticky routing to same provider for each user
- Cache stays warm for individual users
- Load balancing across providers for different users

**Enhanced Reporting:**
- Activity feed broken down by user ID
- Usage analytics per user
- Detailed exports with user-level data

### Implementation

```json
{
  "model": "openai/gpt-4o",
  "messages": [{"role": "user", "content": "Hello"}],
  "user": "user_12345"
}
```

### Code Examples

**TypeScript SDK:**
```typescript
const response = await openRouter.chat.send({
  model: 'openai/gpt-4o',
  messages: [{ role: 'user', content: "What's the weather like today?" }],
  user: 'user_12345',
  stream: false,
});
```

**Python:**
```python
response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "What's the weather like today?"}],
    user="user_12345",
)
```

### Best Practices

**Choose Stable Identifiers:**
- Good: `user_12345`, `customer_abc123`, `account_xyz789`
- Avoid: Random strings that change between requests

**Privacy Considerations:**
- Use internal user IDs, not personal information
- Avoid PII in identifiers
- Consider anonymized identifiers

**Consistency:**
```python
user_id = f"app_{internal_user_id}"
```

---

## Distillation

### Overview

Model distillation is training smaller models using outputs from larger models. Some providers prohibit this, while others allow it. OpenRouter tracks which models permit distillation through the `is_trainable_text` property.

### Why Compliance Matters

Using outputs from models that prohibit distillation could:
- Violate terms of service
- Expose you to legal liability

OpenRouter provides distillation information on a best-effort basis. Always verify specific license terms.

### Finding Distillable Models

**Via UI:** Use the "Distillable" filter on the Models page: `https://openrouter.ai/models?distillable=true`

**Via API:** Use the `enforce_distillable_text` routing parameter:

```json
{
  "model": "meta-llama/llama-3.1-70b-instruct",
  "messages": [{"role": "user", "content": "Explain quantum computing"}],
  "provider": {
    "enforce_distillable_text": true
  }
}
```

### Code Examples

**TypeScript SDK:**
```typescript
const completion = await openRouter.chat.send({
  model: 'meta-llama/llama-3.1-70b-instruct',
  messages: [{ role: 'user', content: 'Explain quantum computing' }],
  provider: { enforceDistillableText: true },
  stream: false,
});
```

**Python:**
```python
response = requests.post('https://openrouter.ai/api/v1/chat/completions',
  headers=headers,
  json={
    'model': 'meta-llama/llama-3.1-70b-instruct',
    'messages': [{'role': 'user', 'content': 'Explain quantum computing'}],
    'provider': {'enforce_distillable_text': True},
  }
)
```

### Use Cases

- Building training datasets
- Creating distillation pipelines
- Compliance workflows for organizations with strict requirements

---

## Quick Reference

| Feature | Endpoint/Parameter | Purpose |
|---------|-------------------|---------|
| Crypto Purchase | `POST /api/v1/credits/coinbase` | Buy credits with cryptocurrency |
| Check Credits | `GET /api/v1/credits` | Monitor account balance |
| Usage Tracking | `usage: { include: true }` | Get token counts and costs |
| User Tracking | `user: "user_id"` | Improve caching and reporting |
| Distillation Filter | `enforce_distillable_text: true` | Only use distillation-allowed models |
| MCP Integration | Convert tools + OpenRouter base URL | Use MCP servers with OpenRouter |

---

## Support Contacts

- General questions: Check the FAQ
- Technical support: support@openrouter.ai
- Credit transfers: support@openrouter.ai
- Provider integration: Fill out the provider form at openrouter.ai/how-to-list
