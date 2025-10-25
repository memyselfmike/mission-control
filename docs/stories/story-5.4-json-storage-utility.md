# Story 5.4: Create JSON Storage Utility

Status: Ready for Review

## Story

As a **developer**,
I want **a low-level JSON storage utility with robust error handling and atomic writes**,
so that **all repository implementations can safely persist data without duplicating file I/O logic**.

## Acceptance Criteria

1. **JSON File I/O**: Utility provides `read_json(path)` and `write_json(path, data)` methods
   - Handles missing files gracefully (returns None or empty dict)
   - Validates JSON structure on read
   - Pretty-prints JSON on write (indent=2)
   - Atomic writes (write to temp file, then rename)

2. **JSONL Operations**: Utility provides `append_jsonl(path, entry)` method
   - Appends single-line JSON entries to log files
   - Creates file if it doesn't exist
   - Thread-safe appends
   - Validates entry is JSON-serializable before writing

3. **Backup on Write**: All write operations create automatic backups
   - Backup naming: `{filename}.backup.{timestamp}.json`
   - Configurable retention (default: keep last 5 backups)
   - Backup cleanup runs automatically during writes

4. **Error Handling**: Comprehensive error handling for all file operations
   - JSONDecodeError → log warning, return None or raise custom exception
   - PermissionError → raise with helpful message
   - FileNotFoundError → handle gracefully based on operation
   - IOError → log and re-raise with context

5. **Type Safety**: Full type hints throughout
   - Type: `JsonDict = Dict[str, Any]`
   - Methods accept/return JsonDict or None
   - Pydantic models supported (via `.dict()`)

6. **Logging**: Structured logging for all operations
   - INFO: successful reads/writes with file paths
   - WARNING: recoverable errors (missing files, invalid JSON)
   - ERROR: unrecoverable errors with stack traces
   - DEBUG: detailed operation info (file sizes, backup counts)

7. **Test Coverage**: 15+ tests covering all functionality
   - Happy path: read/write/append operations
   - Error cases: invalid JSON, missing files, permission errors
   - Edge cases: empty files, corrupted data, concurrent writes
   - Backup functionality: creation, retention, cleanup
   - Thread safety: concurrent append operations

## Tasks / Subtasks

