# Mission Control System - Source Tree Analysis

**Generated:** 2025-10-14
**Project Type:** CLI Tool (Interactive Python Application)
**Architecture:** cli-python-interactive

---

## Directory Structure

```
mission-control-system/
│
├── .claude/                      # Claude Code configuration
│   ├── agents/                   # Agent definitions (file-based)
│   ├── commands/                 # Custom slash commands
│   ├── hooks/                    # Autonomous behavior scripts
│   └── output-styles/            # Agent persona definitions
│
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   └── agent_definitions.py      # Subagent configurations (core)
│
├── data/                         # Business data (gitignored)
│   ├── memory/                   # Persistent context
│   │   └── interaction_logs/     # Conversation history
│   ├── goals/                    # Goals and Rocks
│   │   └── completed/            # Completed goals archive
│   ├── metrics/                  # Business metrics
│   │   └── dashboards/           # Metric dashboards
│   └── notes/                    # Strategic notes
│       ├── ideas/                # Idea backlog
│       ├── meeting-notes/        # Meeting records
│       └── strategic-thoughts/   # Strategic thinking sessions
│
├── workflows/                    # BMAD-style workflow templates
│   ├── daily-focus/              # Daily planning workflows
│   ├── goal-setting/             # Goal setting workflows
│   ├── quarterly-planning/       # Quarterly planning workflows
│   └── weekly-review/            # Weekly review workflows
│
├── templates/                    # Document templates
│
├── output/                       # Generated documents (gitignored)
│   ├── daily-plans/              # Daily plan outputs
│   ├── quarterly-plans/          # Quarterly plan outputs
│   ├── reports/                  # Generated reports
│   └── weekly-reviews/           # Weekly review outputs
│
├── tests/                        # Test suite
│
├── docs/                         # Documentation (currently empty in mission-control-system)
├── epics/                        # Epic specifications (currently empty)
├── stories/                      # Story specifications (currently empty)
│
├── main.py                       # 🔹 Entry point - main CLI application
├── pyproject.toml                # Python project configuration
├── uv.lock                       # UV package lock file
│
├── test_basic.py                 # Basic functionality tests
├── test_installation.py          # Installation verification tests
├── test_mission_control.py       # Mission Control system tests
│
├── .env.example                  # Environment variable template
├── .env                          # Environment variables (gitignored)
│
├── README.md                     # Project overview
├── INSTALLATION.md               # Installation guide
├── QUICKSTART.md                 # Quick start guide
├── ARCHITECTURE-V2.md            # Architecture documentation
├── HOW-TO-ACTIVATE.md            # Activation instructions
├── IMPLEMENTATION-NOTES.md       # Implementation notes
├── EPIC-1-COMPLETE.md            # Epic 1 completion notes
├── FIXES-APPLIED.md              # Bug fixes documentation
└── FINAL-IMPLEMENTATION.md       # Final implementation details
```

---

## Critical Folders

### Core Application

**src/** - Source code directory
- `agent_definitions.py` - Defines 5 specialist subagents (Strategist, Planner, Operator, Analyst, Researcher)
- Entry point: `main.py` (root level)

### Configuration & Setup

**.claude/** - Claude Code integration
- `hooks/` - Autonomous behavior scripts (goal monitoring, pattern detection, action logging)
- `output-styles/` - Agent persona definitions (Chief of Staff, specialists)
- `agents/` - Optional file-based agent definitions
- `commands/` - Custom slash commands for CLI

### Data Management

**data/** - Persistent business data (gitignored)
- `memory/` - Persistent conversation context and learned preferences
- `goals/` - Goal tracking (quarterly rocks, objectives)
- `metrics/` - Business intelligence data
- `notes/` - Strategic notes and ideas

### Workflow System

**workflows/** - BMAD Method workflow templates
- `daily-focus/` - Daily planning and execution workflows
- `goal-setting/` - Goal definition workflows
- `quarterly-planning/` - 90-day planning workflows
- `weekly-review/` - Weekly retrospective workflows

### Output & Reports

**output/** - Generated documents (gitignored)
- `daily-plans/` - Daily planning outputs
- `quarterly-plans/` - Quarterly OKR/Rock outputs
- `reports/` - Analysis and insight reports
- `weekly-reviews/` - Weekly review outputs

### Testing

**tests/** - Test suite directory
- Root level test files: `test_basic.py`, `test_installation.py`, `test_mission_control.py`

---

## Entry Points

**Primary Entry Point:**
- `main.py` - Launches Mission Control CLI application

**Test Entry Points:**
- `test_basic.py` - Basic functionality verification
- `test_installation.py` - Installation and setup verification
- `test_mission_control.py` - Full system integration tests

---

## File Organization Patterns

### Python Modules
- Entry: `main.py` (root)
- Source: `src/` package
- Tests: `tests/` + root-level test files
- Config: `pyproject.toml`, `.env`

### Data Persistence
- User data: `data/` (gitignored, persistent across sessions)
- Generated outputs: `output/` (gitignored, can be recreated)
- Configuration: `.env` (gitignored, user-specific)

### Documentation
- Root-level: Project-wide docs (README, INSTALLATION, ARCHITECTURE)
- `docs/`: Additional documentation (currently empty, to be populated)
- `epics/`: Epic specifications (currently empty)
- `stories/`: Story specifications (currently empty)

---

## Technology Markers

**Language:** Python 3.13+
**Package Manager:** uv (ultrafast Python package installer)
**Framework:** Claude Agent SDK (autonomous agents)
**CLI Framework:** Rich (terminal formatting)
**Build System:** hatchling

---

## Integration Points

### Claude Code Integration
- `.claude/` directory contains all Claude Code configurations
- Hooks system for autonomous behaviors
- Output styles define agent personas
- MCP integration potential (not yet implemented)

### Data Flow
```
User → main.py → Agent Definitions → Subagents → Workflows → Output
                       ↓
                   Memory System (data/)
                       ↓
                   Persistent Context
```

---

## Notes

- **Reference Materials:** The project root contains `bmad/` and `claude-agent-sdk-intro/` directories which are reference materials, not part of the core application
- **Monolith Structure:** Single cohesive CLI application (not microservices or multi-part)
- **Autonomous Design:** System designed to work proactively through hooks and scheduled tasks
- **Data Privacy:** All user data stored locally in `data/` folder (gitignored)

---

**Next Steps:**
- Populate `docs/` folder with generated documentation
- Add epic and story files to respective folders
- Implement remaining autonomous behaviors in `.claude/hooks/`
