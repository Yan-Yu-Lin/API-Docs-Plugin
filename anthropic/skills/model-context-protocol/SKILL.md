---
name: model-context-protocol
description: Comprehensive guidance for Model Context Protocol (MCP), an open protocol for connecting AI applications to external data sources and tools. Use when working with MCP servers, MCP clients, building integrations with Claude Desktop, Claude Code, connecting LLMs to databases, APIs, file systems, implementing tools/resources/prompts, working with stdio or HTTP transports, MCP SDK implementations (TypeScript, Python, Java, Go, Kotlin, Swift, C#, Ruby, Rust, PHP), debugging MCP connections, implementing OAuth authorization, handling JSON-RPC messages, creating agentic workflows, sampling, elicitation, roots management, working with MCP Inspector, deploying remote MCP servers, or any questions about the MCP specification, architecture, best practices, security, or troubleshooting.
---

# Model Context Protocol (MCP)

## What is MCP?

The Model Context Protocol (MCP) is an open-source standard that enables seamless integration between AI applications and external data sources and tools. Think of it as a "USB-C port for AI applications" - it provides a standardized way to connect LLMs to the context they need.

MCP solves a fundamental limitation: AI tools are powerful but often information-limited. Instead of building custom integrations for each use case, MCP provides a universal protocol that works across different tools and platforms.

## Core Architecture

MCP follows a client-server architecture with three key participants:

1. **MCP Host**: The AI application that coordinates connections (e.g., Claude Desktop, Visual Studio Code, ChatGPT)
2. **MCP Client**: Maintains a 1:1 connection with an MCP server and obtains context for the host
3. **MCP Server**: A program that exposes tools, resources, and prompts to clients

Servers can run locally (using stdio transport) or remotely (using HTTP transport). Multiple servers can be connected simultaneously for complex workflows.

## When to Use This Skill

Use this skill when:
- Building MCP servers to expose your data and functionality
- Creating MCP clients to consume MCP services
- Connecting Claude Desktop or Claude Code to local or remote servers
- Implementing tools (model-controlled functions), resources (application-controlled data), or prompts (user-controlled templates)
- Working with any MCP SDK (TypeScript, Python, Java, Go, Kotlin, Swift, C#, Ruby, Rust, PHP)
- Debugging MCP connections or troubleshooting server issues
- Implementing OAuth 2.1 authorization for MCP servers
- Setting up transport layers (stdio, HTTP Streamable-HTTP, SSE)
- Creating agentic workflows with sampling or elicitation
- Understanding the MCP specification or protocol details

## MCP Primitives

MCP defines three main building blocks:

### Tools (Model-Controlled)
Functions that AI models can actively call to perform actions.

**Key characteristics:**
- Schema-defined interfaces using JSON Schema
- Model decides when to use them
- May require user consent
- Support both unstructured (text, images, audio) and structured (JSON) outputs

**Protocol operations:**
- `tools/list`: Discover available tools
- `tools/call`: Execute a tool
- `notifications/tools/list_changed`: List changed notification

### Resources (Application-Controlled)
Passive data sources that provide read-only access to information for context.

**Key characteristics:**
- Each has a unique URI and MIME type
- Supports direct resources (fixed URIs) and resource templates (dynamic URIs with parameters)
- Can be text or binary (base64-encoded)

**Protocol operations:**
- `resources/list`: List available resources
- `resources/templates/list`: List URI templates
- `resources/read`: Retrieve resource contents
- `resources/subscribe`: Monitor resource changes

### Prompts (User-Controlled)
Reusable templates that help structure interactions with language models.

**Key characteristics:**
- Require explicit user invocation
- Support parameter completion
- Can be context-aware (reference resources and tools)

**Protocol operations:**
- `prompts/list`: Discover available prompts
- `prompts/get`: Retrieve prompt details with arguments

## Building MCP Servers

### Quick Start Pattern

All MCP server implementations follow this pattern:

1. **Server initialization** with capabilities declaration
2. **Tool/resource/prompt registration** with handler functions
3. **Transport setup** (stdio or HTTP)
4. **Main execution loop**

### Example: Python Server with FastMCP

```python
from mcp.server.fastmcp import FastMCP
import httpx

# Initialize server
mcp = FastMCP("weather")

# Define tool
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    # Implementation
    return result

# Run server
def main():
    mcp.run(transport='stdio')
```

### Example: TypeScript Server

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather",
  version: "1.0.0",
  capabilities: { resources: {}, tools: {} },
});

