# EPIC-2: Chief of Staff (Orchestrator Agent)

**Status:** Not Started
**Priority:** P0 (Critical - Primary Interface)
**Epic Owner:** Product Lead
**Business Value:** Single point of contact for user - the agent that knows everything and coordinates everyone

---

## Epic Goal

Build the Chief of Staff agent (Alex) as the primary orchestrator and user interface for Mission Control. This agent:
- Serves as the main conversation partner
- Routes to specialist agents intelligently
- Maintains complete business context
- Generates daily briefings autonomously
- Surfaces proactive insights
- Coordinates actions across all agents

---

## Success Criteria

- [ ] User can have natural conversations with Chief of Staff
- [ ] Agent routes to specialists based on intent detection
- [ ] Context maintained across all conversations
- [ ] Daily briefings generated automatically at 6:30 AM
- [ ] Agent proactively surfaces important items
- [ ] Seamless handoffs to/from specialist agents

---

## Key Capabilities

### 1. Intent Detection & Routing
Understands user requests and routes to appropriate specialist:

```
"Let's plan Q1" → Routes to Planner
"Should we pursue this opportunity?" → Routes to Strategist
"I'm overwhelmed today" → Routes to Operator
"What's our revenue trend?" → Routes to Analyst
"Let's chat about vision" → Routes to Strategist
```

### 2. Context Management
Maintains complete picture of:
- Active goals/projects
- Recent decisions
- Upcoming deadlines
- Current priorities
- Team status
- Business metrics

### 3. Daily Briefing (Autonomous)
Every morning at 6:30 AM, generates:
- Top 3 priorities for today
- Schedule overview with gaps for deep work
- Heads up on important items
- Proactive questions/challenges

### 4. Proactive Intelligence
Surfaces insights without being asked:
- "You've mentioned X 3 times - should we address it?"
- "Goal Y is at risk - only 2 weeks left"
- "You haven't reviewed metrics in 10 days"
- "3 opportunities sitting in backlog"

### 5. End of Day Reflection
At EOD (or when user signals), facilitates:
- What got done today
- What didn't (and why)
- New insights/learnings
- Tomorrow's top 3
- One reflection question

### 6. Weekly Review (Fridays 4pm)
Automatically prepares:
- Progress on goals this week
- Wins and challenges
- Patterns noticed
- Prep for next week

---

## Agent Personality

**Name:** Alex (default, customizable)
**Icon:** 🎯

**Persona:**
- Executive assistant who's been with you for years
- Knows your business inside and out
- Anticipates needs before you express them
- Direct and efficient, no fluff
- Challenges you when needed
- Protective of your time and focus

**Communication Style:**
- Professional but personable
- Concise briefings (respects your time)
- Proactive without being annoying
- Asks clarifying questions when needed
- Summarizes conversations for easy scanning

---

## Autonomous Behaviors

### Scheduled Tasks
```yaml
scheduled:
  - time: "06:30"
    action: "generate_daily_briefing"
    output: "Morning briefing with priorities, schedule, heads-up"

  - time: "17:00"
    action: "prompt_eod_reflection"
    output: "EOD check-in invitation"

  - day: "Friday"
    time: "16:00"
    action: "generate_weekly_review"
    output: "Week in review, prep for next week"

  - day: "Last Friday of month"
    time: "16:00"
    action: "suggest_monthly_strategic_review"
    output: "Prompt for strategic check-in with Vision"
```

### Event Monitors
```yaml
events:
  - trigger: "goal_status_changed_to_at_risk"
    action: "notify_in_briefing"

  - trigger: "same_issue_mentioned_3_times"
    action: "surface_pattern"
    message: "You've mentioned [issue] 3 times - should we tackle this?"

  - trigger: "deadline_within_2_days"
    action: "flag_urgently"

  - trigger: "no_goal_review_in_7_days"
    action: "suggest_progress_check"

  - trigger: "opportunity_backlog_over_5"
    action: "suggest_triage"
```

### Learning Behaviors
```yaml
learns:
  - "Best time for strategic conversations"
  - "Preferred briefing length/detail"
  - "Communication style preferences"
  - "Decision-making patterns"
  - "Which prompts user finds helpful vs annoying"
```

---

## Core Workflows

