import pytest
from serinity.core.agent import SerinityAgent


def test_file_reader_tool(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Hello from Serinity local research!")

    db_file = str(tmp_path / "reader_test.db")
    agent = SerinityAgent(db_path=db_file)

    res = agent.run_tool("file_reader", file_path=str(test_file))
    assert res["success"] is True
    assert "Hello from Serinity" in res["content"]
