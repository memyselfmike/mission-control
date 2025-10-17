# Mission Control Architecture
## Autonomous AI-Powered Executive Team

**Version:** 2.0 (Claude Agent SDK Hybrid)
**Date:** 14 October 2025
**Status:** Design Document
**Reference:** See [BMAD Method Analysis](./bmad-method-analysis.md) for workflow patterns

---

## Overview

Mission Control is an autonomous AI-powered executive team built on **Claude Agent SDK** that provides structured accountability, ad-hoc strategic thinking, proactive intelligence, and persistent memory. Unlike traditional assistant tools, Mission Control agents actively surface insights, monitor goals, and extend their own capabilities.

### Key Capabilities

- **Structured Accountability**: Daily check-ins, weekly reviews, quarterly planning
- **Ad-hoc Conversations**: Always available for spontaneous strategic discussions
- **Proactive Intelligence**: Agents surface insights without being asked
- **Persistent Memory**: Context builds over time, agents learn preferences
- **Self-Extending**: System can create custom agents on-demand

### Technology Foundation

**Hybrid Architecture:**
- **Claude Agent SDK** (Python-based): Provides autonomous agent behaviors, subagent spawning, hooks, MCP integration
- **BMAD Method Patterns**: Provides workflow structure, templates, output formatting

This combines the autonomous capabilities of the SDK with the proven organizational patterns of BMAD Method.

---

## Design Principles

### 1. Autonomy Over Automation
Agents don't just respond—they proactively monitor, analyze, and surface insights. They work in the background and bring you what matters.

### 2. Context Persistence
Every conversation builds on the last. Agents remember your business context, preferences, and patterns. No need to re-explain.

### 3. Conversational + Structured
Natural language for ad-hoc discussions, but structured workflows for critical processes (planning, reviews, goal-setting).

### 4. Extensible by Design
The system can spawn new specialized agents on-demand for specific tasks (research, analysis, content creation).

### 5. Tool-Rich Environment
Agents have access to filesystem tools, web search, browser automation (Playwright), and can integrate external services via MCP.

---

## System Architecture

### High-Level Component View

```
┌─────────────────────────────────────────────────────────────┐
│                    USER (CEO/Entrepreneur)                   │
└───────────────────┬─────────────────────────────────────────┘
                    │ Natural Language
                    ↓
┌─────────────────────────────────────────────────────────────┐
│            CLAUDE AGENT SDK CLIENT (main.py)                 │
│  • ClaudeSDKClient with persistent conversation              │
│  • Loads .claude/ configuration                              │
│  • Manages subagent spawning via Task tool                   │
└─────────────┬───────────────────────────────────────────────┘
              │
              ↓
┌─────────────────────────────────────────────────────────────┐
│              CHIEF OF STAFF (Main Agent)                     │
│  • Output Style defines persona                              │
│  • Routes to specialist subagents                            │
│  • Maintains conversation context                            │
│  • Triggers autonomous behaviors via hooks                   │
└─────┬─────────┬──────────┬──────────┬────────────────────┬──┘
      │         │          │          │                    │
      ↓         ↓          ↓          ↓                    ↓
┌──────────┬─────────┬──────────┬─────────┬────────────────────┐
│  SUBAGENT SUBAGENT│ SUBAGENT │ SUBAGENT│  SUBAGENT          │
│ Strategist Planner│ Operator │ Analyst │  Researcher        │
│ (spawned) (spawned)│(spawned) │(spawned)│ (spawned)          │
└──────────┴─────────┴──────────┴─────────┴────────────────────┘
      │         │          │          │           │
      ↓         ↓          ↓          ↓           ↓
┌──────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS BEHAVIORS                       │
│  • Hooks (Stop, PostToolUse, Notification)                   │
│  • Event Monitors (goal_off_track, pattern_detection)        │
│  • Scheduled Tasks (daily_briefing_scheduler)                │
└──────────────────────────────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────────────────────────────┐
│                  MCP INTEGRATIONS                             │
│  • Playwright (browser automation)                            │
│  • Calendar (future)                                          │
│  • Metrics APIs (future)                                      │
│  • Custom tools                                               │
└──────────────────────────────────────────────────────────────┘
      │
      ↓
┌──────────────────────────────────────────────────────────────┐
│              PERSISTENT STORAGE (Filesystem)                  │
│  • Business data (goals, metrics, notes)                      │
│  • Agent memory files                                         │
│  • Workflow templates                                         │
│  • Generated reports and documents                            │
└──────────────────────────────────────────────────────────────┘
```

