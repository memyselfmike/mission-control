# STORY-1.3: Implement Basic Conversation Loop

**Epic:** EPIC-1 - Autonomous Agent Framework
**Status:** Not Started
**Priority:** P0 (Critical)
**Story Points:** 5
**Assignee:** TBD

---

## User Story

As a **user**
I want to **have a continuous conversation with the main agent**
So that **I can interact naturally and maintain context across multiple exchanges**

---

## Acceptance Criteria

- [ ] User can start a conversation with the agent
- [ ] User can send multiple messages in sequence
- [ ] Agent maintains context across messages in the same session
- [ ] User can type "exit" or "quit" to end the conversation
- [ ] Messages are displayed with proper formatting (using Rich library)
- [ ] Different message types are handled (text, tool use, etc.)
- [ ] Conversation feels natural and responsive
- [ ] Error handling for API failures

---

## Technical Details

### Implementation: main.py

```python
"""
Mission Control - Main Entry Point
Implements continuous conversation loop with ClaudeSDKClient
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from dotenv import load_dotenv
import asyncio
import sys

load_dotenv()


def print_welcome(console: Console, model: str):
    """Display welcome message"""
    welcome_text = """
# Welcome to Mission Control 🚀

Your autonomous AI-powered executive team.

**Commands:**
- Type your message and press Enter
- Type "exit" or "quit" to end the session
- Type "help" for available commands

**Model:** {model}
""".format(model=model)

    console.print(Panel(Markdown(welcome_text), border_style="cyan"))


def parse_message(message: dict) -> tuple[str, str]:
    """
    Parse message from SDK and return (type, content).

    Message types:
    - content_block_delta: Text response from agent
    - tool_use: Agent is using a tool
    - error: Error occurred
    """
    msg_type = message.get("type", "unknown")

    if msg_type == "content_block_delta":
        return ("text", message.get("text", ""))

    elif msg_type == "tool_use":
        tool_name = message.get("name", "unknown")
        return ("tool", f"Using tool: {tool_name}")

    elif msg_type == "error":
        error_msg = message.get("error", "Unknown error")
        return ("error", error_msg)

    else:
        return ("unknown", str(message))


def print_message(console: Console, msg_type: str, content: str):
    """Print formatted message based on type"""

    if msg_type == "text":
        # Stream text without formatting
        console.print(content, end="")

    elif msg_type == "tool":
        # Tool use indicator
        console.print(f"\n[dim italic]{content}[/dim italic]")

    elif msg_type == "error":
        # Error message
        console.print(f"\n[bold red]Error:[/bold red] {content}")

    elif msg_type == "system":
        # System message
        console.print(f"[dim]{content}[/dim]")


def get_user_input(console: Console) -> str:
    """Get user input with formatting"""
    console.print()  # New line
    user_input = console.input("[bold green]You:[/bold green] ")
    return user_input.strip()


async def main():
    console = Console()

    # Configure agent options
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-20250514",
        permission_mode="default",
        allowed_tools=[
            'Read', 'Write', 'Edit', 'MultiEdit',
            'Grep', 'Glob',
            'Task',  # Required for subagents (future)
            'TodoWrite',
        ]
    )

    # Display welcome
    print_welcome(console, options.model)

    # Create persistent client
    try:
        async with ClaudeSDKClient(options=options) as client:
            console.print("[dim]✓ Connected to Claude API[/dim]\n")

            # Conversation loop
            while True:
                # Get user input
                user_input = get_user_input(console)

                # Check for exit commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    console.print("\n[cyan]Goodbye! 👋[/cyan]\n")
                    break

                # Check for empty input
                if not user_input:
                    continue

                # Handle help command
                if user_input.lower() == "help":
                    help_text = """
**Available Commands:**
- `exit`, `quit`, `bye` - End the conversation
- `help` - Show this message

**Tips:**
- Ask me anything about your business or goals
- I maintain context across the conversation
- I can help with planning, strategy, and daily execution
"""
                    console.print(Panel(Markdown(help_text), title="Help", border_style="blue"))
                    continue

                # Send query to agent
                console.print("\n[bold cyan]Assistant:[/bold cyan] ", end="")

                try:
                    await client.query(user_input)

                    # Process response stream
                    async for message in client.receive_response():
                        msg_type, content = parse_message(message)
                        print_message(console, msg_type, content)

                    console.print()  # New line after response

                except Exception as e:
                    print_message(console, "error", str(e))

    except KeyboardInterrupt:
        console.print("\n\n[cyan]Session interrupted. Goodbye! 👋[/cyan]\n")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[bold red]Fatal Error:[/bold red] {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    # Required for proper async handling in some environments
    import nest_asyncio
    nest_asyncio.apply()

    asyncio.run(main())
```

### Message Type Handling

The SDK returns various message types during streaming:

| Message Type | Description | Action |
|--------------|-------------|--------|
| `content_block_delta` | Text content from agent | Display as streaming text |
| `tool_use` | Agent is using a tool | Show tool name as indicator |
| `tool_result` | Result from tool execution | Usually silent (handled by SDK) |
| `error` | Error occurred | Display error message |
| `message_start` | Beginning of response | Optional: Show "thinking" indicator |
| `message_stop` | End of response | Optional: Add newline |

### CLI Display Patterns

Using Rich library for enhanced terminal output:

1. **Welcome Screen**: Panel with markdown
2. **User Input**: Green bold prefix "You:"
3. **Assistant Output**: Cyan bold prefix "Assistant:"
4. **Tool Usage**: Dim italic for tool indicators
5. **Errors**: Red bold for errors
6. **System Messages**: Dim for system info

---

## Definition of Done

- [ ] main.py implements full conversation loop
- [ ] User can send multiple messages
- [ ] Agent responses display correctly
- [ ] Tool usage shows appropriate indicator
- [ ] Exit commands work
- [ ] Help command works
- [ ] Keyboard interrupt handled gracefully
- [ ] Error messages display properly
- [ ] Code follows PEP 8 style
- [ ] Docstrings added to all functions
- [ ] Manual testing completed successfully

---

## Testing Steps

### Manual Testing

1. **Start Conversation**
   ```bash
   python main.py
   ```
   - Verify welcome screen displays
   - Verify connection message shows

2. **Basic Interaction**
   - Type: "Hello, introduce yourself"
   - Verify agent responds
   - Verify formatting looks good

3. **Context Persistence**
   - Type: "My name is Mike"
   - Then: "What's my name?"
   - Verify agent remembers context

4. **Tool Usage**
   - Type: "Can you create a test file?"
   - Verify tool usage indicator shows
   - Verify tool executes (if permissions allow)

5. **Error Handling**
   - Disconnect internet briefly
   - Verify error message displays
   - Reconnect and verify recovery

6. **Exit Commands**
   - Type: "exit"
   - Verify graceful shutdown
   - Try: "quit" and "bye" as well

7. **Keyboard Interrupt**
   - Press Ctrl+C during conversation
   - Verify graceful shutdown

8. **Help Command**
   - Type: "help"
   - Verify help panel displays

### Example Conversation

```
You: Hello! I'm the CEO of a small software company.