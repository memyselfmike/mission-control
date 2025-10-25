# Story 6.3: Domain Services

Status: Done

## Story

As a developer,
I want domain services that encapsulate complex business logic and algorithms,
so that domain intelligence (Eisenhower Matrix prioritization, energy matching, time blocking) is reusable, testable, and isolated from application/infrastructure concerns, following Clean Architecture and Domain-Driven Design principles.

## Acceptance Criteria

1. **Domain Services Created**
   - All services in `src/domain/services/` module
   - Services: TaskPrioritizationService, EnergyMatchingService, TimeBlockingService
   - Each service < 150 lines (CLAUDE.md Rule 3.3.1)
   - Pure domain logic with ZERO external dependencies
   - Stateless services (no instance variables except configuration)

2. **TaskPrioritizationService**
   - Implements Eisenhower Matrix (2×2: urgent × important)
   - Methods: categorize_task(task), categorize_tasks(tasks), get_next_action(tasks, criteria)
   - Returns categorized task lists: urgent_important, important_not_urgent, urgent_not_important, neither
   - Uses domain value objects (Priority, Status) only
   - Algorithm based on due_date (urgency) and priority (importance)

3. **EnergyMatchingService**
   - Matches tasks to user's current energy level
   - Methods: match_task_to_energy(task, energy), suggest_tasks_for_energy(tasks, energy)
   - Considers task.energy_requirement vs user's current energy level
   - Returns ranked task lists (best match first)
   - Uses EnergyLevel enum (HIGH, MEDIUM, LOW)

4. **TimeBlockingService**
   - Allocates tasks to time blocks in a day
   - Methods: create_time_blocks(tasks, available_hours), optimize_schedule(blocks)
   - Considers task duration, priority, energy requirements
   - Returns structured time blocks with assigned tasks
   - Uses TimeBlock value object from Story 5.1

5. **Pure Domain Logic**
   - Domain services have ZERO infrastructure dependencies
   - No file I/O, no database access, no HTTP calls
   - No imports from application or infrastructure layers
   - Only imports from domain layer (entities, value objects)
   - Stateless and deterministic (same inputs → same outputs)

6. **Type Safety and Documentation**
   - Complete type hints on all methods
   - Comprehensive docstrings with algorithm descriptions
   - Examples in docstrings showing usage
   - No `Any` types (use domain types)
   - Explicit return types (Task, List[Task], Dict[str, List[Task]])

7. **Comprehensive Unit Tests**
   - 15+ unit tests in `tests/domain/services/test_domain_services.py`
   - Each service has 4-6 tests covering all methods
   - Tests use domain objects only (no mocks needed - pure functions!)
   - Test coverage >= 90% for domain services (CLAUDE.md Rule 6.1.1)
   - Tests verify algorithm correctness and edge cases

## Tasks / Subtasks

