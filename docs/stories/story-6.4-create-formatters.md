# Story 6.4: Create Formatters

Status: Ready

## Story

As a developer,
I want presentation layer formatters that convert domain entities to Rich-formatted strings,
so that CLI commands can display beautiful output without any business logic, following Hexagonal Architecture principles with pure presentation functions.

## Acceptance Criteria

1. **Formatter Module Structure Created**
   - All formatters in `src/presentation/formatters/` module
   - Formatters: `task_formatter.py`, `planning_formatter.py`, `briefing_formatter.py`, `status_formatter.py`
   - Each formatter exports pure functions (no classes unless necessary)
   - Proper module structure with `__init__.py` exports
   - Zero business logic (CLAUDE.md Rule 2.3.1: presentation layer is pure formatting)

2. **TaskFormatter Created**
   - Function: `format_task(task: Task) -> str` - Single task as Rich panel
   - Function: `format_task_list(tasks: List[Task]) -> str` - Task list as Rich table
   - Function: `format_task_summary(task: Task) -> str` - One-line task summary
   - Displays: title, priority, status, energy_level, due_date, tags
   - Uses Rich panels, tables, and text formatting (colors, bold, italic)
   - Zero dependencies on infrastructure or application layers

3. **PlanningFormatter Created**
   - Function: `format_daily_plan(tasks: List[Task], date: datetime) -> str` - Full daily plan
   - Function: `format_priority_matrix(tasks: List[Task]) -> str` - Eisenhower Matrix visualization
   - Function: `format_time_blocks(time_blocks: List[TimeBlock]) -> str` - Time blocking schedule
   - Function: `format_must_wins(tasks: List[Task]) -> str` - MIT (Most Important Tasks) display
   - Uses Rich tables and panels to organize planning output
   - Omega voice integration: energetic, action-oriented language

4. **BriefingFormatter Created**
   - Function: `format_morning_briefing(briefing_data: Dict[str, Any]) -> str` - Full morning briefing
   - Function: `format_briefing_section(title: str, content: str) -> str` - Individual section
   - Function: `format_task_priorities(tasks: List[Task]) -> str` - Priority list
   - Displays: greeting, date, weather (if available), today's tasks, priorities, reminders
   - Time-aware formatting (morning vs afternoon greeting)
   - Uses Rich panels and formatted text

5. **StatusFormatter Created**
   - Function: `format_task_status(task: Task) -> str` - Status badge/indicator
   - Function: `format_progress_summary(completed: int, total: int) -> str` - Progress bar/percentage
   - Function: `format_completion_report(tasks: List[Task]) -> str` - EOD completion summary
   - Uses Rich progress bars, color coding (green=done, yellow=in-progress, red=blocked)
   - Zero business logic (just formatting)

6. **Type Safety and Documentation**
   - Complete type hints on all functions (Task, List[Task], str, datetime, Dict)
   - Comprehensive docstrings (module-level and function-level)
   - Examples in docstrings showing usage with sample Rich output
   - No `Any` types except for flexible briefing_data dict
   - All Rich formatting properly escaped and tested

7. **Comprehensive Unit Tests**
   - 15+ unit tests in `tests/presentation/formatters/test_formatters.py`
   - Each formatter has 2-4 tests (basic formatting, edge cases, empty data)
   - Tests verify Rich markup is present (e.g., `[bold]`, `[green]`, etc.)
   - Tests use mock domain objects (Task, TimeBlock, etc.)
   - Test coverage >= 80% for presentation layer (CLAUDE.md Rule 6.1.1)
   - Zero regressions in existing tests (run full test suite)

## Tasks / Subtasks

