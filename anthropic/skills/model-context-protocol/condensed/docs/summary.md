# Model Context Protocol (MCP) Documentation Summary

This comprehensive summary covers the complete MCP documentation, organized by topic areas. The documentation provides extensive guidance for understanding, implementing, and deploying MCP servers and clients.

---

## 1. Introduction & Core Concepts

### What is MCP?

MCP (Model Context Protocol) is an open-source standard for connecting AI applications to external systems. It functions like a "USB-C port for AI applications," providing a standardized way to connect AI models to data sources, tools, and workflows.

**Key Benefits:**
- **For Developers**: Reduces development time and complexity when building or integrating with AI applications
- **For AI Applications**: Provides access to an ecosystem of data sources, tools, and apps
- **For End-Users**: Results in more capable AI applications that can access data and take actions on their behalf

**Example Use Cases:**
- Agents accessing Google Calendar and Notion for personalized assistance
- Claude Code generating web apps using Figma designs
- Enterprise chatbots connecting to multiple databases for data analysis
- AI models creating 3D designs on Blender and controlling 3D printers

### Architecture Overview

MCP follows a **client-server architecture** with three key participants:

1. **MCP Host**: The AI application that coordinates and manages multiple MCP clients (e.g., Claude Desktop, Visual Studio Code)
2. **MCP Client**: A component that maintains a one-to-one connection to an MCP server and obtains context for the host
3. **MCP Server**: A program that provides context to MCP clients

**Important Note**: MCP servers can run locally (using STDIO transport) or remotely (using Streamable HTTP transport). The term "server" refers to the program's role, not its location.

### Protocol Layers

MCP consists of two main layers:

#### Data Layer
- Implements JSON-RPC 2.0 based protocol for client-server communication
- Handles lifecycle management (connection initialization, capability negotiation, termination)
- Defines core primitives: tools, resources, prompts, and notifications
- Supports client features: sampling, elicitation, and logging

#### Transport Layer
- Manages communication channels and authentication
- Supports two mechanisms:
  - **STDIO Transport**: Uses standard input/output for local process communication
  - **Streamable HTTP Transport**: Uses HTTP POST with optional Server-Sent Events for remote communication

---

## 2. Server Concepts & Primitives

MCP servers expose functionality through three main building blocks:

### Tools (Model-Controlled)

**Definition**: Functions that AI models can actively call to perform actions.

**Key Features:**
- Schema-defined interfaces using JSON Schema validation
- Each tool performs a single operation with typed inputs/outputs
- Model decides when to use them based on user requests
- May require user consent before execution

**Protocol Operations:**
- `tools/list`: Discover available tools (returns array of tool definitions with schemas)
- `tools/call`: Execute a specific tool (returns tool execution result)

**Example Tool Definition:**
```typescript
{
  name: "searchFlights",
  description: "Search for available flights",
  inputSchema: {
    type: "object",
    properties: {
      origin: { type: "string", description: "Departure city" },
      destination: { type: "string", description: "Arrival city" },
      date: { type: "string", format: "date", description: "Travel date" }
    },
    required: ["origin", "destination", "date"]
  }
}
```

**User Interaction Model:**
- Applications can display available tools in UI
- Approval dialogs for individual tool executions
- Permission settings for pre-approving safe operations
- Activity logs showing all tool executions with results

### Resources (Application-Controlled)

**Definition**: Passive data sources that provide read-only access to information for context.

**Key Features:**
- Each resource has a unique URI and MIME type
- Supports two discovery patterns:
  - **Direct Resources**: Fixed URIs pointing to specific data
  - **Resource Templates**: Dynamic URIs with parameters for flexible queries

**Protocol Operations:**
- `resources/list`: List available direct resources
- `resources/templates/list`: Discover resource templates
- `resources/read`: Retrieve resource contents
- `resources/subscribe`: Monitor resource changes

**Resource Template Example:**
```json
{
  "uriTemplate": "weather://forecast/{city}/{date}",
  "name": "weather-forecast",
  "title": "Weather Forecast",
  "description": "Get weather forecast for any city and date",
  "mimeType": "application/json"
}
```

**Parameter Completion**: Supports auto-suggestion for template parameters (e.g., typing "Par" suggests "Paris" or "Park City").

**User Interaction Model:**
- Tree or list views for browsing resources
- Search and filter interfaces
- Automatic context inclusion or smart suggestions
- Manual or bulk selection interfaces

### Prompts (User-Controlled)

**Definition**: Reusable templates that help structure interactions with language models.

**Key Features:**
- Structured templates defining expected inputs and interaction patterns
- Require explicit user invocation (not automatic)
- Can be context-aware, referencing available resources and tools
- Support parameter completion for discovering valid argument values

