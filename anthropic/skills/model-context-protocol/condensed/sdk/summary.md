# Model Context Protocol (MCP) Java SDK - Comprehensive Documentation Summary

## Overview

The Model Context Protocol (MCP) Java SDK provides a complete implementation for building both MCP clients and servers in Java. It enables standardized integration between AI models and tools through a well-defined protocol architecture that supports multiple transport mechanisms and programming paradigms.

## Core Architecture

The SDK follows a layered architecture with clear separation of concerns:

### Three-Layer Architecture

1. **Client/Server Layer**: 
   - `McpClient`: Handles client-side protocol operations including server connection, tool discovery/execution, resource management, and prompt handling
   - `McpServer`: Manages server-side operations including exposing tools, managing resources, providing prompt templates, and handling client requests

2. **Session Layer**:
   - `McpSession`: Manages communication patterns and state
   - `DefaultMcpSession`: Concrete implementation handling message routing and session lifecycle

3. **Transport Layer**:
   - `McpTransport`: Handles JSON-RPC message serialization/deserialization
   - Multiple transport implementations available (STDIO, HTTP Streamable-HTTP, SSE, Servlet-based)

## Key Features

### Protocol Support
- **Version Compatibility Negotiation**: Automatic protocol version negotiation during initialization
- **Capability Negotiation**: Dynamic feature discovery and capability exchange between clients and servers
- **JSON-RPC Communication**: Standards-based message protocol for all interactions

### Core Capabilities

1. **Tools**: 
   - Server-side function exposure with discovery and execution
   - Input/output schema validation
   - Structured and unstructured content type support
   - List change notifications

2. **Resources**: 
   - URI-based resource access patterns
   - Resource management with template support
   - Subscription system for resource updates
   - Content retrieval with MIME type support

3. **Prompts**: 
   - Prompt template handling and management
   - Parameter substitution and context injection
   - Response formatting and instruction templating

4. **Completion**: 
   - Argument autocompletion for prompts and resource URIs
   - Pagination support for large result sets

5. **Progress Tracking**: 
   - Long-running operation progress notifications
   - Real-time status updates

6. **Ping**: 
   - Lightweight health check mechanism
   - Server keepalive functionality

7. **Logging**: 
   - Structured log messages from servers to clients
   - Multiple severity levels (DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY)
   - Client-controlled log level filtering

8. **Roots Management**: 
   - Filesystem boundary definitions
   - Dynamic root addition/removal
   - Root list change notifications

9. **Sampling**: 
   - AI model interaction support
   - Text and image-based interactions
   - Model preference hints and priorities

10. **Elicitation**: 
    - Server-initiated information requests
    - Structured data collection from users through clients

### Programming Paradigms

The SDK supports both **synchronous** and **asynchronous** programming models:

- **Sync API**: `McpSyncClient`, `McpSyncServer` - Traditional blocking operations
- **Async API**: `McpAsyncClient`, `McpAsyncServer` - Reactive programming with Mono/Flux (Project Reactor)

## Transport Implementations

### STDIO Transport
- **Purpose**: In-process communication via standard input/output
- **Features**: 
  - Bidirectional JSON-RPC message handling
  - Non-blocking message processing
  - Process-based integration
  - Lightweight implementation
- **Use Case**: Subprocess-based MCP servers (e.g., Node.js servers via npx)

### HTTP Streamable-HTTP Transport
- **Purpose**: Bidirectional HTTP-based communication
- **Variants**:
  - Java HttpClient-based (framework agnostic)
  - Spring WebFlux-based (reactive)
  - Spring WebMVC-based (servlet)
  - Servlet-based (Jakarta Servlet 6.0)
- **Features**:
  - Concurrent client connections
  - Message routing and session management
  - Graceful shutdown
  - Asynchronous message handling
- **Limitation**: Current implementation lacks resumability due to lack of session storage

