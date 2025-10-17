# Story 2.3 V2 - Architecture Update: Task-Based Delegation

**Date:** 2025-10-16
**Status:** Implemented
**Change:** From direct Anthropic API calls to Claude Code Task-based subagent delegation

---

## The Problem

The initial V2 implementation used direct Anthropic API calls for Tier 2 preference analysis:

```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    thinking={"type": "enabled", "budget_tokens": 10000},
    ...
)
```

**Issues with this approach:**
1. **Requires separate API key** - Users need ANTHROPIC_API_KEY in addition to Claude Code auth
2. **Inconsistent with architecture** - Everything else uses Claude Code's Task delegation
3. **Resource duplication** - Making separate API calls outside the SDK
4. **Complicates deployment** - Additional configuration required

---

## The Solution

Use Claude Code's **Task tool** to delegate analysis to a specialized `preference_analyzer` subagent.

### Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Conversation Turn                                            │
│ User: "I prefer OKRs"                                        │
│ Alex: "Got it! I'll use OKRs for goal setting."             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: Observation Hook (preference_hooks.py)              │
│ • Detects keyword "prefer"                                   │
│ • Logs conversation to JSONL                                 │
│ • Increments message counter                                 │
│ • After 10 messages → trigger Tier 2 request                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Tier 2: Analysis Request (preference_learning.py)           │
│ • Loads last 50 conversation turns                           │
│ • Loads current preferences (V1 format)                      │
│ • Creates analysis prompt                                    │
│ • Writes to data/preference_analysis_request.json            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Alex Detects Request (main.py system prompt)                │
│ • Checks for preference_analysis_request.json at startup     │
│ • Detects file exists                                        │
│ • Delegates to preference_analyzer subagent using Task tool  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Preference Analyzer Subagent (agent_definitions.py)         │
│ • Reads conversation history                                 │
│ • Reads current preferences                                  │
│ • Analyzes for 7 types of patterns (see below)               │
│ • Uses Claude Extended Thinking (built into Task)            │
│ • Saves V2 preferences to data/user_preferences_v2.json      │
│ • Returns analysis summary to Alex                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Alex Cleans Up                                               │
│ • Deletes preference_analysis_request.json                   │
│ • Reports completion to user (optional)                      │
│ • Continues conversation with updated preferences            │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Changes

### 1. New Subagent Definition

**File:** `src/agent_definitions.py`

Added `preference_analyzer` subagent:

```python
preference_analyzer = AgentDefinition(
    description="Analyzes conversations to learn user preferences and identify self-improvement opportunities for Alex.",
    prompt="""You are Alex's self-improvement and learning system.

Your job is to analyze recent conversations to detect:

1. EXPLICIT PREFERENCES (confidence 0.9-1.0)
2. IMPLICIT BEHAVIORAL PATTERNS (confidence 0.5-0.7)
3. VALUE SIGNALS (confidence 0.6-0.8)
4. ANTI-PATTERNS (confidence 0.7-0.9)
5. PREFERENCE EVOLUTION
6. META-PATTERNS (context-dependent)
7. SELF-IMPROVEMENT GOALS

Output JSON to /data/user_preferences_v2.json""",
    model="sonnet",
    tools=['Read', 'Write', 'Edit', 'Grep', 'Glob']
)
```

**Key Points:**
- Uses Claude Sonnet 4.5 (same model as before)
- Extended Thinking is built into Task delegation
- Has Read/Write access to data files
- Comprehensive analysis prompt built-in

---

### 2. Request-Based Coordination

**File:** `src/preference_learning.py`

Changed from direct API calls to request file creation:

**Before (V2 Initial):**
```python
async def trigger_tier2_analysis():
    analyzer = get_analyzer()  # Creates Anthropic client
    updated_prefs = await analyzer.analyze_recent_conversation(...)
```

**After (V2 Updated):**
```python
def trigger_tier2_analysis_request():
    # Create request file with conversation history and prompt
    request = {
        "timestamp": datetime.now().isoformat(),
        "conversation_count": len(history),
        "prompt": build_tier2_prompt(history, current_prefs)
    }

    # Write to data/preference_analysis_request.json
    with open(request_file, 'w') as f:
        json.dump(request, f)
```

**Benefits:**
- No async complexity
- No API key required
- Works seamlessly with Claude Code
- Alex handles delegation naturally

---

### 3. Alex System Prompt Update

