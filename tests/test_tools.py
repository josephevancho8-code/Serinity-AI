import pytest
from serinity.tools.sandbox import PythonSandboxTool
from serinity.tools.file_reader import FileReaderTool


def test_sandbox_tool_execution():
    sandbox = PythonSandboxTool()
    res = sandbox.execute("print('Serinity online')")
    assert res["success"] is True
    assert "Serinity online" in res["stdout"]


def test_file_reader_tool_success(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello from Serinity storage.")

    reader = FileReaderTool()
    res = reader.execute(str(test_file))
    assert res["success"] is True
    assert "Hello from Serinity storage." in res["content"]


def test_file_reader_missing_file():
    reader = FileReaderTool()
    res = reader.execute("non_existent_file.txt")
    assert res["success"] is False
    assert "not found" in res["error"]
