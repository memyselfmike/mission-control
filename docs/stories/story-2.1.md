# STORY-2.1: Business Context Storage

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
**I want to** store and retrieve business context information persistently
**So that** I can remember company details, values, strategic direction, and current goals across sessions without asking redundant questions.

---

## Description

Implement a business context storage system that persists key company information to `data/memory/business_context.json`. This enables agents to maintain awareness of:

- Company information (name, industry, size, mission)
- Core values and principles
- Strategic direction and vision
- Current goals and priorities
- Key people and roles

The system should support both automatic capture (via hooks detecting context mentions) and manual storage (user explicitly provides context). Data must be human-readable JSON and manually editable.

---

## Context & Dependencies

### Prerequisites
- **STORY-1.3:** Basic conversation loop implemented (main.py)
- **STORY-1.5:** Hooks system operational (.claude/hooks/)
- **STORY-1.6:** Chief of Staff persona defined (loads memory on startup)

### Related Stories
- **STORY-2.2:** Conversation History Logging (complements this with interaction logs)
- **STORY-2.3:** Preference Learning System (builds on context storage patterns)
- **STORY-2.4:** Memory Loading on Startup (consumes business_context.json)

### Architecture References
- **Solution Architecture:** Section 7 (Memory and Persistence)
- **Data Architecture:** `data/memory/` directory structure
- **PRD Requirements:** FR-6 (Business Context Storage)

---

## Acceptance Criteria

### AC-1: Context Storage Module
**Given** the application is running
**When** business context is captured or updated
**Then** the system shall store it to `data/memory/business_context.json` with proper structure

**Validation:**
- JSON file created in correct location
- File contains: `company_info`, `values`, `strategic_direction`, `current_goals` sections
- Data persists across application restarts
- File is human-readable and properly formatted

### AC-2: Context Capture via Conversation
**Given** a user provides business context in conversation
**When** Alex (Chief of Staff) detects context information
**Then** the system shall offer to save it to memory

**Validation:**
- User mentions company name → Captured to `company_info.name`
- User states values → Captured to `values[]` array
- User describes vision → Captured to `strategic_direction`
- Confirmation message displayed to user

### AC-3: Manual Context Update
**Given** a user wants to update business context
**When** they request to add/modify context information
**Then** the system shall update `business_context.json` and confirm

**Validation:**
- User can add new company information
- User can update existing values
- User can modify strategic direction
- Changes are immediately persisted
- Confirmation includes what was changed

### AC-4: Context Retrieval API
**Given** business context exists in memory
**When** agents need to access context
**Then** the system shall provide a Python API to load context

**Validation:**
- `load_business_context()` function exists in `src/memory.py`
- Returns dict with all context sections
- Handles missing file gracefully (returns empty structure)
- Loads on application startup automatically

### AC-5: Data Structure Validation
**Given** business context is being saved
**When** the data is written to JSON
**Then** it shall conform to the defined schema

**Validation:**
```json
{
  "company_info": {
    "name": "string",
    "industry": "string",
    "size": "string",
    "mission": "string",
    "founded": "string (optional)"
  },
  "values": ["array of strings"],
  "strategic_direction": {
    "vision_10_year": "string (optional)",
    "vision_3_year": "string (optional)",
    "vision_1_year": "string (optional)",
    "focus_areas": ["array of strings"]
  },
  "current_goals": {
    "quarter": "string (e.g., '2025-Q4')",
    "rocks": ["array of goal strings"]
  },
  "last_updated": "ISO 8601 timestamp"
}
```

### AC-6: Privacy & Security
**Given** sensitive business data is stored
**When** context is written to file
**Then** appropriate privacy measures shall be enforced

**Validation:**
- File stored in `data/` directory (gitignored)
- No data sent to external services without user action
- File permissions set to owner-only on Unix systems
- User controls what is saved (explicit consent)

---

## Technical Implementation Notes

### File Structure
**Location:** `D:\Mission Control\mission-control\data\memory\business_context.json`

**Module:** Create `src/memory.py` with functions:
- `load_business_context()` → dict
- `save_business_context(context: dict)` → bool
- `update_business_context(section: str, data: dict)` → bool
- `get_context_summary()` → str (for display to user)

### Integration Points

**1. Startup Loading (main.py):**
```python
from memory import load_business_context

# In main() function, before conversation loop:
context = load_business_context()
if context:
    # Pass to Chief of Staff system prompt
    initial_context = f"Business context: {get_context_summary()}"
```

**2. Hook for Context Detection (.claude/hooks/context_detector.py):**
```python
# Monitors Stop events for business context mentions
# Triggers save_business_context() when detected
# Examples: "Our company is...", "Our values are...", "Our Q4 goals..."
```

**3. Chief of Staff Persona:**
- Updated to recognize context capture opportunities
- Ask user permission before saving
- Confirm what was saved

### Error Handling
- Missing directory → Create `data/memory/` automatically
- Corrupted JSON → Backup old file, create fresh one
- Missing fields → Use default empty structure
- File write errors → Log error, notify user, retry once

