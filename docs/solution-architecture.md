# Mission Control - Solution Architecture

**Project:** Mission Control - Autonomous AI-Powered Executive Team
**Author:** Mike
**Date:** 2025-10-15
**Version:** 1.0.0
**Architecture Status:** APPROVED FOR IMPLEMENTATION

---

## Executive Summary

Mission Control is a **standalone Python CLI application** that provides entrepreneurs and business leaders with an autonomous executive team powered by Claude Agent SDK. The system combines:

- **BMAD Method workflows** for structured business processes
- **big-3-super-agent patterns** for multi-agent orchestration and observability
- **Claude Agent SDK** for autonomous behaviors and persistent memory

**Key Differentiator:** Unlike traditional AI chatbots (reactive, stateless) or static productivity tools (passive, fragmented), Mission Control is **proactive, persistent, and self-extending**—agents work FOR you, learn YOUR business, and improve over time.

**Architecture Type:** Standalone CLI application with ClaudeSDKClient-based agent orchestration
**Deployment Model:** Self-hosted Python application (local data, privacy-first)
**Target Users:** Entrepreneurs, CEOs, business leaders
**Technology Stack:** Python 3.13+, Claude Agent SDK, Rich CLI, BMAD workflows, MCP integrations

---

## Table of Contents

1. [Technology Stack and Decisions](#1-technology-stack-and-decisions)
2. [System Architecture](#2-system-architecture)
3. [Component Architecture](#3-component-architecture)
4. [Data Architecture](#4-data-architecture)
5. [Agent Architecture](#5-agent-architecture)
6. [Workflow System](#6-workflow-system)
7. [Memory and Persistence](#7-memory-and-persistence)
8. [Observability and Monitoring](#8-observability-and-monitoring)
9. [Integration Architecture](#9-integration-architecture)
10. [Security and Privacy](#10-security-and-privacy)
11. [Proposed Source Tree](#11-proposed-source-tree)
12. [Architecture Decision Records](#12-architecture-decision-records)
13. [Implementation Guidance](#13-implementation-guidance)

---

## 1. Technology Stack and Decisions

### Core Dependencies

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Language** | Python | 3.13+ | Modern async/await, type hints, pattern matching |
| **Agent Framework** | Claude Agent SDK | ≥0.1.0 | Official Anthropic SDK for autonomous agents |
| **AI Model** | Claude Sonnet 4.5 | claude-sonnet-4-5-20250929 | Latest reasoning capabilities for all agents |
| **Terminal UI** | Rich | ≥13.9.0 | Beautiful CLI formatting, tables, progress bars |
| **Package Manager** | uv | ≥0.5.0 | Fast Python package management and script execution |
| **Environment Config** | python-dotenv | ≥1.0.0 | Environment variable management |
| **Data Validation** | Pydantic | ≥2.9.0 | Type-safe data models and validation |
| **HTTP Client** | urllib (stdlib) | - | Observability event posting (no extra deps) |
| **Date/Time** | datetime (stdlib) | - | Timestamps, scheduling |
| **JSON** | json (stdlib) | - | Agent registry, memory files |
| **Threading** | threading (stdlib) | - | Thread-safe registry operations |
| **Async** | asyncio (stdlib) | - | Async agent operations |

### Optional/Future Dependencies

| Category | Technology | Version | Use Case | Priority |
|----------|-----------|---------|----------|----------|
| **Browser Automation** | Gemini 2.5 Computer Use | latest | Web automation with vision | Phase 3 |
| **Voice Interface** | OpenAI Realtime API | latest | Voice-controlled orchestration | Phase 4 |
| **MCP: Calendar** | Google Calendar MCP | latest | Calendar integration | Phase 4 |
| **MCP: Email** | Gmail MCP | latest | Email summarization | Phase 4 |
| **MCP: Metrics** | Stripe MCP | latest | Revenue tracking | Phase 3 |
| **MCP: Accounting** | QuickBooks MCP | latest | Financial data | Phase 4 |
| **Observability Server** | claude-code-hooks-multi-agent-observability | latest | Event dashboard | Phase 2 |
| **Testing** | pytest | ≥8.0.0 | Unit and integration tests | Phase 1 |
| **Linting** | ruff | ≥0.6.0 | Code quality | Phase 1 |

### Development Dependencies

```toml
[project]
name = "mission-control"
version = "0.1.0"
description = "Autonomous AI-powered executive team"
requires-python = ">=3.13"
dependencies = [
    "claude-agent-sdk>=0.1.0",
    "rich>=13.9.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.6.0",
]
browser = [
    "google-genai>=0.3.0",  # Gemini Computer Use
    "playwright>=1.48.0",
]
voice = [
    "websocket-client>=1.8.0",
    "pyaudio>=0.2.14",
    "numpy>=2.0.0",
]

[project.scripts]
mission-control = "mission_control.main:main"
```

### Technology Rationale

**Python 3.13+:**
- Modern async/await for ClaudeSDKClient
- Type hints for maintainability
- Pattern matching for workflow logic
- Excellent Claude Agent SDK support

**Claude Agent SDK:**
- Official Anthropic framework
- Persistent agent sessions
- Hook system for autonomous behaviors
- MCP server integration
- Proven in big-3-super-agent production use

**Claude Sonnet 4.5 for All Agents:**
- Decision: Use same model for consistency initially
- Benefit: Uniform quality across all specialists
- Future: Can optimize with Haiku for Operator (fast daily planning)
- Cost: ~$30-50/month for active daily use (acceptable for target user)

**Rich CLI:**
- Production-proven UI library
- Beautiful terminal formatting without web overhead
- Panels, tables, progress bars, syntax highlighting
- Zero-configuration, works everywhere Python runs

**uv Package Manager:**
- 10-100x faster than pip
- Deterministic dependency resolution
- Script execution with inline deps
- Modern Python tooling

**No Database:**
- Decision: JSON files for persistence (not PostgreSQL/SQLite)
- Rationale: Simplicity, portability, human-readable, version-controllable
- Tradeoff: Not suitable for 10,000+ agents (acceptable for target use case)

**stdlib over dependencies:**
- Use `urllib` instead of `requests` (observability posting)
- Use `json` instead of `orjson` (readability over speed)
- Use `threading` instead of `multiprocessing` (simpler, sufficient)
- Rationale: Minimize dependencies, maximize reliability

---

## 2. System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Rich CLI                                                   │ │
│  │  - Panels (agent responses)                                │ │
│  │  - Tables (goals, metrics, schedules)                      │ │
│  │  - Progress bars (goal tracking)                           │ │
│  │  - Syntax highlighting (code, JSON)                        │ │
│  │  - Input prompts (user queries)                            │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Chief of Staff (Alex) - main.py                           │ │
│  │  - ClaudeSDKClient orchestrator                            │ │
│  │  - Context management (loads business memory)              │ │
│  │  - Delegation logic (routes to specialists)               │ │
│  │  - Workflow selection (BMAD template matching)            │ │
│  │  - Rich UI rendering                                       │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                    AGENT MANAGEMENT LAYER                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Agent Registry (agent_registry.py)                        │ │
│  │  - JSON-based persistence (data/agents/registry.json)     │ │
│  │  - Thread-safe operations                                  │ │
│  │  - Session management                                      │ │
│  │  - Agent lifecycle (create, resume, update, delete)       │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Agent Definitions (agent_definitions.py)                  │ │
│  │  - 5 core specialists (AgentDefinition configs)           │ │
│  │  - Dynamic agent templates                                 │ │
│  │  - System prompts per agent                                │ │
│  │  - Tool allowlists per agent                               │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                      AGENT EXECUTION LAYER                       │
│  ┌──────────────┬──────────────┬──────────────┬───────────────┐ │
│  │ Strategist   │ Planner      │ Operator     │ Analyst       │ │
│  │ (Jordan)     │ (Quinn)      │ (Taylor)     │ (Sam)         │ │
│  │ Sonnet 4.5   │ Sonnet 4.5   │ Sonnet 4.5   │ Sonnet 4.5    │ │
│  │              │              │              │               │ │
│  │ Vision       │ Goals        │ Daily        │ Metrics       │ │
│  │ Strategy     │ Rocks        │ Planning     │ Analysis      │ │
│  │ Values       │ Milestones   │ Priorities   │ Trends        │ │
│  └──────────────┴──────────────┴──────────────┴───────────────┘ │
│  ┌──────────────┬────────────────────────────────────────────┐  │
│  │ Researcher   │ Dynamic Agents (On-Demand)                 │  │
│  │ (Morgan)     │ - MarketResearchAgent                      │  │
│  │ Sonnet 4.5   │ - ContentWriter                            │  │
│  │              │ - DataScientist                            │  │
│  │ Research     │ - DevOpsEngineer                           │  │
│  │ Citations    │ - ...created by Alex as needed             │  │
│  └──────────────┴────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                   AUTONOMOUS BEHAVIORS LAYER                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Hooks (Claude SDK Hook System)                            │ │
│  │  - log_agent_actions.py (Stop hook)                        │ │
│  │  - goal_monitor.py (Stop hook)                             │ │
│  │  - pattern_detector.py (Stop hook)                         │ │
│  │  - daily_briefing.py (Notification hook - scheduled)       │ │
│  │  - send_observability_event.py (All hooks)                 │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                   PERSISTENCE & WORKFLOW LAYER                   │
│  ┌─────────────────────────┬────────────────────────────────┐   │
│  │  Memory System          │  BMAD Workflows                │   │
│  │  (memory_manager.py)    │  (workflow_engine.py)          │   │
│  │                         │                                │   │
│  │  • business_context     │  • daily-planning.yaml         │   │
│  │  • learned_preferences  │  • weekly-review.yaml          │   │
│  │  • interaction_logs/    │  • quarterly-planning.yaml     │   │
│  │  • goals/ (Rocks)       │  • strategic-session.yaml      │   │
│  │  • metrics/ (KPIs)      │  • research-brief.yaml         │   │
│  │  • notes/               │  • agent-improvement.yaml      │   │
│  └─────────────────────────┴────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                    TOOL & INTEGRATION LAYER                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Built-in Claude Tools                                     │ │
│  │  Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  MCP Servers (Model Context Protocol)                     │ │
│  │  - browser (Gemini Computer Use)                          │ │
│  │  - calendar (Google Calendar) - Phase 4                   │ │
│  │  - email (Gmail) - Phase 4                                │ │
│  │  - metrics (Stripe, QuickBooks) - Phase 3-4              │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                ↓↑
┌──────────────────────────────────────────────────────────────────┐
│                 OBSERVABILITY & MONITORING LAYER                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Observability System (observability.py)                   │ │
│  │  - Event streaming to dashboard (http://localhost:4000)   │ │
│  │  - AI-generated event summaries                           │ │
│  │  - Cost tracking (token usage)                            │ │
│  │  - Performance metrics (response times)                   │ │
│  │  - Pattern dashboards                                     │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### Architectural Style

**Pattern:** Layered Architecture with Event-Driven Extensions

1. **Presentation Layer** (Rich CLI) - User interaction
2. **Orchestration Layer** (Chief of Staff) - Request routing, context management
3. **Agent Management Layer** (Registry + Definitions) - Agent lifecycle
4. **Execution Layer** (5 Core + Dynamic Agents) - Task execution
5. **Behavior Layer** (Hooks) - Autonomous operations
6. **Persistence Layer** (Memory + Workflows) - Data storage
7. **Integration Layer** (Tools + MCPs) - External systems
8. **Observability Layer** - Monitoring and debugging

**Key Characteristics:**
- **Standalone**: Runs as independent Python process
- **Local-first**: All data stored locally (privacy)
- **Event-driven**: Hooks trigger on agent actions
- **Self-extending**: Dynamic agent creation
- **Observable**: Real-time event streaming

---

## 3. Component Architecture

### 3.1 Chief of Staff (Alex) - Orchestrator

**File:** `src/main.py`
**Role:** Primary user interface and delegation orchestrator
**Model:** Claude Sonnet 4.5

**Responsibilities:**
- Accept user input via Rich CLI
- Load business context from memory
- Classify user intent (greeting, strategic query, goal tracking, etc.)
- Select appropriate specialist or workflow
- Delegate to specialist with context transfer
- Monitor operator files for task completion
- Present results to user with Rich formatting
- Update memory based on interactions

**Key Functions:**
```python
async def main():
    """Main entry point - continuous conversation loop."""

async def load_context() -> BusinessContext:
    """Load business context, goals, preferences from memory."""

async def classify_intent(user_message: str) -> Intent:
    """Determine what kind of request this is."""

async def delegate_to_specialist(specialist: str, task: str, context: dict) -> OperatorFile:
    """Create specialist agent and delegate task."""

async def check_operator_status(operator_file: Path) -> TaskStatus:
    """Poll operator file for task completion."""

def display_response(agent_name: str, message: str, data: dict):
    """Render agent response with Rich formatting."""
```

**System Prompt Structure:**
```
You are Alex, Chief of Staff for [User Name].

ROLE:
You orchestrate an executive team of 5 specialist agents:
- Jordan (Strategist): Long-term vision, strategy, values
- Quinn (Planner): Quarterly goals, Rocks, milestones
- Taylor (Operator): Daily planning, task prioritization
- Sam (Analyst): Metrics, data analysis, business intelligence
- Morgan (Researcher): Deep research, competitive analysis

CAPABILITIES:
1. Context Awareness: Load business context, goals, preferences
2. Proactive Intelligence: Surface insights without being asked
3. Delegation: Route complex work to appropriate specialists
4. Memory Management: Learn and remember user preferences
5. Dynamic Agent Creation: Create new specialists on-demand

DELEGATION RULES:
- Strategic questions (10-year vision, values) → Jordan
- Quarterly planning, goal setting → Quinn
- Daily planning, task prioritization → Taylor
- Data analysis, metric tracking → Sam
- Research requests, competitive analysis → Morgan
- New capability needed → Ask to create new specialist

PERSONALITY:
- Professional yet warm
- Proactive (suggest actions)
- Context-aware (reference past conversations)
- Transparent (explain reasoning)
- Emoji: 🧑‍💼

[Append business context loaded from data/memory/business_context.json]
```

**ClaudeSDKClient Configuration:**
```python
options = ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": chief_of_staff_system_prompt
    },
    model="claude-sonnet-4-5-20250929",
    cwd=str(PROJECT_ROOT),
    permission_mode="bypassPermissions",
    setting_sources=["project"],
    hooks={
        "Stop": [HookMatcher(hooks=[log_hook, goal_monitor_hook, pattern_hook])],
        "PostToolUse": [HookMatcher(hooks=[context_extractor_hook])],
        "Notification": [HookMatcher(hooks=[scheduled_briefing_hook])]
    },
    allowed_tools=[
        "Read", "Write", "Edit", "Bash", "Glob", "Grep",
        "WebSearch", "WebFetch", "Task", "TodoWrite"
    ]
)
```

### 3.2 Agent Registry

**File:** `src/agent_registry.py`
**Role:** Manage agent lifecycle and session persistence

**Data Model:**
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List

class AgentMetadata(BaseModel):
    session_id: str
    type: str  # "core_specialist" | "dynamic_specialist"
    model: str = "claude-sonnet-4-5-20250929"
    version: str = "1.0.0"
    created_at: datetime
    created_by: Optional[str] = None  # "Alex" for dynamic agents
    last_used: Optional[datetime] = None
    last_improved: Optional[datetime] = None
    tools: List[str] = Field(default_factory=list)
    workflow_preference: Optional[str] = None
    usage_count: int = 0
    operator_files: List[str] = Field(default_factory=list)

class AgentRegistry(BaseModel):
    version: str = "1.0.0"
    agents: Dict[str, AgentMetadata] = Field(default_factory=dict)
```

**Key Operations:**
```python
class AgentRegistryManager:
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.lock = threading.Lock()
        self.registry = self._load()

    def register_agent(self, agent_name: str, metadata: AgentMetadata):
        """Add or update agent in registry."""

    def get_agent(self, agent_name: str) -> Optional[AgentMetadata]:
        """Retrieve agent metadata."""

    def list_agents(self, agent_type: Optional[str] = None) -> List[str]:
        """List all agents, optionally filtered by type."""

    def update_agent(self, agent_name: str, updates: dict):
        """Update agent metadata fields."""

    def delete_agent(self, agent_name: str):
        """Remove agent from registry."""

    def increment_usage(self, agent_name: str):
        """Track agent usage for improvement detection."""

    def add_operator_file(self, agent_name: str, operator_file: str):
        """Track operator files for agent."""
```

**Registry File Location:**
```
data/agents/registry.json
```

**Example Registry:**
```json
{
  "version": "1.0.0",
  "agents": {
    "strategist": {
      "session_id": "abc123def456",
      "type": "core_specialist",
      "model": "claude-sonnet-4-5-20250929",
      "version": "1.0.0",
      "created_at": "2025-10-15T10:00:00Z",
      "created_by": null,
      "last_used": "2025-10-15T14:30:00Z",
      "last_improved": null,
      "tools": ["Read", "Write", "WebSearch", "WebFetch"],
      "workflow_preference": "strategic-session.yaml",
      "usage_count": 12,
      "operator_files": []
    },
    "market-expansion-analyst": {
      "session_id": "xyz789ghi012",
      "type": "dynamic_specialist",
      "model": "claude-sonnet-4-5-20250929",
      "version": "1.1.0",
      "created_at": "2025-10-14T11:30:00Z",
      "created_by": "Alex",
      "last_used": "2025-10-15T09:15:00Z",
      "last_improved": "2025-10-15T08:00:00Z",
      "tools": ["Read", "Write", "WebSearch", "WebFetch", "mcp__browser__browser_use"],
      "workflow_preference": "eu-market-expansion.yaml",
      "usage_count": 5,
      "operator_files": [
        "operator_20251014_113045.md",
        "operator_20251015_091520.md"
      ]
    }
  }
}
```

### 3.3 Agent Definitions

**File:** `src/agent_definitions.py`
**Role:** Define system prompts and configurations for all agents

**Structure:**
```python
from claude_agent_sdk import AgentDefinition
from typing import Dict

# 5 Core Specialists
STRATEGIST_DEFINITION = AgentDefinition(
    description="Long-term vision, strategic direction, values clarification",
    prompt="""
You are Jordan, the Strategist.

EXPERTISE:
- 10-year vision, 3-year picture, 1-year goals
- Core values identification and alignment
- Strategic opportunity evaluation
- Competitive positioning
- Long-term thinking frameworks (Vision/Traction OS, Core Values exercises)

STYLE:
- Thoughtful, probing questions
- Long-term perspective
- Challenge assumptions constructively
- Emoji: 🎯

[Load business context vision section]
    """,
    model="claude-sonnet-4-5-20250929",
    tools=["Read", "Write", "WebSearch", "WebFetch"]
)

PLANNER_DEFINITION = AgentDefinition(
    description="Quarterly goals, Rocks framework, milestone tracking",
    prompt="""
You are Quinn, the Planner.

EXPERTISE:
- Rocks methodology (3-7 quarterly goals)
- OKRs (Objectives and Key Results)
- Milestone setting and tracking
- Quarterly reviews and retrospectives
- Progress monitoring

STYLE:
- Structured, goal-oriented
- Data-driven progress tracking
- Clear milestones and metrics
- Emoji: 📊

[Load active goals from data/goals/]
    """,
    model="claude-sonnet-4-5-20250929",
    tools=["Read", "Write", "Bash"]
)

OPERATOR_DEFINITION = AgentDefinition(
    description="Daily planning, time blocking, task prioritization",
    prompt="""
You are Taylor, the Operator.

EXPERTISE:
- Eisenhower Matrix (urgent/important prioritization)
- Time blocking and calendar optimization
- Daily planning and weekly prep
- GTD (Getting Things Done) principles
- Task breakdown and sequencing

STYLE:
- Tactical, action-oriented
- Efficiency-minded
- Fast execution focus
- Emoji: ⚡

[Load today's calendar if available]
    """,
    model="claude-sonnet-4-5-20250929",
    tools=["Read", "Write", "mcp__calendar__calendar_read"]
)

ANALYST_DEFINITION = AgentDefinition(
    description="Metrics tracking, trend analysis, business intelligence",
    prompt="""
You are Sam, the Analyst.

EXPERTISE:
- KPI tracking and dashboards
- Trend analysis and forecasting
- Root cause analysis
- Data visualization (terminal-based)
- Business intelligence insights

STYLE:
- Data-driven, analytical
- Clear visualizations
- Insight-focused
- Emoji: 📈

[Load metrics from data/metrics/]
    """,
    model="claude-sonnet-4-5-20250929",
    tools=["Read", "Write", "mcp__stripe__get_revenue", "mcp__quickbooks__get_expenses"]
)

RESEARCHER_DEFINITION = AgentDefinition(
    description="Deep research, competitive analysis, citations",
    prompt="""
You are Morgan, the Researcher.

EXPERTISE:
- Market research methodologies
- Competitive landscape analysis
- Citation standards (APA/MLA)
- Information synthesis
- Multi-source research

STYLE:
- Thorough, evidence-based
- Comprehensive coverage
- Proper citations
- Emoji: 🔍

TOOLS:
Use WebSearch, WebFetch, and browser_use extensively for research.
    """,
    model="claude-sonnet-4-5-20250929",
    tools=["Read", "Write", "WebSearch", "WebFetch", "mcp__browser__browser_use"]
)

# Agent Definition Registry
AGENT_DEFINITIONS: Dict[str, AgentDefinition] = {
    "strategist": STRATEGIST_DEFINITION,
    "planner": PLANNER_DEFINITION,
    "operator": OPERATOR_DEFINITION,
    "analyst": ANALYST_DEFINITION,
    "researcher": RESEARCHER_DEFINITION
}

def get_agent_definition(agent_name: str) -> AgentDefinition:
    """Get agent definition by name."""
    return AGENT_DEFINITIONS.get(agent_name)

def create_dynamic_agent_definition(
    agent_name: str,
    description: str,
    expertise: str,
    tools: List[str],
    model: str = "claude-sonnet-4-5-20250929"
) -> AgentDefinition:
    """Create new agent definition dynamically."""
    prompt = f"""
You are {agent_name}, a specialist agent.

EXPERTISE:
{expertise}

You were created on-demand to handle specific tasks that require your specialized knowledge.
Work autonomously, use all available tools, and provide thorough, actionable outputs.
    """

    return AgentDefinition(
        description=description,
        prompt=prompt,
        model=model,
        tools=tools
    )
```

### 3.4 Memory Manager

**File:** `src/memory_manager.py`
**Role:** Manage persistent business context and learned preferences

**Data Models:**
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CompanyInfo(BaseModel):
    name: str
    industry: str
    founding_date: Optional[datetime] = None
    mission: Optional[str] = None
    values: List[str] = Field(default_factory=list)

class Vision(BaseModel):
    ten_year: Optional[str] = None
    three_year: Optional[str] = None
    one_year: Optional[str] = None

class BusinessContext(BaseModel):
    version: str = "1.0.0"
    last_updated: datetime
    company: CompanyInfo
    vision: Vision
    current_priorities: List[str] = Field(default_factory=list)
    key_metrics: Dict[str, Any] = Field(default_factory=dict)

class LearnedPreferences(BaseModel):
    version: str = "1.0.0"
    last_updated: datetime
    communication_style: str = "professional"  # professional, casual, concise, detailed
    preferred_frameworks: List[str] = Field(default_factory=list)  # ["Rocks", "OKR", "Eisenhower Matrix"]
    decision_patterns: List[str] = Field(default_factory=list)
    recurring_topics: List[str] = Field(default_factory=list)
    preferred_agents: Dict[str, int] = Field(default_factory=dict)  # agent_name: usage_count
    notification_preferences: Dict[str, bool] = Field(default_factory=dict)
```

**Key Operations:**
```python
class MemoryManager:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.business_context_path = data_dir / "memory" / "business_context.json"
        self.preferences_path = data_dir / "memory" / "learned_preferences.json"

    def load_business_context(self) -> BusinessContext:
        """Load business context from disk."""

    def save_business_context(self, context: BusinessContext):
        """Save business context to disk."""

    def update_business_context(self, updates: dict):
        """Partial update of business context."""

    def load_preferences(self) -> LearnedPreferences:
        """Load learned preferences."""

    def save_preferences(self, prefs: LearnedPreferences):
        """Save learned preferences."""

    def learn_from_interaction(self, interaction: dict):
        """Update preferences based on user interaction."""

    def get_context_summary(self) -> str:
        """Generate text summary for agent system prompts."""
```

**File Locations:**
```
data/memory/business_context.json
data/memory/learned_preferences.json
data/memory/interaction_logs/2025-10-15.jsonl
```

### 3.5 Workflow Engine

**File:** `src/workflow_engine.py`
**Role:** Load and execute BMAD workflow templates

**Workflow Structure (YAML):**
```yaml
# workflows/daily-planning.yaml
name: daily-planning
description: "Daily planning with Eisenhower Matrix and time blocking"
author: "BMAD Method"
version: "1.0.0"

inputs:
  - name: calendar_events
    type: list
    required: false
  - name: active_goals
    type: list
    required: false

steps:
  - step: 1
    goal: "Review today's commitments"
    action: "Load calendar events and active goals"
    prompt: "What meetings/commitments do you have today?"

  - step: 2
    goal: "Identify high-priority tasks"
    action: "Apply Eisenhower Matrix"
    prompt: "What are your most important tasks (Urgent & Important)?"

  - step: 3
    goal: "Time blocking"
    action: "Assign tasks to calendar blocks"
    prompt: "When will you work on each priority task?"

  - step: 4
    goal: "Generate daily plan"
    action: "Create structured output"
    output_file: "output/daily-plans/{date}.md"
    template: "daily-plan-template.md"

outputs:
  - name: daily_plan_file
    description: "Daily plan markdown file"
    location: "output/daily-plans/{date}.md"
```

**Workflow Execution:**
```python
class WorkflowEngine:
    def __init__(self, workflows_dir: Path):
        self.workflows_dir = workflows_dir

    def load_workflow(self, workflow_name: str) -> dict:
        """Load workflow YAML."""

    async def execute_workflow(
        self,
        workflow_name: str,
        agent_client: ClaudeSDKClient,
        context: dict
    ) -> dict:
        """Execute workflow step-by-step."""
        workflow = self.load_workflow(workflow_name)

        results = {}
        for step in workflow["steps"]:
            # Build prompt with context
            prompt = self._render_prompt(step["prompt"], context)

            # Agent executes step
            response = await agent_client.query(prompt)

            # Extract result
            results[f"step_{step['step']}"] = response

            # Update context for next step
            context.update(results)

        # Generate outputs
        if "outputs" in workflow:
            self._generate_outputs(workflow["outputs"], results, context)

        return results
```

### 3.6 Observability System

**File:** `src/observability.py`
**Role:** Stream events to observability dashboard with AI summaries

**Event Model:**
```python
class ObservabilityEvent(BaseModel):
    source_app: str  # "mission-control: {agent_name}"
    session_id: str
    hook_event_type: str  # "PreToolUse", "PostToolUse", "Stop", etc.
    payload: Dict[str, Any]
    summary: Optional[str] = None  # AI-generated
    timestamp: int  # milliseconds since epoch
```

**Key Functions:**
```python
def send_observability_event(
    agent_name: str,
    hook_type: str,
    session_id: str,
    payload: dict,
    summary: Optional[str] = None,
    server_url: str = "http://localhost:4000/events"
):
    """Send event to observability server (fails silently)."""
    try:
        event = {
            "source_app": f"mission-control: {agent_name}",
            "session_id": session_id,
            "hook_event_type": hook_type,
            "payload": payload,
            "timestamp": int(datetime.now().timestamp() * 1000)
        }

        if summary:
            event["summary"] = summary

        req = urllib.request.Request(
            server_url,
            data=json.dumps(event).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=2) as response:
            pass  # Success

    except Exception:
        pass  # Never block operations due to observability failure

async def generate_event_summary(
    agent_name: str,
    hook_type: str,
    payload: dict
) -> Optional[str]:
    """Generate AI summary of event using Claude."""
    # Use fast query to generate 1-sentence summary
    prompt = f"""
Summarize this agent event in 1 concise sentence:

Agent: {agent_name}
Event: {hook_type}
Details: {json.dumps(payload, indent=2)}

Summary:
    """

    try:
        response = await query(prompt, model="claude-sonnet-4-5-20250929")
        return response.strip()
    except Exception:
        return None
```

---

## 4. Data Architecture

### 4.1 Directory Structure

```
data/                                    # All persistent data (gitignored)
├── agents/                             # Agent registry and workspaces
│   ├── registry.json                   # Master agent registry
│   ├── strategist/                     # Strategist workspace
│   │   ├── sessions/                  # Session transcripts
│   │   └── operator_*.md              # Operator files (if any)
│   ├── planner/                       # Planner workspace
│   ├── operator/                      # Operator workspace
│   ├── analyst/                       # Analyst workspace
│   ├── researcher/                    # Researcher workspace
│   └── market-expansion-analyst/      # Dynamic agent workspace
│       ├── sessions/
│       ├── operator_20251014_113045.md
│       └── browser_tool/              # Screenshots from browser use
├── memory/                            # Business context and preferences
│   ├── business_context.json          # Company info, vision, priorities
│   ├── learned_preferences.json       # Communication style, frameworks
│   └── interaction_logs/              # Conversation history
│       ├── 2025-10-15.jsonl          # Daily log files (JSONL format)
│       └── 2025-10-14.jsonl
├── goals/                             # Rocks framework data
│   ├── 2025-Q4-rocks.json            # Current quarter goals
│   ├── 2025-Q3-rocks.json            # Historical goals
│   └── archive/                       # Completed goals
├── metrics/                           # Business metrics
│   ├── scorecard.json                 # Current KPIs
│   └── historical/                    # Time-series data
│       ├── 2025-10.json
│       └── 2025-09.json
└── notes/                             # User notes and documents
    ├── strategic-thoughts/            # Strategic session outputs
    │   └── 2025-10-14-b2c-evaluation.md
    └── meeting-notes/                 # Meeting capture
        └── 2025-10-15-investor-meeting.md
```

### 4.2 Data Schemas

**Agent Registry (data/agents/registry.json):**
```json
{
  "version": "1.0.0",
  "agents": {
    "{agent_name}": {
      "session_id": "string",
      "type": "core_specialist | dynamic_specialist",
      "model": "claude-sonnet-4-5-20250929",
      "version": "1.0.0",
      "created_at": "ISO8601 timestamp",
      "created_by": "Alex | null",
      "last_used": "ISO8601 timestamp",
      "last_improved": "ISO8601 timestamp | null",
      "tools": ["tool1", "tool2"],
      "workflow_preference": "workflow-name.yaml | null",
      "usage_count": 0,
      "operator_files": ["file1.md", "file2.md"]
    }
  }
}
```

**Business Context (data/memory/business_context.json):**
```json
{
  "version": "1.0.0",
  "last_updated": "ISO8601 timestamp",
  "company": {
    "name": "Acme Corp",
    "industry": "SaaS",
    "founding_date": "2020-01-15",
    "mission": "Empower entrepreneurs with AI",
    "values": ["Innovation", "Integrity", "Customer-first"]
  },
  "vision": {
    "ten_year": "Leading AI productivity platform globally",
    "three_year": "10,000 active users, $10M ARR",
    "one_year": "1,000 users, profitable, enterprise tier launched"
  },
  "current_priorities": [
    "Launch enterprise tier (Q4 2025)",
    "Improve customer retention to 95%",
    "Hire sales lead"
  ],
  "key_metrics": {
    "arr": 450000,
    "users": 250,
    "churn_rate": 0.08
  }
}
```

**Learned Preferences (data/memory/learned_preferences.json):**
```json
{
  "version": "1.0.0",
  "last_updated": "ISO8601 timestamp",
  "communication_style": "professional",
  "preferred_frameworks": ["Rocks", "Eisenhower Matrix", "OKR"],
  "decision_patterns": ["data-driven", "long-term-focus"],
  "recurring_topics": ["international_expansion", "hiring", "product_development"],
  "preferred_agents": {
    "strategist": 12,
    "planner": 8,
    "analyst": 15,
    "researcher": 6,
    "operator": 30
  },
  "notification_preferences": {
    "daily_briefing": true,
    "weekly_review": true,
    "goal_alerts": true
  }
}
```

**Interaction Logs (data/memory/interaction_logs/2025-10-15.jsonl):**
```jsonl
{"timestamp": "2025-10-15T10:30:00Z", "agent": "Alex", "type": "user_message", "content": "Help me plan my day", "session_id": "abc123"}
{"timestamp": "2025-10-15T10:30:15Z", "agent": "Alex", "type": "delegation", "to": "operator", "task": "daily planning", "session_id": "abc123"}
{"timestamp": "2025-10-15T10:32:45Z", "agent": "operator", "type": "workflow_execution", "workflow": "daily-planning.yaml", "status": "complete", "session_id": "def456"}
```

**Quarterly Goals (data/goals/2025-Q4-rocks.json):**
```json
{
  "quarter": "Q4",
  "year": 2025,
  "created_at": "2025-10-01T00:00:00Z",
  "rocks": [
    {
      "id": "Q4-2025-R1",
      "title": "Launch enterprise tier product",
      "description": "Complete enterprise features: SSO, RBAC, audit logs",
      "owner": "Mike",
      "due_date": "2025-12-31",
      "progress": 45,
      "status": "in_progress",
      "milestones": [
        {"title": "SSO integration", "due": "2025-11-15", "complete": true},
        {"title": "RBAC implementation", "due": "2025-12-01", "complete": false},
        {"title": "Beta customer onboarding", "due": "2025-12-15", "complete": false}
      ],
      "metrics": {
        "success_criteria": "5 enterprise customers signed",
        "current_value": 2
      }
    }
  ]
}
```

**Operator File (data/agents/planner/operator_20251015_103045.md):**
```markdown
# Operator File - Quarterly Planning

**Agent:** planner
**Task:** Help define Q4 2025 goals using Rocks framework
**Status:** COMPLETE
**Created:** 2025-10-15T10:30:45Z
**Completed:** 2025-10-15T10:47:32Z

## Task Description

User requested help planning Q4 2025 goals. Executed quarterly-planning.yaml workflow.

## Workflow Execution

### Step 1: Review Q3 2025 Performance
- Revenue goal: Achieved 92% ($460K vs $500K target)
- Product launch: Complete ✅
- Hiring goal: Missed (hired 2 vs 3 planned)

### Step 2: Define Q4 Rocks
Identified 5 priority goals for Q4 2025:

1. **Launch Enterprise Tier** - Complete SSO, RBAC, audit logs (Due: Dec 31)
2. **Achieve $600K Revenue** - 20% growth over Q3 (Due: Dec 31)
3. **Reduce Onboarding Time** - From 7 days to 3 days (Due: Nov 30)
4. **Hire Enterprise Sales Lead** - 5+ years SaaS experience (Due: Nov 15)
5. **Improve Customer Retention** - 95% retention rate target (Due: Dec 31)

### Step 3: Set Milestones
[Details for each Rock...]

### Step 4: Generate Outputs
Created structured goal file with milestones and metrics.

## Artifacts Generated

- `data/goals/2025-Q4-rocks.json` - Structured goal data
- `output/quarterly-plans/2025-Q4-plan.md` - Human-readable plan

## Next Steps

1. Review goals with team
2. Schedule bi-weekly check-ins with Quinn (Planner)
3. Set up metric tracking with Sam (Analyst)

## Agent Recommendations

- Set calendar reminders for milestone deadlines
- Configure goal monitoring hooks to alert if >20% behind schedule
- Consider delegating hiring to HR specialist (dynamic agent)

---

**Status:** COMPLETE ✅
```

---

## 5. Agent Architecture

### 5.1 Agent Lifecycle

```
1. CREATION
   - Core agents: Initialized on first run (5 specialists)
   - Dynamic agents: Created by Alex on-demand
   ↓
2. REGISTRATION
   - Add to agent registry (data/agents/registry.json)
   - Create agent workspace directory
   - Generate session ID
   ↓
3. CONFIGURATION
   - Load AgentDefinition (system prompt, tools, model)
   - Configure ClaudeSDKClient options
   - Register hooks
   ↓
4. EXECUTION
   - Spawn agent with ClaudeSDKClient
   - Transfer context from Chief of Staff
   - Execute task/workflow
   - Create operator file for status
   ↓
5. MONITORING
   - Hooks fire on tool use, completion, errors
   - Events streamed to observability dashboard
   - Operator file updated with progress
   ↓
6. COMPLETION
   - Operator file marked COMPLETE
   - Results saved to workspace
   - Usage count incremented in registry
   ↓
7. LEARNING (optional)
   - If usage_count >= 3: Trigger improvement analysis
   - Agent-Improver evaluates performance
   - System prompt updated, tools added
   - Version incremented
   ↓
8. PERSISTENCE
   - Session continues across restarts
   - Registry maintains agent metadata
   - Workspace preserves operator files
```

### 5.2 Agent Communication Patterns

**Pattern 1: Chief of Staff → Specialist (Synchronous)**
```python
# User requests strategic thinking
user_message = "Should we pivot to B2C?"

# Alex delegates to Strategist
async with ClaudeSDKClient(options=strategist_options) as strategist:
    context = {
        "user_question": user_message,
        "business_context": memory_manager.load_business_context(),
        "current_market": "B2B SaaS"
    }

    response = await strategist.query(
        f"User asks: {user_message}\n\nContext: {json.dumps(context)}\n\nProvide strategic analysis."
    )

    # Alex presents Strategist's response
    display_response("Strategist (Jordan)", response)
```

**Pattern 2: Chief of Staff → Specialist (Asynchronous via Operator File)**
```python
# User requests research (long-running)
user_message = "Research EU SaaS market opportunity"

# Alex creates operator file
operator_file = await create_operator_file(
    agent_name="researcher",
    task=user_message
)

# Alex spawns researcher in background thread
thread = threading.Thread(
    target=execute_agent_task,
    args=("researcher", user_message, operator_file),
    daemon=True
)
thread.start()

# Alex tells user
console.print("Morgan (Researcher) is working on this. I'll notify you when ready.")

# Meanwhile, user can continue conversation with Alex

# Later, Alex checks operator file
status = check_operator_file(operator_file)
if status == "COMPLETE":
    result = read_operator_file(operator_file)
    display_response("Researcher (Morgan)", result)
```

**Pattern 3: Specialist → Dynamic Agent (Cascade)**
```python
# Strategist realizes market research needed
# Strategist (via ClaudeSDKClient) uses Task tool to spawn Researcher
await strategist_client.delegate_to_subagent(
    agent="researcher",
    context={"research_topic": "B2C market sizing"}
)

# Or, Strategist can request Alex create new specialist
strategist_response = """
I need specialized legal expertise for international expansion.
I recommend creating a 'Legal Advisor' agent to analyze EU regulations.
"""

# Alex receives recommendation, asks user
console.print(Panel(
    "Strategist suggests creating Legal Advisor agent. Approve? [Y/n]",
    title="🎯 Jordan (Strategist)"
))

if user_approves():
    legal_agent = create_dynamic_agent(
        name="legal-advisor",
        expertise="International business law, GDPR, compliance",
        tools=["Read", "Write", "WebSearch", "WebFetch"]
    )
```

### 5.3 Tool Permissions Per Agent

| Agent | Read | Write | Edit | Bash | Glob | Grep | WebSearch | WebFetch | browser_use | calendar | email | metrics |
|-------|------|-------|------|------|------|------|-----------|----------|------------|----------|-------|---------|
| **Chief of Staff (Alex)** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| **Strategist (Jordan)** | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Planner (Quinn)** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Operator (Taylor)** | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Analyst (Sam)** | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Researcher (Morgan)** | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Dynamic Agents** | ✅ | ✅ | Varies | ❌ | ✅ | ✅ | Varies | Varies | Varies | ❌ | ❌ | ❌ |

**Rationale:**
- **Alex**: Full permissions (orchestrator needs access to everything)
- **Strategist**: Read-heavy, web research for strategic intel
- **Planner**: Needs Write for goals, calendar access for planning
- **Operator**: Minimal tools, focuses on daily planning
- **Analyst**: Metrics access, read/write for analysis reports
- **Researcher**: Web tools + browser automation for deep research
- **Dynamic Agents**: Tailored permissions based on role

---

## 6. Workflow System

### 6.1 BMAD Workflow Templates

**Core Workflows (Phase 1-2):**

1. **daily-planning.yaml** - Eisenhower Matrix, time blocking
2. **weekly-review.yaml** - Wins, lessons, next week priorities
3. **quarterly-planning.yaml** - Rocks definition, milestone setting
4. **strategic-session.yaml** - 10-year vision, 3-year picture, values
5. **goal-tracking.yaml** - Progress monitoring, off-track detection
6. **meeting-notes.yaml** - Action items, decisions, follow-ups
7. **research-brief.yaml** - Deep research with citations
8. **metric-analysis.yaml** - Trend detection, insight generation
9. **agent-improvement.yaml** - Self-improvement workflow for agents
10. **agent-creation.yaml** - Dynamic agent definition workflow

### 6.2 Workflow Execution Flow

```
1. USER REQUEST
   "Help me plan Q4 2025"
   ↓
2. ALEX (Chief of Staff) analyzes request
   - Intent: Quarterly planning
   - Specialist: Planner (Quinn)
   - Workflow: quarterly-planning.yaml
   ↓
3. ALEX loads context
   - Previous quarter performance (data/goals/2025-Q3-rocks.json)
   - Business priorities (data/memory/business_context.json)
   - Learned preferences (preferred_frameworks: ["Rocks"])
   ↓
4. ALEX delegates to QUINN
   - Creates ClaudeSDKClient for Planner
   - Transfers context
   - Assigns workflow: quarterly-planning.yaml
   ↓
5. QUINN executes workflow steps
   Step 1: Review previous quarter
   Step 2: Define 3-7 Rocks for Q4
   Step 3: Set milestones per Rock
   Step 4: Define success metrics
   Step 5: Generate structured output
   ↓
6. QUINN writes outputs
   - data/goals/2025-Q4-rocks.json (structured data)
   - output/quarterly-plans/2025-Q4-plan.md (human-readable)
   ↓
7. HOOKS fire
   - log_agent_actions.py: Logs workflow completion
   - goal_monitor.py: Sets up monitoring for new goals
   - send_observability_event.py: Streams event to dashboard
   ↓
8. ALEX presents results
   - Rich table with 5 Rocks
   - Progress bars (0% → 100%)
   - Next steps recommendations
```

### 6.3 Workflow Template Format

**Example: daily-planning.yaml**
```yaml
name: daily-planning
version: "1.0.0"
description: "Daily planning with Eisenhower Matrix and time blocking"
author: "BMAD Method"
agent_preference: "operator"  # Taylor is ideal for this workflow

inputs:
  - name: calendar_events
    type: list
    description: "Today's meetings and commitments"
    required: false
    source: "mcp__calendar__calendar_read"

  - name: active_goals
    type: list
    description: "Current quarter Rocks"
    required: false
    source: "data/goals/2025-Q4-rocks.json"

steps:
  - step: 1
    id: review_commitments
    goal: "Review today's schedule and commitments"
    action: |
      Review calendar events and identify time blocks available for focused work.
      Note any meetings or deadlines that constrain your day.
    prompt: |
      Today's calendar:
      {calendar_events}

      Active goals:
      {active_goals}

      What commitments do you have today?

  - step: 2
    id: identify_priorities
    goal: "Identify high-priority tasks using Eisenhower Matrix"
    action: |
      Apply Eisenhower Matrix to classify tasks:
      - Quadrant 1: Urgent & Important (DO FIRST)
      - Quadrant 2: Important, Not Urgent (SCHEDULE)
      - Quadrant 3: Urgent, Not Important (DELEGATE)
      - Quadrant 4: Neither (ELIMINATE)
    prompt: |
      Based on your goals and commitments, what are your tasks for today?

      For each task, classify into Eisenhower Matrix quadrants.
      Focus on Quadrant 1 (Urgent & Important) and Quadrant 2 (Important, Not Urgent).

  - step: 3
    id: time_blocking
    goal: "Assign tasks to specific time blocks"
    action: |
      Create time blocks for focused work on high-priority tasks.
      Recommend 90-minute blocks for deep work.
    prompt: |
      Based on your priorities and available time, when will you work on each task?

      Suggest optimal time blocks considering:
      - Your peak productivity hours
      - Meeting schedule
      - Task complexity (deep work needs longer blocks)

  - step: 4
    id: generate_plan
    goal: "Generate structured daily plan document"
    action: "Write daily plan to output file"
    output_file: "output/daily-plans/{date}.md"
    template: |
      # Daily Plan - {date}

      ## Today's Focus
      {focus_statement}

      ## Schedule
      {time_blocks}

      ## Eisenhower Matrix

      ### Quadrant 1: Urgent & Important (DO FIRST)
      {q1_tasks}

      ### Quadrant 2: Important, Not Urgent (SCHEDULE)
      {q2_tasks}

      ### Quadrant 3: Urgent, Not Important (DELEGATE)
      {q3_tasks}

      ### Quadrant 4: Neither (ELIMINATE)
      {q4_tasks}

      ## Notes
      {user_notes}

outputs:
  - name: daily_plan_file
    description: "Daily plan markdown file"
    location: "output/daily-plans/{date}.md"

  - name: focus_tasks
    description: "List of Quadrant 1 tasks"
    type: "list"

validation:
  - check: "At least 1 Quadrant 1 task identified"
  - check: "Time blocks don't overlap with meetings"
  - check: "Output file created successfully"
```

---

## 7. Memory and Persistence

### 7.1 Memory Types

**Business Context Memory:**
- Location: `data/memory/business_context.json`
- Content: Company info, vision, values, priorities, key metrics
- Update Frequency: As business evolves (manual + automatic)
- Loaded By: All agents in system prompts

**Learned Preferences Memory:**
- Location: `data/memory/learned_preferences.json`
- Content: Communication style, frameworks, decision patterns, agent preferences
- Update Frequency: After every interaction (pattern_detector.py hook)
- Used For: Personalizing agent behavior

**Interaction Logs:**
- Location: `data/memory/interaction_logs/{date}.jsonl`
- Content: Conversation history (JSONL format for streaming)
- Retention: 90 days (configurable)
- Used For: Pattern detection, context retrieval, debugging

**Goal Memory:**
- Location: `data/goals/{year}-{quarter}-rocks.json`
- Content: Quarterly goals (Rocks framework), milestones, progress
- Update Frequency: Real-time (goal_monitor.py hook)
- Used For: Progress tracking, off-track alerts

**Metrics Memory:**
- Location: `data/metrics/scorecard.json` + `historical/{year}-{month}.json`
- Content: Business KPIs (revenue, users, churn, etc.)
- Update Frequency: Daily (via MCP integrations or manual)
- Used For: Trend analysis, dashboards, alerts

### 7.2 Memory Loading Strategy

**On Application Startup:**
```python
async def initialize_mission_control():
    # Load core memory
    business_context = memory_manager.load_business_context()
    preferences = memory_manager.load_preferences()
    active_goals = load_active_goals()  # Current quarter

    # Generate context summary for Chief of Staff
    context_summary = f"""
BUSINESS CONTEXT:
Company: {business_context.company.name}
Industry: {business_context.company.industry}
Mission: {business_context.company.mission}
Values: {', '.join(business_context.company.values)}

VISION:
10-Year: {business_context.vision.ten_year}
3-Year: {business_context.vision.three_year}
1-Year: {business_context.vision.one_year}

CURRENT PRIORITIES:
{chr(10).join(f"- {p}" for p in business_context.current_priorities)}

ACTIVE GOALS (Q4 2025):
{chr(10).join(f"- {rock['title']} ({rock['progress']}% complete)" for rock in active_goals)}

COMMUNICATION PREFERENCES:
Style: {preferences.communication_style}
Preferred Frameworks: {', '.join(preferences.preferred_frameworks)}
    """

    # Append to Chief of Staff system prompt
    chief_of_staff_options.system_prompt["append"] += f"\n\n{context_summary}"
```

**On Agent Delegation:**
```python
async def delegate_to_specialist(specialist_name: str, task: str):
    # Load relevant context for specialist
    if specialist_name == "planner":
        context = {
            "active_goals": load_active_goals(),
            "previous_quarter": load_goals("2025-Q3"),
            "calendar": await get_calendar_events()
        }
    elif specialist_name == "analyst":
        context = {
            "metrics": load_metrics(),
            "historical_data": load_historical_metrics(months=3)
        }
    elif specialist_name == "researcher":
        context = {
            "past_research": load_research_notes(),
            "company_context": memory_manager.load_business_context()
        }

    # Append to specialist system prompt
    specialist_prompt = f"{base_prompt}\n\nCONTEXT FOR THIS TASK:\n{json.dumps(context, indent=2)}"
```

### 7.3 Memory Update Triggers

**Hook: Stop (after every conversation turn)**
```python
# .claude/hooks/log_agent_actions.py
async def stop_hook(input_data: dict, tool_use_id: str, context: HookContext):
    # Log conversation
    log_interaction(
        agent=context.agent_name,
        timestamp=datetime.now(),
        content=input_data.get("response"),
        session_id=context.session_id
    )

    # Update learned preferences
    if detected_preference(input_data):
        update_preferences(preference_data)

    return {}
```

**Hook: PostToolUse (after Write/Edit operations)**
```python
# .claude/hooks/context_extractor.py
async def post_tool_use_hook(input_data: dict, tool_use_id: str, context: HookContext):
    tool_name = input_data.get("tool_name")
    tool_input = input_data.get("tool_input", {})

    # If wrote to goals directory, update goal cache
    if tool_name == "Write" and "data/goals/" in tool_input.get("file_path", ""):
        refresh_goal_cache()

    # If wrote to metrics directory, trigger analysis
    if tool_name == "Write" and "data/metrics/" in tool_input.get("file_path", ""):
        schedule_metric_analysis()

    return {}
```

---

## 8. Observability and Monitoring

### 8.1 Observability Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  MISSION CONTROL AGENTS                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Hook Execution                                          │   │
│  │  - PreToolUse, PostToolUse, Stop, Notification, etc.    │   │
│  │  - Capture event data                                    │   │
│  │  - Generate AI summary (optional)                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  send_observability_event()                              │   │
│  │  - Format event JSON                                     │   │
│  │  - HTTP POST to server                                   │   │
│  │  - Fail silently (non-blocking)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                 HTTP POST (port 4000)
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  OBSERVABILITY SERVER                                           │
│  (claude-code-hooks-multi-agent-observability)                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Event Receiver (/events endpoint)                       │   │
│  │  - Accept JSON events                                    │   │
│  │  - Store in memory/DB                                    │   │
│  │  - Broadcast to WebSocket clients                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↓                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Web Dashboard (Next.js)                                 │   │
│  │  - Real-time event stream                                │   │
│  │  - Agent activity timelines                              │   │
│  │  - Cost tracking                                         │   │
│  │  - Performance metrics                                   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
                     Browser (localhost:3000)
```

### 8.2 Event Types

| Hook Type | Trigger | Data Captured | Use Case |
|-----------|---------|---------------|----------|
| **PreToolUse** | Before tool execution | tool_name, tool_input, agent_name | Track what tools agents are using |
| **PostToolUse** | After tool execution | tool_name, tool_result, execution_time | Monitor tool success/failure, performance |
| **Stop** | Conversation turn ends | response, token_count, session_id | Log conversations, track costs |
| **Notification** | Scheduled event | notification_type, payload | Track autonomous behaviors |
| **SubagentStop** | Subagent task completes | subagent_name, result | Monitor delegation |
| **SessionStart** | Agent session begins | agent_name, session_id | Track agent creation |
| **SessionEnd** | Agent session ends | duration, tokens_used | Calculate session costs |

### 8.3 Event Schema

```json
{
  "source_app": "mission-control: {agent_name}",
  "session_id": "abc123def456",
  "hook_event_type": "PostToolUse",
  "timestamp": 1728998400000,
  "payload": {
    "tool_name": "Write",
    "tool_input": {
      "file_path": "data/goals/2025-Q4-rocks.json",
      "content": "{...}"
    },
    "tool_result": "File written successfully",
    "execution_time_ms": 45
  },
  "summary": "Agent Planner wrote Q4 goals to data/goals/2025-Q4-rocks.json with 5 Rocks defined"
}
```

### 8.4 Cost Tracking

**Token Usage Tracking:**
```python
# Track tokens per agent
token_tracker = {
    "alex": {"input": 0, "output": 0, "cost": 0.0},
    "strategist": {"input": 0, "output": 0, "cost": 0.0},
    "planner": {"input": 0, "output": 0, "cost": 0.0},
    # ...
}

# Stop hook updates costs
async def stop_hook(input_data: dict, tool_use_id: str, context: HookContext):
    token_data = input_data.get("token_usage", {})
    agent_name = context.agent_name

    token_tracker[agent_name]["input"] += token_data.get("input_tokens", 0)
    token_tracker[agent_name]["output"] += token_data.get("output_tokens", 0)

    # Calculate cost (Sonnet 4.5 pricing)
    input_cost = token_data.get("input_tokens", 0) * 0.003 / 1000  # $3/1M input tokens
    output_cost = token_data.get("output_tokens", 0) * 0.015 / 1000  # $15/1M output tokens
    token_tracker[agent_name]["cost"] += input_cost + output_cost

    # Send to observability
    send_observability_event(
        agent_name=agent_name,
        hook_type="CostTracking",
        session_id=context.session_id,
        payload={
            "tokens_used": token_data,
            "cost_usd": input_cost + output_cost
        }
    )
```

---

## 9. Integration Architecture

### 9.1 Multi-Provider Tool Strategy

**Built-in Claude Tools (Always Available):**
- Read, Write, Edit - File operations
- Bash - Shell command execution
- Glob, Grep - File searching
- WebSearch, WebFetch - Internet access

**Gemini Computer Use (Browser Automation):**
```python
# MCP Server for Gemini Browser
from claude_agent_sdk import tool, create_sdk_mcp_server
from google import genai

@tool(
    "browser_use",
    "Automate web tasks with vision-based browser control. Navigate, click, extract data, validate UI.",
    {"task": str, "url": str}
)
async def browser_use_tool(args: dict) -> dict:
    """Execute browser task using Gemini Computer Use."""
    task = args["task"]
    url = args.get("url")

    # Initialize Gemini client
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)

    # Setup Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        if url:
            page.goto(url)

        # Take screenshot
        screenshot = page.screenshot()

        # Send to Gemini with task
        response = gemini_client.chat.send_message(
            messages=[
                Content(parts=[
                    Part(text=f"Task: {task}"),
                    Part(inline_data={"mime_type": "image/png", "data": base64.b64encode(screenshot)})
                ])
            ],
            model="gemini-2.5-computer-use-preview-10-2025"
        )

        # Parse Gemini actions and execute
        # ... (action execution logic)

        browser.close()

    return {"ok": True, "result": response.text}

# Register as MCP server
browser_server = create_sdk_mcp_server(
    name="browser",
    version="1.0.0",
    tools=[browser_use_tool]
)
```

**OpenAI Voice (Optional - Phase 4):**
```python
# Future: Voice interface using OpenAI Realtime API
# Would replace/augment text input to Alex (Chief of Staff)

import websocket
import pyaudio

class VoiceInterface:
    def __init__(self):
        self.ws_url = "wss://api.openai.com/v1/realtime?model=gpt-realtime-2025-08-28"
        self.audio_stream = pyaudio.PyAudio().open(...)

    async def voice_to_text(self) -> str:
        """Convert voice input to text using OpenAI Realtime API."""

    async def text_to_voice(self, text: str):
        """Convert agent response to voice output."""
```

**MCP Servers (Calendar, Email, Metrics):**
```yaml
# .claude/settings.json (future)
{
  "mcpServers": {
    "browser": {
      "command": "python",
      "args": ["src/mcp_servers/browser_server.py"]
    },
    "google-calendar": {
      "command": "mcp-google-calendar",
      "args": ["--auth", ".credentials/google.json"]
    },
    "gmail": {
      "command": "mcp-gmail",
      "args": ["--auth", ".credentials/google.json"]
    },
    "stripe": {
      "command": "mcp-stripe",
      "env": {
        "STRIPE_API_KEY": "${STRIPE_API_KEY}"
      }
    }
  }
}
```

### 9.2 Integration Priorities by Phase

**Phase 1 (Foundation):**
- ✅ Built-in Claude tools (Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch)

**Phase 2 (Autonomous Behaviors):**
- ✅ Observability server integration (event streaming)

**Phase 3 (Dynamic Agents):**
- ✅ Gemini Computer Use (browser automation)
- ✅ Stripe MCP (revenue metrics)

**Phase 4 (Advanced Integrations):**
- ⏳ Google Calendar MCP (schedule awareness)
- ⏳ Gmail MCP (email summaries)
- ⏳ QuickBooks MCP (financial data)
- ⏳ OpenAI Realtime API (voice interface)

---

## 10. Security and Privacy

### 10.1 Data Privacy

**Principles:**
1. **100% Local Storage** - No cloud persistence (data/ directory gitignored)
2. **User Controls All Data** - data/ directory is human-readable, editable, exportable
3. **Transparent API Usage** - Only prompts/responses sent to Anthropic/OpenAI/Google APIs
4. **No Telemetry** - No anonymous usage tracking without explicit consent
5. **Secure Credentials** - API keys in .env file (gitignored)

**Data Classification:**
```
PRIVATE (Never leaves local machine):
- data/memory/business_context.json (company info, vision)
- data/goals/ (quarterly objectives)
- data/metrics/ (business KPIs)
- data/notes/ (strategic thoughts, meeting notes)

SENT TO AI PROVIDERS (for agent operation):
- User prompts
- Agent system prompts (context summaries)
- File contents when agents use Read/Write tools
- Web search queries

SENT TO OBSERVABILITY SERVER (optional, localhost only):
- Event metadata (agent names, tool usage, timestamps)
- AI-generated summaries (no raw business data)
```

### 10.2 Access Control

**File System Permissions:**
```python
# Agents restricted to PROJECT_ROOT
ClaudeAgentOptions(
    cwd=str(PROJECT_ROOT),  # Agents can't access files outside this directory
    permission_mode="bypassPermissions",  # Trust agents within PROJECT_ROOT
)

# For extra safety, validate file paths in PreToolUse hook
async def validate_file_access_hook(input_data: dict, tool_use_id: str, context: HookContext):
    tool_name = input_data.get("tool_name")
    if tool_name in ["Read", "Write", "Edit"]:
        file_path = Path(input_data.get("tool_input", {}).get("file_path", ""))

        # Ensure path is within PROJECT_ROOT
        if not file_path.resolve().is_relative_to(PROJECT_ROOT.resolve()):
            raise PermissionError(f"Access denied: {file_path} is outside project root")

    return {}
```

**API Key Security:**
```bash
# .env file (gitignored)
ANTHROPIC_API_KEY=sk-ant-api03-...
GEMINI_API_KEY=...
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_test_...
```

```python
# Load from environment
from dotenv import load_dotenv
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in .env file")
```

### 10.3 Rate Limiting and Cost Control

**Token Budget Enforcement:**
```python
# Track daily token usage
daily_budget = {
    "date": "2025-10-15",
    "tokens_used": 0,
    "tokens_limit": 1000000,  # 1M tokens/day (~$18 at Sonnet 4.5 pricing)
    "cost_usd": 0.0,
    "cost_limit": 50.0  # $50/day
}

async def check_budget_hook(input_data: dict, tool_use_id: str, context: HookContext):
    """Prevent runaway costs."""
    if daily_budget["cost_usd"] >= daily_budget["cost_limit"]:
        raise RuntimeError(f"Daily cost limit reached: ${daily_budget['cost_limit']}")

    return {}
```

**Agent-Specific Limits:**
```python
# Limit operator file execution time
OPERATOR_FILE_TIMEOUT = 600  # 10 minutes max per task

async def execute_agent_task_with_timeout(agent_name: str, task: str, operator_file: Path):
    try:
        await asyncio.wait_for(
            execute_agent_task(agent_name, task, operator_file),
            timeout=OPERATOR_FILE_TIMEOUT
        )
    except asyncio.TimeoutError:
        operator_file.write_text(f"Status: TIMEOUT\n\nTask exceeded {OPERATOR_FILE_TIMEOUT}s limit.")
```

---

## 11. Proposed Source Tree

```
mission-control-system/
├── .env.example                        # Environment template
├── .gitignore                          # Ignore data/, .env, __pycache__, etc.
├── README.md                           # Project README
├── pyproject.toml                      # Python project config (uv)
├── uv.lock                             # Locked dependencies
│
├── .claude/                            # Claude Code configuration
│   ├── settings.json                  # Hook registration, MCP servers
│   ├── hooks/                         # Autonomous behavior hooks
│   │   ├── log_agent_actions.py
│   │   ├── goal_monitor.py
│   │   ├── pattern_detector.py
│   │   ├── daily_briefing.py
│   │   ├── send_observability_event.py
│   │   └── utils/
│   │       └── summarizer.py          # AI event summarization
│   └── output-styles/                 # Agent personas (future)
│       ├── chief-of-staff.md
│       ├── strategist.md
│       ├── planner.md
│       ├── operator.md
│       ├── analyst.md
│       └── researcher.md
│
├── src/                                # Source code (Hexagonal/Clean Architecture - Post-EPIC-5R)
│   ├── __init__.py
│   │
│   ├── domain/                        # Pure business logic (NO external dependencies)
│   │   ├── __init__.py
│   │   ├── entities/                  # Business objects with behavior
│   │   │   ├── __init__.py
│   │   │   ├── task.py               # Task entity (id, title, status, priority, methods)
│   │   │   ├── goal.py               # Goal entity (Rocks framework)
│   │   │   ├── workflow.py           # Workflow entity
│   │   │   └── metric.py             # Metric entity
│   │   ├── value_objects/            # Immutable values
│   │   │   ├── __init__.py
│   │   │   ├── priority.py           # Priority enum (must_win_today, high, medium, low)
│   │   │   ├── status.py             # Status enum (todo, in_progress, done, deferred)
│   │   │   ├── energy_level.py       # EnergyLevel enum (high, medium, low)
│   │   │   ├── context.py            # Context enum (work, personal, strategic)
│   │   │   └── time_block.py         # TimeBlock value object
│   │   ├── services/                 # Domain services (business logic operations)
│   │   │   ├── __init__.py
│   │   │   ├── task_prioritizer.py   # Eisenhower Matrix logic
│   │   │   └── workflow_engine.py    # Workflow execution logic
│   │   └── repositories/             # Repository INTERFACES (abstract classes)
│   │       ├── __init__.py
│   │       ├── task_repository.py    # ITaskRepository interface
│   │       ├── memory_repository.py  # IMemoryRepository interfaces
│   │       └── goal_repository.py    # IGoalRepository interface
│   │
│   ├── application/                   # Use cases & orchestration
│   │   ├── __init__.py
│   │   ├── task_management/          # Task-related use cases
│   │   │   ├── __init__.py
│   │   │   ├── create_task.py        # CreateTaskUseCase
│   │   │   ├── update_task.py        # UpdateTaskUseCase
│   │   │   └── complete_task.py      # CompleteTaskUseCase
│   │   ├── planning/                 # Planning-related services
│   │   │   ├── __init__.py
│   │   │   ├── daily_planning.py     # DailyPlanningService
│   │   │   ├── morning_briefing.py   # MorningBriefingService
│   │   │   └── eod_wrapup.py         # EODWrapUpService
│   │   ├── memory/                   # Memory management use cases
│   │   │   ├── __init__.py
│   │   │   ├── context_manager.py    # Business context operations
│   │   │   └── preference_manager.py # Preference learning operations
│   │   └── coordination/             # Agent coordination
│   │       ├── __init__.py
│   │       └── agent_coordinator.py  # Agent handoff and delegation
│   │
│   ├── infrastructure/                # External concerns (I/O, events, notifications)
│   │   ├── __init__.py
│   │   ├── persistence/              # Storage implementations
│   │   │   ├── __init__.py
│   │   │   ├── json/                 # JSON storage utilities
│   │   │   │   ├── __init__.py
│   │   │   │   └── json_storage.py   # Common JSON operations
│   │   │   └── repositories/         # Repository implementations
│   │   │       ├── __init__.py
│   │   │       ├── json_task_repository.py        # JsonTaskRepository
│   │   │       ├── json_business_context_repository.py
│   │   │       ├── json_conversation_repository.py
│   │   │       └── json_preference_repository.py
│   │   ├── events/                   # Event system implementation
│   │   │   ├── __init__.py
│   │   │   ├── event_dispatcher.py   # Event dispatching
│   │   │   └── event_handlers.py     # Event handler implementations
│   │   └── notifications/            # Notification system
│   │       ├── __init__.py
│   │       └── notification_service.py
│   │
│   ├── presentation/                  # UI/CLI layer
│   │   ├── __init__.py
│   │   ├── cli/                      # CLI entry point and commands
│   │   │   ├── __init__.py
│   │   │   └── main.py               # Main entry point (Chief of Staff)
│   │   └── formatters/               # Output formatting
│   │       ├── __init__.py
│   │       ├── task_formatter.py     # Task display formatting
│   │       ├── workflow_formatter.py # Workflow output formatting
│   │       └── briefing_formatter.py # Briefing display formatting
│   │
│   ├── shared/                        # Shared utilities (use sparingly)
│   │   ├── __init__.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── date_utils.py         # Date/time utilities
│   │
│   └── mcp_servers/                   # Custom MCP servers
│       ├── __init__.py
│       └── browser_server.py          # Gemini browser integration
│
├── data/                               # Persistent data (gitignored)
│   ├── agents/                        # Agent registry and workspaces
│   │   ├── registry.json
│   │   ├── strategist/
│   │   ├── planner/
│   │   ├── operator/
│   │   ├── analyst/
│   │   ├── researcher/
│   │   └── {dynamic-agent-name}/
│   ├── memory/                        # Business context
│   │   ├── business_context.json
│   │   ├── learned_preferences.json
│   │   └── interaction_logs/
│   ├── goals/                         # Rocks framework
│   │   └── 2025-Q4-rocks.json
│   ├── metrics/                       # Business KPIs
│   │   └── scorecard.json
│   └── notes/                         # User notes
│       ├── strategic-thoughts/
│       └── meeting-notes/
│
├── workflows/                          # BMAD workflow templates
│   ├── daily-planning.yaml
│   ├── weekly-review.yaml
│   ├── quarterly-planning.yaml
│   ├── strategic-session.yaml
│   ├── goal-tracking.yaml
│   ├── meeting-notes.yaml
│   ├── research-brief.yaml
│   ├── metric-analysis.yaml
│   ├── agent-improvement.yaml
│   └── agent-creation.yaml
│
├── templates/                          # Output templates
│   ├── daily-plan-template.md
│   ├── quarterly-plan-template.md
│   └── research-report-template.md
│
├── output/                             # Generated documents (gitignored)
│   ├── daily-plans/
│   ├── weekly-reviews/
│   ├── quarterly-plans/
│   └── research-reports/
│
├── prompts/                            # Agent system prompts
│   ├── chief_of_staff_system_prompt.md
│   ├── strategist_system_prompt.md
│   ├── planner_system_prompt.md
│   ├── operator_system_prompt.md
│   ├── analyst_system_prompt.md
│   └── researcher_system_prompt.md
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── test_agent_registry.py
│   ├── test_memory_manager.py
│   ├── test_workflow_engine.py
│   └── test_integration.py
│
└── docs/                               # Documentation
    ├── index.md
    ├── PRD.md
    ├── epics.md
    ├── solution-architecture.md        # This file
    ├── unified-architecture-vision.md
    ├── big-3-analysis.md
    ├── bmm-workflow-status.md
    └── tech-specs/                     # Per-epic tech specs (Phase 3)
        ├── tech-spec-epic-1.md
        ├── tech-spec-epic-2.md
        └── ...
```

---

## 12. Architecture Decision Records

### ADR-001: Standalone Python App vs. In-Session Slash Command

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
Initial ARCHITECTURE-V2.md proposed running Mission Control as in-session slash commands within Claude Code. This approach was deprecated after analysis showed it was never properly implemented.

**Decision:**
Mission Control will be a **standalone Python CLI application** using ClaudeSDKClient.

**Rationale:**
1. **Proven Pattern:** big-3-super-agent successfully uses standalone approach
2. **Full Control:** ClaudeSDKClient provides complete control over agent lifecycle
3. **Observability:** Hook system works best in standalone mode
4. **Dynamic Agents:** On-demand agent creation requires programmatic control
5. **Simplicity:** No nested Claude instances, clear architecture

**Consequences:**
- ✅ Consistent with big-3 patterns
- ✅ Full control over agent behavior
- ✅ Easier to test and debug
- ❌ Users run `python main.py` instead of `/mission-control` command
- ❌ Requires Python environment setup

**Alternatives Considered:**
- In-session slash command approach (REJECTED - overly complex, nested instances)
- Web-based dashboard (DEFERRED to Phase 4 - CLI-first principle)

---

### ADR-002: Single Model (Sonnet 4.5) vs. Multi-Model Strategy

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
big-3-super-agent uses different models for different tasks (OpenAI for voice, Claude for coding, Gemini for browser). We need to decide model strategy for Mission Control.

**Decision:**
Use **Claude Sonnet 4.5 for all agents** initially (5 core specialists + dynamic agents).

**Rationale:**
1. **Consistency:** Uniform quality across all specialists
2. **Simplicity:** Single model configuration, single API key
3. **Cost Acceptable:** ~$30-50/month for target user (entrepreneurs, CEOs)
4. **Proven:** Sonnet 4.5 has best reasoning capabilities
5. **Optimize Later:** Can switch Operator to Haiku in Phase 2 if needed

**Consequences:**
- ✅ Predictable quality across agents
- ✅ Simpler configuration
- ✅ Single API key management
- ❌ Higher cost than multi-model strategy
- ⚠️ Can optimize later (Haiku for Operator, Opus for complex research)

**Future Optimization:**
- Phase 2: Switch Operator (Taylor) to Haiku 3.5 for fast daily planning
- Phase 3: Use Opus for complex strategic analysis (if released)

---

### ADR-003: JSON Files vs. Database for Persistence

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
Need to decide how to persist agent registry, business context, goals, and metrics.

**Decision:**
Use **JSON files** for all persistence (no PostgreSQL, SQLite, or other database).

**Rationale:**
1. **Human-Readable:** Users can view/edit data directly
2. **Version-Controllable:** Can commit data files to git (if desired)
3. **Portable:** No database setup required
4. **Sufficient Scale:** Target use case is 1 user, <50 agents
5. **BMAD Method Alignment:** BMAD uses file-based outputs

**Consequences:**
- ✅ Zero configuration required
- ✅ Easy to backup (just copy data/ directory)
- ✅ Users trust what they can see
- ❌ Not suitable for 10,000+ agents (acceptable tradeoff)
- ❌ No complex queries (use Python for filtering)

**Alternatives Considered:**
- SQLite (REJECTED - adds complexity, less transparent)
- PostgreSQL (REJECTED - overkill for single-user use case)

---

### ADR-004: Gemini Computer Use vs. Playwright for Browser Automation

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
big-3-super-agent uses Gemini Computer Use for vision-based browser automation. Need to decide if Mission Control should use Gemini or Playwright.

**Decision:**
Use **Gemini Computer Use** as primary browser automation tool (Playwright as backup).

**Rationale:**
1. **Vision-Based:** Gemini can "see" the page like a human
2. **Resilient:** Works even if HTML structure changes
3. **Proven:** Successfully used in big-3-super-agent production
4. **Research Quality:** Better for Researcher agent (Morgan) deep research tasks
5. **Future-Proof:** Vision-based automation is more adaptable

**Consequences:**
- ✅ More reliable for dynamic web pages
- ✅ Better research quality (screenshots + vision analysis)
- ✅ Aligns with big-3 proven pattern
- ❌ Requires Gemini API key (additional provider)
- ❌ Slower than direct Playwright scripting

**Fallback:**
- Keep Playwright as backup for simple automation tasks
- Use Playwright directly if Gemini API unavailable

---

### ADR-005: Observability Server Integration

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
big-3-super-agent integrates with claude-code-hooks-multi-agent-observability for real-time event streaming. Need to decide if Mission Control should use same server.

**Decision:**
Integrate with **claude-code-hooks-multi-agent-observability** server (http://localhost:4000/events).

**Rationale:**
1. **Proven:** Already works with big-3-super-agent
2. **Zero Config:** Just run server, events flow automatically
3. **Real-Time Visibility:** See what agents are doing live
4. **Debugging:** Essential for understanding agent behavior
5. **Non-Blocking:** Fails silently if server unavailable

**Consequences:**
- ✅ Excellent debugging experience
- ✅ Pattern detection insights
- ✅ Cost tracking visibility
- ⚠️ Optional dependency (system works without it)
- ⚠️ Requires running separate server (npm run dev)

**Usage:**
- Development: Run observability server for debugging
- Production: Optional (users can skip if privacy-conscious)

---

### ADR-006: Operator File Pattern for Async Delegation

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
Need pattern for long-running agent tasks (research, strategic analysis) that shouldn't block user interaction.

**Decision:**
Use **operator file pattern** from big-3-super-agent: Create Markdown status files that agents update as they work.

**Rationale:**
1. **Non-Blocking:** User continues conversation with Alex while specialist works
2. **Status Tracking:** Alex can check progress via file
3. **Human-Readable:** Users can view operator files directly
4. **Proven:** Successfully used in big-3-super-agent
5. **Simple:** Just file I/O, no message queues or databases

**Consequences:**
- ✅ Great UX for long-running tasks
- ✅ Transparent (users see operator files)
- ✅ Simple implementation
- ⚠️ Requires polling to check status
- ⚠️ File-based (not suitable for high-frequency tasks)

**Usage:**
- Research tasks (Researcher agent)
- Strategic analysis (Strategist agent)
- Quarterly planning (Planner agent)
- NOT for quick queries (use synchronous delegation)

---

### ADR-007: Dynamic Agent Creation Requires User Approval

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
Alex (Chief of Staff) can create new specialist agents on-demand. Need to decide if this requires user approval or happens automatically.

**Decision:**
**User approval required** for first-time agent creation. Subsequent usage is automatic.

**Rationale:**
1. **Transparency:** User knows system is extending itself
2. **Control:** User can reject if agent not needed
3. **Learning:** System learns from approvals (don't suggest again if rejected)
4. **Trust:** Users trust systems they can control
5. **Cost Awareness:** New agents mean more API usage

**Consequences:**
- ✅ Users stay in control
- ✅ System learns preferences
- ✅ Prevents runaway agent creation
- ⚠️ Requires one-time approval per new agent type

**Example:**
```
User: "I need help with SEO optimization"
Alex: "I don't have an SEO specialist yet. Would you like me to create one?
       This will add a new agent to your team.
       [Yes / No / Customize]"
User: "Yes"
Alex: "Creating SEO Specialist... Done! Starting your request now."
```

---

### ADR-008: BMAD Workflows in YAML, Not Python

**Status:** ACCEPTED
**Date:** 2025-10-15
**Decision Maker:** Mike + AI Architect

**Context:**
Need to decide format for workflow templates (BMAD Method patterns).

**Decision:**
Store workflows as **YAML files with Markdown instructions**, NOT Python code.

**Rationale:**
1. **Human-Readable:** Non-developers can create workflows
2. **Version-Controllable:** Easy to track changes in git
3. **BMAD Standard:** Aligns with existing BMAD Method
4. **AI-Parseable:** Claude can read and modify YAML workflows
5. **No Code Required:** Users customize workflows without programming

**Consequences:**
- ✅ Accessible to non-developers
- ✅ Easy to version control
- ✅ Self-documenting (YAML structure is clear)
- ⚠️ Requires workflow execution engine (workflow_engine.py)
- ❌ Less flexible than Python code (acceptable tradeoff)

**Format:**
```yaml
name: workflow-name
steps:
  - step: 1
    goal: "What this step accomplishes"
    action: "What agent should do"
    prompt: "User-facing question or instruction"
outputs:
  - name: output_name
    location: "output/path/file.md"
```

---

### ADR-009: Hexagonal/Clean Architecture Adoption

**Status:** APPROVED
**Date:** 2025-10-20
**Decision Maker:** Mike (Product Owner) + Architecture Review

**Context:**

During Sprint 4 completion and Sprint 5 planning, architectural debt was identified that threatens long-term maintainability:
- God object: memory.py (1,500 lines handling 4 concerns)
- Anemic domain model: Tasks/workflows as Dict[str, Any] without behavior
- Flat structure: No domain/application/infrastructure separation
- Tight coupling: Direct file I/O throughout, no repository pattern
- Type safety gaps: Excessive use of Dict[str, Any]

Current architecture (flat src/ structure) was appropriate for rapid prototyping but does not scale to enterprise-level system. Architect review identified 83 story points of refactoring needed across 6 phases.

**Decision:**

Mission Control will adopt **Hexagonal/Clean Architecture** pattern with strict layering:

```
src/
├── domain/              # Pure business logic (NO external dependencies)
│   ├── entities/        # Business objects with behavior (Task, Goal, Workflow)
│   ├── value_objects/   # Immutable values (Priority, Status, EnergyLevel)
│   ├── services/        # Domain services (TaskPrioritizer, WorkflowEngine)
│   └── repositories/    # Repository INTERFACES (ITaskRepository, IMemoryRepository)
│
├── application/         # Use cases & orchestration
│   ├── task_management/ # CreateTaskUseCase, CompleteTaskUseCase
│   ├── planning/        # DailyPlanningService, MorningBriefingService
│   ├── memory/          # Memory management use cases
│   └── coordination/    # Agent coordination use cases
│
├── infrastructure/      # External concerns (storage, events, notifications)
│   ├── persistence/
│   │   ├── json/        # JSON storage implementation
│   │   └── repositories/ # JsonTaskRepository, JsonMemoryRepository
│   ├── events/          # Event system implementation
│   └── notifications/   # Notification system implementation
│
└── presentation/        # UI/CLI layer
    ├── cli/             # CLI entry point, command handlers
    └── formatters/      # TaskFormatter, WorkflowFormatter, BriefingFormatter
```

**Rationale:**

1. **Maintainability:** Clear separation of concerns makes code easier to understand and modify
2. **Testability:** Domain layer has zero dependencies, easy to unit test (90%+ coverage target)
3. **Flexibility:** Repository pattern allows swapping storage (JSON → SQLite → PostgreSQL) without changing domain
4. **Extensibility:** Clean boundaries enable adding features without ripple effects
5. **SOLID Principles:** Architecture enforces Single Responsibility, Dependency Inversion
6. **Future Self-Coding:** Clean patterns enable Mission Control to code itself (EPIC-7)

**Consequences:**

✅ **Positive:**
- Faster future development (EPIC-4, 5, 6, 7 easier to implement)
- Fewer bugs (clear boundaries prevent coupling)
- Easier testing (domain isolated from infrastructure)
- Better onboarding (standard patterns, clear structure)
- Enables self-coding (CLAUDE.md standards for AI agents)

⚠️ **Negative:**
- +6 weeks to MVP timeline (4-6 weeks → 10-12 weeks)
- 83 story points of refactoring effort (Phases 1-6)
- Learning curve for contributors (Hexagonal Architecture pattern)

❌ **Mitigated:**
- Strangler Fig pattern reduces migration risk (new alongside old)
- Feature flags enable gradual rollout
- Comprehensive tests protect against regressions
- Checkpoint after Phase 2 (3 weeks) allows course correction

**Implementation:**

- **EPIC-5R:** Architectural Refactoring (83 points, 6 weeks)
- **Engineering Standards:** CLAUDE.md (1,006 lines) defines mandatory patterns
- **Migration Strategy:** Strangler Fig (build new alongside old)
- **Testing Requirements:** 90%+ domain coverage, 80%+ integration coverage

**Alternatives Considered:**

- **Continue with flat structure:** REJECTED - Technical debt compounds, future development slows
- **Big-bang rewrite:** REJECTED - Too risky, Strangler Fig is safer
- **Microservices architecture:** REJECTED - Overkill for single-developer MVP, can evolve later

**Related Decisions:**

- ADR-001: Standalone Python App (reinforces need for clean architecture)
- ADR-002: Python 3.13+ (enables modern type hints for type safety)

**References:**

- CLAUDE.md: Engineering standards document
- EPIC-5R: Architectural Refactoring plan (6 phases)
- Sprint Change Proposal: Course correction decision (2025-10-20)

---

## 13. Implementation Guidance

### 13.1 Development Phases

**Phase 1: Foundation (Sprints 0-4) - EPIC-1 + EPIC-2**
- ✅ Basic Python project structure
- ✅ ClaudeSDKClient setup for Chief of Staff
- ✅ 5 core specialist agents (system prompts, agent definitions)
- ✅ Agent registry (JSON persistence)
- ✅ Memory system (business context, preferences)
- ✅ Rich CLI (panels, basic formatting)
- ✅ Stop hook (logging only)
- ✅ Basic conversation loop (Alex delegates to specialists)

**Deliverable:** User can have conversation with Alex, Alex delegates to 5 specialists, conversation persists in memory.

---

**Phase 2: Autonomous Behaviors (Sprints 5-9) - EPIC-3 + EPIC-4**
- ✅ Goal tracking (Rocks framework in data/goals/)
- ✅ BMAD workflows (daily-planning, weekly-review, quarterly-planning)
- ✅ Workflow execution engine
- ✅ All 9 hook types implemented
- ✅ Scheduled Notification hooks (daily briefings)
- ✅ goal_monitor.py hook
- ✅ pattern_detector.py hook
- ✅ Observability server integration
- ✅ Rich UI tables/dashboards for goals

**Deliverable:** Daily briefings run automatically, goals monitored, pattern detection learning, observability dashboard shows activity.

---

**Phase 3: Dynamic Agents (Sprints 10-14) - EPIC-5 + EPIC-6**
- ✅ Dynamic agent creation (Alex creates new specialists on-demand)
- ✅ Operator file pattern (async delegation)
- ✅ agent-improvement.yaml workflow
- ✅ Agent-Improver meta-agent
- ✅ Gemini Computer Use integration (browser automation)
- ✅ Stripe MCP (revenue metrics)
- ✅ Specialized workflows (eu-market-expansion.yaml, etc.)
- ✅ Rich UI progress bars, sparklines

**Deliverable:** Alex creates new specialists on-demand, agents self-improve based on usage, browser automation working, metrics auto-collected.

---

**Phase 4: Advanced Integrations (Sprints 15-20) - EPIC-7**
- ⏳ Google Calendar MCP (schedule awareness)
- ⏳ Gmail MCP (email summaries)
- ⏳ QuickBooks MCP (financial data)
- ⏳ OpenAI Realtime API (voice interface option)
- ⏳ Multi-modal inputs (image, document upload)
- ⏳ Custom MCP server creator
- ⏳ Web dashboard (optional)

**Deliverable:** Full MCP ecosystem, voice interface, multi-modal inputs, team features.

---

### 13.2 Critical Path: First Working System

**Sprint 0 (Week 1):**
1. Create project structure (pyproject.toml, src/, data/, workflows/)
2. Install dependencies (claude-agent-sdk, rich, pydantic)
3. Create .env.example with ANTHROPIC_API_KEY
4. Write main.py skeleton (ClaudeSDKClient for Chief of Staff)
5. Test basic query with ClaudeSDKClient

**Sprint 1 (Week 2):**
1. Implement agent_definitions.py (5 core specialists)
2. Implement agent_registry.py (JSON persistence)
3. Create Rich UI components (display_response, display_table)
4. Implement delegation logic in main.py
5. Test: Alex delegates to Strategist

**Sprint 2 (Week 3):**
1. Implement memory_manager.py (BusinessContext, LearnedPreferences)
2. Create initial business_context.json and learned_preferences.json
3. Load memory in Chief of Staff system prompt
4. Implement log_agent_actions.py hook
5. Test: Memory persists across restarts

**Sprint 3 (Week 4):**
1. Implement workflow_engine.py (YAML parsing, step execution)
2. Create daily-planning.yaml workflow
3. Test: Operator executes daily planning workflow
4. Create Rich UI for daily plan display
5. Integration test: Full user journey (user request → delegation → workflow → output)

**Deliverable (End of Sprint 3):** **Minimally Viable Mission Control**
- User runs `python main.py`
- Alex (Chief of Staff) greets user with context
- User requests "Help me plan my day"
- Alex delegates to Operator (Taylor)
- Operator executes daily-planning.yaml workflow
- Rich CLI displays daily plan with Eisenhower Matrix
- Memory persists (user preferences, business context)

---

### 13.3 Testing Strategy

**Unit Tests:**
```python
# tests/test_agent_registry.py
def test_register_agent():
    registry = AgentRegistryManager(temp_registry_path)
    registry.register_agent("test-agent", AgentMetadata(...))
    assert registry.get_agent("test-agent") is not None

# tests/test_memory_manager.py
def test_load_business_context():
    memory = MemoryManager(temp_data_dir)
    context = memory.load_business_context()
    assert context.company.name == "Test Company"

# tests/test_workflow_engine.py
def test_execute_workflow():
    engine = WorkflowEngine(workflows_dir)
    result = await engine.execute_workflow("daily-planning", mock_agent, {})
    assert "daily_plan_file" in result
```

**Integration Tests:**
```python
# tests/test_integration.py
async def test_full_conversation_flow():
    """Test complete user journey."""
    # Start Mission Control
    mission_control = MissionControl()

    # User message
    response = await mission_control.process_message("Help me plan my day")

    # Verify delegation to Operator
    assert "Taylor" in response

    # Verify workflow execution
    assert Path("output/daily-plans/2025-10-15.md").exists()

    # Verify memory updated
    prefs = mission_control.memory_manager.load_preferences()
    assert "operator" in prefs.preferred_agents
```

**Manual Testing Checklist:**
- [ ] Conversation with Alex (greeting with context)
- [ ] Delegation to each specialist (5 agents)
- [ ] Workflow execution (daily-planning.yaml)
- [ ] Memory persistence (restart app, context intact)
- [ ] Hook execution (log_agent_actions.py runs)
- [ ] Rich UI (panels, tables display correctly)
- [ ] Error handling (no API key, network error)

---

### 13.4 Deployment Instructions

**Prerequisites:**
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.13+
# macOS: brew install python@3.13
# Windows: Download from python.org
# Linux: Use package manager (apt, yum, etc.)
```

**Setup:**
```bash
# Clone repository
cd mission-control-system

# Create .env file
cp .env.example .env
# Edit .env and add ANTHROPIC_API_KEY

# Install dependencies
uv sync

# Initialize data directory
mkdir -p data/agents data/memory data/goals data/metrics data/notes/strategic-thoughts data/notes/meeting-notes

# Create initial business context
cat > data/memory/business_context.json << 'EOF'
{
  "version": "1.0.0",
  "last_updated": "2025-10-15T00:00:00Z",
  "company": {
    "name": "Your Company",
    "industry": "Your Industry",
    "mission": "Your mission statement",
    "values": ["Value 1", "Value 2"]
  },
  "vision": {
    "ten_year": "Your 10-year vision",
    "three_year": "Your 3-year goal",
    "one_year": "Your 1-year target"
  },
  "current_priorities": [],
  "key_metrics": {}
}
EOF

# Create learned preferences
cat > data/memory/learned_preferences.json << 'EOF'
{
  "version": "1.0.0",
  "last_updated": "2025-10-15T00:00:00Z",
  "communication_style": "professional",
  "preferred_frameworks": [],
  "decision_patterns": [],
  "recurring_topics": [],
  "preferred_agents": {},
  "notification_preferences": {
    "daily_briefing": true,
    "weekly_review": true,
    "goal_alerts": true
  }
}
EOF

# Run Mission Control
uv run python src/main.py
```

**Optional: Observability Dashboard**
```bash
# In separate terminal
git clone https://github.com/disler/claude-code-hooks-multi-agent-observability
cd claude-code-hooks-multi-agent-observability
npm install
npm run dev

# Open http://localhost:3000
# Mission Control events will stream here
```

---

### 13.5 Migration from ARCHITECTURE-V2 (Deprecated)

**If you have old files from in-session approach:**

**DEPRECATED FILES (safe to delete):**
- `main.py` (old subprocess launcher)
- `test_installation.py` (SDK connection test)
- `test_basic.py` (unit tests for subprocess approach)
- `.env` (if using Claude Code auth, not separate API key)

**FILES TO KEEP:**
- `data/` directory (business context, goals, notes)
- `workflows/` directory (BMAD templates)
- `.claude/output-styles/` (agent personas)
- Any custom agent definitions you created

**Migration Steps:**
1. Backup `data/` directory
2. Delete old codebase
3. Clone new standalone app architecture
4. Copy `data/` directory to new project
5. Update `.env` with ANTHROPIC_API_KEY
6. Run `uv sync` and `python src/main.py`

---

## Conclusion

This solution architecture provides a **comprehensive blueprint** for implementing Mission Control as a **unified, self-extending autonomous executive team** that synthesizes:

- **BMAD Method** for structured business workflows
- **big-3-super-agent** for multi-agent orchestration and observability
- **Claude Agent SDK** for autonomous behaviors and persistent memory

**Key Achievements:**
✅ Standalone Python CLI architecture (proven, maintainable)
✅ 5 core specialists + dynamic agent creation (extensible)
✅ Multi-model/multi-provider tool strategy (Gemini, OpenAI, Claude)
✅ Observability with AI summaries (debuggable, transparent)
✅ Self-improving agents (learns and evolves over time)
✅ Privacy-first (100% local data storage)
✅ Production-ready patterns (from big-3 reference implementation)

**Ready for Implementation:** This architecture is **APPROVED** for Phase 1 development (Sprints 0-4).

**Next Steps:**
1. ✅ Review and approve this architecture document
2. ✅ Run cohesion check (validate PRD → Architecture alignment)
3. ⏳ Generate tech specs for each EPIC
4. ⏳ Begin Sprint 0 implementation

---

**Document Version:** 1.0.0
**Status:** APPROVED FOR IMPLEMENTATION
**Last Updated:** 2025-10-15
**Approved By:** Mike (Product Owner) + AI Architect

🚀 **Let's build Mission Control!**
