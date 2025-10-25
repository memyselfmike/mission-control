# Event System Migration Guide

**Story:** 7.1 - Refactor Event System
**Created:** 2025-10-25
**Status:** Phase 1 - Development Complete
**Pattern:** Strangler Fig Migration

---

## Overview

This guide explains how to migrate from the legacy event system (`src/events/`) to the new Hexagonal Architecture event system with domain events, event handlers, and the repository pattern.

---

## Architecture Comparison

### Legacy System (src/events/)

- **Design:** Procedural code with global singleton dispatcher
- **Events:** Represented as `Dict[str, Any]`
- **Storage:** Direct JSON file I/O throughout code
- **Handlers:** Example handlers hardcoded in module
- **Testing:** 72 tests passing

**Files:**
- `src/events/event_registry.py`
- `src/events/event_queue.py`
- `src/events/event_dispatcher.py`
- `src/events/event_watchers.py`
- `src/events/example_handlers.py`

### New System (Hexagonal Architecture)

- **Design:** Clean Architecture with layer separation
- **Events:** Strongly-typed domain event classes (TaskCreated, TaskCompleted, etc.)
- **Storage:** Repository pattern via IEventRepository interface
- **Handlers:** Dependency-injected event handlers implementing IEventHandler
- **Testing:** 25+ new tests + all 72 legacy tests still pass

**Structure:**
```
src/
├── domain/
│   ├── events/                    # Domain events (immutable)
│   │   ├── base_event.py
│   │   └── task_events.py
│   └── repositories/
│       └── event_repository.py    # IEventRepository interface
│
├── application/
│   ├── event_handlers/            # Event handlers (application logic)
│   │   ├── base_handler.py
│   │   └── task_event_handlers.py
│   └── services/
│       └── event_dispatcher_service.py
│
└── infrastructure/
    └── persistence/
        └── repositories/
            └── json_event_repository.py  # JSONL implementation
```

---

## Feature Flag Control

### Default Behavior (Safe)

```bash
# Default: Legacy event system active
USE_NEW_EVENT_SYSTEM=false  # This is the default
```

All existing code continues working with zero changes.

### Enable New Event System

```bash
# Test new event system
export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true

# Or set in .env file
echo "MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true" >> .env
```

### Check Current Mode

The configuration is logged at startup:

```
[config] Configuration loaded:
[config]   USE_NEW_EVENT_SYSTEM = False
[config]   Event system mode: legacy_events
[config]   Source: Default (False)
```

---

## Migration Phases

### Phase 1: Development (Complete) ✅

**Goal:** Build new system alongside old, zero modifications to legacy code

**Status:** Complete (Story 7.1)

**What was done:**
- Created domain events (TaskCreated, TaskCompleted, TaskDeleted, TaskUpdated)
- Implemented event handlers (TaskCreatedHandler, TaskCompletedHandler, etc.)
- Built EventDispatcherService with repository pattern
- Implemented JsonEventRepository with JSONL storage
- Added USE_NEW_EVENT_SYSTEM feature flag
- Wrote 25+ tests
- Verified all 72 legacy tests still pass

**Result:** New system exists but is not active by default

---

### Phase 2: Testing (Next)

**Goal:** Validate new system works correctly in test environments

**Duration:** 1-2 weeks

**Steps:**

1. **Unit Testing:**
   ```bash
   # Run new event system tests
   pytest tests/domain/events/
   pytest tests/application/event_handlers/
   pytest tests/infrastructure/persistence/test_json_event_repository.py
   ```

2. **Integration Testing:**
   ```bash
   # Enable new system in test environment
   export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true

   # Run full test suite
   pytest

   # Verify all tests still pass
   ```

3. **Performance Testing:**
   - Measure event dispatch time (target: <10ms)
   - Compare with legacy system performance
   - Ensure no degradation

4. **Manual Testing:**
   - Create tasks and verify events are fired
   - Complete tasks and check TaskCompleted events
   - Delete tasks and verify TaskDeleted events
   - Update tasks and verify TaskUpdated events
   - Inspect event log files in `data/events/events-YYYY-MM-DD.jsonl`

**Acceptance Criteria:**
- All tests pass with new system
- Performance meets or exceeds legacy system
- Event logs are created and queryable
- Handlers execute correctly

---

### Phase 3: Gradual Rollout (Future)

**Goal:** Switch to new system as default in production

**Duration:** 1-2 weeks with monitoring

**Steps:**

1. **Change Default:**
   ```python
   # In src/config.py
   # Change default from "false" to "true"
   _USE_NEW_EVENT_ENV = os.getenv("MISSION_CONTROL_USE_NEW_EVENT_SYSTEM", "true").lower()
   ```

