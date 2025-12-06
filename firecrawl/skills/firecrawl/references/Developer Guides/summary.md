# Developer Guides Summary

> Comprehensive guides for integrating Firecrawl with LLM frameworks, workflow automation platforms, MCP clients, and common scraping scenarios.

## Contents

| File/Folder | Description |
|-------------|-------------|
| `Full-Stack Templates.md` | Official example apps with RAG chatbots, research assistants, and SaaS starters |
| `Advanced Guides/` | Authenticated scraping with cookies (1 file) |
| `Cookbooks/` | Step-by-step tutorial for building AI research assistant (1 file) |
| `LLM SDKs and Frameworks/` | Integration guides for 9 LLM providers and frameworks |
| `Common Sites/` | Site-specific scraping guides for Wikipedia, Amazon, GitHub, Etsy (4 files) |
| `MCP Setup Guides/` | MCP server setup for Cursor, Claude Code, Windsurf, Factory AI (4 files) |
| `WorkFlow Automation/` | Integration guides for Zapier, Make, n8n, Dify (4 files) |

---

## Key Concepts

Firecrawl provides multiple integration paths for AI applications. The **LLM SDKs** section covers direct integrations with providers like OpenAI, Anthropic, Google Gemini, and frameworks like LangChain, LangGraph, Vercel AI SDK, Mastra, and LlamaIndex. These enable scrape-and-summarize patterns, tool calling, structured extraction, and RAG workflows.

The **MCP (Model Context Protocol)** integration allows AI assistants in Cursor, Claude Code, Windsurf, and Factory AI to access Firecrawl's web scraping and search capabilities directly. This provides real-time web access without custom code.

For **no-code automation**, Firecrawl integrates with Zapier (8,000+ apps), Make (3,000+ apps), n8n (self-hostable), and Dify (LLM app platform). These platforms enable scheduled scraping, data enrichment, and AI-powered workflows.

---

## LLM SDK Integrations

### Vercel AI SDK

Pre-built tools package for AI SDK v5 with scrape, search, map, crawl, batch scrape, and extract operations.

| Tool | Description |
|------|-------------|
| `scrapeTool` | Scrape single URL |
| `searchTool` | Search the web |
| `mapTool` | Discover URLs on site |
| `crawlTool` | Crawl multiple pages |
| `batchScrapeTool` | Scrape multiple URLs |
| `extractTool` | Extract structured data |

```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import { scrapeTool, searchTool } from 'firecrawl-aisdk';

const { text } = await generateText({
  model: openai('gpt-5-mini'),
  prompt: 'Search for Firecrawl and summarize',
  tools: { search: searchTool, scrape: scrapeTool },
});
```

**Source:** `LLM SDKs and Frameworks/Vercel AI SDK.md`

---

### OpenAI Integration

Supports scrape + summarize, function calling, structured outputs, search + analyze, and Responses API with MCP.

```typescript
const tools = [{
  type: 'function' as const,
  function: {
    name: 'scrape_website',
    description: 'Scrape content from any website URL',
    parameters: z.toJSONSchema(ScrapeArgsSchema)
  }
}];

const response = await openai.chat.completions.create({
  model: 'gpt-5-nano',
  messages: [{ role: 'user', content: 'What is Firecrawl?' }],
  tools
});
```

**Source:** `LLM SDKs and Frameworks/OpenAI.md`

---

### Anthropic (Claude)

Integrates with Claude for tool use and structured extraction with Zod schemas.

**Key Patterns:**
- Scrape + Summarize with `claude-haiku-4-5`
- Tool use with `zodToJsonSchema` for input validation
- JSON extraction with pre-filled assistant response

**Source:** `LLM SDKs and Frameworks/Anthropic.md`

---

### LangChain & LangGraph

| Framework | Key Feature |
|-----------|-------------|
| LangChain | Chains, tool calling, `DynamicStructuredTool`, `withStructuredOutput` |
| LangGraph | StateGraph workflows with scrape/analyze nodes |

**Source:** `LLM SDKs and Frameworks/LangChain.md`, `LLM SDKs and Frameworks/LangGraph.md`

---

### Other Frameworks

