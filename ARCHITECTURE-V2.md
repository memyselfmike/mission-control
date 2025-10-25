# Mission Control - Hexagonal Architecture Documentation

**Project:** Mission Control
**Version:** 2.0 (Post-EPIC-5R Refactoring)
**Last Updated:** 2025-10-25
**Author:** Mission Control Dev Team
**Status:** CANONICAL

---

## Table of Contents

1. [Overview](#overview)
2. [Hexagonal Architecture Principles](#hexagonal-architecture-principles)
3. [Layer Descriptions](#layer-descriptions)
4. [Dependency Rules](#dependency-rules)
5. [Current State](#current-state)
6. [Domain Layer Documentation](#domain-layer-documentation)
7. [Repository Pattern](#repository-pattern)
8. [Migration Guide](#migration-guide)
9. [Feature Flag System](#feature-flag-system)
10. [Architecture Decision Records](#architecture-decision-records)

---

## Overview

Mission Control implements **Hexagonal Architecture** (also known as Ports & Adapters or Clean Architecture) to achieve:

- **Testability**: Pure domain logic isolated from external concerns
- **Flexibility**: Easy to swap implementations (JSON → Database)
- **Maintainability**: Clear boundaries and dependencies
- **Scalability**: Add new features without touching core domain

### Why Hexagonal Architecture?

After Sprint 4, architectural debt accumulated:
- `memory.py` god object (1,500 lines)
- Procedural functions operating on dicts
- Tight coupling between business logic and file I/O
- No OOP, no encapsulation, no testability

**EPIC-5R** was created to refactor the codebase to Hexagonal Architecture, establishing a solid foundation for future development.

---

## Hexagonal Architecture Principles

### Core Concept

The application is structured as concentric layers with **dependencies flowing inward**:

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                    │
│          (CLI Commands, Formatters, UI)                 │
│  Depends on: Application Layer                          │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                 APPLICATION LAYER                       │
│       (Use Cases, Services, Orchestration)              │
│  Depends on: Domain Layer                               │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                   DOMAIN LAYER                          │
│   (Entities, Value Objects, Domain Services)            │
│  Depends on: NOTHING (Pure Business Logic)              │
└─────────────────────────────────────────────────────────┘
                   ▲
┌──────────────────┴──────────────────────────────────────┐
│               INFRASTRUCTURE LAYER                      │
│    (Repositories, File I/O, External APIs)              │
│  Depends on: Domain Layer (implements interfaces)       │
└─────────────────────────────────────────────────────────┘
```

### Key Benefits

1. **Testability**: Domain logic tested without file I/O or external dependencies
2. **Flexibility**: Swap JSON storage for database without touching domain
3. **Clarity**: Each layer has single responsibility
4. **Maintainability**: Changes isolated to appropriate layer
5. **Evolution**: Easy to add new features following established patterns

---

## Layer Descriptions

### Domain Layer (src/domain/)

**Purpose:** Pure business logic with ZERO external dependencies

**Contains:**
- **Entities** (`entities/`): Objects with identity and lifecycle (Task, Workflow)
- **Value Objects** (`value_objects/`): Immutable values (Priority, Status, TimeBlock)
- **Domain Services** (`services/`): Business logic spanning multiple entities
- **Repository Interfaces** (`repositories/`): Abstract contracts for persistence
- **Domain Events** (`events/`): Business events (TaskCreated, TaskCompleted)

**Rules:**
- ❌ NO imports from application, infrastructure, or presentation
- ❌ NO file I/O, NO database calls, NO HTTP requests
- ❌ NO external libraries except Python stdlib and typing
- ✅ Pure functions and methods
- ✅ All business rules live here

**Example:**
```python
# src/domain/entities/task.py
class Task:
    """Domain entity representing a task"""

    def __init__(self, id: str, title: str, status: Status, priority: Priority):
        self.id = id
        self.title = title
        self.status = status
        self.priority = priority

    def mark_complete(self) -> None:
        """Business logic: Mark task as complete"""
        if self.status == Status.DONE:
            raise ValueError("Task already complete")
        self.status = Status.DONE
        self.completed_date = datetime.now()

    def is_overdue(self) -> bool:
        """Business logic: Check if task is overdue"""
        if not self.due_date or self.status == Status.DONE:
            return False
        return datetime.now() > self.due_date
```

### Application Layer (src/application/)

**Purpose:** Orchestrate domain objects to fulfill use cases

**Contains:**
- **Use Cases** (`use_cases/`): Single-purpose application operations
- **Services** (`services/`): Application-level orchestration
- **DTOs** (`dtos/`): Data Transfer Objects for inter-layer communication

**Rules:**
- ✅ Can import from domain layer
- ❌ Cannot import from infrastructure or presentation
- ✅ Uses repository interfaces (not implementations)
- ✅ Orchestrates transactions
- ❌ NO business logic (belongs in domain)
- ❌ NO direct file I/O (use repositories)

**Example:**
```python
# src/application/task_management/complete_task_use_case.py
class CompleteTaskUseCase:
    """Use case for completing a task"""

    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: str) -> Task:
        """Complete a task by ID"""
        # Fetch from repository
        task = self.task_repository.find_by_id(task_id)

        if not task:
            raise ValueError(f"Task {task_id} not found")

        # Domain logic
        task.mark_complete()

        # Persist
        self.task_repository.save(task)

        return task
```

### Infrastructure Layer (src/infrastructure/)

**Purpose:** Implement technical concerns (file I/O, databases, external APIs)

**Contains:**
- **Persistence** (`persistence/`): Repository implementations, storage utilities
- **External Services** (`external/`): API clients, integrations
- **Events** (`events/`): Event dispatching, handling

**Rules:**
- ✅ Implements domain interfaces
- ✅ Can import from domain layer
- ❌ Cannot import from application or presentation
- ✅ Handles all file I/O and external calls
- ❌ NO business logic

**Example:**
```python
# src/infrastructure/persistence/repositories/json_task_repository.py
class JsonTaskRepository(ITaskRepository):
    """JSON file-based implementation of ITaskRepository"""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path

    def save(self, task: Task) -> None:
        """Save task to JSON file"""
        tasks_data = JsonStorage.read_json(self.storage_path) or {}
        tasks_data[task.id] = task.to_dict()
        JsonStorage.write_json(self.storage_path, tasks_data)

    def find_by_id(self, task_id: str) -> Optional[Task]:
        """Find task by ID from JSON file"""
        tasks_data = JsonStorage.read_json(self.storage_path)
        if not tasks_data or task_id not in tasks_data:
            return None
        return Task.from_dict(tasks_data[task_id])
```

### Presentation Layer (src/presentation/)

**Purpose:** Handle user interaction and display formatting

**Contains:**
- **CLI Commands** (`cli/`): Command-line interface commands
- **Formatters** (`formatters/`): Rich CLI output formatting
- **Input Handlers** (`handlers/`): User input validation and parsing

**Rules:**
- ✅ Can import from application and domain
- ❌ Should NOT import from infrastructure (use DI)
- ✅ Handles display formatting
- ✅ Validates user input
- ❌ NO business logic
- ❌ NO direct storage access

**Example:**
```python
# src/presentation/cli/commands.py
def daily_planning_command(
    planning_service: DailyPlanningService,
    formatter: PlanningFormatter
) -> None:
    """Execute daily planning workflow"""
    # Get user input
    energy_level = prompt_for_energy_level()

    # Call application service
    plan = planning_service.create_daily_plan(energy_level)

    # Format and display
    output = formatter.format_daily_plan(plan)
    console.print(output)
```

---

## Dependency Rules

### The Iron Law: Dependencies Flow Inward

```
Presentation → Application → Domain
Infrastructure → Domain (implements interfaces)
```

### Allowed Dependencies

✅ **Presentation** can import:
  - Application (use cases, services)
  - Domain (entities, value objects)

✅ **Application** can import:
  - Domain (entities, value objects, repository interfaces)

✅ **Infrastructure** can import:
  - Domain (to implement interfaces)

✅ **Domain** can import:
  - NOTHING (except Python stdlib and typing)

### Forbidden Dependencies

❌ **Domain** CANNOT import:
  - Application, Infrastructure, Presentation

❌ **Application** CANNOT import:
  - Infrastructure, Presentation

❌ **Infrastructure** CANNOT import:
  - Application, Presentation

---

## Current State

### Implemented (EPIC-5R Complete)

**Phase 1: Foundation (Stories 5.1-5.3)**
- ✅ Domain value objects (Priority, Status, EnergyLevel, Context, TimeBlock)
- ✅ Task entity with encapsulated behavior
- ✅ Repository interfaces (ITaskRepository, IMemoryRepository, IEventRepository, INotificationRepository, ICoordinationRepository)

**Phase 2: Infrastructure (Stories 5.4-5.7)**
- ✅ JsonStorage utility for file I/O
- ✅ TaskRepository implementation (JsonTaskRepository)
- ✅ MemoryRepository implementation (JsonMemoryRepository)
- ✅ EventRepository implementation (JsonEventRepository)
- ✅ NotificationRepository implementation (JsonNotificationRepository)
- ✅ CoordinationRepository implementation (JsonCoordinationRepository)

**Phase 3: Application (Stories 6.1-6.3)**
- ✅ DailyPlanningService
- ✅ BriefingService
- ✅ WrapupService

**Phase 4: Presentation (Stories 6.4-6.5)**
- ✅ Formatters (TaskFormatter, PlanningFormatter, BriefingFormatter, StatusFormatter)
- ✅ CLI entry point refactored
- ✅ Feature flag system (USE_NEW_ARCHITECTURE)

**Phase 5: Events & Coordination (Stories 7.1-7.3)**
- ✅ Event system refactored
- ✅ Notification system refactored
- ✅ Agent coordination refactored

**Phase 6: Testing & Documentation (Stories 8.1-8.3)**
- ✅ Domain unit tests (171 tests, 90%+ coverage)
- ✅ Infrastructure integration tests (108+ tests, 85%+ coverage)
- ✅ Architecture documentation (this document)

### Legacy Code Remaining

Using **Strangler Fig** pattern to migrate gradually:

- `src/memory.py` (1,500 lines) - Wrapped by JsonMemoryRepository
- `src/workflows.py` - To be refactored in EPIC-3 Part 2
- `src/morning_briefing.py` - Wrapped by BriefingService
- `src/eod_wrapup.py` - Wrapped by WrapupService
- `src/prioritization.py` - To be refactored to domain services

**Strategy:** Feature flag (`USE_NEW_ARCHITECTURE`) controls routing between old and new implementations.

---

## Domain Layer Documentation

### Value Objects

#### Priority
```python
class Priority(Enum):
    P0_CRITICAL = 0      # Must be done today
    P1_HIGH = 1          # Important, high priority
    P2_MEDIUM = 2        # Should do when possible
    P3_LOW = 3           # Nice to have

    def is_high_priority(self) -> bool:
        return self in [Priority.P0_CRITICAL, Priority.P1_HIGH]
```

#### Status
```python
class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    DEFERRED = "deferred"

    def is_actionable(self) -> bool:
        return self in [Status.TODO, Status.IN_PROGRESS]
```

#### EnergyLevel
```python
class EnergyLevel(Enum):
    HIGH = "high"      # Peak mental energy
    MEDIUM = "medium"  # Moderate energy
    LOW = "low"        # Low energy, routine tasks only

    def matches_priority(self, priority: Priority) -> float:
        """Calculate match score (0.0-1.0) between energy and priority"""
        # HIGH energy perfect for P0/P1
        # MEDIUM energy good for P1/P2
        # LOW energy best for P2/P3
```

#### Context
```python
@dataclass(frozen=True)
class Context:
    """Immutable context value object"""
    category: str
    subcategory: str
    tags: Tuple[str, ...]
    metadata: Tuple[Tuple[str, Any], ...]
```

#### TimeBlock
```python
@dataclass(frozen=True)
class TimeBlock:
    """Immutable time block value object"""
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    task_id: str
    description: str
```

### Entities

#### Task
```python
class Task:
    """Domain entity representing a task with encapsulated behavior"""

    # Fields
    id: str
    title: str
    description: str
    status: Status
    priority: Priority
    energy_required: EnergyLevel
    estimated_time_minutes: Optional[int]
    due_date: Optional[datetime]
    created_date: datetime
    completed_date: Optional[datetime]

    # Factory Methods
    @classmethod
    def create(cls, title: str, priority: Priority, **kwargs) -> 'Task':
        """Create a new task with generated ID"""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """Deserialize task from dict"""

    # Behavior Methods
    def mark_complete(self) -> None:
        """Mark task as completed"""

    def mark_blocked(self, reason: str) -> None:
        """Mark task as blocked"""

    def defer_until(self, new_due_date: datetime) -> None:
        """Defer task to new due date"""

    def is_overdue(self) -> bool:
        """Check if task is overdue"""

    def is_high_priority(self) -> bool:
        """Check if task is high priority (P0/P1)"""

    # Serialization
    def to_dict(self) -> Dict[str, Any]:
        """Serialize task to dict"""
```

### Domain Services

#### TaskPrioritizationService
```python
class TaskPrioritizationService:
    """Domain service for task prioritization logic"""

    @staticmethod
    def categorize_tasks(tasks: List[Task]) -> Dict[str, List[Task]]:
        """Categorize tasks by Eisenhower Matrix (urgent/important)"""

    @staticmethod
    def get_next_action(
        tasks: List[Task],
        current_energy: EnergyLevel,
        available_time: int
    ) -> Optional[Task]:
        """Get next recommended task based on energy and time"""
```

#### EnergyMatchingService
```python
class EnergyMatchingService:
    """Domain service for matching tasks to energy levels"""

    @staticmethod
    def calculate_match_score(
        task_priority: Priority,
        current_energy: EnergyLevel
    ) -> float:
        """Calculate how well a task matches current energy (0.0-1.0)"""

    @staticmethod
    def suggest_tasks_for_energy(
        tasks: List[Task],
        energy_level: EnergyLevel
    ) -> List[Task]:
        """Suggest tasks sorted by energy match score"""
```

#### TimeBlockingService
```python
class TimeBlockingService:
    """Domain service for time blocking logic"""

    @staticmethod
    def create_time_blocks(
        tasks: List[Task],
        start_time: datetime,
        available_hours: int
    ) -> List[TimeBlock]:
        """Create time blocks for tasks"""

    @staticmethod
    def optimize_schedule(
        blocks: List[TimeBlock],
        energy_curve: List[Tuple[datetime, EnergyLevel]]
    ) -> List[TimeBlock]:
        """Optimize schedule based on energy curve"""
```

### Domain Events

#### Base Event
```python
class DomainEvent:
    """Base class for all domain events"""
    event_id: str
    event_type: str
    timestamp: datetime
    metadata: Dict[str, Any]
```

#### Task Events
```python
class TaskCreated(DomainEvent):
    task_id: str
    title: str
    priority: Priority
    status: Status

class TaskCompleted(DomainEvent):
    task_id: str
    completed_at: datetime

class TaskUpdated(DomainEvent):
    task_id: str
    changes: Dict[str, Any]

class TaskDeleted(DomainEvent):
    task_id: str
```

---

## Repository Pattern

### Why Repositories?

Repositories **abstract persistence** from business logic:

- Domain defines **what** needs to be stored (interface)
- Infrastructure defines **how** it's stored (implementation)
- Application uses **interface**, never implementation

### Repository Interface (Domain)

```python
# src/domain/repositories/task_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Task
from ..value_objects import Status, Priority

class ITaskRepository(ABC):
    """Abstract repository interface for task persistence"""

    @abstractmethod
    def save(self, task: Task) -> None:
        """Save task (create or update)"""
        pass

    @abstractmethod
    def find_by_id(self, task_id: str) -> Optional[Task]:
        """Find task by ID"""
        pass

    @abstractmethod
    def find_all(self) -> List[Task]:
        """Find all tasks"""
        pass

    @abstractmethod
    def find_by_status(self, status: Status) -> List[Task]:
        """Find tasks by status"""
        pass

    @abstractmethod
    def find_by_priority(self, priority: Priority) -> List[Task]:
        """Find tasks by priority"""
        pass

    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """Delete task by ID"""
        pass

    @abstractmethod
    def exists(self, task_id: str) -> bool:
        """Check if task exists"""
        pass
```

### Repository Implementation (Infrastructure)

```python
# src/infrastructure/persistence/repositories/json_task_repository.py
from pathlib import Path
from typing import List, Optional
from ....domain.repositories import ITaskRepository
from ....domain.entities import Task
from ....domain.value_objects import Status, Priority
from ..json_storage import JsonStorage

class JsonTaskRepository(ITaskRepository):
    """JSON file-based implementation of ITaskRepository"""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path

    def save(self, task: Task) -> None:
        tasks_data = JsonStorage.read_json(self.storage_path) or {}
        tasks_data[task.id] = task.to_dict()
        JsonStorage.write_json(self.storage_path, tasks_data, backup=True)

    def find_by_id(self, task_id: str) -> Optional[Task]:
        tasks_data = JsonStorage.read_json(self.storage_path)
        if not tasks_data or task_id not in tasks_data:
            return None
        return Task.from_dict(tasks_data[task_id])

    def find_all(self) -> List[Task]:
        tasks_data = JsonStorage.read_json(self.storage_path)
        if not tasks_data:
            return []
        return [Task.from_dict(data) for data in tasks_data.values()]

    def find_by_status(self, status: Status) -> List[Task]:
        all_tasks = self.find_all()
        return [task for task in all_tasks if task.status == status]

    def find_by_priority(self, priority: Priority) -> List[Task]:
        all_tasks = self.find_all()
        return [task for task in all_tasks if task.priority == priority]

    def delete(self, task_id: str) -> bool:
        tasks_data = JsonStorage.read_json(self.storage_path)
        if not tasks_data or task_id not in tasks_data:
            return False
        del tasks_data[task_id]
        JsonStorage.write_json(self.storage_path, tasks_data, backup=True)
        return True

    def exists(self, task_id: str) -> bool:
        tasks_data = JsonStorage.read_json(self.storage_path)
        return bool(tasks_data and task_id in tasks_data)
```

### Using Repositories in Application Layer

```python
# src/application/task_management/create_task_use_case.py
from ...domain.repositories import ITaskRepository
from ...domain.entities import Task
from ...domain.value_objects import Priority

class CreateTaskUseCase:
    """Use case for creating a new task"""

    def __init__(self, task_repository: ITaskRepository):
        # Depend on INTERFACE, not implementation
        self.task_repository = task_repository

    def execute(self, title: str, priority: Priority, **kwargs) -> Task:
        """Create and save a new task"""
        # Create domain entity
        task = Task.create(title=title, priority=priority, **kwargs)

        # Persist via repository interface
        self.task_repository.save(task)

        return task
```

### Adding New Repositories

To add a new repository:

1. **Define interface in domain layer:**
   ```python
   # src/domain/repositories/workflow_repository.py
   class IWorkflowRepository(ABC):
       @abstractmethod
       def save(self, workflow: Workflow) -> None:
           pass
   ```

2. **Implement in infrastructure layer:**
   ```python
   # src/infrastructure/persistence/repositories/json_workflow_repository.py
   class JsonWorkflowRepository(IWorkflowRepository):
       def save(self, workflow: Workflow) -> None:
           # Implementation here
           pass
   ```

3. **Use in application layer:**
   ```python
   # src/application/workflows/execute_workflow_use_case.py
   class ExecuteWorkflowUseCase:
       def __init__(self, workflow_repository: IWorkflowRepository):
           self.workflow_repository = workflow_repository
   ```

---

## Migration Guide

### For Remaining Epics

#### EPIC-3 Part 2: Complete Operator Agent

**Current Legacy Code:**
- `src/workflows.py` (procedural functions)
- `src/prioritization.py` (functions on dicts)

**Migration Steps:**

1. **Create Domain Models:**
   ```python
   # src/domain/entities/workflow.py
   class Workflow:
       def __init__(self, id: str, steps: List[WorkflowStep]):
           self.id = id
           self.steps = steps

       def execute(self) -> WorkflowResult:
           """Execute workflow steps"""
   ```

2. **Create Application Services:**
   ```python
   # src/application/workflows/workflow_service.py
   class WorkflowService:
       def __init__(self, workflow_repo: IWorkflowRepository):
           self.workflow_repo = workflow_repo

       def execute_workflow(self, workflow_id: str) -> WorkflowResult:
           workflow = self.workflow_repo.find_by_id(workflow_id)
           return workflow.execute()
   ```

3. **Update Presentation Layer:**
   ```python
   # src/presentation/cli/commands.py
   def weekly_prep_command(workflow_service: WorkflowService):
       result = workflow_service.execute_workflow("weekly-prep")
       print_workflow_result(result)
   ```

4. **Feature Flag Rollout:**
   ```python
   if config.USE_NEW_ARCHITECTURE:
       workflow_service.execute_workflow("weekly-prep")
   else:
       workflows.weekly_prep()  # Legacy
   ```

#### EPIC-4: Planner Agent

**Create from Scratch Using Architecture:**

1. **Domain Layer:**
   - `entities/goal.py` - Goal entity
   - `entities/project.py` - Project entity
   - `value_objects/goal_status.py` - GoalStatus enum
   - `services/goal_tracking_service.py` - Domain logic

2. **Application Layer:**
   - `use_cases/create_goal_use_case.py`
   - `use_cases/track_progress_use_case.py`
   - `services/planning_service.py`

3. **Infrastructure Layer:**
   - `repositories/json_goal_repository.py`
   - `repositories/json_project_repository.py`

4. **Presentation Layer:**
   - `cli/planning_commands.py`
   - `formatters/goal_formatter.py`

#### EPIC-5: Strategist Agent

Follow same pattern as EPIC-4:
- Domain entities (Strategy, Opportunity)
- Application services (StrategyService)
- Infrastructure repositories (JsonStrategyRepository)
- Presentation commands (strategy_commands.py)

#### EPIC-6: Analyst Agent

Follow same pattern as EPIC-4:
- Domain entities (Metric, Report, Trend)
- Application services (AnalysisService)
- Infrastructure repositories (JsonMetricRepository)
- Presentation commands (analysis_commands.py)

#### EPIC-7: Agent Designer

Follow same pattern as EPIC-4:
- Domain entities (AgentDefinition, Capability)
- Application services (AgentDesignerService)
- Infrastructure repositories (JsonAgentRepository)
- Presentation commands (designer_commands.py)

### Refactoring Patterns

#### From Procedural to OOP

**Before (Procedural):**
```python
def create_task(task_dict: Dict[str, Any]) -> Dict[str, Any]:
    task_dict['created_at'] = datetime.now().isoformat()
    tasks = _load_tasks()
    tasks.append(task_dict)
    _save_tasks(tasks)
    return task_dict
```

**After (OOP with Repository):**
```python
def create_task(title: str, priority: Priority) -> Task:
    task = Task.create(title=title, priority=priority)
    repository.save(task)
    return task
```

#### From Functions on Dicts to Domain Methods

**Before:**
```python
def mark_task_complete(task: Dict) -> None:
    task["status"] = "done"
    task["completed_at"] = datetime.now().isoformat()
```

**After:**
```python
class Task:
    def mark_complete(self) -> None:
        if self.status == Status.DONE:
            raise ValueError("Already complete")
        self.status = Status.DONE
        self.completed_date = datetime.now()
```

#### From Direct File I/O to Repositories

**Before:**
```python
def save_task(task: Dict) -> None:
    with open("data/tasks.json", "w") as f:
        json.dump(task, f)
```

**After:**
```python
def save_task(task: Task, repository: ITaskRepository) -> None:
    repository.save(task)
```

### Migration Checklist

When migrating a feature:

- [ ] Create domain entities and value objects
- [ ] Create repository interface in domain
- [ ] Implement repository in infrastructure
- [ ] Create use cases in application
- [ ] Create formatters/commands in presentation
- [ ] Write unit tests for domain (90%+ coverage)
- [ ] Write integration tests for infrastructure (85%+ coverage)
- [ ] Add feature flag for gradual rollout
- [ ] Test both old and new implementations
- [ ] Update documentation
- [ ] Remove old code after validation

---

## Feature Flag System

### Strangler Fig Pattern

**Strategy:** Build new system alongside old, route via feature flags, gradually retire old code.

**Benefits:**
- Zero downtime migration
- Can rollback instantly
- Validate new code with real usage
- Reduce risk

### Feature Flags

#### USE_NEW_ARCHITECTURE
```python
# src/config.py
import os

USE_NEW_ARCHITECTURE = os.getenv("USE_NEW_ARCHITECTURE", "false").lower() == "true"
```

**Usage:**
```python
# src/main.py or src/presentation/cli/commands.py
from src.config import USE_NEW_ARCHITECTURE

if USE_NEW_ARCHITECTURE:
    # New Hexagonal Architecture path
    planning_service = DailyPlanningService(task_repository, energy_matcher)
    result = planning_service.create_daily_plan(energy_level)
else:
    # Legacy path
    result = workflows.daily_planning(energy_level)
```

### Rollout Strategy

**Phase 1: Development (Current)**
- Feature flag defaults to `False`
- New code tested in isolation
- Both paths maintained

**Phase 2: Testing**
- Set flag to `True` in dev environment
- Run full test suite against new implementation
- Compare behavior with legacy

**Phase 3: Gradual Rollout**
- Set flag to `True` for specific features
- Monitor for issues
- Roll back if needed

**Phase 4: Full Migration**
- Set flag to `True` globally
- Run in production for validation period
- Remove legacy code after confidence

**Phase 5: Cleanup**
- Remove feature flag
- Delete legacy code
- Update documentation

### Example: Dual-Path Routing

```python
# src/presentation/cli/commands.py
from src.config import USE_NEW_ARCHITECTURE

# New implementation (Hexagonal Architecture)
from src.application.planning.daily_planning_service import DailyPlanningService
from src.infrastructure.persistence.repositories.task_repository_json import JsonTaskRepository

# Legacy implementation
import src.workflows as legacy_workflows

def daily_planning_command(energy_level: str) -> None:
    """Execute daily planning workflow"""

    if USE_NEW_ARCHITECTURE:
        # NEW: Use Hexagonal Architecture
        task_repo = JsonTaskRepository(Path("data/tasks.json"))
        planning_service = DailyPlanningService(task_repo)
        plan = planning_service.create_daily_plan(energy_level)
        # Format and display using new formatters
        formatter = PlanningFormatter()
        output = formatter.format_daily_plan(plan)
        console.print(output)
    else:
        # LEGACY: Use procedural functions
        plan = legacy_workflows.daily_planning(energy_level)
        # Display using legacy formatting
        print(plan)
```

---

## Architecture Decision Records

### ADR-009: Adopt Hexagonal Architecture

**Status:** Accepted (2025-10-20)

**Context:**

After Sprint 4, accumulated architectural debt:
- `memory.py` god object (1,500 lines) handling 4 concerns
- Procedural functions operating on dicts (no OOP)
- Tight coupling (business logic mixed with file I/O)
- No testability (mocking file I/O required for unit tests)
- Flat structure (no layering or separation of concerns)
- Anemic domain model (no encapsulation)

**Decision:**

Adopt **Hexagonal Architecture** (Ports & Adapters) with:
- Domain layer: Pure business logic, zero dependencies
- Application layer: Use cases and orchestration
- Infrastructure layer: Persistence, external services
- Presentation layer: CLI and formatting

**Consequences:**

**Benefits:**
1. **Testability**: Domain logic tested without file I/O (unit tests run in <1ms)
2. **Flexibility**: Easy to swap JSON for database later
3. **Maintainability**: Clear boundaries, each layer has single responsibility
4. **Scalability**: Add features without touching core domain
5. **OOP**: Entities with behavior, proper encapsulation
6. **Type Safety**: Strong typing throughout (mypy compliance)
7. **Clarity**: New developers understand structure immediately
8. **Future-Proof**: Standard patterns known to industry

**Trade-offs:**
1. **Initial Effort**: EPIC-5R = 83 points (~6 weeks) to refactor
2. **Learning Curve**: Team must understand architecture patterns
3. **Boilerplate**: More files/classes than procedural code
4. **Migration Complexity**: Strangler Fig requires dual paths

**Implementation:**

Executed via EPIC-5R across 6 phases:
- Phase 1: Foundation (domain value objects, entities, interfaces) - 10 pts
- Phase 2: Infrastructure (repositories, storage utilities) - 16 pts
- Phase 3: Application (use cases, services) - 18 pts
- Phase 4: Presentation (CLI, formatters) - 8 pts
- Phase 5: Events & Coordination - 18 pts
- Phase 6: Testing & Documentation - 13 pts

**Total:** 83 points delivered, 15 stories complete, 279+ tests passing.

**ROI:**

Investment: 6 weeks of refactoring
Benefit: Accelerated future development (EPIC-4 through EPIC-7 will be 30-50% faster)

**Validation:**

- ✅ 171 domain tests (90%+ coverage, <1ms each)
- ✅ 108 infrastructure tests (85%+ coverage, isolated)
- ✅ Zero regressions (all existing features work)
- ✅ Strangler Fig allows gradual migration

---

## Conclusion

Mission Control now has a **solid architectural foundation** for future growth:

- **Clean separation** of concerns across 4 layers
- **Testable** domain logic (90%+ coverage)
- **Flexible** infrastructure (swap implementations easily)
- **Clear patterns** for adding new features
- **Self-documenting** code structure

This architecture enables Mission Control to evolve from MVP to production-grade system while maintaining quality, testability, and developer velocity.

---

**For Questions or Updates:**
- See `CLAUDE.md` for engineering standards
- See `PRODUCT-BACKLOG.md` for project status
- See `docs/epics.md` for feature roadmap
- See `docs/stories/` for implementation details

**Next Steps:**
- Resume feature development (EPIC-3 Part 2, EPIC-4, EPIC-5, EPIC-6, EPIC-7)
- Gradually remove legacy code via Strangler Fig
- Add new features following Hexagonal Architecture patterns
- Maintain 85%+ test coverage

---

*"Good architecture makes the right choice the easy choice."*
