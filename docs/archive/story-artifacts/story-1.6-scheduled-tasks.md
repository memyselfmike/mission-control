# Story 1.6: Scheduled Task Execution Framework

**Epic:** EPIC-1 - Autonomous Agent Framework
**Story Points:** 8
**Priority:** P0 (Critical Path)
**Sprint:** Sprint 2

---

## Story Description

Create a framework for agents to execute tasks on schedules (daily, weekly, monthly). This enables autonomous behaviors like daily briefings, weekly reviews, and periodic reminders.

---

## Acceptance Criteria

- [ ] AC-1: Cron-style scheduler implemented
- [ ] AC-2: Tasks can be registered with schedules
- [ ] AC-3: Tasks execute reliably at specified times
- [ ] AC-4: Failed tasks can be retried
- [ ] AC-5: Execution logged for audit trail
- [ ] AC-6: Tests written (8-10 tests minimum)

---

## Architecture Design

### Components

```
mission-control/
├── src/
│   ├── scheduler.py          # Main scheduler (runs scheduling loop)
│   ├── task_registry.py      # Task registration and storage
│   └── handlers/
│       ├── __init__.py
│       ├── daily_briefing.py # Example: Daily briefing handler
│       └── test_handler.py   # Example: Test handler
├── data/
│   ├── tasks/
│   │   └── scheduled_tasks.json  # Task definitions
│   └── logs/
│       └── task_execution.jsonl  # Execution logs
└── tests/
    └── test_scheduler.py     # Scheduler tests
```

### Data Model

**Task Definition:**
```json
{
  "id": "daily_briefing_9am",
  "name": "Daily Briefing",
  "description": "Generate morning briefing for user",
  "schedule": {
    "type": "daily",
    "time": "09:00"
  },
  "handler": "handlers.daily_briefing.run",
  "enabled": true,
  "metadata": {
    "created": "2025-10-16T12:00:00Z",
    "created_by": "system",
    "last_modified": "2025-10-16T12:00:00Z"
  },
  "execution_history": {
    "last_run": "2025-10-16T09:00:00Z",
    "next_run": "2025-10-17T09:00:00Z",
    "total_runs": 5,
    "success_count": 5,
    "failure_count": 0
  },
  "retry_policy": {
    "max_retries": 3,
    "retry_delay_seconds": 300
  }
}
```

**Execution Log Entry:**
```json
{
  "timestamp": "2025-10-16T09:00:15Z",
  "task_id": "daily_briefing_9am",
  "status": "success",
  "duration_ms": 234,
  "output": "Briefing generated successfully",
  "error": null
}
```

### Schedule Types Supported

1. **Daily:** Execute at specific time every day
   ```json
   {"type": "daily", "time": "09:00"}
   ```

2. **Weekly:** Execute on specific day(s) at specific time
   ```json
   {"type": "weekly", "days": ["monday", "friday"], "time": "09:00"}
   ```

3. **Interval:** Execute every N minutes/hours
   ```json
   {"type": "interval", "minutes": 30}
   ```

4. **Cron:** Advanced cron-style expressions (future)
   ```json
   {"type": "cron", "expression": "0 9 * * 1-5"}
   ```

---

## Technical Approach

### Technology Stack

**Scheduling Library:** Python `schedule`
- Pros: Simple, lightweight, easy to test
- Cons: In-process only (acceptable for MVP)

**Alternative Considered:** APScheduler
- More features but more complex
- Can upgrade later if needed

### Task Handler Contract

All task handlers must follow this interface:

```python
def run(context: dict) -> dict:
    """
    Execute the scheduled task.

    Args:
        context: Task execution context
            - task_id: str
            - scheduled_time: datetime
            - execution_id: str

    Returns:
        dict: Execution result
            - status: "success" | "failure"
            - output: str (success message or data)
            - error: str | None (error message if failed)

    Raises:
        Exception: If task fails critically
    """
    pass
```

### Scheduler Lifecycle

```python
# 1. Initialize
scheduler = TaskScheduler()
scheduler.load_tasks()

# 2. Run scheduling loop (background)
scheduler.start()  # Non-blocking

# 3. Register new tasks dynamically
scheduler.register_task({
    "id": "new_task",
    "schedule": {"type": "daily", "time": "14:00"},
    "handler": "handlers.my_handler.run"
})

# 4. Graceful shutdown
scheduler.stop()
```

---

## Implementation Plan

### Phase 1: Core Infrastructure (Day 1)
1. ✅ Create data model schemas
2. ✅ Implement task registry (save/load JSON)
3. ✅ Write task registration tests
4. ✅ Implement task registration

### Phase 2: Scheduler (Day 2)
5. ⏳ Write scheduler tests
6. ⏳ Implement scheduler with `schedule` library
7. ⏳ Add execution logging
8. ⏳ Add retry logic

### Phase 3: Example Handlers (Day 2)
9. ⏳ Create test handler (simple "hello world")
10. ⏳ Create daily briefing handler (reads context, generates briefing)
11. ⏳ Integration test end-to-end

---

## API Design

### Task Registry API

```python
# task_registry.py

def register_task(task_def: dict) -> bool:
    """Register a new scheduled task"""

def unregister_task(task_id: str) -> bool:
    """Remove a scheduled task"""

def get_task(task_id: str) -> dict:
    """Get task definition by ID"""

def list_tasks(enabled_only: bool = True) -> list:
    """List all tasks"""

def update_task(task_id: str, updates: dict) -> bool:
    """Update task definition"""

def enable_task(task_id: str) -> bool:
    """Enable a disabled task"""

def disable_task(task_id: str) -> bool:
    """Disable a task without deleting it"""
```

