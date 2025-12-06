# JSON mode - Structured result

> Extract structured data from pages via LLMs

<Note>
  **v2 API Change:** JSON schema extraction is fully supported in v2, but the API format has changed. In v2, the schema is embedded directly inside the format object as `formats: [{type: "json", schema: {...}}]`. The v1 `jsonOptions` parameter no longer exists in v2.
</Note>

## Scrape and extract structured data with Firecrawl

Firecrawl uses AI to get structured data from web pages in 3 steps:

1. **Set the Schema (optional):**
   Define a JSON schema (using OpenAI's format) to specify the data you want, or just provide a `prompt` if you don't need a strict schema, along with the webpage URL.

2. **Make the Request:**
   Send your URL and schema to our scrape endpoint using JSON mode. See how here:
   [Scrape Endpoint Documentation](https://docs.firecrawl.dev/api-reference/endpoint/scrape)

3. **Get Your Data:**
   Get back clean, structured data matching your schema that you can use right away.

This makes getting web data in the format you need quick and easy.

## Extract structured data

### JSON mode via /scrape

Used to extract structured data from scraped pages.

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl
  from pydantic import BaseModel

  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  class CompanyInfo(BaseModel):
      company_mission: str
      supports_sso: bool
      is_open_source: bool
      is_in_yc: bool

  result = app.scrape(
      'https://firecrawl.dev',
      formats=[{
        "type": "json",
        "schema": CompanyInfo.model_json_schema()
      }],
      only_main_content=False,
      timeout=120000
  )

  print(result)
  ```

  ```js Node theme={null}
  import FirecrawlApp from "@mendable/firecrawl-js";
  import { z } from "zod";

  const app = new FirecrawlApp({
    apiKey: "fc-YOUR_API_KEY"
  });

  // Define schema to extract contents into
  const schema = z.object({
    company_mission: z.string(),
    supports_sso: z.boolean(),
    is_open_source: z.boolean(),
    is_in_yc: z.boolean()
  });

  const result = await app.scrape("https://firecrawl.dev", {
    formats: [{
      type: "json",
      schema: schema
    }],
  });

  console.log(result);
  ```

  ```bash cURL theme={null}
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev",
        "formats": [ {
          "type": "json",
          "schema": {
            "type": "object",
            "properties": {
              "company_mission": {
                        "type": "string"
              },
              "supports_sso": {
                        "type": "boolean"
              },
              "is_open_source": {
                        "type": "boolean"
              },
              "is_in_yc": {
                        "type": "boolean"
              }
            },
            "required": [
              "company_mission",
              "supports_sso",
              "is_open_source",
              "is_in_yc"
            ]
          }
        } ]
      }'
  ```
</CodeGroup>

Output:

```json JSON theme={null}
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
        "supports_sso": true,
        "is_open_source": true,
        "is_in_yc": true
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}
```

### Structured data without schema

You can also extract without a schema by just passing a `prompt` to the endpoint. The llm chooses the structure of the data.

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl

  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  result = app.scrape(
      'https://firecrawl.dev',
      formats=[{
        "type": "json",
        "prompt": "Extract the company mission from the page."
      }],
      only_main_content=False,
      timeout=120000
  )

  print(result)
  ```

  ```js Node theme={null}
  import FirecrawlApp from "@mendable/firecrawl-js";

  const app = new FirecrawlApp({
    apiKey: "fc-YOUR_API_KEY"
  });

  const result = await app.scrape("https://firecrawl.dev", {
    formats: [{
      type: "json",
      prompt: "Extract the company mission from the page."
    }]
  });

  console.log(result);
  ```

  ```bash cURL theme={null}
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev",
        "formats": [{
          "type": "json",
          "prompt": "Extract the company mission from the page."
        }]
      }'
  ```
</CodeGroup>

Output:

```json JSON theme={null}
{
    "success": true,
    "data": {
      "json": {
        "company_mission": "AI-powered web scraping and data extraction",
      },
      "metadata": {
        "title": "Firecrawl",
        "description": "AI-powered web scraping and data extraction",
        "robots": "follow, index",
        "ogTitle": "Firecrawl",
        "ogDescription": "AI-powered web scraping and data extraction",
        "ogUrl": "https://firecrawl.dev/",
        "ogImage": "https://firecrawl.dev/og.png",
        "ogLocaleAlternate": [],
        "ogSiteName": "Firecrawl",
        "sourceURL": "https://firecrawl.dev/"
      },
    }
}
```

### Real-world example: Extracting company information

Here's a comprehensive example extracting structured company information from a website:

<CodeGroup>
  ```python Python theme={null}
  from firecrawl import Firecrawl
  from pydantic import BaseModel

  app = Firecrawl(api_key="fc-YOUR-API-KEY")

  class CompanyInfo(BaseModel):
      company_mission: str
      supports_sso: bool
      is_open_source: bool
      is_in_yc: bool

  result = app.scrape(
      'https://firecrawl.dev/',
      formats=[{
          "type": "json",
          "schema": CompanyInfo.model_json_schema()
      }]
  )

  print(result)
  ```

  ```js Node theme={null}
  import FirecrawlApp from "@mendable/firecrawl-js";
  import { z } from "zod";

  const app = new FirecrawlApp({
    apiKey: "fc-YOUR_API_KEY"
  });

  const companyInfoSchema = z.object({
    company_mission: z.string(),
    supports_sso: z.boolean(),
    is_open_source: z.boolean(),
    is_in_yc: z.boolean()
  });

  const result = await app.scrape("https://firecrawl.dev/", {
    formats: [{
      type: "json",
      schema: companyInfoSchema
    }]
  });

  console.log(result);
  ```

  ```bash cURL theme={null}
  curl -X POST https://api.firecrawl.dev/v2/scrape \
      -H 'Content-Type: application/json' \
      -H 'Authorization: Bearer YOUR_API_KEY' \
      -d '{
        "url": "https://firecrawl.dev/",
        "formats": [{
          "type": "json",
          "schema": {
            "type": "object",
            "properties": {
              "company_mission": {
                "type": "string"
              },
              "supports_sso": {
                "type": "boolean"
              },
              "is_open_source": {
                "type": "boolean"
              },
              "is_in_yc": {
                "type": "boolean"
              }
            },
            "required": [
              "company_mission",
              "supports_sso",
              "is_open_source",
              "is_in_yc"
            ]
          }
        }]
      }'
  ```
</CodeGroup>

Output:

```json Output theme={null}
{
  "success": true,
  "data": {
    "json": {
      "company_mission": "Turn websites into LLM-ready data",
      "supports_sso": true,
      "is_open_source": true,
      "is_in_yc": true
    }
  }
}
```

### JSON format options

When using JSON mode in v2, include an object in `formats` with the schema embedded directly:

`formats: [{ type: 'json', schema: { ... }, prompt: '...' }]`

Parameters:

* `schema`: JSON Schema describing the structured output you want (required for schema-based extraction).
* `prompt`: Optional prompt to guide extraction (also used for no-schema extraction).

**Important:** Unlike v1, there is no separate `jsonOptions` parameter in v2. The schema must be included directly inside the format object in the `formats` array.


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://docs.firecrawl.dev/llms.txt
