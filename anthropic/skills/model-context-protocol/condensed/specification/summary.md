# Model Context Protocol (MCP) Specification Summary

This document provides a comprehensive summary of the Model Context Protocol specification, covering all versions and components documented in the specification folder.

## Overview and Purpose

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between LLM applications and external data sources and tools. It provides a standardized way to connect LLMs with the context they need, whether building AI-powered IDEs, enhancing chat interfaces, or creating custom AI workflows.

MCP is inspired by the Language Server Protocol (LSP) and applies similar standardization concepts to the AI ecosystem. While LSP standardizes programming language support across development tools, MCP standardizes how to integrate additional context and tools into AI applications.

## Protocol Versioning

### Version Format
MCP uses date-based version identifiers following the format `YYYY-MM-DD`, indicating the last date backwards-incompatible changes were made. The protocol version is only incremented for breaking changes, allowing incremental improvements while preserving interoperability.

### Version States
- **Draft**: In-progress specifications, not yet ready for consumption
- **Current**: The current protocol version (2025-06-18), ready for use and may receive backwards compatible changes
- **Final**: Past, complete specifications that will not be changed

### Documented Versions
- **2024-11-05**: First documented version
- **2025-03-26**: Added authorization framework, Streamable HTTP transport, JSON-RPC batching, tool annotations
- **2025-06-18**: Current version - removed batching, added structured tool output, enhanced authorization, elicitation support, resource links
- **Draft**: Future version with additional enhancements including icon metadata and OpenID Connect Discovery

## Core Architecture

### Components

**Hosts**: LLM applications that initiate connections and manage the overall integration

**Clients**: Connectors within the host application that:
- Establish one stateful session per server
- Handle protocol negotiation and capability exchange
- Route protocol messages bidirectionally
- Manage subscriptions and notifications
- Maintain security boundaries between servers

**Servers**: Services that provide context and capabilities by:
- Exposing resources, tools, and prompts via MCP primitives
- Operating independently with focused responsibilities
- Requesting sampling through client interfaces
- Respecting security constraints
- Can be local processes or remote services

### Design Principles

1. **Servers should be extremely easy to build**
   - Host applications handle complex orchestration
   - Servers focus on specific, well-defined capabilities
   - Simple interfaces minimize implementation overhead

2. **Servers should be highly composable**
   - Each server provides focused functionality in isolation
   - Multiple servers can be combined seamlessly
   - Shared protocol enables interoperability

3. **Servers should not see into other servers**
   - Servers receive only necessary contextual information
   - Full conversation history stays with the host
   - Each server connection maintains isolation
   - Host process enforces security boundaries

4. **Features can be added progressively**
   - Core protocol provides minimal required functionality
   - Additional capabilities can be negotiated as needed
   - Servers and clients evolve independently
   - Protocol designed for future extensibility

## Base Protocol

### Message Format
All messages use JSON-RPC 2.0 specification with:

**Requests**:
- MUST include a string or integer ID (NOT null)
- ID MUST NOT have been previously used in the same session
- Include method name and optional parameters

**Responses**:
- MUST include the same ID as the request
- MUST contain either result or error (not both)
- Error codes MUST be integers

**Notifications**:
- MUST NOT include an ID
- One-way messages requiring no response

### Metadata Field (_meta)
The `_meta` property is reserved for clients and servers to attach additional metadata. Key naming follows a prefix/name format:
- Prefix: Optional series of labels separated by dots, followed by slash
- Reserved prefixes: Any containing "modelcontextprotocol" or "mcp"
- Name: Alphanumeric with hyphens, underscores, dots allowed

## Transport Mechanisms

### stdio Transport
- Client launches MCP server as subprocess
- Server reads from stdin, writes to stdout
- Messages delimited by newlines, MUST NOT contain embedded newlines
- Server MAY write UTF-8 logs to stderr
- Clients SHOULD support stdio whenever possible

