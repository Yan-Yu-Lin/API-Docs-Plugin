---
title: Broadcast
subtitle: Send traces to external observability platforms
headline: Broadcast | OpenRouter Observability
canonical-url: 'https://openrouter.ai/docs/guides/features/broadcast'
'og:site_name': OpenRouter Documentation
'og:title': Broadcast - Send Traces to Observability Platforms
'og:description': >-
  Connect your LLM observability platforms to automatically receive traces from
  your OpenRouter requests. Supports Langfuse, Datadog, Braintrust, and more.
'og:image':
  type: url
  value: >-
    https://openrouter.ai/dynamic-og?title=Broadcast&description=Send%20traces%20to%20observability%20platforms
'og:image:width': 1200
'og:image:height': 630
'twitter:card': summary_large_image
'twitter:site': '@OpenRouterAI'
noindex: false
nofollow: false
---

Broadcast allows you to automatically send traces from your OpenRouter requests to external observability and analytics platforms. This feature enables you to monitor, debug, and analyze your LLM usage across your preferred tools without any additional instrumentation in your application code.

## Enabling Broadcast

To enable broadcast for your account or organization:

1. Navigate to [Settings > Broadcast](https://openrouter.ai/settings/broadcast) in your OpenRouter dashboard
2. Toggle the "Enable Broadcast" switch to turn on the feature
3. Add one or more destinations where you want to send your traces

<Tip>
If you're using an organization account, you must be an organization admin to edit broadcast settings.
</Tip>

Once enabled, OpenRouter will automatically send trace data for all your API requests to your configured destinations.

## Supported Destinations

{/* When updating this list, sync with getPublicDestinationMetadata() in packages/broadcast/registry.ts
    which filters by isActive && releaseStatus === 'stable'. See destination metadata in packages/broadcast/destinations/*.ts */}

The following destinations are currently available:

- Braintrust
- Datadog
- Langfuse
- S3
- Weave
- OTel Collector

Each destination has its own configuration requirements, such as API keys, endpoints, or project identifiers. When adding a destination, you'll be prompted to provide the necessary credentials which are encrypted and stored securely.

For the most up-to-date list of available destinations, visit the [Broadcast settings page](https://openrouter.ai/settings/broadcast) in your dashboard.

### Coming Soon

The following destinations are in development and will be available soon:

- Arize
- AWS Firehose
- Clickhouse
- Dynatrace
- Evidently
- Fiddler
- Galileo
- Grafana
- Helicone
- HoneyHive
- Keywords AI
- Langsmith
- Middleware
- Mona
- New Relic
- OpenInference
- Opik
- Phoenix
- Portkey
- PostHog
- Snowflake
- Supabase
- Webhook
- WhyLabs

## Trace Data

Each broadcast trace includes comprehensive information about your API request:

**Request & Response Data**: The input messages and model output (with multimodal content stripped for efficiency)

**Token Usage**: Prompt tokens, completion tokens, and total tokens consumed

**Cost Information**: The total cost of the request

**Timing**: Request start time, end time, and latency metrics

**Model Information**: The model slug and provider name used for the request

**Tool Usage**: Whether tools were included in the request and if tool calls were made

## User Tracking with Broadcast

To associate traces with specific end-users in your application, include the `user` field in your API requests. This identifier will be included in the broadcast trace data, allowing you to track usage patterns and debug issues for individual users.

```json
{
  "model": "openai/gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Hello, world!"
    }
  ],
  "user": "user_12345"
}
```

The `user` field accepts a string up to 128 characters. This identifier helps you distinguish between different users of your application in your observability platform, making it easier to investigate issues or analyze usage patterns per user.

## Session Tracking with Broadcast

A string up to 128 characters, this identifier is useful to group related requests together (such as a conversation or agent workflow). Just include the `session_id` field in your API requests.

```json
{
  "model": "openai/gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": "Hello, world!"
    }
  ],
  "session_id": "session_abc123"
}
```

Alternatively, you can pass the session ID via the `x-session-id` HTTP header. If provided in both the request body and the header, the body value takes precedence.

## API Key Filtering

Each destination can be configured to only receive traces from specific API keys. This is useful when you want to:
* route traces from different parts of your application to different observability platforms
* isolate monitoring for specific use cases
* or send production API key traces at a lower sampling rate than development keys

When adding or editing a destination, you can select one or more API keys from your account. Only requests made with those selected API keys will have their traces sent to that destination. If no API keys are selected, the destination will receive traces from all your API keys or chatroom requests.

## Sampling Rate

Each destination can be configured with a sampling rate to control what percentage of traces are sent. This is useful for high-volume applications where you want to reduce costs or data volume while still maintaining visibility into your LLM usage. A sampling rate of 1.0 sends all traces, while 0.5 would send approximately 50% of traces.

## Security

Your destination credentials are encrypted before being stored and are only decrypted when sending traces. Traces are sent asynchronously after requests complete, so enabling broadcast does not add latency to your API responses.

## Organization Support

Broadcast can be configured at both the individual user level and the organization level. Organization admins can set up shared destinations that apply to all API keys within the organization, ensuring consistent observability across your team.