| Framework | Key Use Case |
|-----------|--------------|
| **Gemini** | Multi-turn chat, JSON mode extraction |
| **Mastra** | Multi-step workflows with search/scrape/summarize |
| **LlamaIndex** | RAG with vector search and embeddings |
| **Google ADK** | MCP integration for AI agents |

**Source:** `LLM SDKs and Frameworks/Gemini.md`, `LLM SDKs and Frameworks/Mastra.md`, `LLM SDKs and Frameworks/LlamaInde.md`, `LLM SDKs and Frameworks/Agent Development Kit (ADK).md`

---

## MCP Setup Guides

Quick setup for adding Firecrawl to AI coding assistants via Model Context Protocol.

| Client | Setup Command/Config |
|--------|---------------------|
| **Claude Code** | `claude mcp add firecrawl -e FIRECRAWL_API_KEY=key -- npx -y firecrawl-mcp` |
| **Cursor** | Add to MCP settings JSON |
| **Windsurf** | Add to `./codeium/windsurf/model_config.json` |
| **Factory AI** | `/mcp add firecrawl "npx -y firecrawl-mcp" -e FIRECRAWL_API_KEY=key` |

**MCP Server JSON Config:**
```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": { "FIRECRAWL_API_KEY": "YOUR_API_KEY" }
    }
  }
}
```

**Source:** `MCP Setup Guides/MCP Web Search & Scrape in Cursor.md`, `MCP Setup Guides/MCP Web Search & Scrape in Claude Code.md`, `MCP Setup Guides/MCP Web Search & Scrape in Windsurf.md`, `MCP Setup Guides/MCP Web Search & Scrape in Factory AI.md`

---

## Workflow Automation Platforms

### Platform Comparison

| Feature | Zapier | Make | n8n | Dify |
|---------|--------|------|-----|------|
| Type | No-code cloud | Visual builder | Self-hosted/cloud | LLM app platform |
| Integrations | 8,000+ apps | 3,000+ apps | 400+ | Plugins |
| Best For | Quick automation | Visual workflows | Developer control | AI agents/chatbots |
| Firecrawl Actions | Scrape, Crawl, Extract, Search, Map | Same + API Call | Node-based | Scrape, Crawl, Map |

### Common Actions

| Action | Use Case |
|--------|----------|
| **Scrape URL** | Single-page data capture |
| **Crawl Website** | Full site with multiple pages |
| **Extract Data** | AI-powered structured extraction |
| **Search Web** | Research automation |
| **Map Website** | URL discovery, SEO analysis |

**Source:** `WorkFlow Automation/Firecrawl + Zapier.md`, `WorkFlow Automation/Firecrawl + Make.md`, `WorkFlow Automation/Firecrawl + n8n.md`, `WorkFlow Automation/Firecrawl + Dify.md`

---

## Common Sites Scraping

All guides follow consistent patterns: Search, Scrape, Map, Crawl, Batch Scrape, JSON mode extraction.

| Site | Use Cases | JSON Schema Fields |
|------|-----------|-------------------|
| **Wikipedia** | Knowledge graphs, research, fact-checking | `name`, `creator`, `firstAppeared`, `typingDiscipline` |
| **Amazon** | Price monitoring, product data, reviews | `title`, `price`, `rating`, `availability`, `features` |
| **GitHub** | Repository stats, documentation | `name`, `description`, `stars`, `forks`, `language`, `topics` |
| **Etsy** | Product listings, shop data | `title`, `price`, `shopName`, `rating` |

**Example JSON Mode Scrape:**
```typescript
const result = await firecrawl.scrape(url, {
  formats: [{
    type: 'json',
    schema: z.object({
      title: z.string(),
      price: z.string(),
      rating: z.number()
    })
  }]
});
```

**Source:** `Common Sites/Scraping Wikipedia.md`, `Common Sites/Scraping Amazon.md`, `Common Sites/Scraping GitHub.md`, `Common Sites/Scraping Etsy.md`

---

## Advanced Topics

### Authenticated Scraping

Cookie-based authentication for scraping protected content on authorized systems.

**Steps:**
1. Login manually and extract session cookie from DevTools
2. Pass cookie in headers: `headers: { Cookie: 'auth-token=VALUE' }`
3. Use `waitFor` option for dynamic content loading

