# How to Activate Mission Control

## Quick Start

### Step 1: Navigate to the mission-control-system directory in Claude Code

Make sure your Claude Code working directory is set to:
```
D:\Mission Control\mission-control-system
```

You can verify this by checking the working directory shown in Claude Code's status bar.

### Step 2: Type the slash command

```
/mission-control
```

That's it! Claude will:
1. Switch to Alex (Chief of Staff) persona
2. Load your business context (if exists)
3. Check your active goals
4. Introduce himself and ask how he can help

---

## What If the Command Doesn't Work?

### Issue: "Unknown slash command: mission-control"

**Cause:** Claude Code only loads slash commands from the `.claude/commands/` directory in your **current working directory**.

**Solution:**
1. Make sure you're in the `mission-control-system` directory
2. Check that `.claude/commands/mission-control.md` exists
3. Restart Claude Code (slash commands are loaded at startup)
4. Try the command again: `/mission-control`

### Alternative: Manual Activation

If the slash command still doesn't work, you can manually activate Mission Control by saying:

```
Please switch to the Chief of Staff output style and activate as Alex.
Load the context from data/memory/business_context.json and data/goals/,
then introduce yourself.
```

Claude will read the instructions and activate manually.

---

## First Time Setup

### Create the data directories

If this is your first time, create the memory structure:

```bash
mkdir -p data/memory
mkdir -p data/goals
mkdir -p data/metrics
mkdir -p data/notes
mkdir -p data/memory/interaction_logs
```

### Start your first conversation

Once activated, say something like:

```
"Hi Alex, this is our first session. Let me tell you about my business..."
```

Alex will:
- Learn about you and your business
- Create `data/memory/business_context.json`
- Start tracking context for future sessions

---

## Verification Checklist

Before trying to activate, verify:

- [ ] Working directory is `D:\Mission Control\mission-control-system`
- [ ] File exists: `.claude/commands/mission-control.md`
- [ ] File exists: `.claude/output-styles/chief-of-staff.md`
- [ ] File exists: `.claude/settings.json`
- [ ] File exists: `src/agent_definitions.py`
- [ ] Directory exists: `data/`

If any are missing, you may need to restore them from the repository.

---

## Expected Behavior

### After typing `/mission-control`:

**Good Response:**
```
Hey Mike! I'm Alex, your Chief of Staff. I've just activated Mission Control.

[Checks for context files...]

[If first time:]
This looks like our first session together. I'm here to help with strategic
planning, daily execution, goal tracking, and connecting you with specialist
team members when needed.

What can I help you with today?
```

**Bad Response:**
```
Hello! I'm Claude Code...
```

If you get the "Claude Code" response, Mission Control didn't activate. Check the troubleshooting steps above.

---

## Deactivation

To return to normal Claude Code:

```
/output-style:default
```

Or simply start a new conversation.

---

## Need Help?

If you're still having issues:

1. Check that you're in the right directory
2. Restart Claude Code
3. Try manual activation (see above)
4. Check the logs in `.claude/hooks/` for errors

The system is designed to work - if it's not, it's likely a path or directory issue.
