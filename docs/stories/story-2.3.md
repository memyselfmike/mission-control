# STORY-2.3: Preference Learning System

**Epic:** EPIC-2 (Persistent Memory System)
**Story Points:** 6
**Priority:** P0 (Must Have - MVP Blocker)
**Sprint:** Sprint 1
**Status:** Ready
**Created:** 2025-10-15
**Approved:** 2025-10-15
**Author:** Bob (Scrum Master)
**Approved By:** Bob (Scrum Master)

---

## User Story

**As a** Chief of Staff agent (Alex)
**I want to** learn and remember user preferences from conversations
**So that** I can provide increasingly personalized and relevant responses without asking the same questions repeatedly.

---

## Description

Implement a preference learning system that analyzes conversation history to identify, extract, and persist user preferences including communication style, preferred frameworks, decision-making patterns, work habits, and domain-specific preferences. The system should detect preferences both explicitly stated ("I prefer OKRs over SMART goals") and implicitly demonstrated (consistently choosing morning planning sessions).

The learned preferences should be stored in a structured, human-readable format and automatically loaded on startup to inform agent behavior across all conversations.

---

## Context & Dependencies

### Prerequisites
- **STORY-2.1:** Business Context Storage complete (memory.py exists)
- **STORY-2.2:** Conversation History Logging complete (history API available)
- **STORY-1.3:** Basic conversation loop (agents can access history)

### Related Stories
- **STORY-2.4:** Memory Loading on Startup (loads preferences at app start)
- **STORY-2.5:** Memory Pruning Strategy (manages stale preferences)
- **STORY-4.5:** User Behavior Pattern Detection (uses preferences for insights)

### Architecture References
- **Solution Architecture:** Section 7 (Memory and Persistence)
- **Data Architecture:** `data/memory/user_preferences.json` structure
- **PRD Requirements:** FR-8 (Learned Preferences), FR-9 (Personalization)

---

## Acceptance Criteria

### AC-1: Preference Data Model
**Given** the system needs to store diverse user preferences
**When** preferences are saved to storage
**Then** the data model shall include the following categories:

**Validation:**
```json
{
  "communication_style": {
    "verbosity": "concise|detailed|balanced",
    "formality": "casual|professional|formal",
    "emoji_usage": "minimal|occasional|frequent",
    "response_style": "direct|socratic|collaborative"
  },
  "frameworks_and_methods": {
    "goal_setting": ["OKRs", "SMART", "Rocks"],
    "time_management": ["Eisenhower Matrix", "Time Blocking", "Pomodoro"],
    "strategic_planning": ["Vision/Traction", "Blue Ocean", "SWOT"]
  },
  "work_habits": {
    "preferred_planning_time": "morning|afternoon|evening",
    "meeting_preferences": "minimal|moderate|frequent",
    "decision_making_speed": "fast|deliberate|varies"
  },
  "agent_interactions": {
    "delegation_style": "autonomous|collaborative|directed",
    "feedback_frequency": "frequent|occasional|minimal",
    "preferred_agents": ["Alex", "Jordan", "Quinn"]
  },
  "domain_specific": {
    "industry": "SaaS|ecommerce|consulting|...",
    "role": "founder|executive|manager|...",
    "team_size": "solo|small|medium|large"
  },
  "last_updated": "ISO 8601 timestamp",
  "confidence_scores": {
    "communication_style": 0.85,
    "frameworks_and_methods": 0.62
  }
}
```

### AC-2: Explicit Preference Detection
**Given** a user makes an explicit preference statement
**When** the conversation contains phrases like "I prefer", "I like", "I always", "I usually"
**Then** the system shall extract and store the preference

**Validation:**
- Detect "I prefer OKRs" → `frameworks_and_methods.goal_setting: ["OKRs"]`
- Detect "I like concise responses" → `communication_style.verbosity: "concise"`
- Detect "I always plan in the morning" → `work_habits.preferred_planning_time: "morning"`
- Confidence score high (0.9+) for explicit statements
- Timestamps recorded for preference freshness

