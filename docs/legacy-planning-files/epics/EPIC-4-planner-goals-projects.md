# EPIC-4: Planner (Goals & Projects Agent)

**Status:** Not Started
**Priority:** P1 (High - Strategic Execution)
**Epic Owner:** Product Lead
**Business Value:** Translates vision into achievable plans, tracks progress autonomously, ensures goals don't slip

---

## Epic Goal

Build the Planner agent (Quinn) that manages goals, projects, and quarterly planning. This agent:
- Helps set measurable goals (quarterly, annual, multi-year)
- Breaks goals into executable projects/milestones
- Tracks progress autonomously
- Flags when goals go off track
- Suggests re-prioritization when needed
- Facilitates quarterly planning sessions

---

## Success Criteria

- [ ] User can set goals at multiple time horizons
- [ ] Goals tracked automatically with status updates
- [ ] Agent proactively flags off-track goals
- [ ] Quarterly planning workflow provides clarity
- [ ] Progress visible at a glance
- [ ] Agent suggests adjustments when needed

---

## Key Capabilities

### 1. Goal Setting (Framework Agnostic)
Supports multiple approaches:
- **OKRs** (Objectives & Key Results)
- **Rocks** (EOS-style quarterly priorities)
- **SMART Goals** (Specific, Measurable, Achievable, Relevant, Time-bound)
- **Custom** (User defines their own structure)

### 2. Goal Tracking
- Status: On Track, At Risk, Off Track, Complete
- Progress indicators (% complete, milestones hit)
- Automatic status updates based on task completion
- Timeline tracking (days remaining)

