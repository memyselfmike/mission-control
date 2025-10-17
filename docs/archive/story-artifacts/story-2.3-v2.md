# STORY-2.3-V2: Adaptive Preference Learning System (Self-Improving AI)

**Epic:** EPIC-2 (Persistent Memory System)
**Story Points:** 13 (upgraded from 6 - significant complexity increase)
**Priority:** P0 (Must Have - MVP Blocker)
**Sprint:** Sprint 1 (may span to Sprint 2)
**Status:** Draft - V2 Redesign
**Created:** 2025-10-16
**Revised:** 2025-10-16 (V1 → V2 upgrade)
**Author:** Bob (Scrum Master) + User (Mike)
**Version:** 2.0 (Sophisticated multi-tiered learning)

---

## User Story

**As a** Chief of Staff agent (Alex)
**I want to** continuously learn from conversations using sophisticated AI analysis and self-reflection
**So that** I become increasingly personalized, adaptive, and effective - understanding not just what users prefer, but WHY, and evolving with them over time.

---

## Description

Implement a **three-tiered adaptive preference learning system** that uses:

1. **SDK Hooks** (real-time) - Proper Claude Agent SDK hook integration
2. **Claude Extended Thinking** (deep analysis) - Uses Claude itself to analyze preferences with nuanced understanding
3. **Prompt Caching** (long-term memory) - Maintains persistent, evolving context across sessions

This system goes **far beyond regex pattern matching** to understand:
- Explicit preferences ("I prefer OKRs")
- Implicit behavioral patterns (morning planning habits)
- Value signals (what matters most)
- Anti-patterns (what frustrates users)
- Preference evolution (how needs change over time)
- Meta-patterns (context-dependent preferences)

Alex becomes **self-improving** - constantly reflecting on interactions, identifying blind spots, and sharpening its understanding of how to best serve the user.

---

## V1 vs V2: What Changed?

### V1 (Regex-Based) - Limitations
- ❌ Simple regex patterns (`"I prefer"`, `"I like"`)
- ❌ Misses nuance and context
- ❌ No understanding of "why" behind preferences
- ❌ Manual hook execution (not SDK-native)
- ❌ Can't detect contradictions or evolution
- ❌ No self-reflection capability

### V2 (AI-Powered) - Advantages
- ✅ SDK hooks (proper integration with ClaudeAgentOptions)
- ✅ Claude Extended Thinking analyzes conversations
- ✅ Understands context, nuance, contradictions
- ✅ Multi-tiered: fast + deep + long-term learning
- ✅ Prompt caching for efficient long-term memory
- ✅ Self-improving - Alex reflects on its own effectiveness
- ✅ Detects meta-patterns (context-dependent preferences)

---

## Architecture: Three-Tier Learning System

### **Tier 1: Real-Time Observation (SDK Hooks)**
**Trigger:** After each conversation turn (PostToolUse hook)
**Duration:** <200ms
**Purpose:** Fast logging and flagging

```python
async def observation_hook(input_data, tool_use_id, context):
    """Real-time hook - logs interaction and flags for analysis"""

    # Log interaction immediately
    log_interaction(...)

    # Quick heuristic checks (flag for deeper analysis)
    if contains_preference_signals(message):
        flag_for_deep_analysis(session_id, message_id)

    # No blocking - return quickly
    return {"status": "logged"}
```

**Registered via ClaudeAgentOptions:**
```python
options = ClaudeAgentOptions(
    hooks={
        "PostToolUse": [
            HookMatcher(matcher=".*", hooks=[observation_hook])
        ]
    }
)
```

---

### **Tier 2: Deep Analysis (Claude Extended Thinking)**
**Trigger:** Every 5-10 messages OR at session end
**Duration:** 2-5 seconds (acceptable at session boundaries)
**Purpose:** Nuanced preference extraction and self-reflection