### AC-3: Implicit Preference Learning
**Given** conversation history shows repeated patterns
**When** analyzing historical interactions
**Then** the system shall infer implicit preferences from behavior patterns

**Validation:**
- 3+ morning planning sessions → infer `preferred_planning_time: "morning"`
- Consistently brief responses → infer `verbosity: "concise"`
- Frequent delegation to Jordan → add to `preferred_agents`
- Confidence score moderate (0.5-0.7) for implicit inferences
- Requires minimum 5 data points for pattern detection

### AC-4: Preference Storage and Retrieval
**Given** preferences have been learned
**When** saving to storage
**Then** preferences shall be persisted in `data/memory/user_preferences.json`

**Validation:**
- File created automatically with proper permissions (0o600 on Unix)
- JSON formatted with 4-space indentation (human-readable)
- Backup created before overwriting existing file
- `load_user_preferences()` function returns dict with all categories
- Missing file returns default empty structure (graceful handling)
- Corrupted JSON returns empty structure with warning logged

### AC-5: Preference Update API
**Given** new preferences need to be added or updated
**When** calling preference update functions
**Then** the system shall provide API for safe updates

**Validation:**
```python
# API functions required
update_preference(category: str, key: str, value: Any, confidence: float = 1.0) → bool
get_preference(category: str, key: str, default: Any = None) → Any
get_preferences_summary() → str  # Human-readable summary
get_preferences_for_prompt() → str  # Formatted for agent system prompts
merge_preferences(new_prefs: dict, overwrite: bool = False) → bool
```

### AC-6: Preference Analysis Hook
**Given** conversations complete
**When** Stop event fires
**Then** preference detection hook shall analyze conversation for new preferences

**Validation:**
- `.claude/hooks/preference_detector.py` hook created
- Hook analyzes last conversation turn for preference indicators
- Explicit statements detected with pattern matching
- Hook execution <500ms (no conversation blocking)
- Errors logged gracefully (no crashes)
- Updates `user_preferences.json` when preferences detected

### AC-7: Confidence Tracking and Decay
**Given** preferences may become stale over time
**When** preferences are stored
**Then** confidence scores shall be tracked and may decay

**Validation:**
- Each preference has associated confidence score (0.0-1.0)
- Explicit statements start at 0.9-1.0 confidence
- Implicit inferences start at 0.5-0.7 confidence
- Repeated confirmations increase confidence (max 1.0)
- Contradictions decrease confidence (min 0.0)
- Timestamps enable age-based decay (handled in STORY-2.5)

---

## Technical Implementation Notes

### File Structure

**Location:** `D:\Mission Control\mission-control\data\memory\user_preferences.json`

**Module:** Extend `src/memory.py` with preference functions:
- `load_user_preferences()` → dict
- `save_user_preferences(prefs: dict)` → bool
- `update_preference(category, key, value, confidence)` → bool
- `get_preference(category, key, default)` → Any
- `get_preferences_summary()` → str  (for display)
- `get_preferences_for_prompt()` → str  (for agent prompts)
- `merge_preferences(new_prefs, overwrite)` → bool
- `analyze_conversation_for_preferences(history: List[dict])` → dict  (detection logic)

### Integration Points

**1. Preference Detection Hook (.claude/hooks/preference_detector.py):**
```python
#!/usr/bin/env python3
"""
Hook: Preference Detector (Stop Event)

Analyzes completed conversations for explicit and implicit preferences.
Updates user_preferences.json when preferences detected.

Explicit patterns:
- "I prefer X"
- "I like Y"
- "I always Z"
- "I usually A"
- "I don't like B"

Implicit patterns (requires history analysis):
- Repeated time preferences
- Consistent communication style
- Framework usage patterns
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from memory import (
    load_user_preferences,
    load_conversation_history,
    update_preference,
    analyze_conversation_for_preferences
)

def main():
    try:
        # Get recent conversation history (last 10 interactions)
        history = load_conversation_history(limit=10)

        if not history:
            return

        # Analyze for preferences
        detected_prefs = analyze_conversation_for_preferences(history)

        if detected_prefs:
            # Load current preferences
            current_prefs = load_user_preferences()

            # Merge detected preferences
            for category, prefs in detected_prefs.items():
                for key, (value, confidence) in prefs.items():
                    update_preference(category, key, value, confidence)
                    print(f"✓ Learned preference: {category}.{key} = {value}", file=sys.stderr)

    except Exception as e:
        print(f"⚠️  Preference detection error: {e}", file=sys.stderr)
        # Don't crash - graceful degradation

if __name__ == "__main__":
    main()
```

