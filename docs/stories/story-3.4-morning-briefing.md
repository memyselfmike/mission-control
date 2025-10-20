# Story 3.4: Build Morning Briefing Generator

**Epic:** EPIC-3 - Operator (Daily Execution Agent)
**Story Points:** 5
**Priority:** P1
**Type:** Autonomous Workflow
**Status:** Ready
**Created:** 2025-10-18
**Sprint:** Sprint 4

---

## User Story

**As a user**, I want Omega to greet me with an energizing morning briefing when I start Mission Control so that I immediately understand my priorities and context for the day ahead.

---

## Description

Build an autonomous morning briefing that executes when Mission Control starts (integrated with Story 2.4 startup system). The briefing:
- Greets user with energy and context
- Summarizes today's must-win tasks
- Highlights any overdue items
- Shows available time blocks
- Offers to run full daily planning
- Loads relevant context from memory

This is Omega's "first impression" - it should feel energizing, focused, and immediately valuable.

**Duration:** 30 seconds to read
**Trigger:** Automatic on Mission Control startup (morning hours)
**Voice:** Omega's energetic, action-oriented style

---

## Acceptance Criteria

### AC1: Morning Briefing Function Created
- File: `mission-control/src/morning_briefing.py`
- Function: `generate_morning_briefing()` returns formatted text
- Integrates with `src/startup.py` (Story 2.4)
- Executes automatically on startup during morning hours (6am-12pm learned time)

### AC2: Briefing Content Structure
- Greeting (time-aware: "Good morning!")
- Date and day of week
- Must-win tasks (from task system)
- Overdue tasks (if any)
- Available time blocks
- Prompt to run daily planning
- Omega's energetic sign-off

### AC3: Context from Memory Loaded
- User's name (from business context)
- Must-win tasks (from task system)
- Overdue tasks (from task system)
- Yesterday's completion stats (optional, from memory)
- Any pending notifications (from notification system)

### AC4: Time-Aware Greeting
- Morning (6am-12pm): "Good morning! ⚡"
- Afternoon (12pm-5pm): "Good afternoon! Let's refocus."
- Evening (5pm-10pm): "Good evening! Wrapping up or planning tomorrow?"
- Night/Early (10pm-6am): Skip briefing (user is likely not working)

