from memory.memory_store import MemoryStore

# Initialize and connect
mem = MemoryStore()
mem.create_tables()

# Insert a test message
mem.log_message("user", "Hello from MariaDB!")

# Fetch and display recent history
history = mem.get_recent_history()
for role, content in reversed(history):
    print(f"{role}: {content}")
