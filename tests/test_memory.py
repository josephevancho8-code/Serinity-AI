import pytest
from serinity.memory.store import MemoryStore


def test_memory_store_all_operations():
    store = MemoryStore(":memory:")

    # Test adding messages (both primary and alias)
    store.add_chat_message("user", "Hello Serinity")
    store.add_message("assistant", "Hello Joseph")

    # Test full history retrieval
    history = store.get_chat_history()
    assert len(history) == 2

    # Test recent messages with and without limits
    recent_all = store.get_recent_messages(limit=None)
    assert len(recent_all) == 2

    recent_limited = store.get_recent_messages(limit=1)
    assert len(recent_limited) == 1
    assert recent_limited[0]["content"] == "Hello Joseph"

    # Test fact storage and retrieval
    store.store_fact("user_name", "Joseph")
    assert store.get_fact("user_name") == "Joseph"
    assert store.get_fact("missing_key") is None

    # Test clearing history
    store.clear_chat_history()
    assert len(store.get_chat_history()) == 0

    # Test close method
    store.close()


def test_memory_store_destructor():
    store = MemoryStore(":memory:")
    # Explicitly test __del__ destructor path
    store.__del__()
