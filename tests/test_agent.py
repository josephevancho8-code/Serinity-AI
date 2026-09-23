import pytest
from unittest.mock import MagicMock
from serinity.core.agent import SerinityAgent


@pytest.fixture
def agent_instance(tmp_path):
    db_file = str(tmp_path / "test_agent.db")
    return SerinityAgent(db_path=db_file)


def test_agent_initialization(agent_instance):
    assert agent_instance.model.model_name == "qwen2.5:3b"
    assert agent_instance.policy.is_allowed("conversation") is True


def test_agent_policy_blocked_action(agent_instance):
    res = agent_instance.execute_action("delete_data")
    assert res["success"] is False
    assert "blocked" in res["error"]


def test_agent_allowed_action(agent_instance):
    res = agent_instance.execute_action("conversation")
    assert res["success"] is True
    assert res["allowed"] is True


def test_autonomous_tool_execution(agent_instance):
    mock_code_response = "```python\nprint(50 * 4)\n```"
    mock_final_response = "The result of 50 multiplied by 4 is 200."
    agent_instance.model.chat = MagicMock(side_effect=[mock_code_response, mock_final_response])

    response = agent_instance.process_message("What is 50 * 4?")
    assert "200" in response
