# Vercel AI SDK Agents - Comprehensive Summary

This document summarizes the key concepts, patterns, and API usage for building agents with the Vercel AI SDK.

---

## Overview: What Are Agents?

Agents are **large language models (LLMs)** that use **tools** in a **loop** to accomplish tasks. The three core components are:

1. **LLMs** - Process input and decide the next action
2. **Tools** - Extend capabilities beyond text generation (reading files, calling APIs, writing to databases)
3. **Loop** - Orchestrates execution through context management and stopping conditions

---

## The Agent Class

The `Agent` class is the recommended approach for building agents with the AI SDK. It provides:

- **Reduced boilerplate** - Manages loops and message arrays automatically
- **Improved reusability** - Define once, use throughout your application
- **Simplified maintenance** - Single place to update agent configuration
- **Full TypeScript support** - Type safety for tools and outputs

### Basic Agent Creation

```ts
import { Experimental_Agent as Agent, stepCountIs, tool } from 'ai';
import { z } from 'zod';

const myAgent = new Agent({
  model: 'anthropic/claude-sonnet-4.5',
  system: 'You are a helpful assistant.',
  tools: {
    // Your tools here
  },
  stopWhen: stepCountIs(20),
});
```

### Configuration Options

The Agent class accepts the same settings as `generateText` and `streamText`:

- **model** - The LLM model to use
- **system** - System prompt defining agent behavior
- **tools** - Available tools for the agent
- **toolChoice** - Control how tools are used (`'auto'`, `'required'`, `'none'`, or specific tool)
- **stopWhen** - Stopping conditions for the agent loop
- **experimental_output** - Structured output schemas

---

## Defining Tools

Tools extend agent capabilities. Define them with descriptions, input schemas, and execute functions:

```ts
import { tool } from 'ai';
import { z } from 'zod';

const weatherTool = tool({
  description: 'Get the weather in a location',
  inputSchema: z.object({
    location: z.string().describe('The location to get weather for'),
  }),
  execute: async ({ location }) => ({
    location,
    temperature: 72,
  }),
});
```

### Tool Choice Options

```ts
// Let the model decide (default)
toolChoice: 'auto'

// Force tool use
toolChoice: 'required'

// Disable tools
toolChoice: 'none'

// Force a specific tool
toolChoice: { type: 'tool', toolName: 'weather' }
```

---

## System Prompts

System prompts define agent behavior, personality, and constraints. Best practices include:

### Role and Expertise

```ts
system: 'You are an expert data analyst. You provide clear insights from complex data.'
```

### Behavioral Instructions

```ts
system: `You are a senior software engineer conducting code reviews.

Your approach:
- Focus on security vulnerabilities first
- Identify performance bottlenecks
- Suggest improvements for readability
- Be constructive and educational`
```

### Constraints and Rules

```ts
system: `You are a customer support specialist.

Rules:
- Never make promises about refunds without checking policy
- Always be empathetic and professional
- If you don't know something, offer to escalate`
```

### Tool Usage Guidance

```ts
system: `When researching:
1. Always start with a broad search
2. Use document analysis for detailed information
3. Cross-reference multiple sources
4. Cite your sources`
```

---

## Using Agents

### Generate Text (One-time)

```ts
const result = await myAgent.generate({
  prompt: 'What is the weather like?',
});
console.log(result.text);
console.log(result.steps);
```

### Stream Text

```ts
const stream = myAgent.stream({
  prompt: 'Tell me a story',
});

for await (const chunk of stream.textStream) {
  console.log(chunk);
}
```

### Respond to UI Messages (API Routes)

```ts
import { validateUIMessages } from 'ai';

export async function POST(request: Request) {
  const { messages } = await request.json();
  return myAgent.respond({
    messages: await validateUIMessages({ messages }),
  });
}
```

---

## Structured Output

Define structured output schemas using Zod:

```ts
import { Output } from 'ai';

