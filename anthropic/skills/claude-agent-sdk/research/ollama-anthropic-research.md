# Ollama Anthropic API Compatibility Research

**Research Date:** January 22, 2026

## Summary

**Yes, Ollama now natively supports the Anthropic Messages API format.** This was introduced in **Ollama v0.14.0**, released on January 16, 2026.

---

## Key Findings

### 1. Does Ollama support Anthropic Messages API format?

**Yes.** Ollama v0.14.0+ provides native compatibility with the Anthropic Messages API, allowing tools designed for the Anthropic API (like Claude Code) to work directly with Ollama models without any translation layer or shim.

**Source:** https://docs.ollama.com/api/anthropic-compatibility

### 2. Since When? What Version?

- **Version:** Ollama v0.14.0
- **Release Date:** January 16, 2026
- **Announcement:** https://ollama.com/blog/claude

From the release notes:
> "Anthropic API compatibility: support for the `/v1/messages` API"

**Source:** https://github.com/ollama/ollama/releases/tag/v0.14.0

### 3. What Endpoint?

The Anthropic-compatible endpoint is:

```
POST http://localhost:11434/v1/messages
```

This mirrors Anthropic's `/v1/messages` endpoint format.

### 4. Does It Support Tool Use in Anthropic Format?

**Yes.** Tool calling (function calling) is supported in the Anthropic format.

**Supported Features:**
- Messages and multi-turn conversations
- Streaming
- System prompts (string or array)
- Tool calling / function calling
- Tool results
- Extended thinking / thinking blocks
- Vision (image input via base64)

**Example tool calling code:**
```python
import anthropic

client = anthropic.Anthropic(
    base_url='http://localhost:11434',
    api_key='ollama',  # required but ignored
)

message = client.messages.create(
    model='qwen3-coder',
    max_tokens=1024,
    tools=[
        {
            'name': 'get_weather',
            'description': 'Get the current weather in a location',
            'input_schema': {
                'type': 'object',
                'properties': {
                    'location': {
                        'type': 'string',
                        'description': 'The city and state, e.g. San Francisco, CA'
                    }
                },
                'required': ['location']
            }
        }
    ],
    messages=[{'role': 'user', 'content': "What's the weather in San Francisco?"}]
)

for block in message.content:
    if block.type == 'tool_use':
        print(f'Tool: {block.name}')
        print(f'Input: {block.input}')
```

**Source:** https://docs.ollama.com/api/anthropic-compatibility

### 5. Limitations Compared to Real Anthropic API

#### Not Supported

| Feature | Description |
|---------|-------------|
| `/v1/messages/count_tokens` | Token counting endpoint |
| `tool_choice` | Forcing specific tool use or disabling tools |
| `metadata` | Request metadata (user_id) |
| Prompt caching | `cache_control` blocks for caching prefixes |
| Batches API | `/v1/messages/batches` for async batch processing |
| Citations | `citations` content blocks |
| PDF support | `document` content blocks with PDF files |
| Server-sent errors | `error` events during streaming (errors return HTTP status) |

#### Partial Support

| Feature | Status |
|---------|--------|
| Image content | Base64 images supported; URL images **not** supported |
| Extended thinking | Basic support; `budget_tokens` accepted but not enforced |

#### Behavioral Differences

- API key is accepted but **not validated** (use any value like `ollama`)
- `anthropic-version` header is accepted but not used
- Token counts are **approximations** based on the underlying model's tokenizer

**Known Issue (as of Jan 2026):** Some users report that stable Ollama has issues with streaming tool calls that can break Claude Code's agentic loop. Using pre-release versions (0.14.3-rc1 or later) is recommended until fixes land in stable.

**Source:** https://paddo.dev/blog/claude-code-local-ollama/

### 6. How to Configure/Enable It

#### Environment Variables

```bash
export ANTHROPIC_AUTH_TOKEN=ollama    # required but ignored
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_API_KEY=ollama       # required but ignored
```

#### Using with Claude Code

```bash
# Set environment variables and run
ANTHROPIC_AUTH_TOKEN=ollama \
ANTHROPIC_BASE_URL=http://localhost:11434 \
ANTHROPIC_API_KEY=ollama \
claude --model qwen3-coder
```

