# STORY-1.1: Install and Configure Claude Agent SDK

**Epic:** EPIC-1 - Autonomous Agent Framework
**Status:** Not Started
**Priority:** P0 (Critical)
**Story Points:** 3
**Assignee:** TBD

---

## User Story

As a **developer**
I want to **install and configure the Claude Agent SDK**
So that **I can build autonomous agents using the SDK framework**

---

## Acceptance Criteria

- [ ] Python 3.13+ installed and verified
- [ ] `uv` package manager installed
- [ ] Claude Agent SDK package installed via uv
- [ ] Project structure created with pyproject.toml
- [ ] Dependencies resolved and environment working
- [ ] Basic import test passes: `from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions`
- [ ] Authentication configured (either API key or Claude Code login)
- [ ] Test script runs successfully and connects to Claude API

---

## Technical Details

### Prerequisites

1. **Python 3.13+**
   ```bash
   python --version  # Should be 3.13 or higher
   ```

2. **Install uv**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Claude Code CLI (optional)**
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

### Installation Steps

1. **Initialize project with uv**
   ```bash
   cd "D:\Mission Control"
   uv init --python 3.13
   ```

2. **Add dependencies to pyproject.toml**
   ```toml
   [project]
   name = "mission-control"
   version = "0.1.0"
   description = "Autonomous AI-Powered Executive Team"
   requires-python = ">=3.13"
   dependencies = [
       "claude-agent-sdk>=0.1.0",
       "rich>=13.0.0",
       "python-dotenv>=1.0.0",
       "pydantic>=2.0.0",
       "schedule>=1.2.0",
       "watchdog>=3.0.0",
       "nest-asyncio>=1.6.0"
   ]

   [build-system]
   requires = ["hatchling"]
   build-backend = "hatchling.build"
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Create .env file**
   ```bash
   # .env
   ANTHROPIC_API_KEY=your_api_key_here
   ```

   *OR authenticate with Claude Code:*
   ```bash
   claude-code login
   ```

5. **Create test script**
   ```python
   # test_installation.py

   from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
   from dotenv import load_dotenv
   import asyncio

   load_dotenv()

   async def test_connection():
       options = ClaudeAgentOptions(
           model="claude-haiku-4-20250611",
           permission_mode="default"
       )

       async with ClaudeSDKClient(options=options) as client:
           await client.query("Hello, can you confirm the connection is working?")

           async for message in client.receive_response():
               if message.get("type") == "content_block_delta":
                   print(message["text"], end="")

           print("\n✅ Connection successful!")

   if __name__ == "__main__":
       asyncio.run(test_connection())
   ```

6. **Run test**
   ```bash
   uv run python test_installation.py
   ```

### Expected Output

```
Hello! Yes, the connection is working perfectly. I can see that you're testing the Claude Agent SDK installation. Everything is set up correctly!
✅ Connection successful!
```

---

## Definition of Done

- [ ] All dependencies installed successfully
- [ ] Test script runs without errors
- [ ] Connection to Claude API verified
- [ ] .env file created and gitignored
- [ ] Documentation updated with installation steps
- [ ] Code committed to repository

---

## Testing Steps

1. Verify Python version
2. Verify uv installation
3. Run `uv sync` and check for errors
4. Run test script
5. Verify API connection works
6. Try with both API key and Claude Code auth (if available)

---

## Documentation

Create `docs/INSTALLATION.md`:

```markdown
# Installation Guide

## Prerequisites
- Python 3.13+
- uv package manager
- Anthropic API key OR Claude Code authentication

## Steps
1. Install uv: [instructions]
2. Clone repository
3. Run `uv sync`
4. Configure authentication
5. Run test script

## Troubleshooting
[Common issues and solutions]
```

---

## Dependencies

- None (this is the foundation)

---

## Risks

- **Risk:** Python version incompatibility
  - **Mitigation:** Document exact version requirements, test on multiple platforms

- **Risk:** API key issues
  - **Mitigation:** Provide clear setup instructions, support both auth methods

---

## Notes

- This story should be completed first as everything else depends on it
- Reference: claude-agent-sdk-intro repo for installation patterns
- Keep test script as part of the project for regression testing