**Protocol Operations:**
- `prompts/list`: Discover available prompts
- `prompts/get`: Retrieve prompt details

**Example Prompt:**
```json
{
  "name": "plan-vacation",
  "title": "Plan a vacation",
  "description": "Guide through vacation planning process",
  "arguments": [
    { "name": "destination", "type": "string", "required": true },
    { "name": "duration", "type": "number", "description": "days" },
    { "name": "budget", "type": "number", "required": false },
    { "name": "interests", "type": "array", "items": { "type": "string" } }
  ]
}
```

**User Interaction Model:**
- Slash commands (e.g., typing "/" to see available prompts)
- Command palettes for searchable access
- Dedicated UI buttons for frequently used prompts
- Context menus suggesting relevant prompts

### Notifications

MCP supports real-time notifications for dynamic updates. Servers can inform clients about changes without explicit requests.

**Example Notification Flow:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

**Key Features:**
- No response required (JSON-RPC 2.0 notification semantics)
- Capability-based (only sent if declared during initialization)
- Event-driven (server decides when to send based on state changes)
- Enables dynamic environments where tools/resources come and go

---

## 3. Client Concepts & Features

MCP clients are instantiated by host applications to communicate with MCP servers. Understanding the distinction is important: the **host** is the application users interact with, while **clients** are protocol-level components enabling server connections.

### Core Client Features

#### Sampling

**Purpose**: Allows servers to request LLM completions through the client, enabling agentic workflows.

**Key Features:**
- Server requests AI assistance without directly integrating with AI models
- Client maintains complete control over user permissions and security
- Supports human-in-the-loop review at multiple checkpoints

**Sampling Flow:**
1. Server initiates `sampling/createMessage` request
2. Client presents request for user approval
3. User reviews and approves/modifies the request
4. Client forwards to LLM and receives response
5. Client presents response for user approval
6. User reviews and approves/modifies response
7. Client returns approved response to server

**Example Use Case**: A flight analysis tool queries 47 flights and requests AI assistance to analyze options based on user preferences (morning departure, max 1 layover), evaluating complex trade-offs.

**Request Parameters Example:**
```typescript
{
  messages: [{
    role: "user",
    content: "Analyze these flight options and recommend the best choice..."
  }],
  modelPreferences: {
    hints: [{ name: "claude-3-5-sonnet" }],
    costPriority: 0.3,
    speedPriority: 0.2,
    intelligencePriority: 0.9
  },
  systemPrompt: "You are a travel expert...",
  maxTokens: 1500
}
```

#### Roots

**Purpose**: Define filesystem boundaries for server operations, allowing clients to specify which directories servers should focus on.

**Key Features:**
- Exclusively filesystem paths using `file://` URI scheme
- Coordination mechanism (not security boundary)
- Helps servers understand project boundaries and accessible directories
- List can be updated dynamically with `roots/list_changed` notifications

**Root Structure:**
```json
{
  "uri": "file:///Users/agent/travel-planning",
  "name": "Travel Planning Workspace"
}
```

**Design Philosophy:**
- Roots serve as coordination, not security enforcement
- Specification requires servers "SHOULD respect" (not "MUST enforce")
- Works best when servers are trusted or vetted
- Prevents accidents rather than stopping malicious behavior

**Example Use Case**: A travel agent working with multiple client trips benefits from roots to organize filesystem access across different directories for travel files, templates, and client documents.

#### Elicitation

**Purpose**: Enables servers to request specific information from users during interactions, creating dynamic and responsive workflows.

**Key Features:**
- Structured way for servers to gather necessary information on demand
- Servers can pause operations to request specific inputs
- Creates flexible interactions adapting to user needs

**Elicitation Flow:**
1. Server initiates `elicitation/create` request
2. Client presents elicitation UI to user
3. User provides requested information
4. Client returns user response to server
5. Server continues processing with new information

**Example Components:**
```typescript
{
  method: "elicitation/requestInput",
  params: {
    message: "Please confirm your Barcelona vacation booking details:",
    schema: {
      type: "object",
      properties: {
        confirmBooking: { type: "boolean", description: "Confirm the booking" },
        seatPreference: { type: "string", enum: ["window", "aisle", "no preference"] },
        roomType: { type: "string", enum: ["sea view", "city view", "garden view"] },
        travelInsurance: { type: "boolean", default: false }
      },
      required: ["confirmBooking"]
    }
  }
}
```

**User Interaction Model:**
- Clear context about which server is asking and why
- Users can provide information, decline, or cancel the operation
- Clients validate responses against provided schema
- Privacy considerations: Never requests passwords or API keys

---

## 4. Lifecycle Management & Protocol Details

### Initialization Sequence

