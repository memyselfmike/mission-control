# Story 3.6: Build Weekly Prep Workflow

**Epic:** EPIC-3 - Operator (Daily Execution Agent)
**Story Points:** 5
**Priority:** P1
**Type:** Workflow Implementation
**Status:** In Progress
**Created:** 2025-10-20
**Sprint:** Sprint 6 (post-EPIC-5R)
**Started:** 2025-10-25

---

## Implementation Note

**EPIC-5R Complete:** 2025-10-25
**Architecture Available:** Clean architecture with domain entities, repositories, use cases

This story will be implemented using the new Hexagonal Architecture:
- Domain layer: WeeklySummary entity, pattern detection services
- Application layer: Weekly prep use cases (GetWeekCompletionSummaryUseCase, etc.)
- Infrastructure layer: Existing repositories (JsonTaskRepository, memory repositories)
- Presentation layer: WeeklySummaryFormatter, BMAD workflow

Implementation will follow CLAUDE.md engineering standards (Section 11: When Adding New Features).

---

## User Story

**As a user**, I want Omega to guide me through a weekly reflection and planning session each Friday/Sunday so that I can review my progress, capture learnings, and set priorities for the upcoming week with confidence and clarity.

---

## Description

Build a structured weekly prep workflow that executes at the end of each week (Friday evening or Sunday afternoon). The workflow helps users:
- Reflect on the week's wins and challenges
- Review completion patterns and velocity
- Capture weekly learnings for pattern recognition
- Set top priorities for next week
- Plan key time blocks and commitments

This workflow connects daily execution (Stories 3.3, 3.4, 3.5) with longer-term strategic planning. It's Omega's "zoom out" moment - helping users see patterns and plan more effectively.

**Duration:** 15-20 minutes
**Frequency:** Weekly (Friday evening or Sunday afternoon, user preference)
**Trigger:** User says "weekly prep" OR "plan my week" OR autonomous prompt on schedule
**Voice:** Omega's energetic yet reflective style

---

## Acceptance Criteria

### AC1: Workflow Structure Implemented
- File: `mission-control/workflows/weekly-prep.md` (BMAD workflow format)
- 5 workflow steps: Review week, Analyze patterns, Capture learnings, Set priorities, Plan time blocks
- Each step has clear prompts, user inputs, and outputs
- Omega's supportive yet momentum-focused voice throughout

### AC2: Review Week Step
- Display week's completion stats (must-wins, total tasks, completion rate)
- Show daily breakdown (Monday-Friday performance)
- Celebrate wins with context ("You crushed 4/5 days this week!")
- Acknowledge challenges without judgment
- Output: Week summary with key metrics

### AC3: Analyze Patterns Step
- Calculate weekly velocity (tasks completed per day average)
- Identify peak productivity days ("Your best day was Tuesday - 5 tasks done")
- Detect blockers that appeared multiple times
- Compare to previous weeks (if data exists)
- Output: Pattern insights with actionable observations

### AC4: Capture Learnings Step
- Prompt: "What did you learn this week about how you work best?"
- Capture weekly insights (similar to daily learnings but higher level)
- Store learnings tagged with "weekly" category
- Link learnings to specific days/tasks if mentioned
- Output: Weekly learnings captured to memory

### AC5: Set Priorities Step
- Review incomplete tasks from last week (carry forward candidates)
- Prompt: "What are your TOP 3 priorities for next week?"
- Set weekly must-wins (different from daily must-wins)
- Validate priorities align with goals (if goals exist in memory)
- Output: Weekly priorities set, ready for Monday planning

### AC6: Plan Time Blocks Step
- Reference next week's calendar (if available)
- Suggest key time blocks for weekly priorities
- Identify potential conflicts or busy days
- Optional: Set specific days for specific priorities
- Output: Weekly time blocks suggested/confirmed

### AC7: Momentum and Closure
- Omega's forward-looking encouragement
- Clear next action: "Monday morning, we'll turn these into daily must-wins"
- Saved summary accessible for Monday planning
- Integration with morning briefing (reference weekly priorities)
- Output: User feels prepared and energized for next week

---

## Technical Implementation

### Files to Create/Modify

```
mission-control/
├── workflows/
│   └── weekly-prep.md (new file - BMAD workflow, 5 steps)
├── src/
│   └── weekly_prep.py (new file - weekly prep functions)
├── tests/
│   └── test_weekly_prep.py (new file - 15+ tests)
└── data/
    └── sessions/
        └── weekly-summaries/ (new folder - store weekly prep outputs)
```

### Weekly Prep Function Structure

