# Story 7.2: Refactor Notification System

**Epic:** EPIC-5R Phase 5 - Events & Coordination
**Story Points:** 5
**Priority:** P0 (Critical - Phase 5)
**Status:** Ready
**Created:** 2025-10-25
**Assigned To:** DEV Agent

---

## Story Description

Refactor existing `src/notifications.py` (808 lines) to use Hexagonal/Clean Architecture with proper domain events, application services, and repository pattern. This story implements the Strangler Fig pattern to gradually migrate from procedural notification handling to clean OOP-based notification system.

---

## Business Value

- **Clean Architecture:** Notifications follow domain-driven design with proper layer boundaries
- **Event-Driven:** Uses domain events from Story 7.1 (TaskCreated, TaskCompleted, etc.)
- **Maintainability:** Notification system becomes easier to extend and test
- **Type Safety:** Strongly-typed notification models replace Dict[str, Any]
- **Testability:** Repository pattern enables easy mocking and testing
- **Future-Ready:** Clean foundation for self-coding AI agents (CLAUDE.md compliance)

---

## Current State

**Existing Implementation (Story 1.10):**
- Notification system in `src/notifications.py` (808 lines)
- Procedural code with direct file I/O
- Notifications represented as `Dict[str, Any]`
- Tight coupling to pattern analyzer and event dispatcher
- 48 tests passing in `tests/test_notifications.py`

**Issues:**
- No domain model for notifications (just dicts)
- Business logic mixed with infrastructure
- Tight coupling to JSON file storage
- Hard to test (global state, file I/O)
- Violates Hexagonal Architecture principles

---

## Desired State

**New Implementation:**
- Domain model: `Notification` class in `src/domain/models/notification.py`
- `NotificationService` in `src/application/services/notification_service.py`
- Uses domain events from Story 7.1 (TaskCreated, TaskCompleted, etc.)
- Repository implementation in `src/infrastructure/persistence/repositories/json_notification_repository.py`
- Feature flag system: `USE_NEW_NOTIFICATION_SYSTEM` in `src/config.py` (defaults to `False`)
- Strangler Fig pattern: Zero modifications to existing `src/notifications.py`
- 15+ tests in `tests/application/services/test_notification_service.py`
- Zero regressions: All 48 existing tests still pass

---

## Acceptance Criteria

### AC1: Domain Model Created
**Given** the need for strongly-typed notification models
**When** domain models are implemented
**Then**:
- [ ] `src/domain/models/notification.py` created with `Notification` class
- [ ] Fields: `notification_id`, `title`, `message`, `priority`, `category`, `timestamp`, `read`, `dismissed`, `metadata`
- [ ] All fields have type hints
- [ ] Immutable (frozen dataclass)
- [ ] Self-validation in `__post_init__`
- [ ] Factory methods: `from_event(event: DomainEvent)`, `from_pattern(pattern_data: dict)`

### AC2: NotificationService Created
**Given** the need for notification generation and management
**When** NotificationService is implemented
**Then**:
- [ ] `src/application/services/notification_service.py` created
- [ ] Uses dependency injection (repositories passed in constructor)
- [ ] Methods:
  - `generate_from_event(event: DomainEvent) -> Notification`
  - `generate_from_pattern(pattern_data: dict) -> Notification`
  - `get_unread_notifications(limit: int = 10) -> List[Notification]`
  - `mark_as_read(notification_id: str) -> bool`
  - `dismiss_notification(notification_id: str) -> bool`
  - `get_notification_by_id(notification_id: str) -> Optional[Notification]`
- [ ] All operations log entry/exit/errors

### AC3: Event Integration
**Given** the need to react to domain events
**When** event handlers are configured
**Then**:
- [ ] NotificationService registers as handler for task events
- [ ] `TaskCreated` event → generates "New task" notification
- [ ] `TaskCompleted` event → generates "Task completed" notification
- [ ] `TaskDeleted` event → generates "Task deleted" notification
- [ ] Event metadata preserved in notification

