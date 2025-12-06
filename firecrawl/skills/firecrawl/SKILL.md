---
name: firecrawl
description: >-
  Comprehensive documentation for the Firecrawl API, a powerful web scraping, crawling, and data
  extraction service. This skill should be used when working with Firecrawl's API endpoints
  including /scrape, /crawl, /map, /search, /extract, and /batch-scrape. Covers web scraping
  with JavaScript rendering, converting websites to LLM-ready markdown, extracting structured
  JSON data with schemas, batch processing multiple URLs, recursive website crawling, URL
  discovery and mapping, web search with content retrieval, browser actions (click, scroll,
  wait, type), PDF/document parsing, change tracking, caching strategies, proxy and stealth
  mode configuration, webhook integration, MCP server setup for Claude Code and Cursor, and
  integrations with LLM frameworks (LangChain, Vercel AI SDK, LlamaIndex) and workflow
  automation platforms (Zapier, Make, n8n, Dify). Use this skill for any Firecrawl-related
  tasks, web data extraction, or building AI applications that need web content access.
---

# Firecrawl

Firecrawl is an API service that converts websites into LLM-ready data. It crawls accessible
subpages and returns clean markdown, structured JSON, HTML, screenshots, and metadata. No
sitemap is required. Firecrawl handles the hard parts: proxies, anti-bot mechanisms, dynamic
JavaScript content, and output parsing.

## Core Capabilities

- **Scrape**: Extract content from a single URL in multiple formats
- **Batch Scrape**: Process multiple URLs efficiently with parallel execution
- **Crawl**: Recursively traverse websites, discovering and scraping subpages
- **Map**: Quickly discover all URLs on a website without scraping content
- **Search**: Perform web searches and optionally scrape results
- **Extract**: Use LLM to extract structured data with prompts or JSON schemas

## Quick Start

### Installation

```python
# Python
pip install firecrawl-py

from firecrawl import Firecrawl
firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
```

```javascript
// Node.js
npm install @mendable/firecrawl-js

import Firecrawl from '@mendable/firecrawl-js';
const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });
```

### Basic Scraping

```python
# Python
doc = firecrawl.scrape("https://example.com", formats=["markdown", "html"])
print(doc.markdown)
```

```javascript
// Node.js
const doc = await firecrawl.scrape('https://example.com', { formats: ['markdown', 'html'] });
console.log(doc.markdown);
```

```bash
# cURL
curl -X POST "https://api.firecrawl.dev/v2/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "formats": ["markdown", "html"]}'
```

---

## Scrape Endpoint

The `/scrape` endpoint extracts content from a single URL with extensive customization options.

### Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | URL to scrape |
| `formats` | array | `["markdown"]` | Output formats: `markdown`, `html`, `rawHtml`, `links`, `summary`, `images`, or objects for `json`/`screenshot`/`changeTracking` |
| `onlyMainContent` | boolean | `true` | Return only main content, excluding navigation/footers |
| `includeTags` | array | - | HTML tags/classes/IDs to include |
| `excludeTags` | array | - | HTML tags/classes/IDs to exclude |
| `waitFor` | integer | `0` | Extra milliseconds to wait before scraping |
| `maxAge` | integer | `172800000` | Cache freshness in ms (default 2 days). Set `0` for fresh scrape |
| `timeout` | integer | `30000` | Request timeout in milliseconds |
| `actions` | array | - | Browser actions before scraping |
| `parsers` | array | - | Document parsers, e.g., `["pdf"]` |
| `proxy` | string | - | `basic`, `stealth`, or `auto` |
| `location` | object | - | Geographic location: `{ country: "US", languages: ["en"] }` |

### Browser Actions

Execute browser interactions before scraping dynamic content:

```python
doc = firecrawl.scrape("https://example.com", actions=[
    {"type": "wait", "milliseconds": 1000},
    {"type": "click", "selector": "#accept-cookies"},
    {"type": "scroll", "direction": "down"},
    {"type": "write", "selector": "#search", "text": "query"},
    {"type": "press", "key": "Enter"},
    {"type": "screenshot", "fullPage": True}
])
```

