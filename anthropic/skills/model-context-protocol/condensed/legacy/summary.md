# Model Context Protocol (MCP) - Legacy Documentation Summary

This comprehensive summary covers the legacy documentation for the Model Context Protocol (MCP), a flexible architecture enabling seamless communication between LLM applications and integrations.

---

## 1. Core Architecture

### Overview
MCP follows a **client-server architecture** with three key components:

- **Hosts**: LLM applications (like Claude Desktop or IDEs) that initiate connections
- **Clients**: Maintain 1:1 connections with servers inside the host application
- **Servers**: Provide context, tools, and prompts to clients

### Protocol Layer
The protocol layer handles message framing, request/response linking, and high-level communication patterns through key classes:
- `Protocol`: Manages request handlers and notification handlers
- `Client`: Initiates connections and sends requests
- `Server`: Exposes capabilities and responds to requests

Key methods include:
- `setRequestHandler()`: Handle incoming requests
- `setNotificationHandler()`: Handle incoming notifications
- `request()`: Send requests and await responses
- `notification()`: Send one-way notifications

### Transport Layer
Supports multiple transport mechanisms:

1. **Stdio Transport**: Uses standard input/output for local process communication
2. **Streamable HTTP Transport**: Uses HTTP POST for client-to-server messages with optional Server-Sent Events (SSE) for streaming

All transports use **JSON-RPC 2.0** to exchange messages.

### Message Types

1. **Requests**: Expect a response (method, params)
2. **Results**: Successful responses to requests
3. **Errors**: Indicate request failures (code, message, data)
4. **Notifications**: One-way messages without responses

### Connection Lifecycle

**Initialization:**
1. Client sends `initialize` request with protocol version and capabilities
2. Server responds with its protocol version and capabilities
3. Client sends `initialized` notification as acknowledgment
4. Normal message exchange begins

**Message Exchange:**
- Request-Response pattern
- Notifications for one-way communication

**Termination:**
- Clean shutdown via `close()`
- Transport disconnection
- Error conditions

### Error Handling

Standard JSON-RPC error codes:
- ParseError: -32700
- InvalidRequest: -32600
- MethodNotFound: -32601
- InvalidParams: -32602
- InternalError: -32603

Custom error codes can be defined above -32000.

### Security Considerations

1. **Transport Security**: Use TLS for remote connections, validate origins, implement authentication
2. **Message Validation**: Validate all incoming messages, sanitize inputs, check size limits
3. **Resource Protection**: Implement access controls, validate paths, rate limit requests
4. **Error Handling**: Don't leak sensitive information, log security events

---

## 2. Tools

### Overview
Tools are **model-controlled** primitives that enable servers to expose executable functionality to clients. They allow LLMs to interact with external systems, perform computations, and take actions.

### Tool Definition Structure

```typescript
{
  name: string;          // Unique identifier
  description?: string;  // Human-readable description
  inputSchema: {         // JSON Schema for parameters
    type: "object",
    properties: { ... }
  },
  annotations?: {        // Optional behavior hints
    title?: string;
    readOnlyHint?: boolean;
    destructiveHint?: boolean;
    idempotentHint?: boolean;
    openWorldHint?: boolean;
  }
}
```

### Discovery and Invocation

- **Discovery**: Clients send `tools/list` request to get available tools
- **Invocation**: Tools are called via `tools/call` request
- **Updates**: Servers notify clients with `notifications/tools/list_changed`

### Tool Annotations

Tool annotations provide metadata about tool behavior:

- **title**: Human-readable title for UI display
- **readOnlyHint**: Tool doesn't modify its environment
- **destructiveHint**: Tool may perform destructive updates
- **idempotentHint**: Repeated calls with same args have no additional effect
- **openWorldHint**: Tool interacts with external entities

### Tool Patterns

Common tool types include:
- **System Operations**: Execute commands, interact with filesystem
- **API Integrations**: Wrap external APIs (e.g., GitHub, databases)
- **Data Processing**: Transform or analyze data

### Error Handling

Tool errors should be reported **within the result object**, not as protocol-level errors:
- Set `isError: true` in the result
- Include error details in the `content` array
- This allows the LLM to see and potentially handle the error

