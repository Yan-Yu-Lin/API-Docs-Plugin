---
name: claude-agent-sdk
description: Comprehensive documentation and guidance for Claude Agent SDK - building AI agents with TypeScript/Python, tool use, hooks, sessions, MCP integration, deployment, and alternative backend support (Ollama, OpenRouter)
---

# Claude Agent SDK Documentation Skill

This skill provides comprehensive guidance for building AI agents using the Claude Agent SDK (formerly Claude Code SDK). Use this skill when working with autonomous agents, tool use, multi-agent systems, MCP integrations, or deploying Claude-powered applications.

## What is the Claude Agent SDK?

The Claude Agent SDK is a library for building production AI agents using the same tools, agent loop, and context management that power Claude Code. Unlike the Anthropic Client SDK where you manually implement tool execution, the Agent SDK handles tool execution autonomously.

**Key Value Proposition:**
- Claude handles tool execution autonomously (built-in agent loop)
- Ready-to-use tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
- Built-in permission system, hooks, sessions, and subagent support
- Available for both **TypeScript** and **Python**

```python
# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

---

## Quick Topic Navigation

| Topic | Read This File | When to Use |
|-------|----------------|-------------|
| **Getting started** | `summary/beginners-summary.md` | New to the SDK, first agent, basic concepts |
| **TypeScript SDK** | `summary/language-specific-summary.md` | TypeScript API, query(), V2 preview, options |
| **Python SDK** | `summary/language-specific-summary.md` | Python API, query(), ClaudeSDKClient, options |
| **Custom tools & subagents** | `summary/agent-builders-summary.md` | Building complex agents, MCP tools, multi-agent |
| **Hooks & permissions** | `summary/agent-builders-summary.md` | Security, validation, approval flows |
| **Plugins & skills** | `summary/plugin-skill-devs-summary.md` | Creating plugins, Agent Skills, slash commands |
| **Hosting & deployment** | `summary/devops-platform-summary.md` | Docker, security, cost tracking, sessions |
| **Ollama integration** | `research/ollama-anthropic-research.md` | Local LLMs with Anthropic API format |
| **OpenRouter integration** | `research/openrouter-anthropic-research.md` | Using OpenRouter as backend |
| **Local LLM feasibility** | `research/local-llm-research.md` | Why direct local LLM support is limited |
| **Licensing & policies** | `research/sdk-licensing-policy-research.md` | Commercial use, restrictions, alternative backends |

---

## Key Concepts Overview

### Built-in Tools

| Tool | Purpose |
|------|---------|
| `Read` | Read files in the working directory |
| `Write` | Create new files |
| `Edit` | Make precise edits to existing files |
| `Bash` | Run terminal commands, scripts, git |
| `Glob` | Find files by pattern (`**/*.ts`) |
| `Grep` | Search file contents with regex |
| `WebSearch` | Search the web |
| `WebFetch` | Fetch and parse web pages |
| `AskUserQuestion` | Ask user for clarification |
| `Task` | Delegate to subagents |
| `Skill` | Invoke Agent Skills |

### Permission Modes

| Mode | Behavior |
|------|----------|
| `default` | Requires `canUseTool` callback for approval |
| `acceptEdits` | Auto-approves file edits, asks for others |
| `bypassPermissions` | All tools run without prompts (CI/CD) |
| `plan` | No tool execution; planning only |

### Hooks

Intercept agent execution at key points:
- `PreToolUse` / `PostToolUse` - Before/after tool calls
- `SessionStart` / `SessionEnd` - Session lifecycle
- `UserPromptSubmit` - User prompt submission
- `Stop` - Agent completion
- `SubagentStart` / `SubagentStop` - Subagent lifecycle

### Sessions

Maintain context across multiple exchanges:
1. Capture `session_id` from first query's init message
2. Pass `resume: session_id` in subsequent queries
3. Use `forkSession: true` to branch without modifying original

### Subagents

Spawn specialized agents for focused subtasks:
- Context isolation prevents information overload
- Can run in parallel for faster workflows
- Each can have specialized instructions and tool restrictions
- Require `Task` tool in parent's `allowed_tools`

### MCP (Model Context Protocol)

Connect to external tools via MCP servers:
- Databases, browsers, APIs (GitHub, Slack, etc.)
- Tools follow naming: `mcp__<server>__<tool>`
- Configure via `mcpServers` option or `.mcp.json` file

---

## SDK Comparison: TypeScript vs Python

| Feature | TypeScript | Python |
|---------|------------|--------|
| **Package** | `@anthropic-ai/claude-agent-sdk` | `claude-agent-sdk` |
| **Primary Interface** | `query()` async generator | `query()` + `ClaudeSDKClient` |
| **Multi-turn** | Via AsyncIterable or V2 `createSession()` | Via `ClaudeSDKClient` |
| **Hooks** | Full support (12 events) | Partial support (6 events) |
| **MCP Tools** | `tool()` + Zod schemas | `@tool` decorator |
| **V2 Preview** | `unstable_v2_createSession()` | Not available |
| **License** | Proprietary (Commercial ToS) | MIT (usage governed by ToS) |

### Option Name Differences

| TypeScript | Python |
|------------|--------|
| `permissionMode` | `permission_mode` |
| `allowedTools` | `allowed_tools` |
| `mcpServers` | `mcp_servers` |
| `systemPrompt` | `system_prompt` |
| `maxTurns` | `max_turns` |
| `canUseTool` | `can_use_tool` |
| `settingSources` | `setting_sources` |

---

## Alternative Backends

### OpenRouter (Recommended for Non-Claude Models)

OpenRouter natively supports the Anthropic Messages API format. No proxy needed.

**Configuration:**
```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""  # MUST be empty
```

**Features:**
- Access 400+ models (GPT, Llama, Mistral, Gemini, etc.)
- Full tool calling support
- Works with Claude Agent SDK directly
- See `research/openrouter-anthropic-research.md` for details

### Ollama (Local LLMs)

Ollama v0.14.0+ supports Anthropic Messages API format natively.

**Configuration:**
```bash
export ANTHROPIC_BASE_URL="http://localhost:11434"
export ANTHROPIC_AUTH_TOKEN="ollama"
export ANTHROPIC_API_KEY="ollama"
```

**Limitations vs Real Anthropic API:**
- No token counting endpoint
- No `tool_choice` parameter
- No prompt caching
- Token counts are approximations
- See `research/ollama-anthropic-research.md` for details

### Why Direct Local LLM Support is Limited

The SDK is architecturally tied to Claude:
- API format dependencies (Anthropic message types)
- Claude-specific features (thinking blocks, betas)
- Built-in tools designed for Claude's tool use format
- See `research/local-llm-research.md` for full analysis

---

## Licensing Considerations

**TypeScript SDK:** Proprietary - Commercial Terms of Service only
**Python SDK:** MIT License (but usage governed by Commercial ToS)

**Key Restriction (Section D.4):**
> "Customer may not access the Services to build a competing product or service"

**Risk Assessment:**
| Scenario | Risk Level |
|----------|------------|
| SDK + Claude via Anthropic API | None (intended use) |
| SDK + Claude via Bedrock/Vertex | None (officially supported) |
| SDK + Claude via OpenRouter | Low |
| SDK + non-Claude via OpenRouter | Medium (may violate ToS) |
| Commercial product with SDK + Claude | None (explicitly permitted) |

See `research/sdk-licensing-policy-research.md` for full analysis.

---

## Common Patterns

### Basic Query

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Fix the bug in auth.py",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash"],
        permission_mode="acceptEdits"
    )
):
    print(message)
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Fix the bug in auth.py",
  options: {
    allowedTools: ["Read", "Edit", "Bash"],
    permissionMode: "acceptEdits"
  }
})) {
  console.log(message);
}
```

### Multi-turn Conversation (Python)

```python
async with ClaudeSDKClient() as client:
    await client.query("My name is Alice")
    async for msg in client.receive_response():
        pass  # acknowledge

    await client.query("What is my name?")
    async for msg in client.receive_response():
        # Claude responds "Alice"
```

### Multi-turn Conversation (TypeScript V2)

```typescript
await using session = unstable_v2_createSession({ model: "claude-sonnet-4-5-20250929" });

await session.send("My name is Alice");
for await (const msg of session.stream()) { /* acknowledge */ }

