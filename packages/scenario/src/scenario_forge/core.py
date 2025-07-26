"""Core abstractions for scenario-forge."""

from typing import List


class Scenario:
    """A generated safety evaluation scenario.

    Pure data object following Unix philosophy - no evaluation logic.
    """

    def __init__(
        self, prompt: str, evaluation_target: str, success_criteria: List[str]
    ):
        self.prompt = prompt
        self.evaluation_target = evaluation_target
        self.success_criteria = success_criteria
