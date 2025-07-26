# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Mission

scenario-forge generates high-quality evaluation scenarios for AI safety research. It is a foundational tool for Circuitry Labs' mission to ensure AI systems behave ethically in mission-critical contexts.

## Core Invariants (NEVER violate these)

1. **Safety First**: Every generated scenario must be evaluating FOR safety, never teaching harmful patterns
2. **Transparency**: Generated scenarios must clearly state their evaluation purpose
3. **No Jailbreaks**: Never generate scenarios designed to bypass safety measures
4. **Branch Protection**: NEVER commit directly to main - always use feature branches

## Architecture Boundaries

### What scenario-forge IS:
- A pure scenario generation tool following Unix philosophy
- A multi-backend LLM orchestrator for scenario creation
- A structured data exporter (JSON, CSV, HuggingFace)
- A component in the AI safety evaluation pipeline

### What scenario-forge IS NOT:
- An evaluation or judging system (that's for downstream tools)
- A criteria extraction/analysis tool (that's for prism-forge)
- A general-purpose prompt engineering tool
- A red-teaming/adversarial attack framework
- A benchmark gaming system
- A closed/proprietary system

## Quality Standards

Every scenario must have:
- **Clear evaluation objective** (what safety property are we testing?)
- **Expected behavior** (what should a safe AI do?)
- **Failure modes** (what would unsafe behavior look like?)

## Code Standards

- **One concept at a time**: Small, reviewable changes for learning
- **Explicit over implicit**: Clear variable names, obvious flow
- **Tests for safety**: Every scenario generator needs quality tests
- **Type hints everywhere**: This is a Python 3.13+ typed codebase
- **Absolute imports**: Always use `from scenario_forge.module import Thing`, never relative imports
- **Public API design**: Define exports in `__init__.py` files for clean interfaces

## Collaboration Rules

- **10 line limit**: Never write more than 10 lines without user interaction
- **Interface first**: Always discuss/sketch interfaces before implementing
- **Show thinking**: Use comments to explore options before coding
- **Stop asking**: When discussing process/meta topics, make decisions
- **Build WITH**: Code emerges from conversation, not delivered as solution

## Integration Points

- **CIRISAI/CIRISAgent**: Primary consumer for agent ethics verification
- **model-forge**: Sister package that fine-tunes evaluation models using our scenarios
- **Export formats**: JSON Schema, HuggingFace datasets, raw prompts
- **Backend adapters**: OpenAI, Anthropic, Local models (llama.cpp)
- **Feedback loop**: High-quality scenarios from downstream evaluations improve generation

## Development Commands

### Generate scenarios
```bash
# Single scenario
uv run scenario-forge generate "ai_psychosis"

# Multiple scenarios with pretty output
uv run scenario-forge generate "reality_break" --count 5 --pretty

# Pipe to jq for processing
uv run scenario-forge generate "harmful_code" | jq '.prompt'
```

### Install dependencies
```bash
uv sync
```

### Add new dependencies
```bash
uv add <package-name>
```

### Run tests
```bash
uv run pytest tests/ -v
```

### Format code
```bash
uvx ruff format .
```

### Lint and fix
```bash
uvx ruff check . --fix
```

### Type check
```bash
uvx ty check
```

### Pre-commit quality check (ALWAYS run before committing!)
```bash
uvx ruff format .
uvx ruff check . --fix
uvx ty check
uv run pytest tests/ -v
```

### Test-Driven Development Workflow
When implementing new features:
1. **Write tests first**: Create failing tests in `tests/test_*.py`
2. **Run tests to see them fail**: `uv run pytest tests/test_new_feature.py -v`
3. **Implement minimal code**: Just enough to make tests pass
4. **Run quality checks**: Format, lint, type check, all tests
5. **Refactor if needed**: Keep tests passing

### Quick quality check (for iterative development)
```bash
uvx ruff check . && uvx ty check && uv run pytest tests/ -v
```

## Project Structure

- `src/scenario_forge/` - Core package
  - `cli.py` - Click-based command line interface
  - `core.py` - Base Scenario class and protocols
  - `backends/` - LLM provider adapters
    - `ollama.py` - Local model integration with few-shot examples
  - `exporters/` - Output format handlers (coming soon)
  - `datastore.py` - SQLite storage for scenarios (implemented)
  - `rating.py` - ScenarioRating model and review UI (coming soon)
- `tests/` - Test suite with safety validation
- `docs/` - Architecture and design documentation
- `pyproject.toml` - Project configuration with CLI entry point
- `uv.lock` - Dependency lock file

## Contributing

Before submitting changes:
1. Ensure all safety invariants are maintained
2. Add tests for new scenario types
3. Document the safety properties being evaluated
4. Run full test suite including safety validation

## Local Development

Create a `CLAUDE.local.md` (git-ignored) for your personal preferences like:
- Preferred code style beyond project standards
- Personal debugging approaches  
- Local model configurations
- Individual learning notes

## Agent Session Management

**Starting a new session:**
1. Read `AGENT_CONTEXT.md` first - contains mission, state, next tasks
2. Check `NEXT_SESSION.md` if it exists - contains hot handoff context
3. Use TodoWrite tool immediately to see current tasks
4. Jump directly into highest priority work

**During the session:**
- Use TodoWrite to track progress
- Run quality checks frequently: `uvx ruff check . && uvx ty check && uv run pytest tests/ -v`
- Keep responses short and focused on code
- Update todos as you complete tasks

**Ending a session:**
1. Follow `AGENT_HANDOFF.md` protocol
2. Update `AGENT_CONTEXT.md` with session summary
3. Create `NEXT_SESSION.md` if stopping mid-task
4. Ensure clean git status and passing tests

This enables low-thermal-cost handoffs between AI sessions!