### Scheduler API

```python
# scheduler.py

class TaskScheduler:
    def __init__(self):
        """Initialize scheduler"""

    def load_tasks(self):
        """Load tasks from registry"""

    def start(self):
        """Start scheduler (non-blocking)"""

    def stop(self):
        """Stop scheduler gracefully"""

    def run_once(self):
        """Run pending tasks once (for testing)"""

    def execute_task(self, task_id: str) -> dict:
        """Execute a specific task immediately"""
```

---

## Testing Strategy

### Unit Tests (8-10 tests)

```python
# tests/test_task_registry.py

def test_register_task_success()
def test_register_task_duplicate_fails()
def test_register_task_invalid_schema_fails()
def test_unregister_task_success()
def test_get_task_exists()
def test_get_task_not_found()
def test_list_tasks_filters_enabled()
def test_update_task_success()
def test_enable_disable_task()
def test_tasks_persist_to_file()
```

```python
# tests/test_scheduler.py

def test_scheduler_loads_tasks()
def test_scheduler_executes_task_at_time()
def test_scheduler_logs_execution()
def test_scheduler_retries_failed_task()
def test_scheduler_respects_enabled_flag()
def test_execute_task_immediately()
```

### Integration Tests

```python
# tests/test_scheduler_integration.py

def test_end_to_end_daily_task()
def test_end_to_end_with_failure_and_retry()
```

---

## Error Handling

### Task Execution Failures

**Strategy:** Log error, retry based on policy, notify user

```python
try:
    result = handler.run(context)
    log_execution("success", result)
except Exception as e:
    log_execution("failure", str(e))

    if attempts < max_retries:
        schedule_retry(task_id, retry_delay)
    else:
        notify_failure(task_id, e)
```

### Scheduler Failures

**Strategy:** Graceful degradation

- If scheduler crashes, restart on next session
- Tasks don't execute during downtime (acceptable for MVP)
- Future: Persistent scheduler with systemd/supervisor

---

## Performance Considerations

### Scalability

**MVP (Sprint 2):**
- 5-10 tasks max
- In-process scheduler
- Acceptable for single user

**Future (v0.2+):**
- Persistent background scheduler
- Distributed task queue (Celery)
- Multiple concurrent tasks

### Resource Usage

**CPU:** Minimal (sleep-based scheduling)
**Memory:** <10MB for scheduler
**Disk:** ~1MB for task definitions + logs

---

## Security Considerations

### Task Handler Execution

**Risk:** Malicious task handlers
**Mitigation:**
- Only load handlers from `handlers/` directory
- No dynamic code execution from user input
- Validate handler paths

### Task Persistence

**Risk:** Unauthorized task modification
**Mitigation:**
- File permissions (user-only read/write)
- Validate task schema on load
- Audit log of task changes (future)

---

## Migration Path

### From MVP to Production

**Phase 1 (Sprint 2):** In-process scheduler
- Simple `schedule` library
- Works for single user
- Tasks run when app is running

**Phase 2 (v0.2):** Background scheduler
- Systemd service or Windows Task Scheduler
- Runs independently of main app
- More reliable

**Phase 3 (v1.0):** Distributed scheduler
- APScheduler with persistent storage
- Multiple workers
- Enterprise-grade reliability

---

## Example Usage

### Register a Daily Briefing

```python
from task_registry import register_task

briefing_task = {
    "id": "daily_briefing_9am",
    "name": "Daily Briefing",
    "schedule": {
        "type": "daily",
        "time": "09:00"
    },
    "handler": "handlers.daily_briefing.run",
    "enabled": True
}

register_task(briefing_task)
```

### Start Scheduler

```python
from scheduler import TaskScheduler

scheduler = TaskScheduler()
scheduler.load_tasks()
scheduler.start()  # Runs in background

# Scheduler now executes tasks at scheduled times
```

---

## Success Metrics

### Story 1.6 Complete When:
- [ ] All 6 acceptance criteria met
- [ ] 8-10 tests written and passing
- [ ] Example task executes successfully
- [ ] Execution logged correctly
- [ ] Documentation complete
- [ ] Code reviewed

---

## Dependencies

**Prerequisites:**
- ✅ Sprint 1 complete (memory system available)

**New Dependencies:**
- `schedule` library (add to pyproject.toml)

**Blocked By:** None

**Blocks:**
- Story 1.7 (Event Detection - uses scheduler)
- Story 1.9 (Proactive Notifications - uses scheduler)

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Schedule library unreliable | HIGH | LOW | Well-tested library, add retry logic |
| Task handlers crash | MEDIUM | MEDIUM | Error handling, retry policy |
| Performance issues | LOW | LOW | MVP supports 5-10 tasks only |

---

## Future Enhancements

**Sprint 3+:**
- Task dependencies (Task B runs after Task A)
- Task chaining (pipeline of tasks)
- Conditional execution (run if condition met)
- Task history browser (UI)
- Task analytics (success rate, duration trends)

---

_Story 1.6 Design by DEV Agent, 2025-10-16_
_Sprint 2: Building Autonomous Behaviors_
