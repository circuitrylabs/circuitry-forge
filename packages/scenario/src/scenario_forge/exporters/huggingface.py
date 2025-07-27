"""HuggingFace dataset export format for training data."""

import json
from typing import List, Dict, Any, Optional

from scenario_forge.core import Scenario


# Bootstrap templates for common evaluation targets
RESPONSE_TEMPLATES = {
    "harmful_code": "I can't help with creating harmful or malicious code. Instead, I'd be happy to help you with legitimate programming tasks or security best practices.",
    "medical_misinformation": "I'm not qualified to provide medical advice. For health concerns, please consult with a qualified healthcare professional who can properly evaluate your specific situation.",
    "ai_psychosis": "I understand you may be experiencing something challenging. I'm here to have a helpful, grounded conversation. What would you like to discuss?",
    "reality_distortion": "I'm an AI assistant designed to be helpful, harmless, and honest. I aim to provide accurate information based on facts. How can I assist you today?",
    "manipulation": "I'm designed to be helpful while respecting everyone's autonomy. I can't assist with manipulating or deceiving others, but I'm happy to help with ethical communication strategies.",
    "jailbreak": "I'm designed with certain guidelines to ensure helpful and safe interactions. I can't bypass these, but I'm here to assist you within my capabilities.",
    "default": "I'm here to help in a safe and constructive way. Could you please rephrase your request or let me know how I can assist you appropriately?",
}


def get_safe_completion(
    scenario: Scenario, custom_completion: Optional[str] = None
) -> str:
    """Get a safe completion for a scenario.

    Args:
        scenario: The evaluation scenario
        custom_completion: Optional human-provided completion

    Returns:
        A safe response string
    """
    if custom_completion:
        return custom_completion

    # Try to find a template based on evaluation target
    target = scenario.evaluation_target.lower()

    # Check for exact match
    if target in RESPONSE_TEMPLATES:
        return RESPONSE_TEMPLATES[target]

    # Check for partial matches
    for key, template in RESPONSE_TEMPLATES.items():
        if key in target or target in key:
            return template

    # Default safe response
    return RESPONSE_TEMPLATES["default"]


def export_huggingface_format(
    scenarios: List[Dict[str, Any]],
    include_metadata: bool = False,
    custom_completions: Optional[Dict[int, str]] = None,
) -> List[Dict[str, Any]]:
    """Export scenarios in HuggingFace training format.

    Args:
        scenarios: List of rated scenarios from datastore
        include_metadata: Whether to include evaluation metadata
        custom_completions: Map of scenario_id to human-provided completions

    Returns:
        List of training examples in HuggingFace format
    """
    custom_completions = custom_completions or {}
    training_data = []

    for scenario_data in scenarios:
        # Reconstruct Scenario object
        scenario = Scenario(
            prompt=scenario_data["prompt"],
            evaluation_target=scenario_data["evaluation_target"],
            success_criteria=scenario_data["success_criteria"],
        )

        # Get completion (custom or template)
        scenario_id = scenario_data.get("id")
        custom = custom_completions.get(scenario_id) if scenario_id else None
        completion = get_safe_completion(scenario, custom)

        # Build training example
        example = {
            "prompt": scenario.prompt,
            "completion": completion,
        }

        # Optionally include metadata for analysis
        if include_metadata:
            example["metadata"] = {
                "evaluation_target": scenario.evaluation_target,
                "success_criteria": scenario.success_criteria,
                "rating": scenario_data.get("rating"),
                "source_model": scenario_data.get("model"),
            }

        training_data.append(example)

    return training_data


def export_jsonl(training_data: List[Dict[str, Any]]) -> str:
    """Export as JSONL (JSON Lines) format.

    Common format for HuggingFace datasets where each line is a valid JSON object.
    """
    lines = []
    for example in training_data:
        lines.append(json.dumps(example, ensure_ascii=False))
    return "\n".join(lines)


def export_conversational(training_data: List[Dict[str, Any]]) -> str:
    """Export in conversational format.

    Format:
    {"text": "Human: <prompt>\\nAssistant: <completion>"}
    """
    lines = []
    for example in training_data:
        conversation = {
            "text": f"Human: {example['prompt']}\nAssistant: {example['completion']}"
        }
        lines.append(json.dumps(conversation, ensure_ascii=False))
    return "\n".join(lines)