- [ ] Task 1: Create domain services module structure (AC: #1)
  - [ ] Subtask 1.1: Create `src/domain/services/` directory
  - [ ] Subtask 1.2: Create `src/domain/services/__init__.py`
  - [ ] Subtask 1.3: Verify clean import paths work

- [ ] Task 2: Create TaskPrioritizationService (AC: #2)
  - [ ] Subtask 2.1: Create `task_prioritization_service.py`
  - [ ] Subtask 2.2: Define class (stateless, no __init__ needed)
  - [ ] Subtask 2.3: Implement categorize_task(task: Task) -> str method
  - [ ] Subtask 2.4: Implement categorize_tasks(tasks: List[Task]) -> Dict[str, List[Task]]
  - [ ] Subtask 2.5: Implement get_next_action(tasks: List[Task], criteria: Dict) -> Optional[Task]
  - [ ] Subtask 2.6: Define Eisenhower Matrix logic (urgency × importance)
  - [ ] Subtask 2.7: Add comprehensive docstrings with algorithm explanation
  - [ ] Subtask 2.8: Add type hints throughout

- [ ] Task 3: Create EnergyMatchingService (AC: #3)
  - [ ] Subtask 3.1: Create `energy_matching_service.py`
  - [ ] Subtask 3.2: Define class (stateless)
  - [ ] Subtask 3.3: Implement match_task_to_energy(task: Task, energy: EnergyLevel) -> float
  - [ ] Subtask 3.4: Implement suggest_tasks_for_energy(tasks: List[Task], energy: EnergyLevel) -> List[Task]
  - [ ] Subtask 3.5: Define matching algorithm (HIGH→P0, MEDIUM→P1/P2, LOW→P3)
  - [ ] Subtask 3.6: Add ranking logic (sort by match score)
  - [ ] Subtask 3.7: Add docstrings with matching rules
  - [ ] Subtask 3.8: Add type hints

- [ ] Task 4: Create TimeBlockingService (AC: #4)
  - [ ] Subtask 4.1: Create `time_blocking_service.py`
  - [ ] Subtask 4.2: Define class (stateless)
  - [ ] Subtask 4.3: Implement create_time_blocks(tasks: List[Task], available_hours: int) -> List[TimeBlock]
  - [ ] Subtask 4.4: Implement optimize_schedule(blocks: List[TimeBlock]) -> List[TimeBlock]
  - [ ] Subtask 4.5: Define time allocation algorithm (priority + energy + duration)
  - [ ] Subtask 4.6: Add schedule optimization logic (minimize context switching)
  - [ ] Subtask 4.7: Add docstrings with algorithm description
  - [ ] Subtask 4.8: Add type hints

- [ ] Task 5: Configure module exports (AC: #1)
  - [ ] Subtask 5.1: Export all services in services/__init__.py
  - [ ] Subtask 5.2: Test imports work cleanly
  - [ ] Subtask 5.3: Verify no circular dependencies

- [ ] Task 6: Write comprehensive unit tests (AC: #7)
  - [ ] Subtask 6.1: Create `tests/domain/services/` directory
  - [ ] Subtask 6.2: Create `tests/domain/services/__init__.py`
  - [ ] Subtask 6.3: Create `tests/domain/services/test_domain_services.py`
  - [ ] Subtask 6.4: Write 5 tests for TaskPrioritizationService (all categories, edge cases)
  - [ ] Subtask 6.5: Write 5 tests for EnergyMatchingService (all energy levels, ranking)
  - [ ] Subtask 6.6: Write 5 tests for TimeBlockingService (allocation, optimization)
  - [ ] Subtask 6.7: Test edge cases (empty task list, single task, conflicting priorities)
  - [ ] Subtask 6.8: Run coverage report, verify >= 90%

## Dev Notes

### Domain Services vs Application Services

**Domain Services (THIS STORY):**
- Live in `src/domain/services/`
- Pure business logic and algorithms
- Stateless functions operating on domain objects
- ZERO external dependencies (no repositories, no use cases)
- Examples: TaskPrioritizationService, EnergyMatchingService

**Application Services (Story 6.2):**
- Live in `src/application/services/`
- Orchestrate use cases for workflows
- Depend on use cases and domain services
- Examples: DailyPlanningService, MorningBriefingService

**Key Difference:**
- Domain services: "How to prioritize tasks?" (algorithm)
- Application services: "Execute daily planning workflow" (orchestration)

### Clean Architecture - Domain Layer

Domain services are part of the **Domain Layer** (innermost circle):

```
┌─────────────────────────────────────┐
│   Infrastructure Layer              │
│   (Repositories, File I/O)          │
│   ┌─────────────────────────────┐   │
│   │   Application Layer         │   │
│   │   (Use Cases, Services)     │   │
│   │   ┌─────────────────────┐   │   │
│   │   │   Domain Layer      │   │   │
│   │   │   (Entities,        │   │   │
│   │   │    Value Objects,   │   │   │
│   │   │    Domain Services) │◄──┼───┼─── THIS STORY
│   │   └─────────────────────┘   │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Domain Layer Rules (CLAUDE.md):**
1. No outward dependencies (can't import from application/infrastructure)
2. Pure business logic only
3. Stateless and deterministic
4. Testable without mocks (pure functions)
5. Domain services operate on domain objects (Task, Priority, Status)

### Eisenhower Matrix Algorithm

The **Eisenhower Matrix** (2×2 decision framework) categorizes tasks:

```
                Important   | Not Important
                -----------+--------------
Urgent          |  DO FIRST  |  QUICK WINS
                |  (P0/P1)   |  (Delegate)
                -----------+--------------
Not Urgent      |  SCHEDULE  |  ELIMINATE
                |  (P1/P2)   |  (P3/ignore)
```

**Implementation Logic:**
```python
class TaskPrioritizationService:
    """Domain service for task prioritization using Eisenhower Matrix."""

    @staticmethod
    def categorize_task(task: Task) -> str:
        """Categorize single task into Eisenhower Matrix quadrant.

        Urgency: Based on due_date (< 24 hours = urgent)
        Importance: Based on priority (P0/P1 = important)

        Returns:
            - "urgent_important" → Do first
            - "important_not_urgent" → Schedule
            - "urgent_not_important" → Quick wins / delegate
            - "neither" → Eliminate / defer
        """
        is_urgent = task.is_due_soon(hours=24)  # Domain method
        is_important = task.priority in [Priority.P0, Priority.P1]

        if is_urgent and is_important:
            return "urgent_important"
        elif is_important and not is_urgent:
            return "important_not_urgent"
        elif is_urgent and not is_important:
            return "urgent_not_important"
        else:
            return "neither"

    @staticmethod
    def categorize_tasks(tasks: List[Task]) -> Dict[str, List[Task]]:
        """Categorize all tasks into Eisenhower Matrix quadrants.

        Returns:
            Dictionary with 4 keys:
            - urgent_important: Critical tasks (do first)
            - important_not_urgent: Important work (schedule)
            - urgent_not_important: Quick wins (delegate)
            - neither: Low priority (defer/eliminate)
        """
        categories = {
            "urgent_important": [],
            "important_not_urgent": [],
            "urgent_not_important": [],
            "neither": []
        }

        for task in tasks:
            category = TaskPrioritizationService.categorize_task(task)
            categories[category].append(task)

        return categories

    @staticmethod
    def get_next_action(
        tasks: List[Task],
        criteria: Dict[str, Any]
    ) -> Optional[Task]:
        """Get the next recommended task based on criteria.

        Criteria:
        - energy: Current energy level (HIGH, MEDIUM, LOW)
        - available_minutes: Time available
        - focus_mode: bool (prefer deep work vs quick wins)

        Returns:
            Highest priority task matching criteria, or None
        """
        # Filter tasks by criteria
        energy = criteria.get("energy", EnergyLevel.MEDIUM)
        available_minutes = criteria.get("available_minutes", 60)

        # Use EnergyMatchingService
        energy_service = EnergyMatchingService()
        matched_tasks = energy_service.suggest_tasks_for_energy(tasks, energy)

        # Filter by available time
        feasible_tasks = [
            t for t in matched_tasks
            if t.estimated_duration_minutes <= available_minutes
        ]

        # Return highest priority
        return feasible_tasks[0] if feasible_tasks else None
```

### Energy Matching Algorithm

**EnergyMatchingService** matches tasks to user's current energy:

```python
class EnergyMatchingService:
    """Domain service for matching tasks to energy levels."""

    # Energy matching rules
    ENERGY_TO_PRIORITY = {
        EnergyLevel.HIGH: [Priority.P0, Priority.P1],     # Deep work
        EnergyLevel.MEDIUM: [Priority.P1, Priority.P2],   # Regular work
        EnergyLevel.LOW: [Priority.P2, Priority.P3]       # Light work
    }

    @staticmethod
    def match_task_to_energy(task: Task, energy: EnergyLevel) -> float:
        """Calculate match score (0.0-1.0) for task and energy level.

        Args:
            task: Task to match
            energy: Current energy level

        Returns:
            Match score: 1.0 (perfect), 0.5 (acceptable), 0.0 (poor match)
        """
        ideal_priorities = EnergyMatchingService.ENERGY_TO_PRIORITY[energy]

        if task.priority in ideal_priorities:
            return 1.0  # Perfect match
        elif abs(task.priority.value - ideal_priorities[0].value) == 1:
            return 0.5  # Acceptable match
        else:
            return 0.0  # Poor match

    @staticmethod
    def suggest_tasks_for_energy(
        tasks: List[Task],
        energy: EnergyLevel
    ) -> List[Task]:
        """Suggest tasks ranked by energy match score.

        Returns:
            Tasks sorted by match score (best first)
        """
        # Calculate match scores
        scored_tasks = [
            (task, EnergyMatchingService.match_task_to_energy(task, energy))
            for task in tasks
        ]

        # Sort by score (descending), then priority
        scored_tasks.sort(
            key=lambda x: (x[1], x[0].priority.value),
            reverse=True
        )

        return [task for task, score in scored_tasks]
```

### Time Blocking Algorithm

**TimeBlockingService** allocates tasks to time slots:

```python
class TimeBlockingService:
    """Domain service for time blocking and schedule optimization."""

    @staticmethod
    def create_time_blocks(
        tasks: List[Task],
        available_hours: int,
        start_time: Optional[datetime] = None
    ) -> List[TimeBlock]:
        """Create time blocks from task list.

        Algorithm:
        1. Sort tasks by priority + energy requirement
        2. Allocate high-energy tasks to morning blocks
        3. Allocate low-energy tasks to afternoon blocks
        4. Leave buffer time between blocks

        Args:
            tasks: Tasks to schedule
            available_hours: Hours available for work
            start_time: Starting time (default: 9 AM today)

        Returns:
            List of TimeBlock value objects with assigned tasks
        """
        blocks = []
        current_time = start_time or datetime.now().replace(hour=9, minute=0)

        # Group tasks by energy requirement
        high_energy_tasks = [t for t in tasks if t.energy_requirement == EnergyLevel.HIGH]
        medium_energy_tasks = [t for t in tasks if t.energy_requirement == EnergyLevel.MEDIUM]
        low_energy_tasks = [t for t in tasks if t.energy_requirement == EnergyLevel.LOW]

        # Allocate high-energy tasks first (morning)
        for task in high_energy_tasks:
            duration_minutes = task.estimated_duration_minutes or 60
            block = TimeBlock.create(
                start_time=current_time,
                duration_minutes=duration_minutes,
                task_id=task.id,
                energy_level=EnergyLevel.HIGH
            )
            blocks.append(block)
            current_time += timedelta(minutes=duration_minutes + 15)  # Buffer

        # Continue with medium and low energy tasks...

        return blocks

    @staticmethod
    def optimize_schedule(blocks: List[TimeBlock]) -> List[TimeBlock]:
        """Optimize time blocks to minimize context switching.

        Algorithm:
        1. Group similar tasks together
        2. Add appropriate buffer times
        3. Respect energy patterns (high→medium→low)

        Returns:
            Optimized list of time blocks
        """
        # Implementation: Sort by energy level, add buffers, group by context
        # ...
        return blocks
```

### Testing Strategy

Domain services are the **easiest to test** because they're pure functions:

```python
class TestTaskPrioritizationService:
    def test_categorize_urgent_important_task(self):
        # Arrange
        task = Task.create(
            title="Production bug fix",
            priority=Priority.P0,
            due_date=datetime.now() + timedelta(hours=2)  # Urgent (< 24h)
        )

        # Act
        category = TaskPrioritizationService.categorize_task(task)

        # Assert
        assert category == "urgent_important"

    def test_categorize_important_not_urgent_task(self):
        # Arrange
        task = Task.create(
            title="Architecture design",
            priority=Priority.P1,
            due_date=datetime.now() + timedelta(days=7)  # Not urgent
        )

        # Act
        category = TaskPrioritizationService.categorize_task(task)

        # Assert
        assert category == "important_not_urgent"

    def test_categorize_tasks_returns_all_quadrants(self):
        # Arrange
        tasks = [
            Task.create(title="Bug", priority=Priority.P0, due_date=datetime.now() + timedelta(hours=1)),
            Task.create(title="Design", priority=Priority.P1, due_date=datetime.now() + timedelta(days=7)),
            Task.create(title="Email", priority=Priority.P3, due_date=datetime.now() + timedelta(hours=2)),
            Task.create(title="Read docs", priority=Priority.P3, due_date=datetime.now() + timedelta(days=30)),
        ]

        # Act
        categories = TaskPrioritizationService.categorize_tasks(tasks)

        # Assert
        assert len(categories["urgent_important"]) == 1
        assert len(categories["important_not_urgent"]) == 1
        assert len(categories["urgent_not_important"]) == 1
        assert len(categories["neither"]) == 1


class TestEnergyMatchingService:
    def test_high_energy_matches_p0_tasks(self):
        # Arrange
        task = Task.create(title="Deep work", priority=Priority.P0)

        # Act
        score = EnergyMatchingService.match_task_to_energy(task, EnergyLevel.HIGH)

        # Assert
        assert score == 1.0  # Perfect match

    def test_suggest_tasks_for_high_energy_prioritizes_p0(self):
        # Arrange
        tasks = [
            Task.create(title="P3 task", priority=Priority.P3),
            Task.create(title="P0 task", priority=Priority.P0),
            Task.create(title="P1 task", priority=Priority.P1),
        ]

        # Act
        suggested = EnergyMatchingService.suggest_tasks_for_energy(tasks, EnergyLevel.HIGH)

        # Assert
        assert suggested[0].priority == Priority.P0
        assert suggested[1].priority == Priority.P1
        assert suggested[2].priority == Priority.P3
```

**No Mocks Needed:**
- Domain services operate on domain objects only
- Tests create real Task, Priority, EnergyLevel objects
- Pure functions → deterministic output
- Fast tests (no I/O, no network)

### Integration with Application Services

Domain services are **used by** application services (Story 6.2):

```python
# Story 6.2 - Application Service
class DailyPlanningService:
    def __init__(
        self,
        create_task_use_case: CreateTaskUseCase,
        prioritization_service: TaskPrioritizationService  # Domain service
    ):
        self.create_task = create_task_use_case
        self.prioritization = prioritization_service

    def prioritize_tasks(self) -> Dict[str, List[Task]]:
        """Orchestrate task prioritization workflow."""
        # Get tasks via use case (application layer)
        all_tasks = self.list_tasks.execute()

        # Apply domain logic via domain service
        categories = self.prioritization.categorize_tasks(all_tasks)

        # Return result for presentation layer
        return categories
```

**Layer Flow:**
1. **Presentation Layer (CLI):** User triggers "prioritize my tasks"
2. **Application Service:** DailyPlanningService.prioritize_tasks()
3. **Application Use Case:** ListTasksUseCase.execute()
4. **Domain Service:** TaskPrioritizationService.categorize_tasks()
5. **Domain Entity:** Task.is_due_soon(), task.priority
6. **Infrastructure:** JsonTaskRepository.find_all()

### Strangler Fig Migration Notes

**Phase 3 - Domain Services:**
- Creates NEW domain services in src/domain/services/
- Existing code (src/prioritization.py logic) stays untouched
- Domain services are pure functions, zero integration risk
- Application services (Story 6.2) will use these domain services
- No breaking changes to existing functionality

**Future Integration (Phase 4):**
- Refactor existing prioritization logic to use TaskPrioritizationService
- Remove old procedural functions once validated
- Domain services enable reuse across multiple workflows

### References

- [Source: docs/stories/story-5.1-domain-value-objects.md] - Priority, Status, EnergyLevel enums
- [Source: docs/stories/story-5.2-task-entity.md] - Task entity methods
- [Source: docs/stories/story-6.2-planning-services.md] - Application services that use domain services
- [Source: mission-control/CLAUDE.md#1] - Clean Architecture layers
- [Source: mission-control/CLAUDE.md#2] - Domain-Driven Design principles
- [Source: mission-control/CLAUDE.md#6] - Testing standards (90%+ coverage)
- [Source: docs/epics.md#EPIC-5R] - Phase 3: Application Services plan
- [Source: docs/stories/story-3.3-daily-planning-workflow.md] - Eisenhower Matrix usage
- [Source: src/prioritization.py] - Current prioritization logic (to be refactored)

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

### Completion Notes List

### File List
