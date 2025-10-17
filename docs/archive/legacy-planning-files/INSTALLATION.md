# Installation Guide
## Mission Control - Autonomous AI-Powered Executive Team

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Installation](#step-by-step-installation)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Next Steps](#next-steps)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Installation |
|----------|----------------|--------------|
| **Python** | 3.13+ | [python.org](https://www.python.org/downloads/) |
| **uv** | Latest | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| **Git** | 2.x | [git-scm.com](https://git-scm.com/) |

### Account Requirements

You need **ONE** of the following:
- **Anthropic API Key** ([console.anthropic.com](https://console.anthropic.com))
- **Claude Code Account** ([claude.com/claude-code](https://claude.com/claude-code))

---

## Step-by-Step Installation

### Step 1: Verify Python 3.13+

```bash
python --version
# Expected output: Python 3.13.x or higher
```

**If Python 3.13+ is not installed:**

**macOS:**
```bash
brew install python@3.13
```

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer
- Check "Add Python to PATH"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv
```

### Step 2: Install uv Package Manager

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify installation:**
```bash
uv --version
# Expected: uv x.x.x
```

### Step 3: Download/Clone Mission Control

**Option A: Clone from Git (if available)**
```bash
git clone <repository-url>
cd mission-control-system
```

**Option B: Extract from ZIP**
```bash
# Extract the mission-control-system.zip file
cd mission-control-system
```

### Step 4: Install Python Dependencies

```bash
# Initialize uv (creates virtual environment)
uv init --python 3.13

# Install all dependencies
uv sync
```

**Expected output:**
```
Resolved 15 packages in 1.2s
Installed 15 packages in 450ms
  + claude-agent-sdk
  + rich
  + python-dotenv
  + pydantic
  + schedule
  + watchdog
  + nest-asyncio
  ...
```

**Installed packages:**
- `claude-agent-sdk` - Core SDK for autonomous agents
- `rich` - Beautiful CLI formatting
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- `schedule` - Task scheduling
- `watchdog` - File system monitoring
- `nest-asyncio` - Async/await support

### Step 5: Configure Authentication

**Option A: Anthropic API Key**

1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Copy environment template:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` file and add your key:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   USER_NAME=Your Name
   USER_TIMEZONE=America/New_York
   ```

**Option B: Claude Code Authentication**

1. Install Claude Code CLI:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. Authenticate:
   ```bash
   claude-code login
   ```
3. Still create `.env` for user settings (but API key not needed):
   ```bash
   cp .env.example .env
   # Edit USER_NAME and USER_TIMEZONE only
   ```

### Step 6: Test Installation

```bash
uv run python test_installation.py
```

**Expected output:**
```
Mission Control - Installation Test

Connecting to Claude API...
Hello! Yes, the connection is working perfectly...
✅ Connection successful!
Claude Agent SDK is installed and configured correctly.
```

**If test fails**, see [Troubleshooting](#troubleshooting) section below.

---

## Configuration

### Environment Variables

Edit `.env` file:

```bash
# ==============================================
# REQUIRED: Authentication
# ==============================================
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ==============================================
# OPTIONAL: User Configuration
# ==============================================
USER_NAME=Your Name
USER_TIMEZONE=America/New_York

# ==============================================
# OPTIONAL: System Configuration
# ==============================================
LOG_LEVEL=INFO
ENABLE_SCHEDULER=true
ENABLE_EVENT_MONITORS=true

# ==============================================
# OPTIONAL: Development
# ==============================================
DEBUG=false
```

### Business Context (Optional but Recommended)

Create `data/memory/business_context.json` from example:

```bash
cp data/memory/business_context.json.example data/memory/business_context.json
# Edit with your business information
```

### Quarterly Goals (Optional but Recommended)

Create `data/goals/2025-Q4-rocks.json` from example:

```bash
cp data/goals/2025-Q4-rocks.json.example data/goals/2025-Q4-rocks.json
# Edit with your quarterly goals
```

---

## Verification

### 1. Verify Project Structure

```bash
# Unix/macOS/Linux
tree -L 2

# Windows
dir /s /b
```

Should see:
- `.claude/` folder with settings.json, hooks/, output-styles/
- `src/` folder with agent_definitions.py
- `data/` folder with memory/, goals/, metrics/, notes/
- `main.py` entry point
- `pyproject.toml` dependencies

### 2. Verify Dependencies

```bash
uv run python -c "from claude_agent_sdk import ClaudeSDKClient; print('✓ SDK installed')"
uv run python -c "from rich.console import Console; print('✓ Rich installed')"
uv run python -c "from src.agent_definitions import agents; print(f'✓ {len(agents)} agents defined')"
```

**Expected output:**
```
✓ SDK installed
✓ Rich installed
✓ 5 agents defined
```

### 3. Verify Authentication

```bash
uv run python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✓ API key loaded' if os.getenv('ANTHROPIC_API_KEY') else '✗ No API key')"
```

### 4. Run First Conversation

```bash
uv run python main.py
```

**Test interaction:**
```
You: Hello, who are you?
[Agent should introduce as Alex, Chief of Staff]

You: exit
```

---

## Troubleshooting

### Issue: "Python 3.13 not found"

**Solution:**
```bash
# Check all Python versions
python --version
python3 --version
python3.13 --version

# Use specific version with uv
uv init --python 3.13

# If still not found, install Python 3.13+
```

### Issue: "uv: command not found"

**Solution:**
```bash
# Verify uv installation
which uv  # Unix/macOS
where uv  # Windows

# If not found, reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (may need to restart terminal)
# Unix/macOS:
export PATH="$HOME/.cargo/bin:$PATH"
# Windows: Added automatically by installer
```

### Issue: "API key invalid"

**Solution:**
1. Verify API key at [console.anthropic.com](https://console.anthropic.com)
2. Check `.env` file for typos (no spaces around `=`)
3. Try regenerating API key
4. Verify `.env` is in project root directory
5. Verify no quotes around key in `.env`

### Issue: "Module 'claude_agent_sdk' not found"

**Solution:**
```bash
# Reinstall dependencies
uv sync

# If still not working, try explicit install
uv add claude-agent-sdk

# Verify virtual environment is active
# Should see .venv/ directory in project
```

### Issue: "Permission denied" running hooks

**Solution (Unix/macOS/Linux):**
```bash
# Make hooks executable
chmod +x .claude/hooks/*.py
```

**Solution (Windows):**
- Hooks run via `python` command, no chmod needed
- Verify Python is in PATH
- Try running hook manually: `python .claude/hooks/log_agent_actions.py`

### Issue: test_installation.py fails

**Common causes:**
1. **No internet connection** - Check network
2. **API key not set** - Verify `.env` file
3. **API key invalid** - Regenerate key
4. **Firewall blocking** - Check firewall settings
5. **Rate limit** - Wait a few minutes and retry

**Debug steps:**
```bash
# Set debug mode in .env
DEBUG=true

# Run test with verbose output
uv run python test_installation.py --verbose
```

### Issue: Hooks not triggering

**Solution:**
1. Verify `.claude/settings.json` exists
2. Verify hooks are listed in settings.json
3. Test hooks manually:
   ```bash
   python .claude/hooks/log_agent_actions.py
   python .claude/hooks/goal_monitor.py
   ```
4. Check hook output for errors
5. Verify data/ directories exist

---

## Next Steps

After successful installation:

### 1. First Run
```bash
uv run python main.py
```

### 2. Configure Your Business Context
- Copy and edit `data/memory/business_context.json`
- Add your company information
- Update as you go

### 3. Set Your Goals
- Copy and edit `data/goals/2025-Q4-rocks.json`
- Define your quarterly objectives
- Track progress over time

### 4. Explore Agents
Try delegating to specialists:
- "I need help with quarterly planning" → Planner
- "Can you research AI agent frameworks?" → Researcher
- "Help me plan my day" → Operator

### 5. Learn the System
- Ask: "What can you help me with?"
- Try: "How am I tracking on my goals?"
- Explore: "Tell me about your team"

### 6. Customize
- Review `.claude/output-styles/chief-of-staff.md` - adjust persona
- Review `src/agent_definitions.py` - customize agents
- Add your own workflows in `workflows/`

---

## Getting Help

- **Documentation**: Read README.md
- **Issues**: Check GitHub issues (if available)
- **API Docs**: [docs.claude.com/en/api/agent-sdk](https://docs.claude.com/en/api/agent-sdk)

---

## Success!

If you've completed all steps successfully, you now have a fully functional autonomous AI-powered executive team!

**Welcome to Mission Control!** 🚀