**2. Preference Loading on Startup (main.py integration):**
```python
from memory import (
    load_business_context,
    load_user_preferences,
    get_context_for_prompt,
    get_preferences_for_prompt
)

# At startup, load both business context and preferences
business_context = load_business_context()
user_prefs = load_user_preferences()

# Include in system prompt
context_text = get_context_for_prompt()
prefs_text = get_preferences_for_prompt()

system_prompt = f"""You are Alex, Chief of Staff.

Business Context:
{context_text}

User Preferences:
{prefs_text}

Adapt your communication style and recommendations based on these preferences.
"""
```

**3. Explicit Preference Detection (Pattern Matching):**
```python
def analyze_conversation_for_preferences(history: List[dict]) -> dict:
    """
    Analyze conversation history for preference indicators.

    Returns:
        dict: Detected preferences by category with confidence scores

    Example:
        {
            "communication_style": {
                "verbosity": ("concise", 0.9)
            },
            "frameworks_and_methods": {
                "goal_setting": (["OKRs"], 0.95)
            }
        }
    """
    detected = {}

    # Explicit preference patterns
    explicit_patterns = [
        (r"I prefer (\w+)", "high_confidence"),
        (r"I like (\w+)", "high_confidence"),
        (r"I always (\w+)", "medium_confidence"),
        (r"I usually (\w+)", "medium_confidence"),
        (r"I don't like (\w+)", "high_confidence_negative")
    ]

    # Framework name patterns
    framework_keywords = {
        "OKRs": "goal_setting",
        "SMART goals": "goal_setting",
        "Rocks": "goal_setting",
        "Eisenhower": "time_management",
        "time blocking": "time_management"
    }

    # Scan history for patterns
    for entry in history:
        content = entry.get("content", "").lower()

        # Check explicit patterns
        for pattern, confidence_level in explicit_patterns:
            import re
            matches = re.findall(pattern, content)
            for match in matches:
                # Classify preference and add to detected
                pass  # Implementation details

    # Implicit pattern detection (analyze behavioral patterns)
    # - Count morning vs afternoon planning
    # - Measure average response length
    # - Track framework mentions
    # - Identify delegation patterns

    return detected
```

### Error Handling

