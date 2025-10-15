# Mission Control System - Documentation Index

**Project:** Mission Control
**Type:** CLI Tool (Interactive Python Application)
**Architecture:** cli-python-interactive
**Status:** In Development (Sprint 0)
**Generated:** 2025-10-14

---

## Quick Reference

- **Type:** Monolith (with reference materials)
- **Primary Language:** Python 3.13+
- **Architecture:** Interactive CLI with Autonomous Agent System
- **Entry Point:** `mission-control-system/main.py`
- **Package Manager:** uv (ultrafast Python)

---

## Getting Started

1. **New to the project?** Start with [Project Overview](./project-overview.md)
2. **Want to install?** See [Installation Guide](../mission-control-system/INSTALLATION.md)
3. **Quick start?** Check [Quick Start Guide](../mission-control-system/QUICKSTART.md)
4. **Understand the architecture?** Read [Architecture V2](../mission-control-system/ARCHITECTURE-V2.md)

---

## Generated Documentation

### Core Project Documentation

- **[Project Overview](./project-overview.md)** - Executive summary, tech stack, current status
- **[Source Tree Analysis](./source-tree-analysis.md)** - Annotated directory structure with explanations
- **[Workflow Status](./bmm-workflow-status.md)** - BMM workflow planning and progress tracking

### Reference: Project Root Documentation

These documents are located in `../mission-control-system/`:

- **[README.md](../mission-control-system/README.md)** - Main project README
- **[ARCHITECTURE-V2.md](../mission-control-system/ARCHITECTURE-V2.md)** - Complete architecture specification
- **[INSTALLATION.md](../mission-control-system/INSTALLATION.md)** - Installation instructions
- **[QUICKSTART.md](../mission-control-system/QUICKSTART.md)** - Quick start guide
- **[HOW-TO-ACTIVATE.md](../mission-control-system/HOW-TO-ACTIVATE.md)** - Activation instructions
- **[IMPLEMENTATION-NOTES.md](../mission-control-system/IMPLEMENTATION-NOTES.md)** - Implementation details
- **[EPIC-1-COMPLETE.md](../mission-control-system/EPIC-1-COMPLETE.md)** - EPIC-1 completion status
- **[FIXES-APPLIED.md](../mission-control-system/FIXES-APPLIED.md)** - Bug fixes log
- **[FINAL-IMPLEMENTATION.md](../mission-control-system/FINAL-IMPLEMENTATION.md)** - Final implementation summary

---

## Planning & Development

### Current Sprint Stories

Located in `../stories/`:

1. **[STORY-1.1](../stories/STORY-1.1-install-claude-agent-sdk.md)** - Install Claude Agent SDK
2. **[STORY-1.2](../stories/STORY-1.2-create-project-structure.md)** - Create Project Structure
3. **[STORY-1.3](../stories/STORY-1.3-implement-basic-conversation-loop.md)** - Implement Basic Conversation Loop
4. **[STORY-1.4](../stories/STORY-1.4-implement-subagent-definitions.md)** - Implement Subagent Definitions
5. **[STORY-1.5](../stories/STORY-1.5-implement-hooks-system.md)** - Implement Hooks System
6. **[STORY-1.6](../stories/STORY-1.6-create-chief-of-staff-output-style.md)** - Create Chief of Staff Output Style

### Legacy Planning Files

Located in `./legacy-planning-files/`:

**EPICs:**
- [EPIC-1: Autonomous Agent Framework](./legacy-planning-files/epics/EPIC-1-autonomous-agent-framework.md)
- [EPIC-2: Chief of Staff Orchestrator](./legacy-planning-files/epics/EPIC-2-chief-of-staff-orchestrator.md)
- [EPIC-3: Operator (Daily Execution)](./legacy-planning-files/epics/EPIC-3-operator-daily-execution.md)
- [EPIC-4: Planner (Goals & Projects)](./legacy-planning-files/epics/EPIC-4-planner-goals-projects.md)
- [EPIC-5: Strategist (Vision & Thinking)](./legacy-planning-files/epics/EPIC-5-strategist-vision-thinking.md)
- [EPIC-6: Analyst (Business Intelligence)](./legacy-planning-files/epics/EPIC-6-analyst-business-intelligence.md)
- [EPIC-7: Agent Designer (Meta)](./legacy-planning-files/epics/EPIC-7-agent-designer-meta.md)

**Technical Guides:**
- [Mission Control Architecture](./legacy-planning-files/mission-control-architecture.md)
- [Technical Setup Guide](./legacy-planning-files/TECHNICAL-SETUP-GUIDE.md)
- [Implementation Summary](./legacy-planning-files/IMPLEMENTATION-SUMMARY.md)
- [Agent Development Guide](./legacy-planning-files/AGENT-DEVELOPMENT-GUIDE.md)
- [Technical Decisions Template](./legacy-planning-files/technical-decisions-template.md)
- [BMAD Method Analysis](./legacy-planning-files/bmad-method-analysis.md)
- [Implementation Guide](./legacy-planning-files/implementation-guide.md)

