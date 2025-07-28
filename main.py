from chat_engine.llm_interface import LLMInterface
from memory.memory_store import MemoryStore

mem_store = MemoryStore()
mem_store.create_tables()
print("✅ Connected to MariaDB.")

llm = LLMInterface()

def extract_command_line(text):
    if "</think>" in text:
        text = text.split("</think>", 1)[1].strip()
    return text.splitlines()[0].strip()

while True:
    try:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("Exiting...")
            break

        reply, thoughts = llm.chat(user_input)

        # Save both user and assistant messages
        mem_store.log_message("user", user_input)

        # Save original assistant reply regardless of command
        raw_reply = reply
        command_line = extract_command_line(reply)

        if command_line.lower().startswith("/memorystore "):
            memory_text = command_line[13:].strip().strip('"')
            mem_store.store_long_memory(memory_text)
            status = f'/memorystore "{memory_text}" was successful.'
            reply, thoughts = llm.chat(f"{user_input}\n\n{status}")
            mem_store.log_message("assistant", reply)
            if thoughts:
                print(f"[Thoughts] {thoughts}")
            print(f"Assistant: {reply}")

        elif command_line.lower().startswith("/recall "):
            keyword = command_line[8:].strip().strip('"')
            long_results = mem_store.search_long_memory(keyword)
            chat_results = mem_store.search_messages(keyword)
            found = []

            for content, ts in long_results:
                found.append(f"[Long-term] ({ts}): {content}")
            for role, content, ts in chat_results:
                found.append(f"[{role}] ({ts}): {content}")

            recall_msg = f'/recall "{keyword}" returned:\n' + ("\n".join(found) if found else "Nothing found.")
            reply, thoughts = llm.chat(f"{user_input}\n\n{recall_msg}")
            mem_store.log_message("assistant", reply)
            if thoughts:
                print(f"[Thoughts] {thoughts}")
            print(f"Assistant: {reply}")

        else:
            mem_store.log_message("assistant", raw_reply)
            if thoughts:
                print(f"[Thoughts] {thoughts}")
            print(f"Assistant: {raw_reply}")

    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
        break
    except Exception as e:
        print(f"[Error] {e}")
