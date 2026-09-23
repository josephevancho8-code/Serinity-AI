from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseModelAdapter(ABC):
    """
    Abstract interface for reasoning model providers.
    Ensures Serinity Core can swap model backends (Local Ollama, Cloud API, Vision, Coder)
    without breaking memory, policy, or tool integration layers.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass
