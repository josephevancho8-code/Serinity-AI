import pytest
from serinity.models.ollama import OllamaAdapter


def test_ollama_adapter_initialization():
    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    assert adapter.model_name == "qwen2.5:3b"
    assert adapter.host == "http://localhost:11434"


def test_ollama_live_generate():
    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    response = adapter.generate(
        prompt="Respond with the single word: READY",
        system_prompt="You are a system verification engine."
    )
    assert len(response) > 0
    assert "READY" in response.upper()


def test_ollama_live_chat():
    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    messages = [
        {"role": "system", "content": "You are Serinity system tester."},
        {"role": "user", "content": "Say hello."}
    ]
    response = adapter.chat(messages)
    assert len(response) > 0