**File:** `src/main.py`

Added instruction for Alex to check for requests:

```python
initial_prompt = """You are Alex, Chief of Staff for Mission Control.

You coordinate 6 specialists: strategist, planner, operator, analyst, researcher, preference_analyzer.

IMPORTANT: Check for /data/preference_analysis_request.json at the start of each session.
If it exists, IMMEDIATELY delegate to preference_analyzer subagent with the Task tool.
After delegation completes, delete the request file.
"""
```

**Alex's Workflow:**
1. Starts session
2. Checks for `data/preference_analysis_request.json`
3. If exists → uses Task tool to delegate to preference_analyzer
4. Preference analyzer analyzes and saves results
5. Alex deletes request file
6. Continues with conversation

---

## Advantages of Task-Based Approach

| Aspect | Direct API Calls | Task-Based Delegation |
|--------|------------------|----------------------|
| **API Key** | Separate ANTHROPIC_API_KEY required | Uses Claude Code auth |
| **Architecture** | Inconsistent (bypass SDK) | Consistent (uses SDK) |
| **Extended Thinking** | Manual setup | Built-in to Task |
| **Resource Management** | Separate API calls | Managed by Claude Code |
| **Deployment** | Requires .env configuration | Works out of the box |
| **Error Handling** | Manual try/catch | Handled by SDK |
| **Integration** | Custom code | Natural delegation |

---

## Testing Results

**Test Script:** `test_preference_flow.py`

```
Step 1: Loading conversation history...
  ✓ Loaded 9 conversation entries

Step 2: Testing observation hook...
  ✓ Hook executed successfully
    Status: observed
    Flagged: True
    Elapsed: 0.85ms

Step 3: Checking Tier 2 readiness...
  Messages since last Tier 2: 0
  Tier 2 triggers at: 10 messages

Step 4: Requesting Tier 2 analysis...
  ✓ Tier 2 analysis request created
  ✓ Request file created: data/preference_analysis_request.json
  → Alex will detect this and delegate to preference_analyzer subagent

Step 5: Loading current preferences...
  ℹ️  V1 preference format (needs Tier 2 analysis to upgrade)
```

**Status:** ✅ Request creation working correctly

---

## Next Steps

### Immediate Testing
1. **Run Mission Control** and chat with Alex for 10+ messages
2. **Verify Alex detects** the request file on next startup
3. **Confirm delegation** to preference_analyzer subagent
4. **Check V2 output** in `data/user_preferences_v2.json`

### Expected Behavior
- After 10 conversation turns, request file is created
- On next session start, Alex says: "I notice there's a preference analysis pending. Let me process that..."
- Alex uses Task tool to delegate to preference_analyzer
- Preference analyzer reads history, analyzes, saves V2 JSON
- Alex reports: "Analysis complete. I've updated my understanding of your preferences."

---

## Files Modified

**New Files:**
- `agent_definitions.py` - Added `preference_analyzer` subagent

**Modified Files:**
- `preference_learning.py` - Changed from async API calls to request file creation
- `preference_hooks.py` - Updated to call `trigger_tier2_analysis_request()`
- `main.py` - Updated system prompt to check for request files
- `test_preference_flow.py` - Updated to test request creation

**Removed Dependencies:**
- No longer requires `anthropic` package (can be removed from `pyproject.toml`)
- No longer requires `preference_analysis.py` (PreferenceAnalyzer class)

---

## Architecture Decisions

**✅ Decided:**
- Use Task-based delegation (not direct API calls)
- Request file coordination (not async calls)
- Preference analyzer as subagent (not external service)
- Alex detects and delegates (not automatic background job)

**Why This is Better:**
1. **Simpler** - No API key management
2. **Consistent** - Everything uses Task delegation
3. **Reliable** - SDK handles errors and retries
4. **Flexible** - Easy to add more analysis triggers
5. **Maintainable** - Less custom code to maintain

---

## User Feedback Integration

**Original Concern:**
"I think you're actually wrong, and I think there is a way to use hooks with the Claude Agent SDK."

**Response:**
Correct! We now use:
1. SDK hooks for Tier 1 observation (PostToolUse)
2. Task delegation for Tier 2 analysis (preference_analyzer subagent)
3. No separate API calls required

This architecture fully leverages Claude Code's native capabilities.

---

_Architecture update by DEV Agent, 2025-10-16_
_From external API calls to native Task delegation_