### Project Structure

```
mission-control/
│
├── main.py                        # Entry point with ClaudeSDKClient
├── .env                           # ANTHROPIC_API_KEY (optional if using Claude Code auth)
├── pyproject.toml                 # Python dependencies (uv)
│
├── .claude/                       # Claude Code configuration
│   ├── settings.json              # Hooks, MCP servers, permissions
│   │
│   ├── output-styles/             # Agent personas
│   │   ├── chief-of-staff.md
│   │   ├── operator.md
│   │   ├── planner.md
│   │   ├── strategist.md
│   │   └── analyst.md
│   │
│   ├── hooks/                     # Autonomous behavior scripts
│   │   ├── daily_briefing_check.py
│   │   ├── goal_monitor.py
│   │   ├── pattern_detector.py
│   │   └── log_agent_actions.py
│   │
│   └── agents/                    # Optional: File-based agent definitions
│       └── researcher.md
│
├── src/                           # Source code
│   ├── agent_definitions.py       # Subagent AgentDefinition configs
│   ├── cli_interface.py           # Rich CLI display
│   ├── scheduler.py               # Time-based task scheduler
│   └── event_monitors.py          # Event-driven monitors
│
├── data/                          # Business data storage
│   ├── goals/
│   ├── metrics/
│   ├── notes/
│   └── memory/                    # Agent persistent memory
│
├── workflows/                     # BMAD-style workflow templates
│   ├── daily-focus/
│   ├── weekly-review/
│   ├── quarterly-planning/
│   └── goal-setting/
│
├── templates/                     # Document templates
│   ├── daily-plan-template.md
│   ├── weekly-review-template.md
│   └── goal-template.md
│
└── output/                        # Generated documents
    ├── daily-plans/
    ├── weekly-reviews/
    ├── quarterly-plans/
    └── reports/
```

---

## Core Implementation: main.py

### Basic Structure

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition
from rich.console import Console
from dotenv import load_dotenv
import asyncio

load_dotenv()

async def main():
    console = Console()

    # Configure agent options
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-20250514",
        permission_mode="acceptEdits",
        setting_sources=["project"],  # Loads .claude/settings.json

        # Main agent tools
        allowed_tools=[
            'Read', 'Write', 'Edit', 'MultiEdit',
            'Grep', 'Glob',
            'Task',  # Required for subagents!
            'TodoWrite',
            'WebSearch', 'WebFetch',
            # MCP tools added via settings.json
        ],

        # Subagent definitions
        agents={
            "strategist": AgentDefinition(
                description="Long-term vision and strategic clarity specialist",
                prompt="""You are a strategic visionary who helps with:
                - Vision articulation and clarity
                - Goal setting (10-year, 3-year, 1-year)
                - Core values definition
                - Strategic opportunity evaluation

                You think long-term and help the user see the bigger picture.
                """,
                model="sonnet",
                tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite', 'WebSearch', 'WebFetch']
            ),

            "planner": AgentDefinition(
                description="Quarterly planning and goal tracking specialist",
                prompt="""You are a planning expert who helps with:
                - Quarterly planning and review
                - Goal breakdown into 90-day objectives (Rocks)
                - Progress tracking and metrics
                - Accountability and milestone management

                You excel at turning annual goals into actionable quarterly plans.
                """,
                model="sonnet",
                tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite']
            ),

            "operator": AgentDefinition(
                description="Daily execution and productivity specialist",
                prompt="""You are a productivity expert who helps with:
                - Daily planning and prioritization
                - Task management and time blocking
                - Eisenhower Matrix categorization
                - Focus and execution optimization

                You keep the user focused on what matters most each day.
                """,
                model="sonnet",
                tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite']
            ),

            "analyst": AgentDefinition(
                description="Business intelligence and metrics analyst",
                prompt="""You are a data analyst who helps with:
                - Metrics tracking and dashboard creation
                - Trend analysis and insights
                - Performance reporting
                - Data visualization and interpretation

                You turn data into actionable business insights.
                """,
                model="sonnet",
                tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite', 'WebSearch', 'WebFetch']
            ),

            "researcher": AgentDefinition(
                description="Deep research and documentation specialist",
                prompt="""You are an expert researcher who:
                - Performs deep research on topics using web search
                - Creates comprehensive reports with citations
                - Analyzes multiple perspectives and sources
                - Produces well-structured documentation

                Your reports are thorough, accurate, and actionable.
                """,
                model="sonnet",
                tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite', 'WebSearch', 'WebFetch']
            )
        },

        # MCP servers configured in .claude/settings.json
        mcp_servers={
            "Playwright": {
                "command": "npx",
                "args": ["-y", "@playwright/mcp@latest"]
            }
        }
    )

    console.print("[bold cyan]Mission Control initialized[/bold cyan]")
    console.print(f"Model: {options.model}")
    console.print("Subagents available: strategist, planner, operator, analyst, researcher\n")

    # Create persistent client
    async with ClaudeSDKClient(options=options) as client:

        # Conversation loop
        while True:
            user_input = console.input("[bold green]You:[/bold green] ")

            if user_input.lower() in ["exit", "quit"]:
                break

            # Send query
            await client.query(user_input)

            # Process response stream
            async for message in client.receive_response():
                # Parse and display message
                if message["type"] == "content_block_delta":
                    console.print(message["text"], end="")
                elif message["type"] == "tool_use":
                    console.print(f"\n[dim]Using tool: {message['name']}[/dim]")
                # Add more message type handlers...

            console.print("\n")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Agent Specifications

