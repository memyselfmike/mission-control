# BMAD Method Framework Analysis
## Reference Guide for Mission Control Implementation

**Version:** 1.0
**Date:** 14 October 2025
**Author:** Claude (Mission Control Team)
**Purpose:** Comprehensive analysis of BMAD Method v6-alpha architecture to guide Mission Control development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Core Philosophy and Approach](#core-philosophy-and-approach)
3. [System Architecture](#system-architecture)
4. [Agent Architecture Pattern](#agent-architecture-pattern)
5. [Workflow System Pattern](#workflow-system-pattern)
6. [Module Structure Pattern](#module-structure-pattern)
7. [Configuration and Variable System](#configuration-and-variable-system)
8. [File Organization Patterns](#file-organization-patterns)
9. [Applying BMAD Patterns to Mission Control](#applying-bmad-patterns-to-mission-control)
10. [Implementation Roadmap](#implementation-roadmap)
11. [Technical Decisions and Rationale](#technical-decisions-and-rationale)

---

## Executive Summary

The BMAD Method (BMad-CORE v6-alpha) is a **Collaboration Optimized Reflection Engine** designed to enhance human thinking through AI agents rather than replace it. It provides a proven framework for building specialized agent-based systems that guide users through reflective workflows.

### Key Insight for Mission Control

**BMAD Method is to Software Development what Mission Control should be to Executive Management.**

Both systems:
- Use specialized AI agents for different professional roles
- Employ structured workflows to guide users through complex processes
- Adapt to different scales of complexity (BMAD: project size 0-4, Mission Control: business complexity)
- Generate structured documents from templates
- Facilitate rather than automate human expertise
- Build on proven methodologies (BMAD: Agile/Scrum, Mission Control: EOS)

---

## Core Philosophy and Approach

### The BMAD Philosophy: Human Amplification, Not Replacement

**Traditional AI Approach:**
```
User Request → AI Does Everything → Provides Answer
```
**Problem:** Generic, bland solutions with no human insight

**BMAD Approach:**
```
User Request → Agent Facilitates Process → Elicits Human Expertise → Guides Reflection → Co-Creates Solution
```
**Result:** Best thinking from both human and AI through guided collaboration

### How BMAD Achieves This

1. **Specialized Agents as Expert Coaches**
   - PM agent acts like a real Product Manager (asks probing questions, demands clarity)
   - Architect agent thinks like a seasoned architect (considers trade-offs, patterns, scale)
   - Each agent has distinct persona, communication style, and principles

2. **Structured Workflows as Facilitation Frameworks**
   - Workflows don't "do the work" - they guide the user through doing it themselves
   - Step-by-step elicitation of expertise
   - Checkpoints for reflection and validation
   - Optional steps allow experienced users to move faster

3. **Scale Adaptation Based on Context**
   - Level 0: Single atomic change (minimal process)
   - Level 1-2: Small projects (focused documentation)
   - Level 3-4: Complex projects (full architecture and planning)
   - System adapts depth of process to complexity of need

### Mission Control Translation

This same philosophy applies perfectly to executive management:

**Traditional Executive Tool:**
```
"AI, create my business plan" → Generic template → Bland output
```

**Mission Control Approach:**
```
"Let's build your Vision/Traction Organizer"
  → EOS Implementer agent guides through 8 questions
  → Strategist agent probes for clarity on vision
  → User does the hard thinking with expert facilitation
  → Result: Genuine strategic clarity owned by the CEO
```

---

## System Architecture

### BMAD Method Architecture Overview

```
BMAD-METHOD/
│
├── src/                          # Source files (development)
│   ├── core/                     # Core framework
│   │   ├── agents/               # bmad-master orchestrator
│   │   ├── workflows/            # Core workflows (party-mode, init)
│   │   └── tasks/                # Core tasks (workflow.xml execution engine)
│   │
│   ├── modules/                  # Specialized modules
│   │   ├── bmm/                  # BMad Method (software dev)
│   │   │   ├── agents/           # PM, Analyst, Architect, SM, Dev, etc.
│   │   │   ├── workflows/        # 4-phase development workflows
│   │   │   ├── teams/            # Multi-agent team configs
│   │   │   └── _module-installer/
│   │   │
│   │   ├── bmb/                  # BMad Builder (agent/workflow creator)
│   │   └── cis/                  # Creative Intelligence Suite
│   │
│   └── utility/                  # Shared utilities and templates
│
└── Installation creates →

{project-root}/bmad/              # Installed runtime system
    ├── core/
    ├── bmm/                      # (if selected)
    ├── mission-control/          # (our new module!)
    └── _cfg/                     # Runtime configuration
        ├── agents/               # Agent customizations
        ├── config.yaml           # Project config
        ├── agent-manifest.csv    # All installed agents
        ├── workflow-manifest.csv # All workflows
        └── task-manifest.csv     # All tasks
```

### Key Architectural Principles

1. **Source vs. Runtime Separation**
   - `src/` contains development files
   - Installer copies to `{project-root}/bmad/` for runtime
   - Users customize runtime files without affecting source

2. **Module-Based Organization**
   - Each domain (software dev, creativity, etc.) is a module
   - Modules can be installed independently
   - Modules can reference each other's components

3. **Manifest-Based Discovery**
   - All agents registered in `agent-manifest.csv`
   - All workflows registered in `workflow-manifest.csv`
   - bmad-master reads manifests to present options

4. **Configuration-Driven Behavior**
   - Single `config.yaml` per module
   - Variables injected at runtime
   - Agents and workflows reference config variables

---

## Agent Architecture Pattern

### Agent Definition Structure (YAML Format)

```yaml
# Example: pm.agent.yaml
agent:
  metadata:
    id: "bmad/bmm/agents/pm.md"
    name: "John"                    # Agent's name
    title: "Product Manager"        # Role title
    icon: "📋"                      # Visual identifier
    module: "bmm"                   # Parent module

  persona:
    role: "Investigative Product Strategist + Market-Savvy PM"
    identity: "Product management veteran with 8+ years experience..."
    communication_style: "Direct and analytical with stakeholders..."
    principles:
      - "I operate with an investigative mindset..."
      - "My decision-making blends data-driven insights..."

  # Critical actions executed on agent activation
  critical_actions:
    - "Load into memory {project-root}/bmad/bmm/config.yaml"
    - "Remember the users name is {user_name}"
    - "ALWAYS communicate in {communication_language}"

  # Menu of commands available to user
  menu:
    - trigger: "workflow-status"
      workflow: "{project-root}/bmad/bmm/workflows/1-analysis/workflow-status/workflow.yaml"
      description: "Check workflow status and get recommendations"

    - trigger: "plan-project"
      workflow: "{project-root}/bmad/bmm/workflows/2-plan/workflow.yaml"
      description: "Analyze Project Scope and Create PRD"
```

### The Three Agent Types

#### 1. Simple Agent
**Purpose:** Standalone utility, no external dependencies

**Characteristics:**
- Self-contained logic
- Minimal or no file dependencies
- Good for: converters, calculators, quick tools

**Example Use Cases:**
- Format converter agent
- Text analyzer agent
- Quick reference agent

#### 2. Expert Agent (Sidecar Pattern)
**Purpose:** Domain-specific agent with restricted access and persistent knowledge

**Characteristics:**
- Has sidecar files (instructions.md, memories.md)
- Restricted file access (domain boundaries)
- Persistent context across sessions
- Good for: specialized domains with rules and memory

**Example Use Cases:**
- Diary keeper (only accesses diary folder)
- Financial advisor (only accesses financial data)
- Personal trainer (tracks progress over time)

**Critical Pattern:**
```yaml
critical_actions:
  # MANDATORY: Load sidecar files FIRST
  - critical: "MANDATORY"
    action: "Load COMPLETE file {agent-folder}/instructions.md"
  - critical: "MANDATORY"
    action: "Load COMPLETE file {agent-folder}/memories.md"

  # Domain restriction
  - critical: "MANDATORY"
    action: "ONLY access files in {user-folder}/specific-domain/"
```

#### 3. Module Agent (Primary Pattern for Mission Control)
**Purpose:** Full-featured agent integrated with module workflows

**Characteristics:**
- Connected to module config
- Multiple workflows available
- Template-based document generation
- Good for: professional tools with complex workflows

**Example Use Cases:**
- PM agent (plan-project workflow)
- Architect agent (solution-architecture workflow)
- **Mission Control agents** (Chief of Staff, Strategist, Planner, etc.)

### Agent Persona Design

The **persona** section is critical - it's what gives the agent personality and approach:

```yaml
persona:
  # WHO they are professionally
  role: "Investigative Product Strategist + Market-Savvy PM"

  # BACKGROUND and expertise
  identity: "Product management veteran with 8+ years experience
             launching B2B and consumer products. Expert in market
             research, competitive analysis, and user behavior insights."

  # HOW they communicate
  communication_style: "Direct and analytical with stakeholders.
                        Asks probing questions to uncover root causes.
                        Uses data and user insights to support recommendations."

  # WHAT they believe and how they operate
  principles:
    - "I operate with an investigative mindset that seeks the deeper 'why'"
    - "My decision-making blends data-driven insights with judgment"
    - "I communicate with precision and clarity"
```

### Agent Menu Pattern

The menu defines what the agent can do:

```yaml
menu:
  # Workflow commands (most common)
  - trigger: "command-name"
    workflow: "{project-root}/bmad/module/workflows/name/workflow.yaml"
    description: "What this command does"

  # Task commands (simpler operations)
  - trigger: "validate"
    exec: "{project-root}/bmad/core/tasks/validate-workflow.xml"
    description: "Validate document against checklist"

  # Template generation commands
  - trigger: "create-brief"
    exec: "{project-root}/bmad/core/tasks/create-doc.md"
    tmpl: "{project-root}/bmad/module/templates/brief.md"
    description: "Create project brief"
```

**Note:** `*help` and `*exit` are auto-injected by the build system

---

## Workflow System Pattern

### Workflow vs. Task

| Aspect | Task | Workflow |
|--------|------|----------|
| **Purpose** | Single operation | Multi-step process |
| **Format** | XML in `.md` file | Folder with YAML config |
| **Location** | `src/core/tasks/` | `src/modules/*/workflows/` |
| **User Input** | Minimal | Extensive elicitation |
| **Output** | Variable | Usually structured documents |
| **Complexity** | Atomic action | Guided journey |

### Workflow File Structure

Every workflow is a folder containing:

```
workflow-name/
├── workflow.yaml        # REQUIRED - Configuration and metadata
├── instructions.md      # Step-by-step execution guide
├── template.md          # Output document structure
├── checklist.md         # Validation criteria (optional)
└── [supporting files]   # Data, sub-templates, etc.
```

### workflow.yaml Configuration

```yaml
# Metadata
name: "plan-project"
description: "Scale-adaptive project planning for all project levels"
author: "BMad"

# Configuration source
config_source: "{project-root}/bmad/bmm/config.yaml"
project_name: "{config_source}:project_name"
output_folder: "{config_source}:output_folder"
user_name: "{config_source}:user_name"

# Recommended input documents
recommended_inputs:
  - product_brief: "{output_folder}/product-brief.md"
  - market_research: "{output_folder}/market-research.md"

# Paths to workflow components
installed_path: "{project-root}/bmad/bmm/workflows/2-plan"
template: "{installed_path}/prd-template.md"
instructions: "{installed_path}/instructions.md"
validation: "{installed_path}/checklist.md"

# Output configuration
default_output_file: "{output_folder}/PRD.md"
status_file: "{output_folder}/bmm-workflow-status.md"

# Scale adaptation parameters
scale_parameters:
  level_0: "Single atomic change, tech-spec only"
  level_1: "1-10 stories, minimal PRD"
  level_2: "5-15 stories, focused PRD"
  level_3: "12-40 stories, full PRD + architecture"
  level_4: "40+ stories, enterprise PRD"
```

### instructions.md Structure

The instructions guide the agent through executing the workflow:

```markdown
# instructions.md

<critical>The workflow execution engine is governed by: {project_root}/bmad/core/tasks/workflow.xml</critical>
<critical>You MUST have already loaded and processed: workflow.yaml</critical>

<workflow>

<step n="1" goal="Understand project context">
Load any existing documents from recommended_inputs.

Ask the user to describe:
- What problem are they solving?
- Who is the target user?
- What's the desired outcome?

<template-output>project_context</template-output>
</step>

<step n="2" goal="Define core requirements">
Based on the context, elicit 5-10 functional requirements.

For each requirement:
- What user need does it address?
- What is the acceptance criteria?
- What is the priority level?

<template-output>requirements</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="3" goal="Validate completeness">
Review all gathered information against the checklist.

<check if="incomplete">
  <action>Identify missing elements</action>
  <goto step="2">Return to requirements gathering</goto>
</check>

<check if="complete">
  <action>Proceed to document generation</action>
</check>

<template-output>validation_status</template-output>
</step>

</workflow>
```

### Key Workflow Patterns

#### 1. Elicitation Pattern
```xml
<step n="2" goal="Gather requirements">
Ask probing questions to elicit requirements:
- What must the system do?
- What constraints exist?
- What are the success criteria?

Aim for 5-10 specific requirements.

<template-output>requirements</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>
```

The `<invoke-task>` with `halt="true"` triggers advanced elicitation:
- AI agent asks clarifying questions
- Digs deeper on vague responses
- Challenges assumptions
- Ensures specificity

#### 2. Conditional Execution Pattern
```xml
<step n="5" goal="Check prerequisites">
  <action if="file exists">Load existing configuration</action>
  <action if="new project">Initialize from template</action>

  <check if="configuration invalid">
    <action>Log validation errors</action>
    <goto step="3">Return to configuration</goto>
  </check>
</step>
```

#### 3. Repetition Pattern
```xml
<step n="6" goal="Define epics" repeat="3-5">
For epic {{iteration}}:
- Epic name and description
- User value delivered
- Estimated complexity

<template-output>epic_{{iteration}}</template-output>
</step>
```

#### 4. Scale Adaptation Pattern
```xml
<step n="1" goal="Determine project scale">
Ask questions to assess:
- New vs. existing codebase
- Number of features (rough estimate)
- Team size
- Timeline

Based on answers, set scale level (0-4).

<template-output>scale_level</template-output>
</step>

<step n="2" goal="Route to appropriate workflow">
  <action if="level_0 or level_1">Load tech-spec instructions</action>
  <action if="level_2 or level_3">Load PRD instructions</action>
  <action if="level_4">Load enterprise PRD instructions</action>
</step>
```

### template.md Structure

Templates use `{{variable}}` syntax for replacement:

```markdown
# {{project_name}} - Product Requirements Document

**Version:** 1.0
**Date:** {{date}}
**Author:** {{user_name}}

## 1. Vision and Goals

{{vision}}

## 2. Target Users

{{target_users}}

## 3. Functional Requirements

{{requirements}}

## 4. Non-Functional Requirements

{{non_functional_requirements}}

## 5. Success Metrics

{{success_metrics}}

---

*Generated using Mission Control EOS System*
```

Variables come from:
1. `workflow.yaml` config
2. User input during workflow
3. `<template-output>` tags in instructions
4. System variables (date, paths, etc.)

### checklist.md Structure

Validation criteria for the generated document:

```markdown
# PRD Validation Checklist

## Structure
- [ ] All sections present and non-empty
- [ ] No placeholder text remains
- [ ] Proper markdown formatting

## Content Quality
- [ ] Vision is clear and inspirational
- [ ] Target users specifically defined
- [ ] Each requirement has acceptance criteria
- [ ] Success metrics are measurable

## Completeness
- [ ] All functional requirements captured
- [ ] Technical constraints documented
- [ ] Dependencies identified
- [ ] Next steps defined
```

---

## Module Structure Pattern

### Standard Module Layout

```
src/modules/{module-code}/
│
├── README.md                      # Module documentation
│
├── agents/                        # All module agents
│   ├── agent1.agent.yaml
│   ├── agent2.agent.yaml
│   └── agent3.agent.yaml
│
├── workflows/                     # All workflows organized by phase/type
│   ├── workflow1/
│   │   ├── workflow.yaml
│   │   ├── instructions.md
│   │   ├── template.md
│   │   └── checklist.md
│   │
│   ├── workflow2/
│   └── _shared/                   # Shared workflow resources
│
├── tasks/                         # Reusable tasks (optional)
│   ├── task1.md
│   └── task2.xml
│
├── templates/                     # Shared templates (optional)
│   ├── template1.md
│   └── template2.md
│
├── teams/                         # Multi-agent team configs (optional)
│   └── team1.yaml
│
└── _module-installer/             # Installation configuration
    ├── install-menu-config.yaml   # Installer prompts
    └── manifest.yaml              # Module metadata
```

### BMM (BMad Method Module) as Reference

BMM is organized by the 4-phase development workflow:

```
src/modules/bmm/
├── agents/
│   ├── pm.agent.yaml              # Product Manager
│   ├── analyst.agent.yaml         # Business Analyst
│   ├── architect.agent.yaml       # Technical Architect
│   ├── sm.agent.yaml              # Scrum Master
│   ├── dev.agent.yaml             # Developer
│   └── tea.agent.yaml             # Test Architect
│
└── workflows/
    ├── 1-analysis/                # Phase 1: Discovery
    │   ├── brainstorm-project/
    │   ├── research/
    │   └── product-brief/
    │
    ├── 2-plan/                    # Phase 2: Planning
    │   ├── prd/
    │   ├── tech-spec/
    │   └── workflow.yaml          # Router to appropriate sub-workflow
    │
    ├── 3-solutioning/             # Phase 3: Architecture
    │   ├── solution-architecture/
    │   └── tech-spec/
    │
    ├── 4-implementation/          # Phase 4: Development
    │   ├── create-story/
    │   ├── story-context/
    │   ├── dev-story/
    │   └── retrospective/
    │
    └── _shared/                   # Cross-phase resources
        └── bmm-workflow-status-template.md
```

### Mission Control Module Structure (Proposed)

```
src/modules/mission-control/
├── README.md
│
├── agents/
│   ├── chief-of-staff.agent.yaml      # Orchestrator
│   ├── strategist.agent.yaml          # Vision/Strategy
│   ├── planner.agent.yaml             # Quarterly/Rocks
│   ├── operator.agent.yaml            # Daily execution
│   └── eos-implementer.agent.yaml     # EOS expert (Expert Agent type)
│       ├── eos-rules.md               # Sidecar: EOS methodology
│       └── eos-memories.md            # Sidecar: User context
│
└── workflows/
    ├── eos-installation/              # One-time setup
    │   ├── workflow.yaml
    │   ├── instructions.md
    │   └── checklist.md
    │
    ├── vto-create/                    # Vision/Traction Organizer
    │   ├── workflow.yaml
    │   ├── instructions.md
    │   ├── template.md
    │   └── checklist.md
    │
    ├── quarterly-pulsing/             # 90-day review and planning
    │   ├── workflow.yaml
    │   ├── instructions.md
    │   └── template.md
    │
    ├── l10-meeting/                   # Weekly Level 10 Meeting
    │   ├── workflow.yaml
    │   ├── instructions.md
    │   ├── template.md
    │   └── l10-agenda.md
    │
    ├── daily-focus/                   # Daily planning
    │   ├── workflow.yaml
    │   └── instructions.md
    │
    ├── agent-design/                  # Design new AI agent
    │   ├── workflow.yaml
    │   ├── instructions.md
    │   ├── template.md
    │   └── gwc-assessment.md
    │
    └── _shared/
        ├── scorecard-template.md
        └── accountability-chart-template.md
```

---

## Configuration and Variable System

### Configuration File (config.yaml)

Each module has a single configuration file:

```yaml
# bmad/mission-control/config.yaml

# Project identification
project_name: "Mission Control"
output_folder: "D:/Mission Control/output"

# User preferences
user_name: "Mike"
communication_language: "English"

# Business configuration
company_name: "Your Company Name"
industry: "Your Industry"
eos_implementation_date: "2025-10-14"

# Meeting configuration
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

### Variable System

#### 1. System Variables (Built-in)
```
{project-root}         → D:/Mission Control
{date}                 → 2025-10-14
{time}                 → 10:30 AM
```

#### 2. Config Variables (From config.yaml)
```
{config_source}:project_name      → Mission Control
{config_source}:user_name         → Mike
{config_source}:output_folder     → D:/Mission Control/output
```

#### 3. Workflow Variables (From instructions)
```
<template-output>vision</template-output>
    ↓
{{vision}} in template.md
```

#### 4. Module Path Variables
```
{installed_path}                  → {project-root}/bmad/mission-control/workflows/vto-create
{agent-folder}                    → {project-root}/bmad/mission-control/agents/eos-implementer
```

### Variable Usage in Agent Definitions

```yaml
agent:
  critical_actions:
    # Load config and set variables
    - "Load into memory {project-root}/bmad/mission-control/config.yaml"
    - "Remember the user's name is {user_name}"
    - "ALWAYS communicate in {communication_language}"

  menu:
    - trigger: "vto-create"
      workflow: "{project-root}/bmad/mission-control/workflows/vto-create/workflow.yaml"
      description: "Create Vision/Traction Organizer"
```

### Variable Usage in Workflows

```yaml
# workflow.yaml
config_source: "{project-root}/bmad/mission-control/config.yaml"
project_name: "{config_source}:project_name"
output_folder: "{config_source}:output_folder"
default_output_file: "{output_folder}/VTO.md"
```

---

## File Organization Patterns

### Naming Conventions

**Agent Files:**
```
{role-name}.agent.yaml
Examples: pm.agent.yaml, chief-of-staff.agent.yaml
```

**Workflow Folders:**
```
{action-noun}/
Examples: plan-project/, vto-create/, l10-meeting/
```

**Template Files:**
```
{document-type}-template.md
Examples: prd-template.md, vto-template.md, l10-minutes-template.md
```

**Checklist Files:**
```
checklist.md (inside workflow folder)
or
{document-type}-checklist.md
```

### Path Construction Patterns

**Absolute paths using variables (GOOD):**
```
{project-root}/bmad/mission-control/workflows/vto-create/workflow.yaml
{installed_path}/template.md
{output_folder}/VTO.md
```

**Relative paths (AVOID):**
```
../../workflows/vto-create/workflow.yaml    ❌
./template.md                                ❌
```

**Hard-coded paths (NEVER):**
```
D:/Mission Control/bmad/workflows/...        ❌
```

### Manifest Files

All agents and workflows are registered in manifest files:

**agent-manifest.csv:**
```csv
agent_id,agent_name,agent_title,module,icon,file_path
chief-of-staff,Alex,Chief of Staff,mission-control,🎯,bmad/mission-control/agents/chief-of-staff.agent.yaml
strategist,Vision,Strategist,mission-control,🔭,bmad/mission-control/agents/strategist.agent.yaml
```

**workflow-manifest.csv:**
```csv
workflow_id,workflow_name,description,module,file_path
vto-create,Create V/TO,Create Vision/Traction Organizer,mission-control,bmad/mission-control/workflows/vto-create/workflow.yaml
l10-meeting,L10 Meeting,Run Level 10 Meeting,mission-control,bmad/mission-control/workflows/l10-meeting/workflow.yaml
```

---

## Applying BMAD Patterns to Mission Control

### Direct Parallels

| BMAD Method (Software Dev) | Mission Control (Executive) |
|----------------------------|----------------------------|
| **PM Agent** - Plans software projects | **Strategist Agent** - Plans business vision |
| **Analyst Agent** - Research & discovery | **Chief of Staff** - Context gathering & routing |
| **Architect Agent** - Technical design | **Planner Agent** - Quarterly planning & structure |
| **SM Agent** - Sprint management | **Operator Agent** - Daily execution management |
| **Dev Agent** - Implementation | **EOS Implementer** - Process facilitation |
| | |
| **plan-project workflow** | **vto-create workflow** |
| Creates PRD through elicitation | Creates V/TO through 8 questions |
| Scale-adaptive (0-4 complexity) | Scale-adaptive (solopreneur to enterprise) |
| | |
| **create-story workflow** | **daily-focus workflow** |
| Break epic into development story | Break priorities into daily tasks |
| | |
| **retrospective workflow** | **quarterly-pulsing workflow** |
| Review sprint, improve process | Review quarter, set new Rocks |

### Key Adaptation Points

#### 1. Scale Adaptation for Business Complexity

BMAD adapts to project size. Mission Control should adapt to business complexity:

```yaml
# BMAD scale levels
scale_parameters:
  level_0: "Single atomic change"
  level_1: "1-10 stories, 1 epic"
  level_2: "5-15 stories, 1-2 epics"
  level_3: "12-40 stories, 2-5 epics"
  level_4: "40+ stories, enterprise scale"

# Mission Control scale levels (proposed)
scale_parameters:
  level_0: "Solopreneur - You + AI agents"
  level_1: "Small team - 2-5 people"
  level_2: "Growing business - 5-15 people"
  level_3: "Established company - 15-50 people"
  level_4: "Enterprise - 50+ people"
```

The workflow adapts:
- Level 0-1: Simplified V/TO, personal Rocks, individual focus
- Level 2-3: Full Accountability Chart, team Scorecard, department Rocks
- Level 4: Multiple Accountability Charts, consolidated Scorecard, executive team

#### 2. Facilitation vs. Automation

BMAD agents **facilitate** software development, they don't write code automatically.

Mission Control agents should **facilitate** executive thinking, not make decisions automatically.

**Example - L10 Meeting Workflow:**

❌ **Wrong Approach (Automation):**
```
Agent: "I've analyzed your metrics and identified your top 3 issues:
1. Revenue is down
2. Customer churn is up
3. Team morale is low

I recommend hiring 2 salespeople and implementing a retention program."
```

✅ **Right Approach (Facilitation):**
```
Agent: "Let's review your Scorecard. I see 3 numbers are off track this week:
- Sales calls: 45 (goal: 60)
- Customer renewal rate: 82% (goal: 90%)
- Team NPS: 6.5 (goal: 8.0)

Which of these feels most urgent to you right now?
Let's add it to the Issues List and work through it with IDS."

[User selects renewal rate]

Agent: "Great. Let's Identify the issue clearly. In one sentence,
what's the root problem with renewal rate?"

[User responds: "We're not checking in with customers mid-contract"]

Agent: "Good. Now let's Discuss. What are some possible solutions?"

[Facilitates discussion...]

Agent: "Okay, we've discussed 4 options. Which one feels like the best
next step to Solve this issue?"

[User decides, agent captures action item]
```

The agent **guides the process** but the user **does the thinking**.

#### 3. Document Templates Follow EOS Structure

BMAD templates follow software development conventions (PRD, Tech Spec, Architecture).

Mission Control templates should follow EOS conventions exactly:

**Vision/Traction Organizer Template Structure:**
```markdown
# {{company_name}} - Vision/Traction Organizer™

## Core Values
{{core_values}}

## Core Focus™
**Purpose:** {{purpose}}
**Niche:** {{niche}}

## 10-Year Target™
{{ten_year_target}}

## Marketing Strategy
**Target Market:** {{target_market}}
**Three Uniques:** {{three_uniques}}
**Proven Process:** {{proven_process}}

## 3-Year Picture™
{{three_year_picture}}

## 1-Year Plan
{{one_year_plan}}

## Rocks (This Quarter)
{{rocks}}

## Issues List
{{issues_list}}
```

This follows the official EOS V/TO structure precisely.

#### 4. Workflow Patterns Map to EOS Processes

| EOS Process | Mission Control Workflow | Pattern from BMAD |
|-------------|-------------------------|-------------------|
| **Vision/Traction Organizer™** | vto-create | Document generation workflow |
| **Level 10 Meeting™** | l10-meeting | Structured facilitation workflow |
| **Quarterly Planning** | quarterly-pulsing | Retrospective + planning workflow |
| **IDS™ (Identify, Discuss, Solve)** | ids-session | Problem-solving workflow |
| **Accountability Chart** | accountability-chart-update | Visual document workflow |
| **Scorecard** | scorecard-create | Metrics elicitation workflow |
| **GWC™ (Get it, Want it, Capacity)** | gwc-assessment | Evaluation framework workflow |

Each workflow follows BMAD's pattern:
1. Load context (existing documents)
2. Elicit information through questions
3. Guide reflection and decision-making
4. Generate structured output
5. Validate against checklist

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)

**Goal:** Get BMAD installed and create basic module structure

**Tasks:**
1. ✅ Git repository initialized
2. Install BMAD v6-alpha to Mission Control project
3. Create `src/modules/mission-control/` structure
4. Create basic `config.yaml`
5. Create module `README.md`
6. Test BMAD installation with existing modules

**Deliverables:**
- Working BMAD installation
- Empty Mission Control module structure
- Configuration file template

### Phase 2: First Agent (Week 2-3)

**Goal:** Create and test one complete agent with one workflow

**Agent:** EOS Implementer (Expert Agent type)
**Workflow:** vto-create (Vision/Traction Organizer)

**Tasks:**
1. Create `eos-implementer.agent.yaml`
2. Create sidecar files:
   - `eos-rules.md` (EOS methodology reference)
   - `eos-memories.md` (placeholder for user context)
3. Create `workflows/vto-create/`
   - `workflow.yaml`
   - `instructions.md` (8 V/TO questions)
   - `template.md` (V/TO document structure)
   - `checklist.md` (validation criteria)
4. Test end-to-end: Load agent → Run workflow → Generate V/TO
5. Iterate on elicitation questions and template

**Deliverables:**
- Working EOS Implementer agent
- Working V/TO creation workflow
- First generated V/TO document
- Validated pattern for remaining agents

### Phase 3: Core Agent Suite (Week 3-5)

**Goal:** Create remaining 4 core agents with key workflows

**Agents & Primary Workflows:**

1. **Chief of Staff** (Orchestrator)
   - Workflow: `system-status` (show current state)
   - Workflow: `daily-standup` (quick sync)

2. **Strategist**
   - Workflow: `vto-review` (update existing V/TO)
   - Workflow: `rocks-set` (define quarterly Rocks)

3. **Planner**
   - Workflow: `quarterly-pulsing` (90-day review and planning)
   - Workflow: `scorecard-create` (build metrics dashboard)

4. **Operator**
   - Workflow: `daily-focus` (morning planning routine)
   - Workflow: `task-triage` (prioritization)

**Tasks:**
- Follow Phase 2 pattern for each agent
- Each agent: YAML definition + 1-2 workflows
- Test each agent independently
- Test agent handoffs (Chief of Staff → Specialist)

**Deliverables:**
- 5 working agents (EOS Implementer + 4 core agents)
- 8-10 working workflows
- Integration between agents tested

### Phase 4: L10 Meeting (Week 5-6)

**Goal:** Implement the most important EOS workflow

**Why L10 First:**
- Most frequent workflow (weekly)
- Touches all components (Scorecard, Rocks, Issues, To-Dos)
- Demonstrates full facilitation capability

**L10 Meeting Workflow Structure:**
```
workflows/l10-meeting/
├── workflow.yaml
├── instructions.md              # Main L10 orchestration
├── template.md                  # Meeting minutes output
├── checklist.md                 # L10 quality validation
├── l10-agenda.md                # Official 7-step agenda
├── ids-process.md               # IDS facilitation guide
└── segue-prompts.md             # Good news prompts
```

**Tasks:**
1. Create detailed `instructions.md` following 7-step L10 agenda:
   - Segue (5 min)
   - Scorecard Review (5 min)
   - Rock Review (5 min)
   - Customer/Employee Headlines (5 min)
   - To-Do List (5 min)
   - IDS (60 min)
   - Conclude (5 min)
2. Create IDS sub-workflow (Identify, Discuss, Solve)
3. Build meeting minutes template
4. Test full 90-minute L10 meeting simulation
5. Refine facilitation language and timing

**Deliverables:**
- Complete L10 Meeting workflow
- IDS problem-solving sub-workflow
- Meeting minutes template
- Validated weekly cadence capability

### Phase 5: Supporting Workflows (Week 6-7)

**Goal:** Complete the workflow suite

**Remaining Workflows:**

1. **eos-installation** (one-time setup)
   - Guides new user through all foundational documents
   - Creates initial V/TO, Accountability Chart, Scorecard, Rocks
   - Sets up L10 cadence

2. **accountability-chart-update**
   - Build or update organizational structure
   - Define seats and 5 roles per seat
   - Identify open seats

3. **rock-tracking**
   - Update Rock status (on/off track)
   - Identify blockers
   - Adjust as needed

4. **scorecard-update**
   - Enter weekly numbers
   - Flag off-track metrics
   - Add to Issues List if needed

5. **agent-design** (meta-workflow)
   - Define new AI agent for Accountability Chart seat
   - Use GWC assessment
   - Generate agent specification

**Deliverables:**
- Complete workflow suite
- All EOS processes covered
- Meta-capability to design new agents

### Phase 6: Polish and Documentation (Week 7-8)

**Goal:** Production-ready system with complete documentation

**Tasks:**

1. **User Documentation**
   - Getting started guide
   - Agent reference (what each agent does)
   - Workflow reference (when to use each workflow)
   - EOS methodology primer
   - Troubleshooting guide

2. **Developer Documentation**
   - Architecture overview
   - Adding new agents
   - Adding new workflows
   - Customization guide

3. **System Polish**
   - Consistent agent personalities
   - Smooth transitions between workflows
   - Error handling and edge cases
   - Configuration validation

4. **Testing**
   - Complete end-to-end test scenarios
   - All workflows tested
   - Agent interactions tested
   - Document generation validated

**Deliverables:**
- Complete documentation suite
- Polished user experience
- Validated test coverage
- Production-ready v1.0

### Phase 7: Advanced Features (Week 9-10)

**Goal:** Value-added features beyond basic EOS

**Features:**

1. **Analytics Dashboard**
   - Rock completion trends over time
   - Scorecard visualization
   - Meeting effectiveness scores
   - Issue resolution tracking

2. **Smart Recommendations**
   - Suggest Issues based on off-track numbers
   - Recommend Rock prioritization
   - Flag when Accountability Chart needs update

3. **Integration Hooks**
   - Calendar sync for L10 meetings
   - Export to Google Sheets/Excel
   - Import metrics from external sources
   - Email meeting minutes distribution

4. **AI Agent Marketplace**
   - Pre-built agents for common business functions
   - Sales agent, Marketing agent, Finance agent, etc.
   - One-click install to Accountability Chart

**Deliverables:**
- Advanced analytics capability
- Integration with external tools
- Agent marketplace framework
- Mission Control v2.0

---

## Technical Decisions and Rationale

### Decision 1: Use BMAD Method Framework (vs. Build From Scratch)

**Rationale:**
- ✅ Proven architecture for agent-based systems
- ✅ Handles complexity we'd have to solve anyway (agent loading, workflow execution, variable substitution)
- ✅ Modular and extensible by design
- ✅ Active development and community
- ✅ Already solved hard problems (scale adaptation, elicitation, validation)
- ❌ Learning curve for BMAD conventions
- ❌ Dependency on external framework

**Decision:** Use BMAD Method. The benefits far outweigh the learning curve.

### Decision 2: Module Agent Type (vs. Simple or Expert)

**Rationale:**
- Module Agents integrate with config system
- Support multiple complex workflows
- Can reference shared templates and resources
- Appropriate for professional tool suite

**Decision:** All 5 core agents will be Module Agents (Chief of Staff, Strategist, Planner, Operator, EOS Implementer)

### Decision 3: EOS Implementer as Expert Agent Subtype

**Rationale:**
- Needs deep EOS methodology knowledge (sidecar file)
- Should remember user's business context (memories file)
- Benefits from domain-specific expertise pattern

**Decision:** EOS Implementer will be a Module Agent with sidecar files (hybrid approach)

### Decision 4: Workflows Over Tasks

**Rationale:**
- EOS processes are multi-step and require facilitation
- Need user interaction and elicitation
- Generate structured documents
- Require validation

**Decision:** All major EOS processes implemented as Workflows, not Tasks

### Decision 5: Scale Adaptation by Business Size

**Rationale:**
- EOS methodology itself adapts to company size
- Solopreneur needs simpler process than 50-person company
- BMAD's scale pattern (0-4) maps well to business stages

**Decision:** Implement 5-level scale adaptation (0-4) throughout Mission Control

### Decision 6: Template Fidelity to Official EOS

**Rationale:**
- EOS is a trademarked methodology with specific structures
- Users may be familiar with official EOS documents
- Credibility and trust require accuracy

**Decision:** Templates will exactly follow official EOS V/TO™, L10™, Accountability Chart™ structures

### Decision 7: Facilitation Over Automation

**Rationale:**
- Aligns with BMAD philosophy (amplify human, don't replace)
- Executive decisions require human judgment
- Strategic thinking can't be automated
- Trust and adoption require human control

**Decision:** Agents facilitate and guide; humans make all decisions

### Decision 8: Phase L10 Meeting Early (Phase 4)

**Rationale:**
- L10 is the heartbeat of EOS (weekly cadence)
- Most complex workflow - validates architecture
- Demonstrates full facilitation capability
- High value even if other workflows incomplete

**Decision:** Prioritize L10 Meeting workflow in Phase 4

### Decision 9: Agent-Design Meta-Workflow

**Rationale:**
- Demonstrates self-extending system
- Enables custom agents for specific businesses
- Shows sophistication of framework
- High "wow factor" for users

**Decision:** Include agent-design workflow as part of core suite

### Decision 10: Version Control and Iteration Strategy

**Rationale:**
- This is a complex system that will evolve
- Need ability to iterate on prompts and workflows
- Users should be able to update easily
- Changes should not break existing documents

**Decision:**
- Use semantic versioning (v1.0, v1.1, v2.0)
- Maintain backward compatibility with document formats
- Provide migration guides for major versions
- Keep all workflows and templates in version control

---

## Appendix A: Key BMAD Files to Study

For implementation reference, study these source files:

**Agent Examples:**
- `src/modules/bmm/agents/pm.agent.yaml` - Well-structured Module Agent
- `src/modules/bmb/agents/bmad-builder.agent.yaml` - Agent that creates agents
- `src/core/agents/bmad-master.agent.yaml` - Orchestrator pattern

**Workflow Examples:**
- `src/modules/bmm/workflows/2-plan/workflow.yaml` - Scale-adaptive routing
- `src/modules/bmm/workflows/2-plan/prd/` - Complete document workflow
- `src/modules/bmm/workflows/4-implementation/create-story/` - Autonomous workflow

**Documentation:**
- `src/modules/bmb/workflows/create-agent/agent-architecture.md` - Agent structure reference
- `src/modules/bmb/workflows/create-workflow/workflow-creation-guide.md` - Workflow patterns
- `src/modules/bmm/README.md` - Module documentation example

**System Files:**
- `src/core/tasks/workflow.xml` - Workflow execution engine
- `src/utility/templates/agent.customize.template.yaml` - Agent customization

---

## Appendix B: Glossary

**BMAD Terms:**
- **BMAD-CORE** - Collaboration Optimized Reflection Engine, the framework itself
- **BMM** - BMad Method Module, software development lifecycle implementation
- **BMB** - BMad Builder Module, tools for creating agents and workflows
- **CIS** - Creative Intelligence Suite, brainstorming and creativity module
- **Module Agent** - Agent integrated with module config and workflows
- **Expert Agent** - Domain-specific agent with sidecar knowledge files
- **Simple Agent** - Standalone utility agent with no dependencies
- **Workflow** - Multi-step facilitated process generating structured output
- **Task** - Single atomic operation
- **Template** - Document structure with variable placeholders
- **Elicitation** - Process of drawing out user expertise through questions
- **Scale Adaptation** - Adjusting process depth to complexity level

**EOS Terms:**
- **EOS** - Entrepreneurial Operating System, the business methodology
- **V/TO™** - Vision/Traction Organizer, core strategic document
- **L10™** - Level 10 Meeting, weekly 90-minute team meeting
- **IDS™** - Identify, Discuss, Solve, problem-solving methodology
- **Rocks** - 3-7 quarterly priorities
- **Scorecard** - Weekly measurable numbers (5-15 metrics)
- **Accountability Chart™** - Function-based org chart
- **GWC™** - Get it, Want it, Capacity, role fit assessment
- **Core Focus™** - Company purpose and niche
- **Implementer** - Certified EOS consultant who installs the system

---

## Conclusion

The BMAD Method provides an ideal foundation for Mission Control because:

1. **Proven Architecture** - Solves the hard problems of multi-agent systems
2. **Facilitation Philosophy** - Aligns with how executive management should work
3. **Modular Design** - Easy to extend and customize
4. **Scale Adaptive** - Grows with the business
5. **Document Generation** - Natural fit for EOS document workflows
6. **Active Development** - Framework continues to improve

By following BMAD patterns and adapting them to EOS methodology, Mission Control can become the executive equivalent of the BMad Method - a trusted AI-powered executive team that amplifies the CEO's strategic thinking rather than replacing it.

The key is to stay true to both frameworks:
- **BMAD's philosophy:** Facilitate, don't automate
- **EOS's structure:** Follow proven processes exactly

This document serves as the architectural guide for implementation. Refer to specific sections as you build each component, and update this document as you discover new patterns or make architectural decisions.

---

**Next Steps:** Proceed to Phase 1 implementation using the roadmap in this document.

**Questions or Issues:** Document them in `/docs/implementation-notes.md` as you encounter them.
