---
title: Connect Realtime Agents to Twilio
description: Connect your Agents SDK agents to Twilio to use voice agents
---


Twilio offers a [Media Streams API](https://www.twilio.com/docs/voice/media-streams) that sends the
raw audio from a phone call to a WebSocket server. This set up can be used to connect your
[voice agents](/openai-agents-js/guides/voice-agents) to Twilio. You can use the default Realtime Session transport
in `websocket` mode to connect the events coming from Twilio to your Realtime Session. However,
this requires you to set the right audio format and adjust your own interruption timing as phone
calls will naturally introduce more latency than a web-based conversation.

To improve the set up experience, we've created a dedicated transport layer that handles the
connection to Twilio for you, including handling interruptions and audio forwarding for you.

<Aside type="caution">
  This adapter is still in beta. You may run into edge case issues or bugs.
  Please report any issues via [GitHub
  issues](https://github.com/openai/openai-agents-js/issues) and we'll fix
  quickly.
</Aside>

## Setup

1. **Make sure you have a Twilio account and a Twilio phone number.**

2. **Set up a WebSocket server that can receive events from Twilio.**

   If you are developing locally, this will require you to configure a local tunnel like
   this will require you to configure a local tunnel like [`ngrok`](https://ngrok.io/) or
   [Cloudflare Tunnel](https://developers.cloudflare.com/pages/how-to/preview-with-cloudflare-tunnel/)
   to make your local server accessible to Twilio. You can use the `TwilioRealtimeTransportLayer`
   to connect to Twilio.

3. **Install the Twilio adapter by installing the extensions package:**

   ```bash
   npm install @openai/agents-extensions
   ```

4. **Import the adapter and model to connect to your `RealtimeSession`:**

   <Code
     lang="typescript"
     code={twilioBasicExample.replace(
       /\n\s+\/\/ @ts-expect-error - this is not defined/g,
       '',
     )}
   />

5. **Connect your `RealtimeSession` to Twilio:**

   ```typescript
   session.connect({ apiKey: 'your-openai-api-key' });
   ```

Any event and behavior that you would expect from a `RealtimeSession` will work as expected
including tool calls, guardrails, and more. Read the [voice agents guide](/openai-agents-js/guides/voice-agents)
for more information on how to use the `RealtimeSession` with voice agents.

## Tips and Considerations

1. **Speed is the name of the game.**

   In order to receive all the necessary events and audio from Twilio, you should create your
   `TwilioRealtimeTransportLayer` instance as soon as you have a reference to the WebSocket
   connection and immediately call `session.connect()` afterwards.

2. **Access the raw Twilio events.**

   If you want to access the raw events that are being sent by Twilio, you can listen to the
   `transport_event` event on your `RealtimeSession` instance. Every event from Twilio will have a
   type of `twilio_message` and a `message` property that contains the raw event data.

3. **Watch debug logs.**

   Sometimes you may run into issues where you want more information on what's going on. Using
   a `DEBUG=openai-agents*` environment variable will show all the debug logs from the Agents SDK.
   Alternatively, you can enable just debug logs for the Twilio adapter using
   `DEBUG=openai-agents:extensions:twilio*`.

## Full example server

Below is an example of a full end-to-end example of a WebSocket server that receives requests from
Twilio and forwards them to a `RealtimeSession`.


**Example server using Fastify**

```typescript
import Fastify from 'fastify';
import type { FastifyInstance, FastifyReply, FastifyRequest } from 'fastify';
import dotenv from 'dotenv';
import fastifyFormBody from '@fastify/formbody';
import fastifyWs from '@fastify/websocket';
import {
  RealtimeAgent,
  RealtimeSession,
  backgroundResult,
  tool,
} from '@openai/agents/realtime';
import { TwilioRealtimeTransportLayer } from '@openai/agents-extensions';
import { hostedMcpTool } from '@openai/agents';
import { z } from 'zod';
import process from 'node:process';

// Load environment variables from .env file
dotenv.config();

// Retrieve the OpenAI API key from environment variables. You must have OpenAI Realtime API access.
const { OPENAI_API_KEY } = process.env;
if (!OPENAI_API_KEY) {
  console.error('Missing OpenAI API key. Please set it in the .env file.');
  process.exit(1);
}
const PORT = +(process.env.PORT || 5050);

// Initialize Fastify
const fastify = Fastify();
fastify.register(fastifyFormBody);
fastify.register(fastifyWs);

const weatherTool = tool({
  name: 'weather',
  description: 'Get the weather in a given location.',
  parameters: z.object({
    location: z.string(),
  }),
  execute: async ({ location }: { location: string }) => {
    return backgroundResult(`The weather in ${location} is sunny.`);
  },
});

const secretTool = tool({
  name: 'secret',
  description: 'A secret tool to tell the special number.',
  parameters: z.object({
    question: z
      .string()
      .describe(
        'The question to ask the secret tool; mainly about the special number.',
      ),
  }),
  execute: async ({ question }: { question: string }) => {
    return `The answer to ${question} is 42.`;
  },
  needsApproval: true,
});

const agent = new RealtimeAgent({
  name: 'Greeter',
  instructions:
    'You are a friendly assistant. When you use a tool always first say what you are about to do.',
  tools: [
    hostedMcpTool({
      serverLabel: 'deepwiki',
      serverUrl: 'https://mcp.deepwiki.com/sse',
    }),
    secretTool,
    weatherTool,
  ],
});

// Root Route
fastify.get('/', async (_request: FastifyRequest, reply: FastifyReply) => {
  reply.send({ message: 'Twilio Media Stream Server is running!' });
});

// Route for Twilio to handle incoming and outgoing calls
// <Say> punctuation to improve text-to-speech translation
fastify.all(
  '/incoming-call',
  async (request: FastifyRequest, reply: FastifyReply) => {
    const twimlResponse = `
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>O.K. you can start talking!</Say>
    <Connect>
        <Stream url="wss://${request.headers.host}/media-stream" />
    </Connect>
</Response>`.trim();
    reply.type('text/xml').send(twimlResponse);
  },
);

// WebSocket route for media-stream
fastify.register(async (scopedFastify: FastifyInstance) => {
  scopedFastify.get(
    '/media-stream',
    { websocket: true },
    async (connection: any) => {
      const twilioTransportLayer = new TwilioRealtimeTransportLayer({
        twilioWebSocket: connection,
      });

      const session = new RealtimeSession(agent, {
        transport: twilioTransportLayer,
        model: 'gpt-realtime',
        config: {
          audio: {
            output: {
              voice: 'verse',
            },
          },
        },
      });

      session.on('mcp_tools_changed', (tools: { name: string }[]) => {
        const toolNames = tools.map((tool) => tool.name).join(', ');
        console.log(`Available MCP tools: ${toolNames || 'None'}`);
      });

      session.on(
        'tool_approval_requested',
        (_context: unknown, _agent: unknown, approvalRequest: any) => {
          console.log(
            `Approving tool call for ${approvalRequest.approvalItem.rawItem.name}.`,
          );
          session
            .approve(approvalRequest.approvalItem)
            .catch((error: unknown) =>
              console.error('Failed to approve tool call.', error),
            );
        },
      );

      session.on(
        'mcp_tool_call_completed',
        (_context: unknown, _agent: unknown, toolCall: unknown) => {
          console.log('MCP tool call completed.', toolCall);
        },
      );

      await session.connect({
        apiKey: OPENAI_API_KEY,
      });
      console.log('Connected to the OpenAI Realtime API');
    },
  );
});

fastify.listen({ port: PORT }, (err: Error | null) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`Server is listening on port ${PORT}`);
});

process.on('SIGINT', () => {
  fastify.close();
  process.exit(0);
});

```