### 1. Chief of Staff (Main Agent)

**Implementation:** Output Style + Main ClaudeSDKClient context
**File:** `.claude/output-styles/chief-of-staff.md`

**Role:**
- Primary conversational interface
- Routes complex tasks to specialist subagents
- Maintains persistent context across sessions
- Triggers autonomous behaviors via hooks

**Persona Definition:**

```markdown
# Chief of Staff - Alex

You are Alex, an experienced Chief of Staff with 12+ years supporting executives. You are the primary interface for Mission Control and help the user with:

## Core Responsibilities

- **Daily Check-ins**: Help plan each day with focus and clarity
- **Strategic Discussions**: Available for ad-hoc conversations about business strategy
- **Goal Tracking**: Monitor progress on quarterly goals and surface when things are off-track
- **Executive Orchestration**: Know when to handle tasks yourself vs. delegate to specialists

## Specialist Team

You can delegate to expert subagents using the Task tool:

- **Strategist**: Long-term vision, goal-setting, strategic clarity
- **Planner**: Quarterly planning, goal breakdown, progress tracking
- **Operator**: Daily execution, task prioritization, time management
- **Analyst**: Metrics, dashboards, business intelligence
- **Researcher**: Deep research on topics, competitive analysis

## When to Delegate

- User asks for deep research → Delegate to researcher
- User wants quarterly planning → Delegate to planner
- User needs strategic clarity → Delegate to strategist
- User wants daily planning → Delegate to operator
- User requests data analysis → Delegate to analyst

## Communication Style

- Professional yet approachable
- Ask clarifying questions before routing
- Provide context when delegating
- Direct and efficient
- Remember business context across sessions

## Proactive Behaviors

- Surface insights from data you observe
- Alert when goals appear off-track
- Suggest planning sessions at appropriate times
- Recognize patterns in user's work habits
- Offer strategic recommendations unprompted

You maintain context across conversations and build understanding of the user's business over time.
```

**Key Features:**
- Uses `Task` tool to spawn subagents for specialized work
- Maintains conversation history via ClaudeSDKClient
- Can work independently or delegate
- Loads user preferences and business context from data/ folder

### 2. Strategist (Subagent)

**Implementation:** AgentDefinition in agent_definitions.py
**Spawned via:** Task tool with "strategist" agent name

**Role:**
- Long-term vision and strategic clarity
- Goal setting (10-year, 3-year, 1-year)
- Core values definition
- Strategic opportunity evaluation

**Tools Available:**
- Read, Write, Edit (document manipulation)
- Grep, Glob (search)
- TodoWrite (task planning)
- WebSearch, WebFetch (research)

**Example Delegation:**