- [x] Task 1: Create infrastructure persistence module structure (AC: #1, #5)
  - [x] Create `src/infrastructure/persistence/__init__.py`
  - [x] Create `src/infrastructure/persistence/json_storage.py`
  - [x] Create `src/infrastructure/persistence/exceptions.py` (custom exceptions)
  - [x] Add type aliases: `JsonDict`, `JsonList`, `JsonValue`

- [x] Task 2: Implement JSON file read operations (AC: #1, #4, #6)
  - [x] Implement `read_json(path: Path) -> Optional[JsonDict]`
  - [x] Handle `FileNotFoundError` → return None
  - [x] Handle `JSONDecodeError` → log warning, return None
  - [x] Handle `PermissionError` → raise with helpful message
  - [x] Add structured logging (INFO/WARNING/ERROR)

- [x] Task 3: Implement JSON file write operations (AC: #1, #3, #4, #6)
  - [x] Implement `write_json(path: Path, data: JsonDict, backup: bool = True)`
  - [x] Create parent directories if needed
  - [x] Write to temp file first (atomic write pattern)
  - [x] Rename temp → target (atomic operation)
  - [x] Create backup before write (if enabled)
  - [x] Add structured logging

- [x] Task 4: Implement backup functionality (AC: #3, #6)
  - [x] Implement `_create_backup(path: Path) -> Path`
  - [x] Backup naming: `{filename}.backup.{timestamp}.json`
  - [x] Implement `_cleanup_old_backups(path: Path, keep: int = 5)`
  - [x] Auto-cleanup during writes
  - [x] Add DEBUG logging for backup operations

- [x] Task 5: Implement JSONL operations (AC: #2, #4, #6)
  - [x] Implement `append_jsonl(path: Path, entry: JsonDict)`
  - [x] Create file if doesn't exist
  - [x] Thread-safe append (use file locking or atomic operations)
  - [x] Validate entry is JSON-serializable before write
  - [x] Add structured logging

- [x] Task 6: Add custom exceptions (AC: #4)
  - [x] `StorageException` (base class)
  - [x] `InvalidJsonError` (subclass of StorageException)
  - [x] `StoragePermissionError` (subclass of StorageException)
  - [x] All exceptions include helpful error messages

- [x] Task 7: Add logging configuration (AC: #6)
  - [x] Configure module logger: `logger = logging.getLogger(__name__)`
  - [x] Use structured logging with context (file paths, operation types)
  - [x] Log levels: INFO (success), WARNING (recoverable), ERROR (fatal), DEBUG (detailed)

- [x] Task 8: Create comprehensive test suite (AC: #7)
  - [x] Test `read_json`: happy path, missing file, invalid JSON, permission error
  - [x] Test `write_json`: happy path, atomic write, backup creation, directory creation
  - [x] Test `append_jsonl`: happy path, file creation, thread safety, invalid data
  - [x] Test backup functionality: creation, retention, cleanup
  - [x] Test error handling: all exception types, edge cases
  - [x] Integration tests: full read-modify-write cycles

## Dev Notes

### Architecture Context

**Layer**: Infrastructure Layer (mission-control/src/infrastructure/persistence/)

**Dependencies**:
- Domain Layer: NONE (infrastructure is lowest level utility)
- Standard Library: `json`, `pathlib`, `datetime`, `logging`, `tempfile`, `threading`
- Type System: `typing.Dict`, `typing.Any`, `typing.Optional`

**Hexagonal Architecture Compliance**:
- This is a LOW-LEVEL UTILITY in the infrastructure layer
- Has ZERO dependencies on domain or application layers
- Repository implementations will depend on this (not vice versa)
- Pure Python, no framework dependencies

### Implementation Patterns

**Atomic Writes** (prevent corruption):
```python
def write_json(path: Path, data: JsonDict, backup: bool = True) -> None:
    if backup and path.exists():
        _create_backup(path)

    temp_path = path.parent / f".{path.name}.tmp"
    temp_path.write_text(json.dumps(data, indent=2))
    temp_path.rename(path)  # Atomic operation on most filesystems
```

**Thread-Safe JSONL Appends**:
```python
_jsonl_lock = threading.Lock()

def append_jsonl(path: Path, entry: JsonDict) -> None:
    with _jsonl_lock:
        with open(path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
```

**Error Handling**:
```python
try:
    data = json.loads(path.read_text())
    return data
except FileNotFoundError:
    logger.info(f"File not found: {path}, returning None")
    return None
except JSONDecodeError as e:
    logger.warning(f"Invalid JSON in {path}: {e}")
    raise InvalidJsonError(f"Failed to parse {path}") from e
```

### Testing Strategy

**Test Structure**: `tests/infrastructure/persistence/test_json_storage.py`

**Test Categories**:
1. **Unit Tests** (12 tests):
   - `read_json`: 3 tests (success, missing, invalid)
   - `write_json`: 4 tests (success, atomic, backup, directory creation)
   - `append_jsonl`: 3 tests (success, creation, thread-safe)
   - Backup: 2 tests (creation, cleanup)

2. **Integration Tests** (3 tests):
   - Full read-modify-write cycle
   - Concurrent append operations
   - Backup recovery scenario

3. **Edge Cases** (3 tests):
   - Empty JSON files
   - Corrupted data mid-file
   - Permission errors (simulate with mocks)

**Coverage Target**: 100% (this is a critical utility)

### File Structure

```
mission-control/
├── src/
│   └── infrastructure/
│       └── persistence/
│           ├── __init__.py          # Export JsonStorage, exceptions
│           ├── json_storage.py      # Main implementation (200-250 lines)
│           └── exceptions.py        # Custom exception classes (30 lines)
└── tests/
    └── infrastructure/
        └── persistence/
            └── test_json_storage.py # Test suite (400-500 lines)
```

### API Interface

```python
from pathlib import Path
from typing import Dict, Any, Optional

JsonDict = Dict[str, Any]

class JsonStorage:
    """Low-level JSON storage utility with atomic writes and backups."""

    @staticmethod
    def read_json(path: Path) -> Optional[JsonDict]:
        """Read JSON file, return None if missing."""
        ...

    @staticmethod
    def write_json(path: Path, data: JsonDict, backup: bool = True) -> None:
        """Write JSON file atomically with optional backup."""
        ...

    @staticmethod
    def append_jsonl(path: Path, entry: JsonDict) -> None:
        """Append JSON line to JSONL file (thread-safe)."""
        ...

    @staticmethod
    def _create_backup(path: Path) -> Path:
        """Create timestamped backup of file."""
        ...

    @staticmethod
    def _cleanup_old_backups(path: Path, keep: int = 5) -> None:
        """Keep only N most recent backups."""
        ...
```

### References

- [Source: docs/epics.md#EPIC-5R] - Phase 2: Infrastructure (Story 5.4)
- [Source: docs/solution-architecture.md#4-data-architecture] - File-based persistence strategy
- [Source: CLAUDE.md#9-quality-standards] - Error handling, type hints, docstrings required
- [Source: docs/stories/story-5.3-repository-interfaces.md] - Repository interfaces that will use this utility

## Dev Agent Record

### Context Reference

- `docs/stories/story-context-5.4-json-storage-utility.xml`

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

No debug logs required - implementation was straightforward following the documented patterns.

### Completion Notes List

**Implementation Summary:**
- Created complete JSON storage utility with atomic writes, backup management, and comprehensive error handling
- All 7 acceptance criteria met and validated with tests
- 32 tests implemented (exceeds 15+ requirement), all passing at 100%
- Zero regressions in existing test suite (613 tests still passing)
- Thread-safe JSONL operations using locks
- Atomic write pattern using temp file + rename
- Automatic backup creation with configurable retention (default: 5 backups)
- Structured logging throughout (INFO/WARNING/ERROR/DEBUG levels)
- Full type hints and comprehensive docstrings
- Custom exception classes for better error handling

**Architecture Compliance:**
- Infrastructure layer utility with zero dependencies on domain/application layers
- Pure Python implementation using only standard library
- Follows Hexagonal Architecture principles
- Ready for use by repository implementations in Stories 5.5 and 5.6

**Performance:**
- Atomic writes prevent data corruption
- Thread-safe appends support concurrent access
- Backup cleanup runs automatically (no manual maintenance needed)
- Unicode handling verified with full UTF-8 support

### File List

**Created:**
- `mission-control/src/infrastructure/persistence/__init__.py` - Module exports
- `mission-control/src/infrastructure/persistence/exceptions.py` - Custom exception classes (18 lines)
- `mission-control/src/infrastructure/persistence/json_storage.py` - Main JSON storage utility (250 lines)
- `mission-control/tests/infrastructure/persistence/__init__.py` - Test module init
- `mission-control/tests/infrastructure/persistence/test_json_storage.py` - Comprehensive test suite (550+ lines, 32 tests)

**Modified:**
- None (no existing files modified)

## Change Log

- **2025-10-25 09:00**: Story created (Draft status). Part of EPIC-5R Phase 2: Infrastructure. Low-level JSON storage utility for all repository implementations. 15+ tests planned, 100% coverage target.
- **2025-10-25 09:15**: Story marked Ready after SM validation.
- **2025-10-25 09:20**: Story context generated (story-context-5.4-json-storage-utility.xml).
- **2025-10-25 12:35**: Implementation complete. All 8 tasks complete, 32 tests passing (100%), zero regressions. Status: Ready for Review.