### Tool Name Conflicts

When multiple servers expose tools with the same name, applications can disambiguate using:
- Concatenating server name: `web1___search_web`
- Random prefixes: `jrwxs___search_web`
- Server URI prefixes: `web1.example.com:search_web`

### Best Practices

1. Provide clear, descriptive names and descriptions
2. Use detailed JSON Schema definitions
3. Include examples in descriptions
4. Implement proper error handling and validation
5. Use progress reporting for long operations
6. Keep operations focused and atomic
7. Document expected return structures
8. Implement timeouts and rate limiting
9. Log tool usage for debugging

### Security

- Validate all parameters against schema
- Sanitize file paths and system commands
- Implement authentication and authorization
- Rate limit requests
- Don't expose internal errors to clients
- Audit tool usage

---

## 3. Prompts

### Overview
Prompts are **user-controlled** reusable templates and workflows that clients can surface to users. They provide standardized LLM interactions.

### Prompt Structure

```typescript
{
  name: string;              // Unique identifier
  description?: string;      // Human-readable description
  arguments?: [              // Optional argument list
    {
      name: string;
      description?: string;
      required?: boolean;
    }
  ]
}
```

### Discovery and Usage

- **Discovery**: `prompts/list` request returns available prompts
- **Usage**: `prompts/get` request with name and arguments returns messages
- **Updates**: `notifications/prompts/list_changed` notifies of changes

### Dynamic Prompts

Prompts can include:

1. **Embedded Resource Context**: Include resources from the server
2. **Multi-step Workflows**: Define conversation flows with assistant messages
3. **Argument Interpolation**: Use dynamic arguments in prompt text

### Response Format

Prompts return a `messages` array containing:
- Role: "user" or "assistant"
- Content: Can be text or resource references

### UI Integration

Prompts can be surfaced as:
- Slash commands
- Quick actions
- Context menu items
- Command palette entries
- Guided workflows
- Interactive forms

### Best Practices

1. Use clear, descriptive prompt names
2. Provide detailed descriptions
3. Validate all required arguments
4. Handle missing arguments gracefully
5. Consider versioning for templates
6. Cache dynamic content when appropriate
7. Implement error handling
8. Test prompts with various inputs

### Security

- Validate all arguments
- Sanitize user input
- Consider rate limiting
- Implement access controls
- Handle sensitive data appropriately
- Consider prompt injection risks

---

## 4. Resources

### Overview
Resources are **application-controlled** primitives that allow servers to expose data and content for LLM context. Different clients may handle resources differently.

### Resource URIs

Resources are identified by URIs following the format:
```
[protocol]://[host]/[path]
```

Examples:
- `file:///home/user/documents/report.pdf`
- `postgres://database/customers/schema`
- `screen://localhost/display1`

### Resource Types

1. **Text Resources**: UTF-8 encoded text (source code, logs, JSON, plain text)
2. **Binary Resources**: Base64-encoded binary data (images, PDFs, audio, video)

### Resource Discovery

**Direct Resources** via `resources/list`:
```typescript
{
  uri: string;
  name: string;
  description?: string;
  mimeType?: string;
  size?: number;
}
```

**Resource Templates**: URI templates (RFC 6570) for dynamic resources:
```typescript
{
  uriTemplate: string;
  name: string;
  description?: string;
  mimeType?: string;
}
```

### Reading Resources

- Request: `resources/read` with resource URI
- Response: Array of resource contents with `uri`, `mimeType`, and either `text` or `blob`
- Servers may return multiple resources in one response

### Resource Updates

1. **List Changes**: `notifications/resources/list_changed` when available resources change
2. **Content Changes**: 
   - Client subscribes: `resources/subscribe`
   - Server notifies: `notifications/resources/updated`
   - Client fetches: `resources/read`
   - Client unsubscribes: `resources/unsubscribe`

### Best Practices

