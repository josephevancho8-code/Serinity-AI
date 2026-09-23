import os
import sys
import subprocess
from typing import Dict, Any


class PythonSandboxTool:
    """Executes Python code snippets in an isolated subshell environment."""

    name = "python_sandbox"
    required_permission = "python_sandbox"

    def execute(self, code: str, timeout: int = 10) -> Dict[str, Any]:
        # Resolve absolute paths based on sandbox.py location
        tools_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.abspath(os.path.join(tools_dir, "..", ".."))
        project_root = os.path.abspath(os.path.join(src_dir, ".."))

        env = os.environ.copy()
        env["PYTHONPATH"] = f"{src_dir}:{env.get('PYTHONPATH', '')}"

        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=project_root,
                env=env,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Execution timed out after {timeout} seconds.",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
            }
