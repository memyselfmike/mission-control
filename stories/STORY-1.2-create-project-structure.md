# STORY-1.2: Create Project Structure and Folder Organization

**Epic:** EPIC-1 - Autonomous Agent Framework
**Status:** Not Started
**Priority:** P0 (Critical)
**Story Points:** 2
**Assignee:** TBD

---

## User Story

As a **developer**
I want to **create the standard project folder structure**
So that **the codebase is organized and follows best practices**

---

## Acceptance Criteria

- [ ] All core directories created as per architecture document
- [ ] .claude/ folder structure created for Claude Code configuration
- [ ] data/ folders for persistent storage created
- [ ] src/ folder for source code created
- [ ] templates/ and workflows/ folders created
- [ ] .gitignore configured properly
- [ ] README.md created with project overview
- [ ] All folders have appropriate placeholder files or .gitkeep

---

## Technical Details

### Required Folder Structure

```
mission-control/
│
├── .claude/                       # Claude Code configuration
│   ├── settings.json              # Hooks, MCP, permissions
│   ├── output-styles/             # Agent personas
│   │   └── .gitkeep
│   ├── hooks/                     # Autonomous behavior scripts
│   │   └── .gitkeep
│   └── agents/                    # Optional: File-based agent definitions
│       └── .gitkeep
│
├── src/                           # Source code
│   ├── __init__.py
│   ├── agent_definitions.py       # Subagent configs (placeholder)
│   ├── cli_interface.py           # Rich CLI display (placeholder)
│   ├── scheduler.py               # Time-based scheduler (placeholder)
│   └── event_monitors.py          # Event-driven monitors (placeholder)
│
├── data/                          # Business data storage
│   ├── memory/                    # Agent persistent memory
│   │   ├── interaction_logs/
│   │   │   └── .gitkeep
│   │   └── .gitkeep
│   ├── goals/
│   │   ├── completed/
│   │   │   └── .gitkeep
│   │   └── .gitkeep
│   ├── metrics/
│   │   ├── dashboards/
│   │   │   └── .gitkeep
│   │   └── .gitkeep
│   └── notes/
│       ├── strategic-thoughts/
│       │   └── .gitkeep
│       ├── meeting-notes/
│       │   └── .gitkeep
│       └── ideas/
│           └── .gitkeep
│
├── workflows/                     # BMAD-style workflow templates
│   ├── daily-focus/
│   │   └── .gitkeep
│   ├── weekly-review/
│   │   └── .gitkeep
│   ├── quarterly-planning/
│   │   └── .gitkeep
│   └── goal-setting/
│       └── .gitkeep
│
├── templates/                     # Document templates
│   └── .gitkeep
│
├── output/                        # Generated documents
│   ├── daily-plans/
│   │   └── .gitkeep
│   ├── weekly-reviews/
│   │   └── .gitkeep
│   ├── quarterly-plans/
│   │   └── .gitkeep
│   └── reports/
│       └── .gitkeep
│
├── tests/                         # Test suite
│   ├── __init__.py
│   ├── test_agent_definitions.py  # (placeholder)
│   ├── test_workflows.py          # (placeholder)
│   └── test_integration.py        # (placeholder)
│
├── docs/                          # Documentation (already exists)
├── epics/                         # Epic files (already exists)
├── stories/                       # Story files (already exists)
│
├── .env                           # Environment variables (gitignored)
├── .env.example                   # Template for .env
├── .gitignore
├── main.py                        # Entry point (placeholder)
├── pyproject.toml                 # Dependencies (from STORY-1.1)
├── README.md
└── LICENSE
```

---

## Implementation Tasks

### 1. Create Directory Structure

```bash
# Create .claude structure
mkdir -p .claude/output-styles
mkdir -p .claude/hooks
mkdir -p .claude/agents

# Create source code structure
mkdir -p src
mkdir -p tests

# Create data storage structure
mkdir -p data/memory/interaction_logs
mkdir -p data/goals/completed
mkdir -p data/metrics/dashboards
mkdir -p data/notes/strategic-thoughts
mkdir -p data/notes/meeting-notes
mkdir -p data/notes/ideas

# Create workflow structure
mkdir -p workflows/daily-focus
mkdir -p workflows/weekly-review
mkdir -p workflows/quarterly-planning
mkdir -p workflows/goal-setting

# Create templates
mkdir -p templates

# Create output directories
mkdir -p output/daily-plans
mkdir -p output/weekly-reviews
mkdir -p output/quarterly-plans
mkdir -p output/reports
```

### 2. Create .gitignore

```
# .gitignore

# Environment
.env
*.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Data directories (sensitive)
data/memory/
data/goals/
data/metrics/
data/notes/

# Generated output
output/

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Temporary
tmp/
temp/
```

### 3. Create .env.example

