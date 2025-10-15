# EPIC-3: Operator (Daily Execution Agent)

**Status:** Not Started
**Priority:** P1 (High - Immediate Daily Value)
**Epic Owner:** Product Lead
**Business Value:** Daily productivity and execution - the agent that keeps you focused and moving forward every single day

---

## Epic Goal

Build the Operator agent (Taylor) that manages daily execution, task prioritization, and productivity. This agent:
- Helps prioritize work every morning
- Tracks task completion throughout the day
- Suggests time blocking for deep work
- Keeps you focused on what matters
- Learns your productivity patterns
- Autonomous daily planning support

---

## Success Criteria

- [ ] User gets clear daily priorities every morning
- [ ] Task tracking works seamlessly
- [ ] Time blocking suggestions are helpful
- [ ] Agent learns best times for different work types
- [ ] User feels more productive and focused
- [ ] Daily wrap-up captures progress

---

## Key Capabilities

### 1. Daily Planning (Morning)
Every morning (or when user starts work):
- Review calendar and commitments
- Brain dump all tasks
- Apply prioritization framework (Important/Urgent)
- Identify 1-3 "Must Win Today" tasks
- Suggest time blocks for focused work
- Set daily intention

### 2. Task Management
- Capture tasks from any conversation
- Track status (todo, in-progress, done)
- Link tasks to goals/projects
- Flag overdue or at-risk tasks
- Suggest when to tackle each task

### 3. Time Blocking
- Identify available calendar gaps
- Suggest blocks for deep work
- Match task type to best time of day (learned)
- Protect focus time from interruptions
- Adjust blocks when calendar changes

### 4. Mid-Day Check-In (Optional)
Quick pulse:
- On track with priorities?
- Need to adjust plan?
- Capture new urgent items

### 5. End of Day Wrap-Up
- What got done (celebrate!)
- What didn't (why not?)
- Capture learnings
- Prep tomorrow's top 3
- Clear mental load

### 6. Weekly Prep (Fridays)
Look ahead to next week:
- Key deadlines/commitments
- Suggested focus areas
- Time to block now

---

## Agent Personality

**Name:** Taylor (default, customizable)
**Icon:** ⚡

**Persona:**
- Former Navy SEAL turned productivity coach
- No-nonsense, action-oriented
- "What's the next physical action?"
- Ruthlessly focused on execution
- Hates busy-work, loves leverage
- Protective of your deep work time

**Communication Style:**
- Fast-paced, energetic
- Short sentences, clear directives
- Asks "What's the next action?" constantly
- Celebrates wins, even small ones
- Challenges procrastination gently but firmly
- Uses momentum language ("Let's knock this out")

---

## Autonomous Behaviors

### Scheduled Tasks
```yaml
scheduled:
  - time: "user_work_start_time"  # Learned
    action: "prompt_daily_planning"
    output: "Let's plan your day"

  - time: "12:00"
    action: "optional_midday_checkin"
    condition: "user_preference"

  - time: "user_work_end_time"  # Learned
    action: "prompt_eod_wrapup"
    output: "Let's wrap up your day"

  - day: "Friday"
    time: "15:00"
    action: "weekly_prep"
    output: "Let's prep next week"
```

### Event Monitors
```yaml
events:
  - trigger: "task_mentioned_in_conversation"
    action: "capture_to_task_list"

  - trigger: "priority_task_not_started_by_noon"
    action: "gentle_reminder"

  - trigger: "user_says_overwhelmed"
    action: "trigger_triage_workflow"

  - trigger: "calendar_block_freed_up"
    action: "suggest_task_for_timeblock"

  - trigger: "3_days_with_low_completion"
    action: "suggest_priority_review"
```

### Learning Behaviors
```yaml
learns:
  - "Best time for deep work" (e.g., "Mornings 6-9am most productive")
  - "Task completion patterns" (e.g., "Estimates always 2x actual")
  - "Energy levels by time of day"
  - "Which types of tasks get procrastinated"
  - "Ideal task list length" (e.g., "User gets demoralized with 15+ tasks")
  - "Preferred planning depth" (high-level vs detailed)
```

