# Claude Agent SDK: Agent Builders Guide

A comprehensive summary of the Claude Agent SDK documentation for building sophisticated agents, covering custom tools, subagents, hooks, permissions, and user input handling.

---

## Table of Contents

1. [Custom Tools](#custom-tools)
2. [Subagents and Multi-Agent Patterns](#subagents-and-multi-agent-patterns)
3. [Hook System](#hook-system)
4. [Permission System and Security Model](#permission-system-and-security-model)
5. [Handling User Input and Approvals](#handling-user-input-and-approvals)

---

## Custom Tools

Custom tools extend Claude's capabilities by creating in-process MCP (Model Context Protocol) servers that enable Claude to interact with external services, APIs, or perform specialized operations.

### Creating Custom Tools

Use `createSdkMcpServer` and `tool` helper functions to define type-safe custom tools:

**TypeScript:**
```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const customServer = createSdkMcpServer({
  name: "my-custom-tools",
  version: "1.0.0",
  tools: [
    tool(
      "get_weather",
      "Get current temperature for a location",
      {
        latitude: z.number().describe("Latitude coordinate"),
        longitude: z.number().describe("Longitude coordinate")
      },
      async (args) => {
        // Implementation
        return {
          content: [{ type: "text", text: `Temperature: ${temp}` }]
        };
      }
    )
  ]
});
```

**Python:**
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("get_weather", "Get current temperature", {"latitude": float, "longitude": float})
async def get_weather(args: dict) -> dict:
    # Implementation
    return {"content": [{"type": "text", "text": f"Temperature: {temp}"}]}

custom_server = create_sdk_mcp_server(
    name="my-custom-tools",
    version="1.0.0",
    tools=[get_weather]
)
```

### Tool Name Format

MCP tools follow a specific naming convention:
- Pattern: `mcp__{server_name}__{tool_name}`
- Example: `mcp__my-custom-tools__get_weather`

### Key Requirements

- **Streaming Input Mode Required**: Custom MCP tools require an async generator/iterable for the `prompt` parameter
- **Pass as Dictionary**: MCP servers are passed via the `mcpServers` option as a dictionary/object
- **Configurable Access**: Use `allowedTools` to control which tools Claude can use

### Type Safety

- **TypeScript**: Use Zod schemas for runtime validation and TypeScript types
- **Python**: Use simple type mappings (`{"name": str}`) or JSON Schema format for complex validation

### Error Handling

Always return meaningful error messages within the tool's content response rather than throwing exceptions:

```python
try:
    # Tool logic
except Exception as e:
    return {"content": [{"type": "text", "text": f"Failed: {str(e)}"}]}
```

---

## Subagents and Multi-Agent Patterns

Subagents are separate agent instances that your main agent can spawn to handle focused subtasks, enabling context isolation, parallel execution, and specialized behaviors.

### Benefits of Subagents

| Benefit | Description |
|---------|-------------|
| **Context Management** | Separate context prevents information overload |
| **Parallelization** | Multiple subagents run concurrently for faster workflows |
| **Specialized Instructions** | Tailored system prompts with specific expertise |
| **Tool Restrictions** | Limit subagents to specific tools for safety |

### Creating Subagents

Three methods are available:
1. **Programmatic** (recommended): Use the `agents` parameter in `query()` options
2. **Filesystem-based**: Define agents as markdown files in `.claude/agents/`
3. **Built-in**: Claude can invoke the built-in `general-purpose` subagent automatically

**Example:**
```python
async for message in query(
    prompt="Review the authentication module",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Grep", "Glob", "Task"],  # Task required for subagents
        agents={
            "code-reviewer": AgentDefinition(
                description="Expert code review specialist",
                prompt="You are a code review specialist...",
                tools=["Read", "Grep", "Glob"],  # Read-only access
                model="sonnet"  # Model override
            )
        }
    )
)
```

### AgentDefinition Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | `string` | Yes | When to use this agent |
| `prompt` | `string` | Yes | System prompt defining behavior |
| `tools` | `string[]` | No | Allowed tools (inherits all if omitted) |
| `model` | `string` | No | Model override: `sonnet`, `opus`, `haiku`, `inherit` |

### Invocation Methods

- **Automatic**: Claude decides based on task and subagent descriptions
- **Explicit**: Mention subagent by name: "Use the code-reviewer agent to..."

### Dynamic Agent Configuration

Create agent definitions at runtime based on conditions:

```python
def create_security_agent(security_level: str) -> AgentDefinition:
    is_strict = security_level == "strict"
    return AgentDefinition(
        description="Security code reviewer",
        prompt=f"You are a {'strict' if is_strict else 'balanced'} security reviewer...",
        tools=["Read", "Grep", "Glob"],
        model="opus" if is_strict else "sonnet"
    )
```

### Resuming Subagents

Subagents can be resumed to continue where they left off:
1. Capture the `session_id` from messages
2. Extract the `agentId` from Task tool results
3. Pass `resume: sessionId` in subsequent queries

### Important Constraints

- Subagents **cannot** spawn their own subagents (don't include `Task` in subagent tools)
- Subagent transcripts persist independently of the main conversation
- Automatic cleanup after `cleanupPeriodDays` (default: 30 days)

---

## Hook System

Hooks intercept agent execution at key points to add validation, logging, security controls, or custom logic.

### Available Hooks

| Hook Event | Python | TypeScript | Trigger |
|------------|--------|------------|---------|
| `PreToolUse` | Yes | Yes | Before tool execution (can block/modify) |
| `PostToolUse` | Yes | Yes | After tool execution |
| `PostToolUseFailure` | No | Yes | Tool execution failure |
| `UserPromptSubmit` | Yes | Yes | User prompt submission |
| `Stop` | Yes | Yes | Agent execution stop |
| `SubagentStart` | No | Yes | Subagent initialization |
| `SubagentStop` | Yes | Yes | Subagent completion |
| `PreCompact` | Yes | Yes | Conversation compaction |
| `PermissionRequest` | No | Yes | Permission dialog trigger |
| `SessionStart` | No | Yes | Session initialization |
| `SessionEnd` | No | Yes | Session termination |
| `Notification` | No | Yes | Agent status messages |

### Hook Configuration

```python
options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [HookMatcher(matcher='Write|Edit', hooks=[my_callback])]
    }
)
```

### Matcher Options

| Option | Default | Description |
|--------|---------|-------------|
| `matcher` | `undefined` | Regex pattern to match tool names |
| `hooks` | Required | Array of callback functions |
| `timeout` | `60` | Timeout in seconds |

### Callback Function Signature

```python
async def my_hook(input_data, tool_use_id, context):
    # input_data: event details (tool_name, tool_input, etc.)
    # tool_use_id: correlate PreToolUse and PostToolUse events
    # context: AbortSignal in TypeScript, reserved in Python
    return {}  # Return empty to allow, or with hookSpecificOutput to control
```

### Callback Output Options

**Top-level fields:**
- `continue`: Whether agent should continue (default: `true`)
- `stopReason`: Message when `continue` is `false`
- `suppressOutput`: Hide stdout from transcript
- `systemMessage`: Inject message for Claude to see

**hookSpecificOutput fields:**
- `hookEventName`: Required, matches `input.hook_event_name`
- `permissionDecision`: `'allow'`, `'deny'`, or `'ask'`
- `permissionDecisionReason`: Explanation for decision
- `updatedInput`: Modified tool input (requires `allow`)
- `additionalContext`: Context added to conversation

### Permission Decision Flow

1. **Deny** rules checked first (any match = immediate denial)
2. **Ask** rules checked second
3. **Allow** rules checked third
4. **Default to Ask** if nothing matches

### Common Patterns

**Block dangerous operations:**
```python
async def block_dangerous(input_data, tool_use_id, context):
    if 'rm -rf /' in input_data['tool_input'].get('command', ''):
        return {
            'hookSpecificOutput': {
                'hookEventName': input_data['hook_event_name'],
                'permissionDecision': 'deny',
                'permissionDecisionReason': 'Dangerous command blocked'
            }
        }
    return {}
```

**Modify tool input:**
```python
async def redirect_to_sandbox(input_data, tool_use_id, context):
    return {
        'hookSpecificOutput': {
            'hookEventName': input_data['hook_event_name'],
            'permissionDecision': 'allow',
            'updatedInput': {
                **input_data['tool_input'],
                'file_path': f"/sandbox{input_data['tool_input']['file_path']}"
            }
        }
    }
```

**Auto-approve read-only tools:**
```python
async def auto_approve_readonly(input_data, tool_use_id, context):
    if input_data['tool_name'] in ['Read', 'Glob', 'Grep']:
        return {
            'hookSpecificOutput': {
                'hookEventName': input_data['hook_event_name'],
                'permissionDecision': 'allow'
            }
        }
    return {}
```

---

## Permission System and Security Model

The SDK provides layered permission controls to manage how Claude uses tools.

### Permission Evaluation Order

1. **Hooks** - Run first, can allow, deny, or continue
2. **Permission Rules** - Declarative rules in `settings.json` (deny > allow > ask)
3. **Permission Mode** - Global mode setting
4. **canUseTool Callback** - Runtime decision if not resolved

### Permission Modes

| Mode | Description |
|------|-------------|
| `default` | Standard behavior; unmatched tools trigger `canUseTool` |
| `acceptEdits` | Auto-accept file edits and filesystem operations |
| `bypassPermissions` | All tools run without prompts (use with caution) |
| `plan` | No tool execution; Claude plans only |

### Setting Permission Mode

**At query time:**
```python
options = ClaudeAgentOptions(permission_mode="default")
```

**During streaming:**
```python
q = query(prompt="...", options=ClaudeAgentOptions(permission_mode="default"))
await q.set_permission_mode("acceptEdits")  # Change mid-session
```

### Mode Details

**acceptEdits Mode:**
- Auto-approves: File edits (Edit, Write), filesystem commands (`mkdir`, `touch`, `rm`, `mv`, `cp`)
- Other tools still require normal permissions

**bypassPermissions Mode:**
- Auto-approves all tool uses
- Hooks still execute and can block
- **Warning**: Subagents inherit this mode and cannot override it

**plan Mode:**
- Prevents tool execution entirely
- Claude can analyze and create plans
- May use `AskUserQuestion` for clarification

---

## Handling User Input and Approvals

Claude requests user input for tool permissions and clarifying questions, pausing execution until you respond.

### canUseTool Callback

```python
async def can_use_tool(tool_name, input_data, context):
    if tool_name == "AskUserQuestion":
        return await handle_clarifying_questions(input_data)

    # Prompt user for approval
    if approved:
        return PermissionResultAllow(updated_input=input_data)
    return PermissionResultDeny(message="User denied this action")
```

### Response Types

| Response | Python | TypeScript |
|----------|--------|------------|
| Allow | `PermissionResultAllow(updated_input=...)` | `{ behavior: "allow", updatedInput }` |
| Deny | `PermissionResultDeny(message=...)` | `{ behavior: "deny", message }` |

### Response Strategies

- **Approve**: Pass through input unchanged
- **Approve with changes**: Modify input before execution (sanitize paths, add constraints)
- **Reject**: Block and provide explanation
- **Suggest alternative**: Block but guide Claude toward alternatives
- **Redirect**: Use streaming input for complete direction change

### Handling Clarifying Questions (AskUserQuestion)

When Claude needs direction with multiple valid approaches, it calls `AskUserQuestion`:

```json
{
  "questions": [
    {
      "question": "How should I format the output?",
      "header": "Format",
      "options": [
        { "label": "Summary", "description": "Brief overview" },
        { "label": "Detailed", "description": "Full explanation" }
      ],
      "multiSelect": false
    }
  ]
}
```

**Response format:**
```python
return PermissionResultAllow(
    updated_input={
        "questions": input_data["questions"],
        "answers": {
            "How should I format the output?": "Summary"
        }
    }
)
```

### Question Format

| Field | Description |
|-------|-------------|
| `question` | Full question text to display |
| `header` | Short label (max 12 characters) |
| `options` | Array of 2-4 choices with `label` and `description` |
| `multiSelect` | If `true`, allow multiple selections |

### Python Requirements

In Python, `can_use_tool` requires:
1. Streaming mode (async generator for prompt)
2. A `PreToolUse` hook returning `{"continue_": True}` to keep the stream open

### Limitations

- **60-second timeout**: Callbacks must return within 60 seconds
- **Subagents**: `AskUserQuestion` not available in subagents
- **Question limits**: 1-4 questions with 2-4 options each

### Alternative Input Methods

- **Streaming Input**: For interrupting mid-task, providing additional context, or chat interfaces
- **Custom Tools**: For structured input, external approval systems, or domain-specific interactions

---

## Quick Reference

### Essential Imports

**TypeScript:**
```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";
```

**Python:**
```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition, HookMatcher
from claude_agent_sdk import tool, create_sdk_mcp_server
from claude_agent_sdk.types import PermissionResultAllow, PermissionResultDeny
```

### Common Tool Combinations for Subagents

| Use Case | Tools |
|----------|-------|
| Read-only analysis | `Read`, `Grep`, `Glob` |
| Test execution | `Bash`, `Read`, `Grep` |
| Code modification | `Read`, `Edit`, `Write`, `Grep`, `Glob` |
| Full access | Omit `tools` field to inherit all |

### Security Best Practices

1. Use the most restrictive permission mode that works for your use case
2. Implement hooks to block dangerous operations before they execute
3. Restrict subagent tools to minimum required capabilities
4. Always validate and sanitize tool inputs in hooks
5. Log all tool calls for audit trails
6. Be cautious with `bypassPermissions` - subagents inherit it
