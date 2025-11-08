# Model Context Protocol Community Documentation Summary

This summary covers the complete community governance, collaboration, and contribution framework for the Model Context Protocol (MCP) project, based on documentation files in the `community/` folder.

## Overview

The MCP project maintains a comprehensive governance structure and community collaboration framework designed to enable transparent, inclusive, and effective open-source development of a universal standard for model-to-world interactions. The community operates through formal governance hierarchies, collaborative working structures, and clear communication channels.

---

## 1. Governance and Stewardship

### Governance Structure

MCP follows a hierarchical technical governance model similar to Python and PyTorch:

**Technical Hierarchy:**
- **Contributors**: Community members who file issues, make pull requests, and contribute to the project
- **Maintainers**: Drive specific components (SDKs, documentation, etc.) within the MCP project
- **Core Maintainers**: Oversee maintainers and drive overall project direction
- **Lead Core Maintainers (BDFL)**: Ultimate decision-makers for the project
- **MCP Steering Group**: Consists of all maintainers, core maintainers, and lead core maintainers

**Key Principles:**
- All maintainers must have a strong bias towards MCP's design philosophy
- Membership is for individuals, not companies (no corporate seats)
- Maintainers act in the best interests of the protocol and open source community
- All decisions must be recorded transparently on the shared Discord server

### Current Leadership

**Lead Maintainers:**
- Justin Spahr-Summers
- David Soria Parra

**Current Core Maintainers:**
- Inna Harper
- Basil Hosmer
- Paul Carleton
- Nick Cooper
- Nick Aldridge
- Che Liu
- Den Delimarsky

### Roles and Responsibilities

**Maintainers:**
- Responsible for Working or Interest Groups within MCP
- Engage thoughtfully with community contributors
- Maintain and improve their respective areas
- Support documentation, roadmaps, and adjacent project parts
- Present community ideas to core maintainers
- Have write/admin access to their respective repositories
- Can be appointed or removed by core/lead maintainers at any time

**Core Maintainers:**
- Design, review, and steer evolution of the MCP specification
- Articulate cohesive long-term vision
- Mediate and resolve contentious issues fairly and transparently
- Appoint or remove maintainers
- Have power to veto maintainer decisions by majority vote
- Generally have write/admin access to all MCP repositories
- Should use pull-request contribution mechanism like outside contributors
- Meet bi-weekly to discuss and vote on proposals

**Lead Maintainers:**
- Can veto any decision by core or regular maintainers
- Must publicly articulate decision-making with clear reasoning
- Responsible for confirming or removing core maintainers
- Administrators on all MCP project infrastructure
- Act as "Benevolent Dictators for Life" (BDFL model)

### Decision-Making Process

- Core maintainer group meets every two weeks
- Discussions and votes happen on shared Discord server
- Lead, core, and maintainer groups aim to meet in-person every 3-6 months
- All groups should use same contribution process as external contributors
- Decisions must be documented transparently

### Nomination and Removal Process

**Principles:**
- Membership given to individuals on merit basis
- Must demonstrate strong expertise through contributions, reviews, discussions
- Must align with overall MCP principles and direction
- No term limits for maintainers or core maintainers
- Light criteria for moving to 'emeritus' status after long inactivity
- Membership is individual, not corporate

**Nomination Steps:**
1. Collect evidence (history of merged PRs)
2. Discuss among relevant maintainer group
3. Create private Discord channel for nomination
4. Provide context including:
   - GitHub/LinkedIn profiles, Discord username
   - Groups for nomination
   - Group agreement
   - Description of contributions and expected future contributions
   - Current employer, motivations, other context
5. Core/Lead Maintainers discuss and vote
6. If favorable, add to appropriate groups and announce
7. Delete temporary channel after one week

**Removal:**
- Core Maintainers can add/remove regular maintainers
- Lead Maintainers can add/remove core maintainers
- Can be done at any time without stated reason

---

## 2. Working and Interest Groups

MCP organizes collaboration through two distinct structures designed to facilitate focused discussions and concrete deliverables.

### Purpose

These groups exist to:
- **Facilitate high-signal focused discussions**: Contributors opt into notifications, expertise sharing, and regular meetings for relevant topics
- **Establish clear expectations and leadership**: Guide collaborative efforts toward concrete deliverables advancing MCP evolution and adoption

### Meeting Calendar

All meetings published at: **[meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)**

Facilitators must post meeting schedules in advance for discoverability and community participation.

### Interest Groups (IGs)

