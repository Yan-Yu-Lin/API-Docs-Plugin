# Claude Agent SDK - Language-Specific Reference Summary

This document summarizes the TypeScript and Python Agent SDKs for Claude Code, including the TypeScript V2 preview interface.

---

## Table of Contents

1. [TypeScript SDK Overview](#typescript-sdk-overview)
2. [TypeScript V2 Preview](#typescript-v2-preview)
3. [Python SDK Overview](#python-sdk-overview)
4. [SDK Comparison](#sdk-comparison)
5. [Common Patterns and Examples](#common-patterns-and-examples)

---

## TypeScript SDK Overview

### Installation

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Core API

#### `query()` - Primary Function

The main function for interacting with Claude Code. Creates an async generator that streams messages.

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const result = query({
  prompt: 'Hello, Claude!',
  options: {
    model: 'claude-sonnet-4-5-20250929',
    permissionMode: 'acceptEdits'
  }
});

for await (const msg of result) {
  if (msg.type === 'result') {
    console.log(msg.result);
  }
}
```

**Parameters:**
- `prompt`: `string | AsyncIterable<SDKUserMessage>` - Input prompt or async iterable for streaming
- `options`: `Options` - Configuration object

**Returns:** `Query` object extending `AsyncGenerator<SDKMessage, void>`

#### Query Object Methods

| Method | Description |
|--------|-------------|
| `interrupt()` | Interrupts the query (streaming input mode only) |
| `rewindFiles(userMessageUuid)` | Restores files to state at specified message |
| `setPermissionMode(mode)` | Changes permission mode |
| `setModel(model)` | Changes the model |
| `setMaxThinkingTokens(tokens)` | Changes max thinking tokens |
| `supportedCommands()` | Returns available slash commands |
| `supportedModels()` | Returns available models |
| `mcpServerStatus()` | Returns MCP server status |
| `accountInfo()` | Returns account information |

### Key Options

| Option | Type | Description |
|--------|------|-------------|
| `model` | `string` | Claude model to use |
| `permissionMode` | `PermissionMode` | `'default'`, `'acceptEdits'`, `'bypassPermissions'`, `'plan'` |
| `allowedTools` | `string[]` | List of allowed tool names |
| `disallowedTools` | `string[]` | List of disallowed tool names |
| `mcpServers` | `Record<string, McpServerConfig>` | MCP server configurations |
| `systemPrompt` | `string \| SystemPromptPreset` | System prompt configuration |
| `tools` | `string[] \| ToolsPreset` | Tool configuration |
| `maxTurns` | `number` | Maximum conversation turns |
| `maxBudgetUsd` | `number` | Maximum budget in USD |
| `cwd` | `string` | Current working directory |
| `hooks` | `Record<HookEvent, HookCallbackMatcher[]>` | Hook callbacks |
| `agents` | `Record<string, AgentDefinition>` | Subagent definitions |
| `settingSources` | `SettingSource[]` | Which settings to load (`'user'`, `'project'`, `'local'`) |
| `sandbox` | `SandboxSettings` | Sandbox behavior configuration |
| `canUseTool` | `CanUseTool` | Custom permission function |

### MCP Tool Creation

```typescript
import { tool, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

const greetTool = tool(
  'greet',
  'Greet a user by name',
  { name: z.string() },
  async (args) => ({
    content: [{ type: 'text', text: `Hello, ${args.name}!` }]
  })
);

const server = createSdkMcpServer({
  name: 'my-server',
  version: '1.0.0',
  tools: [greetTool]
});
```

### Message Types

- `SDKAssistantMessage` - Assistant responses
- `SDKUserMessage` - User input
- `SDKResultMessage` - Final result with cost/usage
- `SDKSystemMessage` - System initialization
- `SDKPartialAssistantMessage` - Streaming partial messages
- `SDKCompactBoundaryMessage` - Compaction boundary markers

### Hook Events

| Event | Description |
|-------|-------------|
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After tool execution |
| `PostToolUseFailure` | After tool execution failure |
| `Notification` | Notification events |
| `UserPromptSubmit` | When user submits prompt |
| `SessionStart` | Session starts |
| `SessionEnd` | Session ends |
| `Stop` | Stop requested |
| `SubagentStart` | Subagent starts |
| `SubagentStop` | Subagent stops |
| `PreCompact` | Before message compaction |
| `PermissionRequest` | Permission requested |

---

## TypeScript V2 Preview

> **Warning:** The V2 interface is an unstable preview. APIs may change before becoming stable.

### Key Differences from V1

The V2 interface simplifies multi-turn conversations by replacing async generators with explicit `send()`/`stream()` patterns:

- **V1:** Single async generator for both input and output
- **V2:** Separate `send()` for input and `stream()` for output

### Installation

Same package as V1:

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Core Functions

#### `unstable_v2_prompt()` - One-shot Queries

```typescript
import { unstable_v2_prompt } from '@anthropic-ai/claude-agent-sdk';

const result = await unstable_v2_prompt('What is 2 + 2?', {
  model: 'claude-sonnet-4-5-20250929'
});
console.log(result.result);
```

#### `unstable_v2_createSession()` - Session-based Conversations

```typescript
import { unstable_v2_createSession } from '@anthropic-ai/claude-agent-sdk';

await using session = unstable_v2_createSession({
  model: 'claude-sonnet-4-5-20250929'
});

// Turn 1
await session.send('Hello!');
for await (const msg of session.stream()) {
  if (msg.type === 'assistant') {
    console.log(msg.message.content);
  }
}

// Turn 2 - Claude remembers previous context
await session.send('What did I just say?');
for await (const msg of session.stream()) {
  // Process response
}
```

#### `unstable_v2_resumeSession()` - Resume Existing Sessions

```typescript
import { unstable_v2_resumeSession } from '@anthropic-ai/claude-agent-sdk';

await using session = unstable_v2_resumeSession(sessionId, {
  model: 'claude-sonnet-4-5-20250929'
});

await session.send('Continue our conversation');
for await (const msg of session.stream()) {
  // Process response
}
```

### Session Interface

```typescript
interface Session {
  send(message: string): Promise<void>;
  stream(): AsyncGenerator<SDKMessage>;
  close(): void;
}
```

### Cleanup Options

**Automatic (TypeScript 5.2+):**
```typescript
await using session = unstable_v2_createSession({ model: '...' });
// Closes automatically when block exits
```

**Manual:**
```typescript
const session = unstable_v2_createSession({ model: '...' });
// ... use session ...
session.close();
```

### Feature Availability

Not yet available in V2:
- Session forking (`forkSession` option)
- Some advanced streaming input patterns

---

## Python SDK Overview

### Installation

```bash
pip install claude-agent-sdk
```

### Two Interfaces: `query()` vs `ClaudeSDKClient`

| Feature | `query()` | `ClaudeSDKClient` |
|---------|-----------|-------------------|
| Session | New each time | Reuses same session |
| Conversation | Single exchange | Multiple exchanges |
| Connection | Managed automatically | Manual control |
| Streaming Input | Supported | Supported |
| Interrupts | Not supported | Supported |
| Hooks | Not supported | Supported |
| Custom Tools | Not supported | Supported |

### `query()` - Simple One-off Tasks

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are an expert Python developer",
        permission_mode='acceptEdits',
        cwd="/home/user/project"
    )

    async for message in query(
        prompt="Create a Python web server",
        options=options
    ):
        print(message)

asyncio.run(main())
```

### `ClaudeSDKClient` - Continuous Conversations

```python
import asyncio
from claude_agent_sdk import ClaudeSDKClient, AssistantMessage, TextBlock

async def main():
    async with ClaudeSDKClient() as client:
        # First question
        await client.query("What's the capital of France?")
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Claude: {block.text}")

        # Follow-up - Claude remembers context
        await client.query("What's the population of that city?")
        async for message in client.receive_response():
            # Process response
            pass

asyncio.run(main())
```

### ClaudeSDKClient Methods

| Method | Description |
|--------|-------------|
| `connect(prompt)` | Connect with optional initial prompt |
| `query(prompt, session_id)` | Send a new request |
| `receive_messages()` | Receive all messages as async iterator |
| `receive_response()` | Receive until ResultMessage |
| `interrupt()` | Send interrupt signal |
| `rewind_files(uuid)` | Restore files to previous state |
| `disconnect()` | Disconnect from Claude |

### ClaudeAgentOptions

Key options (similar to TypeScript):

| Option | Type | Description |
|--------|------|-------------|
| `model` | `str` | Claude model to use |
| `permission_mode` | `PermissionMode` | `'default'`, `'acceptEdits'`, `'bypassPermissions'`, `'plan'` |
| `allowed_tools` | `list[str]` | Allowed tool names |
| `disallowed_tools` | `list[str]` | Disallowed tool names |
| `mcp_servers` | `dict[str, McpServerConfig]` | MCP server configurations |
| `system_prompt` | `str \| SystemPromptPreset` | System prompt configuration |
| `tools` | `list[str] \| ToolsPreset` | Tool configuration |
| `max_turns` | `int` | Maximum conversation turns |
| `max_budget_usd` | `float` | Maximum budget in USD |
| `cwd` | `str \| Path` | Current working directory |
| `hooks` | `dict[HookEvent, list[HookMatcher]]` | Hook configurations |
| `agents` | `dict[str, AgentDefinition]` | Subagent definitions |
| `setting_sources` | `list[SettingSource]` | Which settings to load |
| `sandbox` | `SandboxSettings` | Sandbox configuration |
| `can_use_tool` | `CanUseTool` | Custom permission callback |

### MCP Tool Creation (Python)

```python
from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any

@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{
            "type": "text",
            "text": f"Hello, {args['name']}!"
        }]
    }

server = create_sdk_mcp_server(
    name="my-server",
    version="1.0.0",
    tools=[greet]
)
```

### Hook Events (Python)

Supported hooks (note: Python SDK doesn't support `SessionStart`, `SessionEnd`, `Notification`):

| Event | Description |
|-------|-------------|
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After tool execution |
| `UserPromptSubmit` | When user submits prompt |
| `Stop` | Stop requested |
| `SubagentStop` | Subagent stops |
| `PreCompact` | Before message compaction |

### Message Types (Python)

- `UserMessage` - User input
- `AssistantMessage` - Assistant response
- `SystemMessage` - System message
- `ResultMessage` - Final result
- `StreamEvent` - Streaming events (when `include_partial_messages=True`)

### Content Blocks

- `TextBlock` - Text content
- `ThinkingBlock` - Thinking content (for models with thinking)
- `ToolUseBlock` - Tool use request
- `ToolResultBlock` - Tool execution result

---

## SDK Comparison

### Feature Matrix

| Feature | TypeScript V1 | TypeScript V2 | Python |
|---------|---------------|---------------|--------|
| **Primary Interface** | `query()` async generator | `createSession()` + `send()`/`stream()` | `query()` + `ClaudeSDKClient` |
| **Multi-turn** | Via AsyncIterable input | Native session support | Via `ClaudeSDKClient` |
| **Hooks** | Full support (12 events) | Inherited from V1 | Partial (6 events) |
| **MCP Tools** | `tool()` + Zod schemas | Same as V1 | `@tool` decorator |
| **Interrupts** | Streaming mode only | Via session | Via `ClaudeSDKClient` |
| **Session Resume** | `resume` option | `resumeSession()` | `resume` option |
| **Session Fork** | Supported | Not yet | Supported |
| **Auto Cleanup** | N/A | `await using` | `async with` |
| **Permissions** | `canUseTool` callback | Same as V1 | `can_use_tool` callback |
| **Sandbox** | Full support | Same as V1 | Full support |

### API Style Comparison

**TypeScript V1:**
```typescript
const q = query({ prompt: '...', options });
for await (const msg of q) { /* process */ }
```

**TypeScript V2:**
```typescript
await using session = unstable_v2_createSession(options);
await session.send('...');
for await (const msg of session.stream()) { /* process */ }
```

**Python query():**
```python
async for message in query(prompt='...', options=options):
    # process
```

**Python ClaudeSDKClient:**
```python
async with ClaudeSDKClient(options) as client:
    await client.query('...')
    async for message in client.receive_response():
        # process
```

### Option Name Differences

| TypeScript | Python |
|------------|--------|
| `permissionMode` | `permission_mode` |
| `allowedTools` | `allowed_tools` |
| `disallowedTools` | `disallowed_tools` |
| `mcpServers` | `mcp_servers` |
| `systemPrompt` | `system_prompt` |
| `maxTurns` | `max_turns` |
| `maxBudgetUsd` | `max_budget_usd` |
| `canUseTool` | `can_use_tool` |
| `settingSources` | `setting_sources` |

---

## Common Patterns and Examples

### 1. Basic Query (All SDKs)

**TypeScript V1:**
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const msg of query({
  prompt: 'Write a hello world in Python',
  options: { permissionMode: 'acceptEdits' }
})) {
  if (msg.type === 'result' && msg.subtype === 'success') {
    console.log(msg.result);
  }
}
```

**TypeScript V2:**
```typescript
import { unstable_v2_prompt } from '@anthropic-ai/claude-agent-sdk';

const result = await unstable_v2_prompt('Write a hello world in Python', {
  permissionMode: 'acceptEdits'
});
console.log(result.result);
```

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage

async for msg in query(
    prompt='Write a hello world in Python',
    options=ClaudeAgentOptions(permission_mode='acceptEdits')
):
    if isinstance(msg, ResultMessage):
        print(msg.result)
```

### 2. Multi-turn Conversation

**TypeScript V2:**
```typescript
await using session = unstable_v2_createSession({ model: 'claude-sonnet-4-5-20250929' });

await session.send('My name is Alice');
for await (const msg of session.stream()) { /* acknowledge */ }

await session.send('What is my name?');
for await (const msg of session.stream()) {
  // Claude responds "Alice"
}
```

**Python:**
```python
async with ClaudeSDKClient() as client:
    await client.query("My name is Alice")
    async for msg in client.receive_response():
        pass  # acknowledge

    await client.query("What is my name?")
    async for msg in client.receive_response():
        # Claude responds "Alice"
        pass
```

### 3. Custom MCP Tool

**TypeScript:**
```typescript
import { tool, createSdkMcpServer, query } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

const calculator = tool(
  'calculate',
  'Perform math calculations',
  { expression: z.string() },
  async ({ expression }) => ({
    content: [{ type: 'text', text: String(eval(expression)) }]
  })
);

const server = createSdkMcpServer({
  name: 'calc',
  tools: [calculator]
});

for await (const msg of query({
  prompt: 'What is 5 * 7?',
  options: {
    mcpServers: { calc: server },
    allowedTools: ['mcp__calc__calculate']
  }
})) {
  // Process response
}
```

**Python:**
```python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeAgentOptions

@tool("calculate", "Perform math calculations", {"expression": str})
async def calculate(args):
    return {
        "content": [{"type": "text", "text": str(eval(args["expression"]))}]
    }

server = create_sdk_mcp_server(name="calc", tools=[calculate])

options = ClaudeAgentOptions(
    mcp_servers={"calc": server},
    allowed_tools=["mcp__calc__calculate"]
)

async with ClaudeSDKClient(options) as client:
    await client.query("What is 5 * 7?")
    async for msg in client.receive_response():
        pass
```

### 4. Hook Implementation

**TypeScript:**
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const logHook = async (input, toolUseId, { signal }) => {
  console.log(`Tool: ${input.tool_name}`);
  return {};
};

for await (const msg of query({
  prompt: 'List files',
  options: {
    hooks: {
      PreToolUse: [{ hooks: [logHook] }],
      PostToolUse: [{ hooks: [logHook] }]
    }
  }
})) {
  // Process
}
```

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher

async def log_hook(input_data, tool_use_id, context):
    print(f"Tool: {input_data.get('tool_name')}")
    return {}

options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [HookMatcher(hooks=[log_hook])],
        'PostToolUse': [HookMatcher(hooks=[log_hook])]
    }
)

async for msg in query(prompt='List files', options=options):
    pass
```

### 5. Custom Permission Handler

**TypeScript:**
```typescript
const canUseTool = async (toolName, input, { signal, suggestions }) => {
  if (toolName === 'Bash' && input.command.includes('rm -rf')) {
    return { behavior: 'deny', message: 'Dangerous command blocked' };
  }
  return { behavior: 'allow', updatedInput: input };
};

for await (const msg of query({
  prompt: 'Clean up temp files',
  options: { canUseTool }
})) {
  // Process
}
```

**Python:**
```python
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny

async def can_use_tool(tool_name, input_data, context):
    if tool_name == 'Bash' and 'rm -rf' in input_data.get('command', ''):
        return PermissionResultDeny(message='Dangerous command blocked')
    return PermissionResultAllow(updated_input=input_data)

options = ClaudeAgentOptions(can_use_tool=can_use_tool)
```

### 6. Sandbox Configuration

**TypeScript:**
```typescript
for await (const msg of query({
  prompt: 'Build the project',
  options: {
    sandbox: {
      enabled: true,
      autoAllowBashIfSandboxed: true,
      network: { allowLocalBinding: true }
    }
  }
})) {
  // Process
}
```

**Python:**
```python
options = ClaudeAgentOptions(
    sandbox={
        "enabled": True,
        "autoAllowBashIfSandboxed": True,
        "network": {"allowLocalBinding": True}
    }
)

async for msg in query(prompt='Build the project', options=options):
    pass
```

### 7. Using Subagents

**TypeScript:**
```typescript
for await (const msg of query({
  prompt: 'Review and fix the code',
  options: {
    agents: {
      reviewer: {
        description: 'Code review specialist',
        prompt: 'You are a code reviewer. Find bugs and issues.',
        tools: ['Read', 'Grep', 'Glob'],
        model: 'sonnet'
      },
      fixer: {
        description: 'Code fixer',
        prompt: 'You fix code issues.',
        tools: ['Read', 'Edit', 'Write'],
        model: 'sonnet'
      }
    }
  }
})) {
  // Process
}
```

**Python:**
```python
from claude_agent_sdk import AgentDefinition

options = ClaudeAgentOptions(
    agents={
        'reviewer': AgentDefinition(
            description='Code review specialist',
            prompt='You are a code reviewer. Find bugs and issues.',
            tools=['Read', 'Grep', 'Glob'],
            model='sonnet'
        ),
        'fixer': AgentDefinition(
            description='Code fixer',
            prompt='You fix code issues.',
            tools=['Read', 'Edit', 'Write'],
            model='sonnet'
        )
    }
)
```

---

## Summary

- **TypeScript V1** provides a powerful async generator interface suitable for most use cases
- **TypeScript V2** (preview) simplifies multi-turn conversations with explicit session management
- **Python SDK** offers two interfaces: `query()` for simple tasks and `ClaudeSDKClient` for continuous conversations
- All SDKs support MCP tools, hooks (with some limitations in Python), permissions, and sandboxing
- Configuration options are nearly identical across SDKs (with naming convention differences)
- Choose the interface based on your needs: one-shot queries, multi-turn conversations, or interactive applications