MCP is a stateful protocol requiring lifecycle management for capability negotiation.

**Initialization Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "elicitation": {}
    },
    "clientInfo": {
      "name": "example-client",
      "version": "1.0.0"
    }
  }
}
```

**Initialization Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": {}
    },
    "serverInfo": {
      "name": "example-server",
      "version": "1.0.0"
    }
  }
}
```

**Key Purposes:**
1. **Protocol Version Negotiation**: Ensures compatibility between client and server
2. **Capability Discovery**: Each party declares supported features (tools, resources, prompts, notifications)
3. **Identity Exchange**: Provides identification and versioning for debugging

**After Initialization:**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

### Complete Tool Execution Flow

**1. Tool Discovery:**
```json
// Request
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}

// Response (shows two example tools)
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "calculator_arithmetic",
        "title": "Calculator",
        "description": "Perform mathematical calculations",
        "inputSchema": {
          "type": "object",
          "properties": {
            "expression": {
              "type": "string",
              "description": "Mathematical expression to evaluate"
            }
          },
          "required": ["expression"]
        }
      },
      {
        "name": "weather_current",
        "title": "Weather Information",
        "description": "Get current weather information",
        "inputSchema": {
          "type": "object",
          "properties": {
            "location": { "type": "string" },
            "units": {
              "type": "string",
              "enum": ["metric", "imperial", "kelvin"],
              "default": "metric"
            }
          },
          "required": ["location"]
        }
      }
    ]
  }
}
```

**2. Tool Execution:**
```json
// Request
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "weather_current",
    "arguments": {
      "location": "San Francisco",
      "units": "imperial"
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Current weather in San Francisco: 68°F, partly cloudy..."
      }
    ]
  }
}
```

**3. Dynamic Updates (Notifications):**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

Upon receiving this notification, clients typically request the updated tool list using `tools/list`.

---

## 5. SDK Information

MCP provides official SDKs for multiple programming languages, all offering the same core functionality and full protocol support:

**Available SDKs:**
- TypeScript
- Python
- Go
- Kotlin
- Swift
- Java
- C#
- Ruby
- Rust
- PHP

**Common Features Across All SDKs:**
- Creating MCP servers that expose tools, resources, and prompts
- Building MCP clients that can connect to any MCP server
- Local and remote transport protocols
- Protocol compliance with type safety

Each SDK follows the idioms and best practices of its language while maintaining consistent functionality.

---

## 6. Building MCP Servers

### Core Server Implementation Pattern

The documentation provides comprehensive tutorials for building servers in multiple languages (Python, TypeScript, Java, Kotlin, C#). All implementations follow similar patterns:

**Essential Components:**
1. Server initialization with capabilities declaration
2. Helper functions for external API calls
3. Tool/resource/prompt registration
4. Transport setup (STDIO or HTTP)
5. Main execution loop

### Python Example (FastMCP)

**Setup:**
```python
from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("weather")
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"
```

**Tool Definition:**
```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.
    
    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)
    
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    
    if not data["features"]:
        return "No active alerts for this state."
    
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)
```

**Running the Server:**
```python
def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
```

### TypeScript Example

**Setup:**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "weather",
  version: "1.0.0",
  capabilities: {
    resources: {},
    tools: {},
  },
});
```

**Tool Registration:**
```typescript
server.tool(
  "get_alerts",
  "Get weather alerts for a state",
  {
    state: z.string().length(2).describe("Two-letter state code"),
  },
  async ({ state }) => {
    const stateCode = state.toUpperCase();
    const alertsUrl = `${NWS_API_BASE}/alerts?area=${stateCode}`;
    const alertsData = await makeNWSRequest<AlertsResponse>(alertsUrl);
    
    if (!alertsData) {
      return {
        content: [{ type: "text", text: "Failed to retrieve alerts data" }]
      };
    }
    
    // Format and return results...
  }
);
```

**Running the Server:**
```typescript
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
```

### Important Logging Guidelines

**For STDIO-based servers:**
- **NEVER** write to standard output (stdout)
- Avoid `print()` in Python, `console.log()` in JavaScript, `fmt.Println()` in Go
- Writing to stdout corrupts JSON-RPC messages and breaks the server
- Use logging libraries that write to stderr or files

**For HTTP-based servers:**
- Standard output logging is fine (doesn't interfere with HTTP responses)

**Best Practices:**
1. Use logging libraries (e.g., `logging` in Python)
2. Tool names should follow the specified format
3. For JavaScript, use `console.error()` instead of `console.log()`

### Testing with Claude for Desktop

**Configuration File Location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Example Configuration (Python):**
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**Example Configuration (TypeScript):**
```json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather/build/index.js"]
    }
  }
}
```

**Important Notes:**
- Use absolute paths (not relative)
- On Windows, use double backslashes (`\\`) or forward slashes (`/`)
- Restart Claude Desktop after configuration changes
- Verify using the tools icon in Claude Desktop interface

---

## 7. Building MCP Clients

### Client Architecture

MCP clients connect to servers to access tools, resources, and prompts. The documentation provides comprehensive examples in Python, TypeScript, Java, Kotlin, and C#.

**Core Client Components:**
1. Client initialization and session management
2. Server connection handling
3. Query processing with tool execution
4. Interactive interface (CLI, GUI, or API)
5. Resource cleanup

### Python Client Example

**Basic Structure:**
```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
```

**Server Connection:**
```python
async def connect_to_server(self, server_script_path: str):
    is_python = server_script_path.endswith('.py')
    is_js = server_script_path.endswith('.js')
    
    command = "python" if is_python else "node"
    server_params = StdioServerParameters(
        command=command,
        args=[server_script_path],
        env=None
    )
    
    stdio_transport = await self.exit_stack.enter_async_context(
        stdio_client(server_params)
    )
    self.stdio, self.write = stdio_transport
    self.session = await self.exit_stack.enter_async_context(
        ClientSession(self.stdio, self.write)
    )
    
    await self.session.initialize()
    
    response = await self.session.list_tools()
    tools = response.tools
    print("Connected to server with tools:", [tool.name for tool in tools])