Supported action types: `wait`, `click`, `write`, `press`, `scroll`, `scrape`, `executeJavascript`, `generatePDF`

### JSON Mode (Structured Extraction)

Extract structured data using a prompt or JSON schema:

```python
from pydantic import BaseModel

class ProductInfo(BaseModel):
    name: str
    price: float
    description: str

result = firecrawl.scrape('https://example.com/product', formats=[{
    "type": "json",
    "schema": ProductInfo.model_json_schema(),
    "prompt": "Extract product information"  # Optional
}])
print(result.json)
```

JSON extraction costs 4 additional credits per page.

### Screenshot Options

```javascript
const doc = await firecrawl.scrape('https://example.com', {
  formats: [{
    type: 'screenshot',
    fullPage: true,
    quality: 80,
    viewport: { width: 1280, height: 800 }
  }]
});
```

---

## Batch Scrape

Process multiple URLs efficiently with built-in rate limiting and parallel execution.

```python
# Start and wait for completion
results = firecrawl.batch_scrape([
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
], formats=["markdown"], poll_interval=2)

# Or start async and check status
job = firecrawl.start_batch_scrape(urls, formats=["markdown"])
status = firecrawl.get_batch_scrape_status(job.id)
```

Webhook events: `batch_scrape.started`, `batch_scrape.page`, `batch_scrape.completed`, `batch_scrape.failed`

---

## Crawl Endpoint

Recursively crawl a website, discovering and scraping all accessible subpages.

### Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | Starting URL |
| `limit` | integer | `10000` | Maximum pages to crawl |
| `maxDiscoveryDepth` | integer | - | Maximum depth for URL discovery |
| `includePaths` | array | - | Regex patterns to include, e.g., `["^/blog/.*$"]` |
| `excludePaths` | array | - | Regex patterns to exclude |
| `crawlEntireDomain` | boolean | `false` | Explore siblings/parents of starting URL |
| `allowSubdomains` | boolean | `false` | Follow subdomains |
| `allowExternalLinks` | boolean | `false` | Follow external domains |
| `scrapeOptions` | object | - | Options passed to scraper for each page |

### Usage

```python
# Start and wait
docs = firecrawl.crawl("https://docs.example.com", limit=50)

# Or start async
job = firecrawl.start_crawl("https://docs.example.com", limit=50)
status = firecrawl.get_crawl_status(job.id)
```

### WebSocket Watcher (Node.js)

```javascript
const watcher = firecrawl.watcher(jobId, { kind: 'crawl', pollInterval: 2 });
watcher.on('document', (doc) => console.log('Scraped:', doc.url));
watcher.on('done', (state) => console.log('Completed:', state.status));
await watcher.start();
```

---

## Map Endpoint

Discover all URLs on a website without scraping content. Extremely fast for URL enumeration.

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | Website to map |
| `limit` | integer | `100` | Maximum URLs to return |
| `search` | string | - | Filter URLs containing text |
| `sitemap` | string | `"include"` | `include`, `skip`, or `only` |
| `includeSubdomains` | boolean | `true` | Include subdomains |

```python
urls = firecrawl.map("https://example.com", limit=500, search="blog")
print(f"Found {len(urls)} URLs")
```

---

## Search Endpoint

Perform web searches and optionally scrape content from results.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search query (supports operators) |
| `limit` | integer | Number of results |
| `sources` | array | `web`, `news`, `images` |
| `location` | string | Geographic location |
| `tbs` | string | Time filter: `qdr:h` (hour), `qdr:d` (day), `qdr:w` (week), `qdr:m` (month), `qdr:y` (year) |
| `scrapeOptions` | object | Options for scraping results |

### Search Operators

- `"exact phrase"` - Non-fuzzy match
- `-keyword` - Exclude term
- `site:domain.com` - Site-specific search
- `intitle:word` - Title contains word