### Autonomous Workflows (No User Trigger Required)
1. **daily-briefing-generator** - Runs at 6:30 AM
2. **weekly-review-generator** - Runs Friday 4 PM
3. **context-monitor** - Runs continuously
4. **pattern-detector** - Analyzes interactions for patterns

### User-Initiated Workflows
1. **catch-up** - "What's the status on everything?"
2. **context-deep-dive** - "Tell me about Project X"
3. **decision-support** - "Help me think through this"
4. **delegation** - "Can you handle this for me?"

### Agent Coordination Workflows
1. **route-to-specialist** - Handoff to other agents
2. **synthesize-insights** - Gather input from multiple agents
3. **coordinate-actions** - Ensure specialists are aligned

---

## User Stories (High-Level)

1. **Conversation Management**
   - Natural language understanding
   - Intent detection
   - Context-aware responses

2. **Daily Briefing**
   - Auto-generate at 6:30 AM
   - Prioritize top items
   - Include proactive insights

3. **EOD Reflection**
   - Prompt for end-of-day check-in
   - Capture learnings
   - Plan tomorrow

4. **Routing & Coordination**
   - Detect when to route to specialists
   - Smooth handoffs with context
   - Synthesize responses from multiple agents

5. **Proactive Intelligence**
   - Surface patterns
   - Flag risks
   - Suggest actions

6. **Context Management**
   - Maintain business state
   - Track all active items
   - Recall previous conversations

---

## Integration Points

**Memory System (EPIC-1):**
- Reads business context
- Writes interaction history
- Updates learned patterns

**Planner Agent (EPIC-4):**
- Routes goal/project questions
- Retrieves goal status for briefings

**Operator Agent (EPIC-3):**
- Routes daily execution questions
- Gets daily task status for briefings

**Strategist Agent (EPIC-5):**
- Routes strategic questions
- Schedules monthly check-ins

**Analyst Agent (EPIC-6):**
- Retrieves metrics for briefings
- Routes data/analysis questions

---

## Technical Architecture

### Agent Definition
```yaml
agent:
  metadata:
    id: "bmad/mission-control/agents/chief-of-staff.md"
    name: "Alex"
    title: "Chief of Staff"
    icon: "🎯"
    type: "orchestrator"

  autonomous_capabilities:
    scheduled_tasks: [daily-briefing, weekly-review, monthly-prompt]
    event_monitors: [goal-risk, pattern-detection, deadline-alert]
    learning: [communication-style, decision-patterns, productivity-times]

  routing_rules:
    - intent: ["plan", "goal", "quarterly", "project"]
      route_to: "planner"
    - intent: ["strategy", "vision", "opportunity", "market"]
      route_to: "strategist"
    - intent: ["today", "tasks", "priorities", "overwhelmed"]
      route_to: "operator"
    - intent: ["metrics", "revenue", "data", "trend"]
      route_to: "analyst"
```

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - **MUST COMPLETE FIRST**
- Module structure created
- Memory system operational

---

## Risks & Mitigations

**Risk:** Intent detection fails, routes to wrong agent
**Mitigation:** Fallback to asking clarifying question

**Risk:** Daily briefings become ignored/annoying
**Mitigation:** User configurable (time, length, what's included)

**Risk:** Agent doesn't have enough context to be useful
**Mitigation:** Aggressive context capture, user can enrich

---

## Acceptance Criteria for Epic

- [ ] Agent responds intelligently to diverse queries
- [ ] Routes correctly to specialists 90%+ of time
- [ ] Daily briefing auto-generates and is useful
- [ ] At least 2 proactive insights surfaced per week
- [ ] User feels agent "knows their business"
- [ ] Smooth handoffs to/from other agents

---

## Stories in Epic

- STORY-2.1: Chief of Staff agent persona definition
- STORY-2.2: Intent detection and routing system
- STORY-2.3: Daily briefing generator (autonomous)
- STORY-2.4: EOD reflection workflow
- STORY-2.5: Weekly review generator
- STORY-2.6: Context retrieval and display
- STORY-2.7: Proactive insight surfacing
- STORY-2.8: Agent coordination/handoff system
- STORY-2.9: Learning system integration

---

## Estimated Effort

**Epic Total:** 35-45 story points (approx. 2-3 weeks)

**Complexity:** High - Orchestration + autonomous behaviors

**Value:** Critical - This is the primary user interface
