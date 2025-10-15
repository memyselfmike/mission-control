# Mission Control
## Autonomous AI-Powered Executive Team

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Claude Agent SDK](https://img.shields.io/badge/Claude%20Agent%20SDK-latest-green.svg)](https://docs.claude.com/en/api/agent-sdk)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Overview

Mission Control is an **autonomous AI-powered executive team** that works FOR you, not just responds TO you. Built on the Claude Agent SDK with BMAD Method patterns, it provides structured accountability, ad-hoc strategic thinking, proactive intelligence, and persistent memory.

### Key Features

- 🤖 **Autonomous Agents** - Proactively monitor, analyze, and surface insights
- 💾 **Persistent Memory** - Context builds across sessions, agents learn your preferences
- 📊 **Proactive Intelligence** - Surface insights without being asked
- 📅 **Scheduled Operations** - Daily briefings, weekly reviews, quarterly planning
- 🎯 **Specialist Subagents** - Delegate to experts (Strategist, Planner, Operator, Analyst, Researcher)
- 🔧 **Extensible** - Easy to add new agents, workflows, and integrations
- 🌐 **MCP Integration** - Connect external tools (Playwright, Calendar, Metrics APIs)

---

## Quick Start

### Prerequisites

- Python 3.13+
- uv package manager
- Anthropic API key OR Claude Code authentication

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/mission-control.git
cd mission-control

# Install dependencies
uv sync

# Configure authentication
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Run
python main.py
```

**First conversation:**
```
You: Hello, who are you?

Alex (Chief of Staff): I'm Alex, your Chief of Staff. I'm here to help with everything from daily planning to strategic thinking. I have a team of specialists ready to help...

You: I need help planning my quarter

Alex: Perfect! I'm bringing in Quinn, our Planner specialist...
[Delegates to Planner subagent]
```

---

## Documentation

### For Users
- **[Installation Guide](docs/TECHNICAL-SETUP-GUIDE.md)** - Step-by-step setup
- **[Architecture Overview](docs/mission-control-architecture.md)** - System design

### For Developers
- **[Development Guide](docs/AGENT-DEVELOPMENT-GUIDE.md)** - Building custom agents
- **[Implementation Summary](docs/IMPLEMENTATION-SUMMARY.md)** - Complete technical overview
- **[Product Backlog](PRODUCT-BACKLOG.md)** - Feature roadmap

### For Project Managers
- **[EPICs](epics/)** - High-level feature specifications
- **[Stories](stories/)** - Detailed implementation tasks

---

## Architecture

Mission Control uses a **hybrid architecture**:

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
│  Strategist  Planner  Operator       │
│  Analyst     Researcher  [Custom]    │
└──────────────────────────────────────┘
```

**Technology Stack:**
- **Claude Agent SDK** - Autonomous behaviors, subagent spawning, MCP integration
- **BMAD Method Patterns** - Structured workflows and templates
- **Python 3.13+** - Modern async/await patterns
- **Rich** - Beautiful CLI interface

---

## Core Agents

### Chief of Staff - Alex
Your primary interface. Maintains context, routes to specialists, works proactively.

**Capabilities:**
- Daily check-ins and planning
- Strategic discussions (ad-hoc or scheduled)
- Goal tracking and monitoring
- Executive orchestration

### Strategist
**Domain:** Long-term vision and strategic clarity
- 10-year vision, 3-year picture, 1-year goals
- Core values definition
- Strategic opportunity evaluation

### Planner
**Domain:** Quarterly planning and goal tracking
- 90-day objectives (Rocks)
- Progress tracking and milestones
- Quarterly reviews

### Operator
**Domain:** Daily execution and productivity
- Daily planning (Eisenhower Matrix)
- Task prioritization and time blocking
- Weekly prep and review

### Analyst
**Domain:** Business intelligence and metrics
- Metrics tracking and dashboards
- Trend analysis and insights
- Performance reporting

### Researcher
**Domain:** Deep research and documentation
- Comprehensive research on topics
- Competitive analysis
- Market research with citations

---

## Example Use Cases

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

Alex: [Reads data/goals/2025-Q4-rocks.json]

You have 5 Rocks:
✅ Website launch - 45% (ON TRACK)
⚠️ Enterprise deals - 30% (OFF TRACK - only 3/10 closed)
✅ V2.0 features - 70% (AHEAD!)

Concern: Enterprise deals Rock needs attention. Want to analyze pipeline with our Analyst?
```

---

## Autonomous Behaviors

Mission Control agents work proactively through:

### 1. Scheduled Tasks
- Daily briefings (6:30 AM configurable)
- Weekly reviews (Monday morning)
- Quarterly planning reminders

### 2. Event Monitors
- Goal goes off-track → Alert
- Deadline approaching → Reminder
- Pattern detected → Insight

### 3. Hooks
- After agent response → Log actions, check goals
- After file edit → Detect patterns
- On notification → Sound/alert

### 4. Pattern Recognition
- Track common request types
- Learn preferred times of day
- Identify recurring challenges
- Surface insights proactively

---

## Development Status

🚧 **Current Status:** Sprint 0 - Foundation (Weeks 1-2)

**Completed:**
- ✅ Architecture document (v2.0 - SDK hybrid)
- ✅ Technical setup guide
- ✅ Agent development guide
- ✅ EPIC-1 story breakdown (6 stories, 31 points)
- ✅ Implementation summary

**In Progress:**
- 🔄 STORY-1.1: Install Claude Agent SDK
- 🔄 STORY-1.2: Project structure
- 🔄 STORY-1.3: Conversation loop
- 🔄 STORY-1.4: Subagent definitions
- 🔄 STORY-1.5: Hooks system
- 🔄 STORY-1.6: Chief of Staff output style

**Next Up:**
- Sprint 1: Persistent memory system
- Sprint 2: Autonomous behaviors
- Sprint 3: Workflows and templates
- Sprint 4: MCP integrations

See [PRODUCT-BACKLOG.md](PRODUCT-BACKLOG.md) for full roadmap.

---

## Project Structure

```
mission-control/
├── .claude/                    # Claude Code configuration
│   ├── settings.json           # Hooks, MCP, permissions
│   ├── output-styles/          # Agent personas
│   ├── hooks/                  # Autonomous scripts
│   └── agents/                 # Optional agent definitions
│
├── src/                        # Source code
│   ├── agent_definitions.py    # Subagent configs
│   ├── cli_interface.py        # Rich CLI
│   ├── scheduler.py            # Scheduled tasks
│   └── event_monitors.py       # Event-driven monitors
│
├── data/                       # Business data (gitignored)
│   ├── memory/                 # Persistent context
│   ├── goals/                  # Goals and Rocks
│   ├── metrics/                # Business metrics
│   └── notes/                  # Strategic notes
│
├── workflows/                  # BMAD-style templates
├── templates/                  # Document templates
├── output/                     # Generated documents (gitignored)
│
├── docs/                       # Documentation
│   ├── mission-control-architecture.md
│   ├── TECHNICAL-SETUP-GUIDE.md
│   ├── AGENT-DEVELOPMENT-GUIDE.md
│   └── IMPLEMENTATION-SUMMARY.md
│
├── epics/                      # Epic specifications
├── stories/                    # Story specifications
│
├── main.py                     # Entry point
├── pyproject.toml              # Dependencies
└── .env                        # Environment (gitignored)
```

---

## Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

### Development Setup

```bash
# Install dev dependencies
uv add --dev pytest pytest-asyncio black pylint mypy

# Run tests
uv run pytest

# Format code
uv run black src/ tests/

# Lint
uv run pylint src/
```

---

## Roadmap

### Phase 1: Foundation (Q4 2025)
- ✅ Claude Agent SDK integration
- ✅ Core subagents (5 specialists)
- ✅ Basic hooks and autonomous behaviors
- 🔄 Persistent memory system

### Phase 2: Workflows (Q1 2026)
- Structured planning workflows
- Document templates
- Workflow automation
- Advanced pattern recognition

### Phase 3: Integrations (Q2 2026)
- Calendar sync (Google, Outlook)
- Metrics APIs (Stripe, QuickBooks, Analytics)
- Email integration
- Slack/Teams notifications

### Phase 4: Scale (Q3 2026)
- Multi-user support
- Team collaboration features
- Custom agent marketplace
- Mobile interface

---

## FAQ

### Q: How is this different from ChatGPT or Claude?
**A:** Mission Control is not just a chatbot. It's an autonomous system that:
- Works proactively (not just reactively)
- Maintains persistent memory across sessions
- Spawns specialist subagents for complex work
- Integrates with external tools and APIs
- Operates on schedules and events

### Q: What's the cost?
**A:** Mission Control uses the Claude API. Costs depend on usage:
- Haiku: ~$0.25 per million input tokens (testing)
- Sonnet: ~$3 per million input tokens (recommended)
- Opus: ~$15 per million input tokens (maximum capability)

Typical usage: $20-50/month for active daily use

### Q: Can I self-host this?
**A:** Yes! Mission Control runs entirely on your machine. Data stays local. Only API calls go to Anthropic.

### Q: Do I need coding knowledge?
**A:** For basic use: No. Just install and interact naturally.
For customization: Some Python knowledge helps but detailed guides are provided.

### Q: What about my data privacy?
**A:** All data stored locally in `data/` folder. You have full control. Only your prompts and agent responses go to Anthropic's API (covered by their privacy policy).

---

## License

[Your License Choice - e.g., MIT]

---

## Acknowledgments

- **Claude Agent SDK** by Anthropic - Foundation for autonomous agents
- **BMAD Method** by sij-ai - Workflow patterns and organizational wisdom
- **Kenneth Liao** - Tutorial and examples that inspired this implementation
- **Community Contributors** - Everyone who helps build and improve Mission Control

---

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/mission-control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mission-control/discussions)
- **Email**: support@yourdomain.com

---

## Stay Connected

- **Website**: [missioncontrol.ai](#)
- **Twitter**: [@MissionControlAI](#)
- **Discord**: [Join Community](#)
- **Blog**: [blog.missioncontrol.ai](#)

---

<div align="center">

**Built with ❤️ using Claude Agent SDK**

[Get Started](docs/TECHNICAL-SETUP-GUIDE.md) • [Documentation](docs/) • [Contribute](#contributing)

</div>
