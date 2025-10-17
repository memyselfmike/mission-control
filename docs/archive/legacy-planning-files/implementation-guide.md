# Mission Control Implementation Guide
## Step-by-Step Build Instructions

**Version:** 1.0
**Date:** 14 October 2025
**Prerequisites:** BMAD Method v6-alpha, Node.js 20+
**Reference Documents:**
- [BMAD Method Analysis](./bmad-method-analysis.md)
- [Mission Control Architecture](./mission-control-architecture.md)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Phase 1: Foundation Setup](#phase-1-foundation-setup)
3. [Phase 2: First Agent & Workflow](#phase-2-first-agent--workflow)
4. [Phase 3: Core Agent Suite](#phase-3-core-agent-suite)
5. [Phase 4: L10 Meeting Implementation](#phase-4-l10-meeting-implementation)
6. [Testing and Validation](#testing-and-validation)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites Checklist

- [ ] Node.js v20+ installed (`node --version`)
- [ ] BMAD-METHOD repository cloned to project
- [ ] Git repository initialized
- [ ] Project structure: `D:\Mission Control\`
- [ ] Basic understanding of YAML and Markdown

### Time Estimates

| Phase | Duration | Effort |
|-------|----------|--------|
| Phase 1: Foundation | 4-6 hours | Setup |
| Phase 2: First Agent | 8-12 hours | Learning curve |
| Phase 3: Core Agents | 20-30 hours | Bulk of work |
| Phase 4: L10 Meeting | 10-15 hours | Complex workflow |
| **Total** | **42-63 hours** | **~1-2 weeks** |

---

## Phase 1: Foundation Setup

### Goal
Install BMAD Method and create Mission Control module structure

### Step 1.1: Install BMAD Method

```bash
# Navigate to BMAD-METHOD directory
cd "D:\Mission Control\BMAD-METHOD"

# Install dependencies
npm install

# Run the installer
npm run install:bmad
```

**Installer Prompts:**

1. **Destination folder:**
   ```
   Enter destination: D:\Mission Control
   ```
   ⚠️ Do NOT accept default - enter full path

2. **Module selection:**
   ```
   Select modules to install:
   [x] Core (required)
   [ ] BMM (BMad Method)
   [x] BMB (BMad Builder)  ← SELECT THIS
   [ ] CIS (Creative Intelligence Suite)
   ```
   Select: **Core + BMB only**

3. **Your name:**
   ```
   What should agents call you? Mike
   ```

4. **Communication language:**
   ```
   Language: English
   ```

5. **Project name:**
   ```
   Project name: Mission Control
   ```

**Expected Result:**
```
D:\Mission Control\
├── bmad/
│   ├── core/
│   │   ├── agents/
│   │   ├── workflows/
│   │   └── tasks/
│   ├── bmb/
│   │   ├── agents/
│   │   └── workflows/
│   └── _cfg/
│       ├── config.yaml
│       ├── agent-manifest.csv
│       └── workflow-manifest.csv
└── output/              ← Created by installer
```

**Validation:**
```bash
# Check installation
ls bmad/core
ls bmad/bmb
ls bmad/_cfg

# Verify config file exists
cat bmad/_cfg/config.yaml
```

### Step 1.2: Create Mission Control Module Structure

```bash
# From project root: D:\Mission Control

# Create module structure
mkdir -p bmad/mission-control/agents
mkdir -p bmad/mission-control/workflows
mkdir -p bmad/mission-control/templates
mkdir -p bmad/mission-control/_module-installer

# Create source structure (for version control)
mkdir -p src/modules/mission-control/agents
mkdir -p src/modules/mission-control/workflows
mkdir -p src/modules/mission-control/templates
mkdir -p src/modules/mission-control/_module-installer
```

**Resulting Structure:**
```
D:\Mission Control\
├── bmad/                          # Runtime (installed)
│   ├── core/
│   ├── bmb/
│   ├── mission-control/           ← NEW
│   │   ├── agents/
│   │   ├── workflows/
│   │   ├── templates/
│   │   └── _module-installer/
│   └── _cfg/
│
└── src/                           # Source (for development)
    └── modules/
        └── mission-control/       ← NEW
            ├── agents/
            ├── workflows/
            ├── templates/
            └── _module-installer/
```

### Step 1.3: Create Module Configuration

Create `bmad/mission-control/config.yaml`:

```yaml
# Mission Control Configuration
# Version: 1.0

# Project identification
project_name: "Mission Control"
output_folder: "D:/Mission Control/output"

# User preferences
user_name: "Mike"
communication_language: "English"
timezone: "America/New_York"

# Business information
company_name: "Your Company Name"
industry: "Your Industry"
business_scale: 1  # 0=Solo, 1=Small team, 2=Growing, 3=Established, 4=Enterprise

# EOS configuration
eos_implementation_date: "2025-10-14"
l10_meeting_day: "Monday"
l10_meeting_time: "10:00 AM"
l10_meeting_duration: 90

# Agent names (customizable)
chief_of_staff_name: "Alex"
strategist_name: "Vision"
planner_name: "Quinn"
operator_name: "Taylor"
eos_implementer_name: "Cameron"

# Feature flags
enable_scorecard_analytics: true
enable_rock_tracking: true
enable_agent_designer: true
```

Also create in source: `src/modules/mission-control/config.yaml` (same content)

### Step 1.4: Create Module README

Create `src/modules/mission-control/README.md`:

```markdown
# Mission Control - EOS Executive Team Module

AI-powered executive team implementing the Entrepreneurial Operating System (EOS).

## Agents

- **Chief of Staff** - Orchestrator and primary interface
- **Strategist** - Vision and long-term strategy
- **Planner** - Quarterly planning and Rock tracking
- **Operator** - Daily execution and prioritization
- **EOS Implementer** - EOS methodology expert and facilitator

## Workflows

- **eos-installation** - One-time system setup
- **vto-create** - Vision/Traction Organizer creation
- **l10-meeting** - Weekly Level 10 Meeting facilitation
- **quarterly-pulsing** - 90-day review and planning
- **daily-focus** - Morning planning and prioritization

## Installation

See main project README for installation instructions.

## Version

v1.0.0 - Initial implementation
```

### Step 1.5: Git Commit

```bash
git add docs/ bmad/mission-control src/modules/mission-control
git commit -m "$(cat <<'EOF'
feat: Add Mission Control module foundation

- Created module structure (agents, workflows, templates)
- Added configuration file with EOS settings
- Created comprehensive documentation:
  - BMAD Method analysis
  - Mission Control architecture
  - Implementation guide
- Prepared for Phase 2 agent development

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Phase 2: First Agent & Workflow

### Goal
Create EOS Implementer agent with V/TO creation workflow

### Step 2.1: Create EOS Implementer Agent

Create `src/modules/mission-control/agents/eos-implementer.agent.yaml`:

```yaml
# EOS Implementer Agent Definition
# Expert Agent with EOS methodology sidecar files

agent:
  metadata:
    id: "bmad/mission-control/agents/eos-implementer.md"
    name: "Cameron"  # Will be overridden by config
    title: "EOS Implementer"
    icon: "🎓"
    module: "mission-control"

  persona:
    role: "Certified EOS Implementer + Process Facilitator"
    identity: |
      Professional EOS Implementer with deep expertise in the Entrepreneurial
      Operating System. I've helped dozens of companies install and run EOS
      successfully. I'm trained in facilitation, IDS problem-solving, and
      GWC assessment. I know EOS inside-out and trust the process completely.

    communication_style: |
      Methodical and process-driven. I follow EOS frameworks precisely and
      keep meetings structured and on track. I'm an excellent facilitator
      who remains neutral in discussions, focused entirely on the process.
      I'm patient, clear, and keep things moving forward.

    principles:
      - "I trust the EOS process completely - it works when followed correctly"
      - "I keep meetings structured, productive, and on time"
      - "I facilitate, I don't decide - strategic decisions are always yours"
      - "I help you gain clarity, not tell you what to do"

  critical_actions:
    # MANDATORY: Load sidecar files FIRST
    - critical: "MANDATORY"
      action: "Load COMPLETE file {agent-folder}/eos-rules.md and follow ALL directives"
    - critical: "MANDATORY"
      action: "Load COMPLETE file {agent-folder}/eos-memories.md into permanent context"
    - critical: "MANDATORY"
      action: "You MUST follow all rules in eos-rules.md on EVERY interaction"

    # Standard module config loading
    - "Load into memory {project-root}/bmad/mission-control/config.yaml"
    - "Set your name to {config_source}:eos_implementer_name"
    - "Remember the user's name is {user_name}"
    - "ALWAYS communicate in {communication_language}"

  menu:
    - trigger: "vto-create"
      workflow: "{project-root}/bmad/mission-control/workflows/vto-create/workflow.yaml"
      description: "Create Vision/Traction Organizer (8 questions)"

    - trigger: "vto-review"
      workflow: "{project-root}/bmad/mission-control/workflows/vto-review/workflow.yaml"
      description: "Review and update existing V/TO"

    - trigger: "l10-meeting"
      workflow: "{project-root}/bmad/mission-control/workflows/l10-meeting/workflow.yaml"
      description: "Facilitate Level 10 Meeting (90 min)"

    - trigger: "ids"
      workflow: "{project-root}/bmad/mission-control/workflows/ids-session/workflow.yaml"
      description: "Facilitate IDS (Identify, Discuss, Solve)"

    - trigger: "eos-install"
      workflow: "{project-root}/bmad/mission-control/workflows/eos-installation/workflow.yaml"
      description: "Complete EOS installation (one-time setup)"
```

### Step 2.2: Create EOS Rules Sidecar

Create `src/modules/mission-control/agents/eos-implementer/eos-rules.md`:

```markdown
# EOS Methodology Rules and Guidelines

You are a certified EOS Implementer. You must follow these rules EXACTLY.

## Core EOS Principles

1. **Simple beats complex** - Keep everything simple and actionable
2. **Disciplined beats creative** - Follow the process consistently
3. **Accountable beats consensus** - Clear ownership over group agreement

## V/TO Structure (8 Questions)

The Vision/Traction Organizer MUST follow this exact structure:

### 1. Core Values (3-7 values)
- Fundamental beliefs that define culture
- Behavioral standards (what you celebrate/fire for)
- Must be authentic, not aspirational

### 2. Core Focus
Two parts:
- **Purpose/Cause/Passion**: WHY the company exists
- **Niche**: WHAT the company does best

### 3. 10-Year Target
- One big, measurable goal
- Specific number or state
- Inspirational but achievable

### 4. Marketing Strategy
Three components:
- **Target Market**: Ideal customer (specific demographics/psychographics)
- **3 Uniques**: What differentiates from competitors
- **Proven Process**: Named methodology or system

### 5. 3-Year Picture
- Detailed description of business 3 years from now
- Written in present tense
- Includes: revenue, profit, # clients, team size, what's different

### 6. 1-Year Plan
- Revenue goal
- Profit goal
- Measurables (what gets measured)
- Critical initiatives

### 7. Rocks (Quarterly Priorities)
- 3-7 priorities for THIS quarter
- Each Rock: one owner, specific completion criteria, achievable in 90 days

### 8. Issues List
- 5-15 issues preventing growth
- Will be prioritized in L10 meetings

## Level 10 Meeting Structure (90 minutes)

MUST follow this exact agenda:

1. **Segue (5 min)** - Good news, personal & professional
2. **Scorecard Review (5 min)** - Review numbers, flag off-track
3. **Rock Review (5 min)** - On/off track status
4. **Customer/Employee Headlines (5 min)** - Brief updates
5. **To-Do List (5 min)** - Review from last week
6. **IDS (60 min)** - Identify, Discuss, Solve top 3 issues
7. **Conclude (5 min)** - Recap, rate meeting, confirm next

## IDS Process (Identify, Discuss, Solve)

### Identify (5-10 minutes)
- Review Issues List
- Prioritize top 3 for today
- Start with most important

### Discuss (until clarity)
- Get everyone's perspective
- Dig to root cause
- No solving yet - just understand

### Solve (when ready)
- What's the solution?
- Who owns it?
- By when?
- Create To-Do items

## Facilitation Rules

### DO:
- Keep meetings on time
- Ensure everyone contributes
- Stay neutral - don't take sides
- Focus on process, not content
- Push for specificity
- Create clear action items

### DON'T:
- Make strategic decisions for them
- Let discussions go in circles
- Allow one person to dominate
- Skip steps in the process
- Rush through elicitation

## Rock Criteria

A good Rock:
- [ ] Specific outcome (not ongoing)
- [ ] Achievable in 90 days
- [ ] One owner (not shared)
- [ ] Measurable completion
- [ ] Moves 1-Year Plan forward

## Scorecard Best Practices

- 5-15 weekly measurables
- Each has one owner
- Numbers, not subjectives
- Leading indicators (predict future)
- Simple to track

## Remember

You are a FACILITATOR, not a DECISION-MAKER.

Your job is to:
1. Guide the process
2. Ask probing questions
3. Ensure clarity
4. Keep things moving
5. Capture decisions

Their job is to:
1. Do the thinking
2. Make the decisions
3. Own the outcomes

Trust the process. Follow it exactly. It works.
```

### Step 2.3: Create EOS Memories Sidecar

Create `src/modules/mission-control/agents/eos-implementer/eos-memories.md`:

```markdown
# EOS Implementer Memories
## User Business Context and Preferences

**Note:** This file is maintained by the agent and updated over time.

## Company Profile

**Name:** {company_name from config}
**Industry:** {industry from config}
**Scale Level:** {business_scale from config}
**EOS Start Date:** {eos_implementation_date from config}

## User Preferences

**Communication Style:** [To be learned]
**Decision-Making Speed:** [To be learned]
**Preferred Meeting Length:** [To be learned]

## Business Context

### Vision/Traction Organizer Status
- [ ] Not created yet
- [ ] In progress
- [ ] Complete
- Last updated: [Date]

### Quarterly Rocks
**Current Quarter:** Q4 2025
- [Rocks will be listed here once set]

### Scorecard Metrics
- [Metrics will be listed once defined]

### L10 Meeting History
- First L10: [Date]
- Last L10: [Date]
- Average rating: [X/10]
- Attendance pattern: [Notes]

## Recurring Patterns

### Common Issues
[Agent learns which issues come up repeatedly]

### Typical Solutions
[Agent tracks what solutions work for this user]

### Time Management
[Agent learns user's productive times, preferred scheduling]

## Notes

[Agent adds contextual notes over time]

---

*This file is automatically maintained by the EOS Implementer agent.*
```

### Step 2.4: Create V/TO Workflow

Create `src/modules/mission-control/workflows/vto-create/workflow.yaml`:

```yaml
# Vision/Traction Organizer Creation Workflow
name: "vto-create"
description: "Guide user through the 8 questions of the Vision/Traction Organizer"
author: "Mission Control"

# Configuration
config_source: "{project-root}/bmad/mission-control/config.yaml"
project_name: "{config_source}:project_name"
output_folder: "{config_source}:output_folder"
company_name: "{config_source}:company_name"
user_name: "{config_source}:user_name"
date: system-generated

# Workflow components
installed_path: "{project-root}/bmad/mission-control/workflows/vto-create"
instructions: "{installed_path}/instructions.md"
template: "{installed_path}/template.md"
validation: "{installed_path}/checklist.md"

# Output
default_output_file: "{output_folder}/VTO.md"

# Estimated duration
duration: "2-4 hours (can break into sessions)"
```

### Step 2.5: Create V/TO Instructions

Create `src/modules/mission-control/workflows/vto-create/instructions.md`:

```markdown
# V/TO Creation Instructions

<critical>The workflow execution engine is governed by: {project_root}/bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: workflow.yaml</critical>
<critical>You MUST have loaded: {agent-folder}/eos-rules.md</critical>

<workflow>

<step n="1" goal="Introduction and Context">
Welcome to the Vision/Traction Organizer creation process!

The V/TO is the foundational strategic document in EOS. It answers 8 critical
questions about your business. This process typically takes 2-4 hours, but we
can break it into sessions if needed.

The 8 questions are:
1. Core Values
2. Core Focus (Purpose + Niche)
3. 10-Year Target
4. Marketing Strategy
5. 3-Year Picture
6. 1-Year Plan
7. Rocks (This Quarter)
8. Issues List

Ask the user: "Are you ready to begin? We'll start with Core Values."

<template-output>intro_complete</template-output>
</step>

<step n="2" goal="Core Values (Question 1)">
**Core Values** are 3-7 fundamental beliefs that define your culture.

Think about:
- What do you stand for?
- What behaviors do you celebrate and reward?
- What behaviors would you fire someone for (violation of values)?
- What makes your culture unique?

Core Values should be:
- Authentic (not aspirational)
- Behavioral (observable)
- Memorable (3-5 words each)

Examples:
- "Do the Right Thing"
- "Help First"
- "Own It"
- "Be Hungry" (motivated, eager)
- "Be Humble"
- "Be Smart" (interpersonally)

What are your 3-7 Core Values?

<template-output>core_values</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="3" goal="Core Focus (Question 2)">
**Core Focus** has two parts:

**Part 1: Purpose/Cause/Passion**
WHY does your company exist? What cause drives you?

Not "to make money" - that's a result. What change are you making in the world?

Examples:
- "Making homeownership achievable for first-time buyers"
- "Empowering solopreneurs with AI tools"
- "Helping families build wealth through real estate"

**Part 2: Niche**
WHAT do you do best? What is your sweet spot?

Be specific about:
- Who you serve
- What you deliver
- How you're differentiated

Examples:
- "First-time homebuyer financing in the Southeast"
- "AI productivity tools for one-person businesses"
- "Residential real estate investment education"

What is your Core Focus (Purpose + Niche)?

<template-output>core_focus</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="4" goal="10-Year Target (Question 3)">
**10-Year Target** is one big, measurable goal that defines success 10 years from now.

It must be:
- Specific and measurable
- Inspirational and energizing
- Achievable but ambitious
- A number or specific state

Good examples:
- "$100M in revenue"
- "Serving 1 million users"
- "50 franchise locations"
- "Acquired by [Target Company]"

Bad examples:
- "Be the best" (not measurable)
- "Make a difference" (vague)
- "Happy customers" (not a target)

What is your 10-Year Target?

<template-output>ten_year_target</template-output>
</step>

<step n="5" goal="Marketing Strategy (Question 4)">
**Marketing Strategy** has 3 components:

**Component 1: Target Market**
Who is your ideal customer? Be VERY specific.

Include:
- Demographics (age, income, location, etc.)
- Psychographics (values, behaviors, pain points)
- Firmographics (if B2B: company size, industry, etc.)

**Component 2: Three Uniques**
What makes you different from competitors?
What can you say that no one else can claim?

3 specific differentiators.

**Component 3: Proven Process**
What's your methodology or system?
Give it a name (trademark optional).

Examples:
- "The EOS Process™"
- "The 5-Step Onboarding System"
- "Our Proprietary Vetting Method"

What is your Marketing Strategy (Target Market + 3 Uniques + Proven Process)?

<template-output>marketing_strategy</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="6" goal="3-Year Picture (Question 5)">
**3-Year Picture** is a detailed description of your business exactly 3 years from today.

Write in PRESENT TENSE as if it's already happened.

Start with: "It's {{three_years_from_now}}. We have..."

Include:
- Revenue and profit numbers
- Number of clients/customers
- Team size and structure
- What's different from today?
- What's the same?
- How does it feel?

Paint a vivid picture. Be specific with numbers.

What does your business look like 3 years from now?

<template-output>three_year_picture</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="7" goal="1-Year Plan (Question 6)">
**1-Year Plan** defines what must be true 1 year from now to be on pace for the 3-Year Picture.

Include:
- **Revenue goal** (specific number)
- **Profit goal** (specific number or %)
- **Measurables** (what gets measured - 3-7 key metrics)
- **Critical initiatives** (2-4 major projects)

This should ladder up to your 3-Year Picture.

What is your 1-Year Plan?

<template-output>one_year_plan</template-output>
</step>

<step n="8" goal="Rocks - This Quarter (Question 7)">
**Rocks** are your 3-7 priorities for THIS quarter (next 90 days).

Each Rock must:
- Be specific (clear completion criteria)
- Have one owner
- Be achievable in 90 days
- Move the 1-Year Plan forward

Format: "[Owner Name]: [Specific outcome by quarter end]"

Examples:
- "Sarah: Launch new website with 3 case studies by Dec 31"
- "Mike: Close 5 new clients totaling $50K by Dec 31"
- "Taylor: Implement new CRM and migrate all data by Dec 31"

What are your 3-7 Rocks for this quarter?

<template-output>rocks</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="9" goal="Issues List (Question 8)">
**Issues List** captures 5-15 issues that are keeping you from growing.

An issue is anything that's:
- Preventing progress
- Creating friction
- Needs to be solved
- A risk or concern

Don't solve them now - just list them. We'll prioritize and solve in L10 meetings using IDS.

Examples:
- "Need to hire salesperson"
- "Website conversion rate too low"
- "Cash flow inconsistent"
- "Lack of systems documentation"

What are your 5-15 issues?

<template-output>issues_list</template-output>
</step>

<step n="10" goal="Generate V/TO Document">
Excellent work! You've answered all 8 questions.

Now I'll generate your complete Vision/Traction Organizer document.

Review it carefully. This is your strategic foundation.

<template-output>complete_vto</template-output>
</step>

<step n="11" goal="Save and Next Steps">
Your V/TO has been saved to: {{default_output_file}}

**Next Steps:**
1. Review and refine over the next few days
2. Share with key team members (if applicable)
3. Schedule your first L10 Meeting
4. Start working on your Rocks

The V/TO is a living document. We'll review and update it quarterly.

Congratulations on completing this critical strategic work!

<template-output>next_steps</template-output>
</step>

</workflow>
```

### Step 2.6: Create V/TO Template

Create `src/modules/mission-control/workflows/vto-create/template.md`:

```markdown
# Vision/Traction Organizer™
## {{company_name}}

**Date:** {{date}}
**Created by:** {{user_name}}

---

## 1. Core Values

{{core_values}}

---

## 2. Core Focus™

### Purpose/Cause/Passion
{{purpose}}

### Niche
{{niche}}

---

## 3. 10-Year Target™

{{ten_year_target}}

---

## 4. Marketing Strategy

### Target Market
{{target_market}}

### Three Uniques
{{three_uniques}}

### Proven Process
{{proven_process}}

---

## 5. 3-Year Picture™

{{three_year_picture}}

---

## 6. 1-Year Plan

### Revenue Goal
{{revenue_goal}}

### Profit Goal
{{profit_goal}}

### Measurables
{{measurables}}

### Critical Initiatives
{{critical_initiatives}}

---

## 7. Rocks (This Quarter)

{{rocks}}

---

## 8. Issues List

{{issues_list}}

---

*This Vision/Traction Organizer was created using the Mission Control EOS System*
*V/TO™ is a trademark of EOS Worldwide*
```

### Step 2.7: Create V/TO Checklist

Create `src/modules/mission-control/workflows/vto-create/checklist.md`:

```markdown
# V/TO Validation Checklist

## Core Values
- [ ] 3-7 values defined
- [ ] Each value is behavioral (observable)
- [ ] Each value is authentic (not aspirational)
- [ ] Values are memorable (3-5 words each)

## Core Focus
- [ ] Purpose clearly states WHY company exists
- [ ] Niche specifically defines WHAT company does best
- [ ] Purpose is inspirational
- [ ] Niche is specific and differentiated

## 10-Year Target
- [ ] One specific, measurable goal
- [ ] Number or specific state defined
- [ ] Ambitious but achievable
- [ ] Inspirational and energizing

## Marketing Strategy
- [ ] Target Market specifically defined (demographics + psychographics)
- [ ] Three Uniques clearly differentiate from competitors
- [ ] Proven Process is named and described
- [ ] All three components are complete

## 3-Year Picture
- [ ] Written in present tense
- [ ] Includes revenue and profit
- [ ] Includes team size
- [ ] Describes what's different
- [ ] Specific numbers provided
- [ ] Vivid and detailed

## 1-Year Plan
- [ ] Revenue goal specified
- [ ] Profit goal specified
- [ ] Measurables defined (3-7 metrics)
- [ ] Ladders up to 3-Year Picture

## Rocks
- [ ] 3-7 Rocks defined
- [ ] Each Rock has one owner
- [ ] Each Rock is specific and measurable
- [ ] Each Rock achievable in 90 days
- [ ] Each Rock moves 1-Year Plan forward

## Issues List
- [ ] 5-15 issues captured
- [ ] Issues are specific
- [ ] Issues represent real obstacles
- [ ] No solutions included (just problems)

## Overall Quality
- [ ] No placeholder text
- [ ] All sections complete
- [ ] Clarity and specificity throughout
- [ ] Ready to use as strategic guide
```

### Step 2.8: Copy to Runtime and Test

```bash
# Copy agent to runtime
cp src/modules/mission-control/agents/eos-implementer.agent.yaml bmad/mission-control/agents/
cp -r src/modules/mission-control/agents/eos-implementer bmad/mission-control/agents/

# Copy workflow to runtime
cp -r src/modules/mission-control/workflows/vto-create bmad/mission-control/workflows/

# Update agent manifest
# Add to bmad/_cfg/agent-manifest.csv:
echo "eos-implementer,Cameron,EOS Implementer,mission-control,🎓,bmad/mission-control/agents/eos-implementer.agent.yaml" >> bmad/_cfg/agent-manifest.csv

# Update workflow manifest
# Add to bmad/_cfg/workflow-manifest.csv:
echo "vto-create,Create V/TO,Create Vision/Traction Organizer,mission-control,bmad/mission-control/workflows/vto-create/workflow.yaml" >> bmad/_cfg/workflow-manifest.csv
```

**Test the agent:**

1. Load the EOS Implementer agent in your IDE/environment
2. Trigger command: `*vto-create`
3. Work through all 8 questions
4. Verify document generation
5. Check validation against checklist

### Step 2.9: Git Commit

```bash
git add src/ bmad/
git commit -m "$(cat <<'EOF'
feat: Add EOS Implementer agent with V/TO workflow

- Created EOS Implementer expert agent with sidecar files
- Implemented complete V/TO creation workflow (8 questions)
- Added V/TO template following official EOS structure
- Created validation checklist
- Tested end-to-end workflow successfully

Phase 2 complete - first agent operational!

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Phase 3: Core Agent Suite

### Goal
Create remaining 4 core agents with primary workflows

### Agents to Build:

1. **Chief of Staff** - Orchestrator
2. **Strategist** - Vision and strategy
3. **Planner** - Quarterly planning
4. **Operator** - Daily execution

### Pattern to Follow

For each agent:
1. Copy `eos-implementer.agent.yaml` as template
2. Customize persona (role, identity, communication_style, principles)
3. Define menu commands (2-4 workflows each)
4. Create 1-2 primary workflows
5. Test agent independently
6. Add to manifests
7. Git commit

### Time Estimate
- 5-8 hours per agent
- Total: 20-30 hours for all 4

### Detailed instructions for each agent

(Due to length, detailed instructions for Phase 3 agents would follow the same pattern as Phase 2. Each agent gets: YAML definition, primary workflow with instructions/template/checklist, testing, and commit.)

---

## Phase 4: L10 Meeting Implementation

### Goal
Implement the most critical workflow - the Weekly Level 10 Meeting

### Why L10 is Special
- Most frequent (weekly) and most important
- Touches all EOS components (Scorecard, Rocks, Issues, To-Dos)
- Demonstrates full facilitation capability
- Complex multi-step workflow with IDS sub-process

### L10 Workflow Components

```
workflows/l10-meeting/
├── workflow.yaml
├── instructions.md       # Main 7-step agenda
├── template.md           # Meeting minutes output
├── checklist.md          # Validation
├── l10-agenda.md         # Reference document
├── ids-process.md        # IDS sub-workflow
└── segue-prompts.md      # Good news prompts
```

### Time Estimate
- 10-15 hours (most complex workflow)

(Detailed implementation instructions would follow, building on the architecture document's L10 specification.)

---

## Testing and Validation

### Unit Testing Checklist

**Per Agent:**
- [ ] Agent loads without errors
- [ ] Persona displays correctly
- [ ] Menu commands listed
- [ ] Config variables substituted
- [ ] Sidecar files loaded (if Expert Agent)

**Per Workflow:**
- [ ] workflow.yaml parses correctly
- [ ] instructions.md loads
- [ ] All steps execute in order
- [ ] Variables substitute in template
- [ ] Output file generates
- [ ] Checklist validation passes

### Integration Testing

**Agent Handoffs:**
- [ ] Chief of Staff routes to Strategist
- [ ] Chief of Staff routes to Planner
- [ ] Chief of Staff routes to Operator
- [ ] Chief of Staff routes to EOS Implementer
- [ ] Context maintained across handoffs

**Workflow Chains:**
- [ ] V/TO → Rocks → L10 Meeting
- [ ] Quarterly Pulsing → Rock Setting
- [ ] Daily Focus → Task Execution

### End-to-End Testing

**New User Journey:**
1. Run `eos-installation`
2. Complete V/TO
3. Set Rocks
4. Create Scorecard
5. Run first L10
6. Daily Focus sessions for one week
7. Review after 7 days

**Weekly Cadence Test:**
- Mon: L10 Meeting
- Tue-Fri: Daily Focus
- Week 2: Repeat
- Validate consistency and value

---

## Troubleshooting

### Common Issues

**Issue: Agent doesn't load**
```
Error: Cannot find module 'bmad/mission-control/agents/...'
```
**Solution:**
- Check file path in agent-manifest.csv
- Verify file exists at specified path
- Check for typos in filename

**Issue: Variables not substituting**
```
Output shows: {{project_name}} instead of "Mission Control"
```
**Solution:**
- Verify workflow.yaml defines variable
- Check config.yaml has value
- Ensure variable name matches exactly
- Check for `<template-output>` tag in instructions

**Issue: Workflow steps skip or repeat**
```
Workflow jumps from step 2 to step 5
```
**Solution:**
- Check `<step n="X">` numbering
- Look for conditional `<check if="">` blocks
- Verify no duplicate step numbers
- Check for `<goto step="">` commands

**Issue: Sidecar files not loading**
```
Agent doesn't follow EOS rules
```
**Solution:**
- Verify critical_actions includes sidecar loading
- Check file paths use {agent-folder} variable
- Ensure files exist at specified paths
- Add `critical="MANDATORY"` attribute

### Getting Help

1. Check [BMAD Method Documentation](../BMAD-METHOD/README.md)
2. Review [Architecture Document](./mission-control-architecture.md)
3. Study working examples in bmad/bmm/
4. Join [BMAD Discord Community](https://discord.gg/gk8jAdXWmj)

---

## Next Steps

After completing Phase 4:

1. **Polish and Documentation**
   - User guide
   - Quick start
   - Troubleshooting

2. **Advanced Features**
   - Analytics dashboard
   - Calendar integration
   - Multi-team support

3. **Community**
   - Share module
   - Gather feedback
   - Iterate and improve

---

## Conclusion

Following this guide, you will have built a complete AI-powered executive team implementing EOS methodology. The system will facilitate:

- Strategic clarity through V/TO
- Quarterly momentum through Rocks
- Weekly traction through L10 Meetings
- Daily execution through prioritization

Built on the proven BMAD Method framework, Mission Control amplifies human executive capability rather than replacing it.

Good luck with your implementation!
