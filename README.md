# API-Docs Marketplace

Comprehensive marketplace for API documentation and SDK expertise skills.

## Overview

This marketplace provides Claude Code skills that contain expert knowledge about various APIs and SDKs, enabling Claude to work more effectively with different API ecosystems.

## Plugins

### OpenAI Plugin

Expert knowledge about OpenAI APIs and SDKs.

**Skills included:**
- `openai-agent-sdk` - Comprehensive knowledge of OpenAI Agent SDK

### Anthropic Plugin

Expert knowledge about Anthropic APIs and protocols.

**Skills included:**
- `model-context-protocol` - Comprehensive knowledge of Model Context Protocol (MCP)

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add Yan-Yu-Lin/API-Docs-Plugin
```

Then install plugins:

```bash
/plugin install openai@api-docs
/plugin install anthropic@api-docs
```

## Development

This marketplace is designed to be extensible. Additional API documentation plugins can be added over time.

## License

MIT
