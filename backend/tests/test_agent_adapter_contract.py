import asyncio
from uuid import uuid4

import pytest

from app.agents.fake import FakeAgentAdapter
from app.agents.schemas import AgentEventType, AgentTaskContext


def make_context() -> AgentTaskContext:
    return AgentTaskContext(
        task_id=uuid4(), attempt_id=uuid4(), actor_id=uuid4(),
        workspace_id=uuid4(), repository_id=uuid4(), workspace_path="/isolated/read-only",
        instruction="Explain the repository structure", read_only=True,
    )


def test_fake_adapter_emits_correlated_events_without_execution():
    async def run_test():
        context = make_context()
        adapter = FakeAgentAdapter()

        capabilities = await adapter.capabilities()
        assert capabilities.engine == "fake"
        assert capabilities.supports_read_only is True

        await adapter.start(context)
        events = [event async for event in adapter.events()]

        assert [event.type for event in events] == [
            AgentEventType.TASK_STARTED, AgentEventType.MESSAGE,
        ]
        assert all(event.task_id == context.task_id for event in events)
        assert all(event.attempt_id == context.attempt_id for event in events)
        assert all(event.correlation_id == context.correlation_id for event in events)
        assert "No repository code was executed" in (events[1].message or "")
        await adapter.close()

    asyncio.run(run_test())


def test_adapter_rejects_second_task_attempt():
    async def run_test():
        adapter = FakeAgentAdapter()
        context = make_context()
        await adapter.start(context)
        with pytest.raises(RuntimeError, match="one task attempt"):
            await adapter.start(context)

    asyncio.run(run_test())
