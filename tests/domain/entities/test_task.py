"""Comprehensive tests for Task domain entity.

Tests cover all acceptance criteria:
- AC1: Task entity creation with value objects
- AC2: Encapsulated business logic methods
- AC3: Self-validation and invariants
- AC4: Factory methods
- AC5: Immutability constraints
- AC6: Domain logic
- AC7: 90%+ test coverage
"""

import pytest
from datetime import datetime, timedelta
from src.domain.entities import Task
from src.domain.value_objects import Priority, Status, EnergyLevel


# Fixtures
@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task.create(
        title="Write comprehensive tests",
        priority=Priority.P1_HIGH,
        energy_required=EnergyLevel.HIGH
    )


@pytest.fixture
def task_with_dates():
    """Create a task with specific dates for testing."""
    return Task.create(
        title="Test task with dates",
        due_date=datetime.now() + timedelta(days=3),
        estimated_time_minutes=60
    )


class TestTaskCreation:
    """Tests for task creation (AC1)."""

    def test_create_task_with_valid_data(self):
        """Test Task.create() with valid data creates task correctly."""
        # Act
        task = Task.create(
            title="Write tests",
            priority=Priority.P1_HIGH,
            energy_required=EnergyLevel.HIGH
        )

        # Assert
        assert task.title == "Write tests"
        assert task.priority == Priority.P1_HIGH
        assert task.energy_required == EnergyLevel.HIGH
        assert task.status == Status.NOT_STARTED
        assert task.created_date is not None
        assert task.id.startswith("TASK-")

    def test_create_task_with_invalid_title_raises_error(self):
        """Test creating task with title < 3 chars raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            Task.create(title="ab")

    def test_create_task_with_empty_title_raises_error(self):
        """Test creating task with empty title raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            Task.create(title="")

    def test_create_task_with_negative_time_raises_error(self):
        """Test creating task with negative estimated time raises ValueError."""
        # Act & Assert
        with pytest.raises(ValueError, match="Estimated time must be positive"):
            Task.create(
                title="Valid title",
                estimated_time_minutes=-10
            )

    def test_create_factory_method_generates_unique_ids(self):
        """Test Task.create() generates unique sequential IDs."""
        # Act
        task1 = Task.create(title="First task")
        task2 = Task.create(title="Second task")

        # Assert
        assert task1.id != task2.id
        assert task1.id.startswith("TASK-")
        assert task2.id.startswith("TASK-")

    def test_create_factory_method_sets_defaults(self):
        """Test Task.create() sets default values correctly."""
        # Act
        task = Task.create(title="Minimal task")

        # Assert
        assert task.status == Status.NOT_STARTED
        assert task.priority == Priority.P2_MEDIUM
        assert task.energy_required == EnergyLevel.MEDIUM
        assert task.description == ""
        assert task.tags == []
        assert task.notes == ""


