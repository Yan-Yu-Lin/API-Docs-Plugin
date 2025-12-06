# Standard Features Summary

> Core Firecrawl capabilities for web scraping, crawling, mapping, and searching

## Contents

| File/Folder | Description |
|-------------|-------------|
| `Crawl.md` | Recursive website crawling with WebSocket/webhook support |
| `Map.md` | Fast URL discovery across websites |
| `Search.md` | Web search with optional content scraping |
| `Scrape/` | Single-page scraping and related features (8 files) |

---

## Key Concepts

Firecrawl provides four main endpoints for web data extraction: **Scrape** for single pages, **Batch Scrape** for multiple URLs, **Crawl** for recursive website traversal, **Map** for URL discovery, and **Search** for web-wide queries with optional content retrieval.

All endpoints support common options like output formats (markdown, HTML, JSON, screenshots), caching via `maxAge`, proxy selection, and location-based content. The `/scrape` endpoint options are available in crawl/batch operations via `scrapeOptions`.

Key performance features include caching (up to 500% faster with `maxAge`), stealth proxies for anti-bot bypass, and structured JSON extraction via LLM. Change tracking enables monitoring content differences over time.

---

## Scrape

### Overview
The `/scrape` endpoint extracts content from a single URL, returning clean markdown by default. Supports PDFs, browser actions, and multiple output formats.

### Key Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `formats` | array | Output types: `markdown`, `html`, `rawHtml`, `links`, `summary`, `images`, or objects for `json`/`screenshot`/`changeTracking` |
| `onlyMainContent` | boolean | Return main content only (default: `true`) |
| `includeTags` / `excludeTags` | array | Filter HTML elements |
| `waitFor` | integer | Extra wait time in ms |
| `maxAge` | integer | Cache freshness in ms (default: 2 days) |
| `timeout` | integer | Request timeout in ms (default: 30000) |
| `actions` | array | Browser actions: `wait`, `click`, `write`, `press`, `scroll`, `scrape`, `executeJavascript` |
| `parsers` | array | Document parsers, e.g., `["pdf"]` |
| `proxy` | string | `basic`, `stealth`, or `auto` |

### Basic Usage

```python
from firecrawl import Firecrawl
firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
doc = firecrawl.scrape("https://firecrawl.dev")
print(doc.markdown)
```

```javascript
import Firecrawl from '@mendable/firecrawl-js';
const firecrawl = new Firecrawl({ apiKey: "fc-YOUR-API-KEY" });
const doc = await firecrawl.scrape('https://firecrawl.dev');
console.log(doc.markdown);
```

**Source:** `Scrape/Scrape.md`

---

## Batch Scrape

### Overview
Scrape multiple URLs in a single batch job. Similar to crawl but for a predefined list of URLs.

### SDK Methods

| Method | Description |
|--------|-------------|
| `batchScrape` / `batch_scrape` | Start and wait for completion |
| `startBatchScrape` / `start_batch_scrape` | Start and return job ID |
| `getBatchScrapeStatus` / `get_batch_scrape_status` | Check job status |

### Usage

```python
job = firecrawl.batch_scrape([
    "https://firecrawl.dev",
    "https://docs.firecrawl.dev",
], formats=["markdown"], poll_interval=2)
```

### Webhook Events
- `batch_scrape.started` - Batch begins
- `batch_scrape.page` - Each URL scraped
- `batch_scrape.completed` - All URLs processed
- `batch_scrape.failed` - Error occurred

**Source:** `Scrape/Batch Scrape.md`

---

## Crawl

### Overview
Recursively crawl a website starting from a URL, following links to discover and scrape subpages. Returns a job ID for status polling.

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max pages to crawl (default: 10000) |
| `maxDiscoveryDepth` | integer | Max depth for URL discovery |
| `includePaths` / `excludePaths` | array | Regex patterns for URL filtering |
| `crawlEntireDomain` | boolean | Explore siblings/parents |
| `allowSubdomains` | boolean | Follow subdomains |
| `allowExternalLinks` | boolean | Follow external domains |
| `scrapeOptions` | object | Scrape options for each page |

### SDK Methods

| Method | Description |
|--------|-------------|
| `crawl` | Start and wait for completion |
| `start_crawl` / `startCrawl` | Start and return job ID |
| `get_crawl_status` / `getCrawlStatus` | Check job status |

### Webhook Events
- `crawl.started`, `crawl.page`, `crawl.completed`, `crawl.failed`

### WebSocket Watcher

```javascript
const watcher = firecrawl.watcher(id, { kind: 'crawl', pollInterval: 2 });
watcher.on('document', (doc) => console.log('DOC', doc));
watcher.on('done', (state) => console.log('DONE', state.status));
await watcher.start();
```

**Source:** `Crawl.md`

---

## Map