**Best Practices:**
- Store cookies in environment variables
- Check expiration times (internal tools: 7-30 days)
- Handle 401/403 errors for expired cookies

**Source:** `Advanced Guides/Authenticated Scraping.md`

---

### Full-Stack Templates

| Template | Use Case | GitHub |
|----------|----------|--------|
| Open Lovable | RAG-powered chatbot | `firecrawl/open-lovable` |
| Open Agent Builder | AI agents with scraping | `firecrawl/open-agent-builder` |
| Fireplexity | AI search with citations | `firecrawl/fireplexity` |
| FireGEO | SaaS with brand monitoring | `firecrawl/firegeo` |
| Fire Enrich | Email to rich dataset | `firecrawl/fire-enrich` |
| Firesearch | Deep research with citations | `firecrawl/firesearch` |
| Firestarter | Website chatbot creator | `firecrawl/firestarter` |
| Open Researcher | Web research assistant | `firecrawl/open-researcher` |

**Source:** `Full-Stack Templates.md`

---

### AI Research Assistant Cookbook

Complete Next.js tutorial building a chat interface with Firecrawl tools and Vercel AI SDK.

**Stack:** Next.js + AI SDK + AI Elements + Firecrawl

**Key Components:**
1. Frontend with `useChat` hook and AI Elements components
2. API route with `streamText` and Firecrawl tools
3. Web search toggle for tool activation

```typescript
const result = streamText({
  model: openai(model),
  messages: convertToModelMessages(messages),
  tools: {
    scrapeWebsite: scrapeWebsiteTool,
    searchWeb: searchWebTool,
  },
  stopWhen: stepCountIs(5),
  toolChoice: webSearch ? "auto" : "none",
});
```

**Source:** `Cookbooks/Building an AI Research Assistant with Firecrawl and AI SDK.md`

---

## File Reference

For detailed information:

**LLM Integrations:**
- `LLM SDKs and Frameworks/Vercel AI SDK.md` - Pre-built tools, streaming examples
- `LLM SDKs and Frameworks/OpenAI.md` - Function calling, structured outputs, MCP
- `LLM SDKs and Frameworks/Anthropic.md` - Claude tool use, extraction
- `LLM SDKs and Frameworks/LangChain.md` - Chains, structured output
- `LLM SDKs and Frameworks/LangGraph.md` - StateGraph workflows
- `LLM SDKs and Frameworks/Gemini.md` - Multi-turn, JSON mode
- `LLM SDKs and Frameworks/Mastra.md` - Multi-step workflows
- `LLM SDKs and Frameworks/LlamaInde.md` - RAG with vector search
- `LLM SDKs and Frameworks/Agent Development Kit (ADK).md` - Google ADK MCP

**MCP Setup:**
- `MCP Setup Guides/MCP Web Search & Scrape in Cursor.md` - Cursor configuration
- `MCP Setup Guides/MCP Web Search & Scrape in Claude Code.md` - Claude Code CLI
- `MCP Setup Guides/MCP Web Search & Scrape in Windsurf.md` - Windsurf config
- `MCP Setup Guides/MCP Web Search & Scrape in Factory AI.md` - Factory AI CLI

**Workflow Automation:**
- `WorkFlow Automation/Firecrawl + Zapier.md` - Zapier integrations, templates
- `WorkFlow Automation/Firecrawl + Make.md` - Make modules, patterns
- `WorkFlow Automation/Firecrawl + n8n.md` - Complete n8n tutorial with Telegram
- `WorkFlow Automation/Firecrawl + Dify.md` - Dify plugin for AI workflows

**Site-Specific:**
- `Common Sites/Scraping Wikipedia.md` - Knowledge extraction
- `Common Sites/Scraping Amazon.md` - E-commerce product data
- `Common Sites/Scraping GitHub.md` - Repository statistics
- `Common Sites/Scraping Etsy.md` - Marketplace listings

**Advanced:**
- `Advanced Guides/Authenticated Scraping.md` - Cookie-based auth
- `Cookbooks/Building an AI Research Assistant with Firecrawl and AI SDK.md` - Full tutorial
- `Full-Stack Templates.md` - Production-ready example apps
