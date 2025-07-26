# scenario-forge: Complete Development Context

## Mission
Build the first self-improving AI safety system that gets smarter every day by learning which scenarios actually find problems.

## How It Works

```
Generate → Test → Measure → Learn → Improve → Repeat
```

1. **Generate** scenarios using LLMs (Ollama default)
2. **Test** them on AI systems (yours or others)
3. **Measure** which scenarios found real issues
4. **Learn** patterns from effective scenarios
5. **Improve** by fine-tuning specialized models
6. **Repeat** with better generators each cycle

## Architecture

```
CLI → Backend (Ollama/OpenAI/etc) → Scenario → Store → Export
 ↓                                              ↓        ↓
User                                         SQLite   JSON/CSV
```

### Core Components
- `scenario_forge/core.py` - Base Scenario class
- `scenario_forge/backends/` - LLM integrations
- `scenario_forge/datastore.py` - SQLite persistence
- `scenario_forge/cli.py` - Command interface

### Data Flow
1. User requests scenario for target (e.g., "ai_psychosis")
2. Backend generates using examples + LLM
3. Scenario saved to SQLite if --save flag
4. Export for testing/sharing

## MVP 0.0 Scope (NOW)

### What We Have
- ✅ Core generation with Ollama
- ✅ SQLite storage with --save flag
- ✅ Test coverage + quality checks

### What We Need
1. **JSON Export** (next task)
   - Export saved scenarios for sharing
   - Format for downstream consumption

2. **Basic Review CLI** 
   - List saved scenarios
   - Add quality ratings
   - Mark effective ones

3. **YAML Target Registry**
   - Move hardcoded examples to YAML
   - Auto-discovery of new targets
   - Living examples that improve

### Development Flow
```bash
# 1. Write test first
uv run pytest tests/test_new_feature.py -v

# 2. Implement minimal code
# 3. Quality check
uvx ruff check . && uvx ty check && uv run pytest tests/ -v

# 4. Use it
scenario-forge generate "target" --save
```

## The Strangeloop (Future Vision)

### Phase 1: Collection (NOW)
Every generated scenario gets stored. Manual ratings show what works.

### Phase 2: Measurement (Q1 2025)
Track where scenarios are deployed and what they find.

### Phase 3: Fine-tuning (Q2 2025)
Train specialized models on effective scenarios:
- `forge-psychosis-v1` - Expert at reality distortion scenarios
- `forge-medical-v1` - Expert at health misinformation scenarios

### Phase 4: Self-Improvement (2026)
Models generate their own training examples, discovering new harm patterns.

## Integration Points

### Downstream (Who uses our scenarios)
- **Your AI system** - Test for safety issues
- **CIRISAgent** - Automated ethics verification
- **Researchers** - Build evaluation datasets

### Upstream (What makes us better)
- **Effectiveness scores** - Which scenarios found issues
- **New patterns** - Emerging harm categories
- **model-forge** - Fine-tuning pipeline (sister project)

## Commands

```bash
# Generate and save
scenario-forge generate "ai_psychosis" --save

# Generate multiple
scenario-forge generate "ai_psychosis" --count 10 --save

# Export (coming soon)
scenario-forge export --format json --min-rating 0.8

# Review (coming soon)
scenario-forge review

# Explore database
sqlite3 ~/.scenario-forge/scenarios.db
```

## Key Principles

1. **Do One Thing Well** - Generate scenarios, not evaluate
2. **Local First** - Your data, your control
3. **Progressive Enhancement** - Start simple, improve through use
4. **Open Source Forever** - Every line, every model

## Success Metrics

- **Now**: Generate quality scenarios
- **Q1 2025**: 1,000+ scenarios with ratings
- **Q2 2025**: First specialized model
- **2026**: 100,000+ scenarios, 10+ specialized models

---

*This is scenario-forge. Every scenario makes AI safer for someone.*