class TestStateTransitions:
    """Tests for state transition methods (AC2)."""

    def test_mark_in_progress_updates_status_and_started_date(self, sample_task):
        """Test mark_in_progress() sets status and started_date."""
        # Arrange
        assert sample_task.started_date is None

        # Act
        sample_task.mark_in_progress()

        # Assert
        assert sample_task.status == Status.IN_PROGRESS
        assert sample_task.started_date is not None
        assert isinstance(sample_task.started_date, datetime)

    def test_mark_in_progress_twice_does_not_change_started_date(self, sample_task):
        """Test calling mark_in_progress() twice keeps original started_date."""
        # Arrange
        sample_task.mark_in_progress()
        first_started_date = sample_task.started_date

        # Act
        sample_task.mark_in_progress()

        # Assert
        assert sample_task.started_date == first_started_date

    def test_mark_complete_updates_status_and_completed_date(self, sample_task):
        """Test mark_complete() sets status, completed_date, and actual time."""
        # Arrange
        sample_task.mark_in_progress()

        # Act
        sample_task.mark_complete(actual_time_minutes=60)

        # Assert
        assert sample_task.status == Status.COMPLETED
        assert sample_task.completed_date is not None
        assert sample_task.actual_time_minutes == 60

    def test_mark_complete_when_already_complete_raises_error(self, sample_task):
        """Test marking complete twice raises ValueError."""
        # Arrange
        sample_task.mark_in_progress()
        sample_task.mark_complete()

        # Act & Assert
        with pytest.raises(ValueError, match="already completed"):
            sample_task.mark_complete()

    def test_block_task_sets_status_and_reason(self, sample_task):
        """Test block() sets status to BLOCKED and stores reason."""
        # Arrange
        sample_task.mark_in_progress()

        # Act
        sample_task.block("Waiting for API access")

        # Assert
        assert sample_task.status == Status.BLOCKED
        assert sample_task.blocked_reason == "Waiting for API access"

    def test_block_without_reason_raises_error(self, sample_task):
        """Test block() without reason raises ValueError."""
        # Arrange
        sample_task.mark_in_progress()

        # Act & Assert
        with pytest.raises(ValueError, match="Blocked reason is required"):
            sample_task.block("")

    def test_defer_task_sets_deferred_until_date(self, sample_task):
        """Test defer_until() sets deferred_until and status."""
        # Arrange
        future_date = datetime.now() + timedelta(days=7)

        # Act
        sample_task.defer_until(future_date)

        # Assert
        assert sample_task.deferred_until == future_date
        assert sample_task.status == Status.NOT_STARTED

    def test_defer_to_past_date_raises_error(self, sample_task):
        """Test deferring to past date raises ValueError."""
        # Arrange
        past_date = datetime.now() - timedelta(days=1)

        # Act & Assert
        with pytest.raises(ValueError, match="Cannot defer to a past date"):
            sample_task.defer_until(past_date)

    def test_cancel_task_sets_status_to_cancelled(self, sample_task):
        """Test cancel() sets status to CANCELLED."""
        # Act
        sample_task.cancel()

        # Assert
        assert sample_task.status == Status.CANCELLED

    def test_can_transition_to_validates_state_changes(self, sample_task):
        """Test can_transition_to() returns correct boolean."""
        # Assert - valid transitions from NOT_STARTED
        assert sample_task.can_transition_to(Status.IN_PROGRESS) is True
        assert sample_task.can_transition_to(Status.CANCELLED) is True

        # Move to IN_PROGRESS
        sample_task.mark_in_progress()

        # Assert - valid transitions from IN_PROGRESS
        assert sample_task.can_transition_to(Status.COMPLETED) is True
        assert sample_task.can_transition_to(Status.BLOCKED) is True


class TestValidation:
    """Tests for validation and invariants (AC3)."""

    def test_title_minimum_length_validation(self):
        """Test titles of 0, 1, 2 chars raise ValueError."""
        # Test empty string
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            Task.create(title="")

        # Test 1 character
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            Task.create(title="a")

        # Test 2 characters
        with pytest.raises(ValueError, match="Title must be at least 3 characters"):
            Task.create(title="ab")

        # Test 3 characters should work
        task = Task.create(title="abc")
        assert task.title == "abc"

    def test_blocked_task_requires_reason(self):
        """Test BLOCKED status requires blocked_reason."""
        # Act & Assert - creating BLOCKED task without reason fails
        with pytest.raises(ValueError, match="Blocked tasks must have a blocked_reason"):
            Task(
                id="TEST-001",
                title="Test task",
                status=Status.BLOCKED,
                priority=Priority.P2_MEDIUM,
                energy_required=EnergyLevel.MEDIUM,
                blocked_reason=None
            )

    def test_completed_task_has_completed_date(self):
        """Test COMPLETED status requires completed_date."""
        # Act & Assert - creating COMPLETED task without date fails
        with pytest.raises(ValueError, match="Completed tasks must have a completed_date"):
            Task(
                id="TEST-001",
                title="Test task",
                status=Status.COMPLETED,
                priority=Priority.P2_MEDIUM,
                energy_required=EnergyLevel.MEDIUM,
                completed_date=None
            )

    def test_estimated_time_must_be_positive(self):
        """Test estimated_time_minutes must be positive."""
        # Test zero
        with pytest.raises(ValueError, match="Estimated time must be positive"):
            Task.create(title="Test task", estimated_time_minutes=0)

        # Test negative
        with pytest.raises(ValueError, match="Estimated time must be positive"):
            Task.create(title="Test task", estimated_time_minutes=-30)

    def test_invalid_state_transition_raises_error(self, sample_task):
        """Test invalid state transitions raise ValueError."""
        # Arrange - complete the task
        sample_task.mark_in_progress()
        sample_task.mark_complete()

        # Act & Assert - cannot go from COMPLETED to IN_PROGRESS
        with pytest.raises(ValueError, match="Cannot transition"):
            sample_task.mark_in_progress()


