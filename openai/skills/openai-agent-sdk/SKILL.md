---
name: openai-agent-sdk
description: Reference documentation for the OpenAI Agents SDK for TypeScript. Use when working with OpenAI Agents SDK, @openai/agents package, building AI agents with TypeScript, implementing multi-agent systems, agent handoffs, tools, guardrails, realtime voice agents, streaming responses, MCP servers, or agent orchestration patterns. Covers agent configuration, model selection, context management, tracing, and integration with Vercel AI SDK, Twilio, and Cloudflare Workers.
---

# OpenAI Agents SDK

The OpenAI Agents SDK for TypeScript is a production-ready framework for building agentic AI applications with a minimal set of abstractions. It enables development of both text-based and voice agents with features like multi-agent orchestration, tool calling, guardrails, and built-in tracing.

## What This Skill Provides

This skill provides comprehensive documentation for building agent-based applications using the OpenAI Agents SDK. The SDK offers:

- Lightweight primitives for defining agents with instructions, tools, and models
- Multi-agent coordination through handoffs and tools-as-agents patterns
- Real-time voice agents using the OpenAI Realtime API
- Built-in tracing, debugging, and monitoring capabilities
- Guardrails for input and output validation
- Streaming support for responsive UIs
- MCP (Model Context Protocol) server integration
- Human-in-the-loop workflows for sensitive operations
- Extensions for Vercel AI SDK, Twilio, and Cloudflare Workers

## When to Use This Skill

Use this skill when encountering questions or tasks related to:

- Building agents using the OpenAI Agents SDK or @openai/agents package
- Implementing multi-agent systems, triage agents, or agent orchestration
- Setting up agent handoffs or agents-as-tools patterns
- Creating and configuring function tools for agents
- Implementing guardrails for input or output validation
- Working with realtime voice agents or the OpenAI Realtime API
- Integrating MCP servers (hosted, streamable HTTP, or stdio)
- Streaming agent responses or handling interruptions
- Managing agent context, conversation history, or state
- Configuring models, temperature, or other model settings
- Implementing human-in-the-loop approval workflows
- Debugging agents with tracing or viewing traces in the OpenAI dashboard
- Deploying agents to Cloudflare Workers or connecting to Twilio
- Using alternative models through Vercel's AI SDK adapter

## Core Concepts

The SDK is built around three main primitives:

1. **Agents** - LLMs configured with instructions, tools, and model settings
2. **Handoffs** - Delegation mechanism allowing agents to transfer conversations to specialist agents
3. **Guardrails** - Validation functions that run in parallel to check inputs and outputs

Additional key concepts include:

- **Runner** - Executes the agent loop, handling tool calls, handoffs, and model interactions
- **Tools** - Function tools, hosted tools, agents-as-tools, or MCP servers
- **Context** - Dependency injection object passed to all tools and callbacks
- **Streaming** - Incremental delivery of agent outputs as they're generated
- **Tracing** - Built-in observability for debugging and monitoring workflows
- **RealtimeAgent** - Speech-to-speech agents for voice interactions
- **RealtimeSession** - Manages ongoing voice conversations with audio handling

## Documentation Structure

The reference documentation is organized into core guides, extensions, and voice agent documentation.

### Core Guides