```python
results = firecrawl.search(
    query="firecrawl web scraping",
    limit=5,
    sources=[{"type": "web"}, {"type": "news"}]
)
```

Cost: 2 credits per 10 search results, plus scraping costs if `scrapeOptions` enabled.

---

## Extract Endpoint

Use LLMs to extract structured data from web pages. Supports wildcards for domain-wide extraction.

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `urls` | array | URLs to extract from; supports wildcards (`example.com/*`) |
| `prompt` | string | Natural language description of desired data |
| `schema` | object | JSON schema defining output structure |
| `enableWebSearch` | boolean | Follow external links for enriched results |

```python
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "pricing_plans": {"type": "array", "items": {"type": "object"}}
    }
}

result = firecrawl.extract(
    urls=["https://example.com/*"],
    prompt="Extract company name and pricing plans",
    schema=schema
)
```

### Async Pattern

```python
job = firecrawl.start_extract(urls, prompt=prompt)
status = firecrawl.get_extract_status(job.id)  # States: processing, completed, failed
```

### FIRE-1 Agent

For complex extraction requiring browser navigation:

```bash
curl -X POST https://api.firecrawl.dev/v2/extract \
  -H 'Authorization: Bearer YOUR_API_KEY' \
  -d '{
    "urls": ["https://example.com"],
    "prompt": "Extract all user comments",
    "agent": { "model": "FIRE-1" }
  }'
```

---

## Performance Optimization

### Caching with maxAge

Use caching for faster responses (up to 500% improvement):

| Duration | Value (ms) |
|----------|------------|
| 5 minutes | 300000 |
| 1 hour | 3600000 |
| 1 day | 86400000 |
| 1 week | 604800000 |

```python
# Use cache (default: 2 days)
doc = firecrawl.scrape(url, max_age=3600000)  # 1 hour cache

# Force fresh scrape
doc = firecrawl.scrape(url, max_age=0)

# Skip storing in cache
doc = firecrawl.scrape(url, store_in_cache=False)
```

### Proxies and Stealth Mode

| Proxy Type | Description | Cost |
|------------|-------------|------|
| `basic` | Fast, minimal protection bypass | Standard |
| `stealth` | Advanced anti-bot bypass, slower | 5 credits |
| `auto` | Try basic, retry with stealth on failure | Variable |

Stealth mode available in US, AU, BR regions.

---

## Change Tracking

Monitor content changes between scrapes:

```javascript
const result = await firecrawl.scrape('https://example.com', {
  formats: ['markdown', { type: 'changeTracking', modes: ['git-diff'] }]
});

console.log(result.changeTracking.changeStatus);
// Values: 'new', 'same', 'changed', 'removed'
```

Modes: `git-diff` (line-by-line) or `json` (structured field comparison, 5 credits).

---

## Document Parsing

Firecrawl automatically parses documents based on URL extension:

- **PDF** (`.pdf`) - Text extraction with OCR support (1 credit/page)
- **Excel** (`.xlsx`, `.xls`) - Each sheet becomes HTML table
- **Word** (`.docx`, `.doc`, `.odt`, `.rtf`) - Preserves structure

```python
doc = firecrawl.scrape("https://example.com/report.pdf", parsers=["pdf"])
```

---

## Webhooks

Configure webhooks for real-time notifications on crawl, batch scrape, and extract operations.

### Configuration

```json
{
  "webhook": {
    "url": "https://your-domain.com/webhook",
    "headers": { "X-Custom-Header": "value" },
    "metadata": { "job_name": "daily_crawl" },
    "events": ["started", "page", "completed", "failed"]
  }
}
```

### Signature Verification

Verify webhook authenticity with HMAC-SHA256:

```javascript
import crypto from 'crypto';

const signature = req.get('X-Firecrawl-Signature');
const expectedSignature = crypto
  .createHmac('sha256', process.env.FIRECRAWL_WEBHOOK_SECRET)
  .update(req.body)  // Use raw body, not parsed JSON
  .digest('hex');

if (!crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(expectedSignature, 'hex'))) {
  return res.status(401).send('Invalid signature');
}
```