```python
# Chief of Staff delegates vision work to Strategist
await client.query("""
I need to spawn the strategist subagent to help the user define their 10-year vision.

Task tool:
- agent: "strategist"
- prompt: "Help the user articulate a clear, measurable 10-year vision for their business.
          Ask probing questions, challenge vague language, and produce a structured vision document
          in /data/goals/10-year-vision.md"
""")
```

### 3. Planner (Subagent)

**Implementation:** AgentDefinition in agent_definitions.py
**Spawned via:** Task tool with "planner" agent name

**Role:**
- Quarterly planning and review
- Breaking annual goals into 90-day objectives (Rocks)
- Progress tracking and milestone management
- Scorecard/metrics setup

**Tools Available:**
- Read, Write, Edit
- Grep, Glob
- TodoWrite

**Key Workflows:**
- Quarterly planning session
- Rock (90-day goal) setting
- Progress review and updates

### 4. Operator (Subagent)

**Implementation:** AgentDefinition in agent_definitions.py
**Spawned via:** Task tool with "operator" agent name

**Role:**
- Daily planning and prioritization
- Eisenhower Matrix task categorization
- Time blocking and scheduling
- Weekly prep and review

**Tools Available:**
- Read, Write, Edit
- Grep, Glob
- TodoWrite

**Key Workflows:**
- Morning daily planning
- Task triage
- Time blocking
- Weekly review prep

### 5. Analyst (Subagent)

**Implementation:** AgentDefinition in agent_definitions.py
**Spawned via:** Task tool with "analyst" agent name

**Role:**
- Business metrics tracking
- Dashboard creation
- Trend analysis and insights
- Performance reporting

**Tools Available:**
- Read, Write, Edit
- Grep, Glob
- TodoWrite
- WebSearch, WebFetch
- (Future: MCP metrics integrations)

### 6. Researcher (Subagent)

**Implementation:** AgentDefinition in agent_definitions.py
**Spawned via:** Task tool with "researcher" agent name

**Role:**
- Deep research on topics
- Competitive analysis
- Market research
- Comprehensive documentation

**Tools Available:**
- Read, Write, Edit
- Grep, Glob
- TodoWrite
- WebSearch, WebFetch
- (Optional: Playwright for web automation)

**Example from Tutorial:**

```python
"researcher": AgentDefinition(
    description="An expert researcher and documentation writer",
    prompt="""You are an expert researcher. Use WebSearch and WebFetch to perform
    thorough research. Research multiple angles to get holistic understanding.
    The final report MUST include citations. Review and edit before completing.""",
    model="sonnet",
    tools=['Read', 'Write', 'Edit', 'Grep', 'Glob', 'TodoWrite', 'WebSearch', 'WebFetch']
)
```

---

## Autonomous Behaviors

### 1. Hooks Configuration

Hooks are event-driven triggers defined in `.claude/settings.json`:

```json
{
  "outputStyle": "Chief of Staff",
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/log_agent_actions.py"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/goal_monitor.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "tool": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pattern_detector.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Purr.aiff"
          }
        ]
      }
    ]
  },
  "mcp": {
    "Playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**Hook Types:**
- **Stop**: Triggered when agent finishes response
- **PostToolUse**: Triggered after specific tool usage
- **Notification**: Triggered on agent notifications
- **User-Prompt-Submit**: Triggered when user submits message

### 2. Hook Scripts

**Goal Monitor** (`.claude/hooks/goal_monitor.py`):

```python
#!/usr/bin/env python3
"""
Monitors goals in /data/goals/ and checks if any are off-track.
Alerts user proactively if intervention needed.
"""

from datetime import datetime
import json
from pathlib import Path

def check_goals():
    goals_dir = Path("data/goals")
    alerts = []

    for goal_file in goals_dir.glob("*.json"):
        with open(goal_file) as f:
            goal = json.load(f)

        # Check if goal is off track
        if goal.get("status") == "off_track":
            alerts.append(f"⚠️ Goal '{goal['name']}' is off track!")

        # Check deadline proximity
        deadline = datetime.fromisoformat(goal["deadline"])
        days_remaining = (deadline - datetime.now()).days

        if days_remaining <= 7 and goal.get("completion") < 80:
            alerts.append(f"🚨 Goal '{goal['name']}' due in {days_remaining} days - only {goal['completion']}% complete")

    if alerts:
        print("\n=== GOAL MONITORING ALERT ===")
        for alert in alerts:
            print(alert)
        print("Consider scheduling a review session.\n")