### Overview
Quickly discover all URLs on a website. Extremely fast for URL enumeration without scraping content.

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Max links to return (default: 100) |
| `search` | string | Filter URLs containing text |
| `sitemap` | string | `include`, `skip`, or `only` |
| `includeSubdomains` | boolean | Include subdomains (default: true) |

### Usage

```python
res = firecrawl.map(url="https://firecrawl.dev", limit=50, sitemap="include")
print(res)  # Returns list of URLs with titles/descriptions
```

**Source:** `Map.md`

---

## Search

### Overview
Perform web searches and optionally scrape content from results in one operation. Supports web, news, and image sources.

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | string | Search query (supports operators) |
| `limit` | integer | Number of results |
| `sources` | array | `web`, `news`, `images` |
| `categories` | array | `github`, `research`, `pdf` |
| `location` | string | Geographic location |
| `tbs` | string | Time filter: `qdr:h`, `qdr:d`, `qdr:w`, `qdr:m`, `qdr:y` |
| `scrapeOptions` | object | Scrape options for results |

### Search Operators
- `"exact phrase"` - Non-fuzzy match
- `-keyword` - Exclude term
- `site:domain.com` - Site-specific
- `intitle:word` - Title contains
- `imagesize:1920x1080` - Exact image size

### Cost
- 2 credits per 10 search results
- Additional scraping costs if `scrapeOptions` enabled

**Source:** `Search.md`

---

## JSON Mode (Structured Extraction)

### Overview
Extract structured data from pages using LLM with optional JSON schema.

### Usage

```python
result = app.scrape(
    'https://firecrawl.dev',
    formats=[{
        "type": "json",
        "schema": {"type": "object", "properties": {"title": {"type": "string"}}},
        "prompt": "Extract the page title"  # Optional
    }]
)
print(result.json)
```

**Cost:** 4 additional credits per page

**Source:** `Scrape/JSON mode - Structured result.md`

---

## Change Tracking

### Overview
Monitor and detect content changes between scrapes. Requires `markdown` format alongside `changeTracking`.

### Change Status Values
- `new` - First scrape of this URL
- `same` - No changes detected
- `changed` - Content modified
- `removed` - Page no longer exists

### Modes
- `git-diff` - Line-by-line diff output
- `json` - Structured field comparison (requires schema, costs 5 credits)

### Usage

```javascript
const result = await firecrawl.scrape('https://example.com', {
  formats: ['markdown', { type: 'changeTracking', modes: ['git-diff'] }]
});
console.log(result.changeTracking.changeStatus);
```

**Source:** `Scrape/Change Tracking.md`

---

## Faster Scraping (Caching)

### Overview
Use `maxAge` to return cached content instantly when available, up to 500% faster.

### Common Values

| Duration | Value (ms) |
|----------|------------|
| 5 minutes | 300000 |
| 1 hour | 3600000 |
| 1 day | 86400000 |
| 1 week | 604800000 |

- Default: 172800000 (2 days)
- Force fresh: `maxAge: 0`
- Skip caching: `storeInCache: false`

**Source:** `Scrape/Faster Scraping.md`

---

## Proxies and Stealth Mode

### Proxy Types

| Type | Description | Cost |
|------|-------------|------|
| `basic` | Fast, for sites with minimal protection | Standard |
| `stealth` | Advanced anti-bot bypass, slower | 5 credits |
| `auto` | Try basic, retry with stealth on failure | Variable |

### Supported Stealth Locations
US, AU, BR (others use basic proxy with browser location emulation)

### Location Configuration

```python
doc = firecrawl.scrape('https://example.com',
    location={'country': 'US', 'languages': ['en']}
)
```

**Source:** `Scrape/Proxies.md`, `Scrape/Stealth Mode.md`

---

## Document Parsing

### Supported Formats
- **Excel** (`.xlsx`, `.xls`) - Each sheet becomes an HTML table
- **Word** (`.docx`, `.doc`, `.odt`, `.rtf`) - Preserves structure
- **PDF** (`.pdf`) - Text extraction with OCR support (1 credit/page)

Parsing is automatic based on URL extension or content-type.

**Source:** `Scrape/Document Parsing.md`

---

## File Reference

For detailed information:
- `Scrape/Scrape.md` - Full scrape options, actions, and examples
- `Scrape/Batch Scrape.md` - Multi-URL scraping with webhooks
- `Scrape/JSON mode - Structured result.md` - LLM-based data extraction
- `Scrape/Change Tracking.md` - Content monitoring and diff modes
- `Scrape/Faster Scraping.md` - Caching with maxAge parameter
- `Scrape/Proxies.md` - Location-based proxy selection
- `Scrape/Stealth Mode.md` - Anti-bot bypass strategies
- `Scrape/Document Parsing.md` - Excel, Word, PDF support
- `Crawl.md` - Recursive crawling with WebSocket/webhooks
- `Map.md` - Fast URL discovery
- `Search.md` - Web search with scraping integration