2. **Monitor Production:**
   - Watch for errors in event handling
   - Monitor event file growth
   - Check handler execution logs
   - Verify analytics are updated

3. **Rollback Plan:**
   If issues detected:
   ```bash
   # Immediate rollback
   export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=false
   # Restart application
   ```

   Or change default back to "false" and redeploy.

4. **Validation Period:**
   - Run both systems in parallel (if possible)
   - Compare event logs
   - Verify data consistency

**Acceptance Criteria:**
- Zero critical errors for 1 week
- All events captured and processed
- Performance within acceptable range
- User workflows unaffected

---

### Phase 4: Deprecation (Future)

**Goal:** Remove legacy event system code

**Duration:** 1 day

**Prerequisites:**
- Phase 3 complete with 2+ weeks of stability
- No incidents related to event system
- All stakeholders approve removal

**Steps:**

1. **Remove Legacy Code:**
   ```bash
   # Delete old event system
   rm -rf src/events/
   ```

2. **Remove Feature Flag:**
   - Remove USE_NEW_EVENT_SYSTEM from config.py
   - Remove conditional logic
   - Clean up dual-path routing

3. **Update Tests:**
   - Remove or archive old event tests
   - Keep new tests as primary

4. **Update Documentation:**
   - Mark this migration guide as complete
   - Update architecture docs
   - Remove references to legacy system

**Acceptance Criteria:**
- Code simplified (no more conditional routing)
- All tests pass
- Documentation updated

---

## Code Examples

### Creating and Dispatching Events

**Old Way (Legacy):**
```python
# Direct access to global dispatcher
from events.event_dispatcher import get_global_dispatcher

dispatcher = get_global_dispatcher()
event = {
    "type": "TaskCreated",
    "task_id": "T123",
    "title": "My Task",
    "timestamp": "2025-10-25T10:00:00"
}
dispatcher.queue_event(event)
```

**New Way (Hexagonal):**
```python
# Create strongly-typed domain event
from src.domain.events import TaskCreated
from src.domain.value_objects import Priority, Status

event = TaskCreated(
    task_id="T123",
    title="My Task",
    priority=Priority.P1,
    status=Status.NOT_STARTED
)

# Dispatch via service (injected)
from src.application.services import EventDispatcherService
from src.infrastructure.persistence.repositories import JsonEventRepository
from pathlib import Path

# Setup (typically done at app startup)
event_repo = JsonEventRepository(storage_dir=Path("data/events"))
handlers = {
    "TaskCreated": TaskCreatedHandler(event_repo),
}
dispatcher = EventDispatcherService(event_repo, handlers)

# Dispatch
success = dispatcher.dispatch(event)
```

### Querying Event History

**Old Way:**
```python
# Manual file reading
import json
with open("data/events.json", "r") as f:
    all_events = json.load(f)

task_events = [e for e in all_events if e.get("task_id") == "T123"]
```

**New Way:**
```python
# Via repository interface
event_repo = JsonEventRepository(storage_dir=Path("data/events"))

# Get recent events
recent = event_repo.get_recent_events(limit=50)

# Find by type
task_created_events = event_repo.find_by_type("TaskCreated", limit=100)

# Find by date range
from datetime import datetime, timedelta
today = datetime.now()
yesterday = today - timedelta(days=1)
todays_events = event_repo.find_by_date_range(yesterday, today)
```

---

## Dual-Path Routing Pattern

During migration, code that fires events uses dual-path routing:

```python
from src.config import USE_NEW_EVENT_SYSTEM

def on_task_created(task_id: str, title: str):
    """Example of dual-path event routing"""

    if USE_NEW_EVENT_SYSTEM:
        # New system path
        from src.domain.events import TaskCreated
        from src.application.services import get_event_dispatcher

        event = TaskCreated(task_id=task_id, title=title, ...)
        dispatcher = get_event_dispatcher()  # Get from DI container
        dispatcher.dispatch(event)

    else:
        # Legacy system path (unchanged)
        from events.event_dispatcher import get_global_dispatcher

        dispatcher = get_global_dispatcher()
        dispatcher.queue_event({
            "type": "TaskCreated",
            "task_id": task_id,
            "title": title,
            ...
        })
```

---

## Testing Strategy

### Regression Testing

```bash
# Ensure legacy tests still pass
pytest tests/test_event_*.py

# Expected: 72 tests passing (100%)
```

### New System Testing

