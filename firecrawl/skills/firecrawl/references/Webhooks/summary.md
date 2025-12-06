# Webhooks Summary

> Real-time HTTP notifications for Firecrawl crawl, batch scrape, and extract operations

## Contents

| File | Description |
|------|-------------|
| `Overview.md` | Webhook configuration, supported operations, and basic usage examples |
| `Event Types.md` | Complete reference of webhook event types and payload structures |
| `Security.md` | HMAC-SHA256 signature verification and security best practices |
| `Testing & Debugging.md` | Local development setup and common troubleshooting tips |

---

## Key Concepts

Webhooks provide real-time push notifications for Firecrawl operations, eliminating the need for status polling. When events occur during crawl, batch scrape, or extract operations, Firecrawl sends HTTP POST requests to your specified endpoint with event data and optional custom metadata.

Every webhook request is signed using HMAC-SHA256 with your account's secret key. This signature (sent in the `X-Firecrawl-Signature` header) proves the request originated from Firecrawl and the payload has not been tampered with. Always verify signatures using timing-safe comparison functions before processing webhook data.

Webhook configuration is flexible: you can specify custom headers, include metadata that gets echoed back in all payloads, and filter which event types you receive. Events follow a consistent structure with `success`, `type`, `id`, `data`, and `metadata` fields.

---

## Webhook Configuration

### Overview
Configure webhooks by adding a `webhook` object to your API request. Supported operations include crawl, batch scrape, and extract.

### Configuration Options

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | Your webhook endpoint URL (must be HTTPS) |
| `headers` | object | No | Custom headers to include in requests |
| `metadata` | object | No | Custom data included in all payloads |
| `events` | array | No | Event types to receive (default: all) |

### Quick Setup Example

```json
{
  "webhook": {
    "url": "https://your-domain.com/webhook",
    "metadata": { "any_key": "any_value" },
    "events": ["started", "page", "completed", "failed"]
  }
}
```

**Source:** `Overview.md`

---

## Event Types

### Overview
All webhook events share a common structure with operation-specific event types for crawl, batch scrape, and extract operations.

### Common Event Structure

```json
{
  "success": true,
  "type": "crawl.page",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [...],
  "metadata": {}
}
```

### Event Types by Operation

| Operation | Events |
|-----------|--------|
| Crawl | `crawl.started`, `crawl.page`, `crawl.completed` |
| Batch Scrape | `batch_scrape.started`, `batch_scrape.page`, `batch_scrape.completed` |
| Extract | `extract.started`, `extract.completed`, `extract.failed` |

### Common Fields

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether the operation was successful |
| `type` | string | Event type identifier |
| `id` | string | Unique job identifier |
| `data` | array | Event-specific data |
| `metadata` | object | Custom metadata from configuration |
| `error` | string | Error message (when `success` is `false`) |

**Source:** `Event Types.md`

---

## Security & Signature Verification

### Overview
Firecrawl signs every webhook using HMAC-SHA256. Verify signatures to ensure requests are authentic and unmodified.

### Signature Header Format

```
X-Firecrawl-Signature: sha256=abc123def456...
```

### Verification Steps

1. Extract signature from `X-Firecrawl-Signature` header
2. Get the raw request body (do not parse first)
3. Compute HMAC-SHA256 using your secret key
4. Compare signatures using timing-safe comparison
5. Process webhook only if signatures match

### Node.js Verification Example

```javascript
import crypto from 'crypto';

// Use raw body parser
app.use('/webhook', express.raw({ type: 'application/json' }));

app.post('/webhook', (req, res) => {
  const signature = req.get('X-Firecrawl-Signature');
  const [algorithm, hash] = signature.split('=');

  const expectedSignature = crypto
    .createHmac('sha256', process.env.FIRECRAWL_WEBHOOK_SECRET)
    .update(req.body)
    .digest('hex');

  if (!crypto.timingSafeEqual(Buffer.from(hash, 'hex'), Buffer.from(expectedSignature, 'hex'))) {
    return res.status(401).send('Invalid signature');
  }

  const event = JSON.parse(req.body);
  res.status(200).send('ok');
});
```

### Security Best Practices

- Always validate signatures before processing
- Use timing-safe comparison functions (`crypto.timingSafeEqual`, `hmac.compare_digest`)
- Require HTTPS for all webhook endpoints
- Keep your webhook secret secure; regenerate if compromised

**Source:** `Security.md`

---

## Testing & Debugging

### Overview
Use tunneling tools for local development and follow systematic debugging approaches for common webhook issues.

### Local Development with Cloudflare Tunnels

```bash
cloudflared tunnel --url localhost:3000
# Output: https://abc123.trycloudflare.com
```

Use the tunnel URL in your webhook configuration for local testing.

### Common Issues

| Issue | Solutions |
|-------|-----------|
| Webhooks not arriving | Check URL accessibility, verify HTTPS, check firewall, review event filters |
| Signature verification failing | Verify correct secret key, use raw body (not parsed JSON) |

### Raw Body Requirement

```javascript
// Wrong - using parsed body
const sig = crypto.createHmac('sha256', secret)
  .update(JSON.stringify(req.body)).digest('hex');

// Correct - using raw body
app.use('/webhook', express.raw({ type: 'application/json' }));
const sig = crypto.createHmac('sha256', secret)
  .update(req.body).digest('hex');
```

**Source:** `Testing & Debugging.md`

---

## File Reference

For detailed information:
- `Overview.md` - Complete setup guide with cURL examples for crawl and batch scrape
- `Event Types.md` - Full payload examples for all event types including page data structure
- `Security.md` - Python/Flask verification example and security rationale
- `Testing & Debugging.md` - Cloudflare Tunnels setup and debugging checklist