```python
# src/weekly_prep.py

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

def get_week_completion_summary(start_date: str = None, end_date: str = None) -> Dict[str, Any]:
    """
    Get summary of week's task completion.

    Args:
        start_date: Week start date (YYYY-MM-DD). Defaults to last Monday.
        end_date: Week end date (YYYY-MM-DD). Defaults to last Friday.

    Returns:
        dict: Summary with:
            - week_range: "Oct 14-18, 2025"
            - completed: List of completed tasks
            - incomplete: List of incomplete tasks
            - daily_breakdown: {date: {completed: int, total: int}}
            - weekly_completion_rate: Percentage (0-100)
            - must_wins_completed: Count
            - must_wins_total: Count
            - total_completed: Total tasks completed
            - total_tasks: Total tasks
            - best_day: Date with highest completion
            - toughest_day: Date with lowest completion
    """
    pass

def calculate_weekly_velocity(weeks: int = 4) -> Dict[str, float]:
    """
    Calculate velocity metrics over recent weeks.

    Args:
        weeks: Number of weeks to analyze (default 4)

    Returns:
        dict: Velocity metrics:
            - avg_tasks_per_day: Average tasks completed per day
            - avg_tasks_per_week: Average tasks completed per week
            - completion_rate_trend: "improving" | "declining" | "stable"
            - this_week_velocity: This week's average
            - last_week_velocity: Last week's average
    """
    pass

def identify_weekly_patterns() -> Dict[str, Any]:
    """
    Identify patterns from the week's data.

    Returns:
        dict: Patterns detected:
            - best_days: List of days with highest completion
            - common_blockers: List of recurring blockers
            - peak_productivity_time: "morning" | "afternoon" | "evening"
            - task_types_completed: Distribution by type/priority
            - insights: List of actionable insights
    """
    pass

def capture_weekly_learning(learning: str, context: str = "", tags: List[str] = None) -> bool:
    """
    Capture weekly learning (higher-level than daily learnings).

    Args:
        learning: User's weekly insight
        context: Optional context
        tags: Optional tags (auto-adds "weekly" tag)

    Returns:
        bool: True if saved successfully
    """
    pass

def set_weekly_priorities(priority_ids: List[str], week_start: str = None) -> bool:
    """
    Set weekly must-win priorities (distinct from daily must-wins).

    Args:
        priority_ids: List of task IDs to mark as weekly priorities
        week_start: Week start date. Defaults to next Monday.

    Returns:
        bool: True if successful
    """
    pass

def get_weekly_priorities(week_start: str = None) -> List[Dict]:
    """
    Get weekly priorities for a specific week.

    Args:
        week_start: Week start date. Defaults to current week.

    Returns:
        List[dict]: Weekly priority tasks
    """
    pass

def save_weekly_summary(summary: Dict[str, Any]) -> bool:
    """
    Save weekly prep summary to memory.

    Args:
        summary: Dict with:
            - week_range: "Oct 14-18, 2025"
            - completion_rate: Percentage
            - wins: List of wins
            - learnings: List of learnings
            - patterns: Dict of patterns detected
            - next_week_priorities: List of priorities
            - notes: Optional notes

    Returns:
        bool: True if saved successfully
    """
    pass

def load_weekly_summary(week_start: str = None) -> Optional[Dict[str, Any]]:
    """
    Load weekly summary for a specific week.

    Args:
        week_start: Week start date. Defaults to current week.

    Returns:
        dict: Weekly summary or None
    """
    pass

def get_week_date_range(week_offset: int = 0) -> tuple:
    """
    Get start and end dates for a week.

    Args:
        week_offset: 0 for current week, -1 for last week, etc.

    Returns:
        tuple: (start_date, end_date) as date objects
    """
    pass

def format_weekly_summary(summary: Dict[str, Any]) -> str:
    """
    Format weekly summary for display.

    Args:
        summary: Weekly summary dict

    Returns:
        str: Formatted summary text
    """
    pass
```

---

## Testing Strategy

### Unit Tests (test_weekly_prep.py)

**Test Coverage (15+ tests):**

1. **Week Completion Summary Tests (4 tests)**
   - Test with full week of data (all 5 days complete)
   - Test with partial week (some days missing)
   - Test with no data (empty week)
   - Test daily breakdown accuracy

2. **Weekly Velocity Tests (3 tests)**
   - Calculate velocity with 4 weeks of data
   - Calculate velocity with 1 week of data
   - Detect trend: improving, declining, stable

3. **Pattern Detection Tests (3 tests)**
   - Identify best/worst days
   - Detect recurring blockers
   - Generate actionable insights

4. **Weekly Learning Tests (2 tests)**
   - Capture weekly learning with auto-tag
   - Load weekly learnings from JSONL

5. **Weekly Priorities Tests (3 tests)**
   - Set weekly priorities (3 tasks)
   - Load weekly priorities for current week
   - Load priorities for future week

6. **Summary Save/Load Tests (2 tests)**
   - Save weekly summary to JSON
   - Load weekly summary by date

7. **Helper Function Tests (3 tests)**
   - Get week date range (current, last, next)
   - Format weekly summary for display
   - Handle edge cases (partial data)

8. **Integration Test (1 test)**
   - Full weekly prep workflow from start to finish

### Integration Tests
- Weekly prep integrates with daily planning (Monday uses weekly priorities)
- Weekly prep integrates with EOD wrap-up (data continuity)
- Weekly prep integrates with memory system (learnings storage)