```

**Query Processing:**
```python
async def process_query(self, query: str) -> str:
    messages = [{"role": "user", "content": query}]
    
    response = await self.session.list_tools()
    available_tools = [{
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.inputSchema
    } for tool in response.tools]
    
    # Call Claude API with tools
    response = self.anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=messages,
        tools=available_tools
    )
    
    # Process tool calls and collect results
    final_text = []
    for content in response.content:
        if content.type == 'text':
            final_text.append(content.text)
        elif content.type == 'tool_use':
            result = await self.session.call_tool(
                content.name, 
                content.input
            )
            final_text.append(f"[Calling tool {content.name}]")
            # Send result back to Claude for final response...
    
    return "\n".join(final_text)
```

**Interactive Loop:**
```python
async def chat_loop(self):
    print("MCP Client Started!")
    print("Type your queries or 'quit' to exit.")
    
    while True:
        query = input("\nQuery: ").strip()
        if query.lower() == 'quit':
            break
        
        response = await self.process_query(query)
        print("\n" + response)
```

### TypeScript Client Example

**Basic Structure:**
```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
import { Anthropic } from "@anthropic-ai/sdk";

class MCPClient {
  private mcp: Client;
  private anthropic: Anthropic;
  private transport: StdioClientTransport | null = null;
  private tools: Tool[] = [];
  
  constructor() {
    this.anthropic = new Anthropic({ apiKey: ANTHROPIC_API_KEY });
    this.mcp = new Client({ name: "mcp-client-cli", version: "1.0.0" });
  }
}
```

**Server Connection:**
```typescript
async connectToServer(serverScriptPath: string) {
  const isPy = serverScriptPath.endsWith(".py");
  const isJs = serverScriptPath.endsWith(".js");
  
  const command = isPy 
    ? (process.platform === "win32" ? "python" : "python3")
    : process.execPath;
  
  this.transport = new StdioClientTransport({
    command,
    args: [serverScriptPath],
  });
  
  await this.mcp.connect(this.transport);
  
  const toolsResult = await this.mcp.listTools();
  this.tools = toolsResult.tools.map((tool) => ({
    name: tool.name,
    description: tool.description,
    input_schema: tool.inputSchema,
  }));
  
  console.log("Connected to server with tools:", 
    this.tools.map(({ name }) => name));
}
```

### How Client-Server Communication Works

When you submit a query:

1. Client gets the list of available tools from the server
2. Query is sent to Claude (or another LLM) along with tool descriptions
3. LLM decides which tools (if any) to use
4. Client executes requested tool calls through the server
5. Results are sent back to the LLM
6. LLM provides a natural language response
7. Response is displayed to the user

### Best Practices for Clients

**Error Handling:**
- Always wrap tool calls in try-catch blocks
- Provide meaningful error messages
- Gracefully handle connection issues

**Resource Management:**
- Use `AsyncExitStack` (Python) or proper cleanup patterns
- Close connections when done
- Handle server disconnections

**Security:**
- Store API keys securely in `.env` files
- Validate server responses
- Be cautious with tool permissions

**Tool Names:**
- Validate according to MCP specification format
- If a tool name conforms to the format, it should not fail validation

### Troubleshooting

**Server Path Issues:**
- Double-check the path to server script
- Use absolute paths if relative paths fail
- On Windows, use forward slashes or escaped backslashes
- Verify correct file extension (.py, .js, .jar)

**Response Timing:**
- First response might take up to 30 seconds
- Normal during server initialization, Claude processing, and tool execution
- Subsequent responses are typically faster

**Common Error Messages:**
- `FileNotFoundError`: Check server path
- `Connection refused`: Ensure server is running
- `Tool execution failed`: Verify required environment variables
- `Timeout error`: Consider increasing timeout configuration

---

## 8. Connection Guides

### Connecting to Local MCP Servers

Local MCP servers run on your computer and provide controlled access to local resources. The guide demonstrates using Claude Desktop as an example.

**Prerequisites:**
- Claude Desktop (latest version)
- Node.js (for most MCP servers)

**Installation Steps:**

1. **Open Claude Desktop Settings**
   - Click Claude menu in system menu bar
   - Select "Settings..."

2. **Access Developer Settings**
   - Navigate to "Developer" tab
   - Click "Edit Config" button

3. **Configure Filesystem Server Example:**

macOS Configuration:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

Windows Configuration:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\username\\Desktop",
        "C:\\Users\\username\\Downloads"
      ]
    }
  }
}
```