---

## Core Workflows

### Autonomous/Scheduled Workflows
1. **daily-planning** - Morning prioritization session
2. **eod-wrapup** - End of day reflection
3. **weekly-prep** - Friday prep for next week
4. **task-monitor** - Continuous tracking

### User-Initiated Workflows
1. **task-triage** - "I'm overwhelmed, help!"
2. **time-blocking** - "Block time for deep work"
3. **quick-capture** - "Add this to my list"
4. **focus-session** - "I need to focus for 2 hours"
5. **priority-check** - "What should I do next?"

### Framework-Agnostic Approaches
User can choose their preferred method:
- **Eisenhower Matrix** (Important/Urgent)
- **MIT (Most Important Tasks)** (3 per day max)
- **Time Blocking** (Themed days/blocks)
- **Eat the Frog** (Hardest thing first)
- **Custom** (User defines their own system)

---

## Task Management System

### Task Structure
```yaml
task:
  id: "TASK-001"
  title: "Finish proposal for Client X"
  status: "in_progress"  # todo, in_progress, done, blocked
  priority: "must_win_today"  # must_win, should_do, nice_to_have
  estimated_time: "2 hours"
  actual_time: null
  energy_required: "high"  # high, medium, low
  context: "deep_work"  # deep_work, admin, communication
  linked_to:
    goal: "GOAL-Q4-01"
    project: "CLIENT-X"
  due_date: "2025-10-14"
  created: "2025-10-13"
  completed: null
  notes: "Needs financial projections from Jordan (CFO)"
```

### Task List Views
- **Today** - Only today's priorities
- **This Week** - Week horizon
- **By Goal** - Grouped by goals/projects
- **Overdue** - What's slipping
- **Waiting On** - Blocked tasks

---

## Daily Planning Workflow (Detailed)

```markdown
<workflow name="daily-planning">

<step n="1" goal="Review calendar">
Let's start by looking at your calendar.

[Agent loads calendar from memory/integration]

You have:
- 9am: Team standup (30 min)
- 2pm: Strategy call (60 min)
- 4pm: FREE

Available blocks:
- 6-9am: 3 hours
- 11am-2pm: 3 hours
- After 4pm: Open

Sound right?

<template-output>calendar_review</template-output>
</step>

<step n="2" goal="Brain dump tasks">
What's on your mind for today? Just tell me everything - we'll organize it in a sec.

[User brain dumps: "Finish proposal, review marketing metrics, hire decision,
email partnerships, prep for strategy call..."]

Got it. I count 12 items. Let's prioritize.

<template-output>task_list</template-output>
</step>

<step n="3" goal="Apply prioritization">
Let's sort these using Important vs Urgent:

**MUST WIN TODAY (Important + Urgent):**
1. Finish proposal for Client X (due today, $50K deal)
2. Hiring decision (candidate has other offers)

**IMPORTANT, NOT URGENT (Your leverage work):**
3. Prep for strategy call (Q1 planning)
4. Review marketing metrics (revenue trending down)

**URGENT, NOT IMPORTANT (Minimize these):**
5. Email partnerships (they're waiting, but not strategic)
6-8. [Other reactive items]

**DELETE/DEFER:**
9-12. [These don't move your goals forward]

Does this feel right? What would you change?

<template-output>prioritized_list</template-output>
</step>

<step n="4" goal="Identify Must-Wins">
Based on this, your TOP 3 MUST-WIN tasks today are:

1. **Finish Client X proposal** (2 hours, deep work)
2. **Make hiring decision** (30 min, clear head needed)
3. **Prep for strategy call** (1 hour, creative thinking)

If you only did these 3 things today, would it be a successful day?

[User: "Yes"]

Perfect. Let's time block them.

<template-output>must_wins</template-output>
</step>

<step n="5" goal="Time blocking">
Here's my recommendation:

**6-8am: DEEP WORK - Client X Proposal**
- Your best focus time (you told me mornings are your superpower)
- 2 hours uninterrupted
- Turn off Slack, close email
- This is your #1 priority

**10:30-11am: DECISION TIME - Hiring**
- After standup, before lunch
- Fresh mind for important decision
- 30 min is enough

**12:30-1:30pm: CREATIVE WORK - Strategy Prep**
- After lunch, energy is good
- 1 hour to gather thoughts for 2pm call

This leaves your 11am-12:30pm block free for:
- Marketing metrics review (30 min)
- Quick emails/admin (30 min)
- Buffer

Sound good?

<template-output>time_blocks</template-output>
</step>

<step n="6" goal="Set daily intention">
One last thing. Complete this sentence:

"Today will be a great day if I..."

[User: "...close the Client X proposal and feel confident in our Q1 strategy"]

Love it. That's your north star today.

Let's execute. 💪

<template-output>daily_intention</template-output>
</step>

</workflow>
```

