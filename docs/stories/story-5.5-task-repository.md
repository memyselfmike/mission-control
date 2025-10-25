# Story 5.5: Implement Task Repository

Status: Draft

## Story

As a developer,
I want a concrete JsonTaskRepository implementing ITaskRepository from Story 5.3,
so that Task entities can be persisted to/from JSON files following the repository pattern with proper serialization/deserialization and all CRUD operations.

## Acceptance Criteria

1. **JsonTaskRepository Class Created**
   - Implements ITaskRepository interface from Story 5.3
   - Located in `src/infrastructure/persistence/repositories/task_repository_json.py`
   - Constructor accepts storage path parameter
   - Uses JsonStorage utility from Story 5.4 for all file I/O
   - Zero domain logic (pure infrastructure concern)

2. **Task Serialization/Deserialization**
   - Implement `_task_to_dict(task: Task) -> Dict[str, Any]` method
   - Converts Task entity → JSON-serializable dictionary
   - Handles all 18 Task fields including optional ones
   - Converts value objects (Priority, Status, EnergyLevel) to string representations
   - Converts datetime fields to ISO format strings
   - Implement `_dict_to_task(data: Dict[str, Any]) -> Task` method
   - Converts dictionary → Task entity
   - Reconstructs value objects from strings
   - Parses ISO datetime strings back to datetime objects
   - Handles missing optional fields gracefully

3. **CRUD Operations Implemented**
   - `save(task: Task) -> None` - Save task to storage (create or update)
   - `find_by_id(task_id: str) -> Optional[Task]` - Retrieve single task by ID
   - `find_all() -> List[Task]` - Retrieve all tasks
   - `find_by_status(status: Status) -> List[Task]` - Query by status
   - `find_by_priority(priority: Priority) -> List[Task]` - Query by priority
   - `delete(task_id: str) -> bool` - Remove task, return True if deleted
   - `exists(task_id: str) -> bool` - Check existence, return True if exists

4. **Error Handling & Validation**
   - Handle missing storage file gracefully (returns None or empty list)
   - Handle corrupted JSON (log error, raise exception)
   - Handle invalid task data during deserialization (validation errors)
   - Handle file permission errors (raise StoragePermissionError)
   - All errors logged with context before raising

5. **Storage Format**
   - JSON file structure: `{task_id: {task_data}, ...}` (dictionary keyed by task ID)
   - Pretty-printed JSON (indent=2) for readability
   - Atomic writes via JsonStorage utility (temp file → rename)
   - Automatic backups on write (via JsonStorage)

6. **Zero Domain Dependencies**
   - Infrastructure layer implementation
   - Depends ONLY on domain interfaces (ITaskRepository, Task, value objects)
   - No business logic in repository
   - Pure storage operations

7. **Comprehensive Tests (20+ tests)**
   - Unit tests in `tests/infrastructure/persistence/repositories/test_task_repository_json.py`
   - Test all 7 CRUD methods (save, find_by_id, find_all, find_by_status, find_by_priority, delete, exists)
   - Test serialization/deserialization round-trip (Task → dict → Task)
   - Test error cases (missing file, corrupted JSON, invalid data, permission errors)
   - Test edge cases (empty storage, task with all optional fields None, task with all fields populated)
   - Test query operations return correct results
   - Integration tests using tmp_path fixture (real file I/O)
   - 100% coverage for repository implementation

## Tasks / Subtasks

