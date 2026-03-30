"""Agent base class and shared input/output types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class AgentInput(BaseModel):
    task: str
    context: dict[str, Any] = {}


class AgentOutput(BaseModel):
    agent_name: str
    status: str = "success"  # "success" | "failed"
    data: Any = None
    error: str | None = None


class BaseAgent(ABC):
    name: str = "base"
    description: str = ""

    @abstractmethod
    async def run(self, input: AgentInput) -> AgentOutput: ...