**Goal:** Facilitate discussion and knowledge-sharing among contributors who share interests in specific MCP sub-topics or contexts. Primary focus is identifying and gathering problems worth addressing through SEPs or other artifacts, while encouraging open exploration of protocol issues and opportunities.

**Expectations:**
- Regular conversations in Interest Group Discord channel
- AND/OR recurring live meetings regularly attended by members
- Meeting dates/times published on MCP community calendar
- Tagged with primary topic and IG Discord channel name (e.g., `auth-ig`)
- Notes publicly shared after meetings as GitHub issues or public Google Docs

**Examples:**
- Security in MCP
- Auth in MCP
- Using MCP in enterprise settings
- Tooling and practices for hosting MCP servers
- Tooling and practices for implementing MCP clients

**Lifecycle:**
- **Creation:** Fill template in #wg-ig-group-creation Discord channel
- Community moderator reviews and calls for vote in private #community-moderators channel
- Majority positive vote over 72h period approves creation
- Creation can be reversed anytime (core/lead maintainers can veto)
- Facilitator(s) and Maintainer(s) organize IG meeting expectations
  - **Facilitator**: Informal role shepherding or speaking for group
  - **Maintainer**: Official representative from MCP steering group (optional)
- **Retirement:** Only when moderators or core/lead maintainers determine it's no longer active/needed
- Successful IGs have no time limit as long as active and maintained

**Creation Template:**
- Facilitator(s)
- Maintainer(s) (optional)
- IGs with potentially similar goals/discussions
- How this IG differentiates from related IGs
- First topic to discuss within the IG

**Note:** IG participation not required to start WG or create SEP, but building consensus in IGs valuable when justifying WG formation or strengthening SEPs.

### Working Groups (WGs)

**Goal:** Facilitate collaboration on a SEP, themed series of SEPs, or otherwise officially endorsed project.

**Expectations:**
- Meaningful progress towards at least one SEP or spec-related implementation OR hold maintenance responsibilities for projects (Inspector, Registry, SDKs)
- Facilitators track progress and communicate status when appropriate
- Meeting dates/times published on MCP community calendar
- Tagged with primary topic and WG Discord channel name (e.g., `agents-wg`)
- Notes publicly shared after meetings as GitHub issues or public Google Docs

**Examples:**
- Registry
- Inspector
- Tool Filtering
- Server Identity

**Lifecycle:**
- **Creation:** Fill template in #wg-ig-group-creation Discord channel
- Community moderator reviews and calls for vote in private #community-moderators channel
- Majority positive vote over 72h period approves creation
- Creation can be reversed anytime (core/lead maintainers can veto)
- Facilitator(s) and Maintainer(s) organize WG meeting expectations
  - **Facilitator**: Informal role shepherding or speaking for group
  - **Maintainer**: Official representative from MCP steering group (optional)
- **Retirement:** When either:
  - Moderators or core/lead maintainers decide no longer active/needed
  - WG has no active Issue/PR for a month or more, or completed all intended Issues/PRs

**Creation Template:**
- Facilitator(s)
- Maintainer(s) (optional)
- Explanation of interest/use cases (ideally from IG discussion, but not required)
- First Issue/PR/SEP that the WG will work on

### Facilitators

- **NOT** equivalent to maintainership role across MCP organization
- Informal role anyone can self-nominate into
- Responsible for shepherding discussions and collaboration within IG or WG
- Lead and Core Maintainers can modify Facilitator/Maintainer lists anytime

### Governance Principles for Groups

All groups are self-governed while adhering to core principles:
1. Clear contribution and decision-making processes
2. Open communication and transparent decisions

Both must:
- Document contribution process
- Maintain transparent communication
- Make decisions publicly (publish meeting notes and proposals)

**Default processes** (for groups without specified processes):
- GitHub pull requests and issues for contributions
- Public channel in official MCP Contributor Discord

### Contribution Pathway

The IG/WG structure provides an elegant on-ramp for contributors:
1. Join Discord, follow IG conversations, attend live calls, participate
2. Offer to facilitate calls, contribute use cases in SEPs and other work
3. Jump in to contribute to WG deliverables when comfortable
4. Active valuable contributors nominated by WG maintainers as new maintainers

### Finding Groups

Current list of WGs and IGs available on MCP Contributor Discord in dedicated section of channels.

---

## 3. Specification Enhancement Proposals (SEPs)

### What is a SEP?

SEP stands for Specification Enhancement Proposal. It is a design document that:
- Provides information to the MCP community
- Describes new features for Model Context Protocol or its processes/environment
- Provides concise technical specification and rationale

