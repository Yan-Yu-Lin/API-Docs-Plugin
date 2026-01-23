# Claude Agent SDK: Plugin/Skill Developers Summary

This document summarizes the Plugin/Skill Developer documentation for the Claude Agent SDK, covering the plugin system architecture, skills, slash commands, and MCP integration.

---

## Table of Contents

1. [Plugin System Architecture](#plugin-system-architecture)
2. [Agent Skills](#agent-skills)
3. [Slash Commands](#slash-commands)
4. [MCP (Model Context Protocol) Integration](#mcp-model-context-protocol-integration)
5. [How These Systems Interact](#how-these-systems-interact)

---

## Plugin System Architecture

### What Are Plugins?

Plugins are packages of Claude Code extensions that can include multiple components:

- **Commands**: Custom slash commands
- **Agents**: Specialized subagents for specific tasks
- **Skills**: Model-invoked capabilities that Claude uses autonomously
- **Hooks**: Event handlers that respond to tool use and other events
- **MCP servers**: External tool integrations via Model Context Protocol

### Plugin Directory Structure

A plugin must contain a `.claude-plugin/plugin.json` manifest file:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── commands/                 # Custom slash commands
│   └── custom-cmd.md
├── agents/                   # Custom agents
│   └── specialist.md
├── skills/                   # Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   └── hooks.json
└── .mcp.json                # MCP server definitions
```

### Loading Plugins

Plugins are loaded by specifying their filesystem paths in the SDK options:

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Hello",
  options: {
    plugins: [
      { type: "local", path: "./my-plugin" },
      { type: "local", path: "/absolute/path/to/another-plugin" }
    ]
  }
})) {
  // Plugin features are now available
}
```

**Python:**
```python
from claude_agent_sdk import query

async for message in query(
    prompt="Hello",
    options={
        "plugins": [
            {"type": "local", "path": "./my-plugin"},
            {"type": "local", "path": "/absolute/path/to/another-plugin"}
        ]
    }
):
    pass
```

### Plugin Commands Namespacing

Commands from plugins are automatically namespaced with the format `plugin-name:command-name` to avoid conflicts.

### Verifying Plugin Installation

Check the system initialization message to verify plugins loaded successfully:

```typescript
if (message.type === "system" && message.subtype === "init") {
  console.log("Plugins:", message.plugins);
  console.log("Commands:", message.slash_commands);
}
```

---

## Agent Skills

### Overview

Agent Skills extend Claude with specialized capabilities that Claude **autonomously invokes** when relevant. Unlike slash commands (user-invoked), Skills are model-invoked based on context matching.

### Key Characteristics

1. **Filesystem artifacts**: Created as `SKILL.md` files in specific directories
2. **Automatically discovered**: Skill metadata is discovered at startup
3. **Model-invoked**: Claude autonomously chooses when to use them based on context
4. **Lazy loaded**: Full content only loaded when triggered

### Skill Locations

- **Project Skills**: `.claude/skills/` - Shared with team via git
- **User Skills**: `~/.claude/skills/` - Personal skills across all projects
- **Plugin Skills**: Bundled with installed Claude Code plugins

### Creating Skills

Skills are directories containing a `SKILL.md` file with YAML frontmatter:

```
.claude/skills/processing-pdfs/
└── SKILL.md
```

### Using Skills with the SDK

Skills require explicit configuration:

1. Include `"Skill"` in your `allowed_tools`
2. Configure `setting_sources` to load Skills from the filesystem

**Python:**
```python
options = ClaudeAgentOptions(
    cwd="/path/to/project",
    setting_sources=["user", "project"],  # Required for Skills
    allowed_tools=["Skill", "Read", "Write", "Bash"]
)
```

**TypeScript:**
```typescript
const options = {
  cwd: "/path/to/project",
  settingSources: ["user", "project"],  // Required for Skills
  allowedTools: ["Skill", "Read", "Write", "Bash"]
};
```

### Important Notes

- **Default behavior**: The SDK does NOT load filesystem settings by default. You must explicitly configure `settingSources`/`setting_sources`.
- **Tool restrictions**: The `allowed-tools` frontmatter field in SKILL.md only works with Claude Code CLI, NOT through the SDK. Use `allowedTools` in query configuration instead.

---

## Slash Commands

### Overview

Slash commands are user-invoked controls that start with `/`. They can be built-in commands or custom commands defined as markdown files.

### Discovering Available Commands

Available commands appear in the system initialization message:

```typescript
if (message.type === "system" && message.subtype === "init") {
  console.log("Available slash commands:", message.slash_commands);
  // Example: ["/compact", "/clear", "/help"]
}
```

### Sending Slash Commands

Send commands by including them in your prompt string:

```typescript
for await (const message of query({
  prompt: "/compact",
  options: { maxTurns: 1 }
})) {
  // Command executes
}
```

### Common Built-in Commands

| Command | Description |
|---------|-------------|
| `/compact` | Reduces conversation history by summarizing older messages |
| `/clear` | Starts a fresh conversation by clearing all history |
| `/help` | Shows available commands |

### Creating Custom Slash Commands

Custom commands are markdown files stored in designated directories:

- **Project commands**: `.claude/commands/` - Available only in current project
- **Personal commands**: `~/.claude/commands/` - Available across all projects

#### Basic Example

Create `.claude/commands/refactor.md`:

```markdown
Refactor the selected code to improve readability and maintainability.
Focus on clean code principles and best practices.
```

This creates the `/refactor` command.

#### With Frontmatter

```markdown
---
allowed-tools: Read, Grep, Glob
description: Run security vulnerability scan
model: claude-sonnet-4-5-20250929
---

Analyze the codebase for security vulnerabilities including:
- SQL injection risks
- XSS vulnerabilities
- Exposed credentials
```

#### Advanced Features

**Arguments and Placeholders:**
```markdown
---
argument-hint: [issue-number] [priority]
description: Fix a GitHub issue
---

Fix issue #$1 with priority $2.
```

**Bash Command Execution:**
```markdown
## Context
- Current status: !`git status`
- Current diff: !`git diff HEAD`
```

**File References:**
```markdown
Review the following:
- Package config: @package.json
- TypeScript config: @tsconfig.json
```

---

## MCP (Model Context Protocol) Integration

### Overview

MCP is an open standard for connecting AI agents to external tools and data sources. With MCP, your agent can:

- Query databases
- Integrate with APIs (Slack, GitHub, etc.)
- Connect to other services without custom implementations

### Transport Types

| Type | Use Case | Configuration |
|------|----------|---------------|
| **stdio** | Local processes via stdin/stdout | `command` and `args` fields |
| **HTTP/SSE** | Cloud-hosted/remote APIs | `type: "http"` or `type: "sse"` with `url` |
| **SDK MCP servers** | Custom tools in application code | Defined programmatically |

### Adding MCP Servers

**In Code:**
```typescript
options: {
  mcpServers: {
    "github": {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-github"],
      env: {
        GITHUB_TOKEN: process.env.GITHUB_TOKEN
      }
    }
  },
  allowedTools: ["mcp__github__*"]
}
```

**From Config File (`.mcp.json`):**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Tool Naming Convention

MCP tools follow the pattern: `mcp__<server-name>__<tool-name>`

Example: A GitHub server named `"github"` with `list_issues` tool becomes `mcp__github__list_issues`.

### Allowing MCP Tools

MCP tools require explicit permission via `allowedTools`:

```typescript
allowedTools: [
  "mcp__github__*",              // All tools from github server
  "mcp__db__query",              // Only query tool from db server
  "mcp__slack__send_message"     // Only send_message from slack
]
```

Wildcards (`*`) allow all tools from a server.

### Alternative: Permission Modes

Instead of listing allowed tools:

- `permissionMode: "acceptEdits"`: Automatically approves tool usage (still prompts for destructive operations)
- `permissionMode: "bypassPermissions"`: Skips all safety prompts (use with caution)

### MCP Tool Search

For large tool sets, tool search dynamically loads tools on-demand instead of preloading all of them:

- **auto mode (default)**: Activates when tools exceed 10% of context window
- Configure via `ENABLE_TOOL_SEARCH` environment variable:
  - `"auto"` - Default threshold (10%)
  - `"auto:5"` - Custom threshold (5%)
  - `"true"` - Always enabled
  - `"false"` - Disabled

### Authentication

**Environment Variables (stdio servers):**
```typescript
env: {
  GITHUB_TOKEN: process.env.GITHUB_TOKEN
}
```

**HTTP Headers (remote servers):**
```typescript
mcpServers: {
  "secure-api": {
    type: "http",
    url: "https://api.example.com/mcp",
    headers: {
      Authorization: `Bearer ${process.env.API_TOKEN}`
    }
  }
}
```

### Error Handling

Check the `init` message for server connection status:

```typescript
if (message.type === "system" && message.subtype === "init") {
  const failedServers = message.mcp_servers.filter(
    s => s.status !== "connected"
  );
  if (failedServers.length > 0) {
    console.warn("Failed to connect:", failedServers);
  }
}
```

---

## How These Systems Interact

### Hierarchical Relationship

```
Plugin
├── Contains Skills (SKILL.md files in skills/ directory)
├── Contains Commands (markdown files in commands/ directory)
├── Contains Agents (markdown files in agents/ directory)
├── Contains Hooks (hooks.json)
└── Contains MCP Servers (.mcp.json)
```

### Invocation Model

| Component | Invoked By | Trigger |
|-----------|------------|---------|
| **Slash Commands** | User | Explicit `/command` in prompt |
| **Skills** | Model (Claude) | Context matching against description |
| **MCP Tools** | Model (Claude) | Task requirements matching tool capabilities |
| **Hooks** | System | Events (tool use, etc.) |

### Loading and Discovery

1. **Plugins**: Loaded via `plugins` option with filesystem paths
2. **Skills**: Loaded when `settingSources`/`setting_sources` includes `"user"` or `"project"`
3. **MCP Servers**: Loaded via `mcpServers`/`mcp_servers` option or `.mcp.json` file
4. **Commands**: Automatically discovered from plugin `commands/` directory or `.claude/commands/`

### Permission Model

- **Skills**: Require `"Skill"` in `allowedTools` plus `settingSources` configuration
- **MCP Tools**: Require explicit permission via `allowedTools` or `permissionMode`
- **Plugin Commands**: Automatically available with `plugin-name:command-name` namespace

### Practical Integration Example

A complete setup loading plugins with skills, commands, and MCP servers:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Help me with the project",
  options: {
    cwd: "/path/to/project",
    settingSources: ["user", "project"],  // Enable Skills loading
    plugins: [
      { type: "local", path: "./my-plugin" }  // Load plugin
    ],
    mcpServers: {
      "github": {
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-github"],
        env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN }
      }
    },
    allowedTools: [
      "Skill",                    // Enable Skills
      "mcp__github__*",           // Enable GitHub MCP tools
      "Read", "Write", "Bash"     // Standard tools
    ]
  }
})) {
  // Process messages
}
```

---

## Summary

| System | Purpose | Location | Invocation |
|--------|---------|----------|------------|
| **Plugins** | Package extensions together | `.claude-plugin/` directory | Loaded via SDK options |
| **Skills** | Model-invoked specialized capabilities | `.claude/skills/` or `~/.claude/skills/` | Automatic (context-based) |
| **Slash Commands** | User-invoked controls | `.claude/commands/` or `~/.claude/commands/` | Explicit `/command` |
| **MCP** | External tool integrations | `.mcp.json` or in-code | Automatic (task-based) |

The Claude Agent SDK provides a flexible, layered architecture where:
- **Plugins** serve as containers for organizing related extensions
- **Skills** enable autonomous Claude capabilities
- **Slash Commands** provide explicit user controls
- **MCP** connects to the broader ecosystem of external tools and services