if __name__ == "__main__":
    check_goals()
```

**Pattern Detector** (`.claude/hooks/pattern_detector.py`):

```python
#!/usr/bin/env python3
"""
Analyzes user behavior patterns and surfaces insights.
Learns preferences and suggests optimizations.
"""

import json
from pathlib import Path
from collections import Counter
from datetime import datetime, timedelta

def detect_patterns():
    logs_dir = Path("data/memory/interaction_logs")

    # Analyze recent activity
    recent_logs = []
    cutoff = datetime.now() - timedelta(days=7)

    for log_file in sorted(logs_dir.glob("*.json"), reverse=True)[:100]:
        with open(log_file) as f:
            log = json.load(f)
            if datetime.fromisoformat(log["timestamp"]) > cutoff:
                recent_logs.append(log)

    # Pattern: Most common request types
    request_types = Counter([log.get("request_type") for log in recent_logs])

    # Pattern: Time of day preferences
    hours = [datetime.fromisoformat(log["timestamp"]).hour for log in recent_logs]
    peak_hours = Counter(hours).most_common(3)

    insights = []

    # Generate insights
    if request_types.get("strategic_planning") > 10:
        insights.append("📊 I notice you're doing a lot of strategic planning lately. Consider scheduling a quarterly review session.")

    if all(h[0] < 10 for h in peak_hours):
        insights.append("🌅 You seem most active in the mornings. I'll prioritize important briefings before 10am.")

    if insights:
        print("\n=== PATTERN INSIGHTS ===")
        for insight in insights:
            print(insight)
        print()

if __name__ == "__main__":
    detect_patterns()
```

### 3. Scheduled Tasks

**Daily Briefing Scheduler** (`src/scheduler.py`):

```python
import schedule
import time
from datetime import datetime
import subprocess

def daily_briefing():
    """Triggers daily briefing at scheduled time"""
    print(f"\n{'='*50}")
    print(f"🌅 DAILY BRIEFING - {datetime.now().strftime('%A, %B %d, %Y')}")
    print(f"{'='*50}\n")

    # Trigger agent to prepare briefing
    subprocess.run([
        "uv", "run", "python", "-c",
        "from src.agent_interface import trigger_briefing; trigger_briefing()"
    ])

def goal_check():
    """Weekly goal progress check"""
    subprocess.run(["uv", "run", ".claude/hooks/goal_monitor.py"])

# Schedule tasks
schedule.every().day.at("06:30").do(daily_briefing)
schedule.every().monday.at("09:00").do(goal_check)

if __name__ == "__main__":
    print("Mission Control Scheduler running...")
    while True:
        schedule.run_pending()
        time.sleep(60)
```

### 4. Event Monitors

Event monitors run continuously and trigger actions based on data changes:

```python
# src/event_monitors.py