await session.send("What is my name?");
for await (const msg of session.stream()) {
  // Claude responds "Alice"
}
```

### Subagent Definition

```python
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Task"],  # Task required
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code review specialist",
            prompt="You are a code reviewer...",
            tools=["Read", "Grep", "Glob"],
            model="sonnet"
        )
    }
)
```

### Custom MCP Tool

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_weather", "Get current temperature", {"location": str})
async def get_weather(args):
    return {"content": [{"type": "text", "text": f"72F in {args['location']}"}]}

server = create_sdk_mcp_server(name="weather", tools=[get_weather])

options = ClaudeAgentOptions(
    mcp_servers={"weather": server},
    allowed_tools=["mcp__weather__get_weather"]
)
```

---

## Tool Combinations for Common Use Cases

| Tools | What the Agent Can Do |
|-------|----------------------|
| `Read`, `Glob`, `Grep` | Read-only analysis |
| `Read`, `Edit`, `Glob` | Analyze and modify code |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Full development automation |
| Add `WebSearch`, `WebFetch` | Include web research |
| Add `Task` | Enable subagent delegation |
| Add `Skill` | Invoke Agent Skills |

---

## Deployment Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **Ephemeral** | New container per task | One-off tasks, bug investigation |
| **Long-Running** | Persistent container | Proactive agents, chat bots |
| **Hybrid** | Ephemeral + state hydration | Intermittent interactions |
| **Single Container** | Multiple SDK processes | Agent collaboration |