### AC4: Repository Implementation
**Given** the need for notification persistence
**When** notification repository is implemented
**Then**:
- [ ] `src/domain/repositories/notification_repository.py` created with `INotificationRepository` interface
- [ ] Interface defines: `save()`, `find_by_id()`, `find_unread()`, `update()`, `delete()`
- [ ] `src/infrastructure/persistence/repositories/json_notification_repository.py` implements interface
- [ ] JSONL format for notification log
- [ ] Graceful error handling with logging

### AC5: Feature Flag System
**Given** the need for gradual migration
**When** feature flag is implemented
**Then**:
- [ ] `src/config.py` updated with `USE_NEW_NOTIFICATION_SYSTEM = False` (default)
- [ ] Dual-path routing in notification entry points
- [ ] Feature flag can be overridden via environment variable `MISSION_CONTROL_USE_NEW_NOTIFICATION_SYSTEM=true`
- [ ] Logging indicates which path is active

### AC6: Strangler Fig Pattern (Zero Breaking Changes)
**Given** the need for backward compatibility
**When** refactoring is complete
**Then**:
- [ ] Zero modifications to existing `src/notifications.py`
- [ ] Old notification system continues to work (when flag = False)
- [ ] New notification system works independently (when flag = True)
- [ ] Can switch between implementations at runtime
- [ ] All 48 existing tests still pass (zero regressions)

### AC7: Comprehensive Tests
**Given** the need for quality assurance
**When** tests are written
**Then**:
- [ ] 15+ tests in `tests/application/services/test_notification_service.py`
- [ ] Domain model tests: `tests/domain/models/test_notification.py` (5+ tests)
- [ ] Repository tests: `tests/infrastructure/persistence/test_json_notification_repository.py` (5+ tests)
- [ ] Integration tests: `tests/integration/test_notification_system_integration.py` (5+ tests)
- [ ] All tests pass (100%)
- [ ] All 48 existing notification tests still pass (zero regressions)
- [ ] Test coverage ≥ 90% for new code

---

## Technical Implementation Plan

### Phase 1: Domain Layer (Notification Model)
1. Create `src/domain/models/__init__.py`
2. Create `src/domain/models/notification.py`:
   - `Notification` class (frozen dataclass)
   - Fields: notification_id, title, message, priority, category, timestamp, read, dismissed, metadata
   - Factory methods: `from_event()`, `from_pattern()`
   - Method: `to_dict()` for serialization
3. Write tests: `tests/domain/models/test_notification.py`

### Phase 2: Application Layer (NotificationService)
1. Create `src/application/services/notification_service.py`:
   - Constructor: `__init__(notification_repo: INotificationRepository)`
   - Methods: generate_from_event, generate_from_pattern, get_unread, mark_as_read, dismiss
   - Entry/exit logging
2. Write tests: `tests/application/services/test_notification_service.py`

### Phase 3: Infrastructure Layer (Repository)
1. Create `src/domain/repositories/notification_repository.py`:
   - `INotificationRepository` interface (ABC)
   - Methods: save, find_by_id, find_unread, update, delete
2. Create `src/infrastructure/persistence/repositories/json_notification_repository.py`:
   - Implements `INotificationRepository`
   - JSONL storage format
   - Use `JsonStorage` utility
3. Write tests: `tests/infrastructure/persistence/test_json_notification_repository.py`

### Phase 4: Event Integration
1. Update `src/application/event_handlers/task_event_handlers.py`:
   - Inject NotificationService into handlers
   - Generate notifications on task events
2. Write integration tests

### Phase 5: Feature Flag & Integration
1. Update `src/config.py`:
   - Add `USE_NEW_NOTIFICATION_SYSTEM = False`
   - Add `get_notification_system_mode()` helper
2. Create dual-path routing in notification entry points
3. Write integration tests: `tests/integration/test_notification_system_integration.py`

### Phase 6: Testing & Validation
1. Run all 48 existing notification tests → Must pass
2. Run 15+ new tests → Must pass
3. Manual validation: Switch flag on/off, verify both paths work
4. Regression testing: Full test suite

