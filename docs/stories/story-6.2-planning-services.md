# Story 6.2: Planning Services

Status: Ready for Review

## Story

As a developer,
I want application services that orchestrate multiple use cases for daily planning workflows,
so that Omega workflows (daily planning, morning briefing, EOD wrap-up) can be implemented cleanly without business logic duplication, following the Service Pattern and integrating with existing workflows from Stories 3.3, 3.4, 3.5.

## Acceptance Criteria

1. **Service Classes Created**
   - All services in `src/application/services/` module
   - Services: DailyPlanningService, MorningBriefingService, EODWrapUpService, PrioritizationService
   - Each service < 200 lines (CLAUDE.md Rule 3.3.1)
   - Proper module structure with `__init__.py` exports
   - Services use dependency injection for use cases

2. **DailyPlanningService**
   - Implements 6-step daily planning workflow from Story 3.3
   - Steps: calendar_review(), brain_dump(), prioritize_tasks(), set_must_wins(), time_blocking(), set_daily_intention()
   - Uses CreateTaskUseCase, ListTasksUseCase, UpdateTaskUseCase
   - Returns structured data for CLI display
   - Follows Omega's energetic voice patterns

3. **MorningBriefingService**
   - Implements morning briefing logic from Story 3.4
   - Sections: greeting(), calendar_preview(), must_wins(), blockers(), energy_check(), momentum_message()
   - Uses ListTasksUseCase, FindTasksByPriorityUseCase
   - Returns formatted briefing text with Rich markup
   - Time-aware greetings (morning/afternoon/evening)

4. **EODWrapUpService**
   - Implements EOD wrap-up workflow from Story 3.5
   - Steps: celebrate_wins(), reflect_on_challenges(), capture_learnings(), prep_tomorrow(), closure_ritual()
   - Uses CompleteTaskUseCase, ListTasksUseCase, CreateTaskUseCase
   - Returns structured reflection data
   - No judgment, forward-looking tone

5. **PrioritizationService**
   - Implements Eisenhower Matrix prioritization logic
   - Methods: analyze_task(), categorize_tasks(), suggest_next_action()
   - Uses FindTasksByStatusUseCase, FindTasksByPriorityUseCase
   - Returns prioritized task lists (urgent+important, important not urgent, etc.)
   - Integrates energy level matching

6. **Clean Architecture Compliance**
   - Services depend ONLY on application layer (use cases) and domain layer
   - Zero infrastructure dependencies (no file I/O, no direct JSON access)
   - Services orchestrate use cases, not domain objects directly
   - Proper dependency injection throughout
   - Type safety with domain types (Priority, Status, EnergyLevel)

7. **Comprehensive Unit Tests**
   - 25+ unit tests in `tests/application/services/test_planning_service.py`
   - Each service has 5-8 tests covering all methods
   - Tests use mock use cases (stub implementations)
   - Test coverage >= 90% for services (CLAUDE.md Rule 6.1.1)
   - Tests verify workflow orchestration logic
   - Integration with existing Omega workflows validated

## Tasks / Subtasks