---

## MCP Server Integration

Firecrawl provides an MCP server for AI coding assistants.

### Claude Code

```bash
claude mcp add firecrawl -e FIRECRAWL_API_KEY=your-api-key -- npx -y firecrawl-mcp
```

### Cursor / Windsurf

Add to MCP configuration:

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

### Remote Hosted URL

```
https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/mcp
```

---

## Rate Limits

### Concurrent Browsers by Plan

| Plan | Concurrent Browsers |
|------|---------------------|
| Free | 2 |
| Hobby | 5 |
| Standard | 50 |
| Growth | 100 |
| Scale/Enterprise | 150+ |

### API Requests per Minute

| Plan | /scrape | /map | /search | /crawl | /extract |
|------|---------|------|---------|--------|----------|
| Free | 10 | 10 | 1 | 5 | 10 |
| Hobby | 100 | 100 | 15 | 50 | 100 |
| Standard | 500 | 500 | 50 | 250 | 500 |
| Growth | 5000 | 5000 | 250 | 2500 | 1000 |

---

## SDK Method Reference (v2)

### JavaScript/TypeScript

| Operation | Start + Wait | Start Async | Check Status |
|-----------|--------------|-------------|--------------|
| Scrape | `scrape(url, opts?)` | - | - |
| Batch | `batchScrape(urls, opts?)` | `startBatchScrape(urls, opts?)` | `getBatchScrapeStatus(id)` |
| Crawl | `crawl(url, opts?)` | `startCrawl(url, opts?)` | `getCrawlStatus(id)` |
| Map | `map(url, opts?)` | - | - |
| Search | `search(query, opts?)` | - | - |
| Extract | `extract(args)` | `startExtract(args)` | `getExtractStatus(id)` |

### Python

| Operation | Start + Wait | Start Async | Check Status |
|-----------|--------------|-------------|--------------|
| Scrape | `scrape(url, **opts)` | - | - |
| Batch | `batch_scrape(urls, **opts)` | `start_batch_scrape(urls, **opts)` | `get_batch_scrape_status(id)` |
| Crawl | `crawl(url, **opts)` | `start_crawl(url, **opts)` | `get_crawl_status(id)` |
| Map | `map(url, **opts)` | - | - |
| Search | `search(query, **opts)` | - | - |
| Extract | `extract(**args)` | `start_extract(**args)` | `get_extract_status(id)` |

---

## Common Patterns

### Web Research Agent

```python
# Search, then scrape relevant results
results = firecrawl.search("latest AI developments", limit=5)
for result in results.web:
    doc = firecrawl.scrape(result.url, formats=["markdown", "summary"])
    print(doc.summary)
```

### RAG Pipeline

```python
# Crawl documentation and prepare for embeddings
docs = firecrawl.crawl("https://docs.example.com",
    limit=100,
    scrape_options={"formats": ["markdown"], "only_main_content": True}
)
for doc in docs:
    # Process for vector store
    chunks = split_into_chunks(doc.markdown)
    embeddings = generate_embeddings(chunks)
```

### Price Monitoring

```python
schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "price": {"type": "number"},
        "availability": {"type": "string"}
    }
}

result = firecrawl.scrape('https://store.example.com/product', formats=[{
    "type": "json",
    "schema": schema
}])
```

---

## References Navigation

This skill includes detailed reference documentation organized by topic:

### Standard Features (`references/Standard Features/`)
Core endpoint documentation for scrape, batch scrape, crawl, map, and search operations.
- `Scrape/` - Scrape endpoint options, JSON mode, change tracking, caching, proxies, document parsing
- `Crawl.md` - Recursive crawling with WebSocket and webhook support
- `Map.md` - Fast URL discovery
- `Search.md` - Web search with operators and content scraping

**When to look here**: Working with core API endpoints, understanding parameters, format options, or troubleshooting scrape/crawl operations.