### HTTP Stateless Streamable-HTTP Transport
- **Purpose**: Simplified stateless server deployments
- **Features**:
  - Unidirectional (client-to-server) communication
  - No session state maintenance
  - Returns `application/json` responses
  - Ideal for microservices and cloud-native deployments
- **Limitation**: Cannot send notifications back to clients

### SSE (Server-Sent Events) Transport
- **Purpose**: Server-to-client event streaming
- **Variants**:
  - Java HttpClient-based (framework agnostic)
  - Spring WebFlux-based (reactive)
  - Spring WebMVC-based (servlet)
  - Servlet-based (Jakarta Servlet 6.0)
- **Features**:
  - Real-time server-to-client updates
  - Concurrent client connections
  - Session management
  - Graceful shutdown

### Transport Customization

#### HttpClient Customization
- **Static customization**: Custom `HttpRequest.Builder` for fixed headers
- **Dynamic customization**: 
  - `McpSyncHttpClientRequestCustomizer` for sync clients
  - `McpAsyncHttpClientRequestCustomizer` for async clients
- **Use Cases**: Adding authentication tokens, custom headers, request modification

#### WebClient Customization
- **Static customization**: Custom `WebClient.Builder` with default headers
- **Dynamic customization**: `ExchangeFilterFunction` for runtime request modification
- **Context Access**: Integration with Reactor context for passing request-specific data

## MCP Client

### Client Features

The MCP Client implements the client-side protocol and handles:
- Protocol version and capability negotiation
- Message transport and JSON-RPC communication
- Tool discovery and execution
- Resource access and management
- Prompt system interactions
- Optional features (roots, sampling, elicitation)

### Creating Clients

#### Synchronous Client Example
```java
McpSyncClient client = McpClient.sync(transport)
    .requestTimeout(Duration.ofSeconds(10))
    .capabilities(ClientCapabilities.builder()
        .roots(true)
        .sampling()
        .elicitation()
        .build())
    .sampling(request -> CreateMessageResult.builder()...build())
    .elicitation(elicitRequest -> ElicitResult.builder()...build())
    .toolsChangeConsumer((List<McpSchema.Tool> tools) -> ...)
    .resourcesChangeConsumer((List<McpSchema.Resource> resources) -> ...)
    .promptsChangeConsumer((List<McpSchema.Prompt> prompts) -> ...)
    .loggingConsumer((LoggingMessageNotification logging) -> ...)
    .progressConsumer((ProgressNotification progress) -> ...)
    .build();

client.initialize();
```

#### Asynchronous Client Example
```java
McpAsyncClient client = McpClient.async(transport)
    .requestTimeout(Duration.ofSeconds(10))
    .capabilities(ClientCapabilities.builder()
        .roots(true)
        .sampling()
        .elicitation()
        .build())
    .sampling(request -> Mono.just(new CreateMessageResult(response)))
    .elicitation(elicitRequest -> Mono.just(ElicitResult.builder()...build()))
    .toolsChangeConsumer(tools -> Mono.fromRunnable(() -> logger.info("Tools updated")))
    .build();

client.initialize().subscribe();
```

### Client Operations

#### Tool Execution
- `listTools()`: Discover available tools
- `callTool(name, arguments)`: Execute a tool with parameters

#### Resource Access
- `listResources()`: Discover available resources
- `readResource(uri)`: Retrieve resource content
- `getResource(name, templateParams)`: Access resources via URI templates

#### Prompt System
- `listPrompts()`: Discover available prompt templates
- `getPrompt(name, arguments)`: Execute a prompt template
- `executePrompt(name, arguments)`: Execute and format prompt

#### Roots Management
- `addRoot(Root)`: Add a filesystem root
- `removeRoot(uri)`: Remove a root
- `rootsListChangedNotification()`: Notify server of changes

#### Completion
- `completeCompletion(CompleteRequest)`: Request autocompletion suggestions

