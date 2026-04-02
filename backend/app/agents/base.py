"""Agent base class and shared input/output types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    task: str
    context: dict[str, Any] = Field(default_factory=dict)


class AgentOutput(BaseModel):
    agent_name: str
    status: Literal["success", "failed"] = "success"
    data: Any = None
    error: str | None = None


class BaseAgent(ABC):
    name: str = "base"
    description: str = ""

    @abstractmethod
    async def run(self, input: AgentInput) -> AgentOutput: ...
