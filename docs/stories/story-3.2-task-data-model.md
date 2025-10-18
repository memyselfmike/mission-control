# Story 3.2: Design Task Data Model and Storage

**Epic:** EPIC-3 - Operator (Daily Execution Agent)
**Story Points:** 5
**Priority:** P1
**Type:** Data Model + API
**Status:** Ready
**Created:** 2025-10-18
**Sprint:** Sprint 4

---

## User Story

**As Omega (Operator agent)**, I want a flexible task data model and storage system so that I can track tasks, priorities, and completion status across user sessions.

---

## Description

Design and implement a comprehensive task management system that stores tasks with rich metadata (priority, status, time estimates, energy levels, goal links) and provides a clean API for task operations (create, read, update, delete, query).

This is the foundation for all Operator workflows - daily planning, briefings, and wrap-ups all rely on task data.

**Key Requirements:**
- Store tasks with rich metadata
- Support multiple priority frameworks (Eisenhower, MIT, custom)
- Track time estimates vs actuals (for learning)
- Link tasks to goals and projects
- Handle task state transitions (todo → in-progress → done)
- Query tasks by status, priority, date, goal

---

## Acceptance Criteria

### AC1: Task Data Model Defined
- Task structure includes: id, title, description, status, priority, dates, time estimates, energy level, context, links
- Status values: `todo`, `in_progress`, `done`, `blocked`, `deferred`
- Priority values: `must_win_today`, `important`, `should_do`, `nice_to_have`
- Energy levels: `high`, `medium`, `low`
- Context types: `deep_work`, `admin`, `communication`, `creative`

### AC2: Task Storage System Implemented
- File: `data/tasks/tasks.json` (JSON format for human readability)
- Backup on write (same as business context storage)
- Auto-create directory if missing
- Graceful error handling (missing files, corrupted JSON)

### AC3: Task Management API Created
- File: `mission-control/src/tasks.py`
- Functions: `create_task()`, `get_task()`, `update_task()`, `delete_task()`, `list_tasks()`
- Query functions: `get_tasks_by_status()`, `get_tasks_by_priority()`, `get_tasks_by_goal()`
- All functions return consistent data structures

### AC4: Task Operations Work Correctly
- Create task with all metadata
- Update task status (todo → in-progress → done)
- Update task priority
- Mark task complete (sets completion timestamp)
- Delete/archive old tasks

### AC5: Task Queries Work Correctly
- Get today's tasks
- Get must-win tasks
- Get tasks by status (all in-progress tasks)
- Get overdue tasks (past due date, not done)
- Get tasks linked to specific goal

### AC6: Time Tracking Supported
- Store estimated time (user provides)
- Store actual time (optional, user provides on completion)
- Calculate variance (actual vs estimated)
- Support learning over time (future enhancement)

### AC7: Integration with Memory System
- Tasks use same patterns as business context storage
- Tasks persist across sessions
- Tasks load on startup (integrate with `src/startup.py`)
- Tasks included in memory status reporting

---

## Technical Implementation

### Files to Create/Modify

```
mission-control/
├── src/tasks.py (new file - task management API)
├── src/startup.py (modify - load tasks on startup)
├── data/tasks/
│   ├── tasks.json (task storage)
│   └── .gitkeep
└── tests/
    └── test_tasks.py (new file - comprehensive tests)
```

### Task Data Structure

```python
{
    "tasks": [
        {
            "id": "TASK-001",
            "title": "Finish proposal for Client X",
            "description": "Complete financial projections and executive summary",
            "status": "in_progress",  # todo, in_progress, done, blocked, deferred
            "priority": "must_win_today",  # must_win_today, important, should_do, nice_to_have
            "estimated_time_minutes": 120,
            "actual_time_minutes": null,
            "energy_required": "high",  # high, medium, low
            "context": "deep_work",  # deep_work, admin, communication, creative
            "linked_to": {
                "goal_id": "GOAL-Q4-01",
                "project_id": "CLIENT-X"
            },
            "due_date": "2025-10-20",
            "created_date": "2025-10-18T09:00:00Z",
            "started_date": "2025-10-18T10:00:00Z",
            "completed_date": null,
            "deferred_until": null,
            "blocked_reason": null,
            "notes": "Needs financial data from Jordan (CFO)",
            "tags": ["client-work", "urgent"],
            "recurrence": null  # daily, weekly, monthly (future)
        }
    ],
    "metadata": {
        "version": "1.0",
        "last_updated": "2025-10-18T10:30:00Z",
        "total_tasks": 1,
        "completed_count": 0
    }
}
```

### API Function Signatures

