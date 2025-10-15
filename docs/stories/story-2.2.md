# STORY-2.2: Conversation History Logging

**Epic:** EPIC-2 (Persistent Memory System)
**Story Points:** 5
**Priority:** P0 (Must Have - MVP Blocker)
**Sprint:** Sprint 1
**Status:** Draft
**Created:** 2025-10-15
**Author:** Bob (Scrum Master)

---

## User Story

**As a** Chief of Staff agent (Alex)
**I want to** log all conversation interactions to structured history files
**So that** I can reference past conversations, track interaction patterns, and provide context-aware responses across sessions.

---

## Description

Implement a conversation history logging system that captures all agent interactions (user messages and agent responses) in timestamped JSONL (JSON Lines) format. Each entry includes metadata (timestamp, agent name, message role, content), enabling conversation replay, pattern analysis, and context loading for future sessions.

The system should log conversations in real-time via the existing `log_agent_actions.py` hook, organize logs by date, and provide API functions to load/query conversation history.

---

## Context & Dependencies

### Prerequisites
- **STORY-1.3:** Basic conversation loop implemented (main.py)
- **STORY-1.5:** Hooks system operational (.claude/hooks/log_agent_actions.py exists)
- **STORY-2.1:** Business Context Storage complete (memory.py module exists)

### Related Stories
- **STORY-2.3:** Preference Learning System (analyzes conversation history for preferences)
- **STORY-2.4:** Memory Loading on Startup (loads conversation summaries)
- **STORY-2.5:** Memory Pruning Strategy (manages conversation history growth)

### Architecture References
- **Solution Architecture:** Section 7 (Memory and Persistence)
- **Data Architecture:** `data/memory/interaction_logs/` directory structure
- **PRD Requirements:** FR-7 (Conversation History Persistence)

---

## Acceptance Criteria

### AC-1: JSONL Log File Creation
**Given** the application is running and conversations are happening
**When** a user sends a message or agent responds
**Then** the system shall log each interaction to `data/memory/interaction_logs/{YYYY-MM-DD}.jsonl`

**Validation:**
- JSONL file created with current date in filename (e.g., `2025-10-15.jsonl`)
- Each line is valid JSON (can be parsed independently)
- File organized by date (one file per day)
- Directory `data/memory/interaction_logs/` created automatically
- File is append-only (never overwrites existing entries)

### AC-2: Log Entry Structure
**Given** an interaction is being logged
**When** the log entry is written
**Then** it shall conform to the defined JSONL schema

**Validation:**
```json
{
  "timestamp": "2025-10-15T14:32:15.123456",
  "session_id": "uuid-string",
  "agent": "Alex",
  "role": "assistant",
  "content": "The agent's response text...",
  "metadata": {
    "model": "claude-sonnet-4",
    "turn_number": 5,
    "tokens": 245
  }
}
```

**Required Fields:**
- `timestamp`: ISO 8601 format with microseconds
- `session_id`: UUID for current conversation session
- `agent`: Agent name ("Alex", "Jordan", "Quinn", etc.)
- `role`: "user" or "assistant"
- `content`: Full message text
- `metadata`: Optional dict with model, turn_number, token count

### AC-3: User Message Logging
**Given** a user sends a message
**When** the message is processed
**Then** the system shall log the user message with role="user"

**Validation:**
- User messages logged before agent response
- `agent` field set to "User" or user's name if known
- `role` field set to "user"
- Full message content captured
- Timestamp reflects message send time

### AC-4: Agent Response Logging
**Given** an agent (Chief of Staff or specialist) responds
**When** the response is completed
**Then** the system shall log the agent response with role="assistant"

**Validation:**
- Agent name captured correctly ("Alex", "Jordan", "Quinn", "Taylor", "Sam", "Morgan")
- `role` field set to "assistant"
- Full response content captured
- Timestamp reflects response completion time
- Turn number increments correctly

### AC-5: History Retrieval API
**Given** conversation history exists in JSONL files
**When** agents or system need to access history
**Then** the system shall provide Python API functions to query logs

**Validation:**
- `load_conversation_history(date=None, limit=None)` → List[dict]
- `get_recent_interactions(hours=24, limit=50)` → List[dict]
- `search_conversations(query: str, days=7)` → List[dict]
- `get_session_history(session_id: str)` → List[dict]
- Functions handle missing files gracefully (return empty list)

### AC-6: Hook Integration
**Given** the `log_agent_actions.py` hook exists
**When** Stop event fires (agent completes response)
**Then** the hook shall append log entry to current date's JSONL file

**Validation:**
- Hook receives agent response text via stdin or argv
- Hook extracts agent name, timestamp, content
- Hook appends to JSONL file without blocking conversation
- Hook execution completes in <200ms
- Hook errors logged but don't crash main app

### AC-7: Privacy & Performance
**Given** conversation history contains sensitive data
**When** logs are written and stored
**Then** privacy and performance measures shall be enforced