**Understanding the Configuration:**
- `"filesystem"`: Friendly name for the server
- `"command": "npx"`: Uses Node.js's npx tool
- `"-y"`: Auto-confirms package installation
- `"@modelcontextprotocol/server-filesystem"`: Package name
- Remaining arguments: Directories the server can access

**Security Consideration:**
Only grant access to directories you're comfortable with Claude reading and modifying. The server runs with your user permissions.

4. **Restart Claude Desktop**
   - Completely quit and restart
   - Look for MCP server indicator in bottom-right corner
   - Click indicator to view available tools

**Using the Filesystem Server:**

Example requests:
- "Can you write a poem and save it to my desktop?"
- "What work-related files are in my downloads folder?"
- "Please organize all images on my desktop into a new folder called 'Images'"

**Approval Process:**
Before executing any file system operation, Claude requests your approval. Review each request carefully before approving.

**Troubleshooting:**

**Logs Location:**
- macOS: `~/Library/Logs/Claude`
- Windows: `%APPDATA%\Claude\logs`

**Log Files:**
- `mcp.log`: General MCP connection logging
- `mcp-server-SERVERNAME.log`: Error logging from named server

**View Recent Logs (macOS/Linux):**
```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp*.log
```

**View Recent Logs (Windows):**
```powershell
type "%APPDATA%\Claude\logs\mcp*.log"
```

**Common Issues:**
1. Server not showing up: Check config syntax, use absolute paths, restart Claude
2. Tool calls failing: Check logs, verify server runs without errors
3. ENOENT error on Windows: Add expanded `%APPDATA%` value to `env` key

### Connecting to Remote MCP Servers

Remote MCP servers are hosted on the internet and accessible from any MCP client with an internet connection.

**Key Advantages:**
- No local installation required
- Accessible from any device
- Ideal for web-based AI applications
- Suitable for services requiring server-side processing

**Custom Connectors:**
Custom Connectors bridge Claude and remote MCP servers, enabling:
- Connection to existing remote MCP servers
- Building custom remote MCP servers for any tool

**Connection Steps:**

1. **Navigate to Connector Settings**
   - Open Claude in browser
   - Click profile icon → "Settings"
   - Select "Connectors" section

