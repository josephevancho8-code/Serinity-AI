import json
import logging
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from serinity.models.base import BaseModelAdapter

logger = logging.getLogger("serinity.models.ollama")


class OllamaAdapter(BaseModelAdapter):
    """
    Native HTTP client for local Ollama daemon. Uses standard library
    to execute non-blocking, zero-dependency inference queries.
    """

    def __init__(self, model_name: str = "qwen2.5:3b", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip("/")

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": kwargs.get("context_size", 4096),
            },
        }
        if system_prompt:
            payload["system"] = system_prompt

        response_data = self._send_request(url, payload)
        return response_data.get("response", "").strip()

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        url = f"{self.host}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": kwargs.get("context_size", 4096),
            },
        }
        response_data = self._send_request(url, payload)
        return response_data.get("message", {}).get("content", "").strip()

    def _send_request(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))
                raise RuntimeError(f"Ollama API returned status code {response.status}")
        except urllib.error.URLError as e:
            logger.error(f"Failed connection to Ollama at {url}: {e}")
            raise RuntimeError(f"Could not connect to Ollama daemon at {self.host}") from e
