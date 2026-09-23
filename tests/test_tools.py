from unittest.mock import patch
import subprocess
import pytest
from serinity.tools.sandbox import PythonSandboxTool


def test_sandbox_success():
    tool = PythonSandboxTool()
    result = tool.execute("print('hello')", timeout=5)
    assert result["success"] is True
    assert result["stdout"] == "hello"


def test_sandbox_timeout():
    tool = PythonSandboxTool()
    result = tool.execute("import time; time.sleep(2)", timeout=1)
    assert result["success"] is False
    assert "timed out" in result["error"]


@patch("subprocess.run")
def test_sandbox_generic_exception(mock_run):
    mock_run.side_effect = Exception("System execution failed")
    tool = PythonSandboxTool()
    result = tool.execute("print('test')")
    assert result["success"] is False
    assert "Execution failed: System execution failed" in result["error"]