```bash
# Test domain events
pytest tests/domain/events/test_task_events.py

# Test event handlers
pytest tests/application/event_handlers/test_task_event_handlers.py

# Test event dispatcher
pytest tests/application/services/test_event_dispatcher_service.py

# Test repository
pytest tests/infrastructure/persistence/test_json_event_repository.py

# Integration tests
pytest tests/integration/test_event_system_integration.py
```

### Feature Flag Testing

```bash
# Test with legacy system
export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=false
pytest

# Test with new system
export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true
pytest

# Both should pass all tests
```

---

## Troubleshooting

### New System Not Active

**Symptom:** Events not appearing in `data/events/events-*.jsonl`

**Solution:**
```bash
# Check configuration
python -c "from src.config import USE_NEW_EVENT_SYSTEM; print(f'New system active: {USE_NEW_EVENT_SYSTEM}')"

# If False, set environment variable
export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true
```

### Event Files Growing Too Large

**Symptom:** `events-YYYY-MM-DD.jsonl` files > 100MB

**Solution:** Daily rotation is automatic. Old files can be archived:
```bash
# Archive old event files
mkdir -p data/events/archive
mv data/events/events-2025-10-*.jsonl data/events/archive/
```

### Performance Issues

**Symptom:** Event dispatch taking > 10ms

**Diagnosis:**
```python
# Enable performance logging (already in EventDispatcherService)
# Check logs for:
# [EventDispatcherService] PERFORMANCE WARNING: Dispatch took XXms
```

**Solutions:**
- Check disk I/O performance
- Consider batch event writes
- Optimize handler logic
- Add caching if needed

### Handler Not Executing

**Symptom:** Events persisted but handlers not running

**Diagnosis:**
```python
# Check handler registration
dispatcher = get_event_dispatcher()
print(f"Registered handlers: {list(dispatcher.handlers.keys())}")
```

**Solution:**
```python
# Ensure handlers are registered
from src.application.event_handlers import TaskCreatedHandler

dispatcher.register_handler("TaskCreated", TaskCreatedHandler())
```

---

## Rollback Procedure

If critical issues are discovered:

### Immediate Rollback (0 downtime)

```bash
# 1. Set environment variable
export MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=false

# 2. Restart application
systemctl restart mission-control  # or your restart command
```

### Code Rollback (if env var not working)

```python
# In src/config.py, change default:
_USE_NEW_EVENT_ENV = os.getenv("MISSION_CONTROL_USE_NEW_EVENT_SYSTEM", "false").lower()
# Ensure default is "false" ----------------^^^^^^^^

# Commit and deploy
```

### Verify Rollback

```bash
# Check logs for:
# [config] Event system mode: legacy_events

# Verify legacy event system active
tail -f logs/application.log | grep "EventDispatcher"
```

---

## Success Metrics

### Phase 2 (Testing)

- ✅ All unit tests passing (25+ new tests)
- ✅ All integration tests passing
- ✅ All regression tests passing (72 legacy tests)
- ✅ Event dispatch time < 10ms (average)
- ✅ Zero critical errors

### Phase 3 (Production)

- ✅ 1 week of production use without incidents
- ✅ Event files created daily
- ✅ All handlers executing successfully
- ✅ Performance within SLA
- ✅ No user-reported issues

### Phase 4 (Cleanup)

- ✅ Legacy code removed
- ✅ Feature flag removed
- ✅ Code simplified
- ✅ Documentation updated

---

## Contact & Support

**Questions?** Contact the development team or Product Owner (Mike).

**Issues?** File a bug report with:
- USE_NEW_EVENT_SYSTEM value
- Error logs
- Event samples (if applicable)
- Steps to reproduce

---

## Appendix: Event File Format

### JSONL Format

Each line is a complete JSON object representing one event:

```json
{"event_id": "e1", "event_type": "TaskCreated", "timestamp": "2025-10-25T10:00:00", "aggregate_id": "T123", "task_id": "T123", "title": "My Task", "priority": "P1", "status": "NOT_STARTED", "metadata": {}}
{"event_id": "e2", "event_type": "TaskCompleted", "timestamp": "2025-10-25T15:30:00", "aggregate_id": "T123", "task_id": "T123", "completed_date": "2025-10-25T15:30:00", "completion_notes": "Done!", "metadata": {}}
```

### Daily Rotation

Files are named by date:
- `events-2025-10-25.jsonl` - October 25, 2025
- `events-2025-10-26.jsonl` - October 26, 2025

Each day gets a new file automatically.

---

**This migration is complete when the legacy system is removed and only the new Hexagonal Architecture event system remains.**

**Current Status:** Phase 1 Complete ✅ (Story 7.1 delivered)
