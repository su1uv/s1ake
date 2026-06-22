# s1ake

> A terminal-native AI coding assistant powered by Google Gemini.

`s1ake` is a keyboard-driven TUI chat agent that can read, write, list, and execute code inside a sandboxed project directory — all while you chat in a clean, reactive terminal interface.

![Python](https://img.shields.io/badge/python-3.13-blue)
![Textual](https://img.shields.io/badge/TUI-Textual-8A2BE2)
![Gemini](https://img.shields.io/badge/LLM-Gemini_2.5_Flash-orange)

---

## ✨ Features

- **Interactive TUI chat** built with [Textual](https://textual.textualize.io/)
- **Function-calling agent** powered by Google's `gemini-2.5-flash`
- **Multi-turn conversation history** with persistent context
- **Live token-usage sidebar** tracks prompt and response token counts
- **Welcome banner** with ASCII art that fades away on first message
- **Sandboxed file tools** restricted to the `./calculator` directory
- **Async workers** keep the UI responsive while the model thinks

---

## 🖥️ Demo

```text
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  █████▀▀█████  ▄▄████ █████▀▀█████ █████  █████ █████▀▀█████      │
│  ███▓█  ███▓█ ▀▀███▓█ ███▓█  ███▓█ ███▓█  ███▓█ ███▓█  ███▓█      │
│  ███▒█  █████   ███▓█ ███▓█  ███▓█ ███▓█  █████ ███▓█  ███▒█      │
│  ███░█          ███▒█ ███▒█▀▀███▒█ ███▒█▀▀████▄ ███▒█  █████      │
│  ▀▀▀▀▀▀▀█████   ███░█ ███░█  ███▒█ ███░█  ███▒█ ███▒█▀ ▄▄▄▄▄      │
│  █████  ███▓█   ███░█ ███░█  ███░█ ███░█  ███░█ ███░█  ███▓█      │
│  ███▓█  ███▒█   ███ █ ███ █  ███ █ ███ █  ███ █ ███░█  ███▒█      │
│  ███▒█  ███░█   ███ █ ███ █  ███ █ ███ █  ███ █ ███ █  ███░█      │
│  █████▄▄█████   █████ █████  █████ █████  █████ █████▄▄█████      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌─ Token usage ─────────────────────────────────────────────────────┐
│ Prompt:    42                                                      │
│ Response:  128                                                     │
└────────────────────────────────────────────────────────────────────┘

> List the files in the calculator project

♥ Here are the files in the calculator directory:
  - calculator.py
  - tests.py

> Run the tests

♥ Running tests...
  test_add ... ok
  test_sub ... ok
```

---

## 🚀 Quick Start

### Requirements

- Python >= 3.13
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

### Installation

Clone the repository and install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
git clone <repository-url>
cd s1ake
uv sync
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-api-key-here
```

### Usage

Launch the terminal UI:

```bash
python main.py
```

Type your request at the bottom prompt and press `Enter`. The agent will plan and execute the necessary tool calls, then reply in the chat pane.

---

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `get_files_info` | List files in the sandboxed directory with size and type info |
| `get_file_content` | Read the contents of a file |
| `run_python_file` | Execute a Python file with optional arguments |
| `write_file` | Write or overwrite a file |

All file paths are resolved relative to `./calculator` and cannot escape that directory.

---

## 📁 Project Structure

```text
.
├── main.py                      # Entry point: launches the TUI
├── pyproject.toml               # Project metadata and dependencies
├── uv.lock                      # Locked dependency tree
├── .env                         # Local environment variables (not committed)
│
├── ui/                          # Textual user interface
│   ├── s1ake.py                 # Main app and layout
│   ├── styles.tcss              # TCSS styling
│   └── components/
│       ├── banner.py            # ASCII welcome banner
│       ├── chat_history.py      # Message scroll area
│       ├── chat_message.py      # Base message widget
│       ├── bot_message.py       # Bot message with markdown rendering
│       ├── user_message.py      # User message widget
│       ├── input_prompt.py      # Input bar
│       └── token_info.py        # Token usage sidebar
│
├── workers/
│   └── send_prompt.py           # Background worker that sends prompts
│
├── functions/                   # Tool implementations
│   ├── get_agent_response.py    # Gemini API call with function calling
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
│
├── src/                         # Shared agent logic
│   ├── call_function.py         # Function dispatch registry
│   ├── prompts.py               # System prompt
│   └── config.py                # Configuration constants
│
├── tests/                       # Manual test scripts for tools
├── calculator/                  # Sandboxed working directory
└── README.md                    # You are here
```

---

## 🔒 Security

File-system tools are scoped to the `./calculator` directory. Any path that resolves outside that directory is rejected, so the agent cannot read from or write to arbitrary locations on your machine.

---

## 🧪 Testing

Run the manual tool test scripts:

```bash
python tests/test_get_files_info.py
python tests/test_get_file_content.py
python tests/test_run_python_file.py
python tests/test_write_file.py
```

---

## 📄 License

This project is for educational and portfolio use.