- [ ] Task 1: Create module structure (AC: #1)
  - [ ] Subtask 1.1: Create `src/presentation/` directory
  - [ ] Subtask 1.2: Create `src/presentation/formatters/` directory
  - [ ] Subtask 1.3: Create `src/presentation/formatters/__init__.py`
  - [ ] Subtask 1.4: Create `src/presentation/__init__.py`
  - [ ] Subtask 1.5: Export formatter functions in __init__.py

- [ ] Task 2: Create TaskFormatter (AC: #2)
  - [ ] Subtask 2.1: Create `task_formatter.py`
  - [ ] Subtask 2.2: Implement `format_task(task: Task) -> str`
  - [ ] Subtask 2.3: Implement `format_task_list(tasks: List[Task]) -> str`
  - [ ] Subtask 2.4: Implement `format_task_summary(task: Task) -> str`
  - [ ] Subtask 2.5: Add Rich panel formatting for single task
  - [ ] Subtask 2.6: Add Rich table formatting for task list
  - [ ] Subtask 2.7: Add color coding for priority and status
  - [ ] Subtask 2.8: Add comprehensive docstrings with examples

- [ ] Task 3: Create PlanningFormatter (AC: #3)
  - [ ] Subtask 3.1: Create `planning_formatter.py`
  - [ ] Subtask 3.2: Implement `format_daily_plan(tasks: List[Task], date: datetime) -> str`
  - [ ] Subtask 3.3: Implement `format_priority_matrix(tasks: List[Task]) -> str`
  - [ ] Subtask 3.4: Implement `format_time_blocks(time_blocks: List[TimeBlock]) -> str`
  - [ ] Subtask 3.5: Implement `format_must_wins(tasks: List[Task]) -> str`
  - [ ] Subtask 3.6: Add Eisenhower Matrix visualization (4 quadrants)
  - [ ] Subtask 3.7: Add time blocking schedule table
  - [ ] Subtask 3.8: Add Omega voice examples in docstrings

- [ ] Task 4: Create BriefingFormatter (AC: #4)
  - [ ] Subtask 4.1: Create `briefing_formatter.py`
  - [ ] Subtask 4.2: Implement `format_morning_briefing(briefing_data: Dict[str, Any]) -> str`
  - [ ] Subtask 4.3: Implement `format_briefing_section(title: str, content: str) -> str`
  - [ ] Subtask 4.4: Implement `format_task_priorities(tasks: List[Task]) -> str`
  - [ ] Subtask 4.5: Add time-aware greeting logic (morning vs afternoon)
  - [ ] Subtask 4.6: Add Rich panel formatting for briefing sections
  - [ ] Subtask 4.7: Add weather integration (if data available)
  - [ ] Subtask 4.8: Add comprehensive docstrings

- [ ] Task 5: Create StatusFormatter (AC: #5)
  - [ ] Subtask 5.1: Create `status_formatter.py`
  - [ ] Subtask 5.2: Implement `format_task_status(task: Task) -> str`
  - [ ] Subtask 5.3: Implement `format_progress_summary(completed: int, total: int) -> str`
  - [ ] Subtask 5.4: Implement `format_completion_report(tasks: List[Task]) -> str`
  - [ ] Subtask 5.5: Add status badge formatting (emojis or symbols)
  - [ ] Subtask 5.6: Add Rich progress bar for completion percentage
  - [ ] Subtask 5.7: Add color coding (green=done, yellow=in-progress, red=blocked)
  - [ ] Subtask 5.8: Add EOD summary formatting

- [ ] Task 6: Update module exports (AC: #1, #6)
  - [ ] Subtask 6.1: Update `src/presentation/formatters/__init__.py` with all formatter functions
  - [ ] Subtask 6.2: Update `src/presentation/__init__.py` to export formatters module
  - [ ] Subtask 6.3: Add type hints to all __init__.py exports
  - [ ] Subtask 6.4: Add module-level docstrings

- [ ] Task 7: Create comprehensive tests (AC: #7)
  - [ ] Subtask 7.1: Create `tests/presentation/` directory
  - [ ] Subtask 7.2: Create `tests/presentation/formatters/` directory
  - [ ] Subtask 7.3: Create `tests/presentation/formatters/test_formatters.py`
  - [ ] Subtask 7.4: Write 4 tests for TaskFormatter (format_task, format_task_list, format_task_summary, edge cases)
  - [ ] Subtask 7.5: Write 4 tests for PlanningFormatter (daily_plan, priority_matrix, time_blocks, must_wins)
  - [ ] Subtask 7.6: Write 3 tests for BriefingFormatter (morning_briefing, section, priorities)
  - [ ] Subtask 7.7: Write 4 tests for StatusFormatter (status, progress, completion_report, edge cases)
  - [ ] Subtask 7.8: Verify Rich markup is present in outputs
  - [ ] Subtask 7.9: Test with empty data (zero tasks)
  - [ ] Subtask 7.10: Run full test suite to ensure zero regressions

## Dev Notes

### Architecture Constraints

**Hexagonal/Clean Architecture (CLAUDE.md ADR-009):**
- Presentation layer is the OUTERMOST layer
- Depends on: Domain layer only (Task, TimeBlock, Priority, Status, etc.)
- NO dependencies on: Application or Infrastructure layers
- Pure functions: Input domain entities → Output Rich-formatted strings
- Zero business logic (that's in domain/application)

**SOLID Principles:**
- SRP: Each formatter handles one concern (task formatting, planning formatting, etc.)
- OCP: Formatters are open for extension (add new format functions) but closed for modification
- LSP: N/A (no inheritance)
- ISP: N/A (no interfaces)
- DIP: Depends on domain abstractions (Task entity), not infrastructure

### Rich CLI Formatting Standards

**Rich Components to Use:**
- `Panel`: For single items (task details, briefing sections)
- `Table`: For lists (task lists, time blocks, priority matrix)
- `Text`: For formatted text with colors, bold, italic
- `Progress`: For completion percentages
- `Console.print()`: For output (not used in formatters - formatters return strings)

**Color Scheme:**
- Priority: P0=red, P1=yellow, P2=blue, P3=green
- Status: NOT_STARTED=gray, IN_PROGRESS=yellow, COMPLETED=green, BLOCKED=red
- Energy: HIGH=green, MEDIUM=yellow, LOW=blue

**Formatting Examples:**
```python
# Task as panel
[bold cyan]Task: {title}[/bold cyan]
Priority: {priority_color}P{priority}[/{priority_color}]
Status: {status_emoji} {status}
```

### Testing Strategy

**Unit Tests (15+ tests):**
1. TaskFormatter tests (4):
   - format_task with full task data
   - format_task_list with multiple tasks
   - format_task_summary with minimal data
   - Edge case: empty task list

2. PlanningFormatter tests (4):
   - format_daily_plan with 5 tasks
   - format_priority_matrix with all 4 quadrants
   - format_time_blocks with 3 blocks
   - format_must_wins with 3 MITs

3. BriefingFormatter tests (3):
   - format_morning_briefing with full data
   - format_briefing_section with title and content
   - format_task_priorities with 5 tasks

4. StatusFormatter tests (4):
   - format_task_status for each status enum
   - format_progress_summary with 7/10 completion
   - format_completion_report with completed tasks
   - Edge case: 0/0 completion (no tasks)

### Project Structure Notes

**File Locations:**
```
src/presentation/
  __init__.py
  formatters/
    __init__.py
    task_formatter.py
    planning_formatter.py
    briefing_formatter.py
    status_formatter.py

tests/presentation/
  formatters/
    test_formatters.py
```

**Import Examples:**
```python
# In CLI commands (Story 6.5)
from src.presentation.formatters import format_task, format_task_list, format_daily_plan

# In tests
from src.domain.entities import Task
from src.domain.value_objects import Priority, Status
from src.presentation.formatters import format_task
```

### References

- [Source: CLAUDE.md] - Engineering standards, Hexagonal Architecture (ADR-009), SOLID principles
- [Source: docs/epics.md#EPIC-5R] - Phase 4: Presentation Layer (8 pts)
- [Source: docs/stories/story-5.1-domain-value-objects.md] - Domain value objects (Priority, Status, EnergyLevel, TimeBlock)
- [Source: docs/stories/story-5.2-task-entity.md] - Task entity structure
- [Source: docs/stories/story-6.1-task-management-use-cases.md] - Application layer pattern
- [Source: docs/solution-architecture.md] - Rich CLI formatting standards

## Dev Agent Record

### Context Reference

- `docs/stories/story-context-6.4-create-formatters.xml` (Generated 2025-10-25)

### Agent Model Used

<!-- Will be filled by DEV agent -->

### Debug Log References

### Completion Notes List

### File List
