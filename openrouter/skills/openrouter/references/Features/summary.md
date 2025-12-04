# OpenRouter Features Summary

This document provides a comprehensive summary of OpenRouter's key features, covering configuration management, model capabilities, data handling, observability, and more.

---

## Presets

Presets allow you to separate LLM configuration from your code by creating named configurations that encapsulate all settings needed for specific use cases.

### What Presets Can Manage
- Provider routing preferences (sort by price, latency, etc.)
- Model selection (specific model or array of models with fallbacks)
- System prompts
- Generation parameters (temperature, top_p, etc.)
- Provider inclusion/exclusion rules

### Usage Methods

**1. Direct Model Reference:**
```json
{
  "model": "@preset/email-copywriter",
  "messages": [...]
}
```

**2. Preset Field:**
```json
{
  "model": "openai/gpt-4",
  "preset": "email-copywriter",
  "messages": [...]
}
```

**3. Combined Model and Preset:**
```json
{
  "model": "openai/gpt-4@preset/email-copywriter",
  "messages": [...]
}
```

### Key Benefits
- Separation of concerns between code and configuration
- Rapid iteration without code deployment
- Organization-wide sharing of best practices
- Version history with rollback capability

---

## Tool & Function Calling

Tool calls give LLMs access to external tools. The LLM suggests which tool to call, the user executes it locally, and provides results back to the LLM.

### Three-Step Process

**Step 1: Inference Request with Tools**
```json
{
  "model": "google/gemini-2.0-flash-001",
  "messages": [...],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "search_gutenberg_books",
        "description": "Search for books in the Project Gutenberg library",
        "parameters": {
          "type": "object",
          "properties": {
            "search_terms": {
              "type": "array",
              "items": {"type": "string"}
            }
          },
          "required": ["search_terms"]
        }
      }
    }
  ]
}
```

**Step 2: Execute Tool Locally**
```javascript
const toolResult = await searchGutenbergBooks(["James", "Joyce"]);
```

**Step 3: Send Tool Results Back**
Include the assistant's tool_calls message and a tool role message with the results.

### Tool Choice Configuration
```json
// Let model decide (default)
{ "tool_choice": "auto" }

// Disable tool usage
{ "tool_choice": "none" }

// Force specific tool
{
  "tool_choice": {
    "type": "function",
    "function": {"name": "search_database"}
  }
}
```

### Parallel Tool Calls
Control whether multiple tools can be called simultaneously:
```json
{ "parallel_tool_calls": false }
```

### Interleaved Thinking
Allows models to reason between tool calls for more sophisticated decision-making. Note: This increases token usage and response latency.

### Agentic Loop Pattern
```python
while iteration_count < max_iterations:
    resp = call_llm(messages)
    if resp.choices[0].message.tool_calls is not None:
        messages.append(get_tool_response(resp))
    else:
        break
```

### Best Practices
- Use clear and descriptive function names
- Provide comprehensive descriptions for tools
- Design tools that work well together for multi-tool workflows

---

## Web Search

Add real-time web data to any model's response using the web search plugin.

### Quick Enable
Append `:online` to the model slug:
```json
{
  "model": "openai/gpt-4o:online"
}
```

Or use the plugins array:
```json
{
  "model": "openrouter/auto",
  "plugins": [{ "id": "web" }]
}
```

### Engine Options
- **native**: Uses provider's built-in web search (OpenAI, Anthropic, Perplexity, xAI)
- **exa**: Uses Exa's search API
- **undefined**: Native if available, otherwise Exa fallback

### Customization
```json
{
  "model": "openai/gpt-4o:online",
  "plugins": [
    {
      "id": "web",
      "engine": "exa",
      "max_results": 3,
      "search_prompt": "Custom prompt for results"
    }
  ]
}
```

### Search Context Size
For native search, control context size with:
```json
{
  "web_search_options": {
    "search_context_size": "high"  // "low", "medium", or "high"
  }
}
```

### Response Format
Results are standardized with annotations:
```json
{
  "message": {
    "content": "Here's the latest news...",
    "annotations": [
      {
        "type": "url_citation",
        "url_citation": {
          "url": "https://example.com/result",
          "title": "Title",
          "content": "Content",
          "start_index": 100,
          "end_index": 200
        }
      }
    ]
  }
}
```

### Pricing
- **Exa search**: $4 per 1000 results (default 5 results = $0.02/request)
- **Native search**: Provider-specific pricing

---

## Structured Outputs

Enforce JSON Schema validation on model responses for consistent, type-safe outputs.

### Usage
```json
{
  "messages": [...],
  "response_format": {
    "type": "json_schema",
    "json_schema": {
      "name": "weather",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "City or location name"
          },
          "temperature": {
            "type": "number",
            "description": "Temperature in Celsius"
          }
        },
        "required": ["location", "temperature"],
        "additionalProperties": false
      }
    }
  }
}
```

### Supported Models
- OpenAI models (GPT-4o and later)
- Google Gemini models
- Anthropic models (Sonnet 4.5 and Opus 4.1)
- Most open-source models
- All Fireworks provided models

### Best Practices
- Include clear descriptions for schema properties
- Always set `strict: true` for exact schema compliance
- Streaming is supported with structured outputs

---

## Message Transforms

Transform prompts that exceed model context size using middle-out compression.

### Usage
```json
{
  "transforms": ["middle-out"],
  "messages": [...],
  "model": "any-model"
}
```

### How It Works
- Removes or truncates messages from the middle of the prompt
- Addresses both token context length and message count limits
- For Anthropic Claude models, handles the maximum message count limit
- Models with 8k context or less default to using middle-out

