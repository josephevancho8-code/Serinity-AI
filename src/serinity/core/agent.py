import re
from typing import Dict, Any, Optional
from serinity.policy.engine import PolicyEngine
from serinity.memory.store import MemoryStore
from serinity.models.ollama import OllamaAdapter
from serinity.tools.sandbox import PythonSandboxTool
from serinity.tools.file_reader import FileReaderTool


class SerinityAgent:
    SYSTEM_PROMPT = (
        "You are Serinity, an autonomous, deterministic, and secure local AI assistant. "
        "Operate with precision, adhere strictly to security policies, and maintain clear context."
    )

    def __init__(
        self,
        model_name: str = "qwen2.5:3b",
        db_path: str = "serinity_memory.db",
        custom_permissions: Optional[Dict[str, bool]] = None,
    ):
        self.policy = PolicyEngine(custom_permissions=custom_permissions)
        self.memory = MemoryStore(db_path=db_path)
        self.model = OllamaAdapter(model_name=model_name)
        self.tools = {
            "python_sandbox": PythonSandboxTool(),
            "file_reader": FileReaderTool(),
        }

    def execute_action(self, action: str) -> Dict[str, Any]:
        """Evaluates and executes high-level system actions against the Policy Engine."""
        allowed = self.policy.is_allowed(action)
        if not allowed:
            return {
                "success": False,
                "allowed": False,
                "error": f"Security Policy Block: Action '{action}' is blocked by policy guardrails.",
            }
        return {
            "success": True,
            "allowed": True,
            "action": action,
            "message": f"Action '{action}' is permitted.",
        }

    def process_message(self, user_input: str, history_limit: int = 10, auto_execute_tools: bool = True) -> str:
        if not self.policy.is_allowed("conversation"):
            return "Security Policy Block: Conversation capability is currently disabled."

        self.memory.add_message("user", user_input)
        history = self.memory.get_recent_messages(limit=history_limit)

        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        messages.extend(history)

        assistant_response = self.model.chat(messages)

        # Autonomous Multi-Turn Tool Loop
        if auto_execute_tools and "```python" in assistant_response:
            code_matches = re.findall(r"```python\s*(.*?)\s*```", assistant_response, re.DOTALL)
            if code_matches:
                code_to_run = code_matches[0].strip()
                tool_result = self.run_tool("python_sandbox", code=code_to_run)
                output = tool_result.get("stdout") or tool_result.get("error") or tool_result.get("stderr")

                # Feed output back into conversation context for natural synthesis
                synthesis_messages = messages + [
                    {"role": "assistant", "content": assistant_response},
                    {
                        "role": "user",
                        "content": f"[System Tool Output]: {output}\nProvide a concise final answer based on this result.",
                    },
                ]
                assistant_response = self.model.chat(synthesis_messages)

        self.memory.add_message("assistant", assistant_response)
        return assistant_response

    def run_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Policy-checked tool execution pipeline."""
        tool = self.tools.get(tool_name)
        if not tool:
            return {"success": False, "error": f"Tool '{tool_name}' not registered."}

        if not self.policy.is_allowed(tool.required_permission):
            return {
                "success": False,
                "error": f"Tool '{tool_name}' execution blocked by policy requirement '{tool.required_permission}'.",
            }

        return tool.execute(**kwargs)
