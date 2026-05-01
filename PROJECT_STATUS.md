# Project Goal
Create a demo LangChain project that can take an attachment and produce:
1. A short summary
2. Two interesting facts

# Current Status
- Project scaffold created.
- Main script now supports `.txt`, `.md`, and `.pdf` attachments via `--attachment` (default `person.txt`).
- LangChain prompt + LLM integration is now Ollama-only using `deepseek-r1:1.5b`.
- Local syntax smoke check passed.
- Updated imports for LangChain v1 compatibility (`PromptTemplate` from `langchain_core.prompts`).

# Pending Tasks
- [x] Add `main.py` implementation
- [x] Add `requirements.txt`
- [x] Add setup/run instructions in `README.md`
- [x] Add `.env.example`
- [x] Run a local smoke check (`python -m py_compile main.py`)
- [ ] Run end-to-end execution with a real attachment and valid API key

# Notes
- Requires local Ollama with `deepseek-r1:1.5b` available.
