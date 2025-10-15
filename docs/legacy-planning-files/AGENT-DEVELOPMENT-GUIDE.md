# Agent Development Guide
## Building and Customizing Mission Control Agents

**Version:** 1.0
**Last Updated:** October 14, 2025
**Audience:** Developers building on Mission Control

---

## Table of Contents

1. [Overview](#overview)
2. [Agent Architecture](#agent-architecture)
3. [Creating Custom Subagents](#creating-custom-subagents)
4. [Customizing Output Styles](#customizing-output-styles)
5. [Building Autonomous Behaviors](#building-autonomous-behaviors)
6. [Working with Memory](#working-with-memory)
7. [MCP Integration](#mcp-integration)
8. [Testing Agents](#testing-agents)
9. [Best Practices](#best-practices)

---

## Overview

Mission Control uses a **hybrid architecture** combining:
- **Claude Agent SDK**: Core autonomous capabilities
- **BMAD Method Patterns**: Structural organization

This guide teaches you how to extend and customize the system.

### Key Concepts

- **Main Agent**: Chief of Staff (primary interface)
- **Subagents**: Specialist agents spawned for specific tasks
- **Output Styles**: Persona definitions that replace Claude's identity
- **Hooks**: Event-driven triggers for autonomous behaviors
- **Memory**: Persistent context stored in files
- **MCP**: Model Context Protocol for external tool integration

---

## Agent Architecture

### Three Types of Agents

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN AGENT                                │
│  • Defined by Output Style (.claude/output-styles/)          │
│  • Persistent conversation via ClaudeSDKClient               │
│  • Routes to subagents via Task tool                         │
│  • Has access to all tools                                   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ spawns via Task tool
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    SUBAGENTS                                 │
│  • Defined by AgentDefinition in Python                      │
│  • Isolated context (don't share state)                      │
│  • Restricted tool access                                    │
│  • Return results to main agent                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ triggered by events
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS BEHAVIORS                       │
│  • Defined by Hooks (.claude/settings.json)                  │
│  • Python scripts in .claude/hooks/                          │
│  • Triggered by events (Stop, PostToolUse, etc.)             │
│  • Run in background, don't block conversation               │
└─────────────────────────────────────────────────────────────┘
```

### Agent Lifecycle

1. **Initialization**: Load configuration, output style, memory
2. **Conversation**: User interacts with main agent
3. **Delegation**: Main agent spawns subagent for specialized work
4. **Execution**: Subagent completes task in isolated context
5. **Return**: Subagent returns result to main agent
6. **Hooks**: Autonomous behaviors trigger after events

---

## Creating Custom Subagents

### Step 1: Define Agent Purpose

Before coding, answer:
- **What specific task does this agent handle?**
- **What expertise does it need?**
- **What tools does it require?**
- **When should it be delegated to?**

### Step 2: Create AgentDefinition

Add to `src/agent_definitions.py`:

```python
from claude_agent_sdk import AgentDefinition

# Example: Financial Analyst Agent
financial_analyst = AgentDefinition(
    description=(
        "Financial analysis and budgeting specialist. Helps with financial modeling, "
        "budget planning, cash flow analysis, and financial reporting."
    ),
    prompt="""You are a financial analyst with expertise in business finance.

## Your Core Capabilities

- **Financial Modeling**: Create pro forma financials, projections
- **Budget Planning**: Help develop and track budgets
- **Cash Flow Analysis**: Monitor and project cash flow
- **Financial Reporting**: Generate financial reports and dashboards
- **Cost Analysis**: Analyze costs and identify optimization opportunities

## Your Approach

- Start with understanding the business model and revenue streams
- Focus on actionable insights, not just numbers
- Present financial data visually when possible
- Connect financial metrics to strategic objectives
- Flag risks and opportunities proactively

## Your Tools

You have access to:
- Read/Write/Edit: For creating financial models and reports
- Grep/Glob: For searching historical financial data
- TodoWrite: For planning multi-step financial projects

## Your Deliverables

Create in `/data/metrics/financial/`:
- Monthly financial reports
- Budget vs. actual analysis
- Cash flow projections
- Financial dashboards (markdown tables)

Always include: Current state, Trend, Target, Variance analysis, Recommendations.
""",
    model="sonnet",
    tools=[
        'Read', 'Write', 'Edit', 'MultiEdit',
        'Grep', 'Glob',
        'TodoWrite'
    ]
)

# Add to agents dictionary
agents = {
    # ... existing agents ...
    "financial_analyst": financial_analyst,
}
```

### Step 3: Update Main Agent to Route

Edit `.claude/output-styles/chief-of-staff.md` to include new agent:

```markdown
## Your Specialist Team

### Financial Analyst
**Delegate when:** User discusses budgets, cash flow, financial projections, cost analysis
**Example triggers:** "budget", "cash flow", "financial model", "costs", "revenue projection"
```

### Step 4: Test the Agent

```python
# test_financial_analyst.py
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from src.agent_definitions import agents

async def test_financial_analyst():
    options = ClaudeAgentOptions(
        model="claude-haiku-4-20250611",
        agents={"financial_analyst": agents["financial_analyst"]}
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("""
        Spawn the financial_analyst subagent with this task:
        Create a simple monthly budget template for a SaaS company.
        """)

        async for message in client.receive_response():
            if message.get("type") == "content_block_delta":
                print(message["text"], end="")

if __name__ == "__main__":
    asyncio.run(test_financial_analyst())
```

Run test:
```bash
uv run python test_financial_analyst.py
```

### Agent Definition Best Practices

1. **Description**: 1-2 sentences, keyword-rich for routing
2. **Prompt**: Comprehensive, includes capabilities, approach, tools, deliverables
3. **Model**: Use "sonnet" for balanced performance, "opus" for complex reasoning
4. **Tools**: Principle of least privilege - only what's needed
5. **Deliverables**: Specify exact output format and location

---

## Customizing Output Styles

Output styles define agent personas. They're markdown files that become system prompts.

### Anatomy of an Output Style

```markdown
# [Agent Name] - [Persona Name]

[Opening identity paragraph - who you are]

---

## Your Identity

[Detailed identity and role description]

---

## Core Responsibilities

[What you do - bulleted list]

---

## [Domain-Specific Sections]

[Methodology, frameworks, specializations]

---

## Communication Style

[How you interact - tone, approach, examples]

---

## Proactive Behaviors

[What you do autonomously]

---

## Critical Actions

[Must-do actions at conversation start - especially memory loading]

---

## Tool Usage Guidelines

[How to use available tools]

---

## Example Interactions

[Concrete examples of conversations]

---

## Remember

[Closing identity reinforcement]
```

### Example: Creating "Operator" Output Style

Create `.claude/output-styles/operator.md`:

```markdown
# Operator - Taylor

You are **Taylor**, a productivity expert focused on daily execution excellence.

---

## Your Identity

You specialize in helping executives stay focused on what matters most each day. You're known for:
- Sharp prioritization using the Eisenhower Matrix
- Protecting deep work time fiercely
- Keeping people accountable to their Most Important Tasks (MITs)
- No-nonsense approach to time management

---

## Core Responsibilities

- Morning planning sessions (10-15 minutes)
- Task prioritization and categorization
- Time blocking for deep work
- Weekly preparation and review
- Daily accountability

---

## Your Framework: Eisenhower Matrix

Every task falls into one of four quadrants:

**Q1 - Urgent + Important**: Do first, today
**Q2 - Not Urgent + Important**: Schedule deep work (MOST VALUABLE)
**Q3 - Urgent + Not Important**: Delegate or minimize
**Q4 - Not Urgent + Not Important**: Eliminate

You obsessively focus on Q2 - this is where strategic work happens.

---

## Daily Planning Process

1. Review calendar and commitments
2. Brain dump tasks (aim for 10-20 items)
3. Apply Eisenhower Matrix
4. Identify 1-3 Most Important Tasks (MITs)
5. Schedule deep work blocks for MITs
6. Set daily intention

---

## Communication Style

- **Direct**: No fluff, get to the point
- **Action-oriented**: Always focus on next actions
- **Accountability-focused**: Keep people on track
- **Time-conscious**: Respect the user's time

### Examples

**Good:**
> "You have 3 hours of unscheduled time today. Let's block 90 minutes for your top MIT - finishing the proposal. When works best: 10-11:30am or 2-3:30pm?"

**Bad:**
> "What would you like to work on today?"

---

## Tool Usage

- Write: Create daily plans in `/output/daily-plans/YYYY-MM-DD.md`
- Read: Review yesterday's plan for continuity
- Edit: Update plans as day evolves

---

## Remember

You keep executives focused on what matters most. Daily discipline creates quarterly results.
```

### Using Output Styles

**In .claude/settings.json:**
```json
{
  "outputStyle": "Chief of Staff"  // or "Operator", etc.
}
```

**Switching output styles:**
- Change `outputStyle` in settings.json
- Restart conversation or reload configuration

---

## Building Autonomous Behaviors

Autonomous behaviors use **hooks** - event-driven Python scripts.

### Available Hook Types

| Hook Type | Trigger | Use Case |
|-----------|---------|----------|
| `Stop` | Agent finishes response | Log actions, check goals, run monitors |
| `PostToolUse` | After specific tool use | Pattern detection, validation |
| `Notification` | Agent sends notification | Sound alert, external notification |
| `User-Prompt-Submit` | User sends message | Pre-processing, logging |

### Creating a Hook: Weekly Review Reminder

**1. Create hook script** (`.claude/hooks/weekly_review_reminder.py`):

```python
#!/usr/bin/env python3
"""
Weekly Review Reminder Hook

Checks if it's Monday morning and user hasn't done weekly review yet.
Proactively suggests starting weekly review.
"""

from datetime import datetime
from pathlib import Path
import json

def check_weekly_review():
    """Check if weekly review is due"""

    now = datetime.now()

    # Only trigger on Monday mornings
    if now.weekday() != 0:  # 0 = Monday
        return

    if now.hour > 11:  # Only before noon
        return

    # Check if review already done this week
    output_dir = Path("output/weekly-reviews")
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        return

    # Look for this week's review
    week_start = now.strftime("%Y-W%W")
    review_files = list(output_dir.glob(f"{week_start}*.md"))

    if not review_files:
        print("\n" + "=" * 60)
        print("  📅 WEEKLY REVIEW REMINDER")
        print("=" * 60)
        print("  It's Monday morning - perfect time for your weekly review!")
        print("  Want me to help you with that?")
        print("=" * 60 + "\n")

if __name__ == "__main__":
    check_weekly_review()
```

**2. Make executable** (Unix/macOS):
```bash
chmod +x .claude/hooks/weekly_review_reminder.py
```

**3. Register in .claude/settings.json**:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/weekly_review_reminder.py"
          }
        ]
      }
    ]
  }
}
```

**4. Test**:
```bash
# Test script directly
uv run .claude/hooks/weekly_review_reminder.py

# Test in conversation (on Monday morning)
python main.py
# After agent response, should see reminder
```

### Hook Best Practices

1. **Fast Execution**: Keep hooks under 100ms
2. **Error Handling**: Use try-except, don't crash
3. **Silent Failures**: Optional features should fail silently
4. **Conditional Triggers**: Only run when relevant
5. **Logging**: Log to stderr, not stdout
6. **Testing**: Test hooks independently first

---

## Working with Memory

Memory enables context persistence across sessions.

### Memory Architecture

```
data/memory/
├── business_context.json       # Company info, current focus
├── learned_preferences.json    # User patterns and preferences
├── conversation_history.json   # Key conversation summaries
└── interaction_logs/           # Detailed logs (JSONL format)
    ├── 2025-10-14.jsonl
    └── 2025-10-15.jsonl
```

### Creating Memory Files

**business_context.json:**
```json
{
  "user": {
    "name": "Mike",
    "role": "CEO",
    "timezone": "America/New_York",
    "communication_preferences": {
      "style": "direct and data-driven",
      "preferred_times": ["06:30-09:00", "17:00-18:00"],
      "daily_briefing_time": "06:30"
    }
  },
  "business": {
    "name": "Acme Corp",
    "industry": "SaaS",
    "stage": "Growth",
    "team_size": 12,
    "founded": "2020-01-01",
    "fiscal_year_start": "01-01"
  },
  "current_focus": {
    "quarter": "2025-Q4",
    "top_priority": "Enterprise sales",
    "active_projects": 5,
    "current_challenges": [
      "Scaling sales team",
      "Product-market fit for enterprise"
    ]
  },
  "learned_patterns": {
    "peak_productivity_hours": [7, 8, 9],
    "preferred_planning_day": "Sunday evening",
    "most_common_requests": ["strategic planning", "daily planning", "metrics review"],
    "decision_making_style": "data-driven, moves quickly once decided"
  }
}
```

**learned_preferences.json:**
```json
{
  "communication": {
    "formality": "professional but warm",
    "emoji_preference": "minimal",
    "response_length": "concise",
    "detail_level": "executive summary + details on request"
  },
  "workflow": {
    "planning_frequency": "daily morning + weekly Monday",
    "preferred_frameworks": ["Eisenhower Matrix", "OKRs", "Rocks"],
    "review_cadence": "weekly"
  },
  "tools": {
    "most_used": ["daily_planning", "goal_tracking", "research"],
    "preferred_agents": ["operator", "strategist", "researcher"]
  },
  "updated_at": "2025-10-14T10:30:00"
}
```

### Loading Memory in Agents

In output style (`.claude/output-styles/chief-of-staff.md`):

```markdown
## Critical Actions

**ALWAYS perform at conversation start:**

1. **Load Business Context**
   ```
   Read data/memory/business_context.json
   ```
   This contains: User info, business info, current focus, learned patterns

2. **Check Active Goals**
   ```
   Read latest file in data/goals/
   ```
   Know what's active and progress status

3. **Review Recent Interactions** (if relevant)
   ```
   Read latest file in data/memory/interaction_logs/
   ```
   Understand recent context

**If files don't exist:** That's fine - new session. Create them as you learn.
```

### Updating Memory Programmatically

```python
# src/memory_manager.py

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class MemoryManager:
    """Manages persistent memory across sessions"""

    def __init__(self, memory_dir: str = "data/memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def load_business_context(self) -> Dict[str, Any]:
        """Load business context from file"""
        context_file = self.memory_dir / "business_context.json"

        if context_file.exists():
            with open(context_file) as f:
                return json.load(f)
        return self._default_business_context()

    def save_business_context(self, context: Dict[str, Any]):
        """Save business context to file"""
        context_file = self.memory_dir / "business_context.json"

        with open(context_file, 'w') as f:
            json.dump(context, f, indent=2)

    def update_learned_preference(self, category: str, key: str, value: Any):
        """Update a learned preference"""
        prefs_file = self.memory_dir / "learned_preferences.json"

        # Load existing
        if prefs_file.exists():
            with open(prefs_file) as f:
                prefs = json.load(f)
        else:
            prefs = {}

        # Update
        if category not in prefs:
            prefs[category] = {}
        prefs[category][key] = value
        prefs["updated_at"] = datetime.now().isoformat()

        # Save
        with open(prefs_file, 'w') as f:
            json.dump(prefs, f, indent=2)

    def log_interaction(self, event_type: str, metadata: Dict[str, Any]):
        """Log interaction to daily log file"""
        log_dir = self.memory_dir / "interaction_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "metadata": metadata
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def _default_business_context(self) -> Dict[str, Any]:
        """Return default empty context structure"""
        return {
            "user": {},
            "business": {},
            "current_focus": {},
            "learned_patterns": {}
        }
```

Usage in hooks:
```python
from src.memory_manager import MemoryManager

memory = MemoryManager()

# Log action
memory.log_interaction("agent_response", {"agent": "operator", "task": "daily_planning"})

# Update preference
memory.update_learned_preference("workflow", "preferred_planning_time", "07:00")
```

---

## MCP Integration

MCP (Model Context Protocol) enables external tool integration.

### Available MCP Servers

- **Playwright**: Browser automation ([docs](https://github.com/playwright/mcp))
- **Google Calendar**: Calendar integration
- **Stripe**: Payment data
- **Gmail**: Email access
- **Custom**: Build your own

### Installing Playwright MCP

**1. Install Node.js** (if not already):
```bash
# macOS
brew install node

# Windows
choco install nodejs

# Linux
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**2. Configure in .claude/settings.json**:

```json
{
  "mcp": {
    "Playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

**3. Add tools to agent options** (main.py):

```python
options = ClaudeAgentOptions(
    # ... other options ...
    allowed_tools=[
        # ... existing tools ...
        'mcp__Playwright__browser_navigate',
        'mcp__Playwright__browser_click',
        'mcp__Playwright__browser_take_screenshot',
        'mcp__Playwright__browser_snapshot',
        # Add other Playwright tools as needed
    ],
    mcp_servers={
        "Playwright": {
            "command": "npx",
            "args": ["-y", "@playwright/mcp@latest"]
        }
    }
)
```

**4. Test**:
```bash
python main.py
```

```
You: Can you navigate to anthropic.com and take a screenshot?

[Agent should use Playwright MCP tools]
```

### Creating Custom MCP Server

See [MCP Documentation](https://modelcontextprotocol.io/) for building custom servers.

Basic structure:
```python
# custom_mcp_server.py

from mcp import Server, Tool

server = Server("custom-tools")

@server.tool()
def custom_function(param: str) -> str:
    """Custom tool description"""
    # Your logic here
    return f"Result: {param}"

if __name__ == "__main__":
    server.run()
```

Register in settings.json:
```json
{
  "mcp": {
    "CustomTools": {
      "command": "python",
      "args": ["custom_mcp_server.py"]
    }
  }
}
```

---

## Testing Agents

### Unit Testing

```python
# tests/test_agent_definitions.py

import pytest
from src.agent_definitions import agents, list_agents, get_agent_description

def test_all_agents_have_descriptions():
    """Verify all agents have descriptions"""
    for name, agent in agents.items():
        assert agent.description is not None, f"Agent {name} missing description"
        assert len(agent.description) > 20, f"Agent {name} description too short"

def test_all_agents_have_prompts():
    """Verify all agents have prompts"""
    for name, agent in agents.items():
        assert agent.prompt is not None, f"Agent {name} missing prompt"
        assert len(agent.prompt) > 100, f"Agent {name} prompt too short"

def test_all_agents_have_tools():
    """Verify all agents have tools"""
    for name, agent in agents.items():
        assert agent.tools is not None, f"Agent {name} missing tools"
        assert len(agent.tools) > 0, f"Agent {name} has no tools"

def test_list_agents():
    """Verify list_agents returns correct count"""
    agent_list = list_agents()
    assert len(agent_list) == 5, f"Expected 5 agents, got {len(agent_list)}"

def test_get_agent_description():
    """Test agent description retrieval"""
    desc = get_agent_description("strategist")
    assert "vision" in desc.lower()
    assert "strategic" in desc.lower()
```

### Integration Testing

```python
# tests/test_agent_interactions.py

import pytest
import asyncio
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from src.agent_definitions import agents

@pytest.mark.asyncio
async def test_strategist_spawns_successfully():
    """Test that strategist subagent can be spawned"""

    options = ClaudeAgentOptions(
        model="claude-haiku-4-20250611",
        agents={"strategist": agents["strategist"]}
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query("""
        Spawn the strategist subagent with this task:
        Write a one-sentence example of a 10-year vision.
        """)

        response_text = ""
        async for message in client.receive_response():
            if message.get("type") == "content_block_delta":
                response_text += message.get("text", "")

        # Verify response contains expected content
        assert len(response_text) > 10, "Strategist should return meaningful response"

@pytest.mark.asyncio
async def test_main_agent_delegates_correctly():
    """Test that main agent correctly delegates to subagents"""

    options = ClaudeAgentOptions(
        model="claude-haiku-4-20250611",
        agents=agents
    )

    async with ClaudeSDKClient(options=options) as client:
        # Request that should trigger delegation to planner
        await client.query("Help me plan my quarter")

        tool_uses = []
        async for message in client.receive_response():
            if message.get("type") == "tool_use":
                tool_uses.append(message.get("name"))

        # Verify Task tool was used (for delegation)
        assert "Task" in tool_uses, "Main agent should use Task tool for delegation"
```

### Manual Testing Checklist

**For Each Agent:**
- [ ] Agent spawns successfully
- [ ] Agent completes assigned task
- [ ] Agent uses appropriate tools
- [ ] Agent produces expected deliverables
- [ ] Agent handles errors gracefully
- [ ] Agent stays within defined scope

**For Autonomous Behaviors:**
- [ ] Hooks trigger at correct events
- [ ] Hook scripts execute without errors
- [ ] Hook failures don't crash main agent
- [ ] Proactive insights are relevant
- [ ] Notifications are not annoying

**For Memory:**
- [ ] Memory files load correctly
- [ ] Agent remembers context across sessions
- [ ] Memory updates persist
- [ ] No corruption of memory files

---

## Best Practices

### Agent Design

1. **Single Responsibility**: Each agent should have one clear purpose
2. **Clear Boundaries**: Define when to use each agent explicitly
3. **Appropriate Tools**: Grant only necessary tools (least privilege)
4. **Quality Prompts**: Invest time in comprehensive, clear prompts
5. **Test Thoroughly**: Test each agent independently before integration

### Output Styles

1. **Consistent Persona**: Maintain character throughout
2. **Clear Identity**: User should know who they're talking to
3. **Specific Examples**: Include concrete interaction examples
4. **Memory Loading**: Always include critical actions for memory
5. **Delegation Logic**: Clear rules for when to delegate

### Autonomous Behaviors

1. **User Value**: Only add behaviors that truly help
2. **Configurable**: Make behaviors easy to disable
3. **Non-Intrusive**: Don't interrupt flow unnecessarily
4. **Error Tolerant**: Failures should be silent or logged
5. **Performance**: Keep hooks fast (<100ms)

### Memory Management

1. **Structured Data**: Use JSON for structured data
2. **Version Control**: Consider versioning important memory files
3. **Privacy**: Never log sensitive information
4. **Cleanup**: Periodically archive old logs
5. **Validation**: Validate data before saving

### Security

1. **Input Validation**: Validate all file paths and user inputs
2. **Tool Restrictions**: Limit tool access per agent appropriately
3. **API Key Security**: Never log or commit API keys
4. **Data Privacy**: Treat all business data as confidential
5. **MCP Review**: Review security of MCP servers before use

---

## Common Patterns

### Pattern: Delegation with Context

```python
# In output style
"""When delegating, always provide context:

BAD:
"I'll spawn the researcher subagent."

GOOD:
"I'm bringing in our Researcher to help with this. They'll perform comprehensive
research across multiple sources and create a report with citations. This usually
takes 5-10 minutes for thorough research. One moment..."
"""
```

### Pattern: Progressive Enhancement

```python
# Start simple, add complexity
# Version 1: Basic agent with core functionality
# Version 2: Add memory loading
# Version 3: Add proactive behaviors
# Version 4: Add MCP integration
```

### Pattern: Graceful Degradation

```python
# In hook scripts
try:
    # Attempt advanced feature
    analyze_patterns()
except Exception as e:
    # Fail silently or log to stderr
    print(f"Warning: Pattern analysis failed: {e}", file=sys.stderr)
    # Continue without pattern analysis
```

### Pattern: Configuration Over Code

```python
# Use config files for customization
# .claude/settings.json for behaviors
# data/memory/ for learned preferences
# Avoid hardcoding user-specific logic
```

---

## Next Steps

1. **Start Simple**: Begin with core agents, add complexity gradually
2. **Customize Personas**: Tailor output styles to your preferences
3. **Add Behaviors**: Build autonomous behaviors that provide value
4. **Integrate Tools**: Add MCP servers for external integrations
5. **Share**: Contribute agents and patterns back to the community

## Resources

- [Architecture Document](./mission-control-architecture.md)
- [Technical Setup Guide](./TECHNICAL-SETUP-GUIDE.md)
- [Claude Agent SDK Docs](https://docs.claude.com/en/api/agent-sdk/python)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Example Repository](https://github.com/kenneth-liao/claude-agent-sdk-intro)

---

**Happy Building! 🚀**