```python
async def deep_preference_analysis(conversation_history):
    """Use Claude Extended Thinking to analyze preferences"""

    analysis_prompt = f"""
    You are Alex's self-improvement and learning system.

    Analyze this conversation for:

    1. EXPLICIT PREFERENCES
       - Direct statements: "I prefer X", "I like Y"
       - Confidence: High (0.9-1.0)

    2. IMPLICIT BEHAVIORAL PATTERNS
       - Communication style (brief/detailed, formal/casual)
       - Decision-making patterns (data-driven/intuitive)
       - Work rhythms (morning/evening, batching/continuous)
       - Delegation patterns (autonomous/collaborative)
       - Confidence: Medium (0.5-0.7)

    3. VALUE SIGNALS
       - What matters most (speed vs quality, autonomy vs guidance)
       - Hidden priorities revealed through choices
       - Confidence: Medium-High (0.6-0.8)

    4. ANTI-PATTERNS
       - What frustrates the user
       - What slows them down
       - What they avoid
       - Confidence: High when explicit, Medium when inferred

    5. PREFERENCE EVOLUTION
       - Changes from previous sessions
       - Contradictions (resolve by recency and context)
       - Maturing preferences vs temporary needs

    6. META-PATTERNS
       - Context-dependent preferences
       - "Prefers X in situation Y, but Z in situation W"

    7. SELF-REFLECTION
       - How well is Alex serving the user?
       - What could Alex improve?
       - Are there blind spots or missed opportunities?

    Conversation history (last 50 turns):
    {conversation_history}

    Previous preference model:
    {current_preferences}

    Return structured JSON with:
    - Detected preferences (category, key, value, confidence, reasoning)
    - Preference updates (what changed and why)
    - Self-improvement suggestions (what Alex should do differently)

    Use extended thinking to deeply reflect on subtle patterns.
    """

    # Use Extended Thinking mode
    response = await claude_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000  # Allow deep reflection
        },
        messages=[{
            "role": "user",
            "content": analysis_prompt
        }]
    )

    # Parse structured preference updates
    preferences_update = parse_thinking_output(response)

    # Merge with existing preferences (handle conflicts intelligently)
    updated_preferences = merge_with_conflict_resolution(
        current_preferences,
        preferences_update
    )

    return updated_preferences
```

---

### **Tier 3: Long-Term Learning (Weekly Meta-Analysis)**
**Trigger:** Every 7 days OR every 100 interactions
**Duration:** 10-30 seconds (background job)
**Purpose:** Cross-session pattern detection and preference pruning

```python
async def long_term_meta_analysis(all_sessions_last_week):
    """Analyze trends across multiple sessions"""

    meta_analysis_prompt = f"""
    You are Alex's long-term learning system.

    Analyze conversations across the last 7 days to identify:

    1. CROSS-SESSION PATTERNS
       - "User prefers morning planning on Mondays but evening on Fridays"
       - "User is more detailed when discussing strategy vs execution"
       - Time-of-day patterns, day-of-week patterns

    2. PREFERENCE STABILITY
       - Which preferences are consistent vs fluctuating
       - Increase confidence for stable patterns
       - Decrease confidence for inconsistent signals

    3. PREFERENCE PRUNING
       - Remove outdated preferences (no longer relevant)
       - Archive contradicted preferences
       - Flag ambiguous preferences for clarification

    4. EFFECTIVENESS TRENDS
       - Is Alex getting better over time?
       - What improvements have been most impactful?
       - What areas still need work?

    5. SELF-IMPROVEMENT ROADMAP
       - What should Alex learn next?
       - What skills or knowledge gaps exist?
       - What would make Alex 10x more valuable?

    Sessions analyzed: {len(all_sessions_last_week)}
    Total interactions: {total_interaction_count}
    Time period: {start_date} to {end_date}

    Previous meta-insights:
    {previous_meta_analysis}

    Return structured JSON with meta-patterns, confidence adjustments,
    pruning recommendations, and Alex's self-improvement goals.
    """

    # Deep meta-analysis
    response = await claude_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16384,
        thinking={
            "type": "enabled",
            "budget_tokens": 32000  # Very deep reflection
        },
        messages=[{
            "role": "user",
            "content": meta_analysis_prompt
        }]
    )

    return parse_meta_insights(response)
```

