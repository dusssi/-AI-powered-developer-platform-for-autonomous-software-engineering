from collections.abc import AsyncIterator
from typing import Protocol

from app.agents.schemas import AgentEvent, AgentTaskContext, EngineCapabilities


class AgentAdapter(Protocol):
    """Replaceable engine boundary. Adapters never own platform authorization."""

    async def capabilities(self) -> EngineCapabilities: ...

    async def start(self, context: AgentTaskContext) -> None: ...

    async def send(self, message: str) -> None: ...

    def events(self) -> AsyncIterator[AgentEvent]: ...

    async def cancel(self, reason: str) -> None: ...

    async def close(self) -> None: ...
