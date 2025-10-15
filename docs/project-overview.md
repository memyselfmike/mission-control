# Mission Control System - Project Overview

**Generated:** 2025-10-14
**Project Type:** CLI Tool - Interactive Python Application
**Status:** In Development (Sprint 0 - Foundation)

---

## Executive Summary

Mission Control is an **autonomous AI-powered executive team** built using the Claude Agent SDK and BMAD Method patterns. It provides structured accountability, ad-hoc strategic thinking, proactive intelligence, and persistent memory through a Rich-formatted CLI interface.

**Key Differentiator:** Autonomous agents that work FOR you, not just respond TO you.

---

## Project Classification

**Repository Type:** Monolith
**Primary Language:** Python 3.13+
**Architecture Pattern:** Interactive CLI with Autonomous Agent System
**Project Level:** 4 (Enterprise scale - multiple products/systems)

---

## Technology Stack Summary

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Core** |
| Language | Python | 3.13+ | Modern async/await support |
| Framework | Claude Agent SDK | >=0.1.0 | Autonomous agent behaviors |
| CLI Interface | Rich | >=13.0.0 | Terminal formatting |
| **Data & Config** |
| Configuration | python-dotenv | >=1.0.0 | Environment management |
| Validation | Pydantic | >=2.0.0 | Data validation |
| **Automation** |
| Scheduling | schedule | >=1.2.0 | Time-based tasks |
| File Watching | watchdog | >=3.0.0 | File system events |
| Async Support | nest-asyncio | >=1.6.0 | Nested event loops |
| **Development** |
| Package Manager | uv | latest | Fast Python packaging |
| Build System | hatchling | latest | Modern build backend |
| Code Quality | black, pylint | latest | Formatting & linting |

---

## Architecture Type

**Interactive CLI (Python)** - `cli-python-interactive`

```
User (CEO/Entrepreneur)
         ↓
Chief of Staff (Main Agent)
  - Persistent conversation
  - Delegates to specialists
  - Autonomous behaviors
         ↓
┌────────────────────────────────────┐
│    Specialist Subagents            │
│  Strategist | Planner | Operator   │
│  Analyst    | Researcher           │
└────────────────────────────────────┘
```

**Hybrid Design:**
- **Claude Agent SDK**: Autonomous behaviors, subagent spawning, MCP integration
- **BMAD Method Patterns**: Workflow structure, templates, process frameworks

---

## Core Features

- 🤖 **Autonomous Agents** - Proactively monitor, analyze, surface insights
- 💾 **Persistent Memory** - Context builds across sessions
- 📊 **Proactive Intelligence** - Surface insights without being asked
- 📅 **Scheduled Operations** - Daily briefings, weekly reviews, quarterly planning
- 🎯 **Specialist Subagents** - Delegate to experts (5 specialists)
- 🔧 **Extensible** - Easy to add agents, workflows, integrations
- 🌐 **MCP Integration** - Connect external tools (Playwright, APIs)

---

## Project Structure

### Core Application
- **Entry Point:** `main.py`
- **Source Code:** `src/agent_definitions.py`
- **Configuration:** `.claude/` directory (hooks, output styles, agents)

### Data Management
- **Persistent Data:** `data/` (memory, goals, metrics, notes)
- **Generated Outputs:** `output/` (plans, reports, reviews)
- **Workflows:** `workflows/` (BMAD-style templates)

### Documentation
- **Project Docs:** Root-level MD files (README, ARCHITECTURE, etc.)
- **Planning:** `../stories/`, `../docs/legacy-planning-files/epics/`
- **Reference:** `../bmad/`, `../claude-agent-sdk-intro/`

---

## Current Implementation Status

### ✅ Completed (Sprint 0 - Weeks 1-2)
- Architecture document (v2.0 - SDK hybrid approach)
- Technical setup guide
- Agent development guide
- EPIC-1 story breakdown (6 stories, 31 points)
- Implementation summary
- Project structure setup

### 🔄 In Progress
- STORY-1.1: Install Claude Agent SDK
- STORY-1.2: Project structure
- STORY-1.3: Conversation loop
- STORY-1.4: Subagent definitions
- STORY-1.5: Hooks system
- STORY-1.6: Chief of Staff output style

### 📋 Next Up
- Sprint 1: Persistent memory system
- Sprint 2: Autonomous behaviors
- Sprint 3: Workflows and templates
- Sprint 4: MCP integrations

---

## Quick Reference

### Entry Points
- **Main Application:** `main.py`
- **Tests:** `test_basic.py`, `test_installation.py`, `test_mission_control.py`

### Key Directories
- **Source:** `src/`
- **Configuration:** `.claude/`
- **Data:** `data/` (gitignored)
- **Workflows:** `workflows/`
- **Output:** `output/` (gitignored)

### Configuration Files
- **Project:** `pyproject.toml`
- **Environment:** `.env` (from `.env.example`)
- **Dependencies:** `uv.lock`

---

## Development Workflow

1. **Setup:** Install Python 3.13+, uv package manager
2. **Install:** `uv sync`
3. **Configure:** Copy `.env.example` to `.env`, add API key
4. **Run:** `python main.py`
5. **Test:** `pytest` or run individual test files

---

## External References

### Within Project
- **BMAD Framework:** `../bmad/` (methodology reference)
- **SDK Examples:** `../claude-agent-sdk-intro/` (learning materials)
- **Legacy Planning:** `../docs/legacy-planning-files/` (original epics & guides)
- **Current Stories:** `../stories/` (EPIC-1 implementation stories)

### Documentation Links
- [Project README](../mission-control-system/README.md)
- [Architecture V2](../mission-control-system/ARCHITECTURE-V2.md)
- [Installation Guide](../mission-control-system/INSTALLATION.md)
- [Quick Start](../mission-control-system/QUICKSTART.md)

---

## Key Insights for AI-Assisted Development

### When Planning Features
1. **Brownfield Context:** This project is in early development but has clear architecture
2. **Reference the source tree:** [source-tree-analysis.md](./source-tree-analysis.md)
3. **Check existing docs:** 25+ documentation files exist (see existing documentation inventory)
4. **Follow patterns:** Hybrid SDK + BMAD approach

### For Implementation
1. **Entry point:** main.py launches the CLI
2. **Subagents:** Defined in src/agent_definitions.py
3. **Autonomous behaviors:** Implemented as hooks in .claude/hooks/
4. **Workflows:** Template-based in workflows/ directory

### For Testing
1. **Test files:** Root-level test_*.py files
2. **Test structure:** tests/ directory for organized test suites
3. **Verification:** test_installation.py validates setup

---

## Next Steps for Development

1. Complete EPIC-1 stories (autonomous agent framework)
2. Implement persistent memory system (Sprint 1)
3. Build autonomous behaviors (Sprint 2)
4. Add workflow templates (Sprint 3)
5. Integrate MCP tools (Sprint 4)

---

**For detailed architecture:** See [Architecture V2](../mission-control-system/ARCHITECTURE-V2.md)
**For source tree:** See [Source Tree Analysis](./source-tree-analysis.md)
**For getting started:** See [Quick Start Guide](../mission-control-system/QUICKSTART.md)
