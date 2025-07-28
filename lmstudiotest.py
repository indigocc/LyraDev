<<<<<<< HEAD
import requests

url = "http://localhost:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-r1-qwen",  # name doesn't matter, just included
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a strange fact about gravity."}
    ],
    "temperature": 0.7,
    "max_tokens": 256
}

response = requests.post(url, headers=headers, json=data)

print(response.json()['choices'][0]['message']['content'])
=======
import requests

url = "http://localhost:1234/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-r1-qwen",  # name doesn't matter, just included
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a strange fact about gravity."}
    ],
    "temperature": 0.7,
    "max_tokens": 256
}

response = requests.post(url, headers=headers, json=data)

print(response.json()['choices'][0]['message']['content'])
>>>>>>> 45cb54d5b63d87a0ab3dac7803cf3a7ffe855c4f