---

## User Stories (High-Level)

1. **Morning Planning**
   - Calendar review
   - Task brain dump
   - Prioritization (multiple frameworks)
   - Must-win identification
   - Time blocking

2. **Task Management**
   - Task capture from conversations
   - Status tracking
   - Due date management
   - Goal linking

3. **Time Blocking**
   - Identify available blocks
   - Match tasks to best times
   - Protect deep work
   - Adjust when calendar changes

4. **Mid-Day Support**
   - Quick check-ins
   - On-track assessment
   - Plan adjustments

5. **EOD Wrap-Up**
   - Completion review
   - Learning capture
   - Tomorrow prep

6. **Weekly Prep**
   - Next week preview
   - Proactive time blocking

7. **Learning System**
   - Track productivity patterns
   - Identify best times for work types
   - Adapt recommendations

---

## Integration Points

**Memory System (EPIC-1):**
- Stores tasks and status
- Tracks completion patterns
- Learns productivity times

**Planner Agent (EPIC-4):**
- Links tasks to goals
- Updates goal progress based on task completion

**Chief of Staff (EPIC-2):**
- Provides task status for daily briefing
- Receives tasks captured in other conversations

**Calendar (Future):**
- Reads calendar for time blocking
- Suggests when to schedule tasks

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - Required
- Task storage system
- Basic BMAD agent structure

---

## Risks & Mitigations

**Risk:** User doesn't want structured daily planning
**Mitigation:** Make it flexible - user can skip or customize depth

**Risk:** Task list becomes overwhelming
**Mitigation:** Auto-archive old tasks, focus on today/this week views

**Risk:** Time estimates always wrong
**Mitigation:** Learn actual vs estimated over time, adjust

---

## Acceptance Criteria for Epic

- [ ] Daily planning workflow completes in <10 minutes
- [ ] User feels clearer on priorities after planning
- [ ] Tasks tracked and updated throughout day
- [ ] At least one time-blocking suggestion proves useful
- [ ] EOD wrap-up captures progress and learnings
- [ ] Agent learns at least one productivity pattern in 2 weeks

---

## Stories in Epic

- STORY-3.1: Operator agent persona and definition
- STORY-3.2: Task data model and storage
- STORY-3.3: Daily planning workflow
- STORY-3.4: Prioritization frameworks (Eisenhower, MIT, custom)
- STORY-3.5: Time blocking suggestions
- STORY-3.6: Task capture from conversations
- STORY-3.7: EOD wrap-up workflow
- STORY-3.8: Weekly prep workflow
- STORY-3.9: Productivity pattern learning
- STORY-3.10: Calendar integration (if available)

---

## Estimated Effort

**Epic Total:** 30-40 story points (approx. 2 weeks)

**Complexity:** Medium-High - Task management + learning

**Value:** High - Immediate daily value for user
