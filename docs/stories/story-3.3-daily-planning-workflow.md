# Story 3.3: Build Daily Planning Workflow

**Epic:** EPIC-3 - Operator (Daily Execution Agent)
**Story Points:** 8
**Priority:** P1
**Type:** Workflow Implementation
**Status:** Draft
**Created:** 2025-10-18
**Sprint:** Sprint 4

---

## User Story

**As a user**, I want a structured daily planning workflow with Omega so that I can start each day with clear priorities, time-blocked focus sessions, and confidence in what I need to accomplish.

---

## Description

Build Omega's signature daily planning workflow that guides users through:
1. Calendar/commitment review
2. Task brain dump
3. Prioritization (Eisenhower Matrix default, supports multiple frameworks)
4. Must-win task identification (1-3 per day)
5. Time blocking recommendations
6. Daily intention setting

This workflow embodies Omega's action-oriented, energetic personality and provides the foundation for daily execution.

**Workflow Duration:** Target 5-10 minutes
**Invocation:** User says "plan my day" OR autonomous morning prompt
**Output:** Prioritized task list, time blocks, daily intention

---

## Acceptance Criteria

### AC1: Workflow Structure Implemented
- File: `mission-control/workflows/daily-planning.md` (BMAD workflow format)
- 6 workflow steps: calendar review, brain dump, prioritization, must-wins, time blocking, intention
- Each step has clear prompts, user inputs, and outputs
- Omega's energetic voice throughout

### AC2: Calendar Review Step
- Display user's commitments (from memory or manual input)
- Identify available time blocks
- Calculate total available hours for work
- Highlight conflicts or tight schedules
- Output: Calendar summary with available blocks

### AC3: Task Brain Dump Step
- Prompt user to list everything on their mind
- Capture tasks quickly (no judgment, no organization yet)
- Add new tasks to task system (Story 3.2 API)
- Pull in existing tasks from task list
- Output: Complete task inventory (new + existing)

### AC4: Prioritization Framework Step
- **Default:** Eisenhower Matrix (Important/Urgent quadrants)
- **Alternative:** MIT (Most Important Tasks - pick 3)
- **Alternative:** Custom (user defines their own system)
- Categorize tasks into priority levels
- Identify must-win vs nice-to-have
- Output: Tasks sorted by priority

### AC5: Must-Win Identification
- Identify 1-3 "must win today" tasks
- Validate with user ("If you only did these 3, successful day?")
- Mark these tasks as `priority: must_win_today` in task system
- Output: Top 3 must-win tasks with estimated times

### AC6: Time Blocking Recommendations
- Match must-win tasks to best available time blocks
- Consider task energy level (high energy → morning blocks)
- Suggest focus blocks for deep work
- Protect time from interruptions
- Output: Time-blocked schedule

### AC7: Daily Intention Setting
- Prompt: "Today will be a great day if I..."
- Capture user's daily north star
- Store in memory for EOD reflection
- Output: One-sentence daily intention

---

## Technical Implementation

### Files to Create/Modify

```
mission-control/
├── workflows/
│   └── daily-planning.md (new file - BMAD workflow)
├── src/
│   ├── workflows.py (new file - workflow execution engine)
│   └── prioritization.py (new file - prioritization frameworks)
├── tests/
│   ├── test_workflows.py (workflow execution tests)
│   └── test_prioritization.py (framework tests)
└── data/
    └── sessions/
        └── daily-plans/ (store daily plan outputs)
```

### Workflow File Structure (daily-planning.md)