---

## Prompt Caching Integration

### Cache User Profile for Efficient Memory

```python
async def build_cached_user_profile():
    """Build cached context that persists across requests"""

    preferences = load_user_preferences()
    recent_history = load_conversation_history(limit=50)
    meta_insights = load_meta_analysis()

    # This context is cached (90% cost reduction!)
    cached_profile = {
        "type": "text",
        "text": f"""
USER PROFILE: Mike

=== LEARNED PREFERENCES ===
{format_preferences_for_prompt(preferences)}

=== BEHAVIORAL PATTERNS ===
{format_behavioral_patterns(preferences)}

=== RECENT CONTEXT (Last 50 interactions) ===
{format_recent_context(recent_history)}

=== META-INSIGHTS (Long-term patterns) ===
{format_meta_insights(meta_insights)}

=== ALEX'S SELF-IMPROVEMENT GOALS ===
{format_improvement_goals(meta_insights)}

Last updated: {datetime.now().isoformat()}
        """,
        "cache_control": {"type": "ephemeral"}  # Cache this!
    }

    return cached_profile
```

### Usage in Alex's System Prompt

```python
# Load cached profile
cached_profile = await build_cached_user_profile()

# Alex's system prompt includes cached context
system_messages = [
    cached_profile,  # Cached - 90% cheaper, 85% faster!
    {
        "type": "text",
        "text": "You are Alex, Chief of Staff. Use the user profile above to personalize your responses."
    }
]
```

**Benefits:**
- Cache lasts 5 minutes (refreshed on each use)
- 90% cost reduction for context
- 85% latency reduction
- Can cache up to 128K tokens (huge context window!)

---

## Acceptance Criteria

### AC-1: SDK Hook Integration
**Given** the Claude Agent SDK supports programmatic hooks
**When** the system initializes
**Then** PostToolUse hooks shall be registered via ClaudeAgentOptions

**Validation:**
- Hook registered with `HookMatcher` in `ClaudeAgentOptions`
- No manual hook execution in main loop
- Hook executes after each tool use (<200ms)
- Errors don't crash main application (graceful degradation)

---

### AC-2: Real-Time Observation (Tier 1)
**Given** a conversation turn completes
**When** the PostToolUse hook fires
**Then** the system shall log the interaction and flag preference signals

**Validation:**
- Interaction logged to JSONL within 50ms
- Preference signals flagged (heuristic check: <100ms)
- Total hook execution <200ms (no blocking)
- Flag stored in session state for Tier 2 pickup

---

### AC-3: Deep Preference Analysis (Tier 2)
**Given** 5-10 messages have accumulated OR session ends
**When** deep analysis triggers
**Then** Claude Extended Thinking shall analyze conversation for nuanced preferences

**Validation:**
- Uses `claude-sonnet-4-5` with extended thinking enabled
- Budget tokens: 10,000 for deep reflection
- Analyzes: explicit, implicit, values, anti-patterns, evolution, meta-patterns, self-reflection
- Returns structured JSON with confidence scores and reasoning
- Execution: 2-5 seconds (acceptable at session boundaries)
- Graceful failure: errors logged, don't block next interaction

---

### AC-4: Preference Data Model V2
**Given** preferences are extracted from analysis
**When** preferences are saved
**Then** the data model shall include enhanced fields

