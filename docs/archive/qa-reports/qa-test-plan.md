# QA Test Plan - Preference Analyzer Flow

**Date:** 2025-10-16
**Tester:** Mike (User)
**Guide:** DEV Agent
**Target:** Story 2.3 V2 - End-to-End Validation

---

## Test Objective

Validate that the complete preference learning flow works end-to-end:
1. Tier 1 hooks detect preferences during conversation
2. Request file created after 10 messages
3. Alex detects request file on next session
4. Alex delegates to preference_analyzer subagent
5. Preference analyzer generates V2 JSON with reasoning
6. Request file is cleaned up

---

## Pre-Test Setup

### 1. Clean Slate (Optional - Fresh Start)
```bash
cd "D:\Mission Control\mission-control"

# Backup existing data
mkdir -p data/backup
cp -r data/memory data/backup/
cp data/preference_analysis_request.json data/backup/ 2>/dev/null || true

# Clear preference data (optional - for clean test)
rm data/user_preferences_v2.json 2>/dev/null || true
rm data/preference_analysis_request.json 2>/dev/null || true

# Keep conversation history to build on it
```

### 2. Verify System State
```bash
# Check files exist
ls -la src/preference_hooks.py
ls -la src/preference_learning.py
ls -la src/agent_definitions.py

# Run import tests
uv run pytest tests/test_imports.py -v
```

**Expected:** All files exist, all 9 tests pass ✅

---

## Test Case 1: Tier 1 Hook Detection

**Goal:** Verify hooks fire and detect preference keywords

### Steps:
1. Start Mission Control:
   ```bash
   uv run python src/main.py
   ```

2. Have a conversation with Alex about preferences (10+ messages):
   ```
   Test Message 1: "Hi Alex! Let's chat about how I like to work."

   Test Message 2: "I prefer using OKRs for goal setting rather than SMART goals."

   Test Message 3: "I always do my planning in the morning between 8-10am."

   Test Message 4: "I like concise responses - keep things brief unless I ask for details."

   Test Message 5: "I prefer async communication over meetings whenever possible."

   Test Message 6: "I'm building a GAO - a Generative Autonomous Organisation."

   Test Message 7: "My industry is technology, specifically AI and automation."

   Test Message 8: "I typically work with small teams of 5-10 people."

   Test Message 9: "I like to move fast and make decisions quickly."

   Test Message 10: "My core values are autonomy, efficiency, and continuous improvement."

   Test Message 11: "exit"
   ```

### Expected Behavior:
- ✅ Alex responds naturally to each message
- ✅ Conversation flows smoothly
- ✅ No errors displayed
- ✅ On exit, goodbye message appears

### Check Logs:
Look in terminal output for debug messages (stderr):
```
[DEBUG] observation_hook called at ...
```

**Expected:** You should see hook calls in the terminal ✅

---

## Test Case 2: Request File Creation

**Goal:** Verify Tier 2 request file is created after 10 messages

### Steps:
1. Check for request file:
   ```bash
   ls -la data/preference_analysis_request.json
   ```

2. View request file contents:
   ```bash
   cat data/preference_analysis_request.json | head -20
   ```

### Expected Results:
- ✅ File exists at `data/preference_analysis_request.json`
- ✅ File contains:
  - `"timestamp"` - ISO format
  - `"conversation_count"` - Should be 10+
  - `"current_preferences_version"` - Should be "1.0"
  - `"analysis_requested": true`
  - `"prompt"` - Contains conversation history

### Validation Questions:
- [ ] Does the file exist?
- [ ] Does it contain conversation history?
- [ ] Does it include your preference statements?
- [ ] Is the JSON valid (no syntax errors)?

---

## Test Case 3: Alex Detects Request File

**Goal:** Verify Alex notices the request file on startup

### Steps:
1. Start Mission Control again:
   ```bash
   uv run python src/main.py
   ```

2. Watch Alex's introduction message carefully

### Expected Behavior (CRITICAL):

**Option A - Alex Proactively Mentions It:**
```
Alex: "Welcome back! I notice there's a preference analysis pending.
Let me process that before we continue..."

→ Using Task...
```

