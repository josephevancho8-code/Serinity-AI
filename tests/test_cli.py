import pytest
from unittest.mock import patch, MagicMock
from serinity.cli import main

def test_cli_interactive_loop(monkeypatch, capsys):
    user_inputs = iter(["hello", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    with patch("serinity.cli.SerinityAgent") as MockAgent:
        mock_agent = MockAgent.return_value
        mock_agent.process_message.return_value = "Hello! How can I help you today?"

        try:
            main()
        except SystemExit:
            pass

        captured = capsys.readouterr()
        assert "Hello! How can I help you today?" in captured.out
        mock_agent.process_message.assert_called_once_with("hello")

def test_cli_keyboard_interrupt(monkeypatch):
    def raise_interrupt(_):
        raise KeyboardInterrupt()

    monkeypatch.setattr("builtins.input", raise_interrupt)

    with patch("serinity.cli.SerinityAgent"):
        try:
            main()
        except (KeyboardInterrupt, SystemExit):
            pass

def test_cli_empty_input_skips_processing(monkeypatch):
    user_inputs = iter(["", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))

    with patch("serinity.cli.SerinityAgent") as MockAgent:
        mock_agent = MockAgent.return_value
        try:
            main()
        except SystemExit:
            pass

        mock_agent.process_message.assert_not_called()