```bash
# .env.example

# Anthropic API Key (get from https://console.anthropic.com)
# OR authenticate via Claude Code CLI: claude-code login
ANTHROPIC_API_KEY=sk-ant-your-key-here

# User Configuration
USER_NAME=Your Name
USER_TIMEZONE=America/New_York

# System Configuration
LOG_LEVEL=INFO
ENABLE_SCHEDULER=true
ENABLE_EVENT_MONITORS=true
```

### 4. Create Placeholder Files

**src/__init__.py:**
```python
"""Mission Control - Autonomous AI-Powered Executive Team"""

__version__ = "0.1.0"
```

**src/agent_definitions.py:**
```python
"""
Agent definitions for subagents.
This module will contain AgentDefinition configurations for all specialist agents.
"""

from claude_agent_sdk import AgentDefinition

# TODO: Implement agent definitions in later stories
agents = {}
```

**src/cli_interface.py:**
```python
"""
CLI interface using Rich for formatted output.
"""

from rich.console import Console

# TODO: Implement CLI interface in later stories

def print_message(message_type: str, content: str):
    """Print formatted message to console"""
    console = Console()
    # Implementation in later story
    pass
```

**src/scheduler.py:**
```python
"""
Time-based task scheduler for autonomous behaviors.
"""

import schedule

# TODO: Implement scheduler in later stories
```

**src/event_monitors.py:**
```python
"""
Event-driven monitors for autonomous behaviors.
"""

from watchdog.observers import Observer

# TODO: Implement event monitors in later stories
```

**main.py:**
```python
"""
Mission Control - Main Entry Point
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich.console import Console
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    console = Console()
    console.print("[bold cyan]Mission Control[/bold cyan]")
    console.print("Initializing...")

    # TODO: Implement full main loop in later stories

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Update README.md

```markdown
# Mission Control

**Autonomous AI-Powered Executive Team**

Mission Control is an autonomous AI-powered executive team built on Claude Agent SDK that provides structured accountability, ad-hoc strategic thinking, proactive intelligence, and persistent memory.

## Features

- 🤖 **Autonomous Agents**: Agents that work proactively, not just reactively
- 💾 **Persistent Memory**: Context builds across sessions
- 📊 **Proactive Insights**: Agents surface insights without being asked
- 📅 **Scheduled Operations**: Daily briefings, weekly reviews, quarterly planning
- 🔧 **Extensible**: Easy to add new agents and workflows

## Technology

- **Claude Agent SDK** (Python): Autonomous behaviors, subagent spawning, MCP integration
- **BMAD Method Patterns**: Structured workflows and templates

## Prerequisites

- Python 3.13+
- uv package manager
- Anthropic API key OR Claude Code authentication

## Quick Start

See [docs/INSTALLATION.md](docs/INSTALLATION.md) for detailed setup instructions.

```bash
# Install dependencies
uv sync

# Configure
cp .env.example .env
# Edit .env with your API key

# Run
python main.py
```

## Project Structure

- `.claude/` - Claude Code configuration (output styles, hooks, agents)
- `src/` - Source code
- `data/` - Persistent business data and agent memory
- `workflows/` - Workflow templates
- `templates/` - Document templates
- `output/` - Generated documents
- `docs/` - Documentation
- `epics/` - Epic specifications
- `stories/` - Story specifications

## Documentation

- [Architecture](docs/mission-control-architecture.md)
- [Installation Guide](docs/INSTALLATION.md)
- [Agent Development Guide](docs/AGENT-DEVELOPMENT-GUIDE.md)
- [Technical Setup](docs/TECHNICAL-SETUP-GUIDE.md)

## Development Status

🚧 **In Development** - See [PRODUCT-BACKLOG.md](PRODUCT-BACKLOG.md) for roadmap

## License

[Your License Here]
```

---

## Definition of Done

- [ ] All directories created
- [ ] .gitignore configured
- [ ] .env.example created
- [ ] Placeholder Python files created with docstrings
- [ ] main.py entry point created
- [ ] README.md updated
- [ ] All sensitive directories added to .gitignore
- [ ] .gitkeep files added where needed to preserve empty directories
- [ ] Structure validated against architecture document
- [ ] Committed to repository

---

## Testing Steps

1. Run `git status` - verify gitignore working correctly
2. Verify data/ and output/ directories not tracked
3. Verify placeholder files can be imported: `python -c "import src; print(src.__version__)"`
4. Verify README renders correctly on GitHub
5. Verify all directories exist as expected

---

## Dependencies

- STORY-1.1 (SDK installation must be complete)

---

## Notes

- Keep placeholder files minimal but documented
- .gitkeep files ensure empty directories are tracked in git
- Sensitive data directories (data/, output/) should never be committed
- This structure follows the architecture document (docs/mission-control-architecture.md)