1. Use clear, descriptive names and URIs
2. Include helpful descriptions
3. Set appropriate MIME types
4. Implement resource templates for dynamic content
5. Use subscriptions for frequently changing resources
6. Handle errors gracefully
7. Consider pagination for large lists
8. Cache resource contents when appropriate
9. Validate URIs before processing
10. Document custom URI schemes

### Security

- Validate all resource URIs
- Implement access controls
- Sanitize file paths to prevent directory traversal
- Be cautious with binary data
- Rate limit resource reads
- Audit resource access
- Encrypt sensitive data in transit
- Validate MIME types
- Implement timeouts

---

## 5. Sampling

### Overview
Sampling allows servers to request LLM completions through the client, enabling sophisticated agentic behaviors while maintaining user control.

**Note**: Not yet supported in Claude Desktop client.

### How Sampling Works

1. Server sends `sampling/createMessage` request to client
2. Client reviews and can modify the request
3. Client samples from an LLM
4. Client reviews the completion
5. Client returns result to server

This **human-in-the-loop** design ensures user control.

### Request Parameters

**Messages**: Conversation history array with role ("user" or "assistant") and content (text or image)

**Model Preferences**:
- `hints`: Array of model name suggestions (e.g., "claude-3", "sonnet")
- `costPriority`: 0-1, importance of minimizing cost
- `speedPriority`: 0-1, importance of low latency
- `intelligencePriority`: 0-1, importance of capabilities

**Context Inclusion**:
- `"none"`: No additional context
- `"thisServer"`: Include context from requesting server
- `"allServers"`: Include context from all connected servers

**Sampling Parameters**:
- `systemPrompt`: Optional system prompt
- `temperature`: 0.0-1.0, controls randomness
- `maxTokens`: Maximum tokens to generate
- `stopSequences`: Array of stop sequences
- `metadata`: Provider-specific parameters

### Response Format

```typescript
{
  model: string;
  stopReason?: "endTurn" | "stopSequence" | "maxTokens" | string;
  role: "user" | "assistant";
  content: {
    type: "text" | "image";
    text?: string;
    data?: string;
    mimeType?: string;
  }
}
```

### Human-in-the-Loop Controls

**For Prompts**:
- Users can view, modify, or reject prompts
- System prompts can be filtered
- Context inclusion controlled by client

**For Completions**:
- Users can view, modify, or reject completions
- Clients can filter completions
- Users control model selection

### Common Patterns

**Agentic Workflows**:
- Reading and analyzing resources
- Making context-based decisions
- Generating structured data
- Handling multi-step tasks

**Context Management**:
- Request minimal necessary context
- Structure context clearly
- Handle size limits
- Update context as needed

### Best Practices

1. Provide clear, well-structured prompts
2. Handle text and image content appropriately
3. Set reasonable token limits
4. Include relevant context
5. Validate responses
6. Handle errors gracefully
7. Consider rate limiting
8. Document expected behavior
9. Test with various parameters
10. Monitor sampling costs

### Security

- Validate message content
- Sanitize sensitive information
- Implement rate limits
- Monitor usage
- Encrypt data in transit
- Handle user data privacy
- Audit sampling requests
- Control cost exposure
- Implement timeouts

---

## 6. Elicitation

### Overview
Elicitation is a feature that allows servers to request additional information from users during interactions, enabling dynamic workflows.

**Introduced in specification revision 2025-06-18**.

### How Elicitation Works

1. Server sends elicitation request with message and expected data structure
2. Client presents request to user with appropriate UI
3. User accepts, declines, or cancels
4. Client validates and returns response
5. Server continues processing with provided information

### Request Structure

**Message**: Clear explanation of what information is needed and why

**Schema**: JSON Schema defining expected response structure (limited to flat objects with primitive types)

Example:
```json
{
  "message": "Please provide your GitHub username",
  "requestedSchema": {
    "type": "object",
    "properties": {
      "username": {
        "type": "string",
        "title": "GitHub Username",
        "description": "Your GitHub username (e.g., octocat)"
      }
    },
    "required": ["username"]
  }
}
```

### Supported Data Types

1. **Text Input**: String with minLength, maxLength, default
2. **Numbers**: Number with minimum, maximum, default
3. **Boolean Choices**: Boolean with default
4. **Selection Lists**: String with enum, enumNames, default