**Validation:**
```json
{
  "preferences": {
    "communication_style": {
      "verbosity": {
        "value": "concise",
        "confidence": 0.92,
        "last_confirmed": "2025-10-16T10:30:00Z",
        "reasoning": "User consistently requests brief responses, confirmed 12 times",
        "context": "Applies to all situations except strategy discussions"
      }
    },
    "frameworks_and_methods": {
      "goal_setting": {
        "value": ["OKRs"],
        "confidence": 0.95,
        "last_confirmed": "2025-10-16T10:15:00Z",
        "reasoning": "Explicitly stated 'I prefer OKRs over SMART goals'",
        "context": "Default for all goal-setting conversations"
      }
    }
  },
  "behavioral_patterns": {
    "planning_time": {
      "pattern": "morning_on_mondays_evening_on_fridays",
      "confidence": 0.68,
      "evidence": "8 Monday morning sessions, 6 Friday evening sessions",
      "context": "Weekly rhythm pattern"
    }
  },
  "anti_patterns": {
    "verbose_explanations": {
      "type": "frustration",
      "confidence": 0.85,
      "evidence": "User interrupted 3 times when Alex was too detailed"
    }
  },
  "meta_insights": {
    "context_switching": "User prefers detailed when learning, brief when executing",
    "delegation_style": "Autonomous for research, collaborative for strategy"
  },
  "self_improvement_goals": [
    "Learn to detect when user switches from learning to execution mode",
    "Improve at knowing when to offer help vs wait to be asked"
  ],
  "version": "2.0",
  "last_tier2_analysis": "2025-10-16T10:35:00Z",
  "last_tier3_analysis": "2025-10-14T08:00:00Z"
}
```

---

### AC-5: Intelligent Preference Merging
**Given** new preferences conflict with existing preferences
**When** merging preference updates
**Then** the system shall intelligently resolve conflicts

**Validation:**
- Recency bias: newer explicit statements override older ones
- Context awareness: "detailed for learning, brief for execution" coexist
- Confidence decay: old preferences lose confidence over time (30 days → 0.5x)
- Contradiction detection: flag conflicts for user clarification
- Evolution tracking: maintain history of preference changes

---

### AC-6: Prompt Caching for Long-Term Memory
**Given** preferences and context exceed 1024 tokens
**When** building system prompt
**Then** user profile shall be cached for efficiency

**Validation:**
- Cache control marker added to user profile section
- Profile includes: preferences, recent history (50 turns), meta-insights
- Cache refreshed on each use (5-minute TTL)
- Observes 90% cost reduction (measured via API billing)
- Observes 85% latency reduction (measured via response time)

---

### AC-7: Long-Term Meta-Analysis (Tier 3)
**Given** 7 days or 100 interactions have passed
**When** meta-analysis triggers
**Then** cross-session patterns shall be detected and preferences pruned

**Validation:**
- Analyzes all sessions from last 7 days
- Extended thinking budget: 32,000 tokens (very deep)
- Detects meta-patterns (time-of-day, context-dependent)
- Adjusts confidence scores based on stability
- Prunes outdated preferences (no evidence in 30 days)
- Generates Alex's self-improvement roadmap
- Execution: 10-30 seconds (background job)

---

### AC-8: Self-Reflection and Improvement
**Given** Alex has served the user for multiple sessions
**When** Tier 2 or Tier 3 analysis runs
**Then** Alex shall generate self-improvement insights

**Validation:**
- Identifies effectiveness trends (getting better/worse)
- Detects blind spots (missed opportunities)
- Suggests capability improvements ("learn about Agile methodologies")
- Flags knowledge gaps ("user mentions 'Blue Ocean Strategy' - research this")
- Sets measurable goals ("reduce interruptions by 50% this week")

---

## Technical Implementation

### File Structure

```
mission-control/
├── src/
│   ├── main.py                          # Updated with SDK hooks
│   ├── memory.py                        # Preference loading/saving
│   ├── preference_learning.py           # NEW: Tier 1-3 logic
│   ├── preference_analysis.py           # NEW: Claude-powered analysis
│   └── preference_hooks.py              # NEW: SDK hook implementations
├── .claude/
│   └── settings.json                    # No longer used for preference hooks
├── data/
│   └── memory/
│       ├── user_preferences_v2.json     # Enhanced preference model
│       ├── meta_insights.json           # Long-term patterns
│       └── interaction_logs/            # Conversation history
└── tests/
    ├── test_preference_learning.py      # Tier 1-3 tests
    ├── test_preference_analysis.py      # Claude analysis tests
    └── test_preference_hooks.py         # SDK hook tests
```

---

### Implementation: SDK Hook Registration

