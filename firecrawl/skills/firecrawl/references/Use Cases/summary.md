# Use Cases Summary

> Transform web data into powerful features for AI applications, sales pipelines, research tools, and business intelligence systems.

## Contents

| File/Folder | Description |
|-------------|-------------|
| `Overview.md` | Navigation hub listing all Firecrawl use cases |
| `AI Platforms.md` | Power RAG chatbots and AI assistants with web knowledge |
| `Deep Research.md` | Build agentic research tools with multi-source synthesis |
| `Lead Enrichment.md` | Extract leads and enrich CRM data from websites |
| `SEO Platforms.md` | Optimize content for AI assistants and search engines |
| `View More/` | Additional use cases (7 files) |

---

## Key Concepts

Firecrawl enables teams to extract and transform web data for various business applications. The platform provides clean markdown, structured JSON, HTML, images, and screenshots from websites, making web data accessible for AI systems, sales teams, researchers, and developers.

Core capabilities include real-time data extraction, JavaScript rendering, authentication support, batch processing, and enterprise-scale crawling. These features power use cases ranging from AI knowledge bases to competitive intelligence systems.

Each use case includes starter templates on GitHub, implementation patterns, and integration guidance for common workflows. The platform integrates with LangChain, n8n, Zapier, and custom frameworks through APIs and SDKs.

---

## AI & Research Applications

### AI Platforms
Power AI assistants with real-time web knowledge, reducing hallucinations with current data.

| Feature | Description |
|---------|-------------|
| RAG Integration | Feed chatbots with up-to-date documentation and domain knowledge |
| Customer Enablement | Let users build AI apps with web data |
| Format Support | Markdown, JSON, HTML, images, screenshots |
| Scale | Enterprise-scale data extraction for AI training |