class TestFactoryMethods:
    """Tests for factory methods (AC4)."""

    def test_from_dict_reconstructs_task(self):
        """Test Task.from_dict() reconstructs all fields correctly."""
        # Arrange
        data = {
            "id": "TASK-001",
            "title": "Test task",
            "status": "NOT_STARTED",
            "priority": "P1_HIGH",
            "energy_required": "HIGH",
            "description": "Test description",
            "estimated_time_minutes": 60,
            "actual_time_minutes": None,
            "work_context": "deep_work",
            "linked_goal_id": "GOAL-001",
            "linked_project_id": None,
            "due_date": "2025-12-31T23:59:59",
            "created_date": "2025-10-22T10:00:00",
            "started_date": None,
            "completed_date": None,
            "deferred_until": None,
            "blocked_reason": None,
            "notes": "Test notes",
            "tags": ["urgent", "important"]
        }

        # Act
        task = Task.from_dict(data)

        # Assert
        assert task.id == "TASK-001"
        assert task.title == "Test task"
        assert task.status == Status.NOT_STARTED
        assert task.priority == Priority.P1_HIGH
        assert task.energy_required == EnergyLevel.HIGH
        assert task.description == "Test description"
        assert task.estimated_time_minutes == 60
        assert task.work_context == "deep_work"
        assert task.linked_goal_id == "GOAL-001"
        assert task.notes == "Test notes"
        assert task.tags == ["urgent", "important"]

    def test_to_dict_serializes_task(self, sample_task):
        """Test to_dict() returns dict with all fields."""
        # Act
        data = sample_task.to_dict()

        # Assert
        assert data["id"] == sample_task.id
        assert data["title"] == "Write comprehensive tests"
        assert data["status"] == "NOT_STARTED"
        assert data["priority"] == "P1_HIGH"
        assert data["energy_required"] == "HIGH"
        assert "created_date" in data
        assert isinstance(data["tags"], list)

    def test_from_dict_to_dict_round_trip(self):
        """Test from_dict() -> to_dict() preserves data."""
        # Arrange
        original_task = Task.create(
            title="Round trip test",
            priority=Priority.P0_CRITICAL,
            energy_required=EnergyLevel.LOW,
            description="Test round trip",
            estimated_time_minutes=45,
            work_context="admin",
            notes="Important notes",
            tags=["test", "round-trip"]
        )

        # Act
        data = original_task.to_dict()
        reconstructed_task = Task.from_dict(data)

        # Assert
        assert reconstructed_task.id == original_task.id
        assert reconstructed_task.title == original_task.title
        assert reconstructed_task.status == original_task.status
        assert reconstructed_task.priority == original_task.priority
        assert reconstructed_task.energy_required == original_task.energy_required
        assert reconstructed_task.description == original_task.description
        assert reconstructed_task.estimated_time_minutes == original_task.estimated_time_minutes
        assert reconstructed_task.work_context == original_task.work_context
        assert reconstructed_task.notes == original_task.notes
        assert reconstructed_task.tags == original_task.tags


class TestImmutability:
    """Tests for immutability constraints (AC5)."""

    def test_id_is_immutable(self, sample_task):
        """Test task ID cannot be reassigned."""
        # Arrange
        original_id = sample_task.id

        # Act & Assert - property has no setter
        with pytest.raises(AttributeError):
            sample_task.id = "MODIFIED-ID"

        assert sample_task.id == original_id

    def test_created_date_is_immutable(self, sample_task):
        """Test created_date cannot be modified after creation."""
        # Arrange
        original_created = sample_task.created_date

        # Act & Assert - property has no setter
        with pytest.raises(AttributeError):
            sample_task.created_date = datetime.now()

        assert sample_task.created_date == original_created

    def test_started_date_is_immutable_after_first_set(self, sample_task):
        """Test started_date set only on first mark_in_progress()."""
        # Act - first call sets started_date
        sample_task.mark_in_progress()
        first_started = sample_task.started_date

        # Second call should not change it
        sample_task.mark_in_progress()

        # Assert
        assert sample_task.started_date == first_started

        # Property has no setter
        with pytest.raises(AttributeError):
            sample_task.started_date = datetime.now()

    def test_completed_date_is_immutable_after_set(self, sample_task):
        """Test completed_date cannot be changed once task is complete."""
        # Arrange
        sample_task.mark_in_progress()
        sample_task.mark_complete()
        original_completed = sample_task.completed_date

        # Act & Assert - property has no setter
        with pytest.raises(AttributeError):
            sample_task.completed_date = datetime.now()

        assert sample_task.completed_date == original_completed