### Model Selection with Compression
OpenRouter tries to find models with context length at least half of your total required tokens. Falls back to highest available context length if needed.

### Rationale
LLMs pay less attention to the middle of sequences, making middle-out compression an effective strategy when perfect recall is not required.

---

## Model Routing

Dynamically route requests between AI models for optimal performance and reliability.

### Auto Router
Uses `openrouter/auto` to automatically select high-quality models based on your prompt (powered by NotDiamond):
```json
{
  "model": "openrouter/auto",
  "messages": [...]
}
```

### Model Fallbacks
The `models` parameter enables automatic fallback when primary model fails:
```json
{
  "models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"],
  "messages": [...]
}
```

Fallbacks trigger on:
- Provider downtime
- Rate limiting
- Content moderation flags
- Context length validation errors

### Using with OpenAI SDK
```python
completion = openai_client.chat.completions.create(
    model="openai/gpt-4o",
    extra_body={
        "models": ["anthropic/claude-3.5-sonnet", "gryphe/mythomax-l2-13b"],
    },
    messages=[...]
)
```

The response includes `model` attribute indicating which model was actually used.

---

## Zero Completion Insurance

OpenRouter protects users from being charged for failed or empty responses.

### Protection Criteria
No credits are deducted when:
- Response has zero completion tokens AND blank/null finish reason
- Response has an error finish reason

### Key Points
- Automatically enabled for all accounts
- Requires no configuration
- Applies across all models and providers
- Protected requests show zero credits on activity page
- Protection applies even if OpenRouter was charged by the provider

---

## Zero Data Retention (ZDR)

Control over data storage and training policies across providers.

### Enabling ZDR
- Global setting available at `/settings/privacy`
- Per-request enforcement via `zdr` parameter:
```json
{
  "model": "gpt-4",
  "messages": [...],
  "provider": {
    "zdr": true
  }
}
```

### Policy Hierarchy
- Per-request `zdr` parameter operates as "OR" with account-wide setting
- Can only ensure ZDR is enabled, not override account-wide enforcement

### Data Policy Details
- OpenRouter tracks specific policies for each endpoint
- Conservative stance: unknown policies assume data retention and training
- In-memory caching is NOT considered "retaining" data
- Providers without retention also cannot train on your data

### OpenRouter's Own Policy
- ZDR by default
- Prompts not retained unless you opt in to prompt logging

### ZDR Endpoints List
Available programmatically at: `https://openrouter.ai/api/v1/endpoints/zdr`

---

## App Attribution

Associate API usage with your application for visibility in rankings and analytics.

### Attribution Headers
- **HTTP-Referer**: Your app's URL (primary identifier)
- **X-Title**: Your app's display name

### Implementation
```typescript
const openRouter = new OpenRouter({
  apiKey: '<OPENROUTER_API_KEY>',
  defaultHeaders: {
    'HTTP-Referer': 'https://myapp.com',
    'X-Title': 'My AI Assistant',
  },
});
```

### Benefits
- **Public App Rankings**: Appear in OpenRouter's public leaderboards (daily, weekly, monthly)
- **Model Apps Tabs**: Featured on individual model pages
- **Detailed Analytics**: Access at `openrouter.ai/apps?url=<your-app-url>`

### Best Practices
- Use your app's primary domain
- Keep titles concise and descriptive
- For localhost development, always include a title header
- Only public apps (those sending headers) appear in rankings

---

## Broadcast

Automatically send traces from OpenRouter requests to external observability platforms.

### Enabling Broadcast
1. Navigate to Settings > Broadcast
2. Toggle "Enable Broadcast"
3. Add destination(s)

### Supported Destinations
- Braintrust
- Datadog
- Langfuse
- S3
- Weave
- OTel Collector

### Coming Soon
Arize, AWS Firehose, Clickhouse, Dynatrace, Evidently, Fiddler, Galileo, Grafana, Helicone, HoneyHive, Keywords AI, Langsmith, and many more.

### Trace Data Includes
- Request & response data (multimodal stripped)
- Token usage (prompt, completion, total)
- Cost information
- Timing and latency metrics
- Model and provider information
- Tool usage details

### User Tracking
```json
{
  "model": "openai/gpt-4o",
  "messages": [...],
  "user": "user_12345"
}
```

### Session Tracking
```json
{
  "model": "openai/gpt-4o",
  "messages": [...],
  "session_id": "session_abc123"
}
```
Alternative: Use `x-session-id` HTTP header.

### Configuration Options
- **API Key Filtering**: Route traces from specific keys to specific platforms
- **Sampling Rate**: Control percentage of traces sent (1.0 = all, 0.5 = 50%)
- **Organization Support**: Shared destinations across all organization API keys

### Security
- Credentials encrypted before storage
- Traces sent asynchronously (no added API latency)

---

## Quick Reference

| Feature | Primary Use Case | Key Parameter |
|---------|-----------------|---------------|
| Presets | Configuration management | `model: "@preset/name"` |
| Tool Calling | External tool integration | `tools: [...]` |
| Web Search | Real-time web data | `model: ".../:online"` |
| Structured Outputs | Type-safe JSON responses | `response_format: {...}` |
| Message Transforms | Context window management | `transforms: ["middle-out"]` |
| Model Routing | Fallbacks and auto-selection | `models: [...]` |
| Zero Completion Insurance | Cost protection | Automatic |
| Zero Data Retention | Privacy control | `provider: { zdr: true }` |
| App Attribution | Analytics and rankings | `HTTP-Referer`, `X-Title` headers |
| Broadcast | Observability integration | Dashboard configuration |