```markdown
# Daily Planning Workflow

**Agent:** Omega (Operator)
**Duration:** 5-10 minutes
**Frequency:** Daily (morning)
**Triggers:** User request OR autonomous morning prompt

---

<workflow name="daily-planning">

<step n="1" goal="Review calendar and commitments">
⚡ Good morning! Let's plan your day.

First, what's on your calendar today?

[Agent prompts for commitments or loads from memory]

Available blocks:
- 6-9am: 3 hours
- 11am-2pm: 3 hours
- After 4pm: Open

Total available: 6+ hours

Sound right?

<template-output>calendar_review</template-output>
</step>

<step n="2" goal="Brain dump all tasks">
What's on your mind for today? Tell me everything - we'll organize it.

[User lists tasks, Omega captures to task system]

Got it. I count {n} items. Let's prioritize.

<template-output>task_inventory</template-output>
</step>

<step n="3" goal="Apply prioritization framework">
Let's sort using Important vs Urgent:

**MUST WIN TODAY (Important + Urgent):**
1. [Task from user input]
2. [Task from user input]

**IMPORTANT, NOT URGENT (Your leverage work):**
3. [Strategic tasks]

**URGENT, NOT IMPORTANT (Minimize these):**
4. [Reactive items]

**DELETE/DEFER:**
5. [Low-value tasks]

Does this feel right?

<template-output>prioritized_list</template-output>
</step>

<step n="4" goal="Identify must-wins">
Your TOP 3 MUST-WIN tasks today:

1. **[Task 1]** ({time}, {energy_level})
2. **[Task 2]** ({time}, {energy_level})
3. **[Task 3]** ({time}, {energy_level})

If you only did these 3, successful day?

<template-output>must_wins</template-output>
</step>

<step n="5" goal="Time blocking">
Here's my recommendation:

**6-8am: DEEP WORK - [Task 1]**
- Your best focus time
- 2 hours uninterrupted
- Turn off Slack, close email

**10:30-11am: [Task 2]**
- After morning meeting
- Fresh mind for this

**12:30-1:30pm: [Task 3]**
- After lunch, energy is good

Sound good?

<template-output>time_blocks</template-output>
</step>

<step n="6" goal="Set daily intention">
One last thing. Complete this:

"Today will be a great day if I..."

[User provides intention]

Love it. That's your north star today.

Let's execute. 💪

<template-output>daily_intention</template-output>
</step>

</workflow>
```

### Prioritization Frameworks (prioritization.py)

```python
# src/prioritization.py

def eisenhower_matrix(tasks: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorize tasks using Eisenhower Matrix (Important/Urgent).

    Returns dict with quadrants:
    - must_win_today: Important + Urgent
    - important_not_urgent: Important, Not Urgent
    - urgent_not_important: Urgent, Not Important
    - defer_delete: Neither Important nor Urgent
    """
    pass

def mit_framework(tasks: List[Dict], max_tasks: int = 3) -> List[Dict]:
    """
    Most Important Tasks - pick top N tasks for the day.
    Default is 3 (MITs).
    """
    pass

def time_blocking_suggestions(
    tasks: List[Dict],
    available_blocks: List[Dict]
) -> List[Dict]:
    """
    Match tasks to time blocks based on:
    - Task energy_required vs block time of day
    - Task estimated_time_minutes vs block duration
    - Task priority

    Returns suggested schedule.
    """
    pass
```

---

## Testing Strategy

### Unit Tests (test_workflows.py)

**Test Coverage (15+ tests):**
1. Load daily-planning.md workflow
2. Execute workflow step-by-step
3. Capture user inputs at each step
4. Generate structured outputs
5. Store workflow results
6. Handle workflow interruption (user exits mid-workflow)
7. Resume workflow from last step

### Prioritization Tests (test_prioritization.py)

**Test Coverage (10+ tests):**
1. Eisenhower Matrix with mixed tasks
2. Eisenhower Matrix with all urgent tasks
3. Eisenhower Matrix with all important tasks
4. MIT framework picks top 3
5. MIT framework with fewer than 3 tasks
6. Time blocking with morning high-energy task
7. Time blocking with multiple blocks
8. Time blocking with no available blocks
9. Time blocking respects task duration
10. Time blocking handles conflicts