### Agentic Features (`references/Agentic Features/`)
LLM-powered extraction with the `/extract` endpoint.
- `Extract.md` - Schema-based and prompt-based extraction, FIRE-1 agent, job status management

**When to look here**: Implementing structured data extraction, using LLM to parse web content, or working with the FIRE-1 AI agent.

### Developer Guides (`references/Developer Guides/`)
Integration guides and tutorials for building applications with Firecrawl.
- `LLM SDKs and Frameworks/` - OpenAI, Anthropic, LangChain, LangGraph, Vercel AI SDK, Gemini, Mastra, LlamaIndex, Google ADK
- `MCP Setup Guides/` - Cursor, Claude Code, Windsurf, Factory AI configuration
- `WorkFlow Automation/` - Zapier, Make, n8n, Dify integrations
- `Common Sites/` - Site-specific guides for Wikipedia, Amazon, GitHub, Etsy
- `Advanced Guides/` - Authenticated scraping with cookies
- `Cookbooks/` - Full-stack tutorials (AI Research Assistant)
- `Full-Stack Templates.md` - Production-ready example applications

**When to look here**: Integrating Firecrawl with LLM frameworks, setting up MCP servers in IDEs, connecting to automation platforms, or looking for complete example projects.

### Use Cases (`references/Use Cases/`)
Domain-specific implementations and templates.
- `AI Platforms.md` - RAG chatbots, AI assistants
- `Deep Research.md` - Multi-source research automation
- `Lead Enrichment.md` - CRM data enrichment
- `SEO Platforms.md` - AI readability optimization
- `View More/` - Competitive intelligence, content generation, e-commerce, finance, monitoring, data migration

**When to look here**: Building specific applications, finding GitHub templates, or understanding how Firecrawl applies to business use cases.

### Webhooks (`references/Webhooks/`)
Real-time event notifications for async operations.
- `Overview.md` - Configuration and setup
- `Event Types.md` - Payload structures for all events
- `Security.md` - HMAC-SHA256 signature verification
- `Testing & Debugging.md` - Local development with Cloudflare Tunnels

**When to look here**: Implementing webhook handlers, verifying signatures, or debugging webhook delivery.

### Contributing (`references/Contributing/`)
Self-hosting and local development guides.
- `Self-hosting.md` - Docker deployment, Kubernetes
- `Running locally.md` - Local development setup
- `OpenSource vs Cloud.md` - Feature comparison

**When to look here**: Self-hosting Firecrawl, contributing to the project, or understanding open-source vs cloud differences.

### Root Reference Files
- `QuickStart.md` - Getting started guide with all endpoints
- `Rate Limits.md` - API rate limits and concurrent browser limits by plan
- `Advanced Scraping Guide.md` - Detailed scrape/crawl parameter reference
- `Firecrawl MCP Server.md` - Complete MCP server documentation
- `Migrating from v1 to v2.md` - SDK migration guide and method mappings

**When to look here**: Initial setup, understanding limits, advanced configuration, or migrating from v1 API.

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Rate limited | Check plan limits, use `maxAge` caching, implement backoff |
| Blocked by anti-bot | Use `proxy: "stealth"` or `proxy: "auto"` |
| Dynamic content not loading | Add `actions` with `wait` and `scroll` |
| PDF not parsing | Set `parsers: ["pdf"]` explicitly |
| Crawl missing pages | Adjust `maxDiscoveryDepth`, check `includePaths`/`excludePaths` |
| Webhook not receiving | Verify HTTPS URL, check signature verification with raw body |

### Error Handling

```python
try:
    doc = firecrawl.scrape(url)
except Exception as e:
    if "rate limit" in str(e).lower():
        time.sleep(60)
        doc = firecrawl.scrape(url)
    elif "timeout" in str(e).lower():
        doc = firecrawl.scrape(url, timeout=60000)
```

---

## API Base URL

```
https://api.firecrawl.dev/v2/
```

Get API key: https://firecrawl.dev/app/api-keys

Documentation: https://docs.firecrawl.dev