### Manual Testing (with Mike)
1. Run weekly prep at end of week → see completion stats
2. Review pattern insights → validate accuracy
3. Set weekly priorities → verify Monday planning uses them
4. Test with incomplete week data → graceful handling
5. Verify Omega's voice/tone throughout
6. Confirm workflow feels energizing, not burdensome

---

## Dependencies

**Prerequisites:**
- ✅ Story 3.2 complete (Task data model - tasks.py)
- ✅ Story 3.3 complete (Daily planning workflow)
- ✅ Story 3.5 complete (EOD wrap-up - learnings pattern)
- ✅ Story 2.1, 2.2, 2.3 complete (Memory system)

**Blocks:**
- None (can be implemented independently)

**Optional Integration:**
- Story 3.4: Morning briefing could reference weekly priorities
- Story 3.7: Pattern learning could enhance insights

---

## Definition of Done

- [ ] `workflows/weekly-prep.md` created with 5 steps
- [ ] `src/weekly_prep.py` created with 10 functions
- [ ] `tests/test_weekly_prep.py` created (15+ tests)
- [ ] All tests passing (100%)
- [ ] All 7 acceptance criteria met
- [ ] Omega's voice consistent throughout
- [ ] Workflow completes in 15-20 minutes
- [ ] Manual testing with Mike successful
- [ ] Committed to git: "Story 3.6: Weekly prep workflow with Omega"

---

## Estimated Effort

**5 story points** (1 day)

**Breakdown:**
- 2 hours: Design workflow structure (5 steps)
- 2 hours: Implement weekly prep functions (week summary, velocity, patterns)
- 1 hour: Integrate with task system (weekly priorities)
- 1 hour: Pattern detection and insights logic
- 2 hours: Write comprehensive tests (15+ tests)
- 1 hour: Manual testing and refinement
- 1 hour: Documentation and polish

---

## Notes

### Design Decisions

**Why Weekly vs Daily?**
- Daily: Tactical execution ("What must I do today?")
- Weekly: Strategic planning ("What matters this week?")
- Different time horizons require different planning modes
- Weekly prep prevents "busy but not productive" weeks

**Why Friday Evening OR Sunday Afternoon?**
- User preference drives timing
- Friday: Close out work week while fresh in mind
- Sunday: Prepare mindset for upcoming week
- Both valid - let user choose in settings

**Why 5 Steps?**
1. Review: Look back with data
2. Analyze: Understand patterns
3. Learn: Capture insights
4. Prioritize: Set top 3 for week
5. Plan: Block time for priorities

Mirrors EOD structure but at weekly level.

**Why Track Weekly Priorities Separately?**
- Daily must-wins: "Today's top 3"
- Weekly priorities: "This week's top 3"
- Different granularity - weekly guides daily
- Monday planning converts weekly priorities → daily must-wins

### Omega's Voice in Weekly Prep

Throughout this workflow:
- ✅ **Celebrate the week:** "You completed 18 tasks this week - that's momentum!"
- ✅ **Data-driven insights:** "Your best day was Tuesday - you knocked out 5 tasks."
- ✅ **No judgment on tough days:** "Wednesday was tough, but you showed up."
- ✅ **Forward focus:** "Next week, we're going after these 3 priorities."
- ✅ **Energizing close:** "You've got clarity. Monday, we execute. ⚡"

### Psychological Benefits

Research shows weekly reflection:
- Increases goal achievement by 33% (progress monitoring)
- Reduces stress through planning clarity
- Builds self-efficacy through win recognition
- Enables pattern learning and improvement
- Prevents "drift" from important to urgent

### Future Enhancements (Not in Scope)
- Month-end reviews (monthly patterns)
- Quarter planning integration
- Goal progress tracking in weekly prep
- Team weekly syncs (if team features added)
- Comparative analytics ("This week vs last 4 weeks")
- Suggested weekly themes based on patterns

### Integration with Other Systems

- **Task System (Story 3.2):** Reads completion data, sets weekly priorities
- **Memory System:** Stores learnings, summaries
- **Daily Planning (Story 3.3):** Weekly priorities feed Monday planning
- **EOD Wrap-up (Story 3.5):** Daily data aggregates to weekly
- **Pattern Recognition (Story 3.7):** Can enhance insights with ML

---

## Related Stories

**Sprint 5 (This Sprint):**
- Story 3.6: Weekly prep workflow (this story)
- Story 3.7: Productivity pattern learning
- Story 3.8: Autonomous task reminders

**Previous Sprints:**
- Story 3.3: Daily planning workflow - ✅ Done
- Story 3.4: Morning briefing - ✅ Done
- Story 3.5: EOD wrap-up - ✅ Done

**Future Sprints:**
- Story 4.x: Monthly/quarterly planning
- Story 4.x: Goal tracking and OKRs
- Story 6.x: Analytics dashboard (trends)

---

**Story Status:** Draft → Pending SM approval

**Created by:** Bob (Scrum Master)
**Date:** 2025-10-20
**Sprint:** Sprint 5
