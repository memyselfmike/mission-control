# STORY-1.5: Implement Hooks System for Autonomous Behaviors

**Epic:** EPIC-1 - Autonomous Agent Framework
**Status:** Not Started
**Priority:** P1 (High)
**Story Points:** 8
**Assignee:** TBD

---

## User Story

As a **system**
I want to **trigger automated actions based on agent events**
So that **agents can operate autonomously and proactively**

---

## Acceptance Criteria

- [ ] .claude/settings.json configured with hooks
- [ ] Hook scripts created in .claude/hooks/
- [ ] Stop hook triggers after agent responses
- [ ] PostToolUse hook triggers after specific tool usage
- [ ] Goal monitoring hook checks for off-track goals
- [ ] Pattern detection hook analyzes user behavior
- [ ] Action logging hook records all agent actions
- [ ] Hooks execute successfully without blocking main conversation
- [ ] Error handling for hook failures

---

## Technical Details

### Hook Types Available

1. **Stop**: Triggered when agent finishes response
2. **PostToolUse**: Triggered after specific tool execution
3. **Notification**: Triggered on agent notifications
4. **User-Prompt-Submit**: Triggered when user submits message

### Implementation: .claude/settings.json

```json
{
  "outputStyle": "Chief of Staff",
  "permissions": {
    "allow": [
      "Bash(uv run:*)",
      "Bash(python:*)"
    ]
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/log_agent_actions.py"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/goal_monitor.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "tool": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pattern_detector.py"
          }
        ]
      },
      {
        "tool": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pattern_detector.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/notification_sound.py"
          }
        ]
      }
    ]
  }
}
```

### Hook Script 1: log_agent_actions.py

```python
#!/usr/bin/env python3
"""
Action Logger Hook

Logs all agent actions to interaction history for:
- Pattern analysis
- Audit trail
- Learning from past interactions
"""

import json
from datetime import datetime
from pathlib import Path
import sys


def log_action():
    """Log agent action to interaction history"""

    # Ensure log directory exists
    log_dir = Path("data/memory/interaction_logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event_type": "agent_response_complete",
        "metadata": {
            "session_id": datetime.now().strftime("%Y%m%d"),
            # Additional context can be added here
        }
    }

    # Write to daily log file
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"

    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Warning: Failed to log action: {e}", file=sys.stderr)


if __name__ == "__main__":
    log_action()
```

### Hook Script 2: goal_monitor.py

```python
#!/usr/bin/env python3
"""
Goal Monitoring Hook

Monitors goals in /data/goals/ and proactively alerts if:
- Goal is marked as off_track
- Goal deadline is approaching and completion is low
- Goal has not been updated recently
"""

from datetime import datetime, timedelta
from pathlib import Path
import json
import sys


def check_goals():
    """Check all goals and alert if issues found"""

    goals_dir = Path("data/goals")

    if not goals_dir.exists():
        return

    alerts = []
    now = datetime.now()

    # Check all goal files
    for goal_file in goals_dir.glob("*.json"):
        try:
            with open(goal_file) as f:
                data = json.load(f)

            # Handle different goal file formats
            if "rocks" in data:  # Quarterly rocks file
                for rock in data.get("rocks", []):
                    alert = check_rock(rock, now)
                    if alert:
                        alerts.append(alert)
            else:  # Single goal file
                alert = check_goal(data, now)
                if alert:
                    alerts.append(alert)

        except Exception as e:
            print(f"Warning: Could not check {goal_file}: {e}", file=sys.stderr)

    # Display alerts if any
    if alerts:
        print("\n" + "=" * 60)
        print("  GOAL MONITORING ALERT")
        print("=" * 60)
        for alert in alerts:
            print(f"{alert['icon']} {alert['message']}")
        print("=" * 60)
        print("Consider reviewing these goals with your Planner agent.\n")


def check_rock(rock: dict, now: datetime) -> dict | None:
    """Check individual rock for issues"""

    # Check if off track
    if rock.get("status") == "off_track":
        return {
            "icon": "⚠️",
            "message": f"Rock '{rock['title']}' is OFF TRACK"
        }

    # Check deadline proximity
    if "due_date" in rock:
        try:
            due_date = datetime.fromisoformat(rock["due_date"])
            days_remaining = (due_date - now).days

            completion = rock.get("completion", 0)

            # Alert if due soon and low completion
            if days_remaining <= 7 and completion < 80:
                return {
                    "icon": "🚨",
                    "message": f"Rock '{rock['title']}' due in {days_remaining} days - only {completion}% complete"
                }

            # Alert if overdue
            if days_remaining < 0:
                return {
                    "icon": "🔴",
                    "message": f"Rock '{rock['title']}' is OVERDUE by {abs(days_remaining)} days"
                }

        except (ValueError, TypeError):
            pass

    return None


def check_goal(goal: dict, now: datetime) -> dict | None:
    """Check individual goal for issues"""

    # Check if off track
    if goal.get("status") == "off_track":
        return {
            "icon": "⚠️",
            "message": f"Goal '{goal.get('name', 'Unknown')}' is OFF TRACK"
        }

    # Check deadline
    if "deadline" in goal:
        try:
            deadline = datetime.fromisoformat(goal["deadline"])
            days_remaining = (deadline - now).days

            completion = goal.get("completion", 0)

            if days_remaining <= 7 and completion < 80:
                return {
                    "icon": "🚨",
                    "message": f"Goal '{goal.get('name', 'Unknown')}' due in {days_remaining} days - only {completion}% complete"
                }

        except (ValueError, TypeError):
            pass

    return None


if __name__ == "__main__":
    check_goals()
```

### Hook Script 3: pattern_detector.py