import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class GoalMonitor(FileSystemEventHandler):
    """Monitors goal files for changes and triggers alerts"""

    def on_modified(self, event):
        if event.src_path.endswith('.json'):
            # Check if goal status changed
            with open(event.src_path) as f:
                goal = json.load(f)

            if goal.get("status") == "off_track":
                self.trigger_alert(goal)

    def trigger_alert(self, goal):
        print(f"🚨 ALERT: Goal '{goal['name']}' is now off track!")
        # Could trigger agent notification here

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(GoalMonitor(), "data/goals", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
```

---

## MCP Integration

### Playwright Browser Automation

Configured in `.claude/settings.json` and available to agents:

```python
# In ClaudeAgentOptions
mcp_servers={
    "Playwright": {
        "command": "npx",
        "args": ["-y", "@playwright/mcp@latest"]
    }
}

# Tools available with mcp__Playwright__ prefix:
allowed_tools=[
    'mcp__Playwright__browser_navigate',
    'mcp__Playwright__browser_click',
    'mcp__Playwright__browser_take_screenshot',
    'mcp__Playwright__browser_snapshot',
    # ... etc
]
```

**Use Cases:**
- Research competitor websites
- Monitor web-based metrics dashboards
- Automate data collection
- Screenshot capture for reports

### Future MCP Integrations

**Calendar Integration:**
```json
"calendar": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-google-calendar"]
}
```

**Metrics APIs:**
```json
"stripe": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-stripe"]
}
```

**Email Integration:**
```json
"gmail": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-gmail"]
}
```

---

## Persistent Memory

### Memory Architecture

Mission Control maintains context through:

1. **File-based Storage**: Business data in `/data` folder
2. **Agent Memory Files**: Loaded via critical_actions
3. **Conversation History**: Maintained by ClaudeSDKClient
4. **Interaction Logs**: Event tracking for pattern recognition

### Memory Files Structure

```
data/
├── memory/
│   ├── business_context.json        # Company info, preferences
│   ├── conversation_history.json    # Summary of past key conversations
│   ├── learned_preferences.json     # User patterns and preferences
│   └── interaction_logs/            # Detailed logs for pattern analysis
│
├── goals/
│   ├── 10-year-vision.json
│   ├── 3-year-goals.json
│   ├── 2025-Q4-rocks.json           # Current quarter objectives
│   └── completed/                   # Archive of completed goals
│
├── metrics/
│   ├── scorecard.json               # Weekly metrics
│   ├── trends.json                  # Historical trends
│   └── dashboards/
│
└── notes/
    ├── strategic-thoughts/
    ├── meeting-notes/
    └── ideas/
```

### Loading Memory into Agents

Chief of Staff loads memory on initialization:

```python
# In .claude/output-styles/chief-of-staff.md

## Critical Actions

ALWAYS perform these actions at the start of every conversation:

1. Load business context: Read `data/memory/business_context.json`
2. Load learned preferences: Read `data/memory/learned_preferences.json`
3. Check recent goals: Read latest file in `data/goals/`
4. Review interaction logs: Scan `data/memory/interaction_logs/` for patterns

This ensures you have full context for every conversation.
```

### Example: Business Context File

```json
{
  "user": {
    "name": "Mike",
    "role": "CEO",
    "timezone": "America/New_York",
    "communication_preferences": {
      "style": "direct and concise",
      "preferred_times": ["06:30-09:00", "17:00-18:00"],
      "daily_briefing_time": "06:30"
    }
  },
  "business": {
    "name": "Company Name",
    "industry": "SaaS",
    "stage": "Growth",
    "team_size": 12,
    "founded": "2020-01-01"
  },
  "current_focus": {
    "quarter": "2025-Q4",
    "top_priority": "Product launch",
    "active_projects": 5
  },
  "learned_patterns": {
    "peak_productivity_hours": [7, 8, 9],
    "preferred_planning_day": "Sunday evening",
    "most_common_requests": ["strategic planning", "daily planning", "research"]
  }
}
```

---

## Key Workflows

Workflows combine SDK capabilities with BMAD Method structural patterns.

### Workflow 1: Daily Focus

**Frequency:** Daily (morning)
**Agent:** Operator (subagent)
**Duration:** 10-15 minutes

**Implementation:**

```python
# Chief of Staff delegates to Operator
async def daily_focus_workflow(client: ClaudeSDKClient, user_input: str):
    """
    Spawn Operator subagent to run daily planning session.
    """
    prompt = f"""
    Spawn the 'operator' subagent to conduct a daily focus session.

    The operator should:
    1. Review today's calendar and commitments
    2. Help user brain dump all tasks
    3. Apply Eisenhower Matrix categorization
    4. Identify 1-3 Most Important Tasks (MITs)
    5. Schedule deep work blocks
    6. Set daily intention
    7. Generate daily plan document in /output/daily-plans/{{date}}.md

    User context: {user_input}
    """

    await client.query(prompt)

    async for message in client.receive_response():
        # Handle messages
        yield message
```

**Template:** `templates/daily-plan-template.md`

```markdown
# Daily Focus - {{date}}

## Today's Intention
{{daily_intention}}

## Most Important Tasks (MITs)
1. {{mit_1}}
2. {{mit_2}}
3. {{mit_3}}

## Eisenhower Matrix

### Quadrant 1: Urgent + Important (Do First)
{{q1_tasks}}

### Quadrant 2: Not Urgent + Important (Schedule Deep Work)
{{q2_tasks}}

### Quadrant 3: Urgent + Not Important (Delegate/Minimize)
{{q3_tasks}}

