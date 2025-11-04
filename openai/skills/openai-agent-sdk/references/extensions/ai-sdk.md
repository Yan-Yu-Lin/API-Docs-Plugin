---
title: Using any model with the Vercel's AI SDK
description: Connect your Agents SDK agents to any model through the Vercel's AI SDK
---


<Aside type="caution">
  This adapter is still in beta. You may run into issues with some model
  providers, especially smaller ones. Please report any issues via [GitHub
  issues](https://github.com/openai/openai-agents-js/issues) and we'll fix
  quickly.
</Aside>

Out of the box the Agents SDK works with OpenAI models through the Responses API or Chat Completions API. However, if you would like to use another model, the [Vercel's AI SDK](https://sdk.vercel.ai/) offers a range of supported models that can be brought into the Agents SDK through this adapter.

## Setup

1. Install the AI SDK adapter by installing the extensions package:

   ```bash
   npm install @openai/agents-extensions
   ```

2. Choose your desired model package from the [Vercel's AI SDK](https://ai-sdk.dev/docs/foundations/providers-and-models) and install it:

   ```bash
   npm install @ai-sdk/openai
   ```

3. Import the adapter and model to connect to your agent:

   ```typescript
   ```

4. Initialize an instance of the model to be used by the agent:

   ```typescript
   const model = aisdk(openai('gpt-5-mini'));
   ```

<Aside type="caution">
  We currently support ai-sdk's model provider v2 modules, which are compatible
  with Vercel AI SDK v5. If you have a specific reason to continue using the v1
  model providers, you can copy the module from
  [examples/ai-sdk-v1](https://github.com/openai/openai-agents-js/tree/main/examples/ai-sdk-v1)
  and include it in your project.
</Aside>

## Example


**AI SDK Setup**

```typescript
import { Agent, run } from '@openai/agents';

// Import the model package you installed
import { openai } from '@ai-sdk/openai';

// Import the adapter
import { aisdk } from '@openai/agents-extensions';

// Create a model instance to be used by the agent
const model = aisdk(openai('gpt-5-mini'));

// Create an agent with the model
const agent = new Agent({
  name: 'My Agent',
  instructions: 'You are a helpful assistant.',
  model,
});

// Run the agent with the new model
run(agent, 'What is the capital of Germany?');

```


## Passing provider metadata

If you need to send provider-specific options with a message, pass them through `providerMetadata`. The values are forwarded directly to the underlying AI SDK model. For example, the following `providerData` in the Agents SDK

```ts
providerData: {
  anthropic: {
    cacheControl: {
      type: 'ephemeral';
    }
  }
}
```

would become

```ts
providerMetadata: {
  anthropic: {
    cacheControl: {
      type: 'ephemeral';
    }
  }
}
```

when using the AI SDK integration.