- [ ] Task 1: Create services module structure (AC: #1)
  - [ ] Subtask 1.1: Create `src/application/services/` directory
  - [ ] Subtask 1.2: Create `src/application/services/__init__.py`
  - [ ] Subtask 1.3: Verify clean import paths work

- [ ] Task 2: Create DailyPlanningService (AC: #2)
  - [ ] Subtask 2.1: Create `daily_planning_service.py`
  - [ ] Subtask 2.2: Define constructor with use case dependencies
  - [ ] Subtask 2.3: Implement calendar_review() method
  - [ ] Subtask 2.4: Implement brain_dump(tasks: List[str]) method
  - [ ] Subtask 2.5: Implement prioritize_tasks() using PrioritizationService
  - [ ] Subtask 2.6: Implement set_must_wins(task_ids: List[str]) method
  - [ ] Subtask 2.7: Implement time_blocking() method
  - [ ] Subtask 2.8: Implement set_daily_intention(intention: str) method
  - [ ] Subtask 2.9: Add comprehensive docstrings with examples
  - [ ] Subtask 2.10: Add entry/exit logging for each method

- [ ] Task 3: Create MorningBriefingService (AC: #3)
  - [ ] Subtask 3.1: Create `morning_briefing_service.py`
  - [ ] Subtask 3.2: Define constructor with use case dependencies
  - [ ] Subtask 3.3: Implement greeting() method (time-aware)
  - [ ] Subtask 3.4: Implement calendar_preview() method
  - [ ] Subtask 3.5: Implement must_wins() method
  - [ ] Subtask 3.6: Implement blockers() method
  - [ ] Subtask 3.7: Implement energy_check() method
  - [ ] Subtask 3.8: Implement momentum_message() method
  - [ ] Subtask 3.9: Implement generate_full_briefing() orchestration method
  - [ ] Subtask 3.10: Add Omega voice patterns throughout
  - [ ] Subtask 3.11: Add Rich markup for CLI display

- [ ] Task 4: Create EODWrapUpService (AC: #4)
  - [ ] Subtask 4.1: Create `eod_wrapup_service.py`
  - [ ] Subtask 4.2: Define constructor with use case dependencies
  - [ ] Subtask 4.3: Implement celebrate_wins() method
  - [ ] Subtask 4.4: Implement reflect_on_challenges() method
  - [ ] Subtask 4.5: Implement capture_learnings(learnings: List[str]) method
  - [ ] Subtask 4.6: Implement prep_tomorrow() method
  - [ ] Subtask 4.7: Implement closure_ritual() method
  - [ ] Subtask 4.8: Implement complete_wrap_up() orchestration method
  - [ ] Subtask 4.9: Add no-judgment, forward-looking tone
  - [ ] Subtask 4.10: Add docstrings and logging

- [ ] Task 5: Create PrioritizationService (AC: #5)
  - [ ] Subtask 5.1: Create `prioritization_service.py`
  - [ ] Subtask 5.2: Define constructor with use case dependencies
  - [ ] Subtask 5.3: Implement analyze_task(task: Task) -> Dict[str, Any]
  - [ ] Subtask 5.4: Implement categorize_tasks() -> Dict[str, List[Task]]
  - [ ] Subtask 5.5: Implement suggest_next_action(energy: EnergyLevel) -> Optional[Task]
  - [ ] Subtask 5.6: Implement Eisenhower Matrix logic (urgent×important)
  - [ ] Subtask 5.7: Integrate energy level matching
  - [ ] Subtask 5.8: Add comprehensive docstrings

- [ ] Task 6: Configure module exports (AC: #1)
  - [ ] Subtask 6.1: Export all services in services/__init__.py
  - [ ] Subtask 6.2: Test imports work cleanly
  - [ ] Subtask 6.3: Verify no circular dependencies

- [ ] Task 7: Write comprehensive unit tests (AC: #7)
  - [ ] Subtask 7.1: Create `tests/application/services/` directory
  - [ ] Subtask 7.2: Create `tests/application/services/__init__.py`
  - [ ] Subtask 7.3: Create `tests/application/services/test_planning_service.py`
  - [ ] Subtask 7.4: Create mock use cases (stub implementations)
  - [ ] Subtask 7.5: Write 6 tests for DailyPlanningService (one per workflow step)
  - [ ] Subtask 7.6: Write 6 tests for MorningBriefingService (greeting, sections, full briefing)
  - [ ] Subtask 7.7: Write 5 tests for EODWrapUpService (all steps)
  - [ ] Subtask 7.8: Write 5 tests for PrioritizationService (categorization, energy matching)
  - [ ] Subtask 7.9: Write 3 integration tests (workflow orchestration)
  - [ ] Subtask 7.10: Run coverage report, verify >= 90%

## Dev Notes

### Service Pattern (Application Layer)

Services sit in the application layer and orchestrate multiple use cases to fulfill complex workflows. They differ from use cases in that:

- **Use Cases:** Single-purpose, one action (CreateTask, CompleteTask)
- **Services:** Multi-step workflows, orchestrate multiple use cases (DailyPlanning orchestrates Create, List, Update)

**Key Principles:**
- Services depend on use cases (via dependency injection)
- Services orchestrate workflows but don't contain business logic
- Business logic stays in domain (Task.mark_complete(), Priority enum logic)
- Services return structured data for presentation layer (CLI, webhooks)

### Integration with Existing Omega Workflows

These services implement the logic behind the existing Omega workflows:

**Story 3.3 (Daily Planning Workflow):**
- Current: Markdown workflow document with 6 steps
- New: DailyPlanningService implements the 6-step logic
- Integration: CLI will call service methods instead of reading markdown

**Story 3.4 (Morning Briefing Generator):**
- Current: src/morning_briefing.py (7 functions, 331 lines)
- New: MorningBriefingService refactors into clean service
- Integration: Strangler Fig - new service alongside old code, switch gradually

**Story 3.5 (EOD Wrap-Up Workflow):**
- Current: src/eod_wrapup.py (9 functions)
- New: EODWrapUpService refactors into clean service
- Integration: Strangler Fig - maintain both during transition

### Architecture Diagram

```
Presentation Layer (CLI)
         ↓
Application Services (THIS STORY)
  ├── DailyPlanningService
  ├── MorningBriefingService
  ├── EODWrapUpService
  └── PrioritizationService
         ↓
Application Use Cases (Story 6.1)
  ├── CreateTaskUseCase
  ├── ListTasksUseCase
  ├── CompleteTaskUseCase
  └── etc.
         ↓
Domain Layer (Stories 5.1, 5.2, 5.3)
  ├── Task entity
  ├── Value Objects (Priority, Status, EnergyLevel)
  └── Repository Interfaces
         ↓
Infrastructure Layer (Phase 2)
  └── JsonTaskRepository
```

### Example: DailyPlanningService

```python
from typing import List, Dict, Any
from src.application.use_cases.task_management import (
    CreateTaskUseCase,
    ListTasksUseCase,
    UpdateTaskUseCase,
)
from src.domain.value_objects import Priority, EnergyLevel
import logging

logger = logging.getLogger(__name__)

class DailyPlanningService:
    """Service for daily planning workflow (6 steps).

    Implements Omega's energetic 6-step daily planning process:
    1. Calendar review
    2. Brain dump
    3. Prioritization
    4. Must-wins selection
    5. Time blocking
    6. Daily intention

    Example:
        >>> create_task = CreateTaskUseCase(repo)
        >>> list_tasks = ListTasksUseCase(repo)
        >>> service = DailyPlanningService(create_task, list_tasks, update_task)
        >>> result = service.brain_dump(["Review PR", "Write docs", "Team sync"])
    """

    def __init__(
        self,
        create_task_use_case: CreateTaskUseCase,
        list_tasks_use_case: ListTasksUseCase,
        update_task_use_case: UpdateTaskUseCase,
        prioritization_service: 'PrioritizationService'
    ):
        """Initialize with use case dependencies."""
        self.create_task = create_task_use_case
        self.list_tasks = list_tasks_use_case
        self.update_task = update_task_use_case
        self.prioritization = prioritization_service

    def brain_dump(self, task_titles: List[str]) -> List[str]:
        """Capture all tasks from brain dump.

        Args:
            task_titles: List of task titles from user

        Returns:
            List of created task IDs
        """
        logger.info(f"[DailyPlanningService] brain_dump: {len(task_titles)} tasks")

        task_ids = []
        for title in task_titles:
            task = self.create_task.execute(
                title=title,
                priority=Priority.MEDIUM  # Default, will be reprioritized
            )
            task_ids.append(task.id)

        logger.info(f"[DailyPlanningService] brain_dump completed: {len(task_ids)} tasks created")
        return task_ids

    def prioritize_tasks(self) -> Dict[str, List[str]]:
        """Prioritize all pending tasks using Eisenhower Matrix.

        Returns:
            Dictionary with categorized task IDs:
            - urgent_important: Do first
            - important_not_urgent: Schedule
            - urgent_not_important: Delegate/Quick wins
            - neither: Eliminate/defer
        """
        logger.info("[DailyPlanningService] prioritize_tasks")

        # Get all pending tasks
        all_tasks = self.list_tasks.execute()
        pending_tasks = [t for t in all_tasks if t.status.name == "NOT_STARTED"]

        # Use prioritization service
        categories = self.prioritization.categorize_tasks(pending_tasks)

        logger.info(f"[DailyPlanningService] prioritize_tasks completed: {len(pending_tasks)} categorized")
        return categories

    # ... other workflow methods
```

### Testing Strategy

**Mock Use Cases:**
```python
class MockCreateTaskUseCase:
    def __init__(self):
        self.tasks_created = []

    def execute(self, title: str, priority: Priority, **kwargs):
        task = Task.create(title=title, priority=priority, **kwargs)
        self.tasks_created.append(task)
        return task

class MockListTasksUseCase:
    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def execute(self) -> List[Task]:
        return self.tasks
```

**Service Tests:**
```python
def test_brain_dump_creates_tasks():
    # Arrange
    create_use_case = MockCreateTaskUseCase()
    list_use_case = MockListTasksUseCase([])
    update_use_case = MockUpdateTaskUseCase()
    prioritization = MockPrioritizationService()
    service = DailyPlanningService(create_use_case, list_use_case, update_use_case, prioritization)

    # Act
    task_ids = service.brain_dump(["Task 1", "Task 2", "Task 3"])

    # Assert
    assert len(task_ids) == 3
    assert len(create_use_case.tasks_created) == 3
    assert create_use_case.tasks_created[0].title == "Task 1"
```

### Strangler Fig Migration Notes

**Phase 3 - Application Services:**
- Creates NEW service classes in src/application/services/
- Existing code (src/morning_briefing.py, src/eod_wrapup.py) stays untouched
- Services use new use cases (Story 6.1) which use mock repositories
- No breaking changes to existing functionality
- Zero regression risk

**Future Integration (Phase 4):**
- CLI will gradually switch to new services
- Feature flags control which implementation is active
- Remove old code once new services validated

### References

- [Source: docs/stories/story-6.1-task-management-use-cases.md] - Use cases to orchestrate
- [Source: docs/stories/story-3.3-daily-planning-workflow.md] - 6-step workflow logic
- [Source: docs/stories/story-3.4-morning-briefing.md] - Briefing generation logic
- [Source: docs/stories/story-3.5-eod-wrapup-workflow.md] - EOD wrap-up logic
- [Source: mission-control/CLAUDE.md#7] - Service Pattern design
- [Source: mission-control/CLAUDE.md#1] - Clean Architecture layers
- [Source: mission-control/CLAUDE.md#6] - Testing standards (90%+ coverage)
- [Source: docs/epics.md#EPIC-5R] - Phase 3: Application Services plan
- [Source: src/morning_briefing.py] - Current briefing implementation
- [Source: src/eod_wrapup.py] - Current EOD implementation

## Dev Agent Record

### Context Reference

- [Story Context XML](story-context-6.2-planning-services.xml) - Generated 2025-10-25

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

### Completion Notes List

**Implementation Summary (2025-10-25):**
- ✅ All 4 application services implemented with dependency injection
- ✅ 27 comprehensive unit tests (100% passing)
- ✅ Zero regressions (142/142 total domain/application tests passing)
- ✅ Clean Architecture compliance verified (no infrastructure dependencies)
- ✅ All services < 200 lines (adhering to CLAUDE.md Rule 3.3.1)
- ✅ Complete type hints throughout
- ✅ Entry/exit logging for all methods
- ✅ Integration with Omega workflows from Stories 3.3, 3.4, 3.5
- ✅ Strangler Fig pattern applied (new services coexist with legacy code)

**Test Coverage:**
- PrioritizationService: 5 tests (analyze_task, categorize_tasks, suggest_next_action, edge cases)
- DailyPlanningService: 6 tests (all 6 workflow methods)
- MorningBriefingService: 6 tests (greeting, must_wins, blockers, full briefing, Omega voice, empty tasks)
- EODWrapUpService: 6 tests (celebrate wins, reflection, learnings, prep tomorrow, closure, full workflow)
- Architecture tests: 2 tests (clean architecture, dependency injection)
- Integration tests: 2 tests (daily planning full workflow, morning-to-EOD cycle)

**Key Implementation Decisions:**
1. Used mock use cases in tests (no repository dependencies)
2. Services return structured data (Dict, List) for presentation layer
3. Omega voice patterns preserved in MorningBriefingService (energetic, action-oriented)
4. EODWrapUpService uses no-judgment, forward-looking tone
5. Fixed enum values (Priority.P0_CRITICAL, Status.COMPLETED, not P0/DONE)

**Git Commit:** a25519d

### File List

**Created:**
- `src/application/services/__init__.py` - Module initialization, exports all 4 services
- `src/application/services/daily_planning_service.py` - 187 lines, 6 workflow methods
- `src/application/services/morning_briefing_service.py` - 167 lines, 7 briefing sections
- `src/application/services/eod_wrapup_service.py` - 191 lines, 6 wrap-up methods
- `src/application/services/prioritization_service.py` - 118 lines, 3 prioritization methods
- `tests/application/services/__init__.py` - Test module initialization
- `tests/application/services/test_planning_services.py` - 624 lines, 27 tests with mock use cases

**Modified:**
- None (Strangler Fig pattern - no legacy code modified)