---

## Dependencies

### Upstream Dependencies (Must be complete)
- ✅ Story 7.1: Refactor Event System (provides domain events)
- ✅ Story 5.1: Domain Value Objects (provides Priority enum)
- ✅ Story 5.3: Repository Interfaces (provides IRepository pattern)
- ✅ Story 5.4: JSON Storage Utility (provides JsonStorage)

### Downstream Dependencies (Blocked by this story)
- ⏳ Story 7.3: Refactor Coordination (depends on notification architecture)

---

## Constraints & Considerations

### Technical Constraints
1. **Backward Compatibility:** Old notification system must continue to work
2. **Zero Regressions:** All 48 existing tests must still pass
3. **Strangler Fig:** No modifications to existing `src/notifications.py`

### Architecture Constraints
1. **Hexagonal Architecture:** Strict layer boundaries (domain → application → infrastructure)
2. **SOLID Principles:** Especially SRP, DIP
3. **Repository Pattern:** All persistence via repositories
4. **Type Safety:** Full type hints

### Testing Constraints
1. **Coverage:** ≥ 90% for new code
2. **Test Count:** ≥ 15 new tests
3. **Integration Tests:** ≥ 5 tests covering full notification flow

---

## Testing Strategy

### Unit Tests (Domain Layer)
- **tests/domain/models/test_notification.py** (5+ tests)
  - Test notification creation with valid data
  - Test notification immutability
  - Test notification validation
  - Test factory methods (from_event, from_pattern)
  - Test serialization (to_dict)

### Unit Tests (Application Layer)
- **tests/application/services/test_notification_service.py** (15+ tests)
  - Test generate_from_event for each event type
  - Test generate_from_pattern
  - Test get_unread_notifications
  - Test mark_as_read
  - Test dismiss_notification
  - Test error handling

### Integration Tests (Infrastructure Layer)
- **tests/infrastructure/persistence/test_json_notification_repository.py** (5+ tests)
  - Test save notification
  - Test find_by_id
  - Test find_unread
  - Test update notification
  - Test delete notification

### Integration Tests (Full Stack)
- **tests/integration/test_notification_system_integration.py** (5+ tests)
  - Test end-to-end notification flow (event → notification → persist)
  - Test feature flag switching
  - Test unread notification retrieval
  - Test notification management (read/dismiss)

### Regression Tests
- **All existing tests** (48 tests in tests/test_notifications.py)
  - Must all still pass with flag = False
  - Zero modifications to test files

---

## Definition of Done

- [ ] All 7 acceptance criteria met
- [ ] 15+ new tests passing (100%)
- [ ] All 48 existing notification tests still passing (zero regressions)
- [ ] Code follows CLAUDE.md engineering standards
- [ ] All functions have type hints
- [ ] All operations log to stdout (entry/exit/errors)
- [ ] Feature flag system working (can switch between old/new)
- [ ] Strangler Fig pattern confirmed (no changes to src/notifications.py)
- [ ] Story committed to git: `Story 7.2: Notification System - Implementation Complete`
- [ ] Code review completed (or self-review if solo)

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing code | Medium | High | Feature flag, Strangler Fig, comprehensive testing |
| Complexity creep | Medium | Medium | Follow SOLID, limit scope to AC7 |
| Event integration issues | Low | Medium | Use proven event handlers from Story 7.1 |

---

## Notes

### Architecture Decisions
- Using frozen dataclasses for immutable notification models
- NotificationService is stateless with dependency injection
- Repository interface enables future migration to database
- JSONL format preserves append-only notification log

### Migration Path
1. **Phase 1 (Story 7.2):** Build new system alongside old, flag defaults to False
2. **Phase 2 (Future):** Gradual rollout, enable flag for specific features
3. **Phase 3 (Future):** Full migration, deprecate old system
4. **Phase 4 (Future):** Remove old src/notifications.py code

---

**Story Created:** 2025-10-25
**Epic:** EPIC-5R Phase 5 - Events & Coordination
**Next:** Run story-ready workflow for SM validation