### User Response Actions

1. **Accept**: Provide requested information
2. **Decline**: Explicitly refuse to provide information
3. **Cancel**: Dismiss without making a choice

Servers should handle each response appropriately.

### Common Use Cases

- Initial setup and configuration
- Dynamic workflows requiring context-specific information
- Collecting user preferences
- Gathering project details
- Service integration (usernames, IDs)

### Best Practices

**For Servers**:
1. Be clear - explain why information is needed
2. Be minimal - only request essential information
3. Be flexible - have fallbacks for declined requests
4. Be timely - request when needed, not preemptively
5. Be respectful - never request passwords or tokens

**For Clients**:
1. Be transparent - show which server is requesting
2. Be protective - allow users to review and modify
3. Be validating - check responses against schema
4. Be empowering - make decline/cancel options prominent
5. Be limiting - implement rate limiting

### Security

**Warning**: Servers must never use elicitation to request passwords, API keys, tokens, or other sensitive credentials.

Key guidelines:
- Only request non-sensitive information
- Clearly indicate requesting server
- Always allow option to decline
- Validate responses against schema
- Implement rate limiting

---

## 7. Roots

### Overview
Roots define the boundaries where servers can operate, providing a way for clients to inform servers about relevant resources and locations.

### What Are Roots?

A root is a URI that a client suggests a server should focus on. Examples:
- `file:///home/user/projects/myapp`
- `https://api.example.com/v1`

### Purpose

1. **Guidance**: Inform servers about relevant resources
2. **Clarity**: Make clear which resources are part of workspace
3. **Organization**: Work with different resources simultaneously

### How Roots Work

**Client**:
1. Declares `roots` capability during connection
2. Provides list of suggested roots
3. Notifies server when roots change

**Server**:
1. Respects provided roots
2. Uses root URIs to locate resources
3. Prioritizes operations within root boundaries

### Root Structure

```json
{
  "roots": [
    {
      "uri": "file:///home/user/projects/frontend",
      "name": "Frontend Repository"
    },
    {
      "uri": "https://api.example.com/v1",
      "name": "API Endpoint"
    }
  ]
}
```

### Common Use Cases

- Project directories
- Repository locations
- API endpoints
- Configuration locations
- Resource boundaries

### Best Practices

1. Only suggest necessary resources
2. Use clear, descriptive names
3. Monitor root accessibility
4. Handle root changes gracefully

---

## 8. Transports

### Overview
Transports provide the foundation for communication between clients and servers, handling the underlying mechanics of message transmission.

### Message Format

MCP uses **JSON-RPC 2.0** as its wire format with three message types:

1. **Requests**: `{jsonrpc, id, method, params?}`
2. **Responses**: `{jsonrpc, id, result?, error?}`
3. **Notifications**: `{jsonrpc, method, params?}`

### Built-in Transport Types

#### 1. Standard Input/Output (stdio)

Uses standard input/output streams for local process communication.

**Use When**:
- Building command-line tools
- Implementing local integrations
- Needing simple process communication
- Working with shell scripts

**TypeScript Example**:
```typescript
// Server
const transport = new StdioServerTransport();
await server.connect(transport);

// Client
const transport = new StdioClientTransport({
  command: "./server",
  args: ["--option", "value"]
});
await client.connect(transport);
```

**Python Example**:
```python
# Server
async with stdio_server() as streams:
    await app.run(streams[0], streams[1], app.create_initialization_options())

# Client
async with stdio_client(params) as streams:
    async with ClientSession(streams[0], streams[1]) as session:
        await session.initialize()
```

#### 2. Streamable HTTP

Uses HTTP POST for client-to-server communication and optional SSE for server-to-client streaming.

**Use When**:
- Building web-based integrations
- Needing client-server communication over HTTP
- Requiring stateful sessions
- Supporting multiple concurrent clients
- Implementing resumable connections

**How It Works**:
1. Client-to-Server: HTTP POST requests to MCP endpoint
2. Server Responses: Single JSON response or SSE stream
3. Server-to-Client: SSE streams from POST responses or GET requests

