from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """Abstract interface for Serinity executable tools."""

    name: str
    description: str
    required_permission: str

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        pass
