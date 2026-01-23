# Claude Agent SDK - Beginners Summary

This document summarizes the essential information from the Claude Agent SDK documentation for beginners.

---

## What is the Claude Agent SDK?

The Claude Agent SDK (formerly Claude Code SDK) is a library that lets you build production AI agents using the same tools, agent loop, and context management that power Claude Code. It is available for both **Python** and **TypeScript**.

With the Agent SDK, you can create AI agents that autonomously:
- Read and edit files
- Run terminal commands
- Search the web
- Analyze and refactor code
- And much more

**Key Difference from the Anthropic Client SDK:**
- **Client SDK**: You send prompts and implement tool execution yourself (manual tool loop)
- **Agent SDK**: Claude handles tool execution autonomously (built-in tool loop)

```python
# Agent SDK: Claude handles tools autonomously
async for message in query(prompt="Fix the bug in auth.py"):
    print(message)
```

---

## Key Concepts for Beginners

### 1. Built-in Tools

The SDK comes with ready-to-use tools:

| Tool | Purpose |
|------|---------|
| **Read** | Read any file in the working directory |
| **Write** | Create new files |
| **Edit** | Make precise edits to existing files |
| **Bash** | Run terminal commands, scripts, git operations |
| **Glob** | Find files by pattern (e.g., `**/*.ts`) |
| **Grep** | Search file contents with regex |
| **WebSearch** | Search the web for current information |
| **WebFetch** | Fetch and parse web page content |
| **AskUserQuestion** | Ask the user clarifying questions |

### 2. The `query` Function

`query` is the main entry point. It returns an async iterator that streams messages as Claude works:

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="Find all TODO comments in this codebase",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"])
):
    print(message)
```

### 3. Permission Modes

Control how much autonomy your agent has:

| Mode | Behavior | Use Case |
|------|----------|----------|
| `acceptEdits` | Auto-approves file edits, asks for other actions | Trusted development workflows |
| `bypassPermissions` | Runs without prompts | CI/CD pipelines, automation |
| `default` | Requires a `canUseTool` callback for approval | Custom approval flows |

### 4. Hooks

Run custom code at key points in the agent lifecycle:
- `PreToolUse` / `PostToolUse` - Before/after tool calls
- `SessionStart` / `SessionEnd` - Session lifecycle
- `Stop` - When agent completes
- `UserPromptSubmit` - When user submits a prompt

### 5. Subagents

Spawn specialized agents for focused subtasks. Define custom agents with specific instructions and tools:

```python
options=ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Task"],
    agents={
        "code-reviewer": AgentDefinition(
            description="Expert code reviewer",
            prompt="Analyze code quality and suggest improvements.",
            tools=["Read", "Glob", "Grep"]
        )
    }
)
```

### 6. MCP (Model Context Protocol)

Connect to external systems like databases, browsers, and APIs using MCP servers:

```python
options=ClaudeAgentOptions(
    mcp_servers={
        "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
    }
)
```

### 7. Sessions

Maintain context across multiple exchanges. Capture the session ID from the first query and resume later:

```python
# First query - capture session_id
async for message in query(prompt="Read the auth module", options=...):
    if hasattr(message, 'subtype') and message.subtype == 'init':
        session_id = message.session_id

# Resume with context
async for message in query(
    prompt="Now find all places that call it",
    options=ClaudeAgentOptions(resume=session_id)
):
    print(message)
```

---

## How to Get Started

### Prerequisites

- **Node.js 18+** (for TypeScript) or **Python 3.10+**
- An Anthropic account and API key

### Step 1: Install Claude Code Runtime

The SDK uses Claude Code as its runtime:

```bash
# macOS/Linux/WSL
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew
brew install --cask claude-code

# Windows (WinGet)
winget install Anthropic.ClaudeCode
```

After installation, run `claude` in your terminal to authenticate.

### Step 2: Install the SDK

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk
```

**Python (with uv):**
```bash
uv init && uv add claude-agent-sdk
```