### Streamable HTTP Transport
Replaced HTTP+SSE from version 2024-11-05. Key features:

**Message Sending**:
- Every JSON-RPC message from client is a new HTTP POST
- Client MUST include Accept header for application/json and text/event-stream
- Server responds with either JSON or SSE stream

**Server Events**:
- Client MAY issue HTTP GET to open SSE stream
- Server MAY send requests and notifications on stream
- Supports resumability via Last-Event-ID header

**Session Management**:
- Server MAY assign session ID during initialization via Mcp-Session-Id header
- Client MUST include session ID in subsequent requests
- Sessions can be terminated by server (404) or client (DELETE)

**Protocol Version Header**:
- Client MUST include MCP-Protocol-Version header on HTTP requests
- Format: `MCP-Protocol-Version: 2025-06-18`
- Allows server to respond based on negotiated protocol version

**Security Warning**:
- Servers MUST validate Origin header to prevent DNS rebinding attacks
- Should bind only to localhost when running locally
- SHOULD implement proper authentication

### Custom Transports
Clients and servers MAY implement additional custom transports while preserving JSON-RPC message format and lifecycle requirements.

## Lifecycle Management

### Initialization Phase
The first required interaction establishing:

**Version Negotiation**:
- Client sends latest supported version in initialize request
- Server responds with same version if supported, or alternative version
- Client disconnects if server version is unsupported
- For HTTP, client MUST include MCP-Protocol-Version header on subsequent requests

**Capability Negotiation**:
Client capabilities:
- `roots`: Filesystem root access
- `sampling`: LLM sampling support
- `elicitation`: User information requests
- `experimental`: Non-standard features

Server capabilities:
- `prompts`: Prompt templates
- `resources`: Context and data
- `tools`: Executable functions
- `logging`: Structured log messages
- `completions`: Argument autocompletion
- `experimental`: Non-standard features

Each capability can have sub-capabilities like `listChanged` and `subscribe`.

**Process**:
1. Client sends initialize request with protocol version, capabilities, client info
2. Server responds with its capabilities, server info, optional instructions
3. Client sends initialized notification to begin normal operations

### Operation Phase
Both parties MUST:
- Respect negotiated protocol version
- Only use successfully negotiated capabilities

### Shutdown Phase
**stdio**: Client closes input stream, waits for server exit, sends SIGTERM then SIGKILL if needed

**HTTP**: Close associated HTTP connections

## Authorization Framework

Based on OAuth 2.1 with selected features for security and interoperability.

### Roles
- **MCP Server**: Acts as OAuth 2.1 resource server
- **MCP Client**: Acts as OAuth 2.1 client
- **Authorization Server**: Issues access tokens for MCP server use

### Key Requirements

**Standards Compliance**:
- OAuth 2.1 (draft-ietf-oauth-v2-1-13)
- OAuth 2.0 Authorization Server Metadata (RFC8414)
- OAuth 2.0 Dynamic Client Registration (RFC7591)
- OAuth 2.0 Protected Resource Metadata (RFC9728)
- Resource Indicators for OAuth 2.0 (RFC8707)

**Authorization Server Discovery**:
- MCP servers MUST implement Protected Resource Metadata (RFC9728)
- MUST use WWW-Authenticate header on 401 Unauthorized
- MCP clients MUST parse WWW-Authenticate headers and use Authorization Server Metadata

**Dynamic Client Registration**:
- Clients and servers SHOULD support RFC7591
- Enables automatic client registration without user interaction
- Critical for seamless connection to new MCP servers

**Resource Parameter**:
- Clients MUST implement RFC8707 Resource Indicators
- MUST include resource parameter in authorization and token requests
- Prevents malicious servers from obtaining access tokens for other services
- Resource parameter identifies canonical URI of MCP server

**Token Usage**:
- Clients MUST use Authorization Bearer header (not query string)
- Tokens MUST be included in every HTTP request
- Servers MUST validate tokens were issued specifically for them
- Servers MUST validate audience claims
- Token passthrough is EXPLICITLY FORBIDDEN

