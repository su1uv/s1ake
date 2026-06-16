# Bootgent

Bootgent is a lightweight, command-line AI coding agent powered by Google's Gemini API. It can explore a sandboxed project directory, read files, run Python scripts, and write files — all via natural language prompts.

## Features

- 🔍 **List directory contents** with file sizes and directory status
- 📄 **Read file contents** with automatic truncation for large files
- ▶️ **Run Python files** with optional command-line arguments
- ✍️ **Write or overwrite files** within the working directory
- 🔒 **Sandboxed access**: all file operations are restricted to a single working directory
- 🤖 **Gemini-powered**: uses `gemini-2.5-flash` with function calling for autonomous task execution

## Requirements

- Python >= 3.13
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd bootgent
   ```

2. Create a virtual environment and install dependencies using [uv](https://docs.astral.sh/uv/):

   ```bash
   uv sync
   ```

   Or with pip:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

## Configuration

Set your Gemini API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Alternatively, create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-api-key-here
```

## Usage

Run the agent with a prompt:

```bash
python main.py "your coding request here"
```

Enable verbose output to see each function call and token usage:

```bash
python main.py "your coding request here" --verbose
```

### Example

```bash
python main.py "List the files in the calculator project"
```

The agent will plan and execute a sequence of tool calls to fulfill your request.

## Available Tools

The agent has access to the following tools, all scoped to the `./calculator` working directory:

| Tool | Description |
|------|-------------|
| `get_files_info` | List files in a directory with size and type info |
| `get_file_content` | Read the contents of a file |
| `run_python_file` | Execute a Python file with optional arguments |
| `write_file` | Write or overwrite a file |

## Project Structure

```
.
├── main.py                   # Entry point for the CLI agent
├── call_function.py          # Function dispatch registry
├── prompts.py                # System prompt for Gemini
├── config.py                 # Configuration constants
├── pyproject.toml            # Project metadata and dependencies
├── functions/                # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
├── test_*.py                 # Manual test scripts for each tool
└── calculator/               # Sandboxed working directory for the agent
```

## Testing

Run the individual test scripts to verify tool behavior:

```bash
python test_get_files_info.py
python test_get_file_content.py
python test_run_python_file.py
python test_write_file.py
```

## Security

All file operations are constrained to the `./calculator` directory. Paths that resolve outside this directory are rejected to prevent unauthorized access to the host filesystem.

## License

This project is for educational and personal use.
