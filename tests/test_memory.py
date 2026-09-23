import os
import pytest
from serinity.memory.store import MemoryStore


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_serinity.db"
    return str(db_file)


def test_memory_store_initialization(temp_db):
    store = MemoryStore(db_path=temp_db)
    assert os.path.exists(temp_db)


def test_chat_history_persistence(temp_db):
    store = MemoryStore(db_path=temp_db)
    store.add_message("user", "System setup request")
    store.add_message("assistant", "System operational")

    history = store.get_recent_messages(limit=5)
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "System setup request"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "System operational"


def test_fact_storage_and_updates(temp_db):
    store = MemoryStore(db_path=temp_db)
    store.store_fact("model_name", "qwen2.5:3b")
    assert store.get_fact("model_name") == "qwen2.5:3b"

    store.store_fact("model_name", "qwen2.5:7b")
    assert store.get_fact("model_name") == "qwen2.5:7b"


def test_clear_chat_history(temp_db):
    store = MemoryStore(db_path=temp_db)
    store.add_message("user", "Temporary message")
    assert len(store.get_recent_messages()) == 1

    store.clear_chat_history()
    assert len(store.get_recent_messages()) == 0
