from typing import Protocol


class Agent(Protocol):
    name: str

    def run(self, payload: dict) -> dict:
        ...