- [index.md](references/index.md) - SDK overview, key features, installation, and hello world example
- [quickstart.md](references/quickstart.md) - Step-by-step guide to creating your first agent with handoffs and tools
- [agents.md](references/agents.md) - Comprehensive guide to agent configuration, context types, output types, dynamic instructions, lifecycle hooks, guardrails, cloning agents, and forcing tool use
- [tools.md](references/tools.md) - Four categories of tools: hosted tools (web search, file search, computer use, code interpreter, image generation), function tools with Zod schemas, agents-as-tools, and MCP servers
- [handoffs.md](references/handoffs.md) - Creating handoffs, customizing handoff behavior, input schemas, input filters, and recommended prompts
- [multi-agent.md](references/multi-agent.md) - Orchestration patterns: LLM-driven vs code-driven orchestration, structured outputs, chaining agents, parallel execution
- [guardrails.md](references/guardrails.md) - Input and output guardrails, tripwire mechanism, implementing guardrails with agents
- [context.md](references/context.md) - Local context for dependency injection vs agent/LLM context, dynamic instructions, exposing data to the model
- [models.md](references/models.md) - Default models, GPT-5 reasoning models, model settings, authentication, prompt configuration, custom model providers
- [running-agents.md](references/running-agents.md) - Runner class, agent loop lifecycle, run arguments, streaming, conversations/chat threads, server-managed conversations, exception handling
- [human-in-the-loop.md](references/human-in-the-loop.md) - Tool approval workflows, interruption handling, serializing state for longer approval times
- [results.md](references/results.md) - Accessing final output, history, state, interruptions, guardrail results, and raw responses
- [streaming.md](references/streaming.md) - Enabling streaming, text streams, event types (raw_model_stream_event, run_item_stream_event, agent_updated_stream_event), human-in-the-loop while streaming
- [mcp.md](references/mcp.md) - Three types of MCP servers: hosted MCP tools (remote servers), streamable HTTP servers, stdio servers. Tool filtering, approval flows, connector-backed servers
- [tracing.md](references/tracing.md) - Built-in tracing, traces and spans, default tracing behavior, custom trace processors, sensitive data handling
- [config.md](references/config.md) - API key configuration, tracing setup, debug logging, sensitive data in logs
- [troubleshooting.md](references/troubleshooting.md) - Supported environments (Node.js, Deno, Bun), limited support for Cloudflare Workers and browsers, debug logging
- [release.md](references/release.md) - Versioning strategy, changelogs for sub-packages
- [voice-agents.md](references/voice-agents.md) - Overview of voice agents using speech-to-speech models, key features, WebSocket vs WebRTC connections

### Extensions

- [extensions/ai-sdk.md](references/extensions/ai-sdk.md) - Using any model through Vercel's AI SDK adapter, setup instructions, provider metadata
- [extensions/twilio.md](references/extensions/twilio.md) - Connecting realtime agents to Twilio using TwilioRealtimeTransportLayer, handling phone call audio, WebSocket server setup
- [extensions/cloudflare.md](references/extensions/cloudflare.md) - Dedicated transport for Cloudflare Workers using fetch-based WebSocket upgrades

### Voice Agents

- [voice-agents/quickstart.md](references/voice-agents/quickstart.md) - Building first voice agent, generating ephemeral tokens, RealtimeAgent and RealtimeSession setup, connecting over WebRTC
- [voice-agents/build.md](references/voice-agents/build.md) - Audio handling, session configuration, handoffs for voice agents, tools (with conversation history access, approval workflows), guardrails (running asynchronously on transcripts), turn detection/VAD, interruptions, text input, conversation history management, delegation through tools
- [voice-agents/transport.md](references/voice-agents/transport.md) - Transport layer options: WebRTC (default with automatic audio), WebSocket (manual audio handling), Cloudflare transport, building custom transports, direct Realtime API access

## Key Features Highlights

### Agent Definition and Configuration

- Define agents with name, instructions, model, tools, and guardrails
- Support for both string and function-based dynamic instructions
- Generic context types for dependency injection
- Output types using Zod schemas or JSON schemas for structured outputs
- Lifecycle hooks for observing agent execution
- Tool choice configuration (auto, required, none, or specific tool)
- Tool use behavior customization to prevent infinite loops

### Multi-Agent Orchestration

- **Manager pattern**: Central agent uses specialized agents as tools
- **Handoffs pattern**: Triage agent delegates entire conversation to specialists
- Handoff customization: input schemas, input filters, callbacks
- Input filters to control conversation history passed during handoffs
- Recommended prompt prefixes for better LLM handoff behavior

### Tool System

- **Hosted tools**: Web search, file search, computer use, code interpreter, image generation
- **Function tools**: Wrap any TypeScript function with Zod schema validation
- **Agents as tools**: Expose entire agents as callable tools
- **MCP servers**: Three integration modes (hosted, streamable HTTP, stdio)
- Tool filtering for MCP servers (static or dynamic)
- Approval workflows for sensitive tool operations

