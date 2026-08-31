import os
from typing import Any

from huggingface_hub import InferenceClient


DEFAULT_MODEL = "HuggingFaceH4/zephyr-7b-beta"
MODEL_CHOICES = [
    "HuggingFaceH4/zephyr-7b-beta",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "microsoft/Phi-3-mini-4k-instruct",
]


def _history_to_messages(history: list[dict[str, Any]]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for item in history:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            messages.append({"role": role, "content": content})
    return messages


def model_inference(
    message: str,
    history: list[dict[str, Any]],
    model: str = DEFAULT_MODEL,
) -> str:
    """Generate a response through Hugging Face's hosted inference API."""
    token = os.environ.get("HF_TOKEN")
    if not token:
        return (
            "Set the HF_TOKEN environment variable to a Hugging Face access token, "
            "then send your message again."
        )

    messages = _history_to_messages(history)
    messages.insert(
        0,
        {
            "role": "system",
            "content": "You are a helpful, concise AI assistant.",
        },
    )
    messages.append({"role": "user", "content": message})

    client = InferenceClient(token=token)
    response = client.chat_completion(
        messages=messages,
        model=model,
        max_tokens=1024,
    )
    return response.choices[0].message.content or ""