```python
#!/usr/bin/env python3
"""
Pattern Detection Hook

Analyzes interaction logs to detect patterns in:
- Most common request types
- Preferred times of day
- Recurring topics
- Behavioral patterns

Surfaces insights proactively.
"""

from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import json
import sys


def detect_patterns():
    """Analyze recent interactions and surface patterns"""

    logs_dir = Path("data/memory/interaction_logs")

    if not logs_dir.exists():
        return

    # Analyze last 7 days
    cutoff = datetime.now() - timedelta(days=7)
    recent_logs = []

    try:
        # Read recent log files
        for log_file in sorted(logs_dir.glob("*.jsonl"), reverse=True)[:7]:
            with open(log_file) as f:
                for line in f:
                    try:
                        log = json.loads(line)
                        log_time = datetime.fromisoformat(log["timestamp"])

                        if log_time > cutoff:
                            recent_logs.append(log)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue

    except Exception as e:
        print(f"Warning: Could not analyze patterns: {e}", file=sys.stderr)
        return

    # Need minimum data for patterns
    if len(recent_logs) < 10:
        return

    insights = []

    # Pattern 1: Most active times
    hours = [datetime.fromisoformat(log["timestamp"]).hour for log in recent_logs]
    peak_hours = Counter(hours).most_common(3)

    if peak_hours and peak_hours[0][1] >= 5:  # At least 5 interactions in peak hour
        peak_hour = peak_hours[0][0]
        if peak_hour < 10:
            insights.append("🌅 You're most active in the mornings. I'll prioritize briefings before 10am.")
        elif peak_hour > 17:
            insights.append("🌙 You're most active in the evenings. I'll save important updates for after 5pm.")

    # Pattern 2: Request type frequency (if tracked)
    request_types = [log.get("request_type") for log in recent_logs if "request_type" in log]
    if request_types:
        type_counts = Counter(request_types).most_common(3)
        if type_counts[0][1] >= 5:
            top_type = type_counts[0][0]
            insights.append(f"📊 You've been focused on {top_type} lately. Want to schedule dedicated time for this?")

    # Display insights if found
    if insights:
        print("\n" + "=" * 60)
        print("  PATTERN INSIGHTS")
        print("=" * 60)
        for insight in insights:
            print(f"  {insight}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    detect_patterns()
```

### Hook Script 4: notification_sound.py (Optional)

```python
#!/usr/bin/env python3
"""
Notification Sound Hook (Optional)

Plays a sound when agent sends notification.
Platform-specific implementation.
"""

import sys
import platform


def play_notification_sound():
    """Play system notification sound"""

    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            import subprocess
            subprocess.run(["afplay", "/System/Library/Sounds/Purr.aiff"], check=False)

        elif system == "Linux":
            import subprocess
            # Try different sound players
            for player in ["paplay", "aplay", "play"]:
                try:
                    subprocess.run([player, "/usr/share/sounds/freedesktop/stereo/message.oga"], check=False)
                    break
                except FileNotFoundError:
                    continue

        elif system == "Windows":
            import winsound
            winsound.MessageBeep(winsound.MB_OK)

    except Exception as e:
        # Silently fail - sound is optional
        pass


if __name__ == "__main__":
    play_notification_sound()
```

---

## Definition of Done

- [ ] .claude/settings.json created with hook configuration
- [ ] All 4 hook scripts implemented in .claude/hooks/
- [ ] Hook scripts have proper permissions (chmod +x on Unix)
- [ ] Hook scripts tested individually
- [ ] Hooks trigger correctly during agent operation
- [ ] Error handling works (hooks don't crash main agent)
- [ ] data/memory/interaction_logs/ directory created
- [ ] Goal monitoring tested with sample goal files
- [ ] Pattern detection tested with sample logs
- [ ] Documentation added for each hook

---

## Testing Steps

### 1. Test Individual Hook Scripts

```bash
# Test action logger
uv run .claude/hooks/log_agent_actions.py
# Verify: Creates log file in data/memory/interaction_logs/

# Test goal monitor (create test goal first)
echo '{"name":"Test Goal","status":"off_track"}' > data/goals/test-goal.json
uv run .claude/hooks/goal_monitor.py
# Verify: Displays alert for off-track goal

# Test pattern detector
uv run .claude/hooks/pattern_detector.py
# Verify: Runs without error (may not show patterns with no data)

# Test notification sound
python .claude/hooks/notification_sound.py
# Verify: Plays sound (platform-dependent)
```

### 2. Test Hook Integration

```bash
# Run main agent
python main.py
```

- Have a conversation
- After agent responds, verify:
  - Action logged to data/memory/interaction_logs/
  - Goal monitor runs (check for alerts if goals exist)
- Use Write or Edit tool
- Verify pattern detector runs after tool use

### 3. Test Error Handling

- Introduce syntax error in hook script
- Verify main agent continues working
- Check for error messages in console

---

## Dependencies

- STORY-1.2 (Project structure - need data/ directories)
- STORY-1.3 (Basic conversation loop)

---

## Security Considerations

- Hook scripts run with same permissions as main process
- Validate all file paths to prevent directory traversal
- Use try-except blocks to prevent hook failures from crashing agent
- Log hook errors to stderr, not stdout

---

## Performance Considerations

- Hooks should execute quickly (<100ms)
- Use async/background execution if hooks are slow
- Consider rate limiting for frequent hooks (PostToolUse)
- Clean up old log files periodically

---

## Notes

- Hooks are the foundation of autonomous behaviors
- Start with simple hooks, add complexity later
- Hook failures should be logged but not break the agent
- Reference: claude-agent-sdk-intro/.claude/settings.json for patterns
- Windows users: Update sound file paths in settings.json