### Guardrails

- Input guardrails run on initial user input (only for first agent)
- Output guardrails run on final agent output (only for last agent)
- Tripwire mechanism for halting execution
- Can use agents internally for classification
- Run in parallel to agent execution

### Realtime Voice Agents

- Speech-to-speech models for voice interactions
- RealtimeAgent and RealtimeSession primitives
- WebRTC (automatic audio) and WebSocket (manual audio) transports
- Built-in voice activity detection and turn detection
- Interruption handling and audio truncation
- Tools, handoffs, and guardrails work with voice agents
- Text input support for multimodal interactions
- Conversation history management with transcript access
- Delegation to backend agents through tools

### Streaming and Responsiveness

- Streaming support for incremental output delivery
- Three event types: raw model events, run items, agent updates
- Text stream helpers compatible with Node.js streams
- Human-in-the-loop interruptions compatible with streaming
- Context-aware streaming with state management

### Context Management

- Local context for tools, callbacks, and lifecycle hooks
- RunContext wrapper providing access to shared state and dependencies
- Agent/LLM context through instructions, input, or retrieval tools
- Dynamic instructions based on context
- Server-managed conversations using conversationId or previousResponseId

### Tracing and Observability

- Built-in tracing enabled by default
- Automatic trace generation for runs, agents, generations, tools, guardrails, handoffs
- OpenAI dashboard integration for visualization
- Custom trace processors for alternative backends
- Sensitive data exclusion options
- Workflow naming and metadata attachment

### Model Support

- Default model: gpt-4.1 (balance of predictability and latency)
- GPT-5 reasoning models with effort and verbosity settings
- OpenAI Responses API (default) or Chat Completions API
- Custom model providers through Model and ModelProvider interfaces
- Vercel AI SDK adapter for using any model
- Model settings: temperature, top_p, penalties, truncation, maxTokens, reasoning.effort, text.verbosity

### State and Result Management

- RunResult with finalOutput, history, newItems, state, interruptions
- StreamedRunResult for streaming scenarios
- State serialization for long-running approval workflows
- Type-safe output types with Agent.create() for handoffs
- Access to raw responses, guardrail results, and original input

### Error Handling

- MaxTurnsExceededError when iteration limit reached
- ModelBehaviorError for invalid model outputs
- InputGuardrailTripwireTriggered and OutputGuardrailTripwireTriggered
- GuardrailExecutionError with state for retry logic
- ToolCallError for function tool failures
- All errors extend AgentsError with optional state property

### Extensions and Integrations

- Vercel AI SDK adapter for accessing any model provider
- Twilio integration for phone-based voice agents
- Cloudflare Workers support with dedicated transport
- MCP server support (hosted, HTTP, stdio)
- Custom transport layers for realtime connections

## Common Patterns

### Basic Agent Creation and Execution

To create and run a simple agent:
- Define Agent with name and instructions
- Use run() utility function with agent and input
- Access result.finalOutput for the response
- See [quickstart.md](references/quickstart.md)

### Multi-Agent Triage System

To orchestrate multiple specialist agents:
- Create specialist agents for each domain
- Create triage agent with handoffs array
- Use Agent.create() for type-safe handoff outputs
- Run triage agent with user input
- See [handoffs.md](references/handoffs.md)

### Adding Tools to Agents

To give agents capabilities:
- Use tool() helper with name, description, parameters (Zod schema), and execute function
- Add tools to agent's tools array
- Context available as second parameter in execute
- See [tools.md](references/tools.md)

### Implementing Guardrails

To validate agent behavior:
- Define InputGuardrail or OutputGuardrail with name and execute function
- Execute returns { outputInfo, tripwireTriggered }
- Add to agent's inputGuardrails or outputGuardrails arrays
- Catch InputGuardrailTripwireTriggered or OutputGuardrailTripwireTriggered errors
- See [guardrails.md](references/guardrails.md)

### Managing Conversations

