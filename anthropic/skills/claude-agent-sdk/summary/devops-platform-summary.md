# Claude Agent SDK: DevOps & Platform Guide

A comprehensive summary of hosting, security, cost tracking, and session management for deploying and operating Claude agents in production.

---

## 1. Hosting Options and Deployment Patterns

### Overview

The Claude Agent SDK differs from traditional stateless LLM APIs by maintaining conversational state and executing commands in a persistent environment. This requires careful consideration of hosting architecture.

### System Requirements

Each SDK instance requires:

| Resource | Requirement |
|----------|-------------|
| Runtime | Python 3.10+ or Node.js 18+ |
| CLI | `npm install -g @anthropic-ai/claude-code` |
| Memory | Recommended 1 GiB RAM |
| Disk | 5 GiB |
| CPU | 1 CPU (adjust based on task) |
| Network | Outbound HTTPS to `api.anthropic.com` |

### Sandbox Providers

Several providers specialize in secure container environments for AI code execution:

- **Modal Sandbox** - With demo implementation available
- **Cloudflare Sandboxes**
- **Daytona**
- **E2B**
- **Fly Machines**
- **Vercel Sandbox**

For self-hosted options: Docker, gVisor, or Firecracker.

### Deployment Patterns

#### Pattern 1: Ephemeral Sessions

Create a new container per task, destroy when complete.

**Best for:** One-off tasks like bug investigation, invoice processing, translation, or media processing.

#### Pattern 2: Long-Running Sessions

Maintain persistent container instances, often running multiple agent processes.

**Best for:** Proactive agents (email monitors), site builders with live editing, high-frequency chat bots.

#### Pattern 3: Hybrid Sessions

Ephemeral containers hydrated with history and state from databases or session resumption features.

**Best for:** Intermittent interactions like project management, deep research tasks, or multi-interaction support tickets.

#### Pattern 4: Single Containers

Multiple SDK processes in one global container.

**Best for:** Agent collaboration scenarios like simulations. Requires preventing agents from overwriting each other.

### Cost Considerations

- Container costs are roughly 5 cents per hour running (minimum)
- Token costs typically dominate overall serving costs
- Tune idle timeouts based on expected user response frequency

---

## 2. Security Best Practices for Production

### Threat Model

Agents can take unintended actions due to:
- **Prompt injection**: Instructions embedded in processed content
- **Model errors**: Unintended behavior from the model

Defense in depth is recommended even though Claude models are designed to resist prompt injection.

### Built-in Security Features

1. **Permissions System**: Configure tools and bash commands to allow, block, or prompt for approval using glob patterns
2. **Static Analysis**: Identifies potentially risky operations before execution
3. **Web Search Summarization**: Reduces prompt injection risk from raw web content
4. **Sandbox Mode**: Restricts filesystem and network access

### Security Principles

#### Security Boundaries

Place sensitive resources (credentials) outside the agent's boundary. Use a proxy pattern where the agent never sees actual credentials.

#### Least Privilege

| Resource | Restriction Options |
|----------|---------------------|
| Filesystem | Mount only needed directories, prefer read-only |
| Network | Restrict to specific endpoints via proxy |
| Credentials | Inject via proxy rather than exposing directly |
| System capabilities | Drop Linux capabilities in containers |

### Isolation Technologies

| Technology | Isolation Strength | Performance Overhead | Complexity |
|------------|-------------------|---------------------|------------|
| Sandbox runtime | Good | Very low | Low |
| Containers (Docker) | Setup dependent | Low | Medium |
| gVisor | Excellent | Medium/High | Medium |
| VMs (Firecracker, QEMU) | Excellent | High | Medium/High |

#### Sandbox Runtime

Install with: `npm install @anthropic-ai/sandbox-runtime`

Uses OS primitives (bubblewrap on Linux, sandbox-exec on macOS) for filesystem and network restrictions.

#### Hardened Docker Configuration

```bash
docker run \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --security-opt seccomp=/path/to/seccomp-profile.json \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=100m \
  --network none \
  --memory 2g \
  --cpus 2 \
  --pids-limit 100 \
  --user 1000:1000 \
  -v /path/to/code:/workspace:ro \
  -v /var/run/proxy.sock:/var/run/proxy.sock:ro \
  agent-image
```

Key options:
- `--cap-drop ALL`: Remove all Linux capabilities
- `--network none`: Remove network interfaces; use Unix socket for communication
- `--read-only`: Immutable root filesystem
- `--user`: Run as non-root

#### gVisor

Intercepts system calls in userspace, reducing kernel attack surface. Configure with:

```json
{
  "runtimes": {
    "runsc": {
      "path": "/usr/local/bin/runsc"
    }
  }
}
```

Run with: `docker run --runtime=runsc agent-image`

### Credential Management

#### The Proxy Pattern (Recommended)

1. Agent sends requests without credentials
2. Proxy (outside agent boundary) adds credentials
3. Proxy forwards to destination
4. Agent never sees actual credentials

Configure via:
- `ANTHROPIC_BASE_URL` for sampling API requests
- `HTTP_PROXY` / `HTTPS_PROXY` for system-wide traffic

#### Proxy Options

- **Envoy Proxy**: Production-grade with `credential_injector` filter
- **mitmproxy**: TLS-terminating for HTTPS inspection
- **Squid**: Caching proxy with ACLs
- **LiteLLM**: LLM gateway with rate limiting