**Session Management**:
- Session initialization with `Mcp-Session-Id` header
- Session persistence in subsequent requests
- Session termination via HTTP DELETE

**Resumability**:
- Event IDs for tracking
- Resume from last event using `Last-Event-ID` header
- Message replay from disconnection point

**Security Considerations**:
1. Validate Origin headers (prevent DNS rebinding attacks)
2. Bind to localhost (127.0.0.1) for local servers
3. Implement authentication
4. Use HTTPS in production
5. Validate session IDs

#### 3. Server-Sent Events (SSE) - Deprecated

**Note**: SSE as standalone transport is deprecated as of protocol version 2024-11-05, replaced by Streamable HTTP.

### Custom Transports

MCP allows custom transport implementations conforming to the Transport interface:

**TypeScript Interface**:
```typescript
interface Transport {
  start(): Promise<void>;
  send(message: JSONRPCMessage): Promise<void>;
  close(): Promise<void>;
  onclose?: () => void;
  onerror?: (error: Error) => void;
  onmessage?: (message: JSONRPCMessage) => void;
}
```

### Error Handling

Transport implementations should handle:
1. Connection errors
2. Message parsing errors
3. Protocol errors
4. Network timeouts
5. Resource cleanup

### Best Practices

1. Handle connection lifecycle properly
2. Implement proper error handling
3. Clean up resources on close
4. Use appropriate timeouts
5. Validate messages before sending
6. Log transport events
7. Implement reconnection logic
8. Handle backpressure
9. Monitor connection health
10. Implement security measures

### Security

**Authentication and Authorization**:
- Implement proper authentication
- Validate client credentials
- Use secure token handling
- Implement authorization checks

**Data Security**:
- Use TLS for network transport
- Encrypt sensitive data
- Validate message integrity
- Implement message size limits
- Sanitize input data

**Network Security**:
- Implement rate limiting
- Use appropriate timeouts
- Handle DoS scenarios
- Monitor for unusual patterns
- Implement firewall rules
- For HTTP transports, validate Origin headers
- For local servers, bind to localhost only

### Backwards Compatibility

**For Servers Supporting Older Clients**:
- Host both old SSE/POST endpoints and new MCP endpoint
- Handle initialization on both endpoints
- Maintain separate handling logic

**For Clients Supporting Older Servers**:
- Accept server URLs for either transport
- Attempt POST with proper Accept headers
- Fall back to legacy SSE on 4xx status
- Issue GET request for SSE stream with `endpoint` event

---

## 9. Debugging

### Overview
Effective debugging is essential for developing MCP servers and integrations. This section covers debugging tools for macOS.

### Debugging Tools

1. **MCP Inspector**
   - Interactive debugging interface
   - Direct server testing
   
2. **Claude Desktop Developer Tools**
   - Integration testing
   - Log collection
   - Chrome DevTools integration

3. **Server Logging**
   - Custom logging implementations
   - Error tracking
   - Performance monitoring

### Debugging in Claude Desktop

#### Checking Server Status

Click icons in Claude.app to view:
- Connected servers
- Available prompts and resources
- Tools made available to model

#### Viewing Logs

```bash
# Follow logs in real-time
tail -n 20 -F ~/Library/Logs/Claude/mcp*.log
```

Logs capture:
- Server connection events
- Configuration issues
- Runtime errors
- Message exchanges

#### Using Chrome DevTools

1. Enable DevTools:
```bash
echo '{"allowDevTools": true}' > ~/Library/Application\ Support/Claude/developer_settings.json
```

2. Open DevTools: `Command-Option-Shift-i`

Use Console panel for client-side errors and Network panel for message payloads and timing.

### Common Issues

#### Working Directory

- Working directory may be undefined (like `/` on macOS)
- Always use absolute paths in configuration
- Use absolute paths in `.env` files

