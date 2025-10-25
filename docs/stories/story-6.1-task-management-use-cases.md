# Story 6.1: Task Management Use Cases

Status: Done

## Story

As a developer,
I want application layer use cases for task management operations,
so that business workflows can orchestrate domain logic without direct storage dependencies, following Clean Architecture principles and enabling comprehensive testing with mocked repositories.

## Acceptance Criteria

1. **Use Case Classes Created**
   - All use cases in `src/application/use_cases/task_management/` module
   - Each use case is a single-purpose class with `execute()` method
   - Use cases: CreateTaskUseCase, UpdateTaskUseCase, CompleteTaskUseCase, DeleteTaskUseCase, GetTaskByIdUseCase, ListTasksUseCase, FindTasksByStatusUseCase, FindTasksByPriorityUseCase
   - Each use case < 150 lines (CLAUDE.md Rule 3.3.1)
   - Proper module structure with `__init__.py` exports

2. **Dependency Injection Pattern**
   - All use cases accept `ITaskRepository` via constructor injection
   - No direct imports of infrastructure implementations
   - Repository stored as instance variable: `self.task_repository`
   - Enables easy testing with mock repositories
   - Follows CLAUDE.md Rule 3.1.4 (use interface, not implementation)

3. **Clean Architecture Compliance**
   - Application layer depends ONLY on domain layer
   - Zero infrastructure dependencies
   - Use cases orchestrate domain objects (Task entity, value objects)
   - No business logic in use cases (that's in domain)
   - Use cases handle transaction boundaries and orchestration only

4. **Comprehensive Error Handling**
   - Validate inputs before calling domain layer
   - Raise meaningful exceptions with context (TaskNotFoundError, InvalidTaskDataError)
   - Handle repository failures gracefully
   - Log all errors with full context before raising
   - Return proper types (Task, List[Task], bool, None)

5. **Entry/Exit Logging**
   - Every use case logs entry: `[UseCase] Executing {use_case_name}: task_id={id}`
   - Every use case logs exit: `[UseCase] Completed {use_case_name}: success={bool}`
   - Log format follows CLAUDE.md Rule 10.5.1
   - Use standard logging module (not print)
   - Tests verify log output using capsys

6. **Type Safety and Documentation**
   - Complete type hints on all methods and parameters
   - Return types specified (Task, Optional[Task], List[Task], bool)
   - Comprehensive docstrings (class-level and execute method)
   - Examples in docstrings showing usage
   - No `Any` types

7. **Comprehensive Unit Tests**
   - 20+ unit tests in `tests/application/use_cases/test_task_management.py`
   - Each use case has 2-4 tests (happy path, error cases)
   - Tests use mock ITaskRepository (in-memory implementation)
   - Test coverage >= 90% for application layer (CLAUDE.md Rule 6.1.1)
   - Tests verify logging output
   - Zero integration tests (those are for repositories, not use cases)

## Tasks / Subtasks

- [ ] Task 1: Create module structure (AC: #1)
  - [ ] Subtask 1.1: Create `src/application/` directory
  - [ ] Subtask 1.2: Create `src/application/use_cases/` directory
  - [ ] Subtask 1.3: Create `src/application/use_cases/task_management/` directory
  - [ ] Subtask 1.4: Create `src/application/use_cases/task_management/__init__.py`
  - [ ] Subtask 1.5: Create `src/application/use_cases/__init__.py`
  - [ ] Subtask 1.6: Create `src/application/__init__.py`

- [ ] Task 2: Create CreateTaskUseCase (AC: #1, #2, #3, #4, #5)
  - [ ] Subtask 2.1: Create `create_task_use_case.py`
  - [ ] Subtask 2.2: Define class with constructor injection (ITaskRepository)
  - [ ] Subtask 2.3: Implement execute(title, priority, ...) method
  - [ ] Subtask 2.4: Call Task.create() factory method
  - [ ] Subtask 2.5: Call task_repository.save(task)
  - [ ] Subtask 2.6: Add entry/exit logging
  - [ ] Subtask 2.7: Add error handling
  - [ ] Subtask 2.8: Add comprehensive docstring with example

- [ ] Task 3: Create GetTaskByIdUseCase (AC: #1, #2, #3, #4, #5)
  - [ ] Subtask 3.1: Create `get_task_by_id_use_case.py`
  - [ ] Subtask 3.2: Define class with constructor injection
  - [ ] Subtask 3.3: Implement execute(task_id: str) -> Optional[Task]
  - [ ] Subtask 3.4: Call task_repository.find_by_id()
  - [ ] Subtask 3.5: Add entry/exit logging
  - [ ] Subtask 3.6: Handle not found case (return None or raise exception)
  - [ ] Subtask 3.7: Add docstring

- [ ] Task 4: Create ListTasksUseCase (AC: #1, #2, #3, #5)
  - [ ] Subtask 4.1: Create `list_tasks_use_case.py`
  - [ ] Subtask 4.2: Implement execute() -> List[Task]
  - [ ] Subtask 4.3: Call task_repository.find_all()
  - [ ] Subtask 4.4: Add logging
  - [ ] Subtask 4.5: Add docstring

- [ ] Task 5: Create UpdateTaskUseCase (AC: #1, #2, #3, #4, #5)
  - [ ] Subtask 5.1: Create `update_task_use_case.py`
  - [ ] Subtask 5.2: Implement execute(task_id, updates: Dict[str, Any]) -> Task
  - [ ] Subtask 5.3: Load existing task from repository
  - [ ] Subtask 5.4: Apply updates to task entity (call task methods)
  - [ ] Subtask 5.5: Save updated task
  - [ ] Subtask 5.6: Add validation and error handling
  - [ ] Subtask 5.7: Add logging and docstring

- [ ] Task 6: Create CompleteTaskUseCase (AC: #1, #2, #3, #4, #5)
  - [ ] Subtask 6.1: Create `complete_task_use_case.py`
  - [ ] Subtask 6.2: Implement execute(task_id: str) -> Task
  - [ ] Subtask 6.3: Load task from repository
  - [ ] Subtask 6.4: Call task.mark_complete()
  - [ ] Subtask 6.5: Save updated task
  - [ ] Subtask 6.6: Add error handling (task not found, already complete)
  - [ ] Subtask 6.7: Add logging and docstring

- [ ] Task 7: Create DeleteTaskUseCase (AC: #1, #2, #3, #4, #5)
  - [ ] Subtask 7.1: Create `delete_task_use_case.py`
  - [ ] Subtask 7.2: Implement execute(task_id: str) -> bool
  - [ ] Subtask 7.3: Call task_repository.delete(task_id)
  - [ ] Subtask 7.4: Return success status
  - [ ] Subtask 7.5: Add logging and docstring

- [ ] Task 8: Create Query Use Cases (AC: #1, #2, #3, #5)
  - [ ] Subtask 8.1: Create `find_tasks_by_status_use_case.py`
  - [ ] Subtask 8.2: Implement execute(status: Status) -> List[Task]
  - [ ] Subtask 8.3: Create `find_tasks_by_priority_use_case.py`
  - [ ] Subtask 8.4: Implement execute(priority: Priority) -> List[Task]
  - [ ] Subtask 8.5: Add logging and docstrings

- [ ] Task 9: Configure module exports (AC: #1)
  - [ ] Subtask 9.1: Export all use cases in task_management/__init__.py
  - [ ] Subtask 9.2: Test imports work: `from src.application.use_cases.task_management import CreateTaskUseCase`
  - [ ] Subtask 9.3: Verify clean import paths

- [ ] Task 10: Write comprehensive unit tests (AC: #7)
  - [ ] Subtask 10.1: Create `tests/application/` directory
  - [ ] Subtask 10.2: Create `tests/application/use_cases/` directory
  - [ ] Subtask 10.3: Create `tests/application/use_cases/__init__.py`
  - [ ] Subtask 10.4: Create `tests/application/use_cases/test_task_management.py`
  - [ ] Subtask 10.5: Create MockTaskRepository (in-memory implementation)
  - [ ] Subtask 10.6: Write 3 tests for CreateTaskUseCase (happy path, validation error, repository error)
  - [ ] Subtask 10.7: Write 2 tests for GetTaskByIdUseCase (found, not found)
  - [ ] Subtask 10.8: Write 2 tests for ListTasksUseCase (has tasks, empty)
  - [ ] Subtask 10.9: Write 3 tests for UpdateTaskUseCase (success, not found, validation error)
  - [ ] Subtask 10.10: Write 3 tests for CompleteTaskUseCase (success, not found, already complete)
  - [ ] Subtask 10.11: Write 2 tests for DeleteTaskUseCase (success, not found)
  - [ ] Subtask 10.12: Write 2 tests for FindTasksByStatusUseCase
  - [ ] Subtask 10.13: Write 2 tests for FindTasksByPriorityUseCase
  - [ ] Subtask 10.14: Write 2 tests for logging output verification (capsys)
  - [ ] Subtask 10.15: Run coverage report, verify >= 90%

## Dev Notes

### Clean Architecture - Application Layer

This story creates the **Application Layer** (use cases) in our Hexagonal/Clean Architecture refactoring. The application layer sits between domain and infrastructure, orchestrating domain objects to fulfill business workflows.

**Key Principle from CLAUDE.md:**
> "Application layer orchestrates domain objects to fulfill use cases. It depends ONLY on domain, never on infrastructure."

**Layer Dependencies:**
```
Presentation Layer (CLI, webhooks)
         ↓
Application Layer (Use Cases) ← THIS STORY
         ↓
Domain Layer (Entities, Value Objects, Repository Interfaces)
         ↑
Infrastructure Layer (JsonTaskRepository, file I/O)
```

**What Goes in Application Layer:**
- Use case classes (single-purpose orchestration)
- Transaction boundaries
- Repository interface calls (not implementations!)
- Input validation
- Error handling and logging
- ❌ NO business logic (that's domain)
- ❌ NO storage code (that's infrastructure)

**What Goes in Domain Layer:**
- Business logic (Task.mark_complete(), Task.is_overdue())
- Entities and value objects
- Domain services (TaskPrioritizer, WorkflowEngine)
- Repository interfaces (abstract only)

### Use Case Pattern

**Structure:**
```python
from src.domain.repositories import ITaskRepository
from src.domain.entities import Task
from src.domain.value_objects import Priority
import logging

logger = logging.getLogger(__name__)

class CreateTaskUseCase:
    """Use case for creating a new task.

    This use case orchestrates the creation of a Task entity
    and persists it using the task repository.

    Example:
        >>> repo = JsonTaskRepository("data/tasks.json")
        >>> use_case = CreateTaskUseCase(repo)
        >>> task = use_case.execute(title="Review PR", priority=Priority.HIGH)
    """

    def __init__(self, task_repository: ITaskRepository):
        """Initialize use case with repository dependency.

        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository

    def execute(self, title: str, priority: Priority, **kwargs) -> Task:
        """Create and save a new task.

        Args:
            title: Task title (min 3 chars)
            priority: Task priority level
            **kwargs: Optional task fields (description, due_date, etc.)

        Returns:
            Created Task entity

        Raises:
            ValueError: If title is invalid
            RepositoryError: If save fails
        """
        logger.info(f"[CreateTaskUseCase] Executing: title='{title}', priority={priority.name}")

        try:
            # Validate inputs
            if not title or len(title) < 3:
                raise ValueError("Title must be at least 3 characters")

            # Create domain entity (business logic in domain)
            task = Task.create(title=title, priority=priority, **kwargs)

            # Persist via repository
            self.task_repository.save(task)

            logger.info(f"[CreateTaskUseCase] Completed: task_id={task.id}, success=True")
            return task

        except Exception as e:
            logger.error(f"[CreateTaskUseCase] Failed: error={str(e)}")
            raise
```

**Key Patterns:**
1. **Constructor Injection:** Accept ITaskRepository (interface, not implementation)
2. **Single Responsibility:** One use case = one action
3. **Domain Orchestration:** Call domain methods (Task.create, task.mark_complete)
4. **Repository Calls:** Use interface methods (save, find_by_id, etc.)
5. **Entry/Exit Logging:** Log start and completion
6. **Error Handling:** Validate, catch, log, raise with context

### Testing Strategy

**Unit Tests Only (No Integration Tests):**

Use cases are tested with **mock repositories** (in-memory implementation), not real file I/O. This makes tests fast, isolated, and focused on use case logic.

**Mock Repository Example:**
```python
class MockTaskRepository(ITaskRepository):
    """In-memory mock for testing"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self.tasks[task.id] = task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def find_all(self) -> List[Task]:
        return list(self.tasks.values())

    def find_by_status(self, status: Status) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == status]

    def find_by_priority(self, priority: Priority) -> List[Task]:
        return [t for t in self.tasks.values() if t.priority == priority]

    def delete(self, task_id: str) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def exists(self, task_id: str) -> bool:
        return task_id in self.tasks
```

**Test Structure (20+ tests):**
```python
class TestCreateTaskUseCase:
    def test_create_task_with_valid_data(self):
        # Arrange
        repo = MockTaskRepository()
        use_case = CreateTaskUseCase(repo)

        # Act
        task = use_case.execute(title="Test Task", priority=Priority.HIGH)

        # Assert
        assert task.title == "Test Task"
        assert task.priority == Priority.HIGH
        assert repo.exists(task.id)

    def test_create_task_with_invalid_title_raises_error(self):
        # Arrange
        repo = MockTaskRepository()
        use_case = CreateTaskUseCase(repo)

        # Act & Assert
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            use_case.execute(title="", priority=Priority.LOW)

    def test_create_task_logs_entry_and_exit(self, capsys):
        # Arrange
        repo = MockTaskRepository()
        use_case = CreateTaskUseCase(repo)

        # Act
        use_case.execute(title="Test Task", priority=Priority.HIGH)

        # Assert
        captured = capsys.readouterr()
        assert "[CreateTaskUseCase] Executing" in captured.out
        assert "[CreateTaskUseCase] Completed" in captured.out
```

**Coverage Target:** >= 90% (CLAUDE.md Rule 6.1.1)

### Directory Structure After This Story

```
mission-control/
├── src/
│   ├── domain/                     # From Stories 5.1, 5.2, 5.3
│   │   ├── entities/
│   │   │   └── task.py
│   │   ├── value_objects/
│   │   │   ├── priority.py
│   │   │   ├── status.py
│   │   │   ├── energy_level.py
│   │   │   ├── context.py
│   │   │   └── time_block.py
│   │   └── repositories/
│   │       ├── task_repository.py
│   │       └── memory_repository.py
│   │
│   └── application/                # NEW - This story
│       ├── __init__.py
│       └── use_cases/
│           ├── __init__.py
│           └── task_management/
│               ├── __init__.py
│               ├── create_task_use_case.py
│               ├── get_task_by_id_use_case.py
│               ├── list_tasks_use_case.py
│               ├── update_task_use_case.py
│               ├── complete_task_use_case.py
│               ├── delete_task_use_case.py
│               ├── find_tasks_by_status_use_case.py
│               └── find_tasks_by_priority_use_case.py
│
└── tests/
    ├── domain/                     # Existing (69 tests passing)
    │   ├── entities/
    │   └── repositories/
    │
    └── application/                # NEW - This story
        ├── __init__.py
        └── use_cases/
            ├── __init__.py
            └── test_task_management.py (20+ tests)
```

### Use Cases to Implement (8 total)

1. **CreateTaskUseCase** - Create new task
   - execute(title, priority, **kwargs) -> Task
   - Calls: Task.create(), repo.save()

2. **GetTaskByIdUseCase** - Retrieve single task
   - execute(task_id: str) -> Optional[Task]
   - Calls: repo.find_by_id()

3. **ListTasksUseCase** - Retrieve all tasks
   - execute() -> List[Task]
   - Calls: repo.find_all()

4. **UpdateTaskUseCase** - Update task fields
   - execute(task_id: str, updates: Dict[str, Any]) -> Task
   - Calls: repo.find_by_id(), task.update_*(), repo.save()

5. **CompleteTaskUseCase** - Mark task complete
   - execute(task_id: str) -> Task
   - Calls: repo.find_by_id(), task.mark_complete(), repo.save()

6. **DeleteTaskUseCase** - Remove task
   - execute(task_id: str) -> bool
   - Calls: repo.delete()

7. **FindTasksByStatusUseCase** - Query by status
   - execute(status: Status) -> List[Task]
   - Calls: repo.find_by_status()

8. **FindTasksByPriorityUseCase** - Query by priority
   - execute(priority: Priority) -> List[Task]
   - Calls: repo.find_by_priority()

### Strangler Fig Migration Notes

**No Breaking Changes:**
- Creates NEW application layer use cases
- Does NOT modify existing code (src/tasks.py, workflows)
- Existing 69 domain tests continue passing
- Use cases tested independently with mock repository
- Real repository implementations come in Phase 2 (Stories 5.4-5.6)

**Future Integration (Story 6.2 - Planning Services):**
- Planning services will use these use cases
- Example: DailyPlanningService will call CreateTaskUseCase, ListTasksUseCase
- Enables clean separation: Services orchestrate use cases, use cases orchestrate domain

### References

- [Source: mission-control/CLAUDE.md#1] - Hexagonal/Clean Architecture layers
- [Source: mission-control/CLAUDE.md#3] - Repository Pattern and Dependency Injection
- [Source: mission-control/CLAUDE.md#6] - Testing standards (90%+ domain/application coverage)
- [Source: mission-control/CLAUDE.md#7] - Design Patterns (Use Case pattern)
- [Source: mission-control/CLAUDE.md#10] - Logging standards (entry/exit logging)
- [Source: docs/stories/story-5.1-domain-value-objects.md] - Value objects (Priority, Status)
- [Source: docs/stories/story-5.2-task-entity.md] - Task entity
- [Source: docs/stories/story-5.3-repository-interfaces.md] - ITaskRepository interface
- [Source: docs/epics.md#EPIC-5R] - Phase 3: Application Services plan
- [Source: docs/PRD.md] - Task management requirements

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

### Completion Notes List

### File List
