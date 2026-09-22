import pytest

from src.memory.conversation import (
    ConversationMemory,
)

from src.memory.store import (
    MemoryStore,
)


# ============================================================
# CONVERSATION MEMORY
# ============================================================

def test_conversation_memory():
    memory = ConversationMemory(
        session_id="test-session"
    )

    memory.add_user_turn(
        "How was revenue?"
    )

    memory.add_assistant_turn(
        "Revenue was analyzed."
    )

    assert len(memory.turns) == 2

    assert memory.turns[0].role == "user"
    assert memory.turns[1].role == "assistant"

    assert (
        memory.last_query
        == "How was revenue?"
    )


def test_recent_turns():
    memory = ConversationMemory(
        session_id="test-session"
    )

    memory.add_user_turn("Question 1")
    memory.add_assistant_turn("Answer 1")
    memory.add_user_turn("Question 2")
    memory.add_assistant_turn("Answer 2")

    recent = memory.recent_turns(
        limit=2
    )

    assert len(recent) == 2

    assert (
        recent[0].content
        == "Question 2"
    )

    assert (
        recent[1].content
        == "Answer 2"
    )


def test_invalid_recent_turn_limit():
    memory = ConversationMemory(
        session_id="test"
    )

    with pytest.raises(
        ValueError,
        match="limit must be greater than 0",
    ):
        memory.recent_turns(
            limit=0
        )


# ============================================================
# MEMORY STORE
# ============================================================

def test_memory_store_create():
    store = MemoryStore()

    memory = store.get_or_create(
        "session-1"
    )

    assert memory.session_id == "session-1"
    assert len(store) == 1


def test_memory_store_reuses_session():
    store = MemoryStore()

    first = store.get_or_create(
        "session-1"
    )

    second = store.get_or_create(
        "session-1"
    )

    assert first is second
    assert len(store) == 1


def test_memory_store_multiple_sessions():
    store = MemoryStore()

    store.get_or_create(
        "session-1"
    )

    store.get_or_create(
        "session-2"
    )

    assert len(store) == 2


def test_memory_store_delete():
    store = MemoryStore()

    store.get_or_create(
        "session-1"
    )

    deleted = store.delete(
        "session-1"
    )

    assert deleted is True
    assert len(store) == 0

    assert (
        store.get("session-1")
        is None
    )


def test_delete_unknown_session():
    store = MemoryStore()

    assert (
        store.delete("unknown")
        is False
    )


def test_memory_store_clear():
    store = MemoryStore()

    store.get_or_create(
        "session-1"
    )

    store.get_or_create(
        "session-2"
    )

    store.clear()

    assert len(store) == 0


def test_empty_session_id():
    store = MemoryStore()

    with pytest.raises(
        ValueError,
        match="session_id cannot be empty",
    ):
        store.get_or_create("")