Or add to shell profile for persistent configuration:
```bash
echo 'export ANTHROPIC_AUTH_TOKEN=ollama' >> ~/.bashrc
echo 'export ANTHROPIC_BASE_URL=http://localhost:11434' >> ~/.bashrc
echo 'export ANTHROPIC_API_KEY=ollama' >> ~/.bashrc
source ~/.bashrc
```

Then run:
```bash
# Local models
claude --model qwen3-coder
claude --model gpt-oss:20b

# Cloud models (via ollama.com)
claude --model glm-4.7:cloud
claude --model minimax-m2.1:cloud
```

#### Model Name Aliasing

For tools that expect specific Anthropic model names (like `claude-3-5-sonnet`), use `ollama cp` to create an alias:

```bash
ollama cp qwen3-coder claude-3-5-sonnet
```

#### Using with Anthropic SDK (Python)

```python
import anthropic

client = anthropic.Anthropic(
    base_url='http://localhost:11434',
    api_key='ollama',  # required but ignored
)

message = client.messages.create(
    model='qwen3-coder',
    max_tokens=1024,
    messages=[
        {'role': 'user', 'content': 'Hello, how are you?'}
    ]
)
print(message.content[0].text)
```

#### Using with Anthropic SDK (JavaScript/TypeScript)

```javascript
import Anthropic from '@anthropic-ai/sdk'

const anthropic = new Anthropic({
  baseURL: 'http://localhost:11434',
  apiKey: 'ollama',
})

const message = await anthropic.messages.create({
  model: 'qwen3-coder',
  messages: [{ role: 'user', content: 'Write a function to check if a number is prime' }],
})

console.log(message.content[0].text)
```

---

## Recommended Models for Coding

### Local Models
- `qwen3-coder` - Excellent for coding tasks
- `gpt-oss:20b` - Strong general-purpose model
- `glm-4.7-flash` - 30B MoE, 3B active parameters, good tool calling support

### Cloud Models (via ollama.com)
- `glm-4.7:cloud` - High-performance cloud model
- `minimax-m2.1:cloud` - Fast cloud model

**Note:** It is recommended to use models with at least 32K token context length for Claude Code.

---

## Supported Request/Response Fields

### Request Fields
- `model`
- `max_tokens`
- `messages` (with text, image base64, array of content blocks, tool_use blocks, tool_result blocks, thinking blocks)
- `system` (string or array)
- `stream`
- `temperature`
- `top_p`
- `top_k`
- `stop_sequences`
- `tools`
- `thinking`

### Response Fields
- `id`
- `type`
- `role`
- `model`
- `content` (text, tool_use, thinking blocks)
- `stop_reason` (end_turn, max_tokens, tool_use)
- `usage` (input_tokens, output_tokens)

### Streaming Events
- `message_start`
- `content_block_start`
- `content_block_delta` (text_delta, input_json_delta, thinking_delta)
- `content_block_stop`
- `message_delta`
- `message_stop`
- `ping`
- `error`

---

## Sources

1. **Official Ollama Documentation - Anthropic Compatibility**
   https://docs.ollama.com/api/anthropic-compatibility

2. **Ollama Blog - Claude Code with Anthropic API compatibility**
   https://ollama.com/blog/claude

3. **Ollama v0.14.0 Release Notes**
   https://github.com/ollama/ollama/releases/tag/v0.14.0

4. **Running Claude Code Fully Local with Ollama (paddo.dev)**
   https://paddo.dev/blog/claude-code-local-ollama/

5. **GitHub Issue - Add Ollama integration guide to Claude Code docs**
   https://github.com/anthropics/claude-code/issues/19564

6. **Reddit Discussion - Claude Code with Anthropic API compatibility**
   https://www.reddit.com/r/ClaudeAI/comments/1qga3u3/claude_code_with_anthropic_api_compatibility/

7. **AI Engineer Guide - How to use any Ollama AI model with Claude Code**
   https://aiengineerguide.com/blog/ollama-claude-code/