Example:
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/data"]
}
```

#### Environment Variables

Servers inherit only a subset of variables (USER, HOME, PATH).

Override with `env` key:
```json
{
  "myserver": {
    "command": "mcp-server-myapp",
    "env": {
      "MYAPP_API_KEY": "some_key"
    }
  }
}
```

#### Server Initialization

Common problems:
1. **Path Issues**: Incorrect paths, missing files, permissions
2. **Configuration Errors**: Invalid JSON, missing fields, type mismatches
3. **Environment Problems**: Missing variables, incorrect values, permissions

#### Connection Problems

When servers fail to connect:
1. Check Claude Desktop logs
2. Verify server process is running
3. Test standalone with Inspector
4. Verify protocol compatibility

### Implementing Logging

#### Server-Side Logging

For stdio transport:
- Messages logged to stderr are captured automatically
- **Warning**: Do not log to stdout (interferes with protocol)

For all transports, send log message notifications:

**Python**:
```python
server.request_context.session.send_log_message(
  level="info",
  data="Server started successfully"
)
```

**TypeScript**:
```typescript
server.sendLoggingMessage({
  level: "info",
  data: "Server started successfully"
});
```

Important events to log:
- Initialization steps
- Resource access
- Tool execution
- Error conditions
- Performance metrics

#### Client-Side Logging

1. Enable debug logging
2. Monitor network traffic
3. Track message exchanges
4. Record error states

### Debugging Workflow

**Development Cycle**:
1. Initial Development: Use Inspector, implement core functionality, add logging
2. Integration Testing: Test in Claude Desktop, monitor logs, check error handling

**Testing Changes**:
- Configuration changes: Restart Claude Desktop
- Server code changes: Use Command-R to reload
- Quick iteration: Use Inspector during development

### Best Practices

**Logging Strategy**:
1. **Structured Logging**: Consistent formats, include context, add timestamps, track request IDs
2. **Error Handling**: Log stack traces, include error context, track patterns, monitor recovery
3. **Performance Tracking**: Log operation timing, monitor resource usage, track message sizes, measure latency

**Security Considerations**:
1. **Sensitive Data**: Sanitize logs, protect credentials, mask personal information
2. **Access Control**: Verify permissions, check authentication, monitor access patterns

### Getting Help

**First Steps**:
1. Check server logs
2. Test with Inspector
3. Review configuration
4. Verify environment

**Support Channels**:
- GitHub issues
- GitHub discussions

**Providing Information**:
- Log excerpts
- Configuration files
- Steps to reproduce
- Environment details

---

## Summary of Key Concepts

### Control Models

MCP defines three control models for different primitives:

1. **Application-Controlled**: Resources - clients decide how and when to use them
2. **User-Controlled**: Prompts - users explicitly select them
3. **Model-Controlled**: Tools - AI models can automatically invoke them (with approval)

### Core Communication Flow

1. **Initialization**: Client and server exchange capabilities
2. **Discovery**: Client discovers resources, tools, and prompts
3. **Interaction**: Tools executed, prompts retrieved, resources read
4. **Updates**: Servers notify clients of changes
5. **Termination**: Clean connection shutdown

### Security Principles

- Human-in-the-loop control for sensitive operations
- Validation at every layer (transport, protocol, application)
- Never request credentials through elicitation
- Sanitize all inputs and outputs
- Implement proper authentication and authorization
- Use encryption for sensitive data
- Rate limiting and monitoring

### Best Practices Across All Components

1. **Clear Naming**: Use descriptive names for all resources, tools, and prompts
2. **Comprehensive Descriptions**: Help users and models understand capabilities
3. **Proper Error Handling**: Report errors appropriately without exposing internals
4. **Validation**: Validate all inputs against schemas
5. **Logging**: Implement structured logging for debugging
6. **Security**: Follow security best practices at every level
7. **Testing**: Test with various scenarios and edge cases
8. **Documentation**: Document expected behaviors and formats
9. **Monitoring**: Track usage, performance, and errors
10. **Graceful Degradation**: Handle failures and missing data appropriately

---

This summary provides a comprehensive overview of the Model Context Protocol's legacy documentation, covering architecture, primitives (tools, prompts, resources), advanced features (sampling, elicitation, roots), transports, and debugging practices. The protocol is designed to enable flexible, secure, and controlled integration between LLM applications and external systems while maintaining user privacy and control.