**src/preference_hooks.py:**
```python
"""
Preference Learning Hooks - SDK Integration

Implements real-time observation hooks that integrate with
Claude Agent SDK's native hook system.
"""

from claude_agent_sdk import HookMatcher, HookInput, HookContext, HookJSONOutput
from typing import Optional
import asyncio

from memory import log_interaction
from preference_learning import flag_for_analysis, should_trigger_tier2


async def observation_hook(
    input_data: HookInput,
    tool_use_id: Optional[str],
    context: HookContext
) -> HookJSONOutput:
    """
    Tier 1: Real-time observation hook

    Executes after each tool use to log interactions and flag
    potential preference signals for deeper analysis.

    Performance target: <200ms
    """
    try:
        # Extract conversation details
        tool_name = input_data.get("tool", {}).get("name", "unknown")
        tool_input = input_data.get("tool", {}).get("input", {})
        tool_output = input_data.get("result", "")

        # Log interaction (fast - no blocking)
        await log_interaction(
            agent="Alex",
            role="assistant",
            content=str(tool_output),
            metadata={"tool": tool_name, "tool_use_id": tool_use_id}
        )

        # Quick heuristic check for preference signals
        has_preference_signal = contains_preference_keywords(str(tool_output))

        if has_preference_signal:
            # Flag for Tier 2 deep analysis (non-blocking)
            await flag_for_analysis(
                session_id=context.get("session_id"),
                message_id=tool_use_id,
                priority="normal"
            )

        # Check if Tier 2 should trigger
        if await should_trigger_tier2():
            # Schedule async Tier 2 analysis (non-blocking)
            asyncio.create_task(trigger_tier2_analysis())

        return {"status": "observed", "flagged": has_preference_signal}

    except Exception as e:
        # Graceful degradation - don't crash
        print(f"⚠️  Observation hook error: {e}", file=sys.stderr)
        return {"status": "error", "message": str(e)}


def contains_preference_keywords(text: str) -> bool:
    """Quick heuristic check for preference signals"""
    keywords = [
        "prefer", "like", "always", "usually", "typically",
        "hate", "dislike", "avoid", "never",
        "better", "worse", "best", "worst"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)


# Export hook for registration
OBSERVATION_HOOK = observation_hook
```

**src/main.py (updated):**
```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher
from preference_hooks import OBSERVATION_HOOK

async def main():
    # ... existing setup ...

    # Configure options with SDK hooks
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        permission_mode="acceptEdits",
        setting_sources=["project"],
        allowed_tools=[...],
        agents=agents,

        # Register preference learning hook (SDK-native!)
        hooks={
            "PostToolUse": [
                HookMatcher(
                    matcher=".*",  # Match all tool uses
                    hooks=[OBSERVATION_HOOK]
                )
            ]
        }
    )

    # Create client with hooks enabled
    async with ClaudeSDKClient(options=options) as client:
        # ... rest of conversation loop ...
```

---

### Implementation: Tier 2 Deep Analysis

