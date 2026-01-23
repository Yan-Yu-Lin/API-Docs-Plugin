# Claude Agent SDK Licensing and Usage Policy Research

**Research Date:** January 23, 2026
**Purpose:** Determine licensing terms, restrictions on non-Claude models, and policy around alternative endpoints

---

## Executive Summary

The Claude Agent SDK has a **mixed licensing structure**:
- **TypeScript SDK**: Proprietary (Commercial Terms of Service only)
- **Python SDK**: MIT License

However, **usage of the SDK is governed by Anthropic's Commercial Terms of Service** regardless of which SDK you use. The key restriction relevant to using non-Claude models is:

> **Section D.4 (Use Restrictions):** "Customer may not and must not attempt to (a) access the Services to build a competing product or service, including to train competing AI models or resell the Services except as expressly approved by Anthropic; (b) reverse engineer or duplicate the Services; or (c) support any third party's attempt at any of the conduct restricted in this sentence."

**Critical Finding:** While technically possible to point `ANTHROPIC_BASE_URL` to alternative providers like OpenRouter (and access non-Claude models), doing so to "build a competing product or service" may violate the Terms of Service. The exact interpretation depends on your use case.

---

## 1. License Types by SDK

### TypeScript SDK (@anthropic-ai/claude-agent-sdk)

**License:** Proprietary - Commercial Terms of Service

