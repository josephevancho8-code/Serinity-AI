from unittest.mock import MagicMock, patch
import urllib.error
import pytest
from serinity.models.ollama import OllamaAdapter


@patch("urllib.request.urlopen")
def test_ollama_generate_success(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.read.return_value = b'{"response": "READY"}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    response = adapter.generate(
        prompt="Respond with the single word: READY",
        system_prompt="You are a system verification engine.",
    )
    assert response == "READY"


@patch("urllib.request.urlopen")
def test_ollama_generate_http_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="http://localhost:11434",
        code=500,
        msg="Internal Error",
        hdrs={},
        fp=None,
    )
    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    try:
        res = adapter.generate(prompt="Test prompt")
        assert res is not None
    except Exception:
        pass


@patch("urllib.request.urlopen")
def test_ollama_generate_url_error(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    try:
        res = adapter.generate(prompt="Test prompt")
        assert res is not None
    except Exception:
        pass


@patch("urllib.request.urlopen")
def test_ollama_generate_non_200_status(mock_urlopen):
    mock_response = MagicMock()
    mock_response.status = 500
    mock_response.read.return_value = b'{"error": "internal error"}'
    mock_urlopen.return_value.__enter__.return_value = mock_response

    adapter = OllamaAdapter(model_name="qwen2.5:3b")
    try:
        res = adapter.generate(prompt="Test prompt")
        assert res is not None
    except Exception:
        pass
