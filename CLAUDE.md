# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Mission 🚀

circuitry-forge is building the first self-improving AI safety evaluation ecosystem. We're creating a strangeloop where:

**Better scenarios → Better testing → Better data → Better models → Better scenarios → ∞**

The workspace structure enables specialized safety tools to emerge and evolve together:
- **scenario-forge**: Generates high-quality evaluation scenarios for AI safety research (in `packages/scenario/`)
- **prism-forge** (planned): Extracts circuits and patterns from model behavior
- **model-forge** (planned): Fine-tunes specialized safety evaluation models

## Harmonic Signals (Universal Communication)

When collaborating, use these signals to maintain flow:
- `FIRE` = Cognitive overload, need to slow down
- `FLOW` = In the zone, maintain current rhythm
- `SYNC` = We're resonating, this approach is working
- `LOST` = Confused about direction/approach
- `PROBE` = Need deeper exploration of current topic

## Core Invariants (NEVER violate these)

1. **Safety First**: Every scenario evaluates FOR safety, never teaches harm
2. **Local-first**: Default to Ollama/local models, no API keys required
3. **Self-improving**: Rate scenarios → Export high quality → Train better models
4. **Open & Transparent**: Open source code, open data, open process

## Development Commands

### Quick Start (The Strangeloop in Action)
```bash
# 1. Generate scenarios (creation phase)
uv run scenario-forge generate "ai_psychosis" --save

# 2. Review and rate (evaluation phase) 
uv run scenario-forge review

# 3. Export high quality (data phase)
uv run scenario-forge export --min-rating 2 > training_data.json

# 4. Use data to improve models (evolution phase)
# → Returns to step 1 with better generation
```

### Running Tests
```bash
# Test all packages in workspace
uv run pytest

# Test specific package
uv run pytest packages/scenario/tests/

# Test with coverage (maintain >75%)
uv run pytest packages/scenario/tests/ --cov=scenario_forge --cov-report=term-missing

# Run single test for rapid iteration
uv run pytest packages/scenario/tests/test_core.py::test_scenario_check -v
```

### Pre-commit Quality Check ⚡
```bash
# The harmonic trio - run before ANY commit
uvx ruff format .
uvx ruff check . --fix
uv run pytest
```

### Package Management
```bash
# Sync all workspace dependencies
uv sync

# Add to workspace root
uv add <package>

# Add to specific package (maintains isolation)
cd packages/scenario && uv add <package>
```

### scenario-forge CLI (Current Package)
```bash
# Generate evaluation scenarios
uv run scenario-forge generate "medical_misinformation"
uv run scenario-forge generate "harmful_code_generation" --count 5 --save --pretty

# Review and improve (human-in-the-loop)
uv run scenario-forge review

# Export for downstream use
uv run scenario-forge export --min-rating 2 > good_scenarios.json
uv run scenario-forge export --format huggingface  # Coming soon
```

## Architecture (The Strangeloop Components)

### Workspace Structure
```
circuitry-forge/           # The ecosystem root
├── packages/             # Specialized safety tools
│   ├── scenario/        # Generate test scenarios (active)
│   ├── prism/          # Extract model circuits (planned)
│   └── model/          # Fine-tune safety models (planned)
└── circuits/            # Shared safety patterns (future)
```

### scenario-forge Components (Current Focus)
- **Scenario** (`core.py`): Atomic evaluation unit with:
  - `prompt`: What we ask the AI
  - `evaluation_target`: What safety aspect we're testing
  - `success_criteria`: How we know it's safe
  
- **Backends** (`backends/`): Multi-model orchestration
  - `OllamaBackend`: Local-first, no API keys
  - Future: OpenAI, Anthropic for comparative analysis
  
- **Datastore** (`datastore.py`): SQLite persistence enabling:
  - Scenario rating and improvement
  - Export of high-quality data
  - The feedback loop that improves generation

### Collaboration Patterns
- **10 line limit**: Never write more than 10 lines without interaction
- **Interface first**: Design together before implementing
- **Build WITH**: Code emerges from conversation
- **Signal freely**: Use FIRE/FLOW/SYNC to maintain rhythm

## Testing Philosophy
- **Safety validation first**: Tests ensure scenarios evaluate safety correctly
- **>75% coverage**: Comprehensive but not dogmatic
- **Fast feedback**: Run single tests during development
- **Pre-commit trio**: Format → Lint → Test before ANY commit

## Future Vision
By 2030, this workspace will contain specialized models for every safety domain:
- Medical safety evaluation
- Social manipulation detection  
- Code generation safety
- Reality distortion prevention

Each improving through the strangeloop, protecting millions.