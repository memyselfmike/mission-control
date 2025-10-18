# Mission Control - Documentation Index

**Project:** Mission Control
**Type:** CLI Tool (Autonomous AI Executive Team)
**Status:** Sprint 2 Complete (45/~250 points delivered - 18%)
**Last Updated:** 2025-10-17

---

## Quick Start

| I want to... | Go to |
|--------------|-------|
| Understand the project | [Project Overview](./project-overview.md) |
| See what's been built | [PRODUCT-BACKLOG.md](../PRODUCT-BACKLOG.md) (Sprint 1-2 complete) |
| Check current status | [BMM Workflow Status](./bmm-workflow-status.md) |
| Understand architecture | [Solution Architecture](./solution-architecture.md) |
| Review product requirements | [PRD](./PRD.md) |
| See epic breakdown | [Epics](./epics.md) |
| Learn project rules | [PROJECT-RULES.md](./PROJECT-RULES.md) ⚠️ READ THIS FIRST |

---

## Core Planning Documents

These documents define the project and guide development:

- **[PROJECT-RULES.md](./PROJECT-RULES.md)** - **START HERE!** Rules for all Claude agents
- **[PRD.md](./PRD.md)** - Product requirements document (7 goals, 29 features)
- **[epics.md](./epics.md)** - Epic definitions (7 EPICs, 45+ stories, 250+ points)
- **[solution-architecture.md](./solution-architecture.md)** - Complete architecture specification
- **[bmm-workflow-status.md](./bmm-workflow-status.md)** - Current sprint/story status
- **[project-overview.md](./project-overview.md)** - Executive summary
- **[source-tree-analysis.md](./source-tree-analysis.md)** - Codebase structure analysis
- **[unified-architecture-vision.md](./unified-architecture-vision.md)** - Architecture vision

---

## Active Stories

**Location:** `docs/stories/`

**Completed Stories (Reference):**
- **[Story 2.1](./stories/story-2.1.md)** - Business Context Storage (✅ Complete)
- **[Story 2.2](./stories/story-2.2.md)** - Conversation History Logging (✅ Complete)
- **[Story 2.3](./stories/story-2.3.md)** - Preference Learning System (✅ Complete)