- [ ] Task 1: Create repository module structure (AC: #1)
  - [ ] Subtask 1.1: Create `src/infrastructure/persistence/repositories/` directory if not exists
  - [ ] Subtask 1.2: Create `task_repository_json.py` file
  - [ ] Subtask 1.3: Create `__init__.py` and export JsonTaskRepository

- [ ] Task 2: Implement JsonTaskRepository class (AC: #1, #2, #3)
  - [ ] Subtask 2.1: Define class implementing ITaskRepository
  - [ ] Subtask 2.2: Add constructor with storage_path parameter
  - [ ] Subtask 2.3: Initialize JsonStorage utility
  - [ ] Subtask 2.4: Add type hints for all methods

- [ ] Task 3: Implement serialization methods (AC: #2)
  - [ ] Subtask 3.1: Implement `_task_to_dict()` - convert Task → dict
  - [ ] Subtask 3.2: Handle value object → string conversion (Priority, Status, EnergyLevel)
  - [ ] Subtask 3.3: Handle datetime → ISO string conversion
  - [ ] Subtask 3.4: Handle optional fields (None values)
  - [ ] Subtask 3.5: Implement `_dict_to_task()` - convert dict → Task
  - [ ] Subtask 3.6: Handle string → value object reconstruction
  - [ ] Subtask 3.7: Handle ISO string → datetime parsing
  - [ ] Subtask 3.8: Handle missing optional fields

- [ ] Task 4: Implement save() method (AC: #3, #5)
  - [ ] Subtask 4.1: Load existing tasks from storage
  - [ ] Subtask 4.2: Convert task to dict using `_task_to_dict()`
  - [ ] Subtask 4.3: Update tasks dictionary with new task
  - [ ] Subtask 4.4: Write updated dictionary to storage using JsonStorage
  - [ ] Subtask 4.5: Log save operation with context

- [ ] Task 5: Implement find methods (AC: #3)
  - [ ] Subtask 5.1: Implement `find_by_id()` - return single task or None
  - [ ] Subtask 5.2: Implement `find_all()` - return all tasks as list
  - [ ] Subtask 5.3: Implement `find_by_status()` - filter by status
  - [ ] Subtask 5.4: Implement `find_by_priority()` - filter by priority
  - [ ] Subtask 5.5: Handle empty storage gracefully

- [ ] Task 6: Implement delete() and exists() methods (AC: #3)
  - [ ] Subtask 6.1: Implement `delete()` - remove task, return success boolean
  - [ ] Subtask 6.2: Implement `exists()` - check existence, return boolean
  - [ ] Subtask 6.3: Log delete operations with context

- [ ] Task 7: Implement error handling (AC: #4)
  - [ ] Subtask 7.1: Handle missing storage file (return None/empty list)
  - [ ] Subtask 7.2: Handle corrupted JSON (log and raise InvalidJsonError)
  - [ ] Subtask 7.3: Handle invalid task data (validation errors)
  - [ ] Subtask 7.4: Handle permission errors (raise StoragePermissionError)
  - [ ] Subtask 7.5: Log all errors with full context before raising

- [ ] Task 8: Write comprehensive tests (AC: #7)
  - [ ] Subtask 8.1: Create test file `tests/infrastructure/persistence/repositories/test_task_repository_json.py`
  - [ ] Subtask 8.2: Test save() - create new task
  - [ ] Subtask 8.3: Test save() - update existing task
  - [ ] Subtask 8.4: Test find_by_id() - found and not found
  - [ ] Subtask 8.5: Test find_all() - empty and populated
  - [ ] Subtask 8.6: Test find_by_status() - matching and no matches
  - [ ] Subtask 8.7: Test find_by_priority() - matching and no matches
  - [ ] Subtask 8.8: Test delete() - success and not found
  - [ ] Subtask 8.9: Test exists() - true and false
  - [ ] Subtask 8.10: Test serialization round-trip (Task → dict → Task equals original)
  - [ ] Subtask 8.11: Test error cases (missing file, corrupted JSON, invalid data, permissions)
  - [ ] Subtask 8.12: Test edge cases (all optional fields None, all fields populated)
  - [ ] Subtask 8.13: Run coverage report, verify 100% for repository
  - [ ] Subtask 8.14: Run all tests, verify no regressions

## Dev Notes

### Architecture Alignment (Hexagonal/Clean Architecture)

This story implements the **infrastructure layer** of the repository pattern, completing the persistence concern for Task entities.

**Layer Separation:**
```
Domain Layer (Story 5.3):
  - ITaskRepository interface (abstract contract)
  - Task entity (business logic)
  - Value objects (Priority, Status, EnergyLevel)

Infrastructure Layer (THIS STORY):
  - JsonTaskRepository (concrete implementation)
  - Serialization/deserialization logic
  - File I/O via JsonStorage utility
```

**Key Principle from CLAUDE.md:**
> "Repository implementations belong in the infrastructure layer. They implement domain interfaces but contain zero business logic."

**Dependency Flow:**
```
JsonTaskRepository (infrastructure)
  ↓ implements
ITaskRepository (domain interface)
  ↓ uses
Task entity + value objects (domain)
  ↓ uses
JsonStorage (infrastructure utility from Story 5.4)
```

### Implementation Patterns

**Serialization Strategy:**

Convert Task entity to/from dictionary representation for JSON storage.

**Task → Dict (Serialization):**
```python
def _task_to_dict(self, task: Task) -> Dict[str, Any]:
    """Convert Task entity to JSON-serializable dictionary"""
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status.value,  # Enum → string
        "priority": task.priority.value,  # Enum → string
        "energy_required": task.energy_required.value if task.energy_required else None,
        "estimated_time_minutes": task.estimated_time_minutes,
        "actual_time_minutes": task.actual_time_minutes,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "defer_until": task.defer_until.isoformat() if task.defer_until else None,
        "completed_date": task.completed_date.isoformat() if task.completed_date else None,
        "blocked_reason": task.blocked_reason,
        "tags": task.tags,
        "context_id": task.context_id,
        "dependencies": task.dependencies,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "version": task.version,
    }
```

**Dict → Task (Deserialization):**
```python
def _dict_to_task(self, data: Dict[str, Any]) -> Task:
    """Convert dictionary to Task entity"""
    from datetime import datetime
    from ...domain.entities.task import Task
    from ...domain.value_objects import Priority, Status, EnergyLevel

    return Task(
        id=data["id"],
        title=data["title"],
        description=data.get("description"),
        status=Status(data["status"]),  # String → Enum
        priority=Priority(data["priority"]),  # String → Enum
        energy_required=EnergyLevel(data["energy_required"]) if data.get("energy_required") else None,
        estimated_time_minutes=data.get("estimated_time_minutes"),
        actual_time_minutes=data.get("actual_time_minutes"),
        due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
        defer_until=datetime.fromisoformat(data["defer_until"]) if data.get("defer_until") else None,
        completed_date=datetime.fromisoformat(data["completed_date"]) if data.get("completed_date") else None,
        blocked_reason=data.get("blocked_reason"),
        tags=data.get("tags", []),
        context_id=data.get("context_id"),
        dependencies=data.get("dependencies", []),
        created_at=datetime.fromisoformat(data["created_at"]),
        updated_at=datetime.fromisoformat(data["updated_at"]),
        version=data.get("version", 1),
    )
```

**Storage Structure:**

JSON file: `data/tasks.json`
```json
{
  "T-20251025-001": {
    "id": "T-20251025-001",
    "title": "Review architecture docs",
    "description": "Review and approve solution-architecture.md",
    "status": "IN_PROGRESS",
    "priority": "P1",
    "energy_required": "MEDIUM",
    "estimated_time_minutes": 60,
    "actual_time_minutes": null,
    "due_date": "2025-10-26T17:00:00",
    "defer_until": null,
    "completed_date": null,
    "blocked_reason": null,
    "tags": ["architecture", "documentation"],
    "context_id": "EPIC-5R",
    "dependencies": [],
    "created_at": "2025-10-25T10:00:00",
    "updated_at": "2025-10-25T10:30:00",
    "version": 1
  }
}
```

### Query Implementation Patterns

**Find by status:**
```python
def find_by_status(self, status: Status) -> List[Task]:
    """Query tasks by status"""
    all_tasks = self.find_all()
    return [task for task in all_tasks if task.status == status]
```

**Find by priority:**
```python
def find_by_priority(self, priority: Priority) -> List[Task]:
    """Query tasks by priority"""
    all_tasks = self.find_all()
    return [task for task in all_tasks if task.priority == priority]
```

### Testing Strategy

**Unit Tests (20+ tests, target: 100% coverage):**

1. **CRUD Operations (10 tests):**
   - test_save_creates_new_task
   - test_save_updates_existing_task
   - test_find_by_id_returns_task_when_found
   - test_find_by_id_returns_none_when_not_found
   - test_find_all_returns_all_tasks
   - test_find_all_returns_empty_list_when_no_tasks
   - test_delete_removes_task_and_returns_true
   - test_delete_returns_false_when_task_not_found
   - test_exists_returns_true_when_task_exists
   - test_exists_returns_false_when_task_not_exists

2. **Query Operations (4 tests):**
   - test_find_by_status_returns_matching_tasks
   - test_find_by_status_returns_empty_list_when_no_matches
   - test_find_by_priority_returns_matching_tasks
   - test_find_by_priority_returns_empty_list_when_no_matches

3. **Serialization (2 tests):**
   - test_serialization_round_trip_preserves_all_fields
   - test_serialization_handles_optional_fields_none

4. **Error Cases (4 tests):**
   - test_find_by_id_handles_missing_file
   - test_find_by_id_raises_error_on_corrupted_json
   - test_save_raises_error_on_permission_denied
   - test_dict_to_task_raises_error_on_invalid_data

**Test Example:**
```python
def test_save_and_find_by_id(tmp_path):
    # Arrange
    storage_path = tmp_path / "tasks.json"
    repo = JsonTaskRepository(storage_path)
    task = Task.create(
        title="Test task",
        priority=Priority.P1,
        estimated_time_minutes=60
    )

    # Act
    repo.save(task)
    retrieved = repo.find_by_id(task.id)

    # Assert
    assert retrieved is not None
    assert retrieved.id == task.id
    assert retrieved.title == task.title
    assert retrieved.priority == task.priority
    assert retrieved.estimated_time_minutes == 60
```

### Project Structure Notes

**Directory After This Story:**
```
mission-control/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   │   └── task.py              # From Story 5.2
│   │   ├── value_objects/           # From Story 5.1
│   │   │   ├── priority.py
│   │   │   ├── status.py
│   │   │   └── energy_level.py
│   │   └── repositories/            # From Story 5.3
│   │       ├── __init__.py
│   │       └── task_repository.py   # ITaskRepository interface
│   │
│   └── infrastructure/
│       └── persistence/
│           ├── json_storage.py      # From Story 5.4
│           ├── exceptions.py        # From Story 5.4
│           └── repositories/        # NEW - This story
│               ├── __init__.py
│               └── task_repository_json.py  # JsonTaskRepository
│
└── tests/
    └── infrastructure/
        └── persistence/
            └── repositories/
                ├── __init__.py
                └── test_task_repository_json.py  # 20+ tests
```

**Alignment with CLAUDE.md Engineering Rules:**
- ✅ Repository implementation in infrastructure layer
- ✅ Implements domain interface (ITaskRepository)
- ✅ Zero business logic (pure storage operations)
- ✅ Uses JsonStorage utility for file I/O
- ✅ Proper error handling and logging
- ✅ Complete type hints throughout
- ✅ File < 400 lines (target: 200-300 lines)

### References

- [Source: mission-control/CLAUDE.md#3] - Repository pattern implementation rules
- [Source: docs/stories/story-5.3-repository-interfaces.md] - ITaskRepository interface contract
- [Source: docs/stories/story-5.2-task-entity.md] - Task entity structure and fields
- [Source: docs/stories/story-5.1-domain-value-objects.md] - Value objects (Priority, Status, EnergyLevel)
- [Source: docs/stories/story-5.4-json-storage-utility.md] - JsonStorage utility API
- [Source: docs/epics.md#EPIC-5R] - Phase 2: Infrastructure plan

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

### Completion Notes List

### File List