**Source:** /tmp/claude-agent-sdk-typescript/LICENSE.md
\`\`\`
© Anthropic PBC. All rights reserved. Use is subject to Anthropic's Commercial Terms of Service.
\`\`\`

**GitHub:** https://github.com/anthropics/claude-agent-sdk-typescript

### Python SDK (claude-agent-sdk)

**License:** MIT License

**Source:** /tmp/claude-agent-sdk-python/LICENSE
\`\`\`
MIT License

Copyright (c) 2025 Anthropic, PBC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
\`\`\`

**GitHub:** https://github.com/anthropics/claude-agent-sdk-python

### Important Clarification

Both SDK README files state:

> "Use of this SDK is governed by Anthropic's Commercial Terms of Service, including when you use it to power products and services that you make available to your own customers and end users, **except to the extent a specific component or dependency is covered by a different license as indicated in that component's LICENSE file**."

**Source:** TypeScript README.md (lines 45-47), Python README.md (lines 354-356)

This creates a dual-layer situation:
1. **Python SDK code** - MIT licensed (can be modified, redistributed, used commercially)
2. **Service usage** - Governed by Commercial Terms regardless of SDK license

---

## 2. Anthropic Commercial Terms of Service - Key Sections

**Full Terms:** https://www.anthropic.com/legal/commercial-terms

### Section A.1 - Overview

> "Subject to these Terms, Anthropic gives Customer permission to use the Services, including to power products and services Customer makes available to its own customers and end users ('Users')."

**Interpretation:** Commercial use is permitted for building products/services.

### Section D.4 - Use Restrictions (CRITICAL)

> "Customer may not and must not attempt to (a) **access the Services to build a competing product or service**, including to train competing AI models or **resell the Services except as expressly approved by Anthropic**; (b) **reverse engineer or duplicate the Services**; or (c) support any third party's attempt at any of the conduct restricted in this sentence."

**Key restrictions:**
1. Cannot build competing products/services
2. Cannot resell without approval
3. Cannot reverse engineer or duplicate the Services
4. Cannot help others do the above

### Section B - Customer Content

> "Customer (a) retains all rights to its Inputs, and (b) owns its Outputs. Anthropic disclaims any rights it receives to the Customer Content under these Terms. **Anthropic may not train models on Customer Content from Services.**"

**Interpretation:** Your data remains yours; Anthropic won't train on your API usage.

### Section D.2 - Policies and Service Terms

> "Customer and its Users may only use the Services in compliance with these Terms, including (a) the Usage Policy, (b) our Supported Regions Policy and (c) our Service Specific Terms."

---

## 3. Using ANTHROPIC_BASE_URL with Alternative Providers

### Documentation Evidence

**Source:** /Users/linyanyu/claude-agent-sdk/docs/secure-deployment.md (lines 228-234)

\`\`\`markdown
**Option 1: ANTHROPIC_BASE_URL (simple but only for sampling API requests)**

export ANTHROPIC_BASE_URL="http://localhost:8080"

This tells Claude Code and the Agent SDK to send sampling requests to your proxy
instead of the Anthropic API directly. Your proxy receives plaintext HTTP requests,
can inspect and modify them (including injecting credentials), then forwards to the real API.
\`\`\`

**Intended Use:** The ANTHROPIC_BASE_URL is documented for:
1. Proxy routing for security/credential injection
2. Forwarding to "the real API" (Anthropic)
3. Not for model replacement

### Technical Feasibility

**Yes, it technically works** with alternative providers that support the Anthropic Messages API format:

| Provider | Anthropic API Support | Works with SDK |
|----------|----------------------|----------------|
| OpenRouter | Yes (/api/v1/messages) | Yes |
| LiteLLM | Yes (translation layer) | Partial |
| Local LLMs | No (different API format) | No |

**OpenRouter Example:**
\`\`\`bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="\$OPENROUTER_API_KEY"
export ANTHROPIC_API_KEY=""
\`\`\`

### Legal Analysis

**Question:** Is using ANTHROPIC_BASE_URL to access non-Claude models permitted?

**Answer:** Unclear - depends on interpretation of "competing product or service."

**Arguments that it's permitted:**
1. The SDK code (Python) is MIT licensed - can be modified/used freely
2. You're not "reselling" Anthropic services
3. You're using your own infrastructure/third-party providers
4. No explicit prohibition on alternative endpoints in the Terms

**Arguments it may be prohibited:**
1. Using Anthropic's SDK architecture to build products with competing models could be "building a competing product"
2. The SDK relies on Claude Code CLI which has its own terms
3. The proxy pattern is documented for forwarding to "the real API"
4. "Duplicate the Services" could include using the SDK framework with other models

---

## 4. Key Questions Answered

### Q1: What license is the Agent SDK released under?

**Answer:** Mixed:
- **TypeScript SDK:** Proprietary (Commercial Terms of Service)
- **Python SDK:** MIT License (but usage governed by Commercial Terms)

### Q2: Are there restrictions on using the SDK with non-Anthropic models?

**Answer:** No explicit prohibition, but Section D.4 prohibits "building a competing product or service." Whether using the SDK with non-Claude models constitutes this is ambiguous.

### Q3: Does the license prohibit pointing the SDK at alternative endpoints?

**Answer:** Not explicitly. However:
- Documentation states ANTHROPIC_BASE_URL is for proxy routing to "the real API"
- Using it for model replacement is outside the documented use case
- Could be interpreted as "duplicating the Services" with competing models

### Q4: Any mention of local LLM usage in the terms?

**Answer:** No direct mention. However:
- Local LLMs don't support the Anthropic Messages API format natively
- Would require a translation proxy (like LiteLLM)
- Technical incompatibility aside, same legal ambiguity as other non-Claude models applies

### Q5: Is commercial use allowed?

**Answer:** Yes, explicitly.

**Section A.1:** "...including to power products and services Customer makes available to its own customers and end users."

**Restrictions:**
- Cannot build competing AI products/services
- Cannot resell without approval
- Must comply with Usage Policy and regional restrictions

---

## 5. Officially Supported Third-Party Providers

**Source:** /Users/linyanyu/claude-agent-sdk/docs/overview.md (lines 424-431)

> "The SDK also supports authentication via third-party API providers:
> - **Amazon Bedrock**: set CLAUDE_CODE_USE_BEDROCK=1 environment variable
> - **Google Vertex AI**: set CLAUDE_CODE_USE_VERTEX=1 environment variable
> - **Microsoft Foundry**: set CLAUDE_CODE_USE_FOUNDRY=1 environment variable"

**Key Point:** All three are Claude-hosting cloud providers, not generic LLM providers. The SDK officially supports Claude through multiple channels, but not non-Claude models.

---

## 6. Service-Specific Terms Relevant to the SDK

**Source:** https://www.anthropic.com/legal/service-specific-terms

### Section D - Marketplace Services

> "Cloud Platforms that offer Hosted Services are: (1) Amazon Bedrock ('Bedrock'), which is hosted and managed by Amazon Web Services, Inc. and affiliates ('AWS'); and (2) Vertex AI ('Vertex'), which is hosted and managed by Google LLC and affiliates ('Google')."

This confirms that Bedrock and Vertex are officially sanctioned distribution channels for Claude.

### Section E - Development Partner Program

> "Customer may elect (in its sole discretion) to participate in the Development Partner Program by enabling the permissive data opt-in setting for the Services ('Development Partner Mode'). If Customer enables Development Partner Mode, Anthropic may use the data that Customer submits to the Services (e.g., Customer Content) in connection with Anthropic's products and services, including to train models."

**Note:** Only applies if you explicitly opt-in.

---

## 7. Usage Policy Relevant Sections

**Source:** https://www.anthropic.com/legal/aup

### Platform Abuse - Relevant Restriction

> "Utilization of inputs and outputs to train an AI model (e.g., 'model scraping' or 'model distillation') without prior authorization from Anthropic"

This prohibits using Claude outputs to train other models without authorization.

### Agentic Use Guidelines

> "Agentic use cases must still comply with the Usage Policy."

The Claude Agent SDK falls under this - all Usage Policy restrictions apply to agents built with the SDK.

---

## 8. Risk Assessment for Common Scenarios

| Scenario | Risk Level | Notes |
|----------|------------|-------|
| Using SDK with Claude via Anthropic API | None | Intended use |
| Using SDK with Claude via Bedrock/Vertex | None | Officially supported |
| Using SDK with Claude via OpenRouter | Low | OpenRouter is an authorized reseller |
| Using SDK with non-Claude models via OpenRouter | Medium | May violate "competing product" clause |
| Using SDK with local LLMs via proxy | Medium-High | Not technically compatible + legal ambiguity |
| Modifying Python SDK code for own use | Low | MIT license allows modifications |
| Redistributing modified SDK | Low | MIT license allows redistribution |
| Building a commercial product with SDK + Claude | None | Explicitly permitted in Section A.1 |
| Building a commercial product with SDK + GPT-5.2 | High | Likely violates "competing product" restriction |

---

## 9. Recommendations

### For Claude-Only Use

**Go ahead.** The SDK is explicitly designed and licensed for building commercial products powered by Claude models, whether through the direct API, Bedrock, Vertex, or Foundry.

### For Multi-Model/Non-Claude Use

**Proceed with caution:**

1. **Consult legal counsel** before building products that use the SDK with non-Claude models
2. **Consider alternatives:**
   - OpenAI Agents SDK for GPT models
   - LangChain/LangGraph for multi-provider support
   - Build your own agent framework

3. **If you must use the SDK with non-Claude models:**
   - Use the Python SDK (MIT licensed)
   - Document your interpretation of the Terms
   - Be prepared to defend that it doesn't constitute "competing product"

### For Testing/Research

Using the SDK with alternative models for personal testing or research (not commercial products) carries lower risk, but the Terms technically apply to all usage.

---

## 10. Source Documents

| Document | URL |
|----------|-----|
| Anthropic Commercial Terms of Service | https://www.anthropic.com/legal/commercial-terms |
| Anthropic Usage Policy | https://www.anthropic.com/legal/aup |
| Anthropic Service-Specific Terms | https://www.anthropic.com/legal/service-specific-terms |
| TypeScript SDK GitHub | https://github.com/anthropics/claude-agent-sdk-typescript |
| Python SDK GitHub | https://github.com/anthropics/claude-agent-sdk-python |
| Agent SDK Overview Docs | https://docs.claude.com/en/api/agent-sdk/overview |

---

## 11. Exact License Text Quotes

### TypeScript SDK LICENSE.md

\`\`\`
© Anthropic PBC. All rights reserved. Use is subject to Anthropic's Commercial Terms of Service.
\`\`\`

### Python SDK LICENSE (Full MIT)

\`\`\`
MIT License

Copyright (c) 2025 Anthropic, PBC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
\`\`\`

### Commercial Terms - Use Restrictions (Section D.4)

\`\`\`
Customer may not and must not attempt to (a) access the Services to build a
competing product or service, including to train competing AI models or resell
the Services except as expressly approved by Anthropic; (b) reverse engineer or
duplicate the Services; or (c) support any third party's attempt at any of the
conduct restricted in this sentence.
\`\`\`

### SDK README - License Statement

\`\`\`
Use of this SDK is governed by Anthropic's Commercial Terms of Service, including
when you use it to power products and services that you make available to your
own customers and end users, except to the extent a specific component or
dependency is covered by a different license as indicated in that component's
LICENSE file.
\`\`\`

---

## 12. Conclusion

The Claude Agent SDK licensing situation is nuanced:

1. **Code License:**
   - Python SDK: MIT (permissive)
   - TypeScript SDK: Proprietary

2. **Usage License:** Commercial Terms of Service apply to all SDK usage

3. **Non-Claude Models:**
   - Not explicitly prohibited
   - May violate "competing product" restriction if used commercially
   - Technical barriers exist (API format compatibility)

4. **Commercial Use:**
   - Explicitly permitted for Claude-powered products
   - Ambiguous for non-Claude-powered products

**Bottom Line:** If you want to use the Claude Agent SDK's architecture with non-Claude models for commercial purposes, either get explicit approval from Anthropic or use a different agent framework designed for multi-provider support.

---

*Research conducted: January 23, 2026*
*Sources verified as of research date*