### Security Considerations

**Token Audience Binding**:
- Critical for preventing token misuse across services
- Servers MUST validate tokens intended for them
- Prevents confused deputy vulnerabilities

**Token Theft Mitigation**:
- Secure token storage required
- Short-lived access tokens recommended
- Refresh token rotation for public clients

**Communication Security**:
- All authorization endpoints MUST use HTTPS
- Redirect URIs MUST be localhost or HTTPS

**Authorization Code Protection**:
- Clients MUST implement PKCE
- Prevents code interception and injection attacks

**Open Redirection Prevention**:
- Clients MUST register redirect URIs
- Servers MUST validate exact redirect URIs
- State parameter verification recommended

**Confused Deputy Problem**:
- MCP proxy servers using static client IDs MUST obtain user consent for each dynamically registered client
- Prevents attackers from leveraging existing consent cookies

## Security Best Practices

### Token Passthrough
Explicitly forbidden anti-pattern where servers accept tokens without validating audience. Risks include:
- Security control circumvention
- Accountability and audit trail issues
- Trust boundary violations
- Future compatibility problems

### Session Hijacking
**Attack Vectors**:
- Session hijack prompt injection via malicious events
- Session hijack impersonation via stolen session IDs

**Mitigations**:
- Servers implementing authorization MUST verify all inbound requests
- MUST NOT use sessions for authentication
- MUST use secure, non-deterministic session IDs
- SHOULD bind session IDs to user-specific information

## Server Features

### Resources
Application-controlled context and data for user or AI model use.

**Capabilities**:
- `subscribe`: Client can subscribe to resource changes
- `listChanged`: Server emits notifications when resource list changes

**Protocol Messages**:
- `resources/list`: Discover available resources (supports pagination)
- `resources/read`: Retrieve resource contents
- `resources/templates/list`: List URI templates with parameters
- `resources/subscribe`: Subscribe to resource changes
- `notifications/resources/list_changed`: List changed notification
- `notifications/resources/updated`: Resource update notification

**Resource Definition**:
- `uri`: Unique identifier (RFC3986)
- `name`: Resource name
- `title`: Optional human-readable display name
- `description`: Optional description
- `mimeType`: Optional MIME type
- `size`: Optional size in bytes

**Content Types**:
- Text content (text field)
- Binary content (base64-encoded blob)

**Annotations**:
- `audience`: Array of "user" and/or "assistant"
- `priority`: Number 0.0-1.0 (0=optional, 1=required)
- `lastModified`: ISO 8601 timestamp

**Common URI Schemes**:
- `https://`: Web-accessible resources (client can fetch directly)
- `file://`: Filesystem-like resources
- `git://`: Git version control resources
- Custom schemes per RFC3986

### Tools
Model-controlled functions for AI to execute actions or retrieve information.

**Capabilities**:
- `tools`: Server supports tools
- `listChanged`: Notifications when tool list changes

**Protocol Messages**:
- `tools/list`: Discover available tools (supports pagination)
- `tools/call`: Invoke a tool
- `notifications/tools/list_changed`: List changed notification

**Tool Definition**:
- `name`: Unique identifier
- `title`: Optional human-readable display name
- `description`: Functionality description
- `inputSchema`: JSON Schema for parameters
- `outputSchema`: Optional JSON Schema for output structure
- `annotations`: Optional behavior descriptions (untrusted unless from trusted server)

**Tool Results**:

Unstructured content in `content` field:
- Text content
- Image content (base64-encoded)
- Audio content (base64-encoded)
- Resource links (URIs to resources)
- Embedded resources (inline resource data)

Structured content:
- JSON object in `structuredContent` field
- Should also include serialized JSON in TextContent for backwards compatibility
- Can be validated against outputSchema

**Error Handling**:
- Protocol errors: JSON-RPC errors for unknown tools, invalid arguments
- Tool execution errors: Reported in results with `isError: true`