const analysisAgent = new Agent({
  model: 'anthropic/claude-sonnet-4.5',
  experimental_output: Output.object({
    schema: z.object({
      sentiment: z.enum(['positive', 'neutral', 'negative']),
      summary: z.string(),
      keyPoints: z.array(z.string()),
    }),
  }),
  stopWhen: stepCountIs(10),
});

const { experimental_output: output } = await analysisAgent.generate({
  prompt: 'Analyze customer feedback',
});
```

---

## Type Safety

Infer types for agent UI messages:

```ts
import {
  Experimental_Agent as Agent,
  Experimental_InferAgentUIMessage as InferAgentUIMessage,
} from 'ai';

const myAgent = new Agent({ /* config */ });
export type MyAgentUIMessage = InferAgentUIMessage<typeof myAgent>;
```

Use in client components:

```tsx
import { useChat } from '@ai-sdk/react';
import type { MyAgentUIMessage } from '@/agent/my-agent';

export function Chat() {
  const { messages } = useChat<MyAgentUIMessage>();
  // Full type safety
}
```

---

## Loop Control

### Stop Conditions

Control when agents stop execution using `stopWhen`:

#### Built-in Conditions

```ts
import { stepCountIs, hasToolCall } from 'ai';

// Stop after maximum steps
stopWhen: stepCountIs(20)

// Stop after calling a specific tool
stopWhen: hasToolCall('someTool')

// Combine multiple conditions (stops when ANY is met)
stopWhen: [
  stepCountIs(20),
  hasToolCall('someTool'),
]
```

#### Custom Conditions

```ts
import { StopCondition, ToolSet } from 'ai';

const hasAnswer: StopCondition<typeof tools> = ({ steps }) => {
  return steps.some(step => step.text?.includes('ANSWER:')) ?? false;
};

// Budget-based stopping
const budgetExceeded: StopCondition<typeof tools> = ({ steps }) => {
  const totalUsage = steps.reduce(
    (acc, step) => ({
      inputTokens: acc.inputTokens + (step.usage?.inputTokens ?? 0),
      outputTokens: acc.outputTokens + (step.usage?.outputTokens ?? 0),
    }),
    { inputTokens: 0, outputTokens: 0 },
  );
  const costEstimate =
    (totalUsage.inputTokens * 0.01 + totalUsage.outputTokens * 0.03) / 1000;
  return costEstimate > 0.5;
};
```

### Prepare Step

The `prepareStep` callback runs before each step, allowing dynamic modifications:

#### Dynamic Model Selection

```ts
prepareStep: async ({ stepNumber, messages }) => {
  if (stepNumber > 2 && messages.length > 10) {
    return { model: 'anthropic/claude-sonnet-4.5' };
  }
  return {};
}
```

#### Context Management

```ts
prepareStep: async ({ messages }) => {
  if (messages.length > 20) {
    return {
      messages: [
        messages[0], // Keep system message
        ...messages.slice(-10), // Keep last 10
      ],
    };
  }
  return {};
}
```

#### Tool Selection by Phase

```ts
prepareStep: async ({ stepNumber }) => {
  if (stepNumber <= 2) {
    return { activeTools: ['search'], toolChoice: 'required' };
  }
  if (stepNumber <= 5) {
    return { activeTools: ['analyze'] };
  }
  return { activeTools: ['summarize'], toolChoice: 'required' };
}
```

#### Message Modification

```ts
prepareStep: async ({ messages }) => {
  const processedMessages = messages.map(msg => {
    if (msg.role === 'tool' && msg.content.length > 1000) {
      return { ...msg, content: summarizeToolResult(msg.content) };
    }
    return msg;
  });
  return { messages: processedMessages };
}
```

### Step Information Available

Both `stopWhen` and `prepareStep` receive:

- `model` - Current model configuration
- `stepNumber` - Current step (0-indexed)
- `steps` - All previous steps with results
- `messages` - Messages to be sent to model

---

## Workflow Patterns

For structured, reliable outcomes with explicit control flow, use core functions with workflow patterns.

### Choosing an Approach

Consider:

- **Flexibility vs Control** - How much freedom does the LLM need?
- **Error Tolerance** - What are consequences of mistakes?
- **Cost Considerations** - More complexity = more LLM calls
- **Maintenance** - Simpler architectures are easier to debug

**Start simple, add complexity only when needed.**

### Sequential Processing (Chains)

Execute steps in predefined order, where each output becomes the next input:

```ts
import { generateText, generateObject } from 'ai';