2. **Add Custom Connector**
   - Scroll to "Add custom connector" button
   - Enter remote MCP server URL (include https://)
   - Click "Add"

3. **Complete Authentication**
   - Follow authentication prompts (OAuth, API keys, etc.)
   - Authentication varies by server implementation
   - May redirect to third-party authentication provider

4. **Access Resources and Prompts**
   - Click paperclip icon in message input
   - View all available resources and prompts
   - Select items to include in conversation

5. **Configure Tool Permissions**
   - Navigate to Connectors settings
   - Click on connected server
   - Enable/disable specific tools
   - Set usage limits and security parameters

**Best Practices:**

**Security:**
- Verify authenticity of remote MCP servers before connecting
- Only connect to servers from trusted sources
- Review permissions during authentication
- Be cautious about granting access to sensitive data

**Managing Multiple Connectors:**
- Organize connectors by purpose or project
- Regularly review and remove unused connectors
- Maintain workspace clarity and security

---

## 9. Development Tools

### MCP Inspector

The MCP Inspector is an interactive developer tool for testing and debugging MCP servers.

**Installation and Basic Usage:**

The Inspector runs directly through `npx` without installation:
```bash
npx @modelcontextprotocol/inspector <command>
```

**Inspecting npm or PyPI Servers:**

npm packages:
```bash
npx -y @modelcontextprotocol/inspector npx <package-name> <args>

# Example:
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem /Users/username/Desktop
```

PyPI packages:
```bash
npx @modelcontextprotocol/inspector uvx <package-name> <args>

# Example:
npx @modelcontextprotocol/inspector uvx mcp-server-git --repository ~/code/mcp/servers.git
```

**Inspecting Locally Developed Servers:**

Node.js servers:
```bash
npx @modelcontextprotocol/inspector node path/to/server/index.js args...
```

Python servers:
```bash
npx @modelcontextprotocol/inspector \
  uv \
  --directory path/to/server \
  run \
  package-name \
  args...
```

**Feature Overview:**

**Server Connection Pane:**
- Select transport for connecting to server
- Customize command-line arguments and environment for local servers

**Resources Tab:**
- Lists all available resources
- Shows resource metadata (MIME types, descriptions)
- Allows resource content inspection
- Supports subscription testing

**Prompts Tab:**
- Displays available prompt templates
- Shows prompt arguments and descriptions
- Enables prompt testing with custom arguments
- Previews generated messages

**Tools Tab:**
- Lists available tools
- Shows tool schemas and descriptions
- Enables tool testing with custom inputs
- Displays tool execution results

**Notifications Pane:**
- Presents all logs recorded from server
- Shows notifications received from server

**Development Workflow:**

1. **Start Development**
   - Launch Inspector with server
   - Verify basic connectivity
   - Check capability negotiation

2. **Iterative Testing**
   - Make server changes
   - Rebuild server
   - Reconnect Inspector
   - Test affected features
   - Monitor messages

3. **Test Edge Cases**
   - Invalid inputs
   - Missing prompt arguments
   - Concurrent operations
   - Verify error handling and responses

---

## 10. Security: Authorization in MCP

Authorization in MCP secures access to sensitive resources and operations. While **optional**, it's strongly recommended for servers handling user data or administrative actions.

### When to Use Authorization

Authorization is recommended when:
- Server accesses user-specific data (emails, documents, databases)
- Auditing who performed which actions is needed
- Server grants access to APIs requiring user consent
- Building for enterprise environments with strict access controls
- Implementing rate limiting or usage tracking per user

**Note on Local Servers:**
For STDIO-based servers, you can use environment-based credentials or third-party libraries instead of OAuth flows. STDIO servers run locally with access to flexible credential options.

OAuth flows are designed for HTTP-based transports where servers are remotely hosted and clients use OAuth to establish authorization.

### Authorization Flow

**1. Initial Handshake**

Server responds with `401 Unauthorized` and points to authorization metadata:
```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="mcp",
  resource_metadata="https://your-server.com/.well-known/oauth-protected-resource"
```

**2. Protected Resource Metadata Discovery**

Client fetches PRM document to learn about authorization server and scopes:
```json
{
  "resource": "https://your-server.com/mcp",
  "authorization_servers": ["https://auth.your-server.com"],
  "scopes_supported": ["mcp:tools", "mcp:resources"]
}
```

**3. Authorization Server Discovery**

Client discovers authorization server capabilities:
```json
{
  "issuer": "https://auth.your-server.com",
  "authorization_endpoint": "https://auth.your-server.com/authorize",
  "token_endpoint": "https://auth.your-server.com/token",
  "registration_endpoint": "https://auth.your-server.com/register"
}
```

**4. Client Registration**

Two options:
- **Pre-registration**: Client has embedded registration information
- **Dynamic Client Registration (DCR)**: Client registers dynamically

DCR Request:
```json
{
  "client_name": "My MCP Client",
  "redirect_uris": ["http://localhost:3000/callback"],
  "grant_types": ["authorization_code", "refresh_token"],
  "response_types": ["code"]
}
```

**5. User Authorization**

Client opens browser to `/authorize` endpoint. After user login and permission grant, authorization server redirects with authorization code.

Token exchange response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "def502...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**6. Making Authenticated Requests**

Client includes access token in requests:
```http
GET /mcp HTTP/1.1
Host: your-server.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
```

Server validates token and processes request if valid.

### Implementation Example with Keycloak

The documentation provides comprehensive examples in TypeScript, Python, and C# using Keycloak as the authorization server.

**Keycloak Setup:**

Start Keycloak container:
```bash
docker run -p 127.0.0.1:8080:8080 \
  -e KC_BOOTSTRAP_ADMIN_USERNAME=admin \
  -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak start-dev
```

**Configuration Steps:**
1. Create `mcp:tools` scope
2. Set scope type to "Default" and enable "Include in token scope"
3. Configure audience mapper for token validation
4. Add trusted hosts for client registration
5. Register MCP server client for token introspection

**Key Configuration Points:**

**Scope Configuration:**
- Create custom scopes (e.g., `mcp:tools`)
- Include in token scope for validation
- Assign to clients as needed

**Audience Configuration:**
- Embed intended destination in access token
- Helps avoid token passthrough scenarios
- Verify token was meant for your server

**Environment Variables (.env file):**
```env
HOST=localhost
PORT=3000
AUTH_HOST=localhost
AUTH_PORT=8080
AUTH_REALM=master
OAUTH_CLIENT_ID=<YOUR_SERVER_CLIENT_ID>
OAUTH_CLIENT_SECRET=<YOUR_SERVER_CLIENT_SECRET>
```

### TypeScript Server Example

The documentation includes a complete TypeScript MCP server with:
- Token introspection via Keycloak
- OAuth metadata endpoints
- Bearer authentication middleware
- Tool registration (addition and multiplication examples)
- Session management

**Key Components:**
- `mcpAuthMetadataRouter`: Provides OAuth metadata endpoints
- `requireBearerAuth`: Middleware for token validation
- `checkResourceAllowed`: Validates audience in tokens
- `tokenVerifier`: Performs introspection and validation

### Python Server Example

Uses FastMCP for simplified authorization integration:
- Configuration management
- Token introspection verification
- OAuth URL generation
- Tool registration with authentication

**Token Verification:**
Implements `IntrospectionTokenVerifier` class:
- Validates tokens via introspection endpoint
- Checks resource/audience claims
- Ensures tokens are active and valid

### C# Server Example

Uses ASP.NET Core with JWT Bearer authentication:
- JWT validation configuration
- Audience validation
- MCP authentication scheme integration
- Tool registration with authorization

**Key Features:**
- Built-in ASP.NET Core token validation
- Custom audience validator
- Event handlers for logging
- Integration with MCP server framework

### Security Best Practices

**Critical Recommendations:**

1. **Use Well-Tested Libraries**: Never implement token validation or authorization logic from scratch
2. **Short-Lived Access Tokens**: Limit token lifetime to reduce risk from stolen credentials
3. **Always Validate Tokens**: Verify token validity and intended audience
4. **Secure Token Storage**: Use encrypted storage with proper access controls
5. **Enforce HTTPS in Production**: Don't accept tokens over plain HTTP (except localhost during development)
6. **Least-Privilege Scopes**: Split access per tool/capability, avoid catch-all scopes
7. **Don't Log Credentials**: Never log Authorization headers, tokens, codes, or secrets
8. **Separate Credentials**: Don't reuse server client secret for end-user flows
9. **Proper Error Responses**: Return proper `WWW-Authenticate` headers on 401
10. **DCR Controls**: Be aware of constraints for Dynamic Client Registration
11. **Audience/Resource Validation**: Require specific audience matching your server
12. **Minimize Error Detail Leakage**: Return generic messages to clients, log details internally
13. **Session Identifier Hardening**: Treat `Mcp-Session-Id` as untrusted input

### Related Standards

MCP authorization builds on:
- **OAuth 2.1**: Core authorization framework
- **RFC 8414**: Authorization Server Metadata discovery
- **RFC 7591**: Dynamic Client Registration
- **RFC 9728**: Protected Resource Metadata
- **RFC 8707**: Resource Indicators

---

## 11. Complete Multi-Server Example

The documentation includes a comprehensive example demonstrating how multiple servers work together:

**Scenario: Multi-Server Travel Planning**

**Connected Servers:**
1. **Travel Server**: Handles flights, hotels, and itineraries
2. **Weather Server**: Provides climate data and forecasts
3. **Calendar/Email Server**: Manages schedules and communications

**Complete Flow:**

**Step 1: User Invokes Prompt**
```json
{
  "prompt": "plan-vacation",
  "arguments": {
    "destination": "Barcelona",
    "departure_date": "2024-06-15",
    "return_date": "2024-06-22",
    "budget": 3000,
    "travelers": 2
  }
}
```

**Step 2: User Selects Resources**
- `calendar://my-calendar/June-2024` (from Calendar Server)
- `travel://preferences/europe` (from Travel Server)
- `travel://past-trips/Spain-2023` (from Travel Server)

**Step 3: AI Processes with Tools**

AI reads selected resources to gather context:
- Identifies available dates from calendar
- Learns preferred airlines and hotel types
- Discovers previously enjoyed locations

AI then executes series of Tools:
- `searchFlights()`: Queries airlines for NYC to Barcelona
- `checkWeather()`: Retrieves climate forecasts for travel dates
- `bookHotel()`: Finds hotels within budget
- `createCalendarEvent()`: Adds trip to user's calendar
- `sendEmail()`: Sends confirmation with trip details

**Result:**
Through multiple MCP servers, the user researched and booked a Barcelona trip tailored to their schedule. The "Plan a Vacation" prompt guided the AI to combine Resources (calendar availability and travel history) with Tools (searching flights, booking hotels, updating calendars) across different servers.

---

## 12. Tutorials

### Use Local MCP Server Tutorial

This tutorial appears as a placeholder ("todo") in the documentation, suggesting it's under development. Based on the pattern of other documentation, it would likely cover:
- Step-by-step setup of a local MCP server
- Configuration with a local client
- Testing and verification
- Common troubleshooting scenarios

---

## 13. Key Takeaways

### For Server Developers

1. **Choose the Right Primitives**: 
   - Use **Tools** for actions the model decides to take
   - Use **Resources** for contextual information the application controls
   - Use **Prompts** for user-initiated templates

2. **Implement Proper Logging**:
   - Never write to stdout for STDIO servers
   - Use stderr or file-based logging
   - Follow language-specific best practices

3. **Consider Authorization**:
   - Required for user-specific data or sensitive operations
   - Use OAuth 2.1 flows for remote servers
   - Consider environment-based credentials for local servers

4. **Test Thoroughly**:
   - Use MCP Inspector during development
   - Test edge cases and error conditions
   - Verify tool schemas and descriptions are clear

### For Client Developers

1. **Handle Tool Execution Properly**:
   - List available tools from all connected servers
   - Pass tools to LLM with proper schemas
   - Execute tool calls through appropriate servers
   - Return results to LLM for response generation

2. **Implement Robust Error Handling**:
   - Wrap external calls in try-catch blocks
   - Provide meaningful error messages
   - Handle server disconnections gracefully

3. **Manage Resources Carefully**:
   - Use proper cleanup patterns (AsyncExitStack, etc.)
   - Close connections when done
   - Handle multiple server connections efficiently

4. **Prioritize Security**:
   - Store API keys securely
   - Validate all server responses
   - Be cautious with tool permissions
   - Implement proper authentication flows

### For Integration Developers

1. **Understand the Architecture**:
   - MCP uses client-server model with JSON-RPC 2.0
   - Supports STDIO (local) and HTTP (remote) transports
   - Stateful protocol requiring lifecycle management

2. **Leverage Multiple Servers**:
   - Combine specialized servers for powerful workflows
   - Resources from one server can inform tool usage in another
   - Prompts can orchestrate cross-server operations

3. **Follow Standards**:
   - MCP builds on OAuth 2.1, RFC 8414, RFC 7591, RFC 9728, RFC 8707
   - Use standardized discovery mechanisms
   - Implement proper capability negotiation

4. **Plan for Scale**:
   - Design for concurrent server connections
   - Implement efficient resource management
   - Consider caching and rate limiting strategies

---

## 14. Additional Resources

### Official Documentation
- **MCP Specification**: Complete protocol specification at modelcontextprotocol.io
- **SDK Documentation**: Language-specific guides for TypeScript, Python, Go, Kotlin, Swift, Java, C#, Ruby, Rust, PHP
- **Reference Implementations**: Official MCP servers repository on GitHub
- **Inspector Repository**: MCP Inspector source code and documentation

### Community Resources
- **Example Servers**: Gallery of official and community-created MCP servers
- **Example Clients**: List of clients supporting MCP integrations
- **Debugging Guide**: Comprehensive debugging strategies and tools

### Standards References
- OAuth 2.1 (draft-ietf-oauth-v2-1-13)
- RFC 8414: Authorization Server Metadata
- RFC 7591: Dynamic Client Registration
- RFC 9728: Protected Resource Metadata
- RFC 8707: Resource Indicators
- JSON-RPC 2.0 Specification

---

## Conclusion

The Model Context Protocol (MCP) provides a comprehensive, standardized approach to connecting AI applications with external systems. By abstracting the complexity of integrations through a well-defined protocol, MCP enables:

- **Rapid Development**: Reduced time to build AI-powered integrations
- **Interoperability**: Standardized communication between diverse systems
- **Security**: Built-in support for OAuth 2.1 authorization
- **Flexibility**: Support for both local and remote servers across multiple programming languages
- **Scalability**: Multi-server architectures for complex workflows

Whether you're building servers to expose your data and tools, creating clients to consume MCP services, or integrating existing applications, MCP provides the foundation for creating powerful, context-aware AI applications that can access the information and perform the actions needed to assist users effectively.

The documentation provides comprehensive guidance, code examples, and best practices across all aspects of MCP implementation, from basic server creation to advanced authorization flows, making it accessible to developers at all levels of expertise.