**Validation:**
- Files stored in `data/memory/interaction_logs/` (gitignored)
- File permissions owner-only on Unix (0o600)
- JSONL format enables streaming (low memory usage)
- Old logs retained (no automatic deletion - handled in STORY-2.5)
- No data sent to external services

---

## Technical Implementation Notes

### File Structure

**Location:** `D:\Mission Control\mission-control\data\memory\interaction_logs\{YYYY-MM-DD}.jsonl`

**Module:** Extend `src/memory.py` with history functions:
- `log_interaction(agent: str, role: str, content: str, metadata: dict = None)` → bool
- `load_conversation_history(date: str = None, limit: int = None)` → List[dict]
- `get_recent_interactions(hours: int = 24, limit: int = 50)` → List[dict]
- `search_conversations(query: str, days: int = 7)` → List[dict]
- `get_session_history(session_id: str)` → List[dict]

### Integration Points

**1. Hook Enhancement (.claude/hooks/log_agent_actions.py):**
```python
# Current hook logs to files - enhance to use JSONL format
import sys
import json
from pathlib import Path
from datetime import datetime

# Receive agent response from stdin
response_data = json.loads(sys.stdin.read())

# Extract fields
agent_name = response_data.get('agent', 'Alex')
content = response_data.get('content', '')
timestamp = datetime.now().isoformat()

# Create log entry
log_entry = {
    "timestamp": timestamp,
    "session_id": os.getenv('SESSION_ID', 'unknown'),
    "agent": agent_name,
    "role": "assistant",
    "content": content,
    "metadata": {
        "model": response_data.get('model', 'unknown'),
        "turn_number": response_data.get('turn', 0)
    }
}

# Append to today's log file
log_file = Path(f"data/memory/interaction_logs/{datetime.now().strftime('%Y-%m-%d')}.jsonl")
log_file.parent.mkdir(parents=True, exist_ok=True)

with open(log_file, 'a', encoding='utf-8') as f:
    f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
```

**2. Session ID Tracking (main.py):**
```python
import uuid

# At start of conversation
session_id = str(uuid.uuid4())
os.environ['SESSION_ID'] = session_id

# Pass to hooks via environment variable
```

**3. User Message Logging (main.py):**
```python
from memory import log_interaction

# When user sends message
user_message = input("You: ")
log_interaction(agent="User", role="user", content=user_message)
```

### Error Handling