**Option B - Alex Mentions Request File Exists:**
```
Alex: "Hello! I see there's a pending preference analysis request.
Would you like me to process that now?"
```

**Option C - Alex Checks But Doesn't Mention (Silent):**
```
Alex: "Good morning! How can I help you today?"
[No mention of request file]
```

### What to Record:
- [ ] Did Alex mention the request file?
- [ ] Did Alex use the Task tool?
- [ ] Did you see "→ Using Task..." message?
- [ ] What exactly did Alex say?

**Copy Alex's exact introduction message here for analysis.**

---

## Test Case 4: Task Delegation to Preference Analyzer

**Goal:** Verify Alex actually delegates to preference_analyzer subagent

### Steps:
1. If Alex asks whether to process the request, respond:
   ```
   "Yes, please analyze my preferences."
   ```

2. Watch for Task tool usage indicators

### Expected Behavior:
```
Alex: "I'll analyze your preferences now."

→ Using Task...

[Preference analyzer processes conversation history]

Alex: "Analysis complete. I've updated my understanding of your preferences."
```

### What to Watch For:
- [ ] Does Alex use the Task tool? (Look for "→ Using Task...")
- [ ] Does processing take 2-5 seconds? (Extended Thinking)
- [ ] Does Alex report success?
- [ ] Any error messages?

### Troubleshooting:
If Alex doesn't detect the request:
- Alex may not have read the system prompt correctly
- Request file may not be in the right location
- Alex may need explicit instruction: "Check for preference analysis requests"

---

## Test Case 5: V2 JSON Output Validation

**Goal:** Verify preference_analyzer creates rich V2 format

### Steps:
1. Check if V2 file was created:
   ```bash
   ls -la data/user_preferences_v2.json
   ```

2. View V2 preferences:
   ```bash
   cat data/user_preferences_v2.json | python -m json.tool | head -50
   ```

### Expected V2 Format:
```json
{
  "preferences": {
    "frameworks_and_methods": {
      "goal_setting": {
        "value": ["OKRs"],
        "confidence": 0.95,
        "reasoning": "User explicitly stated 'I prefer OKRs for goal setting'",
        "evidence": [
          "Turn 2: 'I prefer using OKRs for goal setting'"
        ],
        "context": "General preference for goal-setting frameworks",
        "last_confirmed": "2025-10-16T..."
      }
    },
    "communication_style": {
      "verbosity": {
        "value": "concise",
        "confidence": 0.92,
        "reasoning": "User requested brief responses multiple times",
        "evidence": [
          "Turn 4: 'I like concise responses - keep things brief'"
        ],
        "context": "Applies generally unless details are requested"
      }
    }
  },
  "behavioral_patterns": {
    "morning_planning": {
      "description": "User prefers planning activities in morning (8-10am)",
      "confidence": 0.85,
      "evidence": "Turn 3: 'I always do my planning in the morning between 8-10am'"
    }
  },
  "anti_patterns": {},
  "meta_patterns": {},
  "self_improvement_goals": [
    "Learn to distinguish when user wants brief vs detailed responses",
    "Understand context of GAO (Generative Autonomous Organisation)"
  ],
  "version": "2.0",
  "last_tier2_analysis": "2025-10-16T..."
}
```

### Validation Checklist:
- [ ] File exists at `data/user_preferences_v2.json`
- [ ] JSON is valid (no syntax errors)
- [ ] Has `"version": "2.0"`
- [ ] Contains `"preferences"` object
- [ ] Preferences have rich context:
  - [ ] `value`
  - [ ] `confidence` (0.0-1.0)
  - [ ] `reasoning` (explanation)
  - [ ] `evidence` (quoted turns)
  - [ ] `context` (when it applies)
- [ ] Contains `"behavioral_patterns"` (if detected)
- [ ] Contains `"self_improvement_goals"` (what Alex should learn)
- [ ] Detected your explicit preferences (OKRs, concise, morning planning)

---

## Test Case 6: Request File Cleanup

**Goal:** Verify request file is deleted after processing

