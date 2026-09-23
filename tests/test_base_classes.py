import pytest
from serinity.tools.base import BaseTool
from serinity.models.base import BaseModelAdapter

def test_base_tool_abstract_instantiation():
    class ConcreteTool(BaseTool):
        name = "dummy"
        description = "dummy tool"
        required_permission = "conversation"

        def execute(self, **kwargs):
            return "executed"

    tool = ConcreteTool()
    assert tool.execute() == "executed"

def test_base_model_adapter_abstract_methods():
    class DummyModel(BaseModelAdapter):
        def generate(self, prompt: str, **kwargs) -> str:
            return "generated"

        def chat(self, messages, **kwargs):
            return "chatted"

    model = DummyModel()
    assert model.generate("test") == "generated"
    assert model.chat([]) == "chatted"