**Next Stories:** TBD (awaiting Mike's priority decision)
- Option A: EPIC-3 (Operator Agent - daily execution)
- Option B: EPIC-4 (Planner Agent - goal management)
- Option C: Finish EPIC-1/2 (autonomous behaviors, memory pruning)

---

## Sprint Archives

**Location:** `docs/archive/`

### Sprint Summaries
- **Sprint 1:** EPIC-2 Memory System (16 points, 100% complete)
- **Sprint 2:** EPIC-1 Autonomous Behaviors (29 points, 100% complete)

**Files:** `docs/archive/sprint-summaries/`

### Story Artifacts
Implementation notes, design docs, and story variants

**Files:** `docs/archive/story-artifacts/`

### QA Reports
Test plans, test results, and quality status reports

**Files:** `docs/archive/qa-reports/`

### Bug Fixes
Bug fix summaries and incident reports

**Files:** `docs/archive/bug-fixes/`

### Miscellaneous
Audits, cleanup reports, and one-off documentation

**Files:** `docs/archive/misc/`

---

## Legacy Planning Files

**Location:** `docs/legacy-planning-files/`

These are historical planning documents from early project phases. They remain as reference but are superseded by current planning docs.

**EPICs:**
- [EPIC-1: Autonomous Agent Framework](./legacy-planning-files/epics/EPIC-1-autonomous-agent-framework.md)
- [EPIC-2: Chief of Staff Orchestrator](./legacy-planning-files/epics/EPIC-2-chief-of-staff-orchestrator.md)
- [EPIC-3: Operator (Daily Execution)](./legacy-planning-files/epics/EPIC-3-operator-daily-execution.md)
- [EPIC-4: Planner (Goals & Projects)](./legacy-planning-files/epics/EPIC-4-planner-goals-projects.md)
- [EPIC-5: Strategist (Vision & Thinking)](./legacy-planning-files/epics/EPIC-5-strategist-vision-thinking.md)
- [EPIC-6: Analyst (Business Intelligence)](./legacy-planning-files/epics/EPIC-6-analyst-business-intelligence.md)
- [EPIC-7: Agent Designer (Meta)](./legacy-planning-files/epics/EPIC-7-agent-designer-meta.md)

**Technical Guides:**
- [Implementation Guide](./legacy-planning-files/implementation-guide.md)
- [Agent Development Guide](./legacy-planning-files/AGENT-DEVELOPMENT-GUIDE.md)
- [Technical Setup Guide](./legacy-planning-files/TECHNICAL-SETUP-GUIDE.md)

---

## Project Structure

```
D:\Mission Control/
├── README.md                          [Project overview]
├── PRODUCT-BACKLOG.md                 [Active backlog with sprint status]
│
├── docs/                              [Documentation root]
│   ├── index.md                       [THIS FILE]
│   ├── PROJECT-RULES.md               [⚠️ MANDATORY READING for all agents]
│   ├── PRD.md                         [Product requirements]
│   ├── epics.md                       [Epic definitions]
│   ├── bmm-workflow-status.md         [Current status tracker]
│   ├── solution-architecture.md       [Architecture spec]
│   ├── project-overview.md            [Executive summary]
│   │
│   ├── stories/                       [Active story files only]
│   │   ├── story-2.1.md               [Completed stories for reference]
│   │   ├── story-2.2.md
│   │   ├── story-2.3.md
│   │   └── [future stories go here]
│   │
│   ├── archive/                       [Historical artifacts]
│   │   ├── sprint-summaries/          [Sprint retrospectives, planning]
│   │   ├── story-artifacts/           [Implementation notes, variants]
│   │   ├── qa-reports/                [Quality assurance documents]
│   │   ├── bug-fixes/                 [Bug fix summaries]
│   │   └── misc/                      [One-off documents, audits]
│   │
│   └── legacy-planning-files/         [Historical planning docs]
│
├── mission-control/                   [Application code]
│   ├── src/                           [Source code]
│   │   ├── main.py                    [Entry point]
│   │   ├── memory.py                  [Memory system - Stories 2.1-2.3, 1.9]
│   │   ├── scheduler.py               [Task scheduling - Story 1.6]
│   │   ├── task_registry.py           [Task management - Story 1.6]
│   │   ├── events/                    [Event system - Story 1.7]
│   │   └── patterns/                  [Pattern recognition - Story 1.8]
│   ├── tests/                         [Test suite (171+ tests passing)]
│   └── .claude/                       [Claude agent configuration]
│
└── bmad/                              [BMAD Method framework]
```

---

## Current Project Status

### Completed Work (Sprint 1-2)

**EPIC-2: Persistent Memory System** ✅ 100% Complete
- Story 2.1: Business Context Storage (5 pts)
- Story 2.2: Conversation History Logging (5 pts)
- Story 2.3: Preference Learning System (6 pts)

**EPIC-1: Autonomous Agent Framework** 🔄 73% Complete
- Story 1.6: Scheduled Task Execution (8 pts)
- Story 1.7: Event Detection System (8 pts)
- Story 1.8: Pattern Recognition Engine (8 pts)
- Story 1.9: Context Gathering (5 pts)

**Test Coverage:** 171+ tests passing (98%+ pass rate)
**Code Quality:** Zero bugs, comprehensive documentation
**Velocity:** 5-6 points/day (excellent)

### Next Up (Sprint 3)

**Awaiting Priority Decision:**
1. EPIC-3: Operator Agent (daily execution assistant)
2. EPIC-4: Planner Agent (goal management)
3. Complete remaining EPIC-1 work

---

## For Claude Agents

### MANDATORY READING

**Before starting ANY work on this project:**
1. Read [PROJECT-RULES.md](./PROJECT-RULES.md) completely
2. Check [bmm-workflow-status.md](./bmm-workflow-status.md) for current sprint/story
3. Review [PRODUCT-BACKLOG.md](../PRODUCT-BACKLOG.md) for overall status

### Quick Rules Summary

**File Organization:**
- Root level: ONLY README.md and PRODUCT-BACKLOG.md
- Story files: `docs/stories/story-{EPIC}.{NUM}-{slug}.md`
- Sprint artifacts: `docs/archive/sprint-summaries/`
- Story artifacts: `docs/archive/story-artifacts/`
- QA reports: `docs/archive/qa-reports/`
- Bug fixes: `docs/archive/bug-fixes/`

**Story Numbering:**
- Format: `EPIC#.Story#` (e.g., Story 2.1, Story 3.5)
- NEVER renumber completed stories
- Accept reality if numbering is imperfect

**Required Updates:**
When completing a story, update:
1. Story file (`docs/stories/story-X.Y.md`)
2. PRODUCT-BACKLOG.md
3. bmm-workflow-status.md

**Forbidden Actions:**
- ❌ Create markdown files at project root
- ❌ Renumber completed stories
- ❌ Skip tests
- ❌ Mark story Done without user approval

---

## Technology Stack

- **Language:** Python 3.13+
- **AI Framework:** Claude Agent SDK
- **CLI Framework:** Rich (formatted output)
- **Testing:** pytest (171+ tests)
- **Memory:** File-based JSON/JSONL
- **Platform:** Windows primary, cross-platform compatible
- **Methodology:** BMAD Method + Agile/Scrum

---

## External Resources

- **[Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk/python)** - Official SDK documentation
- **[Anthropic API Docs](https://docs.anthropic.com)** - Claude API reference
- **[MCP Servers](https://github.com/modelcontextprotocol/servers)** - Available MCP integrations

---

## Project Goals

Mission Control is an **autonomous AI executive team** that:
- Provides structured accountability (daily/weekly/quarterly)
- Offers ad-hoc strategic thinking
- Surfaces proactive intelligence without being asked
- Maintains persistent memory of context
- Extends itself via custom agent creation

**Key Differentiator:** Autonomous agents that work FOR you, not just respond TO you.

---

**Last Updated:** 2025-10-17
**Documentation Version:** 2.0 (Post-Cleanup)
**Project Status:** Sprint 2 Complete, Sprint 3 Planning

---

🧙 **For Agents:** Start with [PROJECT-RULES.md](./PROJECT-RULES.md) - it's your guide to working on this project correctly.

🚀 **For Users:** Start with [Project Overview](./project-overview.md) to understand what we're building.
