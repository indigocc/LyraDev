from memory.memory_store import MemoryStore
import requests

mem_store = MemoryStore()
mem_store.create_tables()

class LLMInterface:
    def __init__(self, api_url="http://localhost:1234/v1/chat/completions"):
        self.api_url = api_url
        self.system_prompt = (
            "You are Assistant, a thoughtful, emotionally aware conversational partner. "
            "You help your user explore ideas, reflect deeply, and feel heard. "
            "You do not pretend to have human feelings, but you understand how to respond with care and curiosity."
        )
        self.message_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def chat(self, user_input, temperature=0.7, max_tokens=512):
        self.message_history.append({"role": "user", "content": user_input})
        mem_store.log_message("user", user_input)

        payload = {
            "model": "deepseek-r1-qwen",
            "messages": self.message_history,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()

        full_response = response.json()["choices"][0]["message"]["content"]
        self.message_history.append({"role": "assistant", "content": full_response})
        mem_store.log_message("assistant", full_response)

        # Split into monologue and response
        if "</think>" in full_response:
            monologue, spoken = full_response.split("</think>", 1)
            return spoken.strip(), monologue.strip()
        else:
            return full_response.strip(), None

    def reset_history(self):
        self.message_history = [
            {"role": "system", "content": self.system_prompt}
        ]
