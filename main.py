from chat_engine.llm_interface import LLMInterface
from memory.memory_store import MemoryStore

llm = LLMInterface()
mem_store = MemoryStore()
mem_store.create_tables()

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # Handle recall command
    if user_input.lower().startswith("/recall "):
        parts = user_input[8:].strip().split(" ", 1)
        keyword = parts[0]
        role = None
        if len(parts) == 2 and parts[1] in ("user", "assistant"):
            role = parts[1]
        results = mem_store.search_messages(keyword, role=role)

        if not results:
            print(f"[Assistant]: No memories found for '{keyword}'.")
        else:
            print("[Assistant]: Here’s what I remember:")
            for role, content, timestamp in results:
                print(f"- ({role}) [{timestamp}]: {content}")
        continue  # This ensures the recall doesn’t go to the LLM

    # Regular chat
    reply, thoughts = llm.chat(user_input)
    if thoughts:
        print(f"[Thoughts] {thoughts}")
    print(f"Assistant: {reply}")