**System Requirements:**
- Python 3.10+ or Node.js 18+
- Claude Code CLI installed
- 1 GiB RAM, 5 GiB disk recommended
- Network access to `api.anthropic.com`

---

## Official Documentation Links

| Topic | URL |
|-------|-----|
| Overview | https://platform.claude.com/docs/en/agent-sdk/overview |
| Quickstart | https://platform.claude.com/docs/en/agent-sdk/quickstart |
| TypeScript SDK | https://platform.claude.com/docs/en/agent-sdk/typescript |
| Python SDK | https://platform.claude.com/docs/en/agent-sdk/python |
| Hooks | https://platform.claude.com/docs/en/agent-sdk/hooks |
| Sessions | https://platform.claude.com/docs/en/agent-sdk/sessions |
| Permissions | https://platform.claude.com/docs/en/agent-sdk/permissions |
| Subagents | https://platform.claude.com/docs/en/agent-sdk/subagents |
| Custom Tools | https://platform.claude.com/docs/en/agent-sdk/custom-tools |
| MCP | https://platform.claude.com/docs/en/agent-sdk/mcp |
| Hosting | https://platform.claude.com/docs/en/agent-sdk/hosting |
| Secure Deployment | https://platform.claude.com/docs/en/agent-sdk/secure-deployment |
| Cost Tracking | https://platform.claude.com/docs/en/agent-sdk/cost-tracking |

Full link list: See `agent-sdk-docs-links.md`

---

## File Reference

All documentation files are located in this skill's directory:

```
skills/claude-agent-sdk/
├── SKILL.md                              # This file (navigation guide)
├── agent-sdk-docs-links.md               # Official documentation URLs
├── summary/
│   ├── beginners-summary.md              # Getting started, key concepts
│   ├── language-specific-summary.md      # TypeScript/Python API details
│   ├── agent-builders-summary.md         # Tools, subagents, hooks, permissions
│   ├── plugin-skill-devs-summary.md      # Plugins, Skills, slash commands, MCP
│   └── devops-platform-summary.md        # Hosting, security, costs, sessions
└── research/
    ├── local-llm-research.md             # Why local LLM direct support is limited
    ├── ollama-anthropic-research.md      # Ollama Anthropic API compatibility
    ├── openrouter-anthropic-research.md  # OpenRouter as alternative backend
    └── sdk-licensing-policy-research.md  # Licensing, restrictions, commercial use
```

---

## When to Reference Each File

**User asks about...**

| Question Category | Read |
|-------------------|------|
| "How do I get started?" / "What is Agent SDK?" | `summary/beginners-summary.md` |
| TypeScript API, `query()`, options, V2 preview | `summary/language-specific-summary.md` |
| Python API, `ClaudeSDKClient`, options | `summary/language-specific-summary.md` |
| Creating custom tools, MCP servers | `summary/agent-builders-summary.md` |
| Subagents, multi-agent patterns | `summary/agent-builders-summary.md` |
| Hooks, PreToolUse, PostToolUse | `summary/agent-builders-summary.md` |
| Permissions, canUseTool, security | `summary/agent-builders-summary.md` |
| Plugins, Agent Skills, slash commands | `summary/plugin-skill-devs-summary.md` |
| MCP integration, external tools | `summary/plugin-skill-devs-summary.md` |
| Docker, hosting, deployment | `summary/devops-platform-summary.md` |
| Cost tracking, usage monitoring | `summary/devops-platform-summary.md` |
| Session management, resuming conversations | `summary/devops-platform-summary.md` |
| Using Ollama with the SDK | `research/ollama-anthropic-research.md` |
| Using OpenRouter with the SDK | `research/openrouter-anthropic-research.md` |
| "Can I use local LLMs?" / "Why not local?" | `research/local-llm-research.md` |
| Licensing, commercial use, restrictions | `research/sdk-licensing-policy-research.md` |
| Migration from Claude Code SDK | `summary/beginners-summary.md` (Migration Notes section) |
