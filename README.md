# LyraDev

LyraDev is an experimental command line assistant that communicates with a local
language model and stores conversations in a MariaDB database. The project
provides a simple interface for chatting with the model and recalling past
messages.

## Setup

1. Install **Python 3.11** or newer.
2. (Recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install requests mariadb
   ```
4. Ensure a MariaDB server is available. Create a database named
   `lyra_memory` and a user with permissions to read and write to it. The
   default credentials expected by the code are:
   - host: `10.1.1.5`
   - port: `3307`
   - user: `lyra`
   - password: `Lyra_PW4321`

   Update these values in `memory/memory_store.py` if your environment differs.

## Configuring the database connection

`memory/memory_store.py` defines the connection parameters used by the
application. Edit the `MemoryStore` constructor arguments if you need to
change the host, port, user, password, or database name. The table
`chat_log` will be created automatically when the program first runs.

## Running the application

1. Start your local LLM server. By default the assistant expects an API
   endpoint at `http://localhost:1234/v1/chat/completions` (for example from
   LM Studio).
2. Run the chat interface:
   ```bash
   python main.py
   ```
3. Type your messages at the prompt. Use `/recall <keyword> [user|assistant]`
   to search previous messages stored in the database.

## Running tests

A small script `test_memory.py` is provided to exercise the database layer.
Execute it with:
```bash
python test_memory.py
```
It will store a sample message and print the most recent chat history.