### Filesystem Configuration

**Files to exclude when mounting:**

| File | Risk |
|------|------|
| `.env`, `.env.local` | API keys, database passwords |
| `~/.git-credentials` | Git tokens in plaintext |
| `~/.aws/credentials` | AWS access keys |
| `~/.config/gcloud/` | Google Cloud credentials |
| `~/.kube/config` | Kubernetes credentials |
| `*.pem`, `*.key` | Private keys |

Use `tmpfs` for ephemeral workspaces:

```bash
--tmpfs /workspace:rw,noexec,size=500m
```

---

## 3. Cost Tracking and Usage Monitoring

### Key Concepts

- **Steps**: A single request/response pair between application and Claude
- **Messages**: Individual messages within a step (text, tool uses, tool results)
- **Usage**: Token consumption data attached to assistant messages

### Important Usage Rules

1. **Same ID = Same Usage**: All messages with the same `id` report identical usage
2. **Charge Once Per Step**: Only charge once per unique message ID, not per message
3. **Result Message Contains Cumulative Usage**: Final result has total usage from all steps
4. **Per-Model Breakdown**: `modelUsage` provides authoritative per-model data

### Usage Fields Reference

| Field | Description |
|-------|-------------|
| `input_tokens` | Base input tokens processed |
| `output_tokens` | Tokens generated in response |
| `cache_creation_input_tokens` | Tokens used to create cache entries |
| `cache_read_input_tokens` | Tokens read from cache |
| `service_tier` | Service tier used (e.g., "standard") |
| `total_cost_usd` | Total cost in USD (result message only) |

### Model Usage Type

```typescript
type ModelUsage = {
  inputTokens: number
  outputTokens: number
  cacheReadInputTokens: number
  cacheCreationInputTokens: number
  webSearchRequests: number
  costUSD: number
  contextWindow: number
}
```

### Implementation Pattern

```typescript
class CostTracker {
  private processedMessageIds = new Set<string>();

  processMessage(message: any) {
    if (message.type !== 'assistant' || !message.usage) return;
    if (this.processedMessageIds.has(message.id)) return;

    this.processedMessageIds.add(message.id);
    // Record usage here
  }
}
```

### Best Practices

1. **Use Message IDs for Deduplication**: Track processed IDs to avoid double-charging
2. **Monitor the Result Message**: Contains authoritative cumulative usage
3. **Implement Logging**: Log all usage data for auditing
4. **Handle Failures Gracefully**: Track partial usage even if conversation fails
5. **Consider Streaming**: Accumulate usage as messages arrive

### Edge Cases

- **Output Token Discrepancies**: Use the highest value; verify against `total_cost_usd`
- **Cache Token Tracking**: Track `cache_creation_input_tokens` and `cache_read_input_tokens` separately

---

## 4. Session Management and Persistence

### How Sessions Work

The SDK automatically creates a session and returns a session ID in the initial system message. This ID enables conversation resumption.

### Getting the Session ID

```typescript
for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;
  }
}
```

### Resuming Sessions

Use the `resume` option with a session ID:

```typescript
const response = query({
  prompt: "Continue where we left off",
  options: {
    resume: "session-xyz"
  }
});
```

The SDK automatically loads conversation history and context.

### Forking Sessions

Create a new branch from an existing session without modifying the original.

| Behavior | `forkSession: false` (default) | `forkSession: true` |
|----------|-------------------------------|---------------------|
| Session ID | Same as original | New session ID generated |
| History | Appends to original | Creates new branch |
| Original Session | Modified | Preserved unchanged |
| Use Case | Continue linear conversation | Branch for alternatives |

#### When to Fork

- Explore different approaches from the same starting point
- Create multiple conversation branches
- Test changes without affecting original history
- Maintain separate paths for experiments

### Example: Forking

```typescript
// Fork to try a different approach
const forkedResponse = query({
  prompt: "Let's try a different approach",
  options: {
    resume: originalSessionId,
    forkSession: true
  }
});

// Original session remains unchanged
const continuedOriginal = query({
  prompt: "Continue original approach",
  options: {
    resume: originalSessionId,
    forkSession: false
  }
});
```

---

## Quick Reference

### Recommended Architecture for Production

```
+------------------+     +------------------+     +------------------+
|   Application    |---->|      Proxy       |---->|   Anthropic API  |
+------------------+     | (credential      |     +------------------+
                         |  injection,      |
                         |  domain allow-   |
                         |  list, logging)  |
                         +------------------+
                                ^
                                |
                         +------+------+
                         |             |
                    +----+----+  +-----+-----+
                    | Agent   |  | Agent     |
                    | Container| | Container |
                    | (isolated)| | (isolated)|
                    +----------+ +-----------+
```

### Key Takeaways

1. **Isolation**: Use container-based sandboxing with appropriate isolation technology for your threat model
2. **Credentials**: Never expose directly to agents; use proxy pattern
3. **Network**: Default to `--network none`; route through controlled proxy
4. **Filesystem**: Mount read-only; use tmpfs for ephemeral work
5. **Costs**: Track by unique message ID; use `total_cost_usd` as authoritative
6. **Sessions**: Use forking for branching experiments; resume for continuity