```python
# src/tasks.py

from typing import Dict, List, Optional
from datetime import datetime

def create_task(
    title: str,
    description: str = "",
    priority: str = "should_do",
    estimated_time_minutes: Optional[int] = None,
    energy_required: str = "medium",
    context: str = "admin",
    due_date: Optional[str] = None,
    linked_to: Optional[Dict] = None,
    tags: List[str] = []
) -> Dict:
    """Create a new task and return task object."""
    pass

def get_task(task_id: str) -> Optional[Dict]:
    """Get a single task by ID."""
    pass

def update_task(task_id: str, updates: Dict) -> bool:
    """Update task fields. Returns True if successful."""
    pass

def delete_task(task_id: str) -> bool:
    """Delete a task. Returns True if successful."""
    pass

def list_tasks() -> List[Dict]:
    """Get all tasks."""
    pass

def get_tasks_by_status(status: str) -> List[Dict]:
    """Get all tasks with given status."""
    pass

def get_tasks_by_priority(priority: str) -> List[Dict]:
    """Get all tasks with given priority."""
    pass

def get_todays_tasks() -> List[Dict]:
    """Get tasks due today or overdue."""
    pass

def get_must_win_tasks() -> List[Dict]:
    """Get tasks marked as must_win_today."""
    pass

def mark_task_complete(task_id: str, actual_time_minutes: Optional[int] = None) -> bool:
    """Mark task as done, set completion timestamp."""
    pass

def load_tasks() -> Dict:
    """Load tasks from storage."""
    pass

def save_tasks(tasks_data: Dict) -> bool:
    """Save tasks to storage with backup."""
    pass
```

### Storage Patterns (Follow Story 2.1)

Use same patterns as business context storage:
- JSON format for human readability
- Backup before overwrite (`tasks.json.backup`)
- Auto-create directories
- Graceful error handling
- Return empty structure if file missing

---

## Testing Strategy

### Unit Tests (test_tasks.py)

**Test Coverage (20+ tests):**
1. Create task with minimal fields
2. Create task with all fields
3. Get task by ID
4. Update task status
5. Update task priority
6. Mark task complete (sets timestamp)
7. Delete task
8. List all tasks
9. Get tasks by status (todo, in_progress, done)
10. Get tasks by priority (must_win_today)
11. Get today's tasks
12. Get overdue tasks
13. Get tasks linked to goal
14. Time tracking (estimated vs actual)
15. Task ID generation (unique IDs)
16. Missing file handling (creates new)
17. Corrupted JSON handling (returns empty)
18. Backup creation on save
19. Empty task list handling
20. Task state transitions (todo → in_progress → done)

### Integration Tests
- Create task → reload from disk → verify persistence
- Create multiple tasks → query by status → verify correct results
- Update task → reload → verify changes persisted
- Task loading in startup.py integration

### Manual Testing
1. Create tasks via Python REPL
2. Verify tasks.json is human-readable
3. Edit tasks.json manually, reload, verify parsing
4. Delete tasks.json, verify graceful recreation

---

## Dependencies

**Prerequisites:**
- ✅ Story 2.1 complete (business context storage patterns)
- ✅ Story 2.4 complete (startup.py exists)
- ✅ Story 3.1 complete (Omega persona defined)

**Blocks:**
- Story 3.3: Daily Planning (needs task API)
- Story 3.4: Morning Briefing (needs task queries)
- Story 3.5: EOD Wrap-up (needs task completion)

---

## Definition of Done

- [ ] `src/tasks.py` created with all API functions
- [ ] Task data model documented in code
- [ ] `data/tasks/` directory created with .gitkeep
- [ ] `tests/test_tasks.py` created with 20+ tests
- [ ] All tests passing (100%)
- [ ] Task storage uses same patterns as Story 2.1
- [ ] Task loading integrated with `src/startup.py`
- [ ] All 7 acceptance criteria met
- [ ] Documentation updated (docstrings in tasks.py)
- [ ] Committed to git: "Story 3.2: Task data model and storage API"

---

## Estimated Effort

**5 story points** (1 day)

**Breakdown:**
- 2 hours: Design task data structure
- 2 hours: Implement task API functions (CRUD)
- 1 hour: Implement query functions (status, priority, date)
- 2 hours: Write comprehensive test suite (20+ tests)
- 1 hour: Integration with startup.py

---

## Notes

### Design Decisions

**Why JSON over JSONL?**
- Tasks are a single document (unlike conversation history which is append-only)
- JSON is more human-readable/editable
- Task list is relatively small (< 100 active tasks expected)

**Why File-Based Storage?**
- Consistent with EPIC-2 memory system
- No database dependencies
- Human-readable/editable
- Easy backup and version control
- Good enough for MVP (can migrate to DB later if needed)

### Future Enhancements (Not in Scope)
- Recurring tasks (daily, weekly, monthly)
- Task templates
- Sub-tasks and dependencies
- Task history/audit log
- Advanced queries (full-text search)
- Task archival system

### Integration Points
- **Omega workflows** will use this API for all task operations
- **Memory system** loads tasks on startup
- **Notification system** can alert on overdue tasks
- **Pattern recognition** can learn task completion patterns
- **Future Planner agent** will link tasks to goals

---

## Related Stories

**Sprint 4 (This Sprint):**
- Story 3.1: Operator persona (Omega) - ✅ Ready
- Story 3.3: Build daily planning workflow (depends on this)
- Story 3.4: Build morning briefing (depends on this)
- Story 3.5: Build EOD wrap-up (depends on this)

**Future Sprints:**
- Story 3.6: Task capture from conversations
- Story 3.9: Productivity pattern learning (uses task data)
- Story 4.x: Link tasks to goals (Planner integration)

---

**Story Status:** Draft → Pending approval

**Created by:** Bob (Scrum Master)
**Date:** 2025-10-18
**Sprint:** Sprint 4
