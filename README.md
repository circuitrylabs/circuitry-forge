# circuitry-forge

An AI safety evaluation ecosystem using UV workspaces. Building the first self-improving system where better scenarios lead to better models in an infinite loop.

**The Strangeloop**: Better scenarios → Better testing → Better data → Better models → Better scenarios → ∞

## Quick Start

```bash
# Clone the repository
git clone https://github.com/circuitrylabs/circuitry-forge.git
cd circuitry-forge

# Install dependencies with UV
uv sync

# Generate your first safety scenario
uv run scenario-forge generate "ai_psychosis" --save

# Review and rate scenarios
uv run scenario-forge review

# Export high-quality scenarios
uv run scenario-forge export --min-rating 2 > training_data.json
```

## Workspace Structure

This UV workspace contains specialized AI safety tools:

- **[scenario-forge](packages/scenario/)** - Generate test scenarios for AI safety evaluation (active)
- **prism-forge** - Extract model circuits and patterns (planned)
- **model-forge** - Fine-tune specialized safety models (planned)

## Development

### Prerequisites
- Python 3.13+
- [UV](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.com/) for local LLM inference

### Commands

```bash
# Run tests
uv run pytest

# Format code
uvx ruff format .

# Lint
uvx ruff check . --fix

# Type check
uvx ty

# Pre-commit check
uvx ruff format . && uvx ruff check . --fix && uv run pytest
```

### Adding a New Package

```bash
# Create package directory
mkdir -p packages/your-package/src/your_package

# Add to workspace
cd packages/your-package
uv init --package
```

## Mission

By 2030, circuitry-forge will be the foundation of AI safety testing worldwide - a living system that:

- **Evolves daily**: Every scenario generated makes the system smarter
- **Protects millions**: From AI psychosis to manipulation to misinformation
- **Empowers everyone**: Local-first, open source, no gatekeepers
- **Creates specialists**: Domain-specific models for every safety concern

## Contributing

We welcome contributions! Please read [CLAUDE.md](CLAUDE.md) for development guidelines and harmonic collaboration principles.

## License

MIT License - see [LICENSE](LICENSE) for details.

## About

Built by [Circuitry Labs](https://circuitrylabs.org) for the AI safety research community.

**Together, we make AI safe for everyone.**