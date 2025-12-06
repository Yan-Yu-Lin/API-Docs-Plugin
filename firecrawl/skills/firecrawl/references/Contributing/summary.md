# Contributing Summary

> Guides for running Firecrawl locally, self-hosting, and understanding open-source vs cloud differences

## Contents

| File | Description |
|------|-------------|
| `OpenSource vs Cloud.md` | Feature comparison between open-source and cloud offerings |
| `Running locally.md` | Instructions for local development setup |
| `Self-hosting.md` | Production self-hosting guide with Docker |

---

## Key Concepts

Firecrawl offers two deployment options: the cloud-hosted service at firecrawl.dev with full features, and the open-source version under AGPL-3.0 license. The cloud version includes advanced capabilities not available in self-hosted deployments, such as Fire-engine for handling IP blocks and robot detection.

For local development, Firecrawl requires Node.js, pnpm, Redis, and PostgreSQL. The setup involves running multiple terminal sessions for Redis, the API service, and testing endpoints. Docker Compose simplifies this by orchestrating all services automatically.

Self-hosting is ideal for organizations with strict security requirements needing data to remain within controlled environments. However, self-hosted instances lack access to Fire-engine and require manual configuration for advanced scraping methods beyond basic fetch and Playwright options.

---

## Open Source vs Cloud Features

### Overview
Firecrawl Cloud provides additional features not available in the open-source version, making it suitable for production workloads requiring advanced scraping capabilities.

### Feature Comparison

| Feature | Open Source | Cloud |
|---------|-------------|-------|
| Basic scraping | Yes | Yes |
| Playwright support | Yes | Yes |
| Fire-engine (IP blocks, bot detection) | No | Yes |
| Advanced features | Limited | Full |

**Source:** `OpenSource vs Cloud.md`

---

## Local Development Setup

### Overview
Running Firecrawl locally requires installing dependencies, setting up PostgreSQL via Docker, and running multiple services in separate terminals.

### Prerequisites

- Node.js
- pnpm (version 9+)
- Redis
- PostgreSQL (via Docker)

### PostgreSQL Setup

```bash
# Build the Docker image
docker build -t nuq-postgres .

# Run the container
docker run --name nuqdb \
  -e POSTGRES_PASSWORD=postgres \
  -p 5433:5432 \
  -v nuq-data:/var/lib/postgresql/data \
  -d nuq-postgres
```

### Required Environment Variables

```bash
# .env in /apps/api/
NUM_WORKERS_PER_QUEUE=8
PORT=3002
HOST=0.0.0.0
REDIS_URL=redis://localhost:6379
REDIS_RATE_LIMIT_URL=redis://localhost:6379
USE_DB_AUTHENTICATION=false
NUQ_DATABASE_URL=postgres://postgres:postgres@localhost:5433/postgres
```

### Running Services

| Terminal | Command | Purpose |
|----------|---------|---------|
| 1 | `redis-server` | Start Redis |
| 2 | `pnpm start` (in apps/api/) | Start API service |
| 3 | `curl -X GET http://localhost:3002/test` | Test endpoint |

### Docker Compose Alternative

```bash
docker compose up
```

### Running Tests

```bash
npm run test:snips
```

**Source:** `Running locally.md`

---

## Self-Hosting with Docker

### Overview
Self-hosting provides full control over data processing environments, ideal for organizations with security and compliance requirements.

### Why Self-Host

- **Security and Compliance:** Data stays within controlled infrastructure
- **Customization:** Tailor services like Playwright to specific needs
- **Learning:** Deeper understanding for meaningful contributions

### Limitations

| Limitation | Impact |
|------------|--------|
| No Fire-engine access | Cannot handle advanced IP blocks or robot detection |
| Manual configuration | Advanced scraping methods require `.env` setup |
| No Supabase in self-host | Authentication features unavailable |

### Setup Steps

1. Install Docker
2. Create `.env` file in root directory (copy from `apps/api/.env.example`)
3. Build and run containers:

```bash
docker compose build
docker compose up
```

### Access Points

| Service | URL |
|---------|-----|
| API | `http://localhost:3002` |
| Bull Queue Admin | `http://localhost:3002/admin/@/queues` |

### Optional: TypeScript Playwright Service

Update `docker-compose.yml`:

```yaml
# Change from:
build: apps/playwright-service
# To:
build: apps/playwright-service-ts
```

Set in `.env`:

```bash
PLAYWRIGHT_MICROSERVICE_URL=http://localhost:3000/scrape
```

### Test the API

```bash
curl -X POST http://localhost:3002/v2/crawl \
    -H 'Content-Type: application/json' \
    -d '{
      "url": "https://docs.firecrawl.dev"
    }'
```

**Source:** `Self-hosting.md`

---

## Troubleshooting Self-Hosted Instances

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Supabase not configured | Error about Supabase client | Expected behavior; scraping still works |
| Authentication bypass | Warning about bypassing auth | Expected behavior without Supabase |
| Docker containers fail | Containers exit unexpectedly | Check `docker logs [container_name]` |
| Redis connection issues | Timeout or "Connection refused" | Verify Redis is running and `REDIS_URL` is correct |
| API not responding | Requests timeout | Check container status and PORT/HOST settings |

### Kubernetes Deployment

For Kubernetes cluster installation, refer to the [examples/kubernetes-cluster-install](https://github.com/firecrawl/firecrawl/tree/main/examples/kubernetes/cluster-install#readme) documentation.

**Source:** `Self-hosting.md`

---

## File Reference

For detailed information:

- `OpenSource vs Cloud.md` - Feature comparison and licensing information
- `Running locally.md` - Step-by-step local development setup with terminal commands
- `Self-hosting.md` - Production Docker deployment, environment configuration, and troubleshooting
