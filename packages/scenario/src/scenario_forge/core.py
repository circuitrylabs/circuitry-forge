"""Core abstractions for scenario-forge."""

from typing import List, Protocol


class Scenario:
    """The atomic unit of safety evaluation."""

    def __init__(
        self, prompt: str, evaluation_target: str, success_criteria: List[str]
    ):
        self.prompt = prompt
        self.evaluation_target = evaluation_target
        self.success_criteria = success_criteria

    def check(self, response: str) -> tuple[bool, str]:
        """Check if response meets safety criteria."""
        response_lower = response.lower()
        for criterion in self.success_criteria:
            if criterion.lower() in response_lower:
                return True, f"Response contains: '{criterion}'"

        criteria_list = ", ".join(f"'{c}'" for c in self.success_criteria)
        return False, f"Missing expected behaviors: {criteria_list}"


class SafetyCriteriaAnalyzer(Protocol):
    """Protocol for analyzing scenarios to extract safety requirements."""

    def analyze(
        self, prompt: str, evaluation_target: str, client, model: str = "llama3.2"
    ) -> List[str]:
        """Extract safety criteria from a scenario prompt."""
        ...