**Template:** [Firestarter](https://github.com/mendableai/firestarter) - Instant AI chatbots for websites

**Source:** `AI Platforms.md`

### Deep Research
Build automated research systems that synthesize information from hundreds of sources.

| Capability | Description |
|------------|-------------|
| Iterative Exploration | Discover related topics and sources automatically |
| Multi-Source Synthesis | Combine information from hundreds of websites |
| Citation Preservation | Maintain full source attribution |
| Trend Detection | Identify patterns across multiple sources |

**Templates:**
- [Fireplexity](https://github.com/mendableai/fireplexity) - AI search with real-time citations
- [Firesearch](https://github.com/mendableai/firesearch) - Deep research agent with LangGraph
- [Open Researcher](https://github.com/mendableai/open-researcher) - Visual AI research assistant

**Source:** `Deep Research.md`

---

## Sales & Marketing

### Lead Enrichment
Extract company information and enrich CRM data from websites.

| Data Source | What to Extract |
|-------------|-----------------|
| Business Directories | Industry listings, chamber of commerce, trade associations |
| Company Websites | About pages, team sections, press releases, job postings |

- Integrates with Salesforce, HubSpot, Pipedrive via API or Zapier
- Real-time data directly from company websites
- Contact information from public pages

**Template:** [Fire Enrich](https://github.com/mendableai/fire-enrich)

**Source:** `Lead Enrichment.md`

### Content Generation
Generate AI content based on website data, images, and news.

| Content Type | Use Case |
|--------------|----------|
| Sales Decks | Custom presentations with prospect data |
| Email Campaigns | Personalized outreach at scale |
| Marketing Content | Data-driven blog posts and reports |
| Documentation | Auto-updated technical content |

**Template:** [Open Lovable](https://github.com/mendableai/open-lovable) - Transform websites into React apps

**Source:** `View More/Content Generation.md`

---

## SEO & Competitive Intelligence

### SEO Platforms
Optimize websites for AI assistants and traditional search engines.

| Capability | Description |
|------------|-------------|
| AI Readability Audit | Optimize content for AI comprehension |
| Technical SEO | Site performance, crawlability, broken links |
| Content Analysis | Structure and semantic optimization |
| llms.txt Support | Emerging convention for AI crawler guidance |

**Template:** [FireGEO](https://github.com/mendableai/firegeo) - Multi-region rank tracking

**Source:** `SEO Platforms.md`

### Competitive Intelligence
Monitor competitors and track changes in real-time.

| Track | Examples |
|-------|----------|
| Products | Launches, features, specs, pricing, documentation |
| Marketing | Messaging, campaigns, case studies, testimonials |
| Business | Job postings, partnerships, funding, press releases |
| Technical | API changes, integrations, technology stack |

**Templates:**
- [Firecrawl Observer](https://github.com/mendableai/firecrawl-observer) - Real-time monitoring
- [Fireplexity](https://github.com/mendableai/fireplexity) - Research and analysis

**Source:** `View More/Competitive Intelligence.md`

---

## E-commerce & Product

### Product & E-commerce
Monitor pricing, track inventory, and migrate product catalogs.

| Data Type | Fields |
|-----------|--------|
| Product Data | Title, SKU, specs, descriptions, categories |
| Pricing | Current price, discounts, shipping, tax |
| Inventory | Stock levels, availability, lead times |
| Reviews | Ratings, customer feedback, Q&A sections |

- Supports Shopify, WooCommerce, Magento, BigCommerce
- Handles pagination and infinite scroll
- JavaScript rendering for dynamic pricing

**Template:** [Firecrawl Migrator](https://github.com/mendableai/firecrawl-migrator)

**Source:** `View More/Product & E-commerce.md`

---

## Finance & Investment

### Investment & Finance
Monitor portfolio companies and extract financial insights.

| Signal Type | Examples |
|-------------|----------|
| Company Metrics | Growth indicators, team changes, product launches, funding |
| Market Signals | Industry trends, competitor moves, sentiment, regulatory changes |
| Risk Indicators | Leadership changes, legal issues, customer complaints |
| Alternative Data | Job postings, web traffic, social signals, news mentions |

- Track private companies via public information
- ESG and sustainability monitoring
- Earnings call preparation support

**Template:** [Firecrawl Observer](https://github.com/mendableai/firecrawl-observer)

**Source:** `View More/Investment & Finance.md`

---

## Developer Tools

### Developers & MCP
Integrate Firecrawl into AI coding workflows via Model Context Protocol.

| Platform | Support |
|----------|---------|
| Claude Desktop | Native MCP support |
| Cursor | Native MCP support |
| VS Code | Community extensions |
| Custom | MCP SDK integration |

- Zero infrastructure required
- 15-minute automatic response caching
- Standard API rate limits apply

**Template:** [MCP Server Firecrawl](https://github.com/mendableai/firecrawl-mcp-server)

**Source:** `View More/Developers & MCP.md`

---

## Operations & Infrastructure

### Data Migration
Transfer web data between platforms and systems.

| Migration Type | Examples |
|----------------|----------|
| CMS Content | WordPress, Drupal, Joomla to Contentful, Strapi, Sanity |
| E-commerce | Magento, WooCommerce to Shopify, BigCommerce |
| Content | Pages, posts, articles, media files, metadata |
| Structure | Hierarchies, categories, tags, taxonomies |

- SEO metadata preservation with proper redirects
- Incremental processing with batching
- Media file extraction and cataloging

**Template:** [Firecrawl Migrator](https://github.com/mendableai/firecrawl-migrator)

**Source:** `View More/Data Migration.md`

### Observability & Monitoring
Monitor websites, track uptime, and detect changes.

| Monitor Type | What to Check |
|--------------|---------------|
| Availability | Uptime, response times, error rates |
| Content | Text changes, image updates, layout shifts |
| Performance | Page load times, Core Web Vitals |
| Security | SSL certificates, security headers |

- Full JavaScript rendering for SPAs and React apps
- Synthetic monitoring for user journeys
- Visual regression testing support

**Template:** [Firecrawl Observer](https://github.com/mendableai/firecrawl-observer)

**Source:** `View More/Observability & Monitoring.md`

---

## GitHub Templates Quick Reference

| Template | Use Case |
|----------|----------|
| [Firestarter](https://github.com/mendableai/firestarter) | AI chatbots with web knowledge |
| [Fireplexity](https://github.com/mendableai/fireplexity) | AI search with citations |
| [Firesearch](https://github.com/mendableai/firesearch) | Deep research with LangGraph |
| [Open Researcher](https://github.com/mendableai/open-researcher) | Visual research assistant |
| [Fire Enrich](https://github.com/mendableai/fire-enrich) | Lead enrichment |
| [FireGEO](https://github.com/mendableai/firegeo) | SEO and rank tracking |
| [Open Lovable](https://github.com/mendableai/open-lovable) | Website to React app |
| [Firecrawl Observer](https://github.com/mendableai/firecrawl-observer) | Website monitoring |
| [Firecrawl Migrator](https://github.com/mendableai/firecrawl-migrator) | Data migration |
| [MCP Server Firecrawl](https://github.com/mendableai/firecrawl-mcp-server) | MCP integration |

---

## File Reference

For detailed information:
- `Overview.md` - Complete navigation of all use cases
- `AI Platforms.md` - RAG, chatbots, AI training data workflows
- `Deep Research.md` - Multi-source research tools and templates
- `Lead Enrichment.md` - Sales pipeline and CRM enrichment
- `SEO Platforms.md` - AI readability and search optimization
- `View More/Competitive Intelligence.md` - Competitor tracking and alerts
- `View More/Content Generation.md` - AI content creation workflows
- `View More/Data Migration.md` - Platform migration patterns
- `View More/Developers & MCP.md` - MCP setup and IDE integration
- `View More/Investment & Finance.md` - Portfolio monitoring and due diligence
- `View More/Observability & Monitoring.md` - Uptime and change detection
- `View More/Product & E-commerce.md` - Pricing and catalog extraction
