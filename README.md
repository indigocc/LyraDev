"# LyraDev" 
# 🧠 Lyra: Long-Term Memory Interface for LLMs

Lyra is a local-first AI assistant framework designed to augment language models (LLMs) with persistent long-term memory. It enables context-aware dialogue across sessions, allowing LLMs to store, recall, and reason over facts and experiences that exceed the model’s native context window.

## 🚀 Goals

- **Persistent Long-Term Memory**: Enable the assistant to remember important facts across sessions.
- **Controlled Memory Commands**: Store and retrieve memories only when justified, using explicit commands.
- **Deterministic Interaction**: Strip away LLM “thought noise” and enforce clean message parsing.
- **Local Execution**: Run entirely offline with local database and language model (e.g., LM Studio).

## 🏗️ Architecture Overview

### Components

- `main.py`: Command-line interface that handles user input and coordinates conversation flow.
- `llm_interface.py`: Prepares messages for the LLM, parses replies, and manages memory commands.
- `memory_store.py`: Handles MariaDB-based storage for short-term (chat log) and long-term memory.

### Memory Tables

- `chat_log`: Stores recent message history for prompt reconstruction.
- `long_memory`: Stores persistent memory entries issued via `/memorystore`.

### Command Protocol

The system uses explicit instruction protocols:

- To store memory:  
  `/memorystore "The user on 2023-10-25 is named Finn."`

- To recall memory:  
  `/recall "Finn"`

The assistant is instructed to **only use these commands when necessary**, and to avoid storing trivial or repetitive information.

## 🧠 Memory Handling Logic

### Storage Logic

- Assistant responses are first stored in a temporary buffer.
- If the top-level line of the response starts with `/memorystore`, the memory is extracted and inserted into `long_memory`.
- The system then re-invokes the same user input (plus a success confirmation) so that reasoning can continue without loss.

### Recall Logic

- If the assistant replies with `/recall "<keyword>"`, the system fetches matching long-term memories (and chat history if appropriate).
- Matches are displayed to the user in clean, structured format.

### Thought Filtering

To keep interactions deterministic:
- Any `<think>...</think>` sections from the LLM output are stripped before memory checks.
- Memory logic is only triggered if the *first visible line* is a command.

## ⚙️ Environment & Setup

1. **Dependencies**
   - Python 3.10+
   - `mariadb` Python driver
   - LM Studio or another local LLM endpoint

2. **Environment Variables**
   - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
   - `LLM_API_URL` (defaults to `http://localhost:1234/v1/chat/completions`)

3. **Database Schema**
   Created on startup:
   - `chat_log`: recent messages
   - `long_memory`: persistent memory entries

## 🧪 Testing Strategy

To verify memory commands, run a sequence like:

You: Please just return the following and nothing else:
/memorystore "Today is Tuesday"

You: Please just return the following and nothing else:
/recall "Tuesday"


These should trigger isolated memory events without unnecessary re-processing.

## 📌 Known Issues

- Some models generate excessive internal monologue inside `<think>` tags. These are aggressively filtered out.
- Occasionally, the model re-issues memory commands unnecessarily. This is being tuned via prompt engineering.

## ✨ Future Plans

- Context summarization and memory distillation.
- Visual UI wrapper.
- Fine-grained memory permissions (e.g., private vs shared memory).
- Embedding-based semantic search for `long_memory`.

---

**Author**: Finn Johansen
**License**: MIT