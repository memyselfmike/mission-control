# Story 1.7 - Kickoff

**Story:** 1.7 - Event Detection System
**Story Points:** 8
**Priority:** P0 (Critical Path)
**Sprint:** Sprint 2, Day 3
**Scrum Master:** Bob
**Date:** 2025-10-16

---

## Story Overview

Build an event detection system that enables Mission Control to detect and respond to events from multiple sources (file system changes, time-based triggers, external signals).

**Why This Matters:** This story completes the autonomous behavior foundation started in Story 1.6. While 1.6 enables scheduled actions, 1.7 enables reactive behaviors - the agent can now respond to changes in its environment.

---

## Story Context

### Prerequisites ✅
- ✅ Story 1.6 complete (scheduler available for integration)
- ✅ Sprint 1 complete (memory system available)

### Builds Upon
- **Story 1.6:** Scheduled Task Execution Framework
  - Event handlers can trigger scheduled tasks
  - Events can be logged alongside task execution
  - Shared handler contract

### Enables
- **Story 1.8:** Pattern Recognition Engine (can detect patterns in events)
- **Story 1.9:** Proactive Notifications (events trigger notifications)

---

## Acceptance Criteria

### Must Have (MVP)

- [ ] **AC-1:** File system events can be detected (create, modify, delete)
- [ ] **AC-2:** Time-based events can be registered and triggered
- [ ] **AC-3:** Events can trigger actions (handlers)
- [ ] **AC-4:** Event queue prevents event flooding
- [ ] **AC-5:** All events logged for audit trail
- [ ] **AC-6:** Tests written (8-10 tests minimum)

### Should Have (Stretch)
- [ ] Event filtering (by type, path, etc.)
- [ ] Event batching (group related events)
- [ ] Event priority levels

---

## Technical Design

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│ Event Detection System                                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │ File System  │    │ Time-Based   │    │ External │  │
│  │ Watcher      │    │ Triggers     │    │ Signals  │  │
│  └──────┬───────┘    └──────┬───────┘    └────┬─────┘  │
│         │                   │                  │        │
│         └───────────────────┼──────────────────┘        │
│                             ▼                           │
│                    ┌──────────────────┐                 │
│                    │  Event Queue     │                 │
│                    │  (rate limiting) │                 │
│                    └────────┬─────────┘                 │
│                             ▼                           │
│                    ┌──────────────────┐                 │
│                    │ Event Dispatcher │                 │
│                    └────────┬─────────┘                 │
│                             ▼                           │
│                    ┌──────────────────┐                 │
│                    │ Event Handlers   │                 │
│                    │ (actions)        │                 │
│                    └──────────────────┘                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Component Design

#### 1. Event Registry (`event_registry.py`)
- Register event watchers
- Map events to handlers
- Store event configuration
- CRUD operations

#### 2. Event Queue (`event_queue.py`)
- Queue events for processing
- Rate limiting (prevent flooding)
- Priority queue support
- Thread-safe operations

#### 3. Event Watchers (`event_watchers.py`)
- **File System Watcher:** Monitor file changes using `watchdog` library
- **Time-Based Watcher:** Trigger events at specific times
- **Custom Watchers:** Extensible watcher interface

#### 4. Event Dispatcher (`event_dispatcher.py`)
- Process events from queue
- Route to appropriate handlers
- Log event execution
- Error handling

---

## Data Models

### Event Definition

```json
{
  "id": "file_changed_briefings",
  "name": "Briefing File Changed",
  "type": "file_system",
  "source": {
    "path": "data/briefings",
    "events": ["created", "modified"],
    "patterns": ["*.md"]
  },
  "handler": "handlers.briefing_updated.run",
  "enabled": true,
  "rate_limit": {
    "max_per_minute": 10,
    "batch_window_seconds": 30
  },
  "metadata": {
    "created": "2025-10-16T...",
    "created_by": "system"
  }
}
```

### Event Instance (Queue Entry)

```json
{
  "event_id": "file_changed_briefings_1760615000",
  "definition_id": "file_changed_briefings",
  "timestamp": "2025-10-16T13:00:00Z",
  "type": "file_system",
  "data": {
    "path": "data/briefings/briefing_2025-10-16.md",
    "event_type": "modified"
  },
  "status": "pending",
  "priority": 5
}
```

### Event Log Entry

```json
{
  "event_id": "file_changed_briefings_1760615000",
  "definition_id": "file_changed_briefings",
  "timestamp": "2025-10-16T13:00:00Z",
  "handler": "handlers.briefing_updated.run",
  "status": "success",
  "duration_ms": 45,
  "output": "Briefing processed",
  "error": null
}
```

---

## Implementation Plan

### Phase 1: Event Registry (4 hours)
1. ✅ Design event data model
2. ⏳ Write event registry tests (TDD)
3. ⏳ Implement event registry
4. ⏳ Validate with tests

