# OpenRouter Anthropic API Format Support Research

**Research Date:** January 2026
**Purpose:** Determine if OpenRouter supports Anthropic's Messages API format natively

---

## Executive Summary

**Yes, OpenRouter natively supports the Anthropic Messages API format.** As of late 2025, OpenRouter introduced an "Anthropic Skin" that exposes a `/v1/messages` endpoint compatible with the Anthropic Messages API. This allows tools like Claude Code and the Claude Agent SDK to work directly with OpenRouter without any proxy servers.

---

## Key Findings

### 1. Does OpenRouter support Anthropic Messages API format (`/v1/messages`)?

**YES.** OpenRouter provides a native Anthropic Messages API compatible endpoint.

> "OpenRouter exposes an input that is compatible with the Anthropic Messages API."
>
> "OpenRouter's 'Anthropic Skin' behaves exactly like the Anthropic API. It handles model mapping and passes through advanced features like 'Thinking' blocks and native tool use."

**Source:** [OpenRouter Claude Code Integration Docs](https://openrouter.ai/docs/guides/guides/claude-code-integration)

The endpoint is documented at:
- [Create a message (Anthropic Messages format)](https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-messages)

### 2. OpenRouter supports BOTH API formats

| Format | Endpoint | Use Case |
|--------|----------|----------|
| **OpenAI-compatible** | `/api/v1/chat/completions` | OpenAI SDK, most third-party tools |
| **Anthropic-compatible** | `/api/v1/messages` | Claude Code, Claude Agent SDK, Anthropic SDK |

**Source:** [OpenRouter API Reference](https://openrouter.ai/docs/api/reference/overview)

### 3. Base URL for Anthropic format

```
https://openrouter.ai/api
```

When using the Anthropic SDK or Claude Code, set:
- `ANTHROPIC_BASE_URL="https://openrouter.ai/api"`

The SDK will automatically append `/v1/messages` to make requests to `https://openrouter.ai/api/v1/messages`.

**Important:** Do NOT use `https://openrouter.ai/api/v1` as the base URL for Anthropic format - that's for OpenAI format. Use just `https://openrouter.ai/api`.

**Source:** [OpenRouter Claude Code Integration](https://openrouter.ai/docs/guides/guides/claude-code-integration)

### 4. Can you access non-Claude models via Anthropic format?

**YES.** You can use the Anthropic API format to access any model on OpenRouter (400+ models including GPT, Llama, Mistral, Gemini, etc.).

Configuration via environment variables:

```bash
# Use OpenRouter's Anthropic-compatible endpoint
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""  # MUST be explicitly empty

# Override default models to non-Claude models
export ANTHROPIC_DEFAULT_SONNET_MODEL="openai/gpt-5.2-codex-max"
export ANTHROPIC_DEFAULT_OPUS_MODEL="openai/gpt-5.2-pro"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="minimax/minimax-m2:exacto"
```

**Important Note:** When using non-Claude models, ensure they support tool calling/function calling, as Claude Code relies heavily on this capability.

**Source:** [OpenRouter Claude Code Integration - Changing Models](https://openrouter.ai/docs/guides/guides/claude-code-integration)

### 5. Authentication

OpenRouter uses Bearer token authentication for both API formats:

```
Authorization: Bearer <OPENROUTER_API_KEY>
```

For Claude Code / Claude Agent SDK, set:
```bash
export ANTHROPIC_AUTH_TOKEN="<your-openrouter-api-key>"
export ANTHROPIC_API_KEY=""  # Must be explicitly empty to prevent fallback
```

**Optional headers:**
- `HTTP-Referer`: Your app URL (for OpenRouter leaderboards)
- `X-Title`: Your app name (for OpenRouter leaderboards)

**Source:** [OpenRouter Authentication Docs](https://openrouter.ai/docs/api/reference/authentication)

### 6. Limitations vs Real Anthropic API

| Feature | OpenRouter Anthropic Skin | Native Anthropic API |
|---------|---------------------------|---------------------|
| Messages API format | Full support | Full support |
| Tool/Function calling | Supported (native) | Supported (native) |
| Thinking/Reasoning blocks | Supported (pass-through) | Supported |
| Streaming (SSE) | Supported | Supported |
| Images/PDFs in messages | Supported | Supported |
| Prompt caching | Supported | Supported |
| Model-specific features | Varies by model | Full Claude features |
| Billing | OpenRouter credits | Anthropic billing |
| Rate limits | OpenRouter limits | Anthropic limits |
| Privacy/Logging | OpenRouter policy (opt-in) | Anthropic policy |

**Key differences:**
1. **Billing**: Uses OpenRouter credits, not Anthropic billing
2. **Model availability**: Access to 400+ models beyond Claude
3. **Pricing**: May differ from direct Anthropic pricing
4. **Rate limits**: Subject to OpenRouter's rate limits

**Source:** [OpenRouter Claude Code Integration - How It Works](https://openrouter.ai/docs/guides/guides/claude-code-integration)

### 7. Claude Agent SDK Compatibility

**YES, it works with Claude Agent SDK.**

OpenRouter explicitly documents support for the Anthropic Agent SDK:

> "The Anthropic Agent SDK lets you build AI agents programmatically using Python or TypeScript. Since the Agent SDK uses Claude Code as its runtime, you can connect it to OpenRouter using the same environment variables."

**Configuration:**
```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""  # Important: Must be explicitly empty
```

**TypeScript Example:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// Environment variables should be set before running:
// ANTHROPIC_BASE_URL=https://openrouter.ai/api
// ANTHROPIC_AUTH_TOKEN=your_openrouter_api_key
// ANTHROPIC_API_KEY=""

async function main() {
  for await (const message of query({
    prompt: "Find and fix the bug in auth.py",
    options: {
      allowedTools: ["Read", "Edit", "Bash"],
    },
  })) {
    if (message.type === "assistant") {
      console.log(message.message.content);
    }
  }
}

main();
```

**Python Example:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

# Environment variables should be set before running

async def main():
    async for message in query(
        prompt="Find and fix the bug in auth.py",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Bash"]
        )
    ):
        print(message)

asyncio.run(main())
```

**Source:** [OpenRouter Anthropic Agent SDK Integration](https://openrouter.ai/docs/guides/community/anthropic-agent-sdk)

---

## Using Anthropic SDK Directly with OpenRouter

You can use the official Anthropic Python/JS SDK directly with OpenRouter by changing the base URL:

**Python:**
```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-openrouter-api-key",
    base_url="https://openrouter.ai/api",
)

response = client.messages.create(
    model="anthropic/claude-sonnet-4",  # Use OpenRouter model ID format
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
```

**JavaScript/TypeScript:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: 'your-openrouter-api-key',
  baseURL: 'https://openrouter.ai/api',
});

const response = await client.messages.create({
  model: 'anthropic/claude-sonnet-4',
  max_tokens: 1000,
  messages: [
    { role: 'user', content: 'Hello!' }
  ]
});

console.log(response.content[0].text);
```

**Note:** When using the Anthropic SDK directly (not Claude Code), you may need to use the full OpenRouter model ID format (e.g., `anthropic/claude-sonnet-4` instead of just `claude-sonnet-4`).

---

## Claude Code Quick Setup

```bash
# Add to ~/.bashrc or ~/.zshrc

export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="your-openrouter-api-key"
export ANTHROPIC_API_KEY=""  # MUST be empty

# Optional: Override default models
# export ANTHROPIC_DEFAULT_SONNET_MODEL="openai/gpt-5.2"
```

Then start Claude Code:
```bash
cd /path/to/your/project
claude
```

Verify connection with `/status` command inside Claude Code.

**Source:** [OpenRouter Claude Code Integration](https://openrouter.ai/docs/guides/guides/claude-code-integration)

---

## GitHub Action Support

OpenRouter works with the official Claude Code GitHub Action:

```yaml
- name: Run Claude Code
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.OPENROUTER_API_KEY }}
  env:
    ANTHROPIC_BASE_URL: https://openrouter.ai/api
```

**Source:** [OpenRouter Claude Code Integration - GitHub Action](https://openrouter.ai/docs/guides/guides/claude-code-integration)

---

## Alternative: Using Proxy Servers

Before OpenRouter added native Anthropic format support, users needed proxy servers. These are now largely unnecessary but still exist:

- [y-router](https://github.com/luohy15/y-router) - Simple proxy for Claude Code + OpenRouter
- [anthropic-proxy](https://github.com/maxnowack/anthropic-proxy) - Converts Anthropic to OpenAI format
- [AnthroRouter](https://github.com/CuriosityOS/AnthroRouter) - Anthropic to OpenRouter translation

**Recommendation:** Use the native OpenRouter Anthropic endpoint (`https://openrouter.ai/api`) instead of proxies for better reliability and fewer moving parts.

---

## Sources

1. **OpenRouter Claude Code Integration Guide**
   https://openrouter.ai/docs/guides/guides/claude-code-integration

2. **OpenRouter Anthropic Messages API Reference**
   https://openrouter.ai/docs/api/api-reference/anthropic-messages/create-messages

3. **OpenRouter Anthropic Agent SDK Integration**
   https://openrouter.ai/docs/guides/community/anthropic-agent-sdk

4. **OpenRouter API Reference Overview**
   https://openrouter.ai/docs/api/reference/overview

5. **OpenRouter Authentication Docs**
   https://openrouter.ai/docs/api/reference/authentication

6. **OpenRouter Quickstart Guide**
   https://openrouter.ai/docs/quickstart

7. **AI Engineer Guide - OpenRouter Models in Claude Code**
   https://aiengineerguide.com/blog/openrouter-models-in-claude-code/

8. **Startup Hub - Use OpenRouter in Claude Code**
   https://www.startuphub.ai/ai-news/artificial-intelligence/2025/use-openrouter-in-claude-code-model-freedom-arrives/

---

## Summary Table

| Question | Answer |
|----------|--------|
| Does OpenRouter support `/v1/messages` (Anthropic format)? | **Yes** |
| Does OpenRouter support `/v1/chat/completions` (OpenAI format)? | **Yes** |
| Base URL for Anthropic format? | `https://openrouter.ai/api` |
| Can access non-Claude models via Anthropic format? | **Yes** (400+ models) |
| Authentication method? | Bearer token (OpenRouter API key) |
| Works with Claude Agent SDK? | **Yes** |
| Works with Anthropic Python/JS SDK? | **Yes** (set base_url) |
| Proxy server required? | **No** (native support) |
| Major limitations? | Uses OpenRouter billing/rate limits |
