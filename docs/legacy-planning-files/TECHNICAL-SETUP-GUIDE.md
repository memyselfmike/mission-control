# Technical Setup Guide
## Mission Control - Autonomous AI-Powered Executive Team

**Version:** 1.0
**Last Updated:** October 14, 2025
**Audience:** Developers and Technical Users

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Development Setup](#development-setup)
7. [Production Deployment](#production-deployment)

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation |
|----------|----------------|---------|--------------|
| **Python** | 3.13+ | Runtime environment | [python.org](https://www.python.org/downloads/) |
| **uv** | Latest | Package manager | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| **Git** | 2.x | Version control | [git-scm.com](https://git-scm.com/) |

### Optional Software

| Software | Purpose | When Needed |
|----------|---------|-------------|
| **Node.js** | MCP server support (Playwright) | Modules 5-6, browser automation |
| **Chrome** | Playwright browser automation | Modules 5-6, web scraping |
| **Claude Code CLI** | Alternative authentication | If not using API key |

### Account Requirements

- **Anthropic API Key** OR **Claude Code Account**
  - Get API key: [console.anthropic.com](https://console.anthropic.com)
  - OR install Claude Code: `npm install -g @anthropic-ai/claude-code`

---

## Installation Steps

### Step 1: Verify Python Installation

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
Download from [python.org](https://www.python.org/downloads/) and run installer

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

### Step 3: Clone Repository

```bash
git clone <repository-url>
cd mission-control
```

**OR if starting from scratch:**
```bash
mkdir mission-control
cd mission-control
git init
```

### Step 4: Install Dependencies

```bash
# Initialize uv (if not done)
uv init --python 3.13

# Install all dependencies
uv sync
```

This will install:
- `claude-agent-sdk` - Core SDK
- `rich` - CLI formatting
- `python-dotenv` - Environment variables
- `pydantic` - Data validation
- `schedule` - Task scheduling
- `watchdog` - File system monitoring
- `nest-asyncio` - Async support

**Expected output:**
```
Resolved 15 packages in 1.2s
Installed 15 packages in 450ms
```

### Step 5: Configure Authentication

**Option A: Anthropic API Key**

1. Get API key from [console.anthropic.com](https://console.anthropic.com)

2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your key:
   ```
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

3. No `.env` file needed for API key (but still configure user settings)

### Step 6: Run Test Script

```bash
uv run python test_installation.py
```

**Expected output:**
```
Mission Control - Installation Test
Connecting to Claude API...
Hello! Yes, the connection is working perfectly...
✅ Connection successful!
```

**If test fails:**
- Check API key is correct
- Verify internet connection
- See [Troubleshooting](#troubleshooting) section

---

## Configuration

### Environment Variables (.env)

```bash
# .env

# ============================================
# AUTHENTICATION
# ============================================
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ============================================
# USER CONFIGURATION
# ============================================
USER_NAME=Your Name
USER_TIMEZONE=America/New_York

# ============================================
# SYSTEM CONFIGURATION
# ============================================
LOG_LEVEL=INFO
ENABLE_SCHEDULER=true
ENABLE_EVENT_MONITORS=true

# ============================================
# DEVELOPMENT
# ============================================
DEBUG=false
```

### Claude Code Configuration (.claude/settings.json)

```json
{
  "outputStyle": "Chief of Staff",
  "permissions": {
    "allow": [
      "Bash(uv run:*)",
      "Bash(python:*)"
    ],
    "deny": [],
    "ask": []
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
      }
    ]
  }
}
```

**Platform-specific adjustments:**

**Windows:** Replace bash hook commands with PowerShell:
```json
"command": "powershell -c \"uv run .claude/hooks/log_agent_actions.py\""
```

**macOS/Linux:** Hook commands can use system paths as-is

### Agent Configuration (main.py)

Default model and permissions in `main.py`:

```python
options = ClaudeAgentOptions(
    model="claude-sonnet-4-20250514",  # Change model here
    permission_mode="acceptEdits",     # or "default", "planning", "bypass"
    setting_sources=["project"],       # Load .claude/settings.json
    allowed_tools=[
        'Read', 'Write', 'Edit', 'MultiEdit',
        'Grep', 'Glob',
        'Task',
        'TodoWrite',
        'WebSearch', 'WebFetch',
    ],
    agents=agents  # Subagent definitions from src/agent_definitions.py
)
```

**Model Options:**
- `claude-opus-4-20250514` - Maximum capability (expensive)
- `claude-sonnet-4-20250514` - Balanced (recommended)
- `claude-haiku-4-20250611` - Fast and economical (testing)

---

## Verification

### 1. Verify Project Structure

```bash
tree -L 2
```

**Expected structure:**
```
mission-control/
├── .claude/
│   ├── settings.json
│   ├── output-styles/
│   ├── hooks/
│   └── agents/
├── src/
│   ├── agent_definitions.py
│   ├── cli_interface.py
│   ├── scheduler.py
│   └── event_monitors.py
├── data/
│   ├── memory/
│   ├── goals/
│   ├── metrics/
│   └── notes/
├── workflows/
├── templates/
├── output/
├── tests/
├── main.py
├── pyproject.toml
├── .env
└── README.md
```

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

### 4. Run Full System Test

```bash
python main.py
```

**Test interactions:**
```
You: Hello, who are you?
[Should introduce as Chief of Staff]

You: exit
```

---

## Troubleshooting

### Common Issues

#### Issue: "Python 3.13 not found"

**Solution:**
```bash
# Check Python version
python --version
python3 --version
python3.13 --version

# Use specific version with uv
uv init --python 3.13
```

#### Issue: "uv: command not found"

**Solution:**
```bash
# Verify uv installation
which uv

# If not found, reinstall
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (may need restart terminal)
export PATH="$HOME/.cargo/bin:$PATH"
```

#### Issue: "API key invalid"

**Solution:**
1. Verify API key at [console.anthropic.com](https://console.anthropic.com)
2. Check `.env` file for typos
3. Try regenerating API key
4. Verify no extra spaces in `.env` file

#### Issue: "Module 'claude_agent_sdk' not found"

**Solution:**
```bash
# Reinstall dependencies
uv sync

# If still not working, try explicit install
uv add claude-agent-sdk
```

#### Issue: "Permission denied" when running hooks

**Solution (Unix/macOS):**
```bash
# Make hooks executable
chmod +x .claude/hooks/*.py
```

**Solution (Windows):**
- Hooks run via `uv run python` so no chmod needed
- Verify Python is in PATH

#### Issue: "nest_asyncio" errors

**Solution:**
```bash
# Add to main.py before asyncio.run()
import nest_asyncio
nest_asyncio.apply()
```

### Debug Mode

Enable debug logging:

```bash
# Set in .env
DEBUG=true
LOG_LEVEL=DEBUG

# Run with verbose output
uv run python main.py --verbose
```

### Getting Help

1. Check [GitHub Issues](repository-url/issues)
2. Review [Architecture Document](./mission-control-architecture.md)
3. Consult [Agent Development Guide](./AGENT-DEVELOPMENT-GUIDE.md)

---

## Development Setup

### IDE Configuration

**VS Code (.vscode/settings.json):**
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

### Development Dependencies

```bash
# Add dev dependencies
uv add --dev pytest pytest-asyncio black pylint mypy
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.0
    hooks:
      - id: pylint
EOF

pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_agent_definitions.py
```

---

## Production Deployment

### Option 1: Local Installation

```bash
# Create production .env
cp .env.example .env
# Edit with production API key

# Run in background (Unix)
nohup python main.py &

# OR use screen/tmux
screen -S mission-control
python main.py
# Ctrl+A, D to detach
```

### Option 2: Systemd Service (Linux)

Create `/etc/systemd/system/mission-control.service`:

```ini
[Unit]
Description=Mission Control - Autonomous AI Executive Team
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/mission-control
Environment="PATH=/home/youruser/.cargo/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/youruser/.cargo/bin/uv run python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mission-control
sudo systemctl start mission-control
sudo systemctl status mission-control
```

### Option 3: Docker Container

```dockerfile
# Dockerfile
FROM python:3.13-slim

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Run application
CMD ["uv", "run", "python", "main.py"]
```

Build and run:
```bash
docker build -t mission-control .
docker run -d --name mission-control \
  -e ANTHROPIC_API_KEY=your-key \
  -v $(pwd)/data:/app/data \
  mission-control
```

### Security Considerations

1. **API Key Security**
   - Never commit `.env` to git
   - Use environment variables in production
   - Rotate keys regularly

2. **Data Privacy**
   - `data/` folder contains business information
   - Ensure proper file permissions
   - Consider encryption for sensitive data

3. **Network Security**
   - API calls go to Anthropic servers over HTTPS
   - No inbound network connections required
   - Review MCP server security if using external services

---

## Next Steps

After successful setup:

1. ✅ **Verify Installation** - Run test_installation.py
2. ✅ **First Conversation** - Run main.py and interact with Chief of Staff
3. ✅ **Configure Business Context** - Create data/memory/business_context.json
4. ✅ **Set Goals** - Create data/goals/ files for tracking
5. ✅ **Enable Scheduler** - Setup background scheduler for daily briefings
6. ✅ **Review Agent Development Guide** - Learn to customize and extend

See [AGENT-DEVELOPMENT-GUIDE.md](./AGENT-DEVELOPMENT-GUIDE.md) for next steps in customization and development.

---

## Support

- **Documentation**: [docs/](.)
- **Architecture**: [mission-control-architecture.md](./mission-control-architecture.md)
- **Issues**: [GitHub Issues](repository-url/issues)
- **Claude Code Docs**: [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code)
