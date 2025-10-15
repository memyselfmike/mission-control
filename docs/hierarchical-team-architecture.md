# Mission Control: Hierarchical Team Architecture
**Extending Solution Architecture with Nested Teams, Executive Managers, and Quality Control Loops**

**Date:** 2025-10-15
**Version:** 1.1.0
**Status:** ARCHITECTURAL ENHANCEMENT

---

## Executive Summary

This document extends the base solution architecture to support **hierarchical team structures** with:

- **Executive managers** (CMO, CTO, CFO, CPO, etc.) that act as team orchestrators
- **Nested team hierarchies** (dept → team → sub-team → specialists)
- **Quality control loops** (QA agents validate outputs, trigger revisions)
- **Cross-functional collaboration** (teams coordinate on complex initiatives)

**Key Innovation:** Instead of flat structure (Alex → 5 specialists), we enable **multi-level organizations** where executive managers delegate to teams, teams delegate to sub-teams, and QA loops ensure quality.

---

## The Problem with Flat Structure

**Current Architecture (Flat):**
```
Alex (Chief of Staff)
├─ Jordan (Strategist)
├─ Quinn (Planner)
├─ Taylor (Operator)
├─ Sam (Analyst)
└─ Morgan (Researcher)
```

**Limitations:**
- ❌ No specialization depth (Morgan does ALL research - marketing, tech, legal, etc.)
- ❌ No quality control (agents produce outputs, no validation loop)
- ❌ No team coordination (multiple specialists working on related tasks don't collaborate)
- ❌ No domain expertise (need CMO for marketing, CTO for technical decisions)
- ❌ Doesn't scale (50+ specialists would be chaos)

---

## Hierarchical Team Architecture

### New Structure (Hierarchical)

```
Alex (Chief of Staff - CEO Level)
│
├─ CMO (Chief Marketing Officer) - Executive Manager
│   ├─ Content Team Lead
│   │   ├─ Blog Writer (specialist)
│   │   ├─ Social Media Writer (specialist)
│   │   ├─ Email Copywriter (specialist)
│   │   └─ Content QA Agent (quality control)
│   │
│   ├─ SEO Team Lead
│   │   ├─ Technical SEO Specialist
│   │   ├─ Content SEO Specialist
│   │   ├─ Link Building Specialist
│   │   └─ SEO QA Agent (quality control)
│   │
│   ├─ Paid Acquisition Team Lead
│   │   ├─ Google Ads Specialist
│   │   ├─ Facebook Ads Specialist
│   │   ├─ LinkedIn Ads Specialist
│   │   └─ Ads QA Agent (quality control)
│   │
│   └─ Brand Team Lead
│       ├─ Brand Strategist
│       ├─ Visual Designer
│       ├─ Copywriter
│       └─ Brand QA Agent (quality control)
│
├─ CTO (Chief Technology Officer) - Executive Manager
│   ├─ Engineering Team Lead
│   │   ├─ Backend Engineer
│   │   ├─ Frontend Engineer
│   │   ├─ DevOps Engineer
│   │   └─ Code Review Agent (quality control)
│   │
│   ├─ Product Team Lead
│   │   ├─ Product Designer
│   │   ├─ UX Researcher
│   │   ├─ Product Analyst
│   │   └─ Design QA Agent (quality control)
│   │
│   └─ QA Team Lead
│       ├─ Test Engineer
│       ├─ Security Tester
│       ├─ Performance Tester
│       └─ QA Validator (meta quality control)
│
├─ CFO (Chief Financial Officer) - Executive Manager
│   ├─ Accounting Team Lead
│   │   ├─ Bookkeeper
│   │   ├─ Tax Specialist
│   │   ├─ Audit Specialist
│   │   └─ Accounting QA Agent
│   │
│   ├─ Finance Team Lead
│   │   ├─ FP&A Analyst
│   │   ├─ Investment Analyst
│   │   ├─ Risk Analyst
│   │   └─ Finance QA Agent
│   │
│   └─ Treasury Team Lead
│       ├─ Cash Management Specialist
│       ├─ Banking Relations Specialist
│       └─ Treasury QA Agent
│
├─ CPO (Chief People Officer) - Executive Manager
│   ├─ Recruiting Team Lead
│   │   ├─ Technical Recruiter
│   │   ├─ Sales Recruiter
│   │   ├─ Executive Recruiter
│   │   └─ Recruiting QA Agent
│   │
│   ├─ People Ops Team Lead
│   │   ├─ Onboarding Specialist
│   │   ├─ Benefits Administrator
│   │   ├─ Culture Manager
│   │   └─ People Ops QA Agent
│   │
│   └─ Learning & Development Team Lead
│       ├─ Training Designer
│       ├─ Career Coach
│       └─ L&D QA Agent
│
└─ Jordan (Strategist) - Executive Advisor (remains at C-level)
    Quinn (Planner) - Executive Advisor
    Taylor (Operator) - Executive Advisor
    Sam (Analyst) - Executive Advisor
    Morgan (Researcher) - Director of Research
```

---

## Agent Types in Hierarchical System

### 1. C-Level Orchestrators

**Role:** Executive managers that own entire departments

**Characteristics:**
- Receive high-level directives from Alex
- Break down into team-level initiatives
- Coordinate cross-team collaboration
- Report up to Alex with summaries
- Own department OKRs and strategy

**Examples:**
- CMO (Chief Marketing Officer)
- CTO (Chief Technology Officer)
- CFO (Chief Financial Officer)
- CPO (Chief People Officer)
- COO (Chief Operating Officer)

**System Prompt Pattern:**
```
You are {Name}, Chief {Function} Officer.

ROLE:
You lead the {Function} department, managing {N} teams with {M} specialists.
You report directly to Alex (Chief of Staff).

RESPONSIBILITIES:
- Receive high-level objectives from Alex
- Break down into team-level initiatives
- Delegate to appropriate team leads
- Coordinate cross-team collaboration
- Ensure quality through QA loops
- Report progress and blockers to Alex

TEAM STRUCTURE:
{List of teams and their purposes}

DELEGATION RULES:
- Content strategy → Content Team Lead
- Technical SEO → SEO Team Lead
- Campaign execution → Paid Acquisition Team Lead
(etc.)

QUALITY STANDARDS:
All outputs must pass QA validation before delivery to Alex.
If QA fails, work with team to revise until standards met.

COLLABORATION:
Work with other C-level executives on cross-functional initiatives.
Example: CMO + CTO collaborate on website redesign.
```

### 2. Team Leads

**Role:** Manage specialist teams, coordinate work, ensure quality

**Characteristics:**
- Receive initiatives from C-level executive
- Break down into specialist tasks
- Assign work to appropriate specialists
- Coordinate specialist collaboration
- Trigger QA loops
- Report up to executive with results

**Examples:**
- Content Team Lead (reports to CMO)
- Engineering Team Lead (reports to CTO)
- Accounting Team Lead (reports to CFO)

**System Prompt Pattern:**
```
You are {Name}, {Team} Team Lead.

ROLE:
You manage a team of {N} specialists under {Executive} (C-level).

TEAM MEMBERS:
{List specialists and their expertise}

RESPONSIBILITIES:
- Receive initiatives from {Executive}
- Break down into specialist tasks
- Delegate to appropriate specialists
- Coordinate collaboration between specialists
- Trigger QA validation for all outputs
- Handle revision loops if QA fails
- Report results to {Executive}

QUALITY PROCESS:
1. Specialist produces output
2. Send to {QA Agent} for validation
3. If pass → deliver to {Executive}
4. If fail → work with specialist to revise
5. Repeat until QA passes

COLLABORATION:
Coordinate with other team leads when initiatives overlap.
```

### 3. Specialist Agents

**Role:** Execute specific tasks with deep domain expertise

**Characteristics:**
- Receive tasks from Team Lead
- Execute with specialized knowledge
- Produce outputs (documents, code, analysis, etc.)
- Accept revision feedback from QA
- Iterate until quality standards met

**Examples:**
- Blog Writer (Content Team)
- Technical SEO Specialist (SEO Team)
- Backend Engineer (Engineering Team)
- Tax Specialist (Accounting Team)

**System Prompt Pattern:**
```
You are {Name}, {Specialty} Specialist.

ROLE:
You are an expert in {domain} on the {Team} team.

EXPERTISE:
{Detailed domain knowledge and best practices}

RESPONSIBILITIES:
- Receive tasks from {Team Lead}
- Execute with excellence and attention to detail
- Produce high-quality outputs
- Accept feedback from QA agent
- Revise until quality standards met

QUALITY STANDARDS:
{Specific criteria for your domain}

TOOLS:
{List of tools available to this specialist}

COLLABORATION:
Work with other specialists on your team when needed.
```

### 4. QA Agents (Quality Control)

**Role:** Validate outputs, trigger revision loops

**Characteristics:**
- Receive outputs from specialists
- Validate against quality criteria
- Provide detailed feedback if standards not met
- Trigger revision loops
- Approve when quality achieved

**Examples:**
- Content QA Agent (validates blog posts, emails, social content)
- Code Review Agent (validates code quality, security, performance)
- SEO QA Agent (validates keyword usage, meta tags, structure)
- Accounting QA Agent (validates accuracy, compliance, formatting)

**System Prompt Pattern:**
```
You are {Name}, {Domain} QA Agent.

ROLE:
You ensure all outputs from {Team} meet quality standards.

QUALITY CRITERIA:
{Detailed checklist specific to domain}

VALIDATION PROCESS:
1. Receive output from specialist
2. Check against quality criteria
3. If all criteria met:
   - Status: APPROVED
   - Reasoning: {why it passes}
   - Deliver to {Team Lead}
4. If any criteria fail:
   - Status: REVISION REQUIRED
   - Issues: {list specific problems}
   - Suggestions: {how to fix}
   - Return to specialist for revision

REVISION LOOP:
Continue validation → revision cycles until APPROVED.
Maximum 5 iterations (escalate to {Team Lead} if not resolved).

TONE:
Constructive, specific, helpful (not just "this is bad").
```

---

## Data Model for Hierarchical Teams

### Team Registry Schema

**File:** `data/teams/registry.json`

```json
{
  "version": "1.0.0",
  "teams": {
    "marketing": {
      "name": "Marketing",
      "executive": "cmo",
      "team_leads": ["content-lead", "seo-lead", "paid-acquisition-lead", "brand-lead"],
      "okrs": {
        "Q4-2025": [
          {"objective": "Achieve $100K MRR from inbound", "key_results": [...]}
        ]
      }
    },
    "content-team": {
      "name": "Content Team",
      "parent_team": "marketing",
      "team_lead": "content-lead",
      "specialists": ["blog-writer", "social-writer", "email-copywriter"],
      "qa_agent": "content-qa",
      "focus": "Produce high-quality content across blog, social, email channels"
    }
  }
}
```

### Agent Registry Schema (Enhanced)

**File:** `data/agents/registry.json`

```json
{
  "version": "1.1.0",
  "agents": {
    "cmo": {
      "session_id": "abc123",
      "type": "executive_manager",
      "agent_tier": "c-level",
      "department": "marketing",
      "manages_teams": ["content-team", "seo-team", "paid-acquisition-team", "brand-team"],
      "reports_to": "alex",
      "created_at": "2025-10-15T10:00:00Z",
      "model": "claude-sonnet-4-5-20250929",
      "tools": ["Read", "Write", "Task", "WebSearch"],
      "usage_count": 0
    },
    "content-lead": {
      "session_id": "def456",
      "type": "team_lead",
      "agent_tier": "team-lead",
      "team": "content-team",
      "manages_specialists": ["blog-writer", "social-writer", "email-copywriter"],
      "qa_agent": "content-qa",
      "reports_to": "cmo",
      "created_at": "2025-10-15T10:15:00Z",
      "model": "claude-sonnet-4-5-20250929",
      "tools": ["Read", "Write", "Task"],
      "usage_count": 0
    },
    "blog-writer": {
      "session_id": "ghi789",
      "type": "specialist",
      "agent_tier": "specialist",
      "team": "content-team",
      "specialty": "blog_writing",
      "reports_to": "content-lead",
      "qa_validated_by": "content-qa",
      "created_at": "2025-10-15T10:20:00Z",
      "model": "claude-sonnet-4-5-20250929",
      "tools": ["Read", "Write", "WebSearch", "WebFetch"],
      "usage_count": 0
    },
    "content-qa": {
      "session_id": "jkl012",
      "type": "qa_agent",
      "agent_tier": "qa",
      "team": "content-team",
      "validates_for": ["blog-writer", "social-writer", "email-copywriter"],
      "quality_criteria": "content-quality-checklist.yaml",
      "reports_to": "content-lead",
      "created_at": "2025-10-15T10:25:00Z",
      "model": "claude-sonnet-4-5-20250929",
      "tools": ["Read"],
      "usage_count": 0
    }
  }
}
```

---

## Quality Control Loop Pattern

### QA Workflow

```yaml
# workflows/qa-loop.yaml
name: qa-validation-loop
version: "1.0.0"
description: "Quality control loop with revision cycles"

inputs:
  - name: specialist_agent
    type: string
    description: "Agent that produced the output"

  - name: qa_agent
    type: string
    description: "QA agent that validates"

  - name: output_artifact
    type: string
    description: "Path to output file to validate"

  - name: quality_criteria
    type: string
    description: "Path to quality checklist YAML"

steps:
  - step: 1
    id: qa_validation
    goal: "QA agent validates output"
    action: |
      Load quality criteria from {quality_criteria}.
      Read output from {output_artifact}.
      Check against all criteria.

      Generate validation report:
      - Status: APPROVED | REVISION REQUIRED
      - Criteria Met: [list]
      - Criteria Failed: [list with explanations]
      - Suggestions: [specific improvements]

    validation:
      - if: status == "APPROVED"
        then: goto step 5 (delivery)
      - if: status == "REVISION REQUIRED"
        then: goto step 2 (revision)

  - step: 2
    id: revision_request
    goal: "Send revision request to specialist"
    action: |
      Create revision request with:
      - Original output
      - QA feedback (issues, suggestions)
      - Quality criteria that failed

      Send to {specialist_agent} via operator file.

  - step: 3
    id: specialist_revision
    goal: "Specialist revises output"
    action: |
      {specialist_agent} receives feedback.
      Revises output addressing all issues.
      Updates {output_artifact}.

  - step: 4
    id: re_validation
    goal: "QA re-validates revised output"
    action: |
      Repeat step 1 with revised output.

      If iteration count >= 5:
        Escalate to {team_lead} for manual intervention.

  - step: 5
    id: delivery
    goal: "Deliver approved output"
    action: |
      Mark operator file: Status = APPROVED BY QA
      Notify {team_lead}: Output ready for delivery.

outputs:
  - name: approved_output
    location: "{output_artifact}"

  - name: qa_report
    location: "{output_artifact}.qa-report.json"
    content:
      status: "APPROVED"
      iterations: 2
      criteria_met: [...]
      final_score: 95
```

### QA Criteria Example

**File:** `workflows/quality-criteria/content-quality.yaml`

```yaml
name: content-quality-criteria
version: "1.0.0"
applies_to: ["blog-writer", "social-writer", "email-copywriter"]

criteria:
  - id: C1
    name: "Clear value proposition"
    description: "Content clearly articulates value to reader in first paragraph"
    weight: 10

  - id: C2
    name: "SEO optimization"
    description: "Target keyword appears in title, first paragraph, and 2-3 times in body"
    weight: 8

  - id: C3
    name: "Engaging introduction"
    description: "First 2 sentences hook reader with question, stat, or compelling statement"
    weight: 7

  - id: C4
    name: "Scannable structure"
    description: "Uses headings (H2, H3), bullet points, short paragraphs (<4 sentences)"
    weight: 8

  - id: C5
    name: "Clear call-to-action"
    description: "Ends with specific, actionable CTA"
    weight: 9

  - id: C6
    name: "Grammar and spelling"
    description: "No grammar errors, no spelling mistakes"
    weight: 10

  - id: C7
    name: "Brand voice consistency"
    description: "Matches brand voice guidelines (professional, helpful, concise)"
    weight: 7

  - id: C8
    name: "Fact accuracy"
    description: "All claims are accurate and verifiable"
    weight: 10

scoring:
  passing_score: 75
  excellent_score: 90

validation_format:
  status: "APPROVED | REVISION REQUIRED"
  score: 0-100
  criteria_met: [C1, C2, C4, C6, C7, C8]
  criteria_failed: [C3, C5]
  feedback:
    - criterion: C3
      issue: "Introduction lacks hook - starts with generic statement"
      suggestion: "Open with question: 'Struggling with [problem]?' or stat: '[X]% of businesses face [challenge]'"
    - criterion: C5
      issue: "CTA is vague ('Learn more')"
      suggestion: "Use specific CTA: 'Download our [Resource Name]' or 'Schedule a demo'"
```

---

## Delegation Patterns in Hierarchical System

### Pattern 1: Simple Task (Single Specialist)

```
User → Alex → CMO → Content Lead → Blog Writer → Content QA → ✅ → Content Lead → CMO → Alex → User
```

**Flow:**
1. User: "Write a blog post about AI productivity tools"
2. Alex delegates to CMO: "We need content marketing initiative"
3. CMO delegates to Content Lead: "Blog post on AI productivity tools"
4. Content Lead delegates to Blog Writer: "Create 1500-word blog post, target keyword: 'AI productivity tools', SEO optimized"
5. Blog Writer produces draft, writes to operator file
6. Content Lead triggers QA validation
7. Content QA validates against content-quality.yaml
   - If FAIL → Revision loop (Blog Writer revises)
   - If PASS → Approved ✅
8. Content Lead reports to CMO: "Blog post complete, QA approved"
9. CMO reports to Alex: "Content deliverable ready"
10. Alex presents to user with Rich panel

### Pattern 2: Complex Initiative (Cross-Team Collaboration)

```
User → Alex → CMO + CTO (parallel)
              ↓           ↓
         Content Team  Engineering Team
              ↓           ↓
         Blog Writer   Frontend Engineer
              ↓           ↓
         Content QA    Code Review QA
              ↓           ↓
         Approved      Approved
              ↓           ↓
         CMO           CTO
              ↘           ↙
                  Alex
                   ↓
                  User
```

**Example:** "Launch new website with blog"

1. User: "We need a new website with a blog section"
2. Alex recognizes cross-functional initiative
3. Alex creates coordination plan, delegates to CMO + CTO in parallel
4. CMO owns content strategy:
   - Content Lead → Blog Writers produce 10 launch posts
   - SEO Lead → Technical SEO Specialist optimizes blog structure
   - Each output goes through QA loops
5. CTO owns technical implementation:
   - Engineering Lead → Frontend Engineer builds blog UI
   - Engineering Lead → Backend Engineer implements CMS
   - Code Review QA validates all code
6. CMO and CTO coordinate on integration (blog content fits UI)
7. Both executives report completion to Alex
8. Alex synthesizes and presents to user

### Pattern 3: Iterative Refinement (Quality Loop)

```
Specialist → Output v1 → QA → FAIL → Feedback
                                       ↓
Specialist ← Revision Request ←←←←←←←←┘
    ↓
Output v2 → QA → FAIL → Feedback
                  ↓
Output v3 → QA → PASS ✅ → Team Lead
```

**Example:** Blog post with SEO issues

```
Iteration 1:
- Blog Writer produces draft
- Content QA validates
- Issues found:
  * Keyword "AI productivity" only appears 1x (need 3-5x)
  * Missing meta description
  * H2 headings not optimized
- Status: REVISION REQUIRED

Iteration 2:
- Blog Writer revises addressing all issues
- Content QA re-validates
- Issues found:
  * Keyword now appears 8x (over-optimization)
  * Meta description too long (165 chars, max 155)
- Status: REVISION REQUIRED

Iteration 3:
- Blog Writer fine-tunes
- Content QA validates
- All criteria met ✅
- Status: APPROVED

Delivered to Content Lead → CMO → Alex → User
```

---

## Creating Teams Dynamically

### Team Creation Workflow

**User:** "I want to launch a marketing function"

**Alex Response:**
```
I'll create a Marketing department for you.

Creating team structure:
├─ CMO (Chief Marketing Officer) - Executive manager
├─ Content Team (blog, social, email)
├─ SEO Team (technical, content, link building)
├─ Paid Acquisition Team (Google, Facebook, LinkedIn ads)
└─ Brand Team (strategy, design, copy)

This will create:
- 1 executive (CMO)
- 4 team leads
- 12+ specialists
- 4 QA agents

Estimated setup time: 2-3 minutes
Approve? [Yes / Customize / Cancel]
```

**If user approves:**

1. Alex creates CMO agent using `create_executive_agent()`
2. CMO creates 4 team structures using `create_team()`
3. Each team lead creates specialists using `create_specialist()`
4. Each team lead creates QA agent using `create_qa_agent()`
5. All registered in team registry and agent registry
6. Alex reports: "Marketing department ready! You can now ask CMO to execute marketing initiatives."

### Team Creation Functions

```python
async def create_executive_agent(
    role: str,  # "CMO", "CTO", "CFO", etc.
    department: str,
    teams: List[str],
    reports_to: str = "alex"
) -> AgentMetadata:
    """Create C-level executive manager."""

    system_prompt = f"""
You are {role}, responsible for the {department} department.

You manage {len(teams)} teams:
{chr(10).join(f'- {team}' for team in teams)}

You report to {reports_to}.

Your role is to:
1. Receive high-level objectives from {reports_to}
2. Break down into team initiatives
3. Delegate to appropriate team leads
4. Coordinate cross-team collaboration
5. Ensure quality through QA validation
6. Report results to {reports_to}

Always use quality control loops before delivering work.
    """

    agent_def = create_dynamic_agent_definition(
        agent_name=role.lower(),
        description=f"Executive manager for {department}",
        expertise=system_prompt,
        tools=["Read", "Write", "Task", "WebSearch", "WebFetch"],
        model="claude-sonnet-4-5-20250929"
    )

    # Register in agent registry
    metadata = AgentMetadata(
        session_id=generate_session_id(),
        type="executive_manager",
        agent_tier="c-level",
        department=department,
        manages_teams=teams,
        reports_to=reports_to,
        created_at=datetime.now(),
        model="claude-sonnet-4-5-20250929",
        tools=agent_def.tools
    )

    registry.register_agent(role.lower(), metadata)

    return metadata

async def create_team(
    team_name: str,
    parent_team: Optional[str],
    executive: str,
    specialists: List[Dict[str, str]],  # [{"name": "blog-writer", "specialty": "blog writing"}, ...]
    focus: str
) -> TeamMetadata:
    """Create team with lead, specialists, and QA agent."""

    # Create team lead
    team_lead_name = f"{team_name}-lead"
    team_lead = await create_team_lead_agent(
        name=team_lead_name,
        team=team_name,
        executive=executive,
        specialists=[s["name"] for s in specialists]
    )

    # Create specialists
    for spec in specialists:
        await create_specialist_agent(
            name=spec["name"],
            team=team_name,
            team_lead=team_lead_name,
            specialty=spec["specialty"]
        )

    # Create QA agent
    qa_agent = await create_qa_agent(
        name=f"{team_name}-qa",
        team=team_name,
        validates_for=[s["name"] for s in specialists],
        quality_criteria=f"{team_name}-quality-criteria.yaml"
    )

    # Register in team registry
    team_metadata = TeamMetadata(
        name=team_name,
        parent_team=parent_team,
        team_lead=team_lead_name,
        specialists=[s["name"] for s in specialists],
        qa_agent=qa_agent.name,
        focus=focus
    )

    team_registry.register_team(team_name, team_metadata)

    return team_metadata
```

---

## Cross-Functional Collaboration

### Collaboration Pattern

**Scenario:** CMO and CTO need to collaborate on website redesign

**Flow:**
1. User → Alex: "Redesign our website to improve conversions"
2. Alex identifies cross-functional initiative (marketing + engineering)
3. Alex creates collaboration workspace:
   ```json
   {
     "initiative": "website-redesign",
     "owners": ["cmo", "cto"],
     "workspace": "data/collaborations/website-redesign/",
     "shared_context": {
       "goal": "Improve conversion rate from 2% to 5%",
       "timeline": "Q4 2025",
       "budget": "$50K"
     }
   }
   ```
4. Alex delegates to CMO and CTO in parallel with shared context
5. CMO owns:
   - UX research (what users need)
   - Content strategy (messaging, copy)
   - Conversion optimization (CTAs, forms)
6. CTO owns:
   - Technical implementation (frontend, backend)
   - Performance optimization (page speed)
   - Analytics instrumentation (conversion tracking)
7. CMO and CTO coordinate via shared workspace:
   - CMO writes `requirements.md` → CTO reads for implementation
   - CTO writes `technical-constraints.md` → CMO reads for UX adjustments
8. Teams work in parallel with QA loops
9. Integration phase:
   - CMO's Content Team produces final copy
   - CTO's Engineering Team integrates copy into UI
   - Cross-functional QA validates end-to-end experience
10. Both executives report to Alex
11. Alex synthesizes and presents to user

### Collaboration Workspace Structure

```
data/collaborations/website-redesign/
├── initiative.json              # Goals, timeline, budget, owners
├── shared-context/
│   ├── requirements.md         # CMO's requirements
│   ├── technical-constraints.md # CTO's constraints
│   ├── design-system.md        # Shared design language
│   └── kpis.json               # Success metrics
├── cmo-deliverables/
│   ├── ux-research-report.md
│   ├── content-strategy.md
│   └── conversion-optimization-plan.md
├── cto-deliverables/
│   ├── technical-architecture.md
│   ├── implementation-plan.md
│   └── performance-benchmarks.json
└── integration/
    ├── launch-checklist.md
    └── qa-validation-report.md
```

---

## Agent Tier System

### Tier Definitions

| Tier | Role | Reports To | Manages | Creates | Model |
|------|------|-----------|---------|---------|-------|
| **CEO** | Alex (Chief of Staff) | User | Executives | Executives, strategies | Sonnet 4.5 |
| **C-Level** | CMO, CTO, CFO, CPO, COO | Alex | Teams | Team structures | Sonnet 4.5 |
| **Team Lead** | Content Lead, Engineering Lead | Executive | Specialists | Specialists, tasks | Sonnet 4.5 |
| **Specialist** | Blog Writer, Backend Engineer | Team Lead | Tasks | Outputs | Sonnet 4.5 or Haiku |
| **QA** | Content QA, Code Review QA | Team Lead | Quality | Validation reports | Sonnet 3.7 |

### Permission Matrix

| Tier | Read | Write | Edit | Bash | WebSearch | Task | Create Agents | Approve Work |
|------|------|-------|------|------|-----------|------|---------------|--------------|
| **CEO (Alex)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ Executives | ✅ Final |
| **C-Level** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ Teams | ✅ Dept |
| **Team Lead** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ Specialists | ✅ Team |
| **Specialist** | ✅ | ✅ | Varies | ❌ | Varies | ❌ | ❌ | ❌ |
| **QA** | ✅ | ✅ (reports) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Outputs |

---

## Updated System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                         (Rich CLI + Voice)                          │
└─────────────────────────────────────────────────────────────────────┘
                                ↓↑
┌─────────────────────────────────────────────────────────────────────┐
│                     CHIEF OF STAFF (Alex) - CEO                     │
│          Orchestrates C-level executives, high-level strategy       │
└─────────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│   CMO        │   CTO        │   CFO        │   CPO        │ Jordan  │
│ (Marketing)  │ (Technology) │ (Finance)    │ (People)     │ (Strat) │
│              │              │              │              │ Quinn   │
│              │              │              │              │ (Plan)  │
│              │              │              │              │ Sam     │
│              │              │              │              │ (Analy) │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘
       ↓↑              ↓↑             ↓↑             ↓↑
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Content Team │ Engineering  │ Accounting   │ Recruiting   │
│ Lead         │ Team Lead    │ Team Lead    │ Team Lead    │
└──────────────┴──────────────┴──────────────┴──────────────┘
       ↓↑              ↓↑             ↓↑             ↓↑
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Specialists: │ Specialists: │ Specialists: │ Specialists: │
│ - Blog Write │ - Backend    │ - Bookkeeper │ - Tech Rec   │
│ - Social Wrt │ - Frontend   │ - Tax Spec   │ - Sales Rec  │
│ - Email Copy │ - DevOps     │ - Audit Spec │ - Exec Rec   │
│              │              │              │              │
│ QA Agent:    │ QA Agent:    │ QA Agent:    │ QA Agent:    │
│ - Content QA │ - Code Revw  │ - Acct QA    │ - Recruit QA │
└──────────────┴──────────────┴──────────────┴──────────────┘
                                ↓↑
┌─────────────────────────────────────────────────────────────────────┐
│                    QUALITY CONTROL LOOPS                            │
│     Specialist → QA → [Pass/Fail] → Revision → QA → Approved       │
└─────────────────────────────────────────────────────────────────────┘
                                ↓↑
┌─────────────────────────────────────────────────────────────────────┐
│                CROSS-FUNCTIONAL COLLABORATION LAYER                 │
│       CMO ↔ CTO workspace, CTO ↔ CFO workspace, etc.              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Changes Required

### 1. Agent Registry Schema Update

Add fields to `data/agents/registry.json`:
```json
{
  "agent_tier": "ceo | c-level | team-lead | specialist | qa",
  "reports_to": "alex | cmo | content-lead | ...",
  "manages": ["team1", "team2"] || ["specialist1", "specialist2"],
  "qa_validated_by": "content-qa | code-review-qa | ...",
  "quality_criteria": "path/to/criteria.yaml"
}
```

### 2. New Component: Team Registry

**File:** `src/team_registry.py`

```python
class TeamRegistryManager:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.lock = threading.Lock()
        self.registry = self._load()

    def register_team(self, team_name: str, metadata: TeamMetadata):
        """Add team to registry."""

    def get_team(self, team_name: str) -> Optional[TeamMetadata]:
        """Retrieve team metadata."""

    def list_teams(self, parent_team: Optional[str] = None) -> List[str]:
        """List teams, optionally filtered by parent."""

    def get_team_hierarchy(self, root_team: str) -> dict:
        """Get full hierarchy from root team down."""
```

### 3. New Component: QA Engine

**File:** `src/qa_engine.py`

```python
class QAEngine:
    def __init__(self, criteria_dir: Path):
        self.criteria_dir = criteria_dir

    async def validate_output(
        self,
        output_path: Path,
        criteria_file: str,
        specialist_agent: str
    ) -> QAValidationResult:
        """
        Validate output against quality criteria.

        Returns:
            QAValidationResult with status, score, feedback
        """

    async def run_qa_loop(
        self,
        specialist_agent: str,
        qa_agent: str,
        output_path: Path,
        criteria_file: str,
        max_iterations: int = 5
    ) -> QAValidationResult:
        """
        Run full QA loop with revision cycles.

        Returns final approved output or escalates if max iterations reached.
        """
```

### 4. Updated Workflow Engine

Add QA loop support to workflow execution:

```python
class WorkflowEngine:
    async def execute_workflow_with_qa(
        self,
        workflow_name: str,
        agent_client: ClaudeSDKClient,
        qa_agent: str,
        quality_criteria: str,
        context: dict
    ) -> dict:
        """Execute workflow with QA validation loop."""

        # Execute workflow
        results = await self.execute_workflow(workflow_name, agent_client, context)

        # Trigger QA validation
        qa_result = await qa_engine.run_qa_loop(
            specialist_agent=agent_client.agent_name,
            qa_agent=qa_agent,
            output_path=results["output_file"],
            criteria_file=quality_criteria
        )

        results["qa_validation"] = qa_result

        return results
```

### 5. Updated Agent Definitions

Add executive manager, team lead, and QA agent definition templates:

```python
# src/agent_definitions.py

def create_executive_manager_definition(role: str, department: str, teams: List[str]) -> AgentDefinition:
    """Create C-level executive manager agent definition."""

def create_team_lead_definition(team: str, executive: str, specialists: List[str]) -> AgentDefinition:
    """Create team lead agent definition."""

def create_specialist_definition(specialty: str, team: str, team_lead: str) -> AgentDefinition:
    """Create specialist agent definition."""

def create_qa_agent_definition(team: str, validates_for: List[str], criteria: str) -> AgentDefinition:
    """Create QA agent definition."""
```

---

## Updated Epic Breakdown

### New EPIC-8: Hierarchical Team System

**Priority:** P1 (Should Have - Scalability Critical)
**Story Points:** 34
**Sprint Allocation:** Sprints 21-24
**Status:** Planned

**Epic Goal:**
Implement hierarchical team structure with executive managers, team leads, specialists, and QA loops to enable scalable, quality-controlled agent organization.

**Capabilities Delivered:**
- C-level executive agent creation (CMO, CTO, CFO, CPO, COO)
- Team lead agent creation
- QA agent creation with validation criteria
- Quality control loops with revision cycles
- Team registry system
- Cross-functional collaboration workspaces
- Hierarchical delegation patterns

**Success Criteria:**
- [ ] User can create entire departments (e.g., "Create marketing department")
- [ ] Executive managers successfully delegate to team leads
- [ ] Team leads coordinate specialists and trigger QA loops
- [ ] QA agents validate outputs and trigger revisions
- [ ] Quality loops iterate until standards met (max 5 iterations)
- [ ] Cross-functional initiatives coordinate multiple executives
- [ ] Team hierarchy visualizations in Rich UI

**Stories (~7):**
- **STORY-8.1:** Implement team registry system (5 points)
- **STORY-8.2:** Create executive manager agent type (5 points)
- **STORY-8.3:** Create team lead agent type (5 points)
- **STORY-8.4:** Create QA agent type with validation logic (8 points)
- **STORY-8.5:** Implement quality control loop workflow (8 points)
- **STORY-8.6:** Add cross-functional collaboration workspaces (5 points)
- **STORY-8.7:** Create team hierarchy visualization in Rich UI (3 points)

---

## Conclusion

This hierarchical team architecture transforms Mission Control from a flat structure (5 specialists) into a **scalable, quality-controlled organization** capable of:

✅ **Depth:** Nested teams (CMO → Content Lead → Blog Writer → Content QA)
✅ **Quality:** Every output validated by QA before delivery
✅ **Scalability:** Add entire departments on-demand
✅ **Collaboration:** Cross-functional initiatives coordinate multiple teams
✅ **Realism:** Mirrors how real companies organize

**Key Benefits:**
1. **Specialization:** Deep domain expertise (not generic "researcher" but "Technical SEO Specialist")
2. **Quality Assurance:** No output delivered without QA approval
3. **Coordination:** Executive managers orchestrate complex initiatives
4. **Iteration:** Revision loops ensure excellence
5. **Growth:** System scales from 5 agents to 500+ without chaos

**Implementation Priority:**
- Phase 1-2: Build flat structure (5 core specialists)
- Phase 3: Add dynamic agent creation
- **Phase 4: Implement hierarchical teams (EPIC-8)**

This aligns with your vision of a system that can create **very specialized teams, expertly prompted, with quality control mechanisms** ensuring outputs meet standards.

---

**Next Steps:**
1. Review and approve this architectural enhancement
2. Update solution-architecture.md with hierarchical references
3. Add EPIC-8 to epics.md
4. Proceed with Phase 1 implementation (flat structure first)
5. Implement hierarchical capabilities in Phase 4

🚀 **Ready to build a truly scalable executive team!**