server.tool(
  "get_alerts",
  "Get weather alerts for a state",
  { state: z.string().length(2).describe("Two-letter state code") },
  async ({ state }) => {
    // Implementation
    return { content: [{ type: "text", text: result }] };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
```

### Critical Logging Guidelines

For stdio-based servers:
- **NEVER** write to stdout (use stderr or logging libraries)
- Writing to stdout corrupts JSON-RPC messages and breaks the server
- In Python: Use `logging` module, not `print()`
- In JavaScript: Use `console.error()`, not `console.log()`
- In Go: Don't use `fmt.Println()`

For HTTP-based servers:
- Standard output logging is fine

## Building MCP Clients

### Client Architecture

MCP clients handle:
- Server connection and lifecycle management
- Tool discovery and execution
- Resource access and subscription
- Prompt retrieval and execution
- Integration with LLM APIs (like Claude)

### Query Processing Flow

1. Initialize messages array with user query
2. Get available tools from MCP server
3. Send query to LLM with tool definitions
4. Process response in a loop:
   - Extract text responses
   - Detect and execute tool calls via MCP
   - Add tool results back to conversation
   - Continue until no more tool calls needed
5. Return final response

### Example: Python Client

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic

class MCPClient:
    async def connect_to_server(self, server_script_path: str):
        command = "python" if server_script_path.endswith('.py') else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path]
        )
        
        self.stdio, self.write = await stdio_client(server_params)
        self.session = ClientSession(self.stdio, self.write)
        await self.session.initialize()
        
        # Get tools
        response = await self.session.list_tools()
        tools = response.tools
```

## Configuration

### Connecting to Claude Desktop

Configuration file location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Example configuration:

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**Important notes:**
- Use absolute paths (not relative)
- On Windows: Use double backslashes (`\\`) or forward slashes (`/`)
- Restart Claude Desktop after configuration changes

### Logs Location

- **macOS**: `~/Library/Logs/Claude/`
- **Windows**: `%APPDATA%\Claude\logs`

View logs:
```bash
# macOS/Linux
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log

# Windows
type "%APPDATA%\Claude\logs\mcp*.log"
```

## Transport Mechanisms

### stdio Transport
- For local process communication
- Uses standard input/output streams
- Messages delimited by newlines
- Best for subprocess-based servers

### Streamable HTTP Transport
- For remote server communication
- Client sends HTTP POST for messages
- Server responds with JSON or SSE stream
- Supports session management and resumability
- Requires `MCP-Protocol-Version` header

### Security for HTTP
- Validate Origin header (prevent DNS rebinding attacks)
- Bind to localhost for local servers
- Implement proper authentication
- Use HTTPS in production

## Authorization Framework

MCP uses OAuth 2.1 for authorization:

### Key Requirements
- Servers are OAuth 2.1 resource servers
- Clients implement Dynamic Client Registration (RFC 7591)
- MUST use Resource Indicators (RFC 8707) to prevent token passthrough
- Protected Resource Metadata (RFC 9728) for discovery
- PKCE required for all authorization flows

### Security Best Practices
- Validate access token audience
- Use Authorization Bearer header (not query string)
- Short-lived access tokens
- Never request credentials through elicitation
- Implement HTTPS for all authorization endpoints

## Advanced Features

### Sampling
Allows servers to request LLM completions through the client.

**Use cases:**
- Recursive analysis within tools
- Multi-step reasoning
- Code generation within servers

**Key parameters:**
- Messages: Conversation history
- Model preferences: Hints and priorities (intelligence, speed, cost)
- System prompt: Behavior instructions
- Max tokens: Response length limit

### Elicitation
Enables servers to request specific information from users.

**Use cases:**
- Initial setup and configuration
- Dynamic workflows requiring context
- Collecting user preferences

**Important:** Never request passwords, API keys, or sensitive credentials

### Roots
Define filesystem boundaries for server operations.

**Structure:**
- MUST be file:// URIs
- Optional human-readable names
- Clients can notify servers when roots change

## Development Tools

### MCP Inspector
Interactive debugging tool for testing servers.

**Usage:**
```bash
# Inspect npm package
npx @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /path

# Inspect PyPI package
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/repo

# Inspect local Node.js server
npx @modelcontextprotocol/inspector node path/to/server/index.js

# Inspect local Python server
npx @modelcontextprotocol/inspector uv --directory path/to/server run package-name
```

**Features:**
- Resource browsing and content inspection
- Prompt testing with custom arguments
- Tool execution with custom inputs
- Real-time notifications and logging

### Claude Desktop DevTools

Enable DevTools:
```bash
echo '{"allowDevTools": true}' > ~/Library/Application\ Support/Claude/developer_settings.json
```

Open: `Command-Option-Shift-i`

## Common Issues and Solutions

### Working Directory
- May be undefined (`/` on macOS)
- Always use absolute paths in configuration

### Environment Variables
- Servers inherit only USER, HOME, PATH
- Override with `env` key in configuration

### Server Initialization Issues
Common problems:
- Incorrect paths or missing files
- Invalid JSON configuration
- Missing environment variables
- Permission issues

### Connection Problems
Debugging steps:
1. Check Claude Desktop logs
2. Verify server process is running
3. Test standalone with Inspector
4. Verify protocol compatibility

## SDKs Available

Official SDKs with full protocol support:
- TypeScript
- Python
- Java
- Go
- Kotlin
- Swift
- C#
- Ruby
- Rust
- PHP

All SDKs provide:
- Creating servers and clients
- Local and remote transport support
- Type-safe protocol compliance
- Tool, resource, and prompt management

## Protocol Versioning

MCP uses date-based versions (YYYY-MM-DD):
- **2024-11-05**: First documented version
- **2025-03-26**: Added authorization, Streamable HTTP, tool annotations
- **2025-06-18**: Current version - structured tool output, elicitation, resource links
- **Draft**: Future enhancements with icons, OpenID Connect

## Best Practices

### For Server Developers
1. Provide clear tool/resource/prompt names and descriptions
2. Use detailed JSON Schema definitions
3. Implement proper error handling (report errors in results, not as protocol errors)
4. Use progress reporting for long operations
5. Keep operations focused and atomic
6. Validate all parameters against schema
7. Implement timeouts and rate limiting
8. Never expose internal errors to clients

### For Client Developers
1. List tools from all connected servers
2. Pass tools to LLM with proper schemas
3. Execute tool calls through appropriate servers
4. Return results to LLM for response generation
5. Wrap operations in try-catch blocks
6. Provide meaningful error messages
7. Handle server disconnections gracefully
8. Store API keys securely

### For Security
1. User consent for data access and tool invocation
2. Input validation at every layer
3. Access controls and rate limiting
4. No token passthrough (validate audience)
5. Secure session ID generation
6. Origin header validation for HTTP
7. Human-in-the-loop for tools and sampling
8. Clear UI for security-relevant operations

## Multi-Server Workflows

MCP enables powerful workflows by combining multiple servers:

**Example: Travel Planning**
1. Travel server: Handles flights, hotels, itineraries
2. Weather server: Provides climate forecasts
3. Calendar server: Manages schedules and availability

AI reads resources from multiple servers, executes tools across servers, and combines results into coherent responses.

## Reference Materials

For detailed information on specific topics, refer to the condensed summaries in the `references/` folder:

- `about/`: MCP overview and ecosystem
- `community/`: Governance, contribution guidelines, SEPs
- `development/`: Roadmap and upcoming features
- `docs/`: Complete documentation (architecture, tutorials, examples)
- `legacy/`: Legacy documentation for older patterns
- `sdk/`: Java SDK comprehensive guide
- `specification/`: Complete protocol specification
- `tutorials/`: Building servers and clients step-by-step

## Getting Help

- GitHub Issues: Report bugs and feature requests
- GitHub Discussions: Ask questions and share knowledge
- Official Documentation: https://modelcontextprotocol.io
- MCP Inspector: Test and debug servers locally

## Summary

MCP provides a comprehensive, standardized framework for connecting AI applications with external context and capabilities. It emphasizes security through OAuth 2.1, simplicity in server implementation, composability through multiple servers, and flexibility with progressive feature adoption. Whether building servers to expose data, creating clients to consume services, or integrating existing applications, MCP offers the foundation for creating powerful, context-aware AI applications.
