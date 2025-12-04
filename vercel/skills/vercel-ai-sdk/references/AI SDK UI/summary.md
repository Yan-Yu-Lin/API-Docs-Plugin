# AI SDK UI - Comprehensive Summary

This document provides a detailed summary of all AI SDK UI documentation, covering the framework-agnostic toolkit for building interactive AI-powered applications.

---

## Table of Contents

1. [Overview](#overview)
2. [Chatbot (useChat)](#chatbot-usechat)
3. [Message Persistence](#message-persistence)
4. [Resume Streams](#resume-streams)
5. [Tool Usage](#tool-usage)
6. [Generative User Interfaces](#generative-user-interfaces)
7. [Completion (useCompletion)](#completion-usecompletion)
8. [Object Generation (useObject)](#object-generation-useobject)
9. [Streaming Custom Data](#streaming-custom-data)
10. [Error Handling and Warnings](#error-handling-and-warnings)
11. [Transport Configuration](#transport-configuration)
12. [Reading UI Message Streams](#reading-ui-message-streams)
13. [Message Metadata](#message-metadata)
14. [Stream Protocols](#stream-protocols)

---

## Overview

AI SDK UI is a **framework-agnostic toolkit** designed to help build interactive chat, completion, and assistant applications. It provides robust abstractions for managing chat streams and UI updates on the frontend.

### Main Hooks

- **`useChat`**: Real-time streaming of chat messages with state management for inputs, messages, loading, and errors
- **`useCompletion`**: Handles text completions with automatic UI updates as new completions stream
- **`useObject`**: Consumes streamed JSON objects for displaying structured data

### Framework Support

| Function | React | Svelte | Vue.js | Angular |
|----------|-------|--------|--------|---------|
| useChat | Yes | Yes | Yes | Yes |
| useCompletion | Yes | Yes | Yes | Yes |
| useObject | Yes | Yes | No | Yes |

---

## Chatbot (useChat)

The `useChat` hook creates conversational user interfaces with real-time message streaming.

### Key Features

- **Message Streaming**: Real-time streaming from AI providers
- **Managed States**: Automatic state management for input, messages, status, error
- **Seamless Integration**: Easy integration into any design or layout

### Basic Usage

```tsx
'use client';

import { useChat } from '@ai-sdk/react';
import { DefaultChatTransport } from 'ai';

export default function Page() {
  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({
      api: '/api/chat',
    }),
  });
  // ... component implementation
}
```

### Server-Side API Route

```ts
import { openai } from '@ai-sdk/openai';
import { convertToModelMessages, streamText, UIMessage } from 'ai';

export async function POST(req: Request) {
  const { messages }: { messages: UIMessage[] } = await req.json();

  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
}
```

### Status States

- `submitted`: Message sent, awaiting response stream
- `streaming`: Response actively streaming
- `ready`: Full response received, ready for new message
- `error`: Error occurred during request

### Key Functions

- **`setMessages`**: Modify existing messages (delete, update)
- **`stop`**: Abort the current streaming response
- **`regenerate`**: Reprocess the last message
- **`reload`**: Retry after an error

### Event Callbacks

```tsx
useChat({
  onFinish: ({ message, messages, isAbort, isDisconnect, isError }) => {
    // Handle completion
  },
  onError: error => {
    console.error('Error:', error);
  },
  onData: data => {
    console.log('Received data:', data);
  },
});
```

### Request Configuration

```tsx
// Hook-level configuration
const { messages, sendMessage } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/custom-chat',
    headers: { Authorization: 'your_token' },
    body: { user_id: '123' },
    credentials: 'same-origin',
  }),
});

// Request-level configuration (recommended)
sendMessage(
  { text: input },
  {
    headers: { Authorization: 'Bearer token123' },
    body: { temperature: 0.7 },
    metadata: { userId: 'user123' },
  },
);
```

### Throttling UI Updates

```tsx
const { messages } = useChat({
  experimental_throttle: 50  // Throttle updates to 50ms
});
```

### Features

- **Reasoning Support**: Forward reasoning tokens with `sendReasoning: true`
- **Sources**: Forward web page sources with `sendSources: true`
- **Image Generation**: Handle generated images as file parts
- **Attachments**: Send files via `FileList` or file objects

### Type Inference for Tools

```tsx
import { InferUITools, UIMessage } from 'ai';

type MyUITools = InferUITools<typeof tools>;
type MyUIMessage = UIMessage<never, UIDataTypes, MyUITools>;
```

---

## Message Persistence

Implement message storage and retrieval for chat applications.

### Creating a New Chat

```tsx
import { redirect } from 'next/navigation';
import { createChat } from '@util/chat-store';

export default async function Page() {
  const id = await createChat();
  redirect(`/chat/${id}`);
}
```

### Loading Existing Chats

```tsx
export async function loadChat(id: string): Promise<UIMessage[]> {
  return JSON.parse(await readFile(getChatFile(id), 'utf8'));
}
```

### Validating Messages

Validate messages containing tools, metadata, or data parts using `validateUIMessages`:

```tsx
const validatedMessages = await validateUIMessages({
  messages,
  tools,
  dataPartsSchema,
  metadataSchema,
});
```

### Storing Messages

Use `onFinish` callback in `toUIMessageStreamResponse`:

```tsx
return result.toUIMessageStreamResponse({
  originalMessages: messages,
  onFinish: ({ messages }) => {
    saveChat({ chatId, messages });
  },
});
```

### Server-Side ID Generation

```tsx
return result.toUIMessageStreamResponse({
  generateMessageId: createIdGenerator({
    prefix: 'msg',
    size: 16,
  }),
  // ...
});
```

### Handling Client Disconnects

Use `consumeStream` to ensure messages are saved even on disconnect:

```tsx
result.consumeStream(); // no await
return result.toUIMessageStreamResponse({
  onFinish: ({ messages }) => {
    saveChat({ chatId, messages });
  },
});
```

---

## Resume Streams

Resume ongoing streams after page reloads for long-running generations.

### Client-Side Setup

```tsx
const { messages, sendMessage, status } = useChat({
  id: chatData.id,
  messages: chatData.messages,
  resume: true, // Enable automatic stream resumption
  transport: new DefaultChatTransport({
    prepareSendMessagesRequest: ({ id, messages }) => ({
      body: { id, message: messages[messages.length - 1] },
    }),
  }),
});
```

### Server POST Handler

```ts
return result.toUIMessageStreamResponse({
  async consumeSseStream({ stream }) {
    const streamId = generateId();
    const streamContext = createResumableStreamContext({ waitUntil: after });
    await streamContext.createNewResumableStream(streamId, () => stream);
    saveChat({ id, activeStreamId: streamId });
  },
});
```

### Server GET Handler (Resume Endpoint)

```ts
export async function GET(_, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const chat = await readChat(id);

  if (chat.activeStreamId == null) {
    return new Response(null, { status: 204 });
  }

  const streamContext = createResumableStreamContext({ waitUntil: after });
  return new Response(
    await streamContext.resumeExistingStream(chat.activeStreamId),
    { headers: UI_MESSAGE_STREAM_HEADERS },
  );
}
```

### Important Considerations

- Stream resumption is **not compatible with abort** functionality
- Streams expire after a configurable time in Redis
- Multiple clients can connect to the same stream simultaneously

---

## Tool Usage

The AI SDK supports three types of tools:

1. **Server-side tools**: Automatically executed with `execute` function
2. **Client-side automatic tools**: Handled via `onToolCall` callback
3. **User interaction tools**: Displayed in UI for user confirmation

### Server-Side Tool Definition

```tsx
const result = streamText({
  model: 'anthropic/claude-sonnet-4.5',
  messages: convertToModelMessages(messages),
  tools: {
    getWeatherInformation: {
      description: 'Get weather for a city',
      inputSchema: z.object({ city: z.string() }),
      execute: async ({ city }) => {
        return ['sunny', 'cloudy', 'rainy'][Math.floor(Math.random() * 3)];
      },
    },
    askForConfirmation: {
      description: 'Ask user for confirmation',
      inputSchema: z.object({ message: z.string() }),
      // No execute = client-side tool
    },
  },
});
```

### Client-Side Tool Handling

```tsx
const { messages, sendMessage, addToolOutput } = useChat({
  sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithToolCalls,

  async onToolCall({ toolCall }) {
    if (toolCall.dynamic) return; // Check dynamic tools first

    if (toolCall.toolName === 'getLocation') {
      addToolOutput({
        tool: 'getLocation',
        toolCallId: toolCall.toolCallId,
        output: 'San Francisco',
      });
    }
  },
});
```

### Rendering Tool Parts

Tool parts use typed naming: `tool-${toolName}`

```tsx
message.parts.map(part => {
  switch (part.type) {
    case 'tool-getWeatherInformation':
      switch (part.state) {
        case 'input-streaming':
          return <div>Loading...</div>;
        case 'input-available':
          return <div>Getting weather for {part.input.city}...</div>;
        case 'output-available':
          return <div>Weather: {part.output}</div>;
        case 'output-error':
          return <div>Error: {part.errorText}</div>;
      }
  }
});
```

### Tool Call Streaming

Enabled by default in AI SDK 5.0 - partial tool calls stream in real-time.

### Dynamic Tools

Use `dynamic-tool` type for tools with unknown types at compile time:

```tsx
case 'dynamic-tool':
  return <div>Tool: {part.toolName}</div>;
```

### Server-Side Multi-Step Calls

```tsx
const result = streamText({
  tools: { /* tools with execute functions */ },
  stopWhen: stepCountIs(5),
});
```

---

## Generative User Interfaces

Connect tool results to React components for dynamic UI generation.

### Basic Flow

1. Provide model with prompt and tools
2. Model decides to call a tool
3. Tool executes and returns data
4. Data passes to React component for rendering

### Creating a Tool

```ts
// ai/tools.ts
import { tool as createTool } from 'ai';
import { z } from 'zod';

export const weatherTool = createTool({
  description: 'Display the weather for a location',
  inputSchema: z.object({
    location: z.string().describe('The location to get the weather for'),
  }),
  execute: async ({ location }) => {
    await new Promise(resolve => setTimeout(resolve, 2000));
    return { weather: 'Sunny', temperature: 75, location };
  },
});
```

### Creating UI Components

```tsx
// components/weather.tsx
export const Weather = ({ temperature, weather, location }) => (
  <div>
    <h2>Current Weather for {location}</h2>
    <p>Condition: {weather}</p>
    <p>Temperature: {temperature}C</p>
  </div>
);
```

### Rendering in Chat

```tsx
if (part.type === 'tool-displayWeather') {
  switch (part.state) {
    case 'input-available':
      return <div>Loading weather...</div>;
    case 'output-available':
      return <Weather {...part.output} />;
    case 'output-error':
      return <div>Error: {part.errorText}</div>;
  }
}
```

---

## Completion (useCompletion)

Handle text completions with streaming support.

### Basic Usage

```tsx
'use client';

import { useCompletion } from '@ai-sdk/react';

export default function Page() {
  const { completion, input, handleInputChange, handleSubmit } = useCompletion({
    api: '/api/completion',
  });

  return (
    <form onSubmit={handleSubmit}>
      <input value={input} onChange={handleInputChange} />
      <button type="submit">Submit</button>
      <div>{completion}</div>
    </form>
  );
}
```

### Key Features

- **Loading State**: `isLoading` for showing spinners
- **Error State**: `error` for displaying error messages
- **Controlled Input**: `setInput` for custom input handling
- **Cancellation**: `stop` function to abort streaming
- **Throttling**: `experimental_throttle` option

### Event Callbacks

```tsx
useCompletion({
  onResponse: (response) => { /* ... */ },
  onFinish: (prompt, completion) => { /* ... */ },
  onError: (error) => { /* ... */ },
});
```

---

## Object Generation (useObject)

Stream structured JSON objects with schema validation.

### Schema Definition

```ts
import { z } from 'zod';

export const notificationSchema = z.object({
  notifications: z.array(
    z.object({
      name: z.string().describe('Name of a fictional person.'),
      message: z.string().describe('Message content.'),
    }),
  ),
});
```

### Client Usage

```tsx
import { experimental_useObject as useObject } from '@ai-sdk/react';

const { object, submit } = useObject({
  api: '/api/notifications',
  schema: notificationSchema,
});

// Render partial results
{object?.notifications?.map((notification, index) => (
  <div key={index}>
    <p>{notification?.name}</p>
    <p>{notification?.message}</p>
  </div>
))}
```

### Server Implementation

```ts
import { streamObject } from 'ai';

export async function POST(req: Request) {
  const context = await req.json();

  const result = streamObject({
    model: 'anthropic/claude-sonnet-4.5',
    schema: notificationSchema,
    prompt: `Generate 3 notifications: ${context}`,
  });

  return result.toTextStreamResponse();
}
```

### Enum Output Mode

```tsx
// Client
const { object, submit } = useObject({
  api: '/api/classify',
  schema: z.object({ enum: z.enum(['true', 'false']) }),
});

// Server
const result = streamObject({
  model: 'anthropic/claude-sonnet-4.5',
  output: 'enum',
  enum: ['true', 'false'],
  prompt: `Classify: ${context}`,
});
```

### Key Features

- **Loading State**: `isLoading`
- **Stop Handler**: `stop()` to cancel generation
- **Error State**: `error` for error handling
- **Event Callbacks**: `onFinish`, `onError`

---

## Streaming Custom Data

Stream additional data alongside model responses using data parts.

### Setting Up Type-Safe Data

```tsx
import { UIMessage } from 'ai';

export type MyUIMessage = UIMessage<
  never, // metadata type
  {
    weather: { city: string; weather?: string; status: 'loading' | 'success' };
    notification: { message: string; level: 'info' | 'warning' | 'error' };
  }
>;
```

### Streaming Data from Server

```tsx
const stream = createUIMessageStream<MyUIMessage>({
  execute: ({ writer }) => {
    // Transient data (not added to message history)
    writer.write({
      type: 'data-notification',
      data: { message: 'Processing...', level: 'info' },
      transient: true,
    });

    // Persistent data with ID for reconciliation
    writer.write({
      type: 'data-weather',
      id: 'weather-1',
      data: { city: 'San Francisco', status: 'loading' },
    });

    // Later: update same data part
    writer.write({
      type: 'data-weather',
      id: 'weather-1', // Same ID = update
      data: { city: 'San Francisco', weather: 'sunny', status: 'success' },
    });

    writer.merge(result.toUIMessageStream());
  },
});
```

### Types of Streamable Data

1. **Data Parts (Persistent)**: Added to message history
2. **Sources**: For RAG implementations
3. **Transient Data Parts**: Only available via `onData` callback

### Data Part Reconciliation

Using the same `id` when writing updates the existing part automatically.

### Processing on Client

```tsx
const { messages } = useChat<MyUIMessage>({
  onData: dataPart => {
    if (dataPart.type === 'data-notification') {
      showToast(dataPart.data.message);
    }
  },
});

// Render persistent data parts from message.parts
{message.parts
  .filter(part => part.type === 'data-weather')
  .map((part, index) => (
    <div key={index}>Weather: {part.data.weather}</div>
  ))}
```

---

## Error Handling and Warnings

### Warnings

Warnings appear in browser console with "AI SDK Warning:" prefix:
- Unsupported settings
- Unsupported tools
- Other model issues

**Turn off warnings:**

```ts
globalThis.AI_SDK_LOG_WARNINGS = false;

// Or custom handler
globalThis.AI_SDK_LOG_WARNINGS = warnings => {
  warnings.forEach(warning => console.log('Custom:', warning));
};
```

### Error Handling

```tsx
const { messages, sendMessage, error, regenerate } = useChat();

// Display error with retry
{error && (
  <>
    <div>An error occurred.</div>
    <button onClick={() => regenerate()}>Retry</button>
  </>
)}
```

### Error Callback

```tsx
useChat({
  onError: error => {
    console.error(error);
  },
});
```

### Server-Side Error Messages

```ts
return result.toUIMessageStreamResponse({
  onError: error => {
    if (error instanceof Error) return error.message;
    return 'unknown error';
  },
});
```

---

## Transport Configuration

Fine-grained control over message transmission and response processing.

### Default Transport

```tsx
import { DefaultChatTransport } from 'ai';

const { messages, sendMessage } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/chat',
  }),
});
```

### Custom Configuration

```tsx
const { messages, sendMessage } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/custom-chat',
    headers: { Authorization: 'Bearer token' },
    credentials: 'include',
  }),
});
```

### Dynamic Configuration

```tsx
transport: new DefaultChatTransport({
  headers: () => ({
    Authorization: `Bearer ${getAuthToken()}`,
  }),
  body: () => ({
    sessionId: getCurrentSessionId(),
  }),
}),
```

### Request Transformation

```tsx
transport: new DefaultChatTransport({
  prepareSendMessagesRequest: ({ id, messages, trigger, messageId }) => ({
    headers: { 'X-Session-ID': id },
    body: {
      messages: messages.slice(-10), // Only last 10 messages
      trigger,
      messageId,
    },
  }),
}),
```

### Building Custom Transports

Reference implementations:
- `DefaultChatTransport`: Complete default HTTP transport
- `HttpChatTransport`: Base HTTP transport
- `ChatTransport Interface`: Interface to implement

---

## Reading UI Message Streams

Consume `UIMessage` streams outside traditional chat UIs.

### Basic Usage

```tsx
import { readUIMessageStream, streamText } from 'ai';

async function main() {
  const result = streamText({
    model: 'anthropic/claude-sonnet-4.5',
    prompt: 'Write a short story about a robot.',
  });

  for await (const uiMessage of readUIMessageStream({
    stream: result.toUIMessageStream(),
  })) {
    console.log('Current message state:', uiMessage);
  }
}
```

### Tool Calls Integration

```tsx
for await (const uiMessage of readUIMessageStream({
  stream: result.toUIMessageStream(),
})) {
  uiMessage.parts.forEach(part => {
    switch (part.type) {
      case 'text':
        console.log('Text:', part.text);
        break;
      case 'tool-call':
        console.log('Tool:', part.toolName, part.args);
        break;
      case 'tool-result':
        console.log('Result:', part.result);
        break;
    }
  });
}
```

### Resuming Conversations

```tsx
for await (const uiMessage of readUIMessageStream({
  stream: result.toUIMessageStream(),
  message: lastMessage, // Resume from this message
})) {
  // Process resumed messages
}
```

---

## Message Metadata

Attach custom information at the message level.

### Defining Metadata Types

```tsx
import { UIMessage } from 'ai';
import { z } from 'zod';

export const messageMetadataSchema = z.object({
  createdAt: z.number().optional(),
  model: z.string().optional(),
  totalTokens: z.number().optional(),
});

export type MessageMetadata = z.infer<typeof messageMetadataSchema>;
export type MyUIMessage = UIMessage<MessageMetadata>;
```

### Sending from Server

```ts
return result.toUIMessageStreamResponse({
  messageMetadata: ({ part }) => {
    if (part.type === 'start') {
      return { createdAt: Date.now(), model: 'gpt-5.1' };
    }
    if (part.type === 'finish') {
      return { totalTokens: part.totalUsage.totalTokens };
    }
  },
});
```

### Accessing on Client

```tsx
const { messages } = useChat<MyUIMessage>();

{messages.map(message => (
  <div key={message.id}>
    {message.metadata?.createdAt && (
      <span>{new Date(message.metadata.createdAt).toLocaleTimeString()}</span>
    )}
    {message.metadata?.totalTokens && (
      <span>{message.metadata.totalTokens} tokens</span>
    )}
  </div>
))}
```

### Common Use Cases

- Timestamps
- Model information
- Token usage
- User context
- Performance metrics
- Quality indicators

---

## Stream Protocols

### Text Stream Protocol

Plain text chunks streamed and appended together.

```tsx
// Client
const { messages, sendMessage } = useChat({
  transport: new TextStreamChatTransport({ api: '/api/chat' }),
});

// Server
return result.toTextStreamResponse();
```

### Data Stream Protocol (UI Message Stream)

Uses Server-Sent Events (SSE) format with structured message parts.

**Required Header**: `x-vercel-ai-ui-message-stream: v1`

### Stream Parts

| Part Type | Description |
|-----------|-------------|
| `start` | Beginning of a new message |
| `text-start/delta/end` | Text content streaming |
| `reasoning-start/delta/end` | Reasoning content streaming |
| `source-url` | URL references |
| `source-document` | Document references |
| `file` | File references |
| `data-*` | Custom data parts |
| `error` | Error information |
| `tool-input-start/delta/available` | Tool input streaming |
| `tool-output-available` | Tool execution results |
| `start-step` | Step beginning marker |
| `finish-step` | Step completion marker |
| `finish` | Message completion |
| `[DONE]` | Stream termination |

### Example Data Stream Events

```
data: {"type":"start","messageId":"..."}
data: {"type":"text-delta","id":"...","delta":"Hello"}
data: {"type":"tool-input-available","toolCallId":"...","toolName":"weather","input":{"city":"SF"}}
data: {"type":"finish"}
data: [DONE]
```

### Server Implementation

```ts
return result.toUIMessageStreamResponse();
```

---

## Key API Patterns

### Converting Messages

```ts
import { convertToModelMessages } from 'ai';

const modelMessages = convertToModelMessages(uiMessages);
```

### Creating Streams

```ts
import { createUIMessageStream, createUIMessageStreamResponse } from 'ai';

const stream = createUIMessageStream({ execute: ({ writer }) => { /* ... */ } });
return createUIMessageStreamResponse({ stream });
```

### ID Generation

```ts
import { createIdGenerator, generateId } from 'ai';

const customId = createIdGenerator({ prefix: 'msg', size: 16 });
const simpleId = generateId();
```

---

This summary covers all major aspects of AI SDK UI, providing a comprehensive reference for building AI-powered applications with React, Svelte, Vue.js, and Angular frameworks.