class TestBusinessLogic:
    """Tests for domain logic (AC6)."""

    def test_is_overdue_returns_true_when_past_due(self):
        """Test is_overdue() returns True for task with past due date."""
        # Arrange
        task = Task.create(
            title="Overdue task",
            due_date=datetime.now() - timedelta(days=1)
        )

        # Assert
        assert task.is_overdue() is True

    def test_is_overdue_returns_false_when_complete(self):
        """Test is_overdue() returns False for completed tasks."""
        # Arrange
        task = Task.create(
            title="Complete task",
            due_date=datetime.now() - timedelta(days=1)
        )
        task.mark_in_progress()
        task.mark_complete()

        # Assert
        assert task.is_overdue() is False

    def test_is_overdue_returns_false_when_no_due_date(self, sample_task):
        """Test is_overdue() returns False when no due date set."""
        # Assert
        assert sample_task.due_date is None
        assert sample_task.is_overdue() is False

    def test_calculate_time_variance_with_actual_time(self):
        """Test calculate_time_variance() returns correct variance."""
        # Arrange - task took 30 min more than estimated
        task = Task.create(
            title="Test task",
            estimated_time_minutes=60
        )
        task.mark_in_progress()
        task.mark_complete(actual_time_minutes=90)

        # Act
        variance = task.calculate_time_variance()

        # Assert
        assert variance == 30  # 90 - 60 = 30 (over estimate)

    def test_calculate_time_variance_returns_none_when_missing_data(self, sample_task):
        """Test calculate_time_variance() returns None when data missing."""
        # Assert
        assert sample_task.calculate_time_variance() is None

    def test_is_must_win_today_checks_priority(self):
        """Test is_must_win_today() returns True only for P0_CRITICAL."""
        # Arrange
        critical_task = Task.create(title="Critical", priority=Priority.P0_CRITICAL)
        high_task = Task.create(title="High", priority=Priority.P1_HIGH)

        # Assert
        assert critical_task.is_must_win_today() is True
        assert high_task.is_must_win_today() is False

    def test_get_days_until_due(self):
        """Test get_days_until_due() calculates correctly."""
        # Arrange
        task = Task.create(
            title="Future task",
            due_date=datetime.now() + timedelta(days=5)
        )

        # Act
        days = task.get_days_until_due()

        # Assert
        assert days == 4 or days == 5  # Allow for timing variations

    def test_is_deep_work_categorization(self):
        """Test is_deep_work() checks work_context correctly."""
        # Arrange
        deep_work_task = Task.create(title="Deep work", work_context="deep_work")
        admin_task = Task.create(title="Admin", work_context="admin")

        # Assert
        assert deep_work_task.is_deep_work() is True
        assert admin_task.is_deep_work() is False

    def test_is_admin_categorization(self):
        """Test is_admin() checks work_context correctly."""
        # Arrange
        admin_task = Task.create(title="Admin", work_context="admin")
        deep_task = Task.create(title="Deep", work_context="deep_work")

        # Assert
        assert admin_task.is_admin() is True
        assert deep_task.is_admin() is False

    def test_is_communication_categorization(self):
        """Test is_communication() checks work_context correctly."""
        # Arrange
        comm_task = Task.create(title="Email", work_context="communication")
        admin_task = Task.create(title="Admin", work_context="admin")

        # Assert
        assert comm_task.is_communication() is True
        assert admin_task.is_communication() is False


class TestTagManagement:
    """Tests for tag management (AC6)."""

    def test_add_tag_to_task(self, sample_task):
        """Test add_tag() adds tag to tags list."""
        # Arrange
        assert "urgent" not in sample_task.tags

        # Act
        sample_task.add_tag("urgent")

        # Assert
        assert "urgent" in sample_task.tags

    def test_add_tag_prevents_duplicates(self, sample_task):
        """Test add_tag() prevents duplicate tags."""
        # Arrange
        sample_task.add_tag("urgent")

        # Act
        sample_task.add_tag("urgent")

        # Assert
        assert sample_task.tags.count("urgent") == 1

    def test_remove_tag_from_task(self, sample_task):
        """Test remove_tag() removes tag if exists."""
        # Arrange
        sample_task.add_tag("urgent")
        assert "urgent" in sample_task.tags

        # Act
        result = sample_task.remove_tag("urgent")

        # Assert
        assert result is True
        assert "urgent" not in sample_task.tags

    def test_remove_nonexistent_tag_returns_false(self, sample_task):
        """Test remove_tag() returns False if tag not found."""
        # Act
        result = sample_task.remove_tag("nonexistent")

        # Assert
        assert result is False

    def test_has_tag_returns_correct_boolean(self, sample_task):
        """Test has_tag() returns True if tag exists."""
        # Arrange
        sample_task.add_tag("important")

        # Assert
        assert sample_task.has_tag("important") is True
        assert sample_task.has_tag("nonexistent") is False

    def test_update_notes(self, sample_task):
        """Test update_notes() updates notes field."""
        # Arrange
        assert sample_task.notes == ""

        # Act
        sample_task.update_notes("Important information")

        # Assert
        assert sample_task.notes == "Important information"
