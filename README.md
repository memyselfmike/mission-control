# Mission Control

**Autonomous AI-Powered Executive Team**

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Claude Agent SDK](https://img.shields.io/badge/Claude%20Agent%20SDK-latest-green.svg)](https://docs.claude.com/en/api/agent-sdk)

---

## Overview

Mission Control is an **autonomous AI-powered executive team** that works FOR you, not just responds TO you. Built on the Claude Agent SDK with BMAD Method patterns, it provides structured accountability, ad-hoc strategic thinking, proactive intelligence, and persistent memory.

**Key Differentiator:** Autonomous agents that monitor, analyze, and surface insights without being asked—like having a real executive team that works while you sleep.

---

## Features

- 🤖 **Autonomous Operation** - Agents proactively monitor goals, detect patterns, and surface insights
- 💾 **Persistent Memory** - Context builds across sessions; agents learn your preferences
- 📊 **Proactive Intelligence** - Get insights without asking
- 📅 **Scheduled Operations** - Daily briefings, weekly reviews, quarterly planning
- 🎯 **Specialist Agents** - Delegate to experts (Strategist, Planner, Operator, Analyst)
- 🔧 **Extensible** - Create custom agents, workflows, and integrations

---

## Quick Start

```bash
# Clone with submodules
git clone --recursive https://github.com/memyselfmike/mission-control.git
cd mission-control/mission-control

# Install dependencies
uv sync

# Configure
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run
python main.py
```

---

## Repository Structure

Mission Control uses a **parent + submodule architecture**:

### This Repository (Parent)
**Purpose:** Documentation, planning, and project management

```
mission-control/                    # This repo
├── README.md                       # This file
├── PRODUCT-BACKLOG.md             # Product backlog and epic planning
├── CLAUDE.md                      # Engineering rules and standards
├── docs/                          # All documentation
│   ├── epics.md                   # Epic definitions
│   ├── PRD.md                     # Product requirements
│   ├── solution-architecture.md   # Architecture documentation
│   └── bmm-workflow-status.md     # Current sprint status
├── docs/stories/                  # User story specifications
└── docs/archive/                  # Sprint summaries, QA reports, retrospectives
```

### Application Repository (Submodule)
**Purpose:** All application code and tests
**URL:** https://github.com/memyselfmike/gao-mission-control

```
mission-control/                    # Submodule
├── src/                           # Application source code
├── tests/                         # Test suite
├── main.py                        # Application entry point
└── README.md                      # Developer documentation
```

See the [application repository](https://github.com/memyselfmike/gao-mission-control) for code and development documentation.

---

## Documentation

### For Users
- **[Product Backlog](PRODUCT-BACKLOG.md)** - Feature roadmap and epic planning
- **[Architecture](docs/solution-architecture.md)** - System design and technical overview

### For Developers
- **[Application README](mission-control/README.md)** - Developer setup and code documentation
- **[Engineering Rules](CLAUDE.md)** - Code standards and best practices
- **[Epic Definitions](docs/epics.md)** - High-level feature specifications
- **[User Stories](docs/stories/)** - Detailed implementation specifications

### For Project Managers
- **[BMM Workflow Status](docs/bmm-workflow-status.md)** - Current sprint and story status
- **[Sprint Archives](docs/archive/sprint-summaries/)** - Sprint planning and retrospectives

---

## Core Agents

### Chief of Staff (Alex)
Your primary interface. Maintains context, routes to specialists, works proactively.

**Capabilities:**
- Daily check-ins and planning
- Strategic discussions (ad-hoc or scheduled)
- Goal tracking and monitoring
- Executive orchestration

### Operator (Taylor) ✅ *Complete*
**Domain:** Daily execution and productivity
- Daily planning (Eisenhower Matrix, time blocking)
- Weekly prep and review workflows
- Task pattern learning (types, productivity trends)
- Autonomous task reminders

### Planner (Quinn) 🔜 *Next*
**Domain:** Quarterly planning and goal tracking
- 90-day objectives (Rocks framework)
- Progress tracking and milestones
- Goal health monitoring
- Quarterly reviews

### Strategist (Jordan) 🔜 *Planned*
**Domain:** Long-term vision and strategic clarity
- 10-year vision, 3-year picture, 1-year goals
- Core values definition
- Strategic opportunity evaluation

### Analyst (Sam) 🔜 *Planned*
**Domain:** Business intelligence and metrics
- Metrics tracking and dashboards
- Trend analysis and insights
- Performance reporting

### Researcher (Morgan) 🔜 *Planned*
**Domain:** Deep research and documentation
- Comprehensive research on topics
- Competitive analysis
- Market research with citations

---

## Development Status

**Current Status:** Post-MVP (183/318-388 story points delivered - 47-58% complete)

### Completed EPICs
- ✅ **EPIC-1:** Autonomous Agent Framework (40 points)
- ✅ **EPIC-2:** Persistent Memory System (16 points)
- ✅ **EPIC-3:** Operator Agent (44 points)
- ✅ **EPIC-5R:** Architectural Refactoring (83 points)

### In Progress
- 🔄 **None** - Awaiting next epic selection

### Next Up
- 🔜 **EPIC-4:** Planner Agent (35-45 points)
- 🔜 **EPIC-5:** Strategist Agent (30-40 points)
- 🔜 **EPIC-6:** Analyst Agent (25-35 points)
- 🔜 **EPIC-7:** Agent Designer (30-40 points)

See [PRODUCT-BACKLOG.md](PRODUCT-BACKLOG.md) for complete roadmap.

---

## Architecture

Mission Control uses **Hexagonal/Clean Architecture**:

```
┌─────────────────────────────────────┐
│   USER (CEO/Entrepreneur)           │
└────────────┬────────────────────────┘
             │
             ↓
┌─────────────────────────────────────┐
│   Chief of Staff (Main Agent)       │
│   - Persistent conversation          │
│   - Delegates to specialists         │
│   - Autonomous behaviors             │
└────┬────┬────┬────┬────┬────────────┘
     │    │    │    │    │
     ↓    ↓    ↓    ↓    ↓
┌──────────────────────────────────────┐
│       Specialist Subagents           │
│  Operator  Planner  Strategist       │
│  Analyst   Researcher  [Custom]      │
└──────────────────────────────────────┘
```

**Technology Stack:**
- **Claude Agent SDK** - Autonomous behaviors, subagent spawning, MCP integration
- **BMAD Method Patterns** - Structured workflows and templates
- **Python 3.13+** - Modern async/await patterns
- **Hexagonal Architecture** - Clean separation of concerns
- **Repository Pattern** - All storage access abstracted
- **Rich** - Beautiful CLI interface

---

## Example Interactions

### Morning Planning
```
You: Morning Alex, what's on deck?

Alex: Good morning! You have 3 meetings today. Based on your Q4 Rock "Launch website"
(due in 3 weeks, 45% complete), I suggest blocking 10-12 for focused work on that.

Want me to bring in Taylor (Operator) for detailed planning?
```

### Strategic Thinking
```
You: I'm thinking about hiring a VP of Sales. Thoughts?

Alex: That's significant. Few questions: What's driving this need? Have you defined
what "right" looks like? Timeline?

This feels like a good candidate for a deeper strategy session. Want me to bring in
our Strategist to work through the role definition?
```

### Goal Tracking
```
You: How am I tracking on Q4 goals?

Alex: [Reads goals data]

You have 5 Rocks:
✅ Website launch - 45% (ON TRACK)
⚠️ Enterprise deals - 30% (OFF TRACK - only 3/10 closed)
✅ V2.0 features - 70% (AHEAD!)

Concern: Enterprise deals Rock needs attention. Want to analyze pipeline with our Analyst?
```

---

## Privacy & Data

- **100% Local Storage** - All data stored on your machine
- **No Cloud Sync** - No telemetry or external tracking
- **API Calls Only for AI** - Only Claude API for inference
- **Human-Readable Formats** - JSON/JSONL for all data
- **You Own Your Data** - Export, backup, delete anytime

---

## Contributing

We welcome contributions! Here's how:

1. **Fork the application repository** (the submodule)
2. **Follow engineering standards** in [CLAUDE.md](CLAUDE.md)
3. **Write tests** (85%+ coverage required)
4. **Submit a pull request**

See the [application repository README](mission-control/README.md) for development setup.

---

## Project Management

Mission Control uses the **BMAD Method** for development:

- **EPICs** - High-level features (defined in [docs/epics.md](docs/epics.md))
- **Stories** - Detailed specifications (in [docs/stories/](docs/stories/))
- **Sprints** - 1-2 week iterations
- **Workflow Status** - Tracked in [docs/bmm-workflow-status.md](docs/bmm-workflow-status.md)

All project artifacts are stored in this parent repository for visibility and historical record.

---

## Roadmap

### Phase 1: Foundation (Complete ✅)
- Claude Agent SDK integration
- Core autonomous behaviors
- Operator Agent (daily execution)
- Persistent memory system

### Phase 2: Planning & Strategy (Next 🔜)
- Planner Agent (quarterly goals)
- Strategist Agent (vision & strategy)
- Advanced workflows

### Phase 3: Intelligence (Planned)
- Analyst Agent (business metrics)
- Researcher Agent (deep research)
- Pattern recognition enhancements

### Phase 4: Extensibility (Future)
- Agent Designer (create custom agents)
- Workflow marketplace
- Integration ecosystem

---

## Support & Community

- **Documentation:** [docs/](docs/)
- **Issues:** [GitHub Issues](https://github.com/memyselfmike/mission-control/issues)
- **Discussions:** [GitHub Discussions](https://github.com/memyselfmike/mission-control/discussions)
- **Application Code:** [Submodule Repository](https://github.com/memyselfmike/gao-mission-control)

---

## License

[To be determined]

---

## Acknowledgments

- **Claude Agent SDK** by Anthropic - Foundation for autonomous agents
- **BMAD Method** by sij-ai - Workflow patterns and organizational wisdom
- **Community Contributors** - Everyone who helps build and improve Mission Control

---

<div align="center">

**Built with ❤️ using Claude Agent SDK**

[Get Started](#quick-start) • [Documentation](docs/) • [Application Code](mission-control/)

</div>