**Python (with pip):**
```bash
python3 -m venv .venv && source .venv/bin/activate
pip3 install claude-agent-sdk
```

### Step 3: Set Your API Key

Create a `.env` file or export the environment variable:

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Get your key from the [Claude Console](https://platform.claude.com/).

**Alternative providers:** Amazon Bedrock, Google Vertex AI, and Microsoft Azure are also supported via environment variables.

### Step 4: Write Your First Agent

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage

async def main():
    async for message in query(
        prompt="Review utils.py for bugs and fix any issues you find.",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Glob"],
            permission_mode="acceptEdits"
        )
    ):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review utils.py for bugs and fix any issues you find.",
  options: {
    allowedTools: ["Read", "Edit", "Glob"],
    permissionMode: "acceptEdits"
  }
})) {
  if (message.type === "assistant" && message.message?.content) {
    for (const block of message.message.content) {
      if ("text" in block) console.log(block.text);
    }
  }
}
```

---

## Migration Notes (From Claude Code SDK)

If you are migrating from the old "Claude Code SDK", here are the key changes:

### Package Name Changes

| Aspect | Old | New |
|--------|-----|-----|
| TypeScript Package | `@anthropic-ai/claude-code` | `@anthropic-ai/claude-agent-sdk` |
| Python Package | `claude-code-sdk` | `claude-agent-sdk` |
| Python Import | `claude_code_sdk` | `claude_agent_sdk` |
| Python Options Class | `ClaudeCodeOptions` | `ClaudeAgentOptions` |

### Migration Steps

**TypeScript:**
```bash
npm uninstall @anthropic-ai/claude-code
npm install @anthropic-ai/claude-agent-sdk
```

Update imports:
```typescript
// Before
import { query } from "@anthropic-ai/claude-code";

// After
import { query } from "@anthropic-ai/claude-agent-sdk";
```

**Python:**
```bash
pip uninstall claude-code-sdk
pip install claude-agent-sdk
```

Update imports:
```python
# Before
from claude_code_sdk import query, ClaudeCodeOptions

# After
from claude_agent_sdk import query, ClaudeAgentOptions
```

### Breaking Changes in v0.1.0

1. **System Prompt No Longer Default**
   - The SDK now uses a minimal system prompt by default
   - To restore old behavior, explicitly use the Claude Code preset:
   ```python
   options=ClaudeAgentOptions(
       system_prompt={"type": "preset", "preset": "claude_code"}
   )
   ```

2. **Settings Sources No Longer Loaded by Default**
   - The SDK no longer reads from CLAUDE.md, settings.json, or slash commands automatically
   - To restore old behavior:
   ```python
   options=ClaudeAgentOptions(
       setting_sources=["user", "project", "local"]
   )
   ```

These changes were made to improve isolation and predictability for CI/CD, deployed applications, testing, and multi-tenant systems.

---

## Tool Combinations for Common Use Cases

| Tools | What the Agent Can Do |
|-------|----------------------|
| `Read`, `Glob`, `Grep` | Read-only analysis |
| `Read`, `Edit`, `Glob` | Analyze and modify code |
| `Read`, `Edit`, `Bash`, `Glob`, `Grep` | Full automation |
| Add `WebSearch` | Include web research capability |
| Add `Task` | Enable subagent delegation |

---

## Next Steps

After completing this summary, explore these topics:

- **Permissions**: Fine-grained control over agent capabilities
- **Hooks**: Run custom code at key lifecycle points
- **Sessions**: Build multi-turn agents with persistent context
- **MCP Servers**: Connect to databases, browsers, and APIs
- **Hosting**: Deploy agents to Docker, cloud, and CI/CD
- **Example Agents**: See complete examples at [claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos)

---

## Resources

- [TypeScript SDK Reference](/docs/en/agent-sdk/typescript)
- [Python SDK Reference](/docs/en/agent-sdk/python)
- [Report TypeScript Issues](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
- [Report Python Issues](https://github.com/anthropics/claude-agent-sdk-python/issues)