- Missing file → Return empty default structure (don't crash)
- Corrupted JSON → Log warning, return empty structure
- Invalid preference values → Validate and reject with error
- Write failures → Retry once, log error, continue
- Detection failures → Log warning, don't update preferences

### Performance Considerations

- **Hook execution:** <500ms target (lightweight analysis)
- **Lazy loading:** Only load preferences when needed
- **Caching:** Cache preferences in memory during session
- **Incremental updates:** Don't rewrite entire file for single preference
- **Pattern matching:** Use compiled regex for efficiency

### Testing Strategy

**Unit Tests:**
- Test `load_user_preferences()` with missing/corrupted files
- Test `update_preference()` correctly merges values
- Test `get_preference()` with defaults
- Test preference format validation
- Test confidence score calculations
- Test explicit pattern detection regex
- Test implicit pattern inference logic

**Integration Tests:**
- Full conversation → preference detected → stored → loaded on restart
- Multiple explicit statements → confidence increases
- Contradictory statements → confidence decreases
- Hook integration with real Stop event
- Preferences used in agent system prompt

**User Acceptance Testing:**
1. State explicit preference → Verify stored correctly
2. Demonstrate behavioral pattern → Verify implicit learning
3. Restart app → Verify preferences persist and load
4. Manual edit preferences file → Verify system respects changes
5. Give contradictory preference → Verify old preference updated

---

## Definition of Done

- [ ] `src/memory.py` extended with 8 preference functions
- [ ] `data/memory/user_preferences.json` schema defined and documented
- [ ] `.claude/hooks/preference_detector.py` hook created and registered
- [ ] Explicit preference detection patterns implemented (regex)
- [ ] Implicit preference inference logic implemented
- [ ] Confidence scoring system implemented
- [ ] Preference loading integrated into main.py system prompt
- [ ] All 7 acceptance criteria validated and passing
- [ ] Unit tests written and passing (12+ tests for preference functions)
- [ ] Integration tests passing (hook detection, persistence, loading)
- [ ] User acceptance testing complete with Mike
- [ ] Code reviewed and approved
- [ ] Documentation updated (README with preferences section)
- [ ] Git commit created with proper message
- [ ] Sprint backlog updated (Story 2.3 marked complete)

---

## Out of Scope

The following are explicitly **NOT** part of this story:

- **Advanced ML/NLP for preference detection** (use simple pattern matching for MVP)
- **Preference conflict resolution UI** (manual file editing sufficient)
- **Preference synchronization across devices** (local-only for MVP)
- **Natural language preference queries** ("What does the system know about me?")
- **Preference privacy controls** (all data local, no sharing)
- **Preference import/export** (JSON files are export-ready)
- **Preference version history** (STORY-2.5 may include)
- **Multi-user preference profiles** (single-user app for MVP)
- **Preference recommendation engine** ("You might like OKRs based on...")
- **Agent-specific preference overrides** (global preferences apply to all agents)

---

## Testing Scenarios

### Scenario 1: Explicit Preference Learning
**Given:** User states explicit preference in conversation
**When:** User says "I prefer OKRs for goal setting"
**Then:**
1. Preference detector hook analyzes conversation
2. Extracts "OKRs" and "goal setting" keywords
3. Updates `frameworks_and_methods.goal_setting: ["OKRs"]`
4. Sets confidence score 0.95 (explicit statement)
5. Saves to `user_preferences.json`
6. Next session loads preference and uses OKR terminology

### Scenario 2: Implicit Behavioral Pattern Learning
**Given:** User demonstrates consistent behavior pattern
**When:** User plans morning sessions 5 times in a row
**Then:**
1. System analyzes conversation timestamps
2. Detects morning pattern (timestamps 6-10am)
3. Infers `work_habits.preferred_planning_time: "morning"`
4. Sets confidence score 0.65 (implicit inference)
5. Future suggestions prioritize morning timing

### Scenario 3: Preference Confidence Increase
**Given:** Existing preference with moderate confidence
**When:** User reaffirms preference multiple times
**Then:**
1. First mention: confidence 0.7
2. Second mention: confidence 0.8
3. Third mention: confidence 0.9
4. Fourth mention: confidence 0.95 (approaches max 1.0)
5. System more strongly applies preference

### Scenario 4: Preference Contradiction Handling
**Given:** User states contradictory preference
**When:** Previous: "I prefer detailed responses", Now: "I prefer concise responses"
**Then:**
1. System detects conflict
2. Updates preference to new value "concise"
3. Decreases confidence on old preference to 0.0
4. Sets new preference confidence to 0.9
5. System adapts communication style immediately

### Scenario 5: Preference Persistence Across Sessions
**Given:** Preferences learned in previous session
**When:** User restarts application
**Then:**
1. `load_user_preferences()` called on startup
2. Preferences loaded from JSON file
3. Included in agent system prompts
4. Agent behavior reflects learned preferences
5. No redundant questions asked

### Scenario 6: Manual Preference Editing
**Given:** User manually edits `user_preferences.json`
**When:** User changes `verbosity: "detailed"` to `verbosity: "concise"`
**Then:**
1. System loads edited file on next startup
2. Respects manual changes
3. No automatic overwriting of manual edits
4. Confidence score preserved from file

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| False preference detection (noise) | Medium | Medium | Require high confidence (0.8+) before applying preferences |
| Preferences lock in bad patterns | Medium | Medium | Confidence decay over time, easy manual editing |
| Detection patterns too brittle | High | High | Start simple, iterate based on actual usage patterns |
| Performance impact on hook | Medium | Low | Keep analysis lightweight (<500ms), async processing |
| User doesn't notice personalization | Low | Medium | Make preferences visible in UI, show what was learned |
| Conflicting preferences cause confusion | Medium | Low | Last-write-wins strategy, timestamp tracking |

---

## Success Metrics

- **Primary:** 80%+ of explicit preferences correctly detected and stored
- **Implicit Learning:** 3+ behavioral patterns detected per week of use
- **Personalization Impact:** 30% reduction in redundant questions after 2 weeks
- **User Awareness:** User can describe 5+ learned preferences when asked
- **Confidence Accuracy:** High-confidence (0.9+) preferences have 95%+ accuracy
- **Performance:** Preference detection hook executes in <300ms

---

## Notes

- Preference learning creates the foundation for truly personalized AI assistance
- Start with simple pattern matching - can enhance with ML later
- User should be able to easily inspect and edit learned preferences
- Confidence scores enable graceful handling of uncertain preferences
- Story 2.3 complements Stories 2.1 (business context) and 2.2 (conversation history):
  - Story 2.1: Company-level information (what the business is)
  - Story 2.2: Interaction history (what was said when)
  - Story 2.3: Personal preferences (how the user likes to work)
- This is the "personalization" layer that makes agents feel like they truly know you

---

## Story Dependencies Graph

```
STORY-2.1 (Business Context) ────┐
                                  ├──> STORY-2.3 (Preferences) ──┐
STORY-2.2 (Conversation History) ─┘                                │
                                                                   ├──> STORY-2.4 (Startup Loading)
STORY-1.3 (Conversation Loop) ─────────────────────────────────────┘
```

---

## Dev Agent Record

### Context Reference
- **Story Context File:** TBD (will be generated in story-context workflow)
- **Status:** ✅ APPROVED - Ready for story-context workflow

### SM Validation Record
**Validated:** 2025-10-15
**Validated By:** Bob (Scrum Master)
**Quality Score:** 9.7/10

**Validation Results:**
- ✅ Acceptance Criteria: 7 ACs, all clear and testable (9.7/10)
- ✅ Technical Plan: Detailed with code examples and integration points (9.5/10)
- ✅ Prerequisites: All met (STORY-2.1, 2.2, 1.3 complete) (10/10)
- ✅ Testing Strategy: 12+ unit tests, integration tests, 6 UAT scenarios (9.5/10)
- ✅ Risk Assessment: MEDIUM-LOW, 6 risks with practical mitigations (9/10)
- ✅ Completeness: All required sections present (10/10)
- ✅ Story Points: 6 points appropriate for complexity (10/10)

**Approval Notes:**
Story is exceptionally well-specified with comprehensive acceptance criteria, detailed technical plan including hook implementation, and thorough testing strategy. All prerequisites met. No blocking dependencies. Approved for immediate development. Minor note: Implicit learning algorithm details can be refined during implementation (acceptable for 6-point story).

### Implementation Estimate
**Estimated Implementation Time:** 3-4 hours
**Test Development Time:** 2 hours
**Total Story Time:** 5-6 hours

### Complexity Notes
- **Moderate complexity** (6 points appropriate)
- Most complex part: Pattern detection logic for implicit preferences
- Explicit detection is straightforward regex
- Confidence scoring adds some complexity
- Hook integration similar to Story 2.2 (proven pattern)

---

_Story 2.3 enables personalized agent behavior by learning and remembering user preferences from conversations, eliminating redundant questions and creating a truly adaptive executive assistant experience._