**Tool Naming Guidance**:
- Names should be descriptive and specific
- Use lowercase with underscores for readability
- Follow consistent naming patterns within server

**Security**:
- Servers MUST validate inputs, implement access controls, rate limit, sanitize outputs
- Clients SHOULD prompt for user confirmation, show inputs, validate results, implement timeouts, log usage

### Prompts
User-controlled templates for interacting with language models.

**Capabilities**:
- `prompts`: Server supports prompts
- `listChanged`: Notifications when prompt list changes

**Protocol Messages**:
- `prompts/list`: Retrieve available prompts (supports pagination)
- `prompts/get`: Get specific prompt with arguments
- `notifications/prompts/list_changed`: List changed notification

**Prompt Definition**:
- `name`: Unique identifier
- `title`: Optional human-readable display name
- `description`: Optional description
- `arguments`: Optional list of customization arguments

**Message Content Types**:
All support optional annotations:
- Text content
- Image content (base64-encoded with MIME type)
- Audio content (base64-encoded with MIME type)
- Embedded resources (server-managed content with URI and MIME type)

**Message Roles**:
- `user`: User messages
- `assistant`: Assistant messages

## Client Features

### Sampling
Server-initiated agentic LLM interactions.

**Capabilities**:
- `sampling`: Client supports LLM sampling requests

**Protocol Messages**:
- `sampling/createMessage`: Request language model generation

**Request Parameters**:
- `messages`: Array of messages with role and content
- `modelPreferences`: Optional hints and priorities
- `systemPrompt`: Optional system instructions
- `maxTokens`: Maximum response length

**Model Preferences**:
- `hints`: Optional model name suggestions (treated as substrings)
- `costPriority`: 0-1 (higher = prefer cheaper models)
- `speedPriority`: 0-1 (higher = prefer faster models)
- `intelligencePriority`: 0-1 (higher = prefer more capable models)

**Response**:
- `role`: "assistant"
- `content`: Generated content
- `model`: Actual model used
- `stopReason`: Why generation stopped

**Security**:
- SHOULD always have human in the loop
- Clients SHOULD implement user approval, present requests for review, allow editing
- Validate message content, respect model preferences, implement rate limiting

### Roots
Client-exposed filesystem boundaries for server operation.

**Capabilities**:
- `roots`: Client supports roots
- `listChanged`: Notifications when root list changes

**Protocol Messages**:
- `roots/list`: Retrieve available roots
- `notifications/roots/list_changed`: List changed notification

**Root Definition**:
- `uri`: MUST be file:// URI
- `name`: Optional human-readable name

**Security**:
- Clients MUST validate URIs, prevent path traversal, implement access controls
- Servers SHOULD respect root boundaries, validate paths against roots

### Elicitation
Server-initiated user information requests (new in 2025-06-18).

**Capabilities**:
- `elicitation`: Client supports elicitation requests

**Protocol Messages**:
- `elicitation/create`: Request information from user

**Request Parameters**:
- `message`: Human-readable request message
- `requestedSchema`: JSON Schema defining expected response structure

**Supported Schema Types**:
- String (with optional format: email, uri, date, date-time)
- Number/Integer (with min/max)
- Boolean (with default)
- Enum (string type with enum values and optional enumNames)

Limited to flat objects with primitive properties only.

**Response Actions**:
- `accept`: User approved and submitted data (includes content)
- `decline`: User explicitly declined (no content)
- `cancel`: User dismissed without choice (no content)

**Security**:
- Servers MUST NOT request sensitive information
- Clients SHOULD implement approval controls, validate against schema, indicate requesting server, allow declining
- Both SHOULD implement rate limiting

## Utility Features

### Logging
Structured log message system from servers to clients.

**Capabilities**:
- `logging`: Server emits log messages

**Log Levels** (RFC 5424):
- debug, info, notice, warning, error, critical, alert, emergency