### AC5: Task Summary Quality
- Shows top 3 must-win tasks (if set from yesterday's planning)
- Shows overdue count (without overwhelming details)
- Shows today's task count
- Highlights if no tasks are planned (prompts planning)

### AC6: Actionable Next Steps
- If tasks exist: "Ready to execute? Type 'go' to begin!"
- If no tasks: "Want to plan your day? Type 'plan my day' to start."
- If overdue exists: "You have {n} overdue tasks. Want to triage?"
- Always includes option to run daily planning workflow

### AC7: Performance and UX
- Briefing generates in <500ms
- Output is formatted with Rich library (colors, emphasis)
- Not too verbose (30 seconds to read)
- Skippable (doesn't block conversation start)
- User preference: can disable briefing in settings

---

## Technical Implementation

### Files to Create/Modify

```
mission-control/
├── src/
│   ├── morning_briefing.py (new file - briefing generator)
│   └── startup.py (modify - integrate briefing)
├── tests/
│   └── test_morning_briefing.py (new file - tests)
└── .claude/
    └── settings.json (add briefing preferences)
```

### Morning Briefing Function Structure

```python
# src/morning_briefing.py

from datetime import datetime
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from src.tasks import get_must_win_tasks, get_tasks_by_status
from src.memory import load_business_context

def generate_morning_briefing() -> str:
    """
    Generate morning briefing with tasks, context, and next actions.

    Returns formatted briefing text (Rich markup).
    """
    # Load context
    business_context = load_business_context()
    user_name = business_context.get("user_name", "there")

    # Load tasks
    must_wins = get_must_win_tasks()
    overdue = get_overdue_tasks()
    today_tasks = get_todays_tasks()

    # Time-aware greeting
    hour = datetime.now().hour
    greeting = get_time_aware_greeting(hour)

    # Build briefing
    briefing = f"""
{greeting} {user_name}!

📅 **{datetime.now().strftime("%A, %B %d, %Y")}**

{format_task_summary(must_wins, overdue, today_tasks)}

{suggest_next_action(must_wins, overdue)}

⚡ Omega
"""

    return briefing

def get_time_aware_greeting(hour: int) -> str:
    """Return greeting based on time of day."""
    if 6 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    elif 17 <= hour < 22:
        return "Good evening!"
    else:
        return None  # Skip briefing at night

def format_task_summary(must_wins, overdue, today_tasks) -> str:
    """Format task summary section."""
    lines = []

    if must_wins:
        lines.append("**MUST WIN TODAY:**")
        for i, task in enumerate(must_wins[:3], 1):
            lines.append(f"{i}. {task['title']}")
    elif today_tasks:
        lines.append(f"**TODAY:** {len(today_tasks)} tasks")
    else:
        lines.append("**No tasks planned for today.**")

    if overdue:
        lines.append(f"\n⚠️  **{len(overdue)} overdue tasks**")

    return "\n".join(lines)

def suggest_next_action(must_wins, overdue) -> str:
    """Suggest next action based on task state."""
    if must_wins:
        return "Ready to execute? Let's knock out those must-wins! 💪"
    elif overdue:
        return "Want to triage those overdue tasks? Type 'triage'."
    else:
        return "Want to plan your day? Type 'plan my day' to start."

def should_show_briefing() -> bool:
    """Determine if briefing should show (time + preferences)."""
    hour = datetime.now().hour
    if not (6 <= hour < 22):
        return False

    # Check user preferences
    # settings = load_settings()
    # return settings.get("morning_briefing_enabled", True)

    return True
```

### Integration with Startup (startup.py)

```python
# src/startup.py (modification)

from src.morning_briefing import generate_morning_briefing, should_show_briefing

def initialize_system():
    """Initialize Mission Control on startup."""
    # ... existing initialization ...

    # Morning briefing (if appropriate time)
    if should_show_briefing():
        briefing = generate_morning_briefing()
        if briefing:
            console = Console()
            console.print(Panel(briefing, title="⚡ Omega - Morning Briefing", border_style="cyan"))

    # ... continue with normal startup ...
```

---

## Testing Strategy

### Unit Tests (test_morning_briefing.py)

**Test Coverage (15+ tests):**
1. Generate briefing with must-win tasks
2. Generate briefing with overdue tasks
3. Generate briefing with no tasks
4. Time-aware greeting (morning, afternoon, evening)
5. Skip briefing at night (10pm-6am)
6. Format task summary (1 task, 3 tasks, 10+ tasks)
7. Suggest next action (has tasks, no tasks, overdue)
8. Load user name from business context
9. Load tasks from task system
10. Handle missing business context gracefully
11. Handle empty task list gracefully
12. Performance test (<500ms generation)
13. Rich formatting renders correctly
14. User preference: briefing disabled
15. Briefing skips if already shown today (optional)

### Integration Tests
- Full startup sequence with briefing
- Briefing + Alpha greeting coordination
- Briefing loads all context correctly
- Briefing integrates with notification system

### Manual Testing (with Mike)
1. Start Mission Control in morning → see briefing
2. Start Mission Control in evening → see different greeting
3. Start with no tasks → see planning prompt
4. Start with must-wins → see task list
5. Start with overdue → see triage prompt
6. Verify Omega's voice/tone
7. Verify briefing is helpful, not annoying

---

## Dependencies

**Prerequisites:**
- ✅ Story 2.4 complete (startup.py exists)
- ✅ Story 3.1 complete (Omega persona)
- ✅ Story 3.2 complete (Task API)

**Optional:**
- Story 3.3: Daily Planning (briefing can prompt this)
- Story 1.10: Notification System (can show pending notifications)

**Blocks:**
- None (can be implemented independently)

---

## Definition of Done

- [ ] `src/morning_briefing.py` created with all functions
- [ ] `src/startup.py` updated to call briefing
- [ ] `tests/test_morning_briefing.py` created (15+ tests)
- [ ] All tests passing (100%)
- [ ] All 7 acceptance criteria met
- [ ] Briefing generates in <500ms
- [ ] Omega's voice consistent throughout
- [ ] Manual testing with Mike successful
- [ ] Briefing is helpful and energizing (not annoying)
- [ ] Committed to git: "Story 3.4: Morning briefing with Omega"

---

## Estimated Effort

**5 story points** (1 day)

**Breakdown:**
- 2 hours: Design briefing structure and content
- 2 hours: Implement briefing generation function
- 1 hour: Integrate with startup.py
- 2 hours: Rich formatting and UX polish
- 2 hours: Write comprehensive tests (15+ tests)
- 1 hour: Manual testing and refinement

---

## Notes

### Design Decisions

**Why Show Briefing at Startup?**
- Immediate value on application start
- Sets the tone for the day
- No extra user action required
- Can be skipped if not desired

**Why Time-Aware Greetings?**
- Shows context awareness
- Feels more personal
- Different times have different priorities
- Night/early morning: skip to avoid annoyance

**Why Keep It Short?**
- Users want to start working quickly
- Long briefings are ignored
- 30 seconds to read is sweet spot
- Can dive deeper with daily planning workflow

### Omega's Voice in Briefing

The briefing should embody Omega's personality:
- **Energetic:** "Let's knock out those must-wins!"
- **Action-oriented:** "Ready to execute?"
- **Focused:** Shows only what matters (top 3 tasks)
- **Momentum:** Uses ⚡ emoji, "Let's go" language
- **Supportive:** Celebrates readiness, offers help if behind

### Future Enhancements (Not in Scope)
- Weather/calendar API integration
- Habit streaks ("5 days of planning in a row!")
- Motivational quotes
- Yesterday's completion percentage
- Week-at-a-glance view
- Customizable briefing templates
- Voice output (text-to-speech)

### User Preferences (Future)

Settings to control briefing:
- `morning_briefing_enabled`: true/false
- `morning_briefing_start_time`: "6:00"
- `morning_briefing_end_time`: "12:00"
- `morning_briefing_style`: "full" | "minimal"

---

## Related Stories

**Sprint 4 (This Sprint):**
- Story 3.1: Operator persona (Omega) - ✅ Ready
- Story 3.2: Task data model - Draft
- Story 3.3: Daily planning workflow - Draft
- Story 3.5: EOD wrap-up - Draft

**Future Sprints:**
- Story 3.8: Weekly prep workflow
- Story 3.9: Productivity pattern learning
- Story 2.4+: Enhanced startup personalization

---

**Story Status:** Draft → Pending approval

**Created by:** Bob (Scrum Master)
**Date:** 2025-10-18
**Sprint:** Sprint 4

---

## Dev Agent Record

### Context Reference
- Story Context XML: `docs/stories/story-context-3.4-morning-briefing.xml` (Generated: 2025-10-20)
