# Research: Using Claude Agent SDK with Local LLMs

## Executive Summary

**Can the Claude Agent SDK be configured to use local LLMs by swapping the base URL?**

**Answer: No.** The Claude Agent SDK is architecturally tied to Claude models and the Anthropic API. While `ANTHROPIC_BASE_URL` exists, it is designed for proxy routing (credential injection, security) rather than swapping to a different model provider.

---

## Research Questions Answered

### Q1: Can you set ANTHROPIC_BASE_URL in the SDK options or only via env var?

**Answer: Environment variable only.**

The SDK documentation shows **no programmatic option** for base URL configuration. Searching through the TypeScript and Python SDK references reveals:

**TypeScript Options** (from `/Users/linyanyu/claude-agent-sdk/docs/typescript.md`, lines 91-133):
- 40+ configuration properties listed
- Includes `model`, `fallbackModel`, `env`, etc.
- **No `baseUrl`, `endpoint`, or `apiUrl` property**

**Python ClaudeAgentOptions** (from `/Users/linyanyu/claude-agent-sdk/docs/python.md`, lines 449-527):
- Similar comprehensive options
- Includes `model`, `fallback_model`, `env`
- **No `base_url` or endpoint configuration**

The only documented method is via environment variable:

```bash
export ANTHROPIC_BASE_URL="http://localhost:8080"
```

---

### Q2: Any SDK-specific configuration for custom endpoints?

**Answer: No SDK-specific options. Only environment variables for proxy routing.**

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/secure-deployment.md` (lines 228-244)

```markdown
**Option 1: ANTHROPIC_BASE_URL (simple but only for sampling API requests)**

export ANTHROPIC_BASE_URL="http://localhost:8080"

This tells Claude Code and the Agent SDK to send sampling requests to your proxy
instead of the Anthropic API directly. Your proxy receives plaintext HTTP requests,
can inspect and modify them (including injecting credentials), then forwards to the real API.

**Option 2: HTTP_PROXY / HTTPS_PROXY (system-wide)**

export HTTP_PROXY="http://localhost:8080"
export HTTPS_PROXY="http://localhost:8080"

Claude Code and the Agent SDK respect these standard environment variables,
routing all HTTP traffic through the proxy.
```

**Key insight:** Documentation explicitly says requests are "forwarded to the real API" - this is for proxy routing, not model replacement.

---

### Q3: Does the SDK have hardcoded Anthropic dependencies?

**Answer: Yes, extensively.**

#### 1. API Format Dependencies

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/typescript.md` (lines 419-445)

```typescript
type SDKAssistantMessage = {
  type: 'assistant';
  uuid: UUID;
  session_id: string;
  message: APIAssistantMessage; // From Anthropic SDK
  parent_tool_use_id: string | null;
}

type SDKPartialAssistantMessage = {
  type: 'stream_event';
  event: RawMessageStreamEvent; // From Anthropic SDK
  parent_tool_use_id: string | null;
  uuid: UUID;
  session_id: string;
}
```

The SDK imports and depends on types from `@anthropic-ai/sdk`.

#### 2. Network Requirements

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/hosting.md` (lines 33-35)

```markdown
- **Network access**
  - Outbound HTTPS to `api.anthropic.com`
  - Optional: Access to MCP servers or external tools
```

#### 3. Model-Specific Features

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/typescript.md` (lines 1896-1904)

```typescript
type SdkBeta = 'context-1m-2025-08-07';

// Beta features are Claude-specific:
// | `'context-1m-2025-08-07'` | Enables 1 million token context window | Claude Sonnet 4, Claude Sonnet 4.5 |
```

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/python.md` (lines 994-1001)

```python
@dataclass
class ThinkingBlock:
    thinking: str
    signature: str
```

ThinkingBlock support is specific to Claude models with thinking capability.

#### 4. Officially Supported Providers (All Host Claude)

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/overview.md` (lines 424-428)

```markdown
The SDK also supports authentication via third-party API providers:

- **Amazon Bedrock**: set `CLAUDE_CODE_USE_BEDROCK=1` environment variable
- **Google Vertex AI**: set `CLAUDE_CODE_USE_VERTEX=1` environment variable
- **Microsoft Foundry**: set `CLAUDE_CODE_USE_FOUNDRY=1` environment variable
```

All three are Claude-hosting cloud providers, not generic LLM providers.

---

### Q4: What's the proxy pattern mentioned in secure-deployment?

**Answer: Security-focused request routing with credential injection.**