**Purpose:**
- Primary mechanism for proposing major new features
- Collecting community input on issues
- Documenting design decisions that go into MCP
- SEP author builds consensus and documents dissenting opinions
- Maintained as GitHub Issues, creating revision history as historical record

### What Qualifies as a SEP?

Reserve SEP process for changes substantial enough to require:
- Broad community discussion
- Formal design document
- Historical record of decision-making

**Consider proposing SEP for:**
- **New Feature or Protocol Change:**
  - Adding new API endpoints or methods
  - Changing syntax/semantics of existing data structures/messages
  - Introducing new interoperability standards between MCP-compatible tools
  - Significant changes to specification definition, presentation, or validation
- **Breaking Changes:** Any non-backwards-compatible change
- **Governance or Process Changes:** Altering decision-making or contribution guidelines
- **Complex or Controversial Topics:** Multiple valid solutions or significant debate expected

For smaller, direct changes, regular GitHub issue or pull request often more appropriate.

### SEP Types

1. **Standards Track SEP:**
   - Describes new feature or implementation for Model Context Protocol
   - May describe interoperability standard supported outside core protocol specification

2. **Informational SEP:**
   - Describes MCP design issue
   - Provides general guidelines or information to community
   - Does not propose new feature
   - Does not necessarily represent community consensus or recommendation

3. **Process SEP:**
   - Describes process surrounding MCP
   - Proposes change to or event in a process
   - Like Standards Track but applies to areas other than MCP protocol itself

### SEP Workflow