#### Logging Control
- `setLoggingLevel(LoggingLevel)`: Set minimum log level filter

### Client Capabilities

#### Roots Support
Defines filesystem boundaries for server operations. Servers can request the list of accessible roots and receive notifications when the list changes.

#### Sampling Support
Enables servers to request LLM interactions through the client. Features:
- Servers leverage AI without requiring API keys
- Clients maintain control over model access
- Support for text and image interactions
- Optional MCP server context inclusion
- Model preference hints (intelligence, speed priorities)

#### Elicitation Support
Allows servers to request specific information or clarification from clients using structured schemas.

#### Logging Support
Clients register logging consumers to receive server log messages with configurable severity level filtering.

#### Progress Support
Clients register progress consumers to receive real-time updates on long-running operations.

#### Change Notifications
Clients can register consumers for:
- Tools change notifications
- Resources change notifications
- Prompts change notifications

### Context Information Management

#### Sync Client Context
Uses `transportContextProvider` to extract thread-local information and make it available to transport customizers.

#### Async Client Context
Uses Reactor `contextWrite` to pass information through the reactive chain, accessible via `Mono.deferContextual`.

## MCP Server

### Server Features

The MCP Server implements the server-side protocol and provides:
- Tool exposure with discovery and execution
- Resource management with URI-based access
- Prompt template provision
- Capability negotiation
- Concurrent client connection management
- Structured logging, progress tracking, and notifications

### Creating Servers

#### Synchronous Server Example
```java
McpSyncServer syncServer = McpServer.sync(transportProvider)
    .serverInfo("my-server", "1.0.0")
    .capabilities(ServerCapabilities.builder()
        .resources(false, true)
        .tools(true)
        .prompts(true)
        .logging()
        .completions()
        .build())
    .build();

syncServer.addTool(syncToolSpecification);
syncServer.addResource(syncResourceSpecification);
syncServer.addPrompt(syncPromptSpecification);
```

#### Asynchronous Server Example
```java
McpAsyncServer asyncServer = McpServer.async(transportProvider)
    .serverInfo("my-server", "1.0.0")
    .capabilities(ServerCapabilities.builder()
        .resources(false, true)
        .tools(true)
        .prompts(true)
        .logging()
        .completions()
        .build())
    .build();

asyncServer.addTool(asyncToolSpecification).subscribe();
asyncServer.addResource(asyncResourceSpecification).subscribe();
asyncServer.addPrompt(asyncPromptSpecification).subscribe();
```

### Thread-Local Preservation in Sync Servers

`McpSyncServer` delegates to an underlying `McpAsyncServer`. To ensure thread-locals remain available when handlers execute, use:
```java
McpServer.sync(...).immediateExecution(true)
```

### Server Specifications

#### Tool Specification

Tools enable AI models to perform calculations, access APIs, query databases, and manipulate files.

**Components**:
- **Tool Definition**: Name, description, parameter schema (JSON Schema)
- **Handler Function**: Implementation logic
  - First argument: `McpAsyncServerExchange`/`McpSyncServerExchange` for client interaction
  - Second argument: Map of tool arguments
  - Returns: `CallToolResult`

**Example**:
```java
var syncToolSpecification = new McpServerFeatures.SyncToolSpecification(
    new Tool("calculator", "Basic calculator", schema),
    (exchange, arguments) -> {
        // Tool implementation
        return new CallToolResult(result, false);
    }
);
```

#### Resource Specification

Resources provide context to AI models by exposing data (files, database records, API responses, etc.).

**Components**:
- **Resource Definition**: URI, name, description, MIME type, annotations
- **Handler Function**: Resource read implementation
  - First argument: `McpAsyncServerExchange`/`McpSyncServerExchange`
  - Second argument: `ReadResourceRequest`
  - Returns: `ReadResourceResult` with content list