- Missing directory → Create `data/memory/interaction_logs/` automatically
- Corrupted JSONL → Skip invalid lines, log warning, continue
- File write errors → Retry once, log error, continue (don't block conversation)
- Disk space full → Log error, gracefully degrade (stop logging but don't crash)
- Permission errors → Log error, attempt to fix permissions, continue

### Performance Considerations

- **Append-only writes:** O(1) write performance
- **JSONL format:** Streaming reads (don't load entire file into memory)
- **Daily rotation:** Prevents single file from growing too large
- **Lazy loading:** Only load history when explicitly requested
- **Indexed search:** Use grep/ripgrep for fast text search (no database needed for MVP)

### Testing Strategy

**Unit Tests:**
- Test `log_interaction()` creates valid JSONL
- Test `load_conversation_history()` parses JSONL correctly
- Test `get_recent_interactions()` filters by time range
- Test `search_conversations()` finds matching content
- Test `get_session_history()` returns session-specific logs
- Test missing file handling (returns empty list)
- Test corrupted JSONL line handling (skips line, continues)

**Integration Tests:**
- Full conversation flow with logging
- Multiple sessions in same day
- Conversation spanning multiple days
- Hook integration with real Stop event
- Search across multiple log files

**User Acceptance Testing:**
1. Have conversation → Verify all turns logged
2. Restart app → Load recent history and verify continuity
3. Search for keyword → Verify correct results returned
4. Multiple sessions → Verify session IDs distinct
5. Manual JSONL edit → Verify system handles gracefully

---

## Definition of Done

- [ ] `src/memory.py` extended with 5 history functions
- [ ] `.claude/hooks/log_agent_actions.py` updated to write JSONL format
- [ ] Session ID tracking added to `main.py`
- [ ] User message logging integrated into conversation loop
- [ ] JSONL schema defined and validated
- [ ] All 7 acceptance criteria validated and passing
- [ ] Unit tests written and passing (15+ tests for history functions)
- [ ] Integration tests passing (full conversation logging)
- [ ] User acceptance testing complete with Mike
- [ ] Code reviewed and approved
- [ ] Documentation updated (README with conversation history section)
- [ ] Git commit created with proper message
- [ ] Sprint backlog updated (Story 2.2 marked complete)

---

## Out of Scope

The following are explicitly **NOT** part of this story:

- **Conversation summarization** (future enhancement - STORY-2.4 may include)
- **Preference extraction from history** (handled in STORY-2.3)
- **Automatic history pruning** (handled in STORY-2.5)
- **Full-text search with database** (JSONL + grep sufficient for MVP)
- **Conversation analytics/dashboards** (future enhancement)
- **Export to other formats** (JSONL is export-ready, no conversion needed)
- **Encryption of logs** (not required for MVP - local files only)
- **Multi-user conversation tracking** (single-user app for MVP)

---

## Testing Scenarios

### Scenario 1: First Conversation Logging
**Given:** Fresh installation with no log files
**When:** User has first conversation with Alex
**Then:**
1. Directory `data/memory/interaction_logs/` created
2. File `2025-10-15.jsonl` created (current date)
3. User message logged with role="user"
4. Alex response logged with role="assistant"
5. Both entries have same session_id
6. Timestamps are sequential

### Scenario 2: Multi-Day Conversation
**Given:** Logs exist for 2025-10-14
**When:** User has conversation on 2025-10-15
**Then:**
1. New file `2025-10-15.jsonl` created
2. Previous file `2025-10-14.jsonl` unchanged
3. `get_recent_interactions(hours=48)` returns entries from both files
4. Session IDs are different across days

### Scenario 3: Specialist Delegation Logging
**Given:** User asks strategic question
**When:** Alex delegates to Jordan (Strategist)
**Then:**
1. User question logged with agent="User"
2. Alex handoff logged with agent="Alex"
3. Jordan response logged with agent="Jordan"
4. All entries have same session_id
5. Turn numbers increment correctly (1, 2, 3)

### Scenario 4: Conversation History Search
**Given:** 7 days of conversation logs exist
**When:** User searches for keyword "quarterly goals"
**Then:**
1. `search_conversations("quarterly goals", days=7)` called
2. All matching entries returned across all log files
3. Results sorted by timestamp (newest first)
4. Entries include full context (agent, timestamp, content)

### Scenario 5: Session Replay
**Given:** User had conversation yesterday
**When:** User wants to review yesterday's session
**Then:**
1. `get_session_history(session_id)` called
2. All entries from that session returned in order
3. Turn numbers sequential (1, 2, 3, ...)
4. Both user and assistant messages included
5. Can replay conversation chronologically

### Scenario 6: Corrupted Log Handling
**Given:** One line in JSONL file is malformed
**When:** System loads conversation history
**Then:**
1. `load_conversation_history()` parses valid lines
2. Skips corrupted line with warning logged
3. Returns all valid entries
4. No exception thrown

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| JSONL files grow very large | High | High | Daily rotation, pruning in STORY-2.5 |
| Disk space exhaustion | High | Low | Monitor disk usage, warn if low, graceful degradation |
| Performance degradation with history loading | Medium | Medium | Lazy loading, limit parameter, streaming reads |
| Hook execution slowdown | Medium | Low | Keep hook <200ms, async write, no blocking |
| Session ID collision | Low | Very Low | UUID v4 has astronomically low collision rate |
| Log file corruption from concurrent writes | Medium | Low | Single-threaded app, append-only writes |

---

## Success Metrics

- **Primary:** 100% of conversation turns logged successfully
- **Performance:** Log write time <50ms, no conversation latency
- **Search:** Keyword search completes in <1 second for 7 days of logs
- **Reliability:** Zero data loss, zero crashes from logging errors
- **User Experience:** Mike confirms logging is transparent (not noticeable)
- **Data Quality:** JSONL files manually reviewable and editable

---

## Notes

- JSONL format chosen for simplicity, streaming, human-readability
- One file per day balances file size vs. file count
- Session ID enables tracking conversations across app restarts
- Hook approach ensures logging doesn't block main conversation
- grep/ripgrep sufficient for search - no database complexity needed for MVP
- Story 2.2 complements Story 2.1 (business context) - different purposes:
  - Story 2.1: High-level business info (company, values, goals)
  - Story 2.2: Interaction history (who said what when)

---

## Story Dependencies Graph

```
STORY-1.3 (Conversation Loop) ────┐
                                   ├──> STORY-2.2 (Conversation History) ──┐
STORY-1.5 (Hooks) ────────────────┘                                         │
                                                                             ├──> STORY-2.4 (Startup Loading)
STORY-2.1 (Business Context) ───────────────────────────────────────────────┤
                                                                             │
STORY-2.3 (Preferences) ────────────────────────────────────────────────────┘
```

---

## Dev Agent Record

### Context Reference
- **Story Context File:** Will be generated via `story-context` workflow
- **Status:** Story drafted, ready for `story-ready` validation

### Implementation Plan (To Be Executed)
1. Extend `src/memory.py` with history functions (5 functions)
2. Update `.claude/hooks/log_agent_actions.py` for JSONL format
3. Add session ID tracking to `main.py`
4. Integrate user message logging in conversation loop
5. Create comprehensive test suite (15+ tests)
6. Validate all 7 acceptance criteria

**Estimated Implementation Time:** 2-3 hours
**Test Development Time:** 1-2 hours
**Total Story Time:** 3-5 hours

---

_Story 2.2 provides structured conversation history logging, enabling agents to reference past interactions and users to search conversation logs. This complements Story 2.1's business context storage._