**Submission Location:** GitHub Issue in [specification repository](https://github.com/modelcontextprotocol/modelcontextprotocol)

**Workflow Steps:**

1. **SEP author creates well-formatted GitHub Issue:**
   - Tag with `SEP` and `proposal` labels
   - SEP number = GitHub Issue number (used interchangeably)

2. **Find sponsor:**
   - Must be Core Maintainer or Maintainer from MCP steering group
   - Maintainers regularly review open proposals to determine sponsorship
   - Can tag relevant maintainers from maintainer list in proposal
   - **Sponsor responsibilities:**
     - Ensure proposal actively developed
     - Ensure meets quality standard
     - Present and discuss in core maintainer meetings

3. **Once sponsor found:**
   - GitHub Issue assigned to sponsor
   - Sponsor adds `draft` tag
   - Ensures SEP number in title
   - Assigns milestone

4. **Sponsor informal review:**
   - Reviews proposal
   - May request changes based on community feedback
   - When ready, adds `in-review` tag

5. **Formal review:**
   - After `in-review` tag added, enters formal Core Maintainer review
   - May be accepted, rejected, or returned for revision

6. **No sponsor within three months:**
   - Core Maintainers may close SEP as `dormant`

**Note:** Proposals without sponsors reviewed in regular intervals. Proposals without sponsor within six months automatically rejected.

### SEP Format

Each SEP should include:

1. **Preamble:**
   - Short descriptive title
   - Names and contact info for each author
   - Current status

2. **Abstract:**
   - Short (~200 word) description of technical issue being addressed

3. **Motivation:**
   - Clearly explain why existing protocol specification inadequate
   - Critical for SEPs changing Model Context Protocol
   - Submissions without sufficient motivation may be rejected outright

4. **Specification:**
   - Describe syntax and semantics of new protocol feature
   - Detailed enough for competing, interoperable implementations
   - PR with specification changes should be provided

5. **Rationale:**
   - Explain why particular design decisions made
   - Describe alternate designs considered and related work
   - Provide evidence of community consensus
   - Discuss important objections/concerns raised during discussion

6. **Backward Compatibility:**
   - SEPs introducing backward incompatibilities must include section describing them and their severity
   - Explain how author proposes to deal with incompatibilities

7. **Reference Implementation:**
   - Must be completed before SEP given "Final" status
   - Need not be completed before SEP accepted
   - Follows principle of "rough consensus and running code" for resolving protocol details

8. **Security Implications:**
   - Explicitly write out security concerns
   - Make reviewers aware of security considerations

### SEP States

- **`proposal`**: SEP proposal without sponsor
- **`draft`**: SEP proposal with sponsor
- **`in-review`**: SEP proposal ready for review
- **`accepted`**: Accepted by Core Maintainers, still requires final wording and reference implementation
- **`rejected`**: Rejected by Core Maintainers
- **`withdrawn`**: Withdrawn (may be re-submitted later)
- **`final`**: Finalized with reference implementation complete and incorporated
- **`superseded`**: Replaced by newer SEP
- **`dormant`**: Has not found sponsors and was closed

### SEP Review & Resolution

**Review Schedule:** Core Maintainers review SEPs bi-weekly

**Acceptance Criteria:**
- Prototype implementation demonstrating proposal
- Clear benefit to MCP ecosystem
- Community support and consensus

**After Acceptance:**
- Reference implementation must be completed
- When complete and incorporated into main source code, status changes to "Final"

**Other Outcomes:**
- Can be "Rejected" or "Withdrawn"
- Withdrawn SEPs may be re-submitted later

### Reporting Bugs or Submitting Updates

For SEPs not yet `final`:
- Best to send comments/changes directly to SEP author

For finalized SEPs:
- Submit corrections as GitHub comment on issue or PR to reference implementation

### Transferring SEP Ownership

**Good reasons:**
- Original author lacks time/interest
- Author unreachable or not responding

**Bad reason:**
- Disagreeing with SEP direction (submit competing SEP instead)

Process aims to retain original author as co-author, but up to original author. Project tries to build consensus, but competing SEPs possible when consensus not achievable.

### Copyright

SEP guidelines document placed in public domain or under CC0-1.0-Universal license, whichever more permissive.

---

## 4. Communication Channels

MCP provides multiple channels for different types of communication and collaboration.

### Channel Overview

- **[Discord](https://discord.gg/6CSzBmMkjX)**: Real-time or ad-hoc discussions
- **[GitHub Discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions)**: Structured, longer-form discussions
- **[GitHub Issues](https://github.com/modelcontextprotocol/modelcontextprotocol/issues)**: Actionable tasks, bug reports, feature requests
- **Security Issues**: Follow process in [SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md)

All communication governed by [Code of Conduct](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CODE_OF_CONDUCT.md). Expectation of respectful, professional, inclusive interactions across all channels.

### Discord

**Purpose:** Real-time contributor discussion and collaboration. Designed around **MCP contributors**, not for general MCP support.

**Server Structure:** Both public and private channels

#### Public Channels (Default)

**Purpose:** Open community engagement, collaborative development, transparent project coordination

**Primary Use Cases:**
- **Public SDK and tooling development**: All development from ideation to release planning (e.g., `#typescript-sdk-dev`, `#inspector-dev`)
- **Working and Interest Group discussions**
- **Community onboarding** and contribution guidance
- **Community feedback** and collaborative brainstorming
- Public **office hours** and **maintainer availability**

**Avoid:**
- **MCP user support**: Participants expected to read official docs and start GitHub Discussions for questions/support
- **Service/product marketing**: Interactions vendor-neutral, not for brand-building or sales. Brand/product mentions discouraged outside examples or specification-focused responses

#### Private Channels (Exceptions)

**Purpose:** Confidential coordination and sensitive matters that cannot be discussed publicly. Access restricted to designated maintainers.

**Strict Criteria for Private Use:**
- **Security incidents** (CVEs, protocol vulnerabilities)
- **People matters** (maintainer-related discussions, code of conduct policies)
- Select channels configured as **read-only** (e.g., maintainer decision making)
- Coordination requiring **immediate** or **focused response** with limited audience

**Transparency Requirements:**
- **All technical and governance decisions** affecting community **must be documented** in GitHub Discussions/Issues, labeled with `notes`
- **Some individual contributor matters** may remain private when appropriate (personal circumstances, disciplinary actions, sensitive individual matters)
- Private channels used as **temporary "incident rooms"**, not for routine development

**Important:** Any significant Discord discussion leading to potential decision/proposal must be moved to GitHub Discussion or Issue to create persistent, searchable record. Proposals then promoted to full-fledged PRs with associated work items (GitHub Issues) as needed.

### GitHub Discussions

**Purpose:** Structured, long-form discussion and debate on project direction, features, improvements, community topics

**When to Use:**
- Project roadmap planning and milestone discussions
- Announcements and release communications
- Community polls and consensus-building processes
- Feature requests with context and rationale
- If specific repository doesn't have Discussions enabled, open GitHub Issue instead

### GitHub Issues

**Purpose:** Bug reports, feature tracking, actionable development tasks

**When to Use:**
- Submit SEP proposals (following SEP guidelines)
- Bug reports with reproducible steps
- Documentation improvements with specific scope
- CI/CD problems and infrastructure issues
- Release tasks and milestone tracking

### Security Issues

**Critical:** **Do NOT post security issues publicly**

**Process:**
1. Use private security reporting process (follow [SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md) for protocol-level issues)
2. Contact lead and/or core maintainers directly
3. Follow responsible disclosure guidelines

### Decision Records

All MCP decisions documented and captured in public channels:

- **Technical decisions**: GitHub Issues and SEPs
- **Specification changes**: [MCP website changelog](https://modelcontextprotocol.io/specification/draft/changelog)
- **Process changes**: [Community documentation](https://modelcontextprotocol.io/community/governance)
- **Governance decisions/updates**: GitHub Issues and SEPs

**Documentation Context Retention:**
- Decision makers
- Background context and motivation
- Options considered
- Rationale for chosen approach
- Implementation steps

---

## 5. Antitrust Policy

**Effective Date:** September 29, 2025

### Introduction

MCP's mission is developing a universal standard for model-to-world interactions, enabling LLMs and agents to seamlessly connect with external data sources and tools. The Antitrust Policy exists to avoid antitrust risks while carrying out this pro-competitive mission.

### Core Principle

**Goal of Antitrust Laws:** Encourage vigorous competition

**Project Commitment:** Nothing in policy prohibits or limits participants' ability to make, sell, or use any product, or otherwise compete in marketplace.

**Policy Nature:**
- Provides general guidance on compliance with Antitrust Law
- Conservative and intended to promote compliance
- Does not create duties/obligations beyond what Antitrust Laws actually require
- If inconsistency exists between policy and Antitrust Laws, laws preempt and control

**Compliance Expectation:** All participants and contributors use best reasonable efforts to comply with all applicable state/federal antitrust and trade regulation laws, and antitrust/competition laws of other countries (collectively "Antitrust Laws").

### Participation

Technical participation in MCP shall be **open to all**, subject only to compliance with project charter and governance documents.

### Conduct of Meetings

**Risk:** Meetings among actual or potential competitors may lead to improper disclosure/discussion of information violating Antitrust Laws or anti-competitive behavior.

**Prohibited Topics** at Project-related meetings, conference calls, or forums:

Participants **must not** discuss or exchange information regarding:
- Individual company's current/projected prices, price changes, differentials, markups, discounts, allowances, terms/conditions of sale (including credit terms), or data bearing on prices (profits, margins, cost)
- Industry-wide pricing policies, price levels, price changes, differentials, or similar
- Actual/projected changes in industry production, capacity, or inventories
- Bids or intentions to bid for particular products, procedures for responding to bid invitations, or specific contractual arrangements
- Individual company plans concerning design, characteristics, production, distribution, marketing, or introduction dates of particular products (including proposed territories or customers)
- Matters relating to actual/potential individual suppliers that might exclude them from any market or influence business conduct toward such suppliers
- Matters relating to actual/potential customers that might influence business conduct toward such customers
- Individual company current/projected cost of procurement, development, or manufacture of any product
- Individual company market shares for any product or all products
- Confidential or otherwise sensitive business plans or strategy

**Required Behaviors** at all Project Meetings:

Participants **must:**
- Adhere to prepared agendas
- Insist meeting minutes be prepared and distributed to all participants
- Ensure meeting minutes accurately reflect matters that transpired
- Consult with their respective counsel on all antitrust questions related to Project Meetings
- Protest against any discussions appearing to violate these policies or Antitrust Laws
- Leave any meeting where such discussions continue
- Insist such protest be noted in minutes

### Requirements/Standard Setting

The Project may establish standards, technical requirements, and/or specifications for use (collectively "requirements").

**Restrictions:**
- Participants **shall not** enter agreements prohibiting or restricting any participant from establishing or adopting any other requirements
- Participants **shall not** undertake efforts (directly or indirectly) to prevent any firm from manufacturing, selling, or supplying any product not conforming to a requirement
- Project **shall not** promote standardization of commercial terms (such as terms for license and sale)

### Contact Information

To contact MCP regarding Antitrust Policy matters:
- Email: **antitrust@modelcontextprotocol.io**
- Subject line: Reference "Antitrust Policy"

---

## Key Relationships Between Components

### How Components Work Together

1. **Governance provides framework** for all community activities:
   - Lead and Core Maintainers oversee entire project
   - Maintainers responsible for specific areas
   - All decisions documented transparently

2. **Working and Interest Groups organize collaboration:**
   - IGs identify problems and facilitate discussions
   - WGs produce concrete deliverables (SEPs, implementations)
   - Both feed into SEP process and specification evolution
   - Groups self-governed within governance principles

3. **SEPs formalize changes:**
   - Primary mechanism for proposing major features
   - Require sponsor from steering group
   - Go through defined workflow from proposal to final
   - Require prototype, community support, and reference implementation

4. **Communication channels support all activities:**
   - Discord for real-time collaboration (especially WG/IG meetings)
   - GitHub Discussions for structured long-form discourse
   - GitHub Issues for actionable tasks and SEP proposals
   - All decisions documented publicly for transparency

5. **Antitrust Policy protects project:**
   - Ensures open, competitive participation
   - Sets clear boundaries for meeting conduct
   - Prevents anti-competitive behavior
   - Maintains MCP's pro-competitive mission

### Contribution Pathway Flow

**Entry → Engagement → Contribution → Leadership:**

1. Join Discord, participate in Interest Groups
2. Attend meetings, contribute to discussions
3. Offer to facilitate, contribute use cases to SEPs
4. Contribute to Working Group deliverables
5. Get nominated as maintainer based on valuable contributions

### Decision-Making Flow

**Proposal → Sponsorship → Review → Implementation:**

1. Community identifies need (often through IG discussions)
2. SEP created by author in GitHub Issues
3. Sponsor found from steering group
4. Informal review and iteration
5. Formal review by Core Maintainers
6. Acceptance or rejection
7. Reference implementation
8. Finalization and integration

---

## Important Policies and Expectations

### Transparency

- All technical and governance decisions documented publicly
- Meeting notes shared as GitHub issues or public Google Docs
- Private channels only for security incidents, people matters, or immediate coordination
- Decision records retain full context (decision makers, motivation, alternatives, rationale, implementation)

### Open Participation

- Technical participation open to all
- Based on individual merit, not company affiliation
- No corporate seats in governance
- Maintainers act in best interest of protocol and community

### Quality and Consensus

- SEPs require prototype, clear benefit, and community support
- Changes substantial enough for SEP process get formal review
- Smaller changes use regular GitHub workflow
- Rough consensus and running code principle

### Professional Conduct

- All communication governed by Code of Conduct
- Respectful, professional, inclusive interactions expected
- Security issues handled through responsible disclosure
- Antitrust compliance mandatory at all meetings

---

## Resources and Links

### Primary Links

- **Community Calendar:** [meet.modelcontextprotocol.io](https://meet.modelcontextprotocol.io/)
- **Discord Server:** [discord.gg/6CSzBmMkjX](https://discord.gg/6CSzBmMkjX)
- **GitHub Discussions:** [github.com/modelcontextprotocol/modelcontextprotocol/discussions](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions)
- **GitHub Issues:** [github.com/modelcontextprotocol/modelcontextprotocol/issues](https://github.com/modelcontextprotocol/modelcontextprotocol/issues)
- **Specification Repository:** [github.com/modelcontextprotocol/specification](https://github.com/modelcontextprotocol/specification)
- **Maintainer List:** [github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/MAINTAINERS.md)
- **Security Policy:** [github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/SECURITY.md)
- **Code of Conduct:** [github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CODE_OF_CONDUCT.md](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/CODE_OF_CONDUCT.md)
- **Specification Changelog:** [modelcontextprotocol.io/specification/draft/changelog](https://modelcontextprotocol.io/specification/draft/changelog)
- **Community Documentation:** [modelcontextprotocol.io/community/governance](https://modelcontextprotocol.io/community/governance)

### Contact Information

- **Antitrust Policy:** antitrust@modelcontextprotocol.io

---

## Summary

The Model Context Protocol has established a comprehensive, transparent, and inclusive community framework that enables effective collaboration on developing a universal standard for model-to-world interactions. The framework balances formal governance structures with flexible collaboration mechanisms, ensuring both accountability and innovation.

Key strengths of the MCP community framework:

1. **Clear hierarchy with distributed responsibility**: From contributors to lead maintainers, each level has defined roles and accountabilities
2. **Multiple pathways for participation**: Interest Groups for discussion, Working Groups for deliverables, direct SEP submission
3. **Transparent decision-making**: All decisions documented publicly with full context
4. **Formal change process**: SEPs provide structured way to propose, review, and implement major changes
5. **Open and competitive**: Individual merit-based participation, no corporate control
6. **Legal compliance**: Strong antitrust policy protecting project's pro-competitive mission
7. **Appropriate communication channels**: Right tool for each type of interaction (Discord, Discussions, Issues)

This framework positions MCP for sustainable, community-driven evolution while maintaining technical excellence and legal compliance.