### Integration Tests
- Full workflow execution (all 6 steps)
- Task creation during brain dump
- Task priority updates during prioritization
- Time blocks stored and retrievable
- Daily intention stored for EOD reference

### Manual Testing (with Mike)
1. Run full daily planning workflow
2. Try Eisenhower Matrix prioritization
3. Try MIT prioritization
4. Verify Omega's voice/tone throughout
5. Confirm 5-10 minute completion time
6. Check task persistence after workflow

---

## Dependencies

**Prerequisites:**
- ✅ Story 3.1 complete (Omega persona)
- ✅ Story 3.2 complete (Task API)
- Memory system (load/save workflow outputs)

**Blocks:**
- Story 3.4: Morning Briefing (needs this workflow)
- Story 3.5: EOD Wrap-up (references daily intention from this workflow)

---

## Definition of Done

- [ ] `workflows/daily-planning.md` created with 6 steps
- [ ] `src/workflows.py` created (workflow execution engine)
- [ ] `src/prioritization.py` created with 3 frameworks
- [ ] `tests/test_workflows.py` created (15+ tests)
- [ ] `tests/test_prioritization.py` created (10+ tests)
- [ ] All tests passing (100%)
- [ ] All 7 acceptance criteria met
- [ ] Omega's voice/tone consistent throughout
- [ ] Workflow completes in 5-10 minutes
- [ ] Manual testing with Mike successful
- [ ] Committed to git: "Story 3.3: Daily planning workflow with Omega"

---

## Estimated Effort

**8 story points** (1.5-2 days)

**Breakdown:**
- 2 hours: Design workflow structure (6 steps)
- 3 hours: Implement workflow execution engine
- 2 hours: Implement prioritization frameworks (Eisenhower, MIT)
- 2 hours: Implement time blocking logic
- 3 hours: Write comprehensive tests (25+ tests)
- 2 hours: Integration testing and refinement
- 1 hour: Documentation and polish

---

## Notes

### Design Decisions

**Why Workflow Files (Markdown)?**
- Follows BMAD Method patterns
- Human-readable and editable
- Clear structure for step-by-step execution
- Can be customized without code changes

**Why Default to Eisenhower Matrix?**
- Most widely recognized framework
- Balances urgency with importance
- Prevents "urgent-only" firefighting
- User can override with MIT or custom

**Why 1-3 Must-Wins?**
- Research shows 1-3 is achievable
- More than 3 dilutes focus
- Gives clear success criteria for the day
- Prevents overwhelming task lists

### Omega's Voice in Workflow

Throughout the workflow, Omega should:
- Use energetic, action-oriented language
- Ask "What's the next action?" mindset
- Celebrate decisions ("Love it!")
- Challenge gently ("If you only did these 3...")
- Use momentum language ("Let's execute")
- Include ⚡ emoji for energy

### Future Enhancements (Not in Scope)
- Calendar API integration (auto-load calendar)
- Machine learning for time estimates
- Pattern recognition (what usually gets done when)
- Weekly planning integration
- Goal alignment in prioritization

### Integration with Other Systems

- **Task System (Story 3.2):** Creates/updates tasks
- **Memory System:** Stores daily intentions, time blocks
- **Notification System:** Can remind about time blocks
- **Pattern Recognition:** Can learn best planning times
- **Future Planner Agent:** Can align tasks with goals

---

## Related Stories

**Sprint 4 (This Sprint):**
- Story 3.1: Operator persona (Omega) - ✅ Ready
- Story 3.2: Task data model - Draft
- Story 3.4: Morning briefing (uses this workflow)
- Story 3.5: EOD wrap-up (references daily intention)

**Future Sprints:**
- Story 3.6: Task capture from conversations
- Story 3.8: Weekly prep workflow
- Story 3.9: Productivity pattern learning
- Story 4.x: Goal-task alignment (Planner integration)

---

**Story Status:** Draft → Pending approval

**Created by:** Bob (Scrum Master)
**Date:** 2025-10-18
**Sprint:** Sprint 4