### Steps:
1. Check if request file still exists:
   ```bash
   ls -la data/preference_analysis_request.json
   ```

### Expected Behavior:
- ✅ File should be deleted (Alex cleans up after delegation)
- ⚠️ If file still exists, Alex may not have completed cleanup

---

## Test Case 7: Preference Persistence

**Goal:** Verify preferences load on next session

### Steps:
1. Exit and restart Mission Control:
   ```bash
   exit
   uv run python src/main.py
   ```

2. Ask Alex about your preferences:
   ```
   "What do you know about my preferences?"
   ```

### Expected Behavior:
Alex should reference your preferences:
- ✅ "I know you prefer OKRs for goal setting"
- ✅ "You like concise responses"
- ✅ "You do planning in the morning"

---

## Test Case 8: Incremental Learning

**Goal:** Verify system updates preferences on subsequent conversations

### Steps:
1. Have another 10+ message conversation with NEW preferences:
   ```
   "Actually, I've changed my mind about something."
   "I now prefer SMART goals over OKRs for short-term projects."
   "But I still like OKRs for long-term strategic goals."
   [Continue with 8+ more messages]
   "exit"
   ```

2. Restart and check for new request file
3. Let Alex process it
4. Check V2 JSON for updates

### Expected Behavior:
- ✅ New request file created after 10 more messages
- ✅ Alex processes on next startup
- ✅ V2 JSON updated with nuanced understanding:
  - OKRs for long-term
  - SMART for short-term
  - Meta-pattern detected: context-dependent preference

---

## Test Case 9: Error Handling

**Goal:** Verify graceful degradation if things fail

### Steps:
1. Simulate error: Rename preference_analyzer:
   ```bash
   # Don't actually do this unless testing error handling
   # This is a hypothetical test
   ```

2. Try the flow again

### Expected Behavior:
- ✅ System doesn't crash
- ✅ Error logged to stderr
- ⚠️ User sees friendly message (not raw exception)

---

## QA Results Template

### Test Results Summary

**Tester:** Mike
**Date:** 2025-10-16
**Duration:** ___ minutes

| Test Case | Status | Notes |
|-----------|--------|-------|
| TC1: Tier 1 Hook Detection | ⏳ | |
| TC2: Request File Creation | ⏳ | |
| TC3: Alex Detects Request | ⏳ | |
| TC4: Task Delegation | ⏳ | |
| TC5: V2 JSON Output | ⏳ | |
| TC6: Request File Cleanup | ⏳ | |
| TC7: Preference Persistence | ⏳ | |
| TC8: Incremental Learning | ⏳ | |
| TC9: Error Handling | ⏳ | |

**Overall Status:** ⏳ PENDING

### Issues Found:
1.
2.
3.

### Observations:
-
-
-

### Recommendation:
- [ ] PASS - Story 2.3 V2 complete, ready for Sprint 2
- [ ] CONDITIONAL PASS - Minor issues, can proceed with caveats
- [ ] FAIL - Critical issues, needs rework

---

## Post-Test Actions

### If Tests Pass ✅
1. Update QA-STATUS-REPORT.md with results
2. Mark Story 2.3 V2 as COMPLETE
3. Create Sprint 1 completion summary
4. Bring Bob (Scrum Master) back for Sprint 2 planning

### If Tests Fail ❌
1. Document all issues found
2. Prioritize by severity (critical/major/minor)
3. Create bug fix tasks
4. Re-test after fixes
5. Update documentation

---

## Quick Reference Commands

```bash
# Start Mission Control
cd "D:\Mission Control\mission-control"
uv run python src/main.py

# Check request file
cat data/preference_analysis_request.json

# Check V2 preferences
cat data/user_preferences_v2.json | python -m json.tool

# Check conversation history
ls -la data/memory/conversations/

# Run tests
uv run pytest tests/test_imports.py -v

# View recent conversation
tail -20 data/memory/conversations/$(ls -t data/memory/conversations/ | head -1)
```

---

_QA Test Plan by DEV Agent, 2025-10-16_
_Ready for systematic validation_