### Quadrant 4: Not Urgent + Not Important (Eliminate)
{{q4_tasks}}

## Time Blocks
{{time_blocks}}

## Calendar
{{calendar_summary}}

---
*Generated by Mission Control - Operator Agent*
```

### Workflow 2: Weekly Review

**Frequency:** Weekly (Monday morning before L10)
**Agent:** Operator + Chief of Staff
**Duration:** 30 minutes

**Purpose:**
- Review last week's progress
- Identify wins and learnings
- Prepare for L10 meeting
- Set week's priorities

### Workflow 3: Quarterly Planning

**Frequency:** Quarterly
**Agent:** Planner (subagent)
**Duration:** 2-3 hours (can span multiple sessions)

**Purpose:**
- Review previous quarter
- Set 3-7 Rocks (90-day goals)
- Break down annual goals
- Establish metrics and milestones

### Workflow 4: Strategic Vision Session

**Frequency:** Annual or as-needed
**Agent:** Strategist (subagent)
**Duration:** 2-4 hours

**Purpose:**
- Define/refine 10-year vision
- Articulate 3-year picture
- Set 1-year goals
- Clarify core values and mission

### Workflow 5: Deep Research Project

**Frequency:** On-demand
**Agent:** Researcher (subagent)
**Duration:** Variable

**Purpose:**
- Comprehensive research on topic
- Competitive analysis
- Market research
- Documentation with citations

**Example Invocation:**

```python
# User requests research
await client.query("""
I need deep research on the AI agent market landscape -
competitors, pricing, features, market trends.
""")

# Chief of Staff delegates to Researcher
# Researcher subagent spawned with:
# - WebSearch and WebFetch tools
# - Instruction to create comprehensive report
# - Requirement to include citations
# - Deliverable: /output/reports/ai-agent-market-analysis.md
```

---

## Scale Adaptation

Mission Control adapts to user needs and business complexity:

### Personal Use (Individual)

**Characteristics:**
- Single user (entrepreneur/executive)
- Focus on personal productivity and strategy
- Simplified workflows

**Active Agents:**
- Chief of Staff
- Operator (daily)
- Strategist (periodic)

**Key Workflows:**
- Daily focus
- Weekly review
- Quarterly personal planning

### Small Team (2-10 people)

**Characteristics:**
- Small team with informal structure
- Collaborative goals
- Shared metrics

**Active Agents:**
- All core agents
- Team-focused prompts

**Key Workflows:**
- All personal workflows
- Team goal setting
- Shared scorecard

### Growing Business (10-50 people)

**Characteristics:**
- Defined roles and departments
- Multiple projects tracked
- Formal processes

**Active Agents:**
- All agents + custom agents per department
- Analyst for metrics dashboards

**Key Workflows:**
- Department-level planning
- Cross-team coordination
- Strategic initiative tracking

### Enterprise (50+ people)

**Characteristics:**
- Complex org structure
- Multiple divisions
- Executive dashboard needs

**Active Agents:**
- Agent hierarchy matching org structure
- Specialized analysts
- Custom agents for specific functions

**Key Workflows:**
- Multi-level planning
- Consolidated reporting
- Strategic program management

---

## Security and Privacy

### Data Storage

- **Local-first**: All data stored locally in project folder
- **User control**: Full ownership of all documents and context
- **No cloud dependency**: Works offline (except web search/MCP features)

### API Key Management

```
# .env file (gitignored)
ANTHROPIC_API_KEY=sk-ant-...

# OR authenticate via Claude Code CLI (no key needed)
claude-code login
```

### Sensitive Information

- Business context files contain company information
- Agent memory includes learned preferences
- Interaction logs track detailed activity

**Recommendation:** Add to `.gitignore`:
```
.env
data/memory/
data/goals/
output/
*.log
```

---

## Testing Strategy

### Unit Testing

Test individual components:

```python
# tests/test_agent_definitions.py

def test_strategist_definition():
    """Verify strategist subagent config is valid"""
    from src.agent_definitions import agents

    strategist = agents["strategist"]
    assert strategist.description is not None
    assert "vision" in strategist.description.lower()
    assert strategist.model == "sonnet"
    assert "WebSearch" in strategist.tools

