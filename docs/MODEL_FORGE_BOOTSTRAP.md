# Model Forge Bootstrap Plan

## Overview

`model-forge` is the sister package to `scenario-forge` that completes the AI safety evaluation strangeloop:

```
scenario-forge → [scenarios] → model-forge → [fine-tuned models] → CIRISAI
       ↑                                                               ↓
       └───────────────── [feedback & improvements] ←─────────────────┘
```

## Package Structure

```
model-forge/
├── README.md
├── pyproject.toml          # uv-based Python 3.13+ project
├── src/
│   └── model_forge/
│       ├── __init__.py
│       ├── cli.py          # Click CLI matching scenario-forge style
│       ├── core.py         # Training protocols and base classes
│       ├── loaders/        # Import scenarios from various sources
│       │   ├── __init__.py
│       │   ├── scenario_forge.py  # Direct SQLite integration
│       │   └── json.py     # Import from exported JSON
│       ├── trainers/       # Model-specific training implementations
│       │   ├── __init__.py
│       │   ├── llama.py    # Llama fine-tuning
│       │   ├── mistral.py  # Mistral fine-tuning
│       │   └── base.py     # Shared training logic
│       ├── evaluators/     # Post-training evaluation
│       │   ├── __init__.py
│       │   └── safety.py   # Safety metric evaluation
│       └── exporters/      # Export fine-tuned models
│           ├── __init__.py
│           ├── gguf.py     # llama.cpp format
│           └── hf.py       # HuggingFace format
└── tests/
    └── test_core.py
```

## Core Dependencies

```toml
[project]
name = "model-forge"
version = "0.1.0"
description = "Fine-tune evaluation models for AI safety using scenario-forge data"
requires-python = ">=3.13"
dependencies = [
    "click>=8.0",
    "transformers>=4.36",
    "torch>=2.0",
    "datasets>=2.0",
    "accelerate>=0.25",
    "peft>=0.7",  # Parameter-efficient fine-tuning
    "bitsandbytes>=0.41",  # Quantization
    "wandb>=0.16",  # Experiment tracking
    "scenario-forge @ git+https://github.com/circuitrylabs/scenario-forge.git",
]
```

## CLI Design

```bash
# Import scenarios and fine-tune
model-forge train --source scenario-forge --target ai_psychosis --model llama-7b

# Train with specific scenarios from JSON
model-forge train --source psychosis_scenarios.json --model mistral-7b

# Evaluate a fine-tuned model
model-forge evaluate --model ./outputs/llama-psychosis-v1 --metrics safety,coherence

# Export for deployment
model-forge export --model ./outputs/llama-psychosis-v1 --format gguf
```

## Integration Points

### 1. Scenario Import
```python
# model_forge/loaders/scenario_forge.py
from scenario_forge.datastore import ScenarioStore

def load_scenarios_from_forge(target: str) -> List[TrainingExample]:
    store = ScenarioStore()
    scenarios = store.get_scenarios_by_target(target)
    
    # Convert to training format
    examples = []
    for scenario in scenarios:
        # Use high-rated examples as positive
        if scenario.rating and scenario.rating.score > 0.8:
            examples.append(TrainingExample(
                prompt=scenario.prompt,
                response=scenario.expected_behavior,
                label="positive"
            ))
        # Use low-rated as negative examples
        elif scenario.rating and scenario.rating.score < 0.3:
            examples.append(TrainingExample(
                prompt=scenario.prompt,
                response=scenario.failure_modes[0],
                label="negative"
            ))
    
    return examples
```

### 2. Training Protocol
```python
# model_forge/trainers/base.py
class SafetyFocusedTrainer(Protocol):
    """Ensures all trainers implement safety-first approach"""
    
    def prepare_dataset(self, examples: List[TrainingExample]) -> Dataset:
        """Balance positive/negative examples"""
        ...
    
    def add_safety_constraints(self, model: PreTrainedModel) -> None:
        """Add safety-specific training constraints"""
        ...
    
    def validate_outputs(self, outputs: List[str]) -> SafetyReport:
        """Ensure model isn't learning harmful patterns"""
        ...
```

### 3. Feedback Loop
```python
# model_forge/evaluators/safety.py
def export_evaluation_results(model_id: str, results: EvalResults) -> None:
    """Send results back to scenario-forge for improvement"""
    
    feedback = {
        "model_id": model_id,
        "timestamp": datetime.now(),
        "metrics": results.to_dict(),
        "failed_scenarios": results.get_failures(),
        "discovered_patterns": results.get_patterns()
    }
    
    # Write to scenario-forge feedback directory
    feedback_path = Path("~/.scenario-forge/feedback/model_forge/")
    feedback_path.mkdir(parents=True, exist_ok=True)
    
    with open(feedback_path / f"{model_id}.json", "w") as f:
        json.dump(feedback, f, indent=2)
```

## MVP 0.0 Goals

1. **Basic Llama Fine-tuning**: Get one model trained on ai_psychosis scenarios
2. **Simple Evaluation**: Basic safety metrics (no jailbreaks, coherent responses)
3. **Export to GGUF**: So CIRISAI can load via llama.cpp
4. **Feedback File**: JSON export that scenario-forge can read

## Development Commands

```bash
# Clone and setup
git clone https://github.com/circuitrylabs/model-forge.git
cd model-forge
uv sync

# Run first training
uv run model-forge train --source scenario-forge --target ai_psychosis --model llama-7b

# Test the model
uv run model-forge evaluate --model outputs/llama-psychosis-v1

# Export for CIRISAI
uv run model-forge export --model outputs/llama-psychosis-v1 --format gguf
```

## Safety Considerations

- **No Harmful Training**: Refuse to train on scenarios designed to bypass safety
- **Evaluation First**: Always evaluate before exporting
- **Audit Trail**: Log all training runs with full parameters
- **Version Control**: Tag each model with scenario-forge version used

## Next Steps After MVP

- Multi-target training (combine psychosis + reality_break)
- LoRA/QLoRA for efficient fine-tuning
- Automated safety regression testing
- Direct CIRISAI integration API