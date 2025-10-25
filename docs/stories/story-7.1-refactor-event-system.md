# Story 7.1: Refactor Event System

**Epic:** EPIC-5R Phase 5 - Events & Coordination
**Story Points:** 8
**Priority:** P0 (Critical - Blocks Phase 5)
**Status:** Ready for Review
**Created:** 2025-10-25
**Assigned To:** DEV Agent

---

## Story Description

Refactor existing `src/events/` module to use Hexagonal/Clean Architecture with proper domain events, event handlers in application layer, and event dispatcher using repository pattern. This story implements the Strangler Fig pattern to gradually migrate from procedural event handling to clean OOP-based event system.

---

## Business Value

- **Clean Architecture:** Events follow domain-driven design with proper layer boundaries
- **Maintainability:** Event system becomes easier to extend and test
- **Type Safety:** Domain events replace Dict[str, Any] with strongly-typed classes
- **Testability:** Repository pattern enables easy mocking and testing
- **Future-Ready:** Clean foundation for self-coding AI agents (CLAUDE.md compliance)

---

## Current State

**Existing Implementation (Story 1.7):**
- Event system in `src/events/` (event_registry.py, event_queue.py, event_dispatcher.py, event_watchers.py, example_handlers.py)
- Procedural code with direct file I/O
- Events represented as `Dict[str, Any]`
- Global singleton pattern for dispatcher
- 72 tests passing in `tests/test_event_*.py`

**Issues:**
- No domain model for events (just dicts)
- Business logic mixed with infrastructure
- Tight coupling to JSON file storage
- Hard to test (global state, file I/O)
- Violates Hexagonal Architecture principles

---

## Desired State

**New Implementation:**
- Domain events as classes: `TaskCreated`, `TaskCompleted`, `TaskDeleted`, `TaskUpdated`
- Event handlers in `src/application/event_handlers/`
- `EventDispatcher` uses `IEventRepository` interface
- Repository implementation in `src/infrastructure/persistence/repositories/json_event_repository.py`
- Feature flag system: `USE_NEW_EVENT_SYSTEM` in `src/config.py` (defaults to `False`)
- Strangler Fig pattern: Zero modifications to existing `src/events/*.py` files
- 25+ tests in `tests/application/events/test_event_system.py`
- Zero regressions: All 72 existing tests still pass

---

## Acceptance Criteria

### AC1: Domain Events Created
**Given** the need for strongly-typed event models
**When** domain events are implemented
**Then**:
- [ ] `src/domain/events/__init__.py` created
- [ ] `src/domain/events/base_event.py` created with `DomainEvent` base class
- [ ] `src/domain/events/task_events.py` created with:
  - `TaskCreated(task_id, title, priority, status, timestamp, metadata)`
  - `TaskCompleted(task_id, completed_date, completion_notes, timestamp, metadata)`
  - `TaskDeleted(task_id, reason, timestamp, metadata)`
  - `TaskUpdated(task_id, changes, old_values, new_values, timestamp, metadata)`
- [ ] All events inherit from `DomainEvent`
- [ ] All events immutable (frozen dataclasses)
- [ ] All events have type hints
- [ ] All events validate themselves in `__post_init__`

### AC2: Event Handler Interfaces
**Given** the need for event processing
**When** event handlers are implemented
**Then**:
- [ ] `src/application/event_handlers/__init__.py` created
- [ ] `src/application/event_handlers/base_handler.py` created with `IEventHandler` interface
- [ ] `src/application/event_handlers/task_event_handlers.py` created with:
  - `TaskCreatedHandler` (logs creation, updates analytics)
  - `TaskCompletedHandler` (logs completion, updates stats)
  - `TaskDeletedHandler` (logs deletion, cleans up references)
  - `TaskUpdatedHandler` (logs changes, tracks history)
- [ ] All handlers implement `IEventHandler.handle(event: DomainEvent) -> bool`
- [ ] All handlers use dependency injection (repositories passed in constructor)

### AC3: Event Dispatcher Refactored
**Given** the need for clean event routing
**When** EventDispatcher is refactored
**Then**:
- [ ] `src/application/services/event_dispatcher_service.py` created
- [ ] Uses `IEventRepository` for persistence (not direct file I/O)
- [ ] Handler registration via constructor injection
- [ ] `dispatch(event: DomainEvent) -> bool` method
- [ ] `dispatch_async(event: DomainEvent) -> Future[bool]` method
- [ ] Event history tracked in repository
- [ ] Performance logging (dispatch time < 10ms target)

### AC4: Repository Implementation
**Given** the need for event persistence
**When** event repository is implemented
**Then**:
- [ ] `src/domain/repositories/event_repository.py` created with `IEventRepository` interface
- [ ] Interface defines: `save_event()`, `find_by_id()`, `find_by_type()`, `find_by_date_range()`, `get_recent_events()`
- [ ] `src/infrastructure/persistence/repositories/json_event_repository.py` implements `IEventRepository`
- [ ] Uses `JsonStorage` utility from Story 5.4
- [ ] JSONL format for event log
- [ ] Daily rotation (one file per day)
- [ ] Graceful error handling with logging

### AC5: Feature Flag System
**Given** the need for gradual migration
**When** feature flag is implemented
**Then**:
- [ ] `src/config.py` updated with `USE_NEW_EVENT_SYSTEM = False` (default)
- [ ] Dual-path routing in event entry points:
  ```python
  if USE_NEW_EVENT_SYSTEM:
      # New clean architecture path
      service = EventDispatcherService(event_repo, handlers)
      service.dispatch(task_created_event)
  else:
      # Old procedural path (unchanged)
      from events.event_dispatcher import get_global_dispatcher
      dispatcher = get_global_dispatcher()
      dispatcher.process_next_event()
  ```
- [ ] Feature flag can be overridden via environment variable `MISSION_CONTROL_USE_NEW_EVENT_SYSTEM=true`
- [ ] Logging indicates which path is active

### AC6: Strangler Fig Pattern (Zero Breaking Changes)
**Given** the need for backward compatibility
**When** refactoring is complete
**Then**:
- [ ] Zero modifications to existing `src/events/*.py` files
- [ ] Old event system continues to work (when flag = False)
- [ ] New event system works independently (when flag = True)
- [ ] Can switch between implementations at runtime
- [ ] Migration guide created in `docs/migration/event-system-migration.md`
- [ ] All 72 existing tests still pass (zero regressions)

### AC7: Comprehensive Tests
**Given** the need for quality assurance
**When** tests are written
**Then**:
- [ ] 25+ tests in `tests/application/events/test_event_system.py`
- [ ] Domain event tests: `tests/domain/events/test_task_events.py` (10+ tests)
- [ ] Handler tests: `tests/application/event_handlers/test_task_event_handlers.py` (10+ tests)
- [ ] Repository tests: `tests/infrastructure/persistence/test_json_event_repository.py` (5+ tests)
- [ ] Integration tests: `tests/integration/test_event_system_integration.py` (5+ tests)
- [ ] All tests pass (100%)
- [ ] All 72 existing event tests still pass (zero regressions)
- [ ] Test coverage ≥ 90% for new code

---

## Technical Implementation Plan

### Phase 1: Domain Layer (Domain Events)
1. Create `src/domain/events/__init__.py`
2. Create `src/domain/events/base_event.py`:
   - `DomainEvent` base class (frozen dataclass)
   - Fields: `event_id`, `event_type`, `timestamp`, `aggregate_id`, `metadata`
   - Method: `to_dict()` for serialization
3. Create `src/domain/events/task_events.py`:
   - `TaskCreated`: task_id, title, priority, status
   - `TaskCompleted`: task_id, completed_date, notes
   - `TaskDeleted`: task_id, reason
   - `TaskUpdated`: task_id, changes (dict), old_values, new_values
4. Write tests: `tests/domain/events/test_task_events.py`

### Phase 2: Application Layer (Event Handlers)
1. Create `src/application/event_handlers/__init__.py`
2. Create `src/application/event_handlers/base_handler.py`:
   - `IEventHandler` interface (ABC)
   - Method: `handle(event: DomainEvent) -> bool`
3. Create `src/application/event_handlers/task_event_handlers.py`:
   - `TaskCreatedHandler`: Logs creation, updates analytics
   - `TaskCompletedHandler`: Logs completion, updates stats
   - `TaskDeletedHandler`: Logs deletion, cleanup
   - `TaskUpdatedHandler`: Logs changes, tracks history
4. Write tests: `tests/application/event_handlers/test_task_event_handlers.py`

### Phase 3: Application Service (Event Dispatcher)
1. Create `src/application/services/event_dispatcher_service.py`:
   - Constructor: `__init__(event_repo: IEventRepository, handlers: Dict[str, IEventHandler])`
   - Method: `dispatch(event: DomainEvent) -> bool`
   - Method: `dispatch_async(event: DomainEvent) -> Future[bool]`
   - Method: `get_event_history(limit: int = 100) -> List[DomainEvent]`
2. Entry/exit logging for all methods
3. Performance tracking (dispatch time)
4. Write tests: `tests/application/services/test_event_dispatcher_service.py`

### Phase 4: Infrastructure Layer (Repository)
1. Create `src/domain/repositories/event_repository.py`:
   - `IEventRepository` interface (ABC)
   - Methods: `save_event()`, `find_by_id()`, `find_by_type()`, `find_by_date_range()`, `get_recent_events()`
2. Create `src/infrastructure/persistence/repositories/json_event_repository.py`:
   - Implements `IEventRepository`
   - JSONL storage format
   - Daily file rotation
   - Use `JsonStorage` utility
3. Write tests: `tests/infrastructure/persistence/test_json_event_repository.py`

### Phase 5: Feature Flag & Integration
1. Update `src/config.py`:
   - Add `USE_NEW_EVENT_SYSTEM = False`
   - Add `get_event_system_mode()` helper
2. Create dual-path routing in key entry points (identify during implementation)
3. Write integration tests: `tests/integration/test_event_system_integration.py`
4. Create migration guide: `docs/migration/event-system-migration.md`

### Phase 6: Testing & Validation
1. Run all 72 existing event tests → Must pass
2. Run 25+ new tests → Must pass
3. Performance validation: Dispatch time < 10ms
4. Manual validation: Switch flag on/off, verify both paths work
5. Regression testing: Full test suite (280+ tests)

---

## Dependencies

### Upstream Dependencies (Must be complete)
- ✅ Story 5.1: Domain Value Objects (provides Priority, Status enums)
- ✅ Story 5.2: Task Entity (provides Task domain model)
- ✅ Story 5.3: Repository Interfaces (provides IRepository pattern)
- ✅ Story 5.4: JSON Storage Utility (provides JsonStorage for repositories)
- ✅ Story 6.5: CLI Entry Point (provides feature flag pattern example)

### Downstream Dependencies (Blocked by this story)
- ⏳ Story 7.2: Refactor Notification System (depends on domain events)
- ⏳ Story 7.3: Refactor Coordination (depends on event system architecture)

---

## Constraints & Considerations

### Technical Constraints
1. **Backward Compatibility:** Old event system must continue to work
2. **Performance:** No degradation from current baseline (<10ms dispatch)
3. **Zero Regressions:** All 72 existing tests must still pass
4. **Strangler Fig:** No modifications to existing `src/events/*.py` files

### Architecture Constraints
1. **Hexagonal Architecture:** Strict layer boundaries (domain → application → infrastructure)
2. **SOLID Principles:** Especially SRP, DIP, ISP
3. **Repository Pattern:** All persistence via repositories
4. **Type Safety:** Full type hints, no Dict[str, Any] for domain models