def test_daily_focus_template():
    """Verify daily focus template renders correctly"""
    from templates import render_template

    output = render_template("daily-plan-template.md", {
        "date": "2025-10-14",
        "mit_1": "Finish architecture doc",
        "mit_2": "Review Q4 goals",
        "mit_3": "Team sync",
    })

    assert "2025-10-14" in output
    assert "Finish architecture doc" in output
```

### Integration Testing

Test agent interactions:

```python
# tests/test_agent_interactions.py

async def test_chief_delegates_to_operator():
    """Verify Chief of Staff can spawn Operator subagent"""

    async with ClaudeSDKClient(options=test_options) as client:
        await client.query("Help me plan my day")

        # Verify Task tool was used
        # Verify operator subagent was spawned
        # Verify daily plan was generated
```

### End-to-End Testing

Test complete workflows:

```python
# tests/test_workflows.py

async def test_daily_focus_workflow_e2e():
    """Test complete daily focus workflow"""

    # 1. User requests daily planning
    # 2. Chief of Staff spawns Operator
    # 3. Operator conducts planning session
    # 4. Document generated in /output
    # 5. User receives summary

    # Verify all steps completed
    # Verify output file exists
    # Verify content matches template
```

---

## Success Metrics

### Engagement Metrics

- **Daily briefing usage**: Target 5+ days/week
- **Proactive insights surfaced**: Track how often agents surface unprompted insights
- **Subagent spawns**: Track delegation patterns

### Productivity Metrics

- **Goals on-track**: Percentage of goals marked on-track
- **Planning consistency**: Weekly/quarterly planning sessions completed
- **Time to insight**: How quickly agents surface relevant information

### System Metrics

- **Response latency**: Agent response times
- **Subagent success rate**: Subagent task completion
- **Hook execution**: Autonomous behavior trigger frequency
- **Memory accuracy**: Context retention across sessions

---

## Maintenance and Evolution

### Regular Maintenance

- Update agent prompts based on user feedback
- Refine hook scripts for better pattern detection
- Expand MCP integrations
- Improve memory management

### Versioning Strategy

- **Patch (2.0.1)**: Bug fixes, prompt tweaks
- **Minor (2.1.0)**: New subagents, new workflows
- **Major (3.0.0)**: Architecture changes, new SDK features

### Extension Points

1. **Custom Subagents**: Add new specialist agents via AgentDefinition
2. **New Workflows**: Add workflow templates to `/workflows`
3. **MCP Tools**: Integrate new external services
4. **Hooks**: Add autonomous behaviors via hook scripts
5. **Memory**: Enhance context persistence and pattern recognition

---

## Deployment Options

### Option 1: Local Development

```bash
# Clone repo
git clone <repo-url>
cd mission-control

# Install dependencies
uv sync

# Configure
cp .env.example .env
# Edit .env with ANTHROPIC_API_KEY

# Run
python main.py
```

### Option 2: Background Service

Run scheduler as background service:

```bash
# Install as systemd service (Linux)
sudo cp mission-control.service /etc/systemd/system/
sudo systemctl enable mission-control
sudo systemctl start mission-control

# Scheduler runs continuously, triggers briefings and monitors
```

### Option 3: Claude Code Integration

Use Claude Code CLI as interface:

```bash
# Navigate to project
cd mission-control

# Claude Code loads .claude/ config automatically
claude-code

# Agents available in CLI with full MCP and hooks support
```

---

## Conclusion

Mission Control v2.0 represents a **hybrid architecture** that combines:

1. **Claude Agent SDK**: Autonomous behaviors, subagent spawning, MCP integration
2. **BMAD Method Patterns**: Structured workflows, templates, organization

This architecture delivers:

- ✅ **Autonomy**: Agents work proactively, not just reactively
- ✅ **Persistence**: Context builds across sessions
- ✅ **Extensibility**: Easy to add new agents and workflows
- ✅ **Structure**: Proven patterns for executive workflows
- ✅ **Intelligence**: Pattern recognition and insight generation

**Key Differentiators:**

- Not just a chatbot—an autonomous executive team
- Not just reactive—proactively surfaces insights
- Not just one-off conversations—builds persistent context
- Not just fixed capabilities—self-extending system

**Next Steps:** Proceed to EPIC-1 stories for implementation planning.