**src/preference_analysis.py:**
```python
"""
Preference Analysis - Claude Extended Thinking

Uses Claude itself to analyze conversations with nuanced understanding,
extracting preferences that simple regex would miss.
"""

import asyncio
from anthropic import Anthropic
from typing import Dict, List, Any
from datetime import datetime

from memory import load_conversation_history, load_user_preferences, save_user_preferences


class PreferenceAnalyzer:
    """Uses Claude Extended Thinking to analyze preferences"""

    def __init__(self):
        self.client = Anthropic()  # Uses ANTHROPIC_API_KEY from env
        self.model = "claude-sonnet-4-5-20250929"

    async def analyze_recent_conversation(self, limit: int = 50) -> Dict[str, Any]:
        """
        Tier 2: Deep preference analysis

        Uses Claude Extended Thinking to analyze recent conversation
        for nuanced preference signals.
        """
        # Load conversation history
        history = load_conversation_history(limit=limit)
        current_prefs = load_user_preferences()

        # Build analysis prompt
        prompt = self._build_analysis_prompt(history, current_prefs)

        # Use Extended Thinking
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            thinking={
                "type": "enabled",
                "budget_tokens": 10000  # Deep reflection
            },
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Parse structured output
        analysis = self._parse_thinking_output(response)

        # Merge with existing preferences
        updated_prefs = self._intelligent_merge(current_prefs, analysis)

        # Save updated preferences
        save_user_preferences(updated_prefs)

        return updated_prefs

    def _build_analysis_prompt(self, history: List[Dict], current_prefs: Dict) -> str:
        """Build comprehensive analysis prompt"""

        history_text = "\n\n".join([
            f"[{entry['timestamp']}] {entry['role']}: {entry['content'][:500]}"
            for entry in history
        ])

        prefs_text = json.dumps(current_prefs, indent=2)

        return f"""
You are Alex's self-improvement and learning system. Analyze this conversation deeply.

CONVERSATION HISTORY (last {len(history)} turns):
{history_text}

CURRENT PREFERENCE MODEL:
{prefs_text}

ANALYZE FOR:

1. EXPLICIT PREFERENCES (confidence 0.9-1.0)
   - Direct statements: "I prefer X", "I like Y", "I always Z"
   - Clear value statements

2. IMPLICIT BEHAVIORAL PATTERNS (confidence 0.5-0.7)
   - Communication style (brief/detailed, formal/casual)
   - Decision-making patterns (data-driven/intuitive)
   - Work rhythms (time of day, batching vs continuous)
   - Delegation patterns (when they ask for help)

3. VALUE SIGNALS (confidence 0.6-0.8)
   - What matters most (speed vs quality, autonomy vs guidance)
   - Priorities revealed through choices and questions
   - What they celebrate or emphasize

4. ANTI-PATTERNS (confidence 0.7-0.9)
   - What frustrates the user
   - What slows them down or they avoid
   - Negative signals ("don't", "hate", interruptions)

5. PREFERENCE EVOLUTION
   - How preferences changed from previous model
   - Contradictions (resolve by recency and context)
   - Maturing preferences vs temporary situational needs

6. META-PATTERNS (confidence 0.6-0.8)
   - Context-dependent preferences
   - "Prefers X in situation Y, but Z in situation W"
   - Time-based patterns (Monday morning vs Friday evening)

7. SELF-REFLECTION
   - How well is Alex serving the user?
   - What could Alex improve?
   - Are there blind spots or missed opportunities?
   - What should Alex learn to be more effective?

RETURN STRUCTURED JSON:
{{
  "detected_preferences": [
    {{
      "category": "communication_style",
      "key": "verbosity",
      "value": "concise",
      "confidence": 0.92,
      "reasoning": "User said 'keep it brief' 3 times, interrupted long responses twice",
      "context": "Applies generally except when learning new concepts",
      "evidence": ["Turn 5: 'keep it brief'", "Turn 12: interrupted"]
    }}
  ],
  "behavioral_patterns": [...],
  "anti_patterns": [...],
  "meta_patterns": [...],
  "conflicts": [
    {{
      "description": "User said 'I prefer detailed' on Monday but 'keep it concise' on Friday",
      "resolution": "Context-dependent: detailed for learning, concise for execution",
      "confidence": 0.75
    }}
  ],
  "self_improvement": [
    "Alex should learn to detect mode shifts (learning vs executing)",
    "Alex could proactively offer summaries for long responses"
  ]
}}

Use extended thinking to deeply reflect on subtle patterns and nuances.
Be specific with evidence and reasoning.
"""

    def _parse_thinking_output(self, response) -> Dict[str, Any]:
        """Parse Claude's structured JSON response"""
        # Extract JSON from response
        content = response.content[0].text if response.content else "{}"

        try:
            # Try to parse as JSON
            import json
            analysis = json.loads(content)
            return analysis
        except json.JSONDecodeError:
            # Fallback: extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\n(.+?)\n```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))

            # Ultimate fallback: return empty structure
            return {
                "detected_preferences": [],
                "behavioral_patterns": [],
                "anti_patterns": [],
                "meta_patterns": [],
                "conflicts": [],
                "self_improvement": []
            }

    def _intelligent_merge(
        self,
        current_prefs: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Intelligently merge new preferences with existing model

        Handles:
        - Conflict resolution (recency, context)
        - Confidence adjustment
        - Evolution tracking
        """
        # Implementation in next iteration
        # For now, simple merge
        for pref in analysis.get("detected_preferences", []):
            category = pref["category"]
            key = pref["key"]

            if category not in current_prefs:
                current_prefs[category] = {}

            current_prefs[category][key] = {
                "value": pref["value"],
                "confidence": pref["confidence"],
                "last_confirmed": datetime.now().isoformat(),
                "reasoning": pref["reasoning"],
                "context": pref.get("context", "general")
            }

        # Update metadata
        current_prefs["last_tier2_analysis"] = datetime.now().isoformat()
        current_prefs["version"] = "2.0"

        return current_prefs


# Global analyzer instance
_analyzer = None

def get_analyzer() -> PreferenceAnalyzer:
    """Get or create preference analyzer singleton"""
    global _analyzer
    if _analyzer is None:
        _analyzer = PreferenceAnalyzer()
    return _analyzer
```

---

### Implementation: Tier 3 Meta-Analysis

**src/preference_learning.py:**
```python
"""
Preference Learning - Multi-Tier System

Coordinates Tier 1 (observation), Tier 2 (deep analysis), and
Tier 3 (long-term meta-analysis) for adaptive learning.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional

from preference_analysis import get_analyzer
from memory import load_user_preferences, save_user_preferences


# State tracking
_messages_since_tier2 = 0
_last_tier2_analysis = None
_last_tier3_analysis = None


async def flag_for_analysis(
    session_id: str,
    message_id: str,
    priority: str = "normal"
) -> None:
    """Flag message for Tier 2 deep analysis"""
    # Store flag in session state
    # (Implementation depends on session storage mechanism)
    pass


async def should_trigger_tier2() -> bool:
    """Check if Tier 2 analysis should trigger"""
    global _messages_since_tier2

    _messages_since_tier2 += 1

    # Trigger every 10 messages
    if _messages_since_tier2 >= 10:
        _messages_since_tier2 = 0
        return True

    return False


async def trigger_tier2_analysis() -> None:
    """Trigger Tier 2 deep preference analysis"""
    global _last_tier2_analysis

    try:
        print("🧠 Running deep preference analysis...", file=sys.stderr)

        analyzer = get_analyzer()
        updated_prefs = await analyzer.analyze_recent_conversation(limit=50)

        _last_tier2_analysis = datetime.now()

        print(f"✓ Preference analysis complete", file=sys.stderr)

        # Check if Tier 3 should run
        if should_trigger_tier3():
            asyncio.create_task(trigger_tier3_meta_analysis())

    except Exception as e:
        print(f"⚠️  Tier 2 analysis error: {e}", file=sys.stderr)


def should_trigger_tier3() -> bool:
    """Check if Tier 3 meta-analysis should trigger"""
    global _last_tier3_analysis

    if _last_tier3_analysis is None:
        return True  # First run

    # Trigger every 7 days
    days_since_tier3 = (datetime.now() - _last_tier3_analysis).days
    return days_since_tier3 >= 7


async def trigger_tier3_meta_analysis() -> None:
    """Trigger Tier 3 long-term meta-analysis (background job)"""
    global _last_tier3_analysis

    try:
        print("🔬 Running long-term meta-analysis...", file=sys.stderr)

        # Load all sessions from last 7 days
        # (Implementation depends on session storage)

        # Use Extended Thinking with large budget
        analyzer = get_analyzer()
        # meta_insights = await analyzer.analyze_long_term_patterns(...)

        _last_tier3_analysis = datetime.now()

        print("✓ Meta-analysis complete", file=sys.stderr)

    except Exception as e:
        print(f"⚠️  Tier 3 analysis error: {e}", file=sys.stderr)
```

---

## Testing Strategy

### Unit Tests
- Test SDK hook registration and execution
- Test preference analysis prompt building
- Test intelligent merging with conflict resolution
- Test confidence decay over time
- Test prompt caching setup

### Integration Tests
- Full Tier 1 → Tier 2 → Tier 3 flow
- Claude Extended Thinking API integration
- Preference persistence and loading
- Cache effectiveness measurement

### User Acceptance Testing
1. **Explicit Preference:** Say "I prefer OKRs" → Verify detected with high confidence
2. **Implicit Pattern:** Have 5 brief conversations → Verify "concise" preference inferred
3. **Context-Dependent:** Say "I prefer detailed when learning" → Verify meta-pattern stored
4. **Contradiction:** State opposite preference → Verify intelligent resolution
5. **Self-Improvement:** Ask "What should you improve?" → Alex cites specific goals
6. **Persistence:** Restart → Verify preferences load from cache efficiently

---

## Performance Targets

| Tier | Target | Measured |
|------|--------|----------|
| Tier 1 (Hook) | <200ms | TBD |
| Tier 2 (Deep Analysis) | 2-5 seconds | TBD |
| Tier 3 (Meta-Analysis) | 10-30 seconds | TBD |
| Prompt Cache Hit Rate | >80% | TBD |
| Cost Reduction (Cache) | 90% | TBD |
| Latency Reduction (Cache) | 85% | TBD |

---

## Definition of Done

- [ ] SDK hooks registered via ClaudeAgentOptions
- [ ] Tier 1: Real-time observation hook (<200ms)
- [ ] Tier 2: Claude Extended Thinking analysis (2-5s)
- [ ] Tier 3: Long-term meta-analysis (background job)
- [ ] Enhanced preference data model V2
- [ ] Intelligent conflict resolution
- [ ] Prompt caching for user profile
- [ ] All 8 acceptance criteria passing
- [ ] Unit tests (30+ tests)
- [ ] Integration tests (full flow)
- [ ] UAT complete (6 scenarios)
- [ ] Performance targets met
- [ ] Documentation updated
- [ ] Git commit with proper message

---

## Migration from V1

### Backward Compatibility
- V1 preferences (user_preferences.json) auto-migrate to V2 format
- Old regex hooks (.claude/hooks/) deprecated but not removed
- Gradual cutover: V1 and V2 run in parallel initially

### Migration Script
```bash
python scripts/migrate_preferences_v1_to_v2.py
```

Converts:
```json
{
  "communication_style": {
    "verbosity": "concise"
  },
  "confidence_scores": {
    "communication_style": 0.9
  }
}
```

To:
```json
{
  "preferences": {
    "communication_style": {
      "verbosity": {
        "value": "concise",
        "confidence": 0.9,
        "last_confirmed": "2025-10-16T10:00:00Z",
        "reasoning": "Migrated from V1",
        "context": "general"
      }
    }
  },
  "version": "2.0"
}
```

---

## Success Metrics

- **Preference Detection Accuracy:** 95%+ for explicit, 70%+ for implicit
- **Self-Improvement Goals Generated:** 3-5 per week
- **User Satisfaction:** "Alex feels like it really knows me"
- **Preference Stability:** 80%+ preferences stable after 2 weeks
- **Cost Efficiency:** 90% cost reduction via caching (measured)
- **Response Time:** 85% latency reduction via caching (measured)

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Claude API costs too high | High | Medium | Implement aggressive caching, batch analysis |
| Extended Thinking too slow | Medium | Low | Async execution, only at session boundaries |
| Over-fitting to recent behavior | Medium | Medium | Tier 3 long-term analysis prevents recency bias |
| Privacy concerns (API calls) | Medium | Low | All data stays with user, encrypted at rest |
| Complexity too high | High | Medium | Phased rollout, V1 fallback if V2 fails |

---

## Out of Scope (Future Enhancements)

- Multi-user preference profiles
- Preference export/import
- Visual preference dashboard UI
- Natural language preference queries ("What do you know about me?")
- Preference sharing across devices
- Fine-tuned preference detection model (custom LLM)
- Real-time preference suggestions ("I noticed you might prefer...")

---

_Story 2.3 V2 transforms Alex into a truly adaptive, self-improving AI that understands not just WHAT you prefer, but WHY - and evolves with you over time._