### Testing Constraints
1. **Coverage:** ≥ 90% for new code
2. **Test Count:** ≥ 25 new tests
3. **Integration Tests:** ≥ 5 tests covering full event flow
4. **Performance Tests:** Verify <10ms dispatch time

---

## Testing Strategy

### Unit Tests (Domain Layer)
- **tests/domain/events/test_task_events.py** (10+ tests)
  - Test event creation with valid data
  - Test event immutability (cannot modify after creation)
  - Test event validation (invalid data raises errors)
  - Test event serialization (to_dict)

### Unit Tests (Application Layer)
- **tests/application/event_handlers/test_task_event_handlers.py** (10+ tests)
  - Test each handler's handle() method
  - Test handler logging output (capsys)
  - Test handler with mock repositories
  - Test handler error handling

- **tests/application/services/test_event_dispatcher_service.py** (5+ tests)
  - Test dispatch with registered handlers
  - Test dispatch with no handler (graceful handling)
  - Test dispatch_async (concurrent handling)
  - Test event history retrieval
  - Test performance logging

### Integration Tests (Infrastructure Layer)
- **tests/infrastructure/persistence/test_json_event_repository.py** (5+ tests)
  - Test save_event (creates JSONL file)
  - Test find_by_id (retrieves event)
  - Test find_by_type (filters by event type)
  - Test find_by_date_range (date filtering)
  - Test get_recent_events (ordering and limiting)

### Integration Tests (Full Stack)
- **tests/integration/test_event_system_integration.py** (5+ tests)
  - Test end-to-end event flow (create event → dispatch → handle → persist)
  - Test feature flag switching (old vs new implementation)
  - Test concurrent event handling
  - Test event history across sessions
  - Test performance (dispatch time < 10ms)

### Regression Tests
- **All existing tests** (72 tests in tests/test_event_*.py)
  - Must all still pass with flag = False
  - Zero modifications to test files

---

## Definition of Done

- [ ] All 7 acceptance criteria met
- [ ] 25+ new tests passing (100%)
- [ ] All 72 existing event tests still passing (zero regressions)
- [ ] Code follows CLAUDE.md engineering standards
- [ ] All functions have type hints
- [ ] All operations log to stdout (entry/exit/errors)
- [ ] Performance validated: Dispatch time < 10ms
- [ ] Feature flag system working (can switch between old/new)
- [ ] Strangler Fig pattern confirmed (no changes to src/events/*.py)
- [ ] Migration guide created
- [ ] Story committed to git: `Story 7.1: Refactor Event System - Implementation Complete`
- [ ] Code review completed (or self-review if solo)

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Performance degradation | Low | High | Performance tests, profiling, optimization |
| Breaking existing code | Medium | High | Feature flag, Strangler Fig, comprehensive testing |
| Complexity creep | Medium | Medium | Follow SOLID, limit scope to AC7 |
| Repository pattern overhead | Low | Low | Use lightweight JsonStorage, optimize file I/O |

---

## Notes

### Architecture Decisions
- Using frozen dataclasses for immutable domain events
- Event handlers are stateless services with dependency injection
- Repository interface enables future migration to database
- JSONL format preserves append-only event log (good for audit trail)

### Performance Considerations
- Current baseline: <10ms event dispatch
- Target: No degradation (<10ms with new system)
- Strategy: Minimize object creation, use efficient serialization, lazy loading

### Migration Path
1. **Phase 1 (Story 7.1):** Build new system alongside old, flag defaults to False
2. **Phase 2 (Future):** Gradual rollout, enable flag for specific event types
3. **Phase 3 (Future):** Full migration, deprecate old system
4. **Phase 4 (Future):** Remove old src/events/ code

### Self-Coding AI Preparation
- CLAUDE.md compliance enables future AI agents to extend event system
- Clear patterns: Domain event → Handler → Dispatcher → Repository
- Comprehensive logging enables AI debugging
- Type safety enables AI code generation

---

**Story Created:** 2025-10-25
**Epic:** EPIC-5R Phase 5 - Events & Coordination
**Next:** Run story-ready workflow for SM validation
