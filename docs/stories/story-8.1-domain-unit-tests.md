# Story 8.1: Unit Tests for Domain Layer

Status: Draft

## Story

As a **Developer**,
I want **comprehensive unit tests for all domain layer components**,
so that **we achieve 90%+ test coverage and can refactor confidently**.

## Acceptance Criteria

1. **AC1**: Value objects have 100% test coverage (Priority, Status, EnergyLevel, Context, TimeBlock)
2. **AC2**: Task entity has 100% test coverage (all 18 fields, 9 behavior methods, 3 factory methods)
3. **AC3**: Domain services have 90%+ test coverage (TaskPrioritizationService, EnergyMatchingService, TimeBlockingService)
4. **AC4**: Domain events have 90%+ test coverage (BaseEvent, TaskEvents)
5. **AC5**: Domain models have 90%+ test coverage (Notification model)
6. **AC6**: Integration tests verify domain services working together (at least 20 new tests)
7. **AC7**: All tests follow CLAUDE.md standards (AAA pattern, descriptive names, isolated, fast <10ms each)

## Tasks / Subtasks

- [ ] Task 1: Additional tests for value objects (AC1)
  - [ ] 1.1: Test all edge cases for Priority enum
  - [ ] 1.2: Test all edge cases for Status enum
  - [ ] 1.3: Test all edge cases for EnergyLevel enum
  - [ ] 1.4: Test Context value object validation
  - [ ] 1.5: Test TimeBlock value object validation and overlaps
- [ ] Task 2: Additional tests for Task entity (AC2)
  - [ ] 2.1: Test all Task factory methods edge cases
  - [ ] 2.2: Test Task behavior methods edge cases
  - [ ] 2.3: Test Task immutability enforcement
  - [ ] 2.4: Test Task validation logic
- [ ] Task 3: Comprehensive tests for domain services (AC3)
  - [ ] 3.1: Test TaskPrioritizationService with various task sets
  - [ ] 3.2: Test EnergyMatchingService with different energy levels
  - [ ] 3.3: Test TimeBlockingService with various schedules
  - [ ] 3.4: Test service edge cases and error handling
- [ ] Task 4: Tests for domain events (AC4)
  - [ ] 4.1: Test BaseEvent creation and properties
  - [ ] 4.2: Test all TaskEvents (created, completed, blocked, etc.)
  - [ ] 4.3: Test event serialization/deserialization
- [ ] Task 5: Tests for domain models (AC5)
  - [ ] 5.1: Test Notification model creation
  - [ ] 5.2: Test Notification validation
  - [ ] 5.3: Test Notification priority handling
- [ ] Task 6: Integration tests for domain services (AC6)
  - [ ] 6.1: Test TaskPrioritization + EnergyMatching together
  - [ ] 6.2: Test EnergyMatching + TimeBlocking together
  - [ ] 6.3: Test full workflow: prioritize → match energy → create blocks
  - [ ] 6.4: Test domain services with various task combinations
- [ ] Task 7: Verify test quality and coverage (AC7)
  - [ ] 7.1: Run coverage report for domain layer
  - [ ] 7.2: Verify all tests follow AAA pattern
  - [ ] 7.3: Verify all tests have descriptive names
  - [ ] 7.4: Verify all tests run fast (<10ms each)
  - [ ] 7.5: Verify zero test interdependencies

## Dev Notes

### Architecture Context

**Layer:** Domain (Pure business logic, zero dependencies on infrastructure)
**Pattern:** Hexagonal/Clean Architecture
**Testing Philosophy:** Fast, isolated unit tests. Integration tests for service composition.

### Current Test Coverage (Baseline)

From existing stories:
- Story 5.1: 30 tests for value objects (Priority, Status, EnergyLevel, Context, TimeBlock)
- Story 5.2: 44 tests for Task entity
- Story 5.3: 25 tests for repository interfaces
- Story 6.3: Tests for domain services (TaskPrioritizationService, EnergyMatchingService, TimeBlockingService)

**Current Coverage:** ~75-80% estimated
**Target Coverage:** 90%+ for domain layer

### Testing Standards (CLAUDE.md)

All tests must follow:
1. **AAA Pattern**: Arrange, Act, Assert (clear sections)
2. **Descriptive Names**: test_method_scenario__expected_behavior
3. **Isolation**: No shared state, no test interdependencies
4. **Performance**: Each test <10ms (domain tests should be microseconds)
5. **Coverage**: Use pytest-cov to measure and report

### Test Organization

```
tests/domain/
├── entities/
│   └── test_task.py (existing, enhance)
├── value_objects/
│   └── test_value_objects.py (existing, enhance)
├── services/
│   └── test_domain_services.py (existing, enhance)
├── events/
│   └── test_domain_events.py (new)
├── models/
│   └── test_notification.py (new)
└── integration/
    └── test_domain_integration.py (new - 20+ tests)
```

### Project Structure Notes

**Alignment**: Follows Hexagonal Architecture (ADR-009)
- Domain layer is pure Python (no external dependencies except stdlib)
- No infrastructure imports (no file I/O, no database, no network)
- All dependencies injected via interfaces (repository pattern)

**Testing Approach**:
- Unit tests use mocks for repository interfaces
- Integration tests use in-memory repositories (when available)
- Focus on behavior, not implementation

### References

- [Source: D:\Mission Control\mission-control\CLAUDE.md#Testing Standards]
- [Source: D:\Mission Control\docs\epics.md#EPIC-5R Phase 6]
- [Source: D:\Mission Control\docs\solution-architecture.md#Hexagonal Architecture]
- [Source: D:\Mission Control\docs\stories\story-5.1-domain-value-objects.md]
- [Source: D:\Mission Control\docs\stories\story-5.2-task-entity.md]
- [Source: D:\Mission Control\docs\stories\story-6.3-domain-services.md]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

<!-- Will be filled during implementation -->

### Debug Log References

### Completion Notes List

### File List
