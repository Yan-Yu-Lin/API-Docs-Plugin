# Agentic Features Summary

> LLM-powered structured data extraction from web pages with optional AI agent navigation

## Contents

| File | Description |
|------|-------------|
| `Extract.md` | Complete guide to the `/extract` endpoint for structured data extraction using LLMs |

---

## Key Concepts

The Agentic Features in Firecrawl center around the `/extract` endpoint, which uses LLMs to extract structured data from web pages. Unlike traditional scraping that returns raw content, extraction produces clean, structured JSON based on a schema or natural language prompt.

The endpoint supports wildcards for domain-wide extraction (e.g., `example.com/*`), enabling automated crawling and parsing of multiple pages. Web search can be enabled to enrich results with data from linked external pages.

For complex extraction tasks requiring browser interaction, FIRE-1 is an AI agent that can navigate pages, click elements, and handle dynamic content that traditional scrapers cannot access.

---

## Extract Endpoint

### Overview

The `/extract` endpoint simplifies collecting structured data from URLs or entire domains. Provide URLs (with optional wildcards), a prompt or JSON schema, and Firecrawl handles crawling, parsing, and collating the results.

### Key Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `urls` | Yes | Array of URLs; supports wildcards (`/*`) |
| `prompt` | If no schema | Natural language description of desired data |
| `schema` | If no prompt | JSON schema defining output structure |
| `enableWebSearch` | No | Follow external links for enriched results |

### Basic Usage

```python
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

schema = {
    "type": "object",
    "properties": {"description": {"type": "string"}},
    "required": ["description"],
}

res = firecrawl.extract(
    urls=["https://docs.firecrawl.dev"],
    prompt="Extract the page description",
    schema=schema,
)
```

### Response Format

```json
{
  "success": true,
  "data": {
    "company_mission": "...",
    "supports_sso": false,
    "is_open_source": true
  }
}
```

**Source:** `Extract.md`

---

## Job Status Management

### Overview

Extraction jobs return a Job ID for tracking progress. Use the SDK's wait methods or poll the status endpoint directly.

### Job States

| State | Description |
|-------|-------------|
| `completed` | Extraction finished successfully |
| `processing` | Job still running |
| `failed` | Error occurred |
| `cancelled` | User cancelled job |

### Async Pattern

```python
# Start job without waiting
extract_job = firecrawl.start_extract(
    ['https://docs.firecrawl.dev/*'],
    prompt="Extract company features"
)

# Poll for status
job_status = firecrawl.get_extract_status(extract_job.id)
```

**Source:** `Extract.md`

---

## Extraction Modes

### Schema-Based Extraction

Provide a JSON schema for rigid, predictable output structure:

```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "price": { "type": "number" }
  },
  "required": ["title", "price"]
}
```

### Prompt-Only Extraction

Let the LLM determine structure for exploratory requests:

```python
data = firecrawl.extract(
    ['https://docs.firecrawl.dev/'],
    prompt="Extract Firecrawl's mission from the page."
)
```

### URL-Less Extraction (Alpha)

Extract data using only a prompt without specifying URLs:

```python
result = firecrawl.extract(
    prompt="Extract the company mission from Firecrawl's website.",
    schema=ExtractSchema
)
```

**Source:** `Extract.md`

---

## Web Search Enhancement

### Overview

Enable `enableWebSearch` to expand crawling beyond provided URLs, gathering enriched context from linked pages.

### Usage

```python
data = firecrawl.extract(
    ['https://example.com/product'],
    prompt="Extract product details including reviews",
    enable_web_search=True
)
```

**Source:** `Extract.md`

---

## FIRE-1 Agent

### Overview

FIRE-1 is an AI agent for complex extraction requiring browser navigation, element interaction, and multi-page traversal.

### Usage

```bash
curl -X POST https://api.firecrawl.dev/v2/extract \
    -H 'Authorization: Bearer YOUR_API_KEY' \
    -d '{
      "urls": ["https://example-forum.com/topic/123"],
      "prompt": "Extract all user comments",
      "agent": {
        "model": "FIRE-1"
      }
    }'
```

**Source:** `Extract.md`

---

## Known Limitations

- Large-scale site coverage (e.g., "all Amazon products") not supported in single request
- Complex logical queries may not reliably return all expected data
- Results may vary across runs for large/dynamic sites
- Beta status: features continue to evolve

**Source:** `Extract.md`

---

## File Reference

For detailed information:
- `Extract.md` - Complete `/extract` endpoint documentation with code examples in Python, Node.js, and cURL