**Protocol Messages**:
- `logging/setLevel`: Client configures minimum log level
- `notifications/message`: Server sends log messages

**Message Parameters**:
- `level`: Severity level
- `logger`: Optional logger name
- `data`: Arbitrary JSON-serializable data

**Security**:
- Log messages MUST NOT contain credentials, secrets, PII, or sensitive system details
- Servers SHOULD rate limit, include context, use consistent logger names
- Clients MAY present in UI, filter/search, persist logs

### Pagination
Cursor-based pagination for large result sets.

**Model**:
- Opaque cursor tokens (not numbered pages)
- Server-determined page size
- Clients MUST NOT assume fixed page size

**Response Format**:
- Current page of results
- Optional `nextCursor` if more results exist

**Request Format**:
- Include `cursor` from previous response to continue

**Supported Operations**:
- `resources/list`
- `resources/templates/list`
- `prompts/list`
- `tools/list`

**Guidelines**:
- Servers SHOULD provide stable cursors, handle invalid cursors gracefully
- Clients MUST treat cursors as opaque, don't parse/modify/persist across sessions
- Missing nextCursor indicates end of results

### Completion
Argument autocompletion for prompts and resources.

**Capabilities**:
- `completions`: Server supports argument autocompletion

**Protocol Messages**:
- `completion/complete`: Request completion suggestions

**Request Parameters**:
- `ref`: PromptReference or ResourceReference
  - `ref/prompt` with name
  - `ref/resource` with URI template
- `argument`: Object with name and current value
- `context`: Optional object with already-resolved arguments

**Response**:
- `values`: Array of suggestions (max 100)
- `total`: Optional total matches
- `hasMore`: Boolean for additional results

**Implementation**:
- Servers SHOULD sort by relevance, implement fuzzy matching, rate limit, validate inputs
- Clients SHOULD debounce requests, cache results, handle partial results

### Progress Tracking
Optional progress notifications for long-running operations.

**Flow**:
1. Requester includes `progressToken` in request metadata (_meta)
2. Receiver MAY send progress notifications with:
   - Original progress token
   - Current progress value (MUST increase)
   - Optional total value
   - Optional message string

**Requirements**:
- Progress and total MAY be floating point
- Notifications MUST only reference active request tokens
- Receivers MAY choose not to send notifications or omit total if unknown
- Progress MUST stop after completion

### Cancellation
Optional request cancellation via notifications.

**Protocol Messages**:
- `notifications/cancelled`: Cancel in-progress request

**Parameters**:
- `requestId`: ID of request to cancel
- `reason`: Optional reason string

**Requirements**:
- MUST only reference previously issued, in-progress requests
- Initialize request MUST NOT be cancelled by clients
- Receivers SHOULD stop processing, free resources, not send response
- Receivers MAY ignore if request unknown/completed/uncancellable
- Both parties MUST handle race conditions gracefully

### Ping
Connection health verification mechanism.

**Protocol Messages**:
- `ping`: Request with no parameters

**Response**:
- Empty result object

**Usage**:
- Either party can initiate
- Receiver MUST respond promptly
- No response within timeout MAY trigger connection termination
- Implementations SHOULD periodically ping, make timeout/frequency configurable, avoid excessive pinging

## Version Evolution

### 2024-11-05 to 2025-03-26
Major additions:
- Comprehensive authorization framework based on OAuth 2.1
- Streamable HTTP transport replacing HTTP+SSE
- JSON-RPC batching support
- Tool annotations for describing behavior
- Audio data support
- Progress notification messages
- Completions capability for autocompletion

### 2025-03-26 to 2025-06-18
Major changes:
- Removed JSON-RPC batching
- Added structured tool output with outputSchema
- Classified MCP servers as OAuth Resource Servers
- Required Resource Indicators (RFC8707) implementation
- Enhanced security considerations and best practices documentation
- Added elicitation for server-initiated user information requests
- Added resource links in tool call results
- Required MCP-Protocol-Version header for HTTP requests
- Changed lifecycle operation from SHOULD to MUST
- Added _meta field to additional interface types
- Added context field to CompletionRequest
- Added title field for human-friendly display names

