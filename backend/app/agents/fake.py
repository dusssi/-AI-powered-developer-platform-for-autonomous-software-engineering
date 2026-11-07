import asyncio
from collections.abc import AsyncIterator

from app.agents.schemas import (
    AgentEvent,
    AgentEventType,
    AgentTaskContext,
    EngineCapabilities,
)


class FakeAgentAdapter:
    """Deterministic adapter for contract tests; it never runs tools or shell commands."""

    def __init__(self) -> None:
        self._context: AgentTaskContext | None = None
        self._events: list[AgentEvent] = []
        self._closed = False

    async def capabilities(self) -> EngineCapabilities:
        return EngineCapabilities(
            engine="fake", version="1", streaming=True, cancellation=True,
            structured_tool_events=False, supports_read_only=True,
        )

    async def start(self, context: AgentTaskContext) -> None:
        if self._context is not None:
            raise RuntimeError("Adapter instances can only run one task attempt")
        self._context = context
        self._events.append(self._event(AgentEventType.TASK_STARTED))
        self._events.append(self._event(
            AgentEventType.MESSAGE, message="Fake adapter started. No repository code was executed."
        ))

    async def send(self, message: str) -> None:
        if self._context is None or self._closed:
            raise RuntimeError("Adapter has not been started or is already closed")
        self._events.append(self._event(AgentEventType.MESSAGE, message=message))

    async def events(self) -> AsyncIterator[AgentEvent]:
        while self._events:
            yield self._events.pop(0)
            await asyncio.sleep(0)

    async def cancel(self, reason: str) -> None:
        if self._context is None or self._closed:
            return
        self._events.append(self._event(AgentEventType.TASK_CANCELLED, payload={"reason": reason}))

    async def close(self) -> None:
        self._closed = True
        self._events.clear()

    def _event(
        self, event_type: AgentEventType, *, message: str | None = None,
        payload: dict | None = None,
    ) -> AgentEvent:
        assert self._context is not None
        return AgentEvent(
            task_id=self._context.task_id,
            attempt_id=self._context.attempt_id,
            correlation_id=self._context.correlation_id,
            engine="fake", type=event_type, message=message, payload=payload or {},
        )