### Phase 2: Event Queue (2 hours)
5. ⏳ Write event queue tests (TDD)
6. ⏳ Implement event queue with rate limiting
7. ⏳ Add priority support
8. ⏳ Validate with tests

### Phase 3: Event Watchers (3 hours)
9. ⏳ Install `watchdog` library
10. ⏳ Write file system watcher tests
11. ⏳ Implement file system watcher
12. ⏳ Write time-based watcher tests
13. ⏳ Implement time-based watcher
14. ⏳ Validate with tests

### Phase 4: Event Dispatcher (2 hours)
15. ⏳ Write dispatcher tests (TDD)
16. ⏳ Implement event dispatcher
17. ⏳ Add event logging
18. ⏳ Validate with tests

### Phase 5: Integration & Testing (2 hours)
19. ⏳ Create example event handlers
20. ⏳ Write integration tests
21. ⏳ Test end-to-end workflows
22. ⏳ Create demo scenarios

**Total Estimated Time:** ~13 hours (fits in 1-2 days with TDD approach)

---

## Technical Decisions

### Event Detection Library

**Decision:** Use `watchdog` for file system events

**Rationale:**
- ✅ Cross-platform (Windows, Linux, macOS)
- ✅ Well-maintained and popular
- ✅ Supports multiple file system event types
- ✅ Efficient (uses native OS APIs)

**Alternatives Considered:**
- `os.stat()` polling: Too slow, CPU intensive
- Custom inotify wrapper: Linux-only

### Event Queue Implementation

**Decision:** Use Python `queue.PriorityQueue`

**Rationale:**
- ✅ Thread-safe out of the box
- ✅ Priority support built-in
- ✅ Standard library (no external dependency)
- ✅ Simple and reliable

**Future:** Could upgrade to Redis queue for distributed systems

### Rate Limiting Strategy

**Decision:** Token bucket algorithm

**Rationale:**
- ✅ Simple to implement
- ✅ Allows bursts while limiting average rate
- ✅ Per-event-type limiting

---

## Event Types Supported

### 1. File System Events ✅

**Supported Events:**
- `created` - New file created
- `modified` - File contents changed
- `deleted` - File removed
- `moved` - File renamed/moved

**Use Cases:**
- Detect new briefings
- Monitor log files
- Watch configuration changes

### 2. Time-Based Events ✅

**Supported Triggers:**
- Specific time (e.g., 9:00 AM)
- Interval (e.g., every 30 minutes)
- Day of week (e.g., every Monday)

**Use Cases:**
- Daily reminders
- Weekly reports
- Periodic health checks

### 3. External Events (Future)

**Potential Sources:**
- Webhooks
- API callbacks
- Message queues
- System signals

---

## Integration with Story 1.6

### Shared Components

1. **Handler System**
   - Events use same handler contract as scheduled tasks
   - Handlers receive context dict
   - Return status, output, error

2. **Logging System**
   - Events logged to same JSONL format
   - Unified audit trail

3. **Configuration**
   - Events stored in `data/events/` directory
   - Similar JSON structure to tasks

### New Capabilities

- Events can trigger scheduled tasks
- Tasks can emit events (e.g., on completion)
- Combined event + schedule triggers

---

## Testing Strategy

### Unit Tests (10-12 tests)

```python
# test_event_registry.py
def test_register_event()
def test_get_event()
def test_list_events()
def test_update_event()
def test_delete_event()
def test_validate_event_schema()

# test_event_queue.py
def test_enqueue_event()
def test_dequeue_event()
def test_priority_ordering()
def test_rate_limiting()

# test_event_watchers.py
def test_file_watcher_detects_create()
def test_file_watcher_detects_modify()
def test_time_watcher_triggers()

# test_event_dispatcher.py
def test_dispatch_event_to_handler()
def test_dispatch_logs_execution()
def test_dispatch_handles_errors()
```

### Integration Tests (3-5 tests)

```python
# test_events_integration.py
def test_end_to_end_file_event()
def test_end_to_end_time_event()
def test_event_triggers_scheduled_task()
def test_multiple_events_processed()
```

**Target:** 15+ tests (exceeding minimum of 8-10)

---

## Example Use Cases

### Use Case 1: Auto-Process New Briefings

**Scenario:** When a new briefing is created, automatically update mission control dashboard

**Event Definition:**
```python
{
  "id": "new_briefing_created",
  "type": "file_system",
  "source": {
    "path": "data/briefings",
    "events": ["created"],
    "patterns": ["briefing_*.md"]
  },
  "handler": "handlers.update_dashboard.run"
}
```

### Use Case 2: Configuration Change Detection

**Scenario:** Detect when user preferences change and notify Alex

**Event Definition:**
```python
{
  "id": "preferences_changed",
  "type": "file_system",
  "source": {
    "path": "data/user_preferences_v2.json",
    "events": ["modified"]
  },
  "handler": "handlers.notify_preference_change.run"
}
```