**Example**:
```java
var syncResourceSpecification = new McpServerFeatures.SyncResourceSpecification(
    new Resource("custom://resource", "name", "description", "mime-type", null),
    (exchange, request) -> {
        return new ReadResourceResult(contents);
    }
);
```

#### Prompt Specification

Prompt templates enable consistent message formatting with parameter substitution.

**Components**:
- **Prompt Definition**: Name, description, list of arguments (with required flag)
- **Handler Function**: Template processing and formatting
  - First argument: `McpAsyncServerExchange`/`McpSyncServerExchange`
  - Second argument: `GetPromptRequest`
  - Returns: `GetPromptResult` with description and messages

**Example**:
```java
var syncPromptSpecification = new McpServerFeatures.SyncPromptSpecification(
    new Prompt("greeting", "description", List.of(
        new PromptArgument("name", "description", true)
    )),
    (exchange, request) -> {
        return new GetPromptResult(description, messages);
    }
);
```

#### Completion Specification

Provides autocompletion suggestions for prompt arguments and resource URIs.

**Components**:
- **Completion Reference**: Type (PromptReference or ResourceReference) and identifier
- **Handler Function**: Completion logic
  - First argument: `McpAsyncServerExchange`/`McpSyncServerExchange`
  - Second argument: `CompleteRequest`
  - Returns: `CompleteResult` with suggestions, total count, hasMore flag

**Example**:
```java
var syncCompletionSpecification = new McpServerFeatures.SyncCompletionSpecification(
    new McpSchema.PromptReference("code_review"),
    (exchange, request) -> {
        return new McpSchema.CompleteResult(
            new CompleteResult.CompleteCompletion(
                List.of("python", "pytorch", "pyside"),
                10,
                false
            )
        );
    }
);
```

### Using Sampling from a Server

Servers can request language model generations from compatible clients. No special server configuration is needed.

**Key Steps**:
1. Check client sampling support via `exchange.getClientCapabilities().sampling()`
2. Create `CreateMessageRequest` with:
   - Messages: Input content (text or image)
   - Model preferences: Hints and priorities (intelligence, speed)
   - System prompt: Behavior instructions
   - Max tokens: Response length limit
3. Call `exchange.createMessage(request)`
4. Process the `CreateMessageResult`

**Example**:
```java
if (exchange.getClientCapabilities().sampling() == null) {
    return new CallToolResult("Client does not support AI capabilities", false);
}

McpSchema.CreateMessageRequest request = McpSchema.CreateMessageRequest.builder()
    .messages(List.of(new McpSchema.SamplingMessage(McpSchema.Role.USER,
        new McpSchema.TextContent("Calculate: " + arguments.get("expression")))
    .modelPreferences(McpSchema.ModelPreferences.builder()
        .hints(List.of(McpSchema.ModelHint.of("claude-3-sonnet")))
        .intelligencePriority(0.8)
        .speedPriority(0.5)
        .build())
    .systemPrompt("You are a helpful calculator assistant.")
    .maxTokens(100)
    .build();

McpSchema.CreateMessageResult result = exchange.createMessage(request);
```

### Using Elicitation from a Server

Servers can request additional information from users through the client.

**Key Steps**:
1. Check client elicitation support via `exchange.getClientCapabilities().elicitation()`
2. Create `ElicitRequest` with:
   - Message: Prompt for the user
   - Requested schema: JSON Schema for expected response structure
3. Call `exchange.createElicitation(request)`
4. Process the `ElicitResult` containing structured data

**Example**:
```java
if (exchange.getClientCapabilities().elicitation() == null) {
    return new CallToolResult("Client does not support elicitation", false);
}

McpSchema.ElicitRequest request = McpSchema.ElicitRequest.builder()
    .message("Please provide additional information")
    .requestedSchema(
        Map.of("type", "object", 
               "properties", Map.of("message", Map.of("type", "string")))
    )
    .build();

McpSchema.ElicitResult result = exchange.createElicitation(request);
```

### Logging Support