**Strategic:**
- [Strategy on a Page (SOAP)](./strategy on a page/SOAP-overview.md)

---

## Reference Materials

These directories contain reference materials used to build Mission Control:

### BMAD Framework (`../bmad/`)
BMAD Method patterns and workflows used for project organization. This is a reference implementation, not part of the Mission Control application itself.

### Claude Agent SDK Examples (`../claude-agent-sdk-intro/`)
Tutorial and examples for learning the Claude Agent SDK. Used as learning materials during development.

**Key Files:**
- [SDK Tutorial README](../claude-agent-sdk-intro/README.md)
- Module examples: `0_querying.py` through `6_subagents.py`

---

## Project Files

### Configuration
- **pyproject.toml** - Python project dependencies and configuration
- **uv.lock** - Locked dependency versions
- **.env.example** - Environment variable template
- **.env** - Environment configuration (gitignored)

### Source Code
- **main.py** - Main CLI entry point
- **src/agent_definitions.py** - Subagent configurations

### Testing
- **test_basic.py** - Basic functionality tests
- **test_installation.py** - Installation verification
- **test_mission_control.py** - Full system integration tests
- **tests/** - Organized test suite directory

---

## Project Structure at a Glance

```
Mission Control/                    # Project root
├── mission-control-system/         # ← Main application
│   ├── main.py                    # Entry point
│   ├── src/                       # Source code
│   ├── .claude/                   # Agent configuration
│   ├── data/                      # Persistent data (gitignored)
│   ├── workflows/                 # BMAD workflows
│   └── ...
├── docs/                          # ← You are here
│   ├── index.md                   # This file
│   ├── project-overview.md        # Executive summary
│   ├── source-tree-analysis.md    # Directory structure
│   └── legacy-planning-files/     # Original planning docs
├── stories/                       # Current sprint stories
├── bmad/                          # BMAD Method (reference)
└── claude-agent-sdk-intro/        # SDK examples (reference)
```

---

## For AI-Assisted Development

### When Creating a PRD for New Features

1. **Start here:** Read [Project Overview](./project-overview.md)
2. **Understand structure:** Review [Source Tree Analysis](./source-tree-analysis.md)
3. **Check architecture:** See [Architecture V2](../mission-control-system/ARCHITECTURE-V2.md)
4. **Reference patterns:** Review [Agent Development Guide](./legacy-planning-files/AGENT-DEVELOPMENT-GUIDE.md)

### When Implementing Features

1. **Entry point:** `mission-control-system/main.py`
2. **Subagents:** `mission-control-system/src/agent_definitions.py`
3. **Hooks:** `mission-control-system/.claude/hooks/`
4. **Workflows:** `mission-control-system/workflows/`

### When Testing

1. **Run tests:** `pytest` from mission-control-system directory
2. **Verify setup:** `python test_installation.py`
3. **Integration test:** `python test_mission_control.py`

---

## Workflow Status Tracking

**Current Phase:** 1-Analysis
**Current Workflow:** document-project (Complete)
**Next Step:** plan-project

See [Workflow Status](./bmm-workflow-status.md) for complete workflow planning and progress.

---

## Additional Resources

### External Documentation
- **[Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk/python)** - Official SDK documentation
- **[MCP Servers Directory](https://github.com/modelcontextprotocol/servers)** - Available MCP integrations
- **[Anthropic API Docs](https://docs.anthropic.com)** - Claude API reference

### Project Management
- **Product Backlog:** See `../PRODUCT-BACKLOG.md`
- **Implementation Ready:** See `../IMPLEMENTATION-READY.md`
- **README:** See `../README.md`

---

## Quick Navigation

| I want to... | Go to |
|--------------|-------|
| Understand the project | [Project Overview](./project-overview.md) |
| See the code structure | [Source Tree Analysis](./source-tree-analysis.md) |
| Install the system | [Installation Guide](../mission-control-system/INSTALLATION.md) |
| Get started quickly | [Quick Start](../mission-control-system/QUICKSTART.md) |
| Learn the architecture | [Architecture V2](../mission-control-system/ARCHITECTURE-V2.md) |
| Build custom agents | [Agent Development Guide](./legacy-planning-files/AGENT-DEVELOPMENT-GUIDE.md) |
| Check progress | [Workflow Status](./bmm-workflow-status.md) |
| View current stories | [Stories](../stories/) |
| Review EPICs | [Legacy Planning Files](./legacy-planning-files/epics/) |

---

**Last Updated:** 2025-10-14
**Documentation Version:** 1.0
**Project Version:** 0.1.0 (In Development)

---

🚀 **Ready to build?** Start with the [Quick Start Guide](../mission-control-system/QUICKSTART.md)!