To maintain chat history:
- Store history from result.history
- Pass accumulated history to next run() call
- Alternatively use conversationId or previousResponseId for server-managed state
- See [running-agents.md](references/running-agents.md)

### Streaming Responses

To stream agent output:
- Pass { stream: true } to run()
- Use stream.toTextStream() for text-only output
- Or iterate with for await loop for all events
- Await stream.completed before exiting
- See [streaming.md](references/streaming.md)

### Voice Agent Setup

To create a voice agent:
- Generate ephemeral client token from backend
- Create RealtimeAgent with name and instructions
- Create RealtimeSession with agent and model
- Connect with session.connect({ apiKey })
- See [voice-agents/quickstart.md](references/voice-agents/quickstart.md)

### Human-in-the-Loop Approval

To require approval for tool calls:
- Set needsApproval: true on tool definition
- Check result.interruptions for pending approvals
- Call state.approve(interruption) or state.reject(interruption)
- Resume with run(agent, state)
- See [human-in-the-loop.md](references/human-in-the-loop.md)

### Using MCP Servers

To integrate MCP tools:
- For hosted: use hostedMcpTool({ serverLabel, serverUrl })
- For stdio: use MCPServerStdio({ fullCommand })
- For HTTP: use MCPServerStreamableHttp({ url, name })
- Add to agent's mcpServers or tools array
- See [mcp.md](references/mcp.md)

### Custom Model Integration

To use non-OpenAI models:
- Install @openai/agents-extensions and desired AI SDK provider
- Import aisdk adapter and model provider
- Create model with aisdk(provider('model-name'))
- Pass model to Agent constructor
- See [extensions/ai-sdk.md](references/extensions/ai-sdk.md)

### Tracing and Debugging

To monitor agent execution:
- Tracing enabled by default, view at platform.openai.com/traces
- Set workflowName in RunConfig for grouping
- Use withTrace() for multi-run traces
- Set DEBUG=openai-agents* for verbose logs
- See [tracing.md](references/tracing.md)

## Quick Reference

- **To create an agent**: Use `new Agent({ name, instructions, tools?, model? })`
- **To run an agent**: Use `await run(agent, input)` or `await runner.run(agent, input)`
- **To add handoffs**: Set `handoffs: [agent1, agent2]` in Agent constructor
- **To create tools**: Use `tool({ name, description, parameters, execute })`
- **To enable streaming**: Pass `{ stream: true }` to run()
- **To get final output**: Access `result.finalOutput`
- **To maintain history**: Pass `result.history` to next run
- **To create voice agent**: Use `new RealtimeAgent()` and `new RealtimeSession()`
- **To view traces**: Visit https://platform.openai.com/traces
- **To handle approvals**: Check `result.interruptions` and use `state.approve/reject()`
- **To configure model**: Set `model: 'gpt-5'` or `modelSettings: { temperature: 0.7 }`
- **To add guardrails**: Set `inputGuardrails` or `outputGuardrails` array
- **To use MCP servers**: Add to `mcpServers` array or use hosted MCP tools
- **To debug**: Set `DEBUG=openai-agents*` environment variable

## Installation

```bash
npm install @openai/agents zod@3
```

For voice agents only:
```bash
npm install @openai/agents-realtime
```

For extensions:
```bash
npm install @openai/agents-extensions
```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for agent execution
- `OPENAI_DEFAULT_MODEL` - Default model to use for all agents
- `OPENAI_AGENTS_DISABLE_TRACING` - Set to 1 to disable tracing
- `OPENAI_AGENTS_DONT_LOG_MODEL_DATA` - Set to 1 to exclude LLM inputs/outputs from logs
- `OPENAI_AGENTS_DONT_LOG_TOOL_DATA` - Set to 1 to exclude tool inputs/outputs from logs
- `DEBUG` - Set to openai-agents* for verbose debug logging

## Supported Environments

- Node.js 22+
- Deno 2.35+
- Bun 1.2.5+
- Cloudflare Workers (with nodejs_compat, limited tracing, manual flush)
- Browsers (limited tracing support)