### 2025-06-18 to Draft
Upcoming additions:
- Icon metadata for tools, resources, resource templates, and prompts
- Enhanced authorization with OpenID Connect Discovery 1.0 support
- Incremental scope consent via WWW-Authenticate
- Tool naming guidance
- Clarified Origin header validation in Streamable HTTP
- Updated security best practices
- Decoupled request payloads from RPC method definitions

## TypeScript Schema

The authoritative specification is defined in TypeScript schema files (schema.ts) for each version. These include:

**Common Types**:
- Annotations (audience, priority, lastModified)
- Content types (Text, Image, Audio)
- Resource contents (Text, Blob)
- Client and Server capabilities
- Request/Response/Notification messages

**JSON Schema** is automatically generated from TypeScript for automated tooling.

## Key Terminology

**Host**: LLM application container managing clients

**Client**: Isolated connector to a single server

**Server**: Service providing resources, tools, or prompts

**Resource**: Context and data with URI identifier

**Prompt**: Templated message for model interaction

**Tool**: Executable function for model to invoke

**Sampling**: LLM completion request from server to client

**Root**: Filesystem boundary definition

**Elicitation**: User information request from server

**Capability**: Optional protocol feature negotiated during initialization

**Session**: Logically related interactions from initialization to shutdown

**Cursor**: Opaque pagination token

**Annotation**: Metadata describing content usage or display

**Progress Token**: Identifier for tracking long-running operations

## Implementation Considerations

### Must Implement
- Base protocol (JSON-RPC 2.0 messages)
- Lifecycle management (initialization, operation, shutdown)
- At least one transport (preferably stdio)

### Should Implement
- Appropriate capabilities based on use case
- Timeouts for all requests
- Progress tracking for long operations
- Proper error handling
- Security best practices
- User consent flows for sensitive operations

### May Implement
- Additional custom capabilities
- Custom transports
- Extended metadata in _meta fields
- Custom URI schemes

## Security Requirements

### Critical
- User consent for data access and tool invocation
- User control over sampling requests
- Access token validation and audience checking
- No token passthrough
- Secure session ID generation
- Origin header validation for HTTP
- HTTPS for all authorization endpoints
- PKCE implementation

### Important
- Input validation
- Rate limiting
- Access controls
- Secure token storage
- Proper error messages (don't leak sensitive info)
- Audit logging
- Clear UI for security-relevant operations

### Recommendations
- Human in the loop for tools and sampling
- Confirmation prompts for destructive operations
- Clear visual indicators for AI actions
- Least privilege principle
- Regular security reviews
- Monitor for suspicious patterns

## Use Cases and Examples

### Resources
- File contents for code analysis
- Database schemas for query generation
- Git history for context
- Documentation for reference
- Configuration data

### Tools
- API calls to external services
- File system operations
- Database queries
- Code execution
- Data transformations

### Prompts
- Slash commands in chat interfaces
- Templated workflows
- Standard operating procedures
- Code review templates
- Analysis frameworks

### Sampling
- Recursive analysis within tools
- Multi-step reasoning
- Code generation within servers
- Translation tasks
- Summarization

## Conclusion

The Model Context Protocol provides a comprehensive, well-designed framework for integrating LLMs with external context and capabilities. It emphasizes:

1. **Security**: Strong OAuth 2.1-based authorization, explicit user consent, clear boundaries
2. **Simplicity**: Easy server implementation, clear separation of concerns
3. **Composability**: Multiple independent servers, modular capabilities
4. **Flexibility**: Progressive feature adoption, custom extensions
5. **Interoperability**: Standard protocols, clear specifications, version negotiation

The protocol continues to evolve with community feedback while maintaining backwards compatibility and a focus on security, developer experience, and user safety.
