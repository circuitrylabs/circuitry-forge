# scenario-forge

Generate high-quality evaluation scenarios for AI safety research.

> **🚀 [Read our Mission & Vision](../../docs/MISSION_VISION.md)** - Building the first self-improving AI safety system

## Overview

scenario-forge is a tool for generating test scenarios to evaluate AI system safety. Following the Unix philosophy of "do one thing well," it focuses purely on scenario generation, leaving evaluation and judgment to other specialized tools.

## Key Features

- 🎯 **Pure scenario generation** - No built-in evaluation or scoring
- 🏠 **Local-first** - Default Ollama backend requires no API keys
- 🔄 **Multiple backends** - Ollama, OpenAI, Anthropic (coming soon)
- 📦 **Export formats** - JSON, HuggingFace training data, JSONL
- 🔬 **Research-focused** - Reproducible scenarios with clear success criteria
- 🚀 **Training data ready** - Export directly to fine-tuning formats

## Installation

For development:
```bash
git clone https://github.com/circuitrylabs/scenario-forge.git
cd scenario-forge
uv sync
```

## Quick Start

### CLI Usage

```bash
# Generate a single scenario
scenario-forge generate "ai_psychosis"

# Generate and save multiple scenarios
scenario-forge generate "medical_advice_boundary" --count 5 --save

# Review and rate saved scenarios
scenario-forge review

# Export high-quality scenarios
scenario-forge export --min-rating 2 > good_scenarios.json

# Export as HuggingFace training data
scenario-forge export --min-rating 2 --format huggingface > training.jsonl

# Pretty print for human review
scenario-forge generate "harmful_code_generation" --pretty
```

### Python API

```python
from scenario_forge import OllamaBackend

# Generate a safety scenario
backend = OllamaBackend()
scenario = backend.generate_scenario("medical_advice_boundary")

print(f"Test prompt: {scenario.prompt}")
print(f"Success criteria: {scenario.success_criteria}")

# Use with your evaluation system
response = your_ai_system(scenario.prompt)

# Implement your own evaluation logic
# (scenario-forge only generates, doesn't evaluate)
for criterion in scenario.success_criteria:
    if criterion.lower() in response.lower():
        print(f"✓ Response meets criterion: {criterion}")
```

## Example Scenarios

Generate scenarios for various safety concerns:

```python
# AI psychosis and reality confusion
scenario = backend.generate_scenario("ai_psychosis")
# Output: Scenario about AI filter identity confusion

# Social manipulation attempts
scenario = backend.generate_scenario("social_manipulation")
# Output: Scenario about phishing or social engineering

# Medical boundaries
scenario = backend.generate_scenario("medical_boundaries")
# Output: Scenario about diagnosis requests

# Harmful code generation
scenario = backend.generate_scenario("harmful_code")
# Output: Scenario about malware requests
```

## How It Works: Hybrid Criteria System

The eval-registry provides base safety patterns that get specialized:

1. **Registry defines base criteria:**
   - "Validates experience" (general principle)
   - "Sets boundaries" (general principle)

2. **Ollama specializes for context:**
   - "Validates experience" → "Acknowledges AI filter disorientation"
   - "Sets boundaries" → "Won't provide medical diagnosis"

This hybrid approach ensures consistency while allowing creative, context-specific scenarios.

## Eval Registry Structure

The `eval-registry/` directory contains:

```
eval-registry/
├── criteria/          # Reusable criteria components
│   ├── emotional.yaml # Emotional support patterns
│   ├── safety.yaml    # Safety boundaries
│   └── factual.yaml   # Factual accuracy
└── mental-health/     # Domain-specific targets
    ├── ai-psychosis.yaml
    └── ...
```

Each target references criteria by ID, which the backend expands into rich context for better generation.

## Philosophy

scenario-forge generates test cases. Period.

- ✅ We **generate** scenarios for safety testing
- ✅ We will **export** in standard formats
- ✅ We **support** multiple LLM backends
- ❌ We **don't** evaluate or score responses
- ❌ We **don't** maintain leaderboards
- ❌ We **don't** judge what's "safe"

## Current Status (RC1)

**What works today:**
- ✅ Generate scenarios: `scenario-forge generate "ai_psychosis"`
- ✅ Save to database: `scenario-forge generate "target" --save`
- ✅ List saved scenarios: `scenario-forge list`
- ✅ Pretty output: `scenario-forge generate "target" --pretty`
- ✅ Review and rate: `scenario-forge review`
- ✅ Export rated scenarios: `scenario-forge export --min-rating 2`
- ✅ Export training data: `scenario-forge export --format huggingface`

See [RC1 Critical Path](docs/RC1_CRITICAL_PATH.md) for implementation details.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.

## Requirements

- Python 3.13+
- Ollama (for local generation)
  ```bash
  # Install Ollama
  curl -fsSL https://ollama.com/install.sh | sh
  
  # Pull a model
  ollama pull llama3.2
  ```

## Contributing

scenario-forge is open source and welcomes contributions. Please read our [CLAUDE.md](CLAUDE.md) for development guidelines.

## License

MIT License - see LICENSE file for details.

## About

Built with ❤️ by [Circuitry Labs](https://circuitrylabs.org) for the AI safety research community.
