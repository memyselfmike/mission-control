"""Task domain entity with encapsulated business logic.

This entity represents a task in the Mission Control system following
Hexagonal/Clean Architecture principles. It uses value objects from Story 5.1
and encapsulates all business logic related to task management.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from ..value_objects import Priority, Status, EnergyLevel

# ID counter for generating unique task IDs
_task_id_counter = 0


class Task:
    """Domain entity representing a task with encapsulated behavior.

    Task is a rich domain entity (not an anemic data holder). It validates
    its own invariants and contains all business logic for task management.

    Invariants:
    - Title must be at least 3 characters
    - BLOCKED status requires blocked_reason
    - COMPLETED status requires completed_date
    - Estimated time must be positive if provided
    - id, created_date, started_date, completed_date are immutable once set
    """

    def __init__(
        self,
        id: str,
        title: str,
        status: Status,
        priority: Priority,
        energy_required: EnergyLevel,
        description: str = "",
        estimated_time_minutes: Optional[int] = None,
        actual_time_minutes: Optional[int] = None,
        work_context: Optional[str] = None,
        linked_goal_id: Optional[str] = None,
        linked_project_id: Optional[str] = None,
        due_date: Optional[datetime] = None,
        created_date: Optional[datetime] = None,
        started_date: Optional[datetime] = None,
        completed_date: Optional[datetime] = None,
        deferred_until: Optional[datetime] = None,
        blocked_reason: Optional[str] = None,
        notes: str = "",
        tags: Optional[List[str]] = None,
    ):
        """Initialize a Task entity with validation.

        Args:
            id: Unique task identifier (immutable)
            title: Task title (minimum 3 characters)
            status: Current task status (value object)
            priority: Task priority (value object)
            energy_required: Energy level needed (value object)
            description: Detailed task description
            estimated_time_minutes: Estimated time to complete (must be positive)
            actual_time_minutes: Actual time spent
            work_context: Context category (deep_work, admin, communication, etc.)
            linked_goal_id: ID of linked goal
            linked_project_id: ID of linked project
            due_date: Task deadline
            created_date: When task was created (immutable, auto-set if None)
            started_date: When task was started (immutable after first set)
            completed_date: When task was completed (immutable after set)
            deferred_until: Date task is deferred until
            blocked_reason: Reason task is blocked (required if status=BLOCKED)
            notes: Additional notes
            tags: List of tags

        Raises:
            ValueError: If any invariants are violated
        """
        # Validate title
        if not title or len(title) < 3:
            raise ValueError("Title must be at least 3 characters")

        # Validate estimated time
        if estimated_time_minutes is not None and estimated_time_minutes <= 0:
            raise ValueError("Estimated time must be positive")

        # Validate BLOCKED status requires reason
        if status == Status.BLOCKED and not blocked_reason:
            raise ValueError("Blocked tasks must have a blocked_reason")

        # Validate COMPLETED status requires date
        if status == Status.COMPLETED and not completed_date:
            raise ValueError("Completed tasks must have a completed_date")

        # Set immutable fields
        self._id = id
        self._created_date = created_date or datetime.now()
        self._started_date = started_date
        self._completed_date = completed_date

        # Set mutable fields
        self.title = title
        self._status = status
        self.priority = priority
        self.energy_required = energy_required
        self.description = description
        self.estimated_time_minutes = estimated_time_minutes
        self.actual_time_minutes = actual_time_minutes
        self.work_context = work_context
        self.linked_goal_id = linked_goal_id
        self.linked_project_id = linked_project_id
        self.due_date = due_date
        self.deferred_until = deferred_until
        self.blocked_reason = blocked_reason
        self.notes = notes
        self.tags = tags or []

    # Immutable properties
    @property
    def id(self) -> str:
        """Task ID (immutable)."""
        return self._id

    @property
    def created_date(self) -> datetime:
        """Date task was created (immutable)."""
        return self._created_date

    @property
    def started_date(self) -> Optional[datetime]:
        """Date task was started (immutable after first set)."""
        return self._started_date

    @property
    def completed_date(self) -> Optional[datetime]:
        """Date task was completed (immutable after set)."""
        return self._completed_date

    @property
    def status(self) -> Status:
        """Current task status."""
        return self._status

    # State transition methods
    def mark_in_progress(self) -> None:
        """Mark task as in progress.

        Sets status to IN_PROGRESS and sets started_date on first call only.

        Raises:
            ValueError: If state transition is invalid
        """
        if not self.can_transition_to(Status.IN_PROGRESS):
            raise ValueError(f"Cannot transition from {self._status} to IN_PROGRESS")

        self._status = Status.IN_PROGRESS
        # Set started_date only on first transition to IN_PROGRESS
        if self._started_date is None:
            self._started_date = datetime.now()

    def mark_complete(self, actual_time_minutes: Optional[int] = None) -> None:
        """Mark task as complete.

        Sets status to COMPLETED, sets completed_date, and optionally records actual time.

        Args:
            actual_time_minutes: Optional actual time spent on task

        Raises:
            ValueError: If task is already complete or transition is invalid
        """
        if self._status == Status.COMPLETED:
            raise ValueError("Task already completed")

        if not self.can_transition_to(Status.COMPLETED):
            raise ValueError(f"Cannot transition from {self._status} to COMPLETED")

        self._status = Status.COMPLETED
        self._completed_date = datetime.now()
        if actual_time_minutes is not None:
            self.actual_time_minutes = actual_time_minutes

    def block(self, reason: str) -> None:
        """Block task with a reason.

        Args:
            reason: Why the task is blocked

        Raises:
            ValueError: If reason is empty or transition is invalid
        """
        if not reason:
            raise ValueError("Blocked reason is required")

        if not self.can_transition_to(Status.BLOCKED):
            raise ValueError(f"Cannot transition from {self._status} to BLOCKED")

        self._status = Status.BLOCKED
        self.blocked_reason = reason

    def defer_until(self, date: datetime) -> None:
        """Defer task until a specific date.

        Args:
            date: Date to defer until

        Raises:
            ValueError: If date is in the past or transition is invalid
        """
        if date < datetime.now():
            raise ValueError("Cannot defer to a past date")

        # Deferred tasks go to NOT_STARTED status
        if not self.can_transition_to(Status.NOT_STARTED):
            # If already NOT_STARTED, that's fine
            if self._status != Status.NOT_STARTED:
                raise ValueError(f"Cannot defer task with status {self._status}")

        self._status = Status.NOT_STARTED
        self.deferred_until = date

    def cancel(self) -> None:
        """Cancel the task.

        Raises:
            ValueError: If transition is invalid
        """
        if not self.can_transition_to(Status.CANCELLED):
            raise ValueError(f"Cannot transition from {self._status} to CANCELLED")

        self._status = Status.CANCELLED

    def can_transition_to(self, new_status: Status) -> bool:
        """Check if task can transition to a new status.

        Args:
            new_status: Target status

        Returns:
            True if transition is valid, False otherwise
        """
        return self._status.can_transition_to(new_status)

    # Query and calculation methods
    def is_overdue(self) -> bool:
        """Check if task is overdue.

        Returns:
            True if task has a due date in the past and is not complete
        """
        if not self.due_date or self._status == Status.COMPLETED:
            return False
        return datetime.now() > self.due_date

    def is_must_win_today(self) -> bool:
        """Check if task is a must-win priority.

        Returns:
            True if task has P0_CRITICAL priority
        """
        return self.priority == Priority.P0_CRITICAL

    def calculate_time_variance(self) -> Optional[int]:
        """Calculate variance between estimated and actual time.

        Returns:
            Positive number if over estimate, negative if under, None if missing data
        """
        if self.estimated_time_minutes is None or self.actual_time_minutes is None:
            return None
        return self.actual_time_minutes - self.estimated_time_minutes

    def get_days_until_due(self) -> Optional[int]:
        """Calculate days until due date.

        Returns:
            Number of days until due (negative if overdue), None if no due date
        """
        if not self.due_date:
            return None
        delta = self.due_date - datetime.now()
        return delta.days

    # Categorization methods
    def is_deep_work(self) -> bool:
        """Check if task requires deep work."""
        return self.work_context == "deep_work"

    def is_admin(self) -> bool:
        """Check if task is administrative."""
        return self.work_context == "admin"

    def is_communication(self) -> bool:
        """Check if task is communication-related."""
        return self.work_context == "communication"

    # Tag management
    def add_tag(self, tag: str) -> None:
        """Add a tag to the task.

        Args:
            tag: Tag to add (duplicates are prevented)
        """
        if tag and tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the task.

        Args:
            tag: Tag to remove

        Returns:
            True if tag was removed, False if tag not found
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return True
        return False

    def has_tag(self, tag: str) -> bool:
        """Check if task has a specific tag.

        Args:
            tag: Tag to check

        Returns:
            True if task has the tag
        """
        return tag in self.tags

    def update_notes(self, notes: str) -> None:
        """Update task notes.

        Args:
            notes: New notes content
        """
        self.notes = notes

    # Factory methods
    @classmethod
    def create(
        cls,
        title: str,
        priority: Priority = Priority.P2_MEDIUM,
        energy_required: EnergyLevel = EnergyLevel.MEDIUM,
        **kwargs
    ) -> "Task":
        """Factory method to create a new task with defaults.

        Args:
            title: Task title
            priority: Task priority (default: MEDIUM)
            energy_required: Energy level required (default: MEDIUM)
            **kwargs: Additional optional fields

        Returns:
            New Task instance with generated ID and defaults

        Raises:
            ValueError: If validation fails
        """
        global _task_id_counter
        _task_id_counter += 1
        task_id = f"TASK-{_task_id_counter:03d}"

        return cls(
            id=task_id,
            title=title,
            status=Status.NOT_STARTED,
            priority=priority,
            energy_required=energy_required,
            **kwargs
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Deserialize task from dictionary (e.g., from JSON storage).

        Args:
            data: Dictionary with task data

        Returns:
            Reconstructed Task instance

        Raises:
            ValueError: If data is invalid
        """
        # Convert string values to value objects
        return cls(
            id=data["id"],
            title=data["title"],
            status=Status.from_string(data["status"]),
            priority=Priority.from_string(data["priority"]),
            energy_required=EnergyLevel.from_string(data["energy_required"]),
            description=data.get("description", ""),
            estimated_time_minutes=data.get("estimated_time_minutes"),
            actual_time_minutes=data.get("actual_time_minutes"),
            work_context=data.get("work_context"),
            linked_goal_id=data.get("linked_goal_id"),
            linked_project_id=data.get("linked_project_id"),
            due_date=datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None,
            created_date=datetime.fromisoformat(data["created_date"]) if data.get("created_date") else None,
            started_date=datetime.fromisoformat(data["started_date"]) if data.get("started_date") else None,
            completed_date=datetime.fromisoformat(data["completed_date"]) if data.get("completed_date") else None,
            deferred_until=datetime.fromisoformat(data["deferred_until"]) if data.get("deferred_until") else None,
            blocked_reason=data.get("blocked_reason"),
            notes=data.get("notes", ""),
            tags=data.get("tags", []).copy() if data.get("tags") else [],
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize task to dictionary (e.g., for JSON storage).

        Returns:
            Dictionary with all task data (value objects converted to strings)
        """
        return {
            "id": self.id,
            "title": self.title,
            "status": str(self.status),
            "priority": str(self.priority),
            "energy_required": str(self.energy_required),
            "description": self.description,
            "estimated_time_minutes": self.estimated_time_minutes,
            "actual_time_minutes": self.actual_time_minutes,
            "work_context": self.work_context,
            "linked_goal_id": self.linked_goal_id,
            "linked_project_id": self.linked_project_id,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_date": self.created_date.isoformat(),
            "started_date": self.started_date.isoformat() if self.started_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "deferred_until": self.deferred_until.isoformat() if self.deferred_until else None,
            "blocked_reason": self.blocked_reason,
            "notes": self.notes,
            "tags": self.tags.copy(),
        }