**Source:** `/Users/linyanyu/claude-agent-sdk/docs/secure-deployment.md` (lines 213-226)

```markdown
### The proxy pattern

The recommended approach is to run a proxy outside the agent's security boundary
that injects credentials into outgoing requests. The agent sends requests without
credentials, the proxy adds them, and forwards the request to its destination.

This pattern has several benefits:

1. The agent never sees the actual credentials
2. The proxy can enforce an allowlist of permitted endpoints
3. The proxy can log all requests for auditing
4. Credentials are stored in one secure location rather than distributed to each agent
```

**Documented proxy tools** (line 249-252):
- **Envoy Proxy** - production-grade with `credential_injector` filter
- **mitmproxy** - TLS-terminating for inspecting/modifying HTTPS
- **Squid** - caching proxy with access control lists
- **LiteLLM** - LLM gateway with credential injection and rate limiting

**Architecture diagram** (from lines 143-147):

```markdown
**Unix socket architecture:**

With `--network none`, the container has no network interfaces at all.
The only way for the agent to reach the outside world is through the mounted
Unix socket, which connects to a proxy running on the host. This proxy can
enforce domain allowlists, inject credentials, and log all traffic.
```

---

## Why Local LLMs Won't Work

### API Format Incompatibility

| Feature | Anthropic Messages API | OpenAI Chat API (most local LLMs) |
|---------|------------------------|-----------------------------------|
| Endpoint | `/v1/messages` | `/v1/chat/completions` |
| Content | `content: [{type: "text", text: "..."}]` | `content: "..."` |
| Tool calls | `tool_use` block type | `function_call` / `tool_calls` |
| Streaming | `message_start`, `content_block_delta`, etc. | `delta` chunks |
| Model names | `claude-3-opus-20240229` | `gpt-4`, `llama3` |

### Architectural Barriers

1. **SDK Runtime**: Uses Claude Code CLI which expects Claude models
2. **Built-in Tools**: Read, Write, Edit, Bash, Glob, Grep - all designed for Claude's tool use format
3. **System Prompts**: Pre-configured for Claude capabilities (`preset: 'claude_code'`)
4. **Response Parsing**: Expects Anthropic-specific message structures

---

## Theoretical Workaround: LiteLLM as Translation Layer

LiteLLM is mentioned in the docs as a proxy option. It could theoretically translate between API formats:

**Setup (not officially supported):**
```bash
export ANTHROPIC_BASE_URL="http://localhost:4000/anthropic"
# Run LiteLLM with Anthropic-to-local translation
```

**Problems:**
1. **Tool calling translation** - Non-trivial, especially for complex tool chains
2. **Streaming format** - Different event structures may cause parsing errors
3. **No official support** - Could break with any SDK update
4. **Capability gaps** - Local LLMs may not follow complex instructions reliably

---

## Conclusion

The Claude Agent SDK **cannot be used with local LLMs** through base URL swapping because:

| Aspect | Finding |
|--------|---------|
| Base URL Config | Environment variable only (`ANTHROPIC_BASE_URL`), designed for proxying to Anthropic API |
| SDK Options | No programmatic endpoint configuration |
| Dependencies | Hardcoded Anthropic API types, message formats, streaming events |
| Proxy Pattern | For security/credential injection, not model replacement |

### Alternatives for Local LLM Agents

- **OpenAI Agents SDK** - For OpenAI-compatible local LLMs
- **LangChain/LangGraph** - Framework-agnostic
- **AutoGen** - Multi-agent with local LLM support
- **Composio** - Multi-provider tool framework
- **Semantic Kernel** - Microsoft's multi-provider SDK

---

## Source File References

| File Path | Key Content |
|-----------|-------------|
| `/Users/linyanyu/claude-agent-sdk/docs/overview.md` | API key setup, Bedrock/Vertex/Foundry support (lines 418-432) |
| `/Users/linyanyu/claude-agent-sdk/docs/typescript.md` | Options type (lines 91-133), message types (lines 419-445), SdkBeta (lines 1896-1904) |
| `/Users/linyanyu/claude-agent-sdk/docs/python.md` | ClaudeAgentOptions (lines 449-527), ThinkingBlock (lines 994-1001) |
| `/Users/linyanyu/claude-agent-sdk/docs/hosting.md` | Network requirements - api.anthropic.com (lines 33-35) |
| `/Users/linyanyu/claude-agent-sdk/docs/secure-deployment.md` | ANTHROPIC_BASE_URL (lines 228-234), proxy pattern (lines 213-252) |

---

*Research conducted: 2026-01-22*