### 3. Quarterly Planning
Structured planning sessions:
- Review last quarter (what worked/didn't)
- Set 3-7 priorities for next 90 days
- Define success criteria
- Identify resources needed
- Anticipate obstacles

### 4. Progress Monitoring (Autonomous)
- Checks goal status daily
- Flags when progress stalls
- Notices when deadline approaching
- Tracks completion patterns

### 5. Project Planning
Break goals into:
- Milestones
- Tasks (delegates to Operator)
- Dependencies
- Resources needed

### 6. Strategic Alignment
- Links quarterly goals to annual vision
- Ensures daily tasks ladder up to goals
- Identifies misalignment

---

## Agent Personality

**Name:** Quinn (default, customizable)
**Icon:** 📊

**Persona:**
- McKinsey consultant turned COO
- Data-driven but pragmatic
- "What gets measured gets done"
- Structured thinking, loves frameworks
- Balances ambition with realism
- Holds you accountable (gently but firmly)

**Communication Style:**
- Clear, structured communication
- Uses frameworks and visual organization
- Asks clarifying questions
- Data-backed recommendations
- Celebrates progress, diagnoses problems
- "Let's break this down" is favorite phrase

---

## Autonomous Behaviors

### Scheduled Tasks
```yaml
scheduled:
  - day: "Monday"
    time: "06:00"
    action: "update_weekly_progress"
    output: "Progress update for Chief of Staff briefing"

  - day: "Last Friday of Quarter"
    time: "09:00"
    action: "prompt_quarterly_planning"
    output: "Time for quarterly planning session"

  - day: "First of Month"
    time: "09:00"
    action: "generate_monthly_review"
    output: "Monthly progress report"
```

### Event Monitors
```yaml
events:
  - trigger: "goal_progress_stalled_7_days"
    action: "flag_at_risk"
    notification: "Goal X hasn't moved in 7 days"

  - trigger: "goal_deadline_within_2_weeks"
    action: "assess_likelihood"
    notification: "Goal Y due in 2 weeks - current status?"

  - trigger: "goal_marked_off_track"
    action: "suggest_review_session"
    message: "Want to discuss Goal Z that's off track?"

  - trigger: "3_tasks_completed_for_goal"
    action: "update_goal_progress"

  - trigger: "quarter_end_approaching"
    action: "prepare_quarterly_review"
```

### Learning Behaviors
```yaml
learns:
  - "Goal completion patterns" (e.g., "User finishes 80% of goals")
  - "Planning accuracy" (e.g., "Estimates usually 1.5x actual")
  - "Best goal structure" (e.g., "User prefers 5 goals max")
  - "Effective milestone sizes"
  - "Which types of goals get abandoned"
```

---

## Goal Data Model

```yaml
goal:
  id: "GOAL-Q4-2025-01"
  title: "Launch new product line"
  owner: "Mike"

  timeframe:
    type: "quarterly"  # quarterly, annual, multi-year
    quarter: "Q4 2025"
    start_date: "2025-10-01"
    end_date: "2025-12-31"
    days_remaining: 78

  framework: "okr"  # okr, rock, smart, custom

  objective: "Successfully launch new product line"
  key_results:
    - metric: "3 paying customers"
      target: 3
      current: 0
      unit: "customers"
    - metric: "Revenue generated"
      target: 15000
      current: 0
      unit: "dollars"

  status: "on_track"  # on_track, at_risk, off_track, complete
  progress_percent: 25

  milestones:
    - title: "Complete market research"
      due: "2025-10-31"
      status: "complete"
    - title: "Build MVP"
      due: "2025-11-30"
      status: "in_progress"
    - title: "First customer"
      due: "2025-12-15"
      status: "not_started"

  linked_tasks:
    - "TASK-001"
    - "TASK-042"
    - "TASK-073"

  dependencies:
    - "Need CFO to approve budget"
    - "Waiting on tech infrastructure from IT"

  notes: "User very excited about this, top priority"
  created: "2025-10-01"
  last_reviewed: "2025-10-14"
```

---

## Core Workflows

### Autonomous/Scheduled Workflows
1. **progress-monitor** - Daily check on all goals
2. **weekly-progress-update** - Monday summary
3. **monthly-review** - First of month report
4. **quarterly-prep** - Prompt for planning session

### User-Initiated Workflows
1. **set-goal** - Define new goal (any framework)
2. **quarterly-planning** - Full 90-day planning session
3. **progress-review** - Check status on all goals
4. **goal-update** - Modify existing goal
5. **project-plan** - Break goal into project plan
6. **reprioritize** - Adjust when circumstances change
7. **goal-retrospective** - Learn from completed/failed goals

---

## Quarterly Planning Workflow (Detailed)

```markdown
<workflow name="quarterly-planning">

<step n="1" goal="Review last quarter">
Let's start by reviewing last quarter (Q3 2025).

You set 5 goals:
✅ Goal 1: Achieve $50K revenue (DONE - $52K actual)
✅ Goal 2: Hire 2 team members (DONE)
⚠️  Goal 3: Launch marketing campaign (PARTIAL - launched but underperformed)
❌ Goal 4: Build iOS app (NOT COMPLETED - deprioritized)
✅ Goal 5: Establish partnerships (DONE - 3 partnerships)

**Success rate: 60% complete, 20% partial**

What worked well last quarter?
What didn't work?
What did you learn?

<template-output>quarter_review</template-output>
</step>

<step n="2" goal="Define planning horizon">
Now let's set your priorities for Q4 2025 (Oct 1 - Dec 31).

What's most important for the business this quarter?
- Revenue growth?
- Product development?
- Team building?
- Market expansion?
- Something else?

<template-output>focus_areas</template-output>
</step>

<step n="3" goal="Set quarterly goals">
Based on your focus, let's define 3-7 goals for Q4.

Remember the criteria:
- Specific and measurable
- Achievable in 90 days
- Significant impact on business
- Clear success criteria

For each goal, tell me:
- What is it?
- How will you measure success?
- Why is this important?

<template-output>quarterly_goals</template-output>
<invoke-task halt="true">{project-root}/bmad/core/tasks/adv-elicit.xml</invoke-task>
</step>

<step n="4" goal="Define milestones">
For each goal, let's break it into 3-5 milestones.

[For Goal 1: Launch new product line]

What are the key milestones to get there?

Example:
- Milestone 1: Complete market research (Oct 31)
- Milestone 2: Build MVP (Nov 30)
- Milestone 3: First paying customer (Dec 15)

<template-output>milestones</template-output>
</step>

<step n="5" goal="Identify dependencies">
What do you need to achieve these goals?
- Budget/resources?
- Team support?
- External partners?
- Technology/tools?

What could block progress?

<template-output>dependencies</template-output>
</step>

<step n="6" goal="Reality check">
Okay, let's reality check this plan.

You have 13 weeks in Q4.
You're setting X goals with Y total milestones.

Based on Q3 (60% completion rate), is this realistic?

Too ambitious? Too conservative? Just right?

<template-output>reality_check</template-output>
</step>

<step n="7" goal="Prioritize">
If you could only complete 3 of these goals, which 3 would have the biggest impact?

This helps when we need to make trade-offs mid-quarter.

<template-output>prioritization</template-output>
</step>

<step n="8" goal="Set check-in cadence">
How do you want to track these?

I suggest:
- Weekly: Quick progress pulse (5 min)
- Mid-quarter (Nov 15): Deep review, adjust if needed
- End of quarter (Dec 31): Full retrospective

Work for you?

<template-output>check_in_schedule</template-output>
</step>

<step n="9" goal="Generate Q4 plan">
Perfect. Generating your Q4 2025 plan...

[Agent creates structured document]

Saved to: {output_folder}/Q4-2025-Plan.md

I'll track these autonomously and flag if anything goes off track.

Let's execute. 📊

<template-output>complete_plan</template-output>
</step>

</workflow>
```

---

## User Stories (High-Level)

1. **Goal Setting**
   - Support multiple frameworks (OKR, Rocks, SMART, Custom)
   - Define measurable success criteria
   - Set timeframes (quarterly, annual, multi-year)

2. **Quarterly Planning**
   - Review last quarter
   - Set next quarter priorities
   - Define milestones and dependencies

3. **Progress Tracking**
   - Automatic status updates
   - Visual progress indicators
   - Timeline tracking

4. **Autonomous Monitoring**
   - Daily progress checks
   - Flag at-risk goals
   - Suggest interventions

5. **Project Planning**
   - Break goals into milestones
   - Create task lists
   - Identify dependencies

6. **Reporting**
   - Weekly progress summaries
   - Monthly reviews
   - Quarterly retrospectives

7. **Learning System**
   - Track completion patterns
   - Improve planning accuracy
   - Identify what works

---

## Integration Points

**Memory System (EPIC-1):**
- Stores all goals and progress
- Tracks historical completion rates

**Operator Agent (EPIC-3):**
- Tasks link to goals
- Task completion updates goal progress

**Chief of Staff (EPIC-2):**
- Provides goal status for briefings
- Routes goal-related questions

**Strategist (EPIC-5):**
- Quarterly goals ladder up to strategic vision
- Annual goals inform quarterly planning

---

## Dependencies

- EPIC-1 (Autonomous Agent Framework) - Required
- Goal storage system
- Task linkage system

---

## Risks & Mitigations

**Risk:** User doesn't complete quarterly planning (too long)
**Mitigation:** Allow incremental planning, save progress

**Risk:** Goals become stale/ignored
**Mitigation:** Autonomous monitoring flags lack of progress

**Risk:** Too many goals = nothing gets done
**Mitigation:** Agent suggests 3-7 max, challenges if too many

---

## Acceptance Criteria for Epic

- [ ] User can set goals in preferred framework
- [ ] Quarterly planning workflow completes successfully
- [ ] Goal progress tracked automatically
- [ ] At least one proactive alert when goal at risk
- [ ] Progress reports generated weekly/monthly
- [ ] User feels accountable to goals

---

## Stories in Epic

- STORY-4.1: Planner agent persona and definition
- STORY-4.2: Goal data model (framework agnostic)
- STORY-4.3: Goal-setting workflow
- STORY-4.4: Quarterly planning workflow
- STORY-4.5: Progress tracking system
- STORY-4.6: Autonomous monitoring
- STORY-4.7: Project planning (goal→milestones→tasks)
- STORY-4.8: Progress reporting (weekly/monthly)
- STORY-4.9: Goal retrospective workflow
- STORY-4.10: Learning system for planning accuracy

---

## Estimated Effort

**Epic Total:** 35-45 story points (approx. 2-3 weeks)

**Complexity:** High - Goal management + autonomous monitoring

**Value:** High - Keeps user focused on what matters most
