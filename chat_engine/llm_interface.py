import os
import requests
from memory.memory_store import MemoryStore

class LLMInterface:
    def __init__(self):
        self.api_url = os.getenv("LLM_API_URL", "http://localhost:1234/v1/chat/completions")
        self.mem_store = MemoryStore()
        self.mem_store.create_tables()

        self.system_prompt = (
            "You are Lyra, an AI assistant with long-term memory. Your context length is limited, "
            "so you must assess what information is worth preserving permanently.\n\n"
            "To store facts, instructions, or details that may be relevant across multiple sessions or once context is lost, "
            "return a message in the following exact format:\n"
            "/memorystore \"<specific, contextual memory>\"\n"
            "Example: /memorystore \"The user on 2023-10-25 is named Finn.\"\n\n"
            "Once you issue this command, the system will store it in long-term memory and immediately re-invoke the same user input "
            "along with a success confirmation, like:\n"
            "/memorystore \"...\" was successful.\n\n"
            "This lets you continue your reasoning and responses with memory intact.\n\n"
            "You may also issue /recall <keyword> to retrieve relevant long-term memories if context has been lost.\n\n"
            "Only use /memorystore or /recall when it is clearly justified. Be concise, contextual, and avoid storing trivial interactions."
        )

    def chat(self, user_input):
        recent_history = self.mem_store.get_recent_history()
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        for role, content in recent_history:
            messages.append({"role": role, "content": content})

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            reply = response.json()['choices'][0]['message']['content']
        except Exception as e:
            reply = f"[Error contacting LLM API: {e}]"
            return reply, None

        # Extract and remove internal thoughts (if present)
        thoughts = None
        if "</think>" in reply:
            pre_think, post_think = reply.split("</think>", 1)
            if "<think>" in pre_think:
                thoughts = pre_think.split("<think>", 1)[-1].strip()
            reply = post_think.strip()

        self.mem_store.log_message("user", user_input)

        if reply.startswith("/memorystore "):
            entry = reply[len("/memorystore "):].strip(" \"")
            self.mem_store.store_long_memory(entry)
            self.mem_store.log_message("assistant", f"Stored memory: {entry}")
            confirm_message = f"/memorystore \"{entry}\" was successful."
            return self.chat(user_input + "\n" + confirm_message)

        elif reply.startswith("/recall "):
            keyword = reply[len("/recall "):].strip(" \"")
            results = self.mem_store.search_long_memory(keyword)
            if results:
                summary = "\n".join(f"- [{ts}] {entry}" for entry, ts in results)
                reply = f"[Recall results for '{keyword}']\n{summary}"
            else:
                reply = f"[No long-term memory found for '{keyword}']"
            self.mem_store.log_message("assistant", reply)
        else:
            self.mem_store.log_message("assistant", reply)

        return reply, thoughts