Servers can send structured log messages to clients from within tool/resource/prompt handlers.

**Features**:
- Multiple severity levels (DEBUG through EMERGENCY)
- Client-side log level filtering
- Session-based logging via `McpAsyncServerExchange`/`McpSyncServerExchange`

**Example**:
```java
exchange.loggingNotification(
    McpSchema.LoggingMessageNotification.builder()
        .level(McpSchema.LoggingLevel.DEBUG)
        .logger("test-logger")
        .data("Debug message")
        .build()
).block();
```

## Dependencies and Installation

### Core Dependency (Maven)
```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp</artifactId>
</dependency>
```

The core module includes STDIO, SSE, and Streamable-HTTP transports without requiring external web frameworks.

### Optional Spring Dependencies

For Spring Framework users:

```xml
<!-- WebFlux-based transports (reactive) -->
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp-spring-webflux</artifactId>
</dependency>

<!-- WebMVC-based transports (servlet) -->
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp-spring-webmvc</artifactId>
</dependency>
```

### Bill of Materials (BOM)

The BOM manages dependency versions automatically:

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>io.modelcontextprotocol.sdk</groupId>
            <artifactId>mcp-bom</artifactId>
            <version>0.12.1</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

### Additional Dependencies
- `io.modelcontextprotocol.sdk:mcp-test` - Testing utilities for MCP applications

## Error Handling

The SDK provides comprehensive error handling through the `McpError` class, covering:
- Protocol compatibility issues
- Transport communication errors
- JSON-RPC messaging failures
- Tool execution errors
- Resource management errors
- Prompt handling errors
- Timeout and connection issues

This unified approach ensures consistent error management across both synchronous and asynchronous operations.

## Integration Patterns

### Spring AI Integration

The Java MCP SDK is designed to work seamlessly with Spring AI:
- Spring AI MCP Client Boot Starter
- Spring AI MCP Server Boot Starter
- WebFlux and WebMVC transport integrations

### Deployment Scenarios

1. **Process-based**: STDIO transport for subprocess servers (Node.js, Python, etc.)
2. **Microservices**: Stateless Streamable-HTTP for cloud-native deployments
3. **Distributed systems**: Streamable-HTTP or SSE with proper message routing
4. **Traditional web apps**: Servlet-based transports with Jakarta Servlet 6.0

## Key Considerations

### Transport Selection

- **STDIO**: Best for local subprocess integration, lightweight
- **Streamable-HTTP**: Best for bidirectional communication, distributed systems
- **Stateless Streamable-HTTP**: Best for scalable cloud deployments, unidirectional flow
- **SSE**: Best for real-time server-to-client updates

### Sync vs Async

- **Sync**: Traditional blocking code, easier to understand, thread-local support
- **Async**: Reactive programming, better scalability, Project Reactor integration

### Session State

- **Stateful transports** (STDIO, Streamable-HTTP, SSE): Maintain session state, support bidirectional notifications
- **Stateless transports**: No session state, simplified deployment, cannot send notifications to clients

### Scalability

- WebFlux-based transports are highly scalable and recommended for high-throughput scenarios
- Stateless transports eliminate session storage requirements for horizontal scaling
- Proper message routing required for distributed server deployments

## Related Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.org/docs/concepts/architecture)
- [Spring AI MCP Documentation](https://docs.spring.io/spring-ai/reference/)
- [Quickstart Demo - Client](https://modelcontextprotocol.org/quickstart/client)
- [Quickstart Demo - Server](https://modelcontextprotocol.org/quickstart/server)

## Summary

The Model Context Protocol Java SDK provides a comprehensive, production-ready implementation for building MCP clients and servers. Its layered architecture, multiple transport options, and support for both synchronous and asynchronous programming make it suitable for a wide range of applications from simple command-line tools to complex distributed systems. The SDK's integration with Spring Framework and Spring AI further enhances its utility in enterprise Java environments.