### Testing Strategy

**Unit Tests:**
- Test `load_business_context()` with missing file
- Test `save_business_context()` creates proper JSON
- Test `update_business_context()` modifies specific sections
- Test schema validation
- Test file creation in `data/memory/`

**Integration Tests:**
- Full conversation flow with context capture
- Startup with existing context file
- Context update via conversation
- Manual file edit, then reload

**User Acceptance Testing:**
1. User provides company info → Verify saved correctly
2. User restarts application → Verify context remembered
3. User manually edits JSON → Verify changes persist
4. User adds values → Verify appended to array

---

## Definition of Done

- [ ] `src/memory.py` module created with all required functions
- [ ] `business_context.json` schema defined and validated
- [ ] Context loading integrated into `main.py` startup
- [ ] Context detector hook created in `.claude/hooks/context_detector.py`
- [ ] Chief of Staff persona updated to recognize context opportunities
- [ ] All 6 acceptance criteria validated and passing
- [ ] Unit tests written and passing (100% coverage for memory.py)
- [ ] Integration tests passing
- [ ] User acceptance testing complete with Mike
- [ ] Code reviewed and approved
- [ ] Documentation updated (README.md with memory system section)
- [ ] Git commit created with proper message
- [ ] Sprint backlog updated (Story 2.1 marked complete)

---

## Out of Scope

The following are explicitly **NOT** part of this story:

- **Conversation history logging** (handled in STORY-2.2)
- **Preference learning** (handled in STORY-2.3)
- **Automatic memory pruning** (handled in STORY-2.5)
- **Multi-user support** (future phase)
- **Encrypted storage** (not required for MVP - local files only)
- **Cloud sync** (against privacy-first philosophy)
- **Version history for context** (nice-to-have, not MVP)

---

## Testing Scenarios

### Scenario 1: First-Time Context Capture
**Given:** Fresh installation with no business_context.json
**When:** User says "We're a SaaS company in the HR tech space"
**Then:**
1. Alex recognizes company information
2. Asks: "Should I remember this? (Your company: SaaS in HR tech)"
3. User confirms
4. File created with company_info populated
5. Confirmation: "Got it! I've saved your company info to memory."

### Scenario 2: Adding Values Over Time
**Given:** Existing business_context.json with company info
**When:** User says "Our core values are integrity, innovation, and customer obsession"
**Then:**
1. Alex detects values statement
2. Offers to save to memory
3. Appends to `values[]` array
4. Displays updated values list

### Scenario 3: Context at Startup
**Given:** business_context.json exists with complete context
**When:** User starts Mission Control
**Then:**
1. Context loaded automatically
2. Alex greets user with context awareness: "Good morning! How can I help with [Company Name] today?"
3. No redundant questions about company basics

### Scenario 4: Manual JSON Edit
**Given:** User wants to manually update context
**When:** User edits `business_context.json` in text editor and saves
**Then:**
1. Next conversation, Alex loads updated context
2. Responds based on new information
3. No errors from manual edits (as long as valid JSON)

### Scenario 5: Strategic Direction Update
**Given:** Quarterly planning conversation
**When:** User describes Q4 2025 goals
**Then:**
1. Alex offers to save to `current_goals.rocks`
2. Updates quarter field to "2025-Q4"
3. Stores goals array
4. Future conversations reference these goals

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| JSON corruption from manual edits | High | Medium | Validate JSON on load, backup before write |
| Context grows too large | Medium | High | Document in STORY-2.5 (pruning), warn if >10KB |
| User forgets what's stored | Low | Medium | Provide `show_context()` command to display |
| File permissions on Windows | Medium | Low | Test on Windows, document any issues |
| Concurrent access issues | High | Low | Single-user app, no concurrency expected |

---

## Success Metrics

- **Primary:** Business context persists across 100% of application restarts
- **User Experience:** Zero redundant questions about company basics after context captured
- **Performance:** Context load time <100ms on startup
- **Data Quality:** Context summary displayable in <200 characters for quick reference
- **User Satisfaction:** Mike confirms context capture feels natural (not robotic)

---

## Notes

- This story lays foundation for all memory features in EPIC-2
- Keep context structure flexible - will evolve as users add more detail
- Consider adding `version` field to JSON for future schema migrations
- Business context complements conversation history (separate concerns)
- Focus on company-level info, not user preferences (that's STORY-2.3)

---

## Story Dependencies Graph

```
STORY-1.5 (Hooks) ────┐
                       ├──> STORY-2.1 (Business Context) ──┐
STORY-1.6 (Persona) ──┘                                     │
                                                             ├──> STORY-2.4 (Startup Loading)
STORY-2.2 (History) ────────────────────────────────────────┤
                                                             │
STORY-2.3 (Preferences) ────────────────────────────────────┘
```

---

**Status:** Ready for `story-ready` workflow (Bob review and approval)
**Next Step:** Execute `story-ready` workflow to validate completeness and approve for development