### Use Case 3: Periodic Health Check

**Scenario:** Check system health every 30 minutes

**Event Definition:**
```python
{
  "id": "health_check_periodic",
  "type": "time_based",
  "source": {
    "interval": "30m"
  },
  "handler": "handlers.health_check.run"
}
```

---

## Success Metrics

### Story Complete When:
- [ ] All 6 acceptance criteria met
- [ ] 15+ tests written and passing
- [ ] File system events detected and processed
- [ ] Time-based events triggered correctly
- [ ] Event handlers execute successfully
- [ ] Rate limiting prevents flooding
- [ ] All events logged
- [ ] Integration with Story 1.6 working
- [ ] Documentation complete

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| File watcher OS-specific issues | MEDIUM | MEDIUM | Use cross-platform `watchdog` library |
| Event flooding crashes system | HIGH | LOW | Rate limiting + queue |
| Handler failures block queue | MEDIUM | LOW | Error handling + retry logic |
| Performance impact | LOW | LOW | Efficient watchers, async processing |

---

## Dependencies

### External Libraries Needed
- **`watchdog`** - File system event monitoring
- **`queue`** - Built-in (no install needed)

### Internal Dependencies
- ✅ Story 1.6 (scheduler & handlers)
- ✅ Sprint 1 (memory system)

---

## Definition of Done

### Story Level
- [ ] Code implemented (all 4 components)
- [ ] Tests written (15+ tests)
- [ ] Tests passing (100%)
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Integration with Story 1.6 validated
- [ ] Demo prepared

---

## Day 3 Plan

### Morning Session (4 hours)
1. **Event Registry** (Phase 1)
   - Design data model
   - Write tests (TDD)
   - Implement event registration
   - Validate with tests

2. **Event Queue** (Phase 2)
   - Write tests
   - Implement queue with rate limiting
   - Validate with tests

### Afternoon Session (4 hours)
3. **Event Watchers** (Phase 3)
   - Install watchdog
   - Write file system watcher tests
   - Implement file system watcher
   - Validate with tests

**End of Day 3 Target:** Phases 1-3 complete (~60% of story)

---

## Day 4 Plan (if needed)

### Morning Session (2 hours)
4. **Event Dispatcher** (Phase 4)
   - Write dispatcher tests
   - Implement dispatcher
   - Add event logging
   - Validate with tests

### Afternoon Session (2 hours)
5. **Integration & Testing** (Phase 5)
   - Create example handlers
   - Write integration tests
   - Test end-to-end workflows
   - Create demo scenarios

**End of Day 4 Target:** Story 1.7 complete (8 points)

---

## Sprint 2 Progress Forecast

| Day | Story | Points | Cumulative | Status |
|-----|-------|--------|------------|--------|
| 1-2 | 1.6 | 8 | 8 | ✅ Complete |
| 3 | 1.7 (Phases 1-3) | 4.8 | 12.8 | ⏳ Starting |
| 3-4 | 1.7 (Phases 4-5) | 3.2 | 16 | ⏳ Planned |
| 4-5 | 1.8 | 8 | 24 | ⏳ Planned |
| 5 | 1.9 | 5 | 29 | ⏳ Planned |

**Status:** ✅ On track for 29-point sprint completion

---

## Team Commitments

### DEV Agent Commits To:
- ✅ TDD approach (write tests first)
- ✅ Daily progress summary (end of Day 3)
- ✅ Complete Phases 1-3 today (60% of story)
- ✅ Maintain high code quality

### Scrum Master (Bob) Commits To:
- ✅ Track Story 1.7 progress
- ✅ Remove blockers
- ✅ Update sprint board
- ✅ Mid-sprint check-in tomorrow

### Product Owner (Mike) Commits To:
- ✅ Available for questions
- ✅ Review progress
- ✅ Provide feedback on approach

---

## Questions & Clarifications

### Pre-Implementation Questions

1. **Event Storage:** Should events persist across sessions?
   - **Assumption:** Yes, store in `data/events/event_definitions.json`

2. **Event History:** How long should we keep event logs?
   - **Assumption:** Keep in JSONL, no auto-deletion (user manages)

3. **Rate Limits:** Default rate limit values?
   - **Assumption:** 10 events/minute per event type, 30s batch window

4. **File Watcher Scope:** Watch entire directories or specific files?
   - **Assumption:** Support both (configurable in event definition)

---

## Next Steps

### Immediate Actions (Start Now)
1. ✅ Story 1.7 kickoff complete
2. ⏳ Review technical design
3. ⏳ Install `watchdog` library
4. ⏳ Create event registry test file
5. ⏳ Begin Phase 1 (Event Registry)

**Let's build Story 1.7!** 🚀

---

_Story 1.7 Kickoff by Bob (Scrum Master), 2025-10-16_
_Sprint 2, Day 3 - Let's make Mission Control reactive!_