async function generateMarketingCopy(input: string) {
  // Step 1: Generate copy
  const { text: copy } = await generateText({
    model: 'openai/gpt-4o',
    prompt: `Write marketing copy for: ${input}`,
  });

  // Step 2: Quality check
  const { object: qualityMetrics } = await generateObject({
    model: 'openai/gpt-4o',
    schema: z.object({
      hasCallToAction: z.boolean(),
      emotionalAppeal: z.number().min(1).max(10),
      clarity: z.number().min(1).max(10),
    }),
    prompt: `Evaluate this copy: ${copy}`,
  });

  // Step 3: Conditionally improve
  if (!qualityMetrics.hasCallToAction || qualityMetrics.emotionalAppeal < 7) {
    const { text: improvedCopy } = await generateText({
      model: 'openai/gpt-4o',
      prompt: `Improve this copy: ${copy}`,
    });
    return { copy: improvedCopy, qualityMetrics };
  }

  return { copy, qualityMetrics };
}
```

### Routing

Let the model decide which path to take based on context:

```ts
async function handleCustomerQuery(query: string) {
  // Classify the query
  const { object: classification } = await generateObject({
    model: 'openai/gpt-4o',
    schema: z.object({
      type: z.enum(['general', 'refund', 'technical']),
      complexity: z.enum(['simple', 'complex']),
    }),
    prompt: `Classify: ${query}`,
  });

  // Route based on classification
  const { text: response } = await generateText({
    model: classification.complexity === 'simple'
      ? 'openai/gpt-4o-mini'
      : 'openai/o4-mini',
    system: {
      general: 'Customer service for general inquiries.',
      refund: 'Refund specialist. Follow company policy.',
      technical: 'Technical support. Step-by-step troubleshooting.',
    }[classification.type],
    prompt: query,
  });

  return { response, classification };
}
```

### Parallel Processing

Execute independent subtasks simultaneously:

```ts
async function parallelCodeReview(code: string) {
  const [securityReview, performanceReview, maintainabilityReview] =
    await Promise.all([
      generateObject({
        model: 'openai/gpt-4o',
        system: 'Security expert. Identify vulnerabilities.',
        schema: z.object({
          vulnerabilities: z.array(z.string()),
          riskLevel: z.enum(['low', 'medium', 'high']),
        }),
        prompt: `Review: ${code}`,
      }),
      generateObject({
        model: 'openai/gpt-4o',
        system: 'Performance expert. Identify bottlenecks.',
        schema: z.object({
          issues: z.array(z.string()),
          impact: z.enum(['low', 'medium', 'high']),
        }),
        prompt: `Review: ${code}`,
      }),
      generateObject({
        model: 'openai/gpt-4o',
        system: 'Code quality expert.',
        schema: z.object({
          concerns: z.array(z.string()),
          qualityScore: z.number().min(1).max(10),
        }),
        prompt: `Review: ${code}`,
      }),
    ]);

  // Aggregate results
  const { text: summary } = await generateText({
    model: 'openai/gpt-4o',
    prompt: `Synthesize reviews: ${JSON.stringify([
      securityReview.object,
      performanceReview.object,
      maintainabilityReview.object,
    ])}`,
  });

  return { reviews: [securityReview, performanceReview, maintainabilityReview], summary };
}
```

### Orchestrator-Worker

A primary model coordinates specialized workers:

```ts
async function implementFeature(featureRequest: string) {
  // Orchestrator: Plan
  const { object: plan } = await generateObject({
    model: 'openai/o4-mini',
    system: 'Senior architect planning implementations.',
    schema: z.object({
      files: z.array(z.object({
        purpose: z.string(),
        filePath: z.string(),
        changeType: z.enum(['create', 'modify', 'delete']),
      })),
    }),
    prompt: `Plan: ${featureRequest}`,
  });

  // Workers: Execute changes
  const fileChanges = await Promise.all(
    plan.files.map(async file => {
      const workerPrompt = {
        create: 'Expert at implementing new files.',
        modify: 'Expert at modifying existing code.',
        delete: 'Expert at safely removing code.',
      }[file.changeType];

      const { object: change } = await generateObject({
        model: 'anthropic/claude-sonnet-4.5',
        system: workerPrompt,
        schema: z.object({ explanation: z.string(), code: z.string() }),
        prompt: `Implement ${file.filePath}: ${file.purpose}`,
      });

      return { file, implementation: change };
    }),
  );

  return { plan, changes: fileChanges };
}
```

### Evaluator-Optimizer

Add quality control with iterative improvement:

```ts
async function translateWithFeedback(text: string, targetLanguage: string) {
  let currentTranslation = '';
  let iterations = 0;
  const MAX_ITERATIONS = 3;

  // Initial translation (small model)
  const { text: translation } = await generateText({
    model: 'openai/gpt-4o-mini',
    prompt: `Translate to ${targetLanguage}: ${text}`,
  });
  currentTranslation = translation;

  // Evaluation-optimization loop
  while (iterations < MAX_ITERATIONS) {
    // Evaluate (larger model)
    const { object: evaluation } = await generateObject({
      model: 'anthropic/claude-sonnet-4.5',
      schema: z.object({
        qualityScore: z.number().min(1).max(10),
        preservesTone: z.boolean(),
        specificIssues: z.array(z.string()),
      }),
      prompt: `Evaluate translation: Original: ${text}, Translation: ${currentTranslation}`,
    });

    if (evaluation.qualityScore >= 8 && evaluation.preservesTone) {
      break;
    }

    // Improve based on feedback
    const { text: improved } = await generateText({
      model: 'anthropic/claude-sonnet-4.5',
      prompt: `Improve translation based on: ${evaluation.specificIssues.join(', ')}
      Original: ${text}, Current: ${currentTranslation}`,
    });

    currentTranslation = improved;
    iterations++;
  }

  return { finalTranslation: currentTranslation, iterationsRequired: iterations };
}
```

---

## Manual Loop Control

For complete control, implement your own loop with core functions:

```ts
import { generateText, ModelMessage } from 'ai';

const messages: ModelMessage[] = [{ role: 'user', content: '...' }];
let step = 0;
const maxSteps = 10;

while (step < maxSteps) {
  const result = await generateText({
    model: 'anthropic/claude-sonnet-4.5',
    messages,
    tools: { /* your tools */ },
  });

  messages.push(...result.response.messages);

  if (result.text) {
    break; // Stop when model generates text
  }

  step++;
}
```

This approach provides complete control over:

- Message history management
- Step-by-step decision making
- Custom stopping conditions
- Dynamic tool and model selection
- Error handling and recovery

---

## Key Takeaways

1. **Start with the Agent class** for most use cases - it handles boilerplate and provides a clean API
2. **Use workflow patterns** when you need deterministic, structured outcomes
3. **Configure stop conditions** to prevent runaway loops and control costs
4. **Use prepareStep** for dynamic behavior based on execution history
5. **Combine patterns** - sequential, parallel, routing, orchestration, and evaluation can work together
6. **Start simple** - add complexity only when required
7. **Consider cost and latency** - more steps and larger models increase